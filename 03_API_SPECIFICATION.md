# API Specification — SWĪKRIT Backend

Base URL (local): `http://localhost:8000/api`
Base URL (production): `https://<your-render-app>.onrender.com/api`

All requests/responses are JSON. All endpoints are prefixed with `/api`.

---

## 1. POST `/api/roadmap`

Generates a compliance roadmap for a given industry profile.

**Request body:**
```json
{
  "industry_type": "pharmaceutical manufacturing",
  "district": "Pune",
  "investment_scale_crores": 50,
  "unit_size": "large",
  "existing_land": false
}
```

**Response body (200 OK):**
```json
{
  "roadmap_id": "rm_8f2a1c",
  "generated_at": "2026-09-01T10:00:00Z",
  "total_estimated_days": 240,
  "clearances": [
    {
      "id": "clr_001",
      "name": "MIDC Land Allotment",
      "department": "MIDC",
      "sequence_order": 1,
      "depends_on": [],
      "estimated_days": 45,
      "estimated_fee_inr": 250000,
      "is_critical_path": true,
      "required_documents": ["Form-1", "Site plan"],
      "common_rejection_reasons": ["Incomplete Form-1"]
    },
    {
      "id": "clr_002",
      "name": "MPCB Consent to Establish",
      "department": "Maharashtra Pollution Control Board",
      "sequence_order": 2,
      "depends_on": ["clr_001"],
      "estimated_days": 60,
      "estimated_fee_inr": 180000,
      "is_critical_path": true,
      "required_documents": ["Form-1", "Site plan"],
      "common_rejection_reasons": ["Incomplete Form-1"]
    }
  ]
}
```

**Error response (422/500):**
```json
{ "error": "invalid_industry_type", "message": "Industry type not recognized in knowledge base." }
```

---

## 2. POST `/api/audit`

Analyzes uploaded document(s) against required regulations for gap detection.

**Request:** `multipart/form-data`
- `files`: one or more PDF files (max 3, max 10MB each)
- `roadmap_id`: string (links audit to a previously generated roadmap)

**Response body (200 OK):**
```json
{
  "audit_id": "au_3d9b2",
  "roadmap_id": "rm_8f2a1c",
  "documents_analyzed": 2,
  "gaps": [
    {
      "clearance_id": "clr_001",
      "document_name": "factory_plan.pdf",
      "issue": "Missing environmental clearance annexure",
      "severity": "high",
      "recommendation": "Attach Form-1 environmental annexure per MPCB guideline 4.2"
    }
  ],
  "compliant_count": 3,
  "gap_count": 1
}
```

---


## 3. POST `/api/chat`

RAG-grounded chatbot answering compliance questions using local ChromaDB and Llama.

**Request body:**
```json
{
  "question": "What is the fire safety norm?",
  "profile": {
    "industry_type": "Pharma",
    "district": "Pune",
    "investment_scale_crores": 50,
    "unit_size": "large",
    "existing_land": false
  },
  "history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi!"}
  ]
}
```

**Response body (200 OK):**
```json
{
  "answer": "According to the Maharashtra Fire Prevention Act...",
  "sources": [
    {"document": "Fire_Safety_Act.pdf", "page": 4, "excerpt": "Storage exceeding 500 sq meters requires..."}
  ]
}
```

---

## 4. POST `/api/schemes`

Matches the user's project profile with applicable state subsidies and incentives.

**Request body:**
```json
{
  "industry_type": "pharmaceutical manufacturing",
  "district": "Pune",
  "investment_scale_crores": 50,
  "unit_size": "large",
  "existing_land": false
}
```

**Response body (200 OK):**
```json
{
  "schemes": [
    {
      "name": "Package Scheme of Incentives (PSI) 2019",
      "benefit": "100% SGST Refund for 10 years",
      "match_level": "high",
      "tags": ["Tax", "Subsidy"],
      "eligibility_note": "As a new unit in a developing zone, you are fully eligible."
    }
  ]
}
```

---

## 5. GET `/api/health`

Simple uptime check.

**Response (200 OK):**
```json
{ "status": "ok", "timestamp": "2026-09-01T10:00:00Z" }
```

---

## Rate Limiting & Timeouts

- All AI-dependent endpoints (`/roadmap`, `/audit`) must implement an 8-second timeout with fallback to cached/static data (see Architecture doc, Section 4)
- Recommended: wrap AI calls with `asyncio.wait_for()` in FastAPI

## Environment Variables Required

```
GROQ_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
TAVILY_API_KEY=
DATABASE_URL=
CHROMA_PERSIST_DIR=./chroma_data
CORS_ALLOWED_ORIGIN=https://your-app.vercel.app
```
