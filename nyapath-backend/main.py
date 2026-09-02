from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from contextlib import asynccontextmanager
import uuid
import datetime

import os

import models
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the embedding model and open ChromaDB before serving traffic, so the
    # first /api/roadmap of a demo isn't the one that pays the cold-start cost.
    try:
        import rag_engine
        rag_engine.warm_retriever()
        print("RAG retriever warmed.")
    except Exception as e:
        print(f"RAG warm-up skipped ({e}). Roadmaps will run ungrounded.")
    yield


app = FastAPI(
    title="Nyapath API",
    description="Maharashtra Industrial Compliance Intelligence Engine",
    lifespan=lifespan,
)

# Any localhost/127.0.0.1 port covers Vite whichever port it picks (5173, 5174, ...)
# without falling back to a wildcard. Set CORS_ALLOWED_ORIGIN to the Vercel URL on deploy.
_allowed_origins = [o.strip() for o in os.getenv("CORS_ALLOWED_ORIGIN", "").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    # No cookies or Authorization header are used. Keep this False: the CORS spec
    # forbids credentials alongside a wildcard origin, and enabling it here would
    # break the browser request the moment a wildcard crept back in.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Schemas ---
class RoadmapRequest(BaseModel):
    industry_type: str
    district: str
    investment_scale_crores: float
    unit_size: str
    existing_land: bool

class ClearanceDetail(BaseModel):
    id: str
    name: str
    department: str
    sequence_order: int
    depends_on: List[str]
    estimated_days: int
    estimated_fee_inr: float
    is_critical_path: bool
    # response_model *filters* the dict rag_engine returns, so anything not declared
    # here is silently dropped on the way out. These two are generated per clearance
    # and are what the detail panel shows instead of its old hardcoded copy.
    required_documents: List[str] = []
    common_rejection_reasons: List[str] = []

class RoadmapResponse(BaseModel):
    roadmap_id: str
    generated_at: str
    total_estimated_days: int
    clearances: List[ClearanceDetail]

class ChatTurn(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    question: str
    # The profile is optional so the assistant still answers before a roadmap exists.
    profile: Optional[RoadmapRequest] = None
    history: List[ChatTurn] = []

class SchemeRequest(BaseModel):
    industry_type: str
    district: str
    investment_scale_crores: float
    unit_size: str
    existing_land: bool = False

# --- Routes ---

@app.get("/api/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.datetime.utcnow().isoformat()}

@app.post("/api/roadmap", response_model=RoadmapResponse)
def generate_roadmap(req: RoadmapRequest, db: Session = Depends(get_db)):
    """
    Generates a compliance roadmap for a given industry profile using Groq/Langchain.
    """
    import rag_engine
    
    result = rag_engine.generate_roadmap_with_llm(
        industry_type=req.industry_type,
        district=req.district,
        investment_scale_crores=req.investment_scale_crores,
        unit_size=req.unit_size,
        existing_land=req.existing_land
    )
    
    if not result:
        raise HTTPException(status_code=500, detail="Failed to generate AI roadmap")
        
    return result

@app.post("/api/audit")
async def audit_documents(roadmap_id: str, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    """
    Analyzes uploaded documents against required regulations for gap detection using LLM.
    """
    import audit_engine
    import shutil
    import tempfile
    import os

    uploaded_files_data = []
    temp_dir = tempfile.mkdtemp()

    try:
        # Save uploaded files to temp directory
        for file in files:
            # basename() only: the client controls filename, and a value like
            # "..\\..\\evil.py" would otherwise resolve outside temp_dir.
            safe_name = os.path.basename(file.filename or "") or f"upload_{uuid.uuid4().hex[:8]}"
            file_path = os.path.join(temp_dir, safe_name)
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            uploaded_files_data.append({"filename": safe_name, "filepath": file_path})

        # Run the audit engine
        result = audit_engine.run_document_audit(roadmap_id, uploaded_files_data)
        return result
    finally:
        # rmtree, not rmdir: a partially-written directory would otherwise raise
        # from the finally block and mask the real error.
        shutil.rmtree(temp_dir, ignore_errors=True)

@app.post("/api/chat")
def chat_with_assistant(req: ChatRequest, db: Session = Depends(get_db)):
    """
    RAG-grounded chatbot.
    """
    import chat_engine
    
    # Pass profile as dict if it exists
    profile_dict = req.profile.model_dump() if req.profile else None
    history_list = [turn.model_dump() for turn in req.history]
    
    return chat_engine.run_chat(req.question, profile_dict, history_list)

@app.post("/api/schemes")
def match_schemes(req: SchemeRequest, db: Session = Depends(get_db)):
    """
    Finds applicable incentives based on profile.
    """
    import schemes_engine
    
    return schemes_engine.run_schemes_matcher(req.model_dump())
