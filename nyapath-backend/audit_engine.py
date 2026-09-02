import os
import uuid
import tempfile
import fitz  # PyMuPDF
from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class GapItem(BaseModel):
    clearance_id: str = Field(description="The ID of the clearance this document relates to (e.g. clr_001)")
    document_name: str = Field(description="Name of the uploaded document")
    issue: str = Field(description="Description of the missing or non-compliant information")
    severity: str = Field(description="Severity of the gap: low, medium, or high")
    recommendation: str = Field(description="Actionable advice to fix the issue")

class AuditOutput(BaseModel):
    gaps: List[GapItem] = Field(description="List of detected compliance gaps")
    compliant_count: int = Field(description="Number of compliant aspects found")
    gap_count: int = Field(description="Total number of gaps found")

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from a given PDF file."""
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    return text

def _normalize_audit(result: dict) -> dict:
    """Coerce LLM audit output into the shape the frontend renders.

    The UI maps over result.gaps and reads five string fields off each item, so a
    missing key or a non-list `gaps` would throw in React, not here. Fix it at the
    boundary and recompute the counts rather than trusting the model's arithmetic.
    """
    gaps = result.get("gaps")
    if not isinstance(gaps, list):
        gaps = []
    clean = []
    for g in gaps:
        if not isinstance(g, dict):
            continue
        sev = str(g.get("severity") or "medium").strip().lower()
        clean.append({
            "clearance_id": str(g.get("clearance_id") or ""),
            "document_name": str(g.get("document_name") or "Uploaded document"),
            "issue": str(g.get("issue") or "Unspecified gap"),
            "severity": sev if sev in ("low", "medium", "high", "critical") else "medium",
            "recommendation": str(g.get("recommendation") or ""),
        })
    result["gaps"] = clean
    result["gap_count"] = len(clean)
    try:
        result["compliant_count"] = max(0, int(result.get("compliant_count") or 0))
    except (TypeError, ValueError):
        result["compliant_count"] = 0
    return result


def run_document_audit(roadmap_id: str, uploaded_files_data: list) -> dict:
    """
    uploaded_files_data: list of dicts with 'filename' and 'filepath'
    """
    # 1. Extract all text
    combined_text = ""
    unreadable = []
    for file_info in uploaded_files_data:
        extracted = extract_text_from_pdf(file_info['filepath'])
        if not extracted.strip():
            # fitz raises on non-PDF input (docx, images, scans with no text
            # layer) and we swallow it above. Without this check the LLM would be
            # asked to audit an empty string and would invent plausible gaps.
            unreadable.append(file_info['filename'])
            continue
        combined_text += f"\n--- Document: {file_info['filename']} ---\n"
        combined_text += extracted

    if not combined_text.strip():
        return {
            "audit_id": f"au_{uuid.uuid4().hex[:5]}",
            "roadmap_id": roadmap_id,
            "documents_analyzed": len(uploaded_files_data),
            "gaps": [{
                "clearance_id": "",
                "document_name": ", ".join(unreadable) or "(none)",
                "issue": "No readable text could be extracted. Only text-based PDFs are supported; "
                         "scanned images and Word files need to be converted or OCR'd first.",
                "severity": "high",
                "recommendation": "Re-upload each document as a text-based PDF.",
            }],
            "compliant_count": 0,
            "gap_count": 1,
            "sources": [],
        }

    # 2. Setup LLM — shared factory so the Groq model id lives in exactly one place
    # (rag_engine.GROQ_MODEL). This module used to hardcode its own copy, which is
    # how it ended up pointing at a decommissioned model while the roadmap worked.
    from rag_engine import get_llm, retrieve_context
    llm = get_llm()

    # Ground the audit in the ingested regulation PDFs instead of the model's memory.
    # Best-effort: retrieve_context() swallows its own errors and returns ("", []).
    reg_context, sources = retrieve_context(
        "Required annexures, forms and compliance conditions for: "
        + " ".join(combined_text.split())[:600]
    )
    if not reg_context.strip():
        reg_context = "(No regulatory excerpts retrieved. Rely on general Maharashtra compliance knowledge.)"

    parser = JsonOutputParser(pydantic_object=AuditOutput)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert compliance auditor for Maharashtra industrial regulations. "
                   "Analyze the provided document text against standard required clearances (like MPCB Consent, MIDC Land, Fire Safety NOC). "
                   "Identify any missing annexures, incomplete forms, or regulatory gaps. "
                   "Prefer issues you can justify from the regulatory context below. "
                   "Return ONLY valid JSON matching the schema.\n\n{format_instructions}\n\n"
                   "REGULATORY CONTEXT:\n{reg_context}"),
        ("human", "Uploaded Documents Text:\n{document_text}\n\nPerform a gap analysis.")
    ])

    chain = prompt | llm | parser

    try:
        result = chain.invoke({
            "document_text": combined_text[:20000],  # Limit to avoid context overflow
            "reg_context": reg_context,
            "format_instructions": parser.get_format_instructions()
        })

        result = _normalize_audit(result)
        result["audit_id"] = f"au_{uuid.uuid4().hex[:5]}"
        result["roadmap_id"] = roadmap_id
        result["documents_analyzed"] = len(uploaded_files_data)
        result["sources"] = sources
        if unreadable:
            # Say so explicitly. A silently-skipped scan looks identical to a clean
            # document in the UI otherwise.
            result["gaps"].insert(0, {
                "clearance_id": "",
                "document_name": ", ".join(unreadable),
                "issue": "No readable text could be extracted, so this file was not audited.",
                "severity": "high",
                "recommendation": "Re-upload as a text-based PDF (scans need OCR first).",
            })
            result["gap_count"] = len(result["gaps"])

        return result
    except Exception as e:
        print(f"Audit generation failed: {e}")
        return {
            "audit_id": f"au_{uuid.uuid4().hex[:5]}",
            "roadmap_id": roadmap_id,
            "documents_analyzed": len(uploaded_files_data),
            "gaps": [],
            "compliant_count": 0,
            "gap_count": 0,
            "error": str(e),
        }
