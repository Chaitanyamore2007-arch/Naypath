import os
import json
import uuid
import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")

# One place to change the model. Groq deprecates model ids fairly often, and having
# the same string copied into three modules is how two of them end up stale.
#
# History that matters for this repo: llama-3.1-70b-versatile was decommissioned long
# ago, and llama-3.3-70b-versatile was deprecated 2026-06-17 and shut down for
# Free/Developer tiers on 2026-08-16 — i.e. before today. Groq points new traffic at
# openai/gpt-oss-120b, so that is the default. If a call ever fails with
# "model_decommissioned", check https://console.groq.com/docs/deprecations and set
# GROQ_MODEL in .env rather than editing code.
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


def get_llm(temperature: float = 0.1):
    return ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model=GROQ_MODEL, temperature=temperature)


# FastEmbed loads a ~130MB ONNX model the first time it is constructed, and
# Chroma re-opens the sqlite + HNSW segments on every construction. Doing that
# inside the request handler meant every /api/roadmap call paid the cost, and a
# cold first call can exceed the frontend's 20s axios timeout. Build once per
# process instead; warm_retriever() lets the server pay it at startup.
_retriever = None


def warm_retriever():
    """Build (or return) the process-wide retriever. Safe to call repeatedly."""
    global _retriever
    if _retriever is None:
        from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
        from langchain_community.vectorstores import Chroma

        embeddings = FastEmbedEmbeddings()
        vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
        _retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    return _retriever


def retrieve_context(query: str, k: int = 5):
    """Returns (context_text, sources). Never raises — retrieval is best-effort."""
    try:
        docs = warm_retriever().invoke(query)
    except Exception as e:
        # A missing/corrupt chroma_data or an uninstalled fastembed should degrade
        # to an ungrounded answer, not a 500 that blanks the UI mid-demo.
        print(f"Retrieval unavailable, continuing without RAG context: {e}")
        return "", []

    context_text = "\n\n".join(d.page_content for d in docs)
    sources = []
    for d in docs:
        raw = d.metadata.get("source", "regulation")
        # Chroma stores the ingest-time path ("./regulations\\MPCB_Guidelines_2026.pdf"),
        # and it is a Windows path, so split on both separators.
        name = raw.replace("\\", "/").rstrip("/").split("/")[-1]
        sources.append({
            "document": name,
            "page": d.metadata.get("page"),
            "excerpt": " ".join(d.page_content.split())[:220],
        })
    return context_text, sources


# We use Pydantic models to define the exact JSON structure we want Groq to return
class ClearanceNode(BaseModel):
    id: str = Field(description="Unique ID like clr_001")
    name: str = Field(description="Name of the clearance or NOC")
    department: str = Field(description="Department issuing the clearance")
    sequence_order: int = Field(description="Order in which this should be applied (1, 2, 3...)")
    depends_on: List[str] = Field(description="List of IDs of clearances that must be obtained before this one")
    estimated_days: int = Field(description="Estimated days to obtain")
    estimated_fee_inr: float = Field(description="Estimated fee in INR")
    is_critical_path: bool = Field(description="True if this is a blocking clearance for setup")
    required_documents: List[str] = Field(
        default_factory=list,
        description="3 to 5 specific documents the applicant must submit for this clearance",
    )
    common_rejection_reasons: List[str] = Field(
        default_factory=list,
        description="1 to 3 concrete reasons applications for this clearance are commonly rejected",
    )

class RoadmapOutput(BaseModel):
    total_estimated_days: int = Field(description="Total estimated days for all clearances")
    clearances: List[ClearanceNode] = Field(description="List of required clearances")


def _normalize_clearances(result: dict) -> dict:
    """Coerce LLM output into the shape FastAPI's response_model will accept.

    Pydantic v2 does not coerce int -> str, so an LLM that answers
    "id": 1 / "depends_on": [1] would fail response validation and turn a good
    roadmap into a 500. Stringify ids and default the list fields here instead.
    """
    clearances = result.get("clearances") or []
    for i, c in enumerate(clearances, start=1):
        c["id"] = str(c.get("id") or f"clr_{i:03d}")
        c["depends_on"] = [str(d) for d in (c.get("depends_on") or [])]
        c["required_documents"] = [str(d) for d in (c.get("required_documents") or [])]
        c["common_rejection_reasons"] = [str(r) for r in (c.get("common_rejection_reasons") or [])]
        c["sequence_order"] = int(c.get("sequence_order") or 1)
        c["estimated_days"] = max(0, int(c.get("estimated_days") or 0))
        c["estimated_fee_inr"] = max(0.0, float(c.get("estimated_fee_inr") or 0))
        c["is_critical_path"] = bool(c.get("is_critical_path"))
    result["clearances"] = clearances
    if not result.get("total_estimated_days"):
        result["total_estimated_days"] = sum(c["estimated_days"] for c in clearances)
    return result


def generate_roadmap_with_llm(industry_type: str, district: str, investment_scale_crores: float, unit_size: str, existing_land: bool):
    """
    Calls Groq LLaMA-3 to generate the compliance roadmap using context from ChromaDB.
    """
    # 1. Retrieve grounding context from ChromaDB.
    search_query = f"Regulations for {industry_type} industry in {district} Maharashtra, investment {investment_scale_crores} crores."
    context_text, _sources = retrieve_context(search_query)
    if not context_text.strip():
        context_text = "(No regulatory excerpts retrieved. Rely on general Maharashtra compliance knowledge.)"

    # 2. Setup LLM
    llm = get_llm()

    parser = JsonOutputParser(pydantic_object=RoadmapOutput)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert industrial compliance consultant for Maharashtra, India. "
                   "Generate a realistic sequence of required NOCs, licenses, and clearances for the user's project. "
                   "Use the provided regulatory context to inform your answer. "
                   "Ensure dependencies make logical sense (e.g., Company Incorporation before Land Allotment, Land before Factory License). "
                   "For every clearance also list the specific documents required and the reasons applications "
                   "of that type are commonly rejected. Keep each string under 90 characters. "
                   "Return ONLY valid JSON matching the requested schema.\n\n{format_instructions}\n\n"
                   "REGULATORY CONTEXT:\n{context}"),
        ("human", "Project Details:\n"
                  "- Industry: {industry_type}\n"
                  "- District: {district}, Maharashtra\n"
                  "- Investment: {investment_scale_crores} Crores INR\n"
                  "- Unit Size: {unit_size}\n"
                  "- Has Existing Land: {existing_land}\n\n"
                  "What clearances do I need?")
    ])
    
    chain = prompt | llm | parser
    
    try:
        result = chain.invoke({
            "context": context_text,
            "industry_type": industry_type,
            "district": district,
            "investment_scale_crores": investment_scale_crores,
            "unit_size": unit_size,
            "existing_land": existing_land,
            "format_instructions": parser.get_format_instructions()
        })
        
        # Coerce types before FastAPI's response_model sees them.
        result = _normalize_clearances(result)

        # Add backend metadata
        result["roadmap_id"] = f"rm_{uuid.uuid4().hex[:6]}"
        result["generated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
        
        return _normalize_clearances(result)
    except Exception as e:
        print(f"Error generating roadmap: {e}")
        return None
