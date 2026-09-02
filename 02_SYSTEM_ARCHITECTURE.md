# System Architecture — SWĪKRIT

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser)                       │
│   React + Vite + Tailwind + React Flow + Framer Motion        │
│   Hosted on: Vercel                                            │
└───────────────────────────┬─────────────────────────────────┘
                             │ HTTPS / REST (JSON)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND API (FastAPI)                      │
│                    Hosted on: Render                           │
│  ┌───────────────┐  ┌────────────────┐  ┌──────────────────┐ │
│  │ /profile       │  │ /audit-docs    │  │ /clearance/{id}  │ │
│  │ (roadmap gen)  │  │ (gap analysis) │  │ (detail lookup)  │ │
│  └───────┬────────┘  └───────┬────────┘  └──────────────────┘ │
└──────────┼───────────────────┼─────────────────────────────────┘
           ▼                   ▼
┌──────────────────┐  ┌──────────────────┐
│  LangChain RAG    │  │  Doc Extraction   │
│  Orchestration    │  │  Layer            │
└─────────┬─────────┘  └─────────┬─────────┘
          ▼                      ▼
┌──────────────────┐  ┌──────────────────┐    ┌────────────────┐
│  ChromaDB          │  │  Gemini 1.5 Flash │    │  Groq LLaMA-3.3 │
│  (regulation        │  │  (PDF ingestion)   │    │  (fast roadmap  │
│  vector store)      │  │                    │    │  generation)    │
└──────────────────┘  └──────────────────┘    └────────────────┘
                                                        │
                                              ┌────────────────┐
                                              │  Claude Haiku    │
                                              │  (gap audit       │
                                              │  reasoning)        │
                                              └────────────────┘
          │
          ▼
┌──────────────────┐
│  PostgreSQL        │
│  (sessions,         │
│  saved roadmaps)    │
│  Hosted on: Render  │
└──────────────────┘
```

## 2. Component Responsibilities

### Frontend (Vercel)
- Renders industry profile form
- Renders React Flow compliance roadmap graph
- Handles PDF upload UI
- Renders gap audit report and Gantt timeline
- Calls backend REST API only — no direct AI API calls from client (keeps API keys server-side)

### Backend API (Render — FastAPI)
- `/api/roadmap` (POST): accepts industry profile, returns structured JSON roadmap
- `/api/audit` (POST): accepts uploaded PDF(s) + industry context, returns gap report JSON
- `/api/clearance/{clearance_id}` (GET): returns static detail data for a specific clearance node
- `/api/health` (GET): health check for uptime monitoring

### RAG Layer (LangChain + ChromaDB)
- ChromaDB stores pre-chunked, pre-embedded Maharashtra regulatory documents
- On `/api/roadmap` call: query ChromaDB with industry type + district → retrieve relevant regulation chunks → pass to Groq LLM with a structured-output prompt → return JSON list of required clearances with sequencing

### Document Audit Layer (Gemini 1.5 Flash + Claude Haiku)
- Gemini 1.5 Flash: extracts structured content directly from uploaded PDF (native PDF understanding, no separate OCR step needed)
- Claude Haiku: compares extracted content against the relevant regulation chunks retrieved from ChromaDB, produces gap report as structured JSON

### Database (PostgreSQL on Render)
- `sessions` table: stores each demo/user session for later retrieval
- `roadmaps` table: caches generated roadmaps by profile hash (also serves as your demo-day fallback cache)

## 3. Data Flow — Roadmap Generation (Primary Demo Flow)

1. User submits profile (industry, district, investment scale) via frontend form
2. Frontend POSTs to `/api/roadmap`
3. Backend checks PostgreSQL cache for identical profile hash — if hit, returns instantly (this is your demo-day safety net)
4. If cache miss: backend queries ChromaDB for relevant regulation chunks
5. Chunks + profile are passed to Groq LLaMA-3.3-70B with a structured JSON output prompt
6. Backend validates the JSON structure, assigns sequencing/dependencies between clearances
7. Result is cached in PostgreSQL and returned to frontend
8. Frontend renders the roadmap as a React Flow graph, color-coded by department

## 4. Fallback Strategy (Critical for Live Demo)

AI APIs can fail or rate-limit during a live demo in front of judges. Build these safeguards:

- **Cache-first for the exact demo query**: run your demo scenario once before presenting and let it cache in PostgreSQL. On demo day, if the live call fails, the cached response returns instantly and looks identical.
- **Timeout + static fallback**: if any AI API call exceeds 8 seconds, backend returns a pre-defined static JSON roadmap for that industry type rather than hanging on stage.
- **Local demo backup**: keep a fully offline version of the frontend with hardcoded JSON responses (no backend calls) as an absolute last resort if venue wifi fails entirely.

## 5. Security Notes

- All AI API keys live only in backend environment variables — never exposed to frontend
- CORS configured to only allow the deployed Vercel frontend origin
- No user authentication required for MVP (no login) — reduces scope and attack surface
- Uploaded PDFs are processed in-memory and not persisted to disk beyond the session (no compliance/privacy concerns since no real applicant data is involved in demo)
