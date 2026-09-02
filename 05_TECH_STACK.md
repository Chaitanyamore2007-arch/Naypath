# Tech Stack — SWĪKRIT

## Frontend
| Tool | Purpose |
|---|---|
| React 18 + Vite | Core framework, fast dev server |
| Tailwind CSS | Styling |
| ShadCN/UI | Pre-built accessible components (forms, dialogs) |
| React Flow | Interactive compliance roadmap graph — the demo centerpiece |
| Framer Motion | Loading animations, transitions |
| Axios | API calls to backend |
| React Hook Form + Zod | Form handling + validation |

## Backend
| Tool | Purpose |
|---|---|
| FastAPI (Python 3.11+) | REST API framework |
| LangChain | RAG orchestration, prompt chaining |
| ChromaDB | Vector store for regulation embeddings |
| Uvicorn | ASGI server |
| PyPDF / PyMuPDF | PDF text extraction fallback (if not using Gemini native PDF) |
| SQLAlchemy + asyncpg | PostgreSQL ORM |
| python-dotenv | Environment variable management |

## AI / LLM Layer
| Model | Use Case |
|---|---|
| Groq (LLaMA-3.3-70B) | Fast roadmap generation, general queries |
| Claude Haiku 4.5 (Anthropic API) | Document gap-audit reasoning (accuracy-critical) |
| Gemini 1.5 Flash | Native PDF document ingestion |
| Tavily Search API | Real-time lookup for regulations not in local knowledge base |

## Database & Storage
- PostgreSQL (hosted on Render)
- ChromaDB (local persistent storage within backend container/disk)

## Deployment
| Layer | Platform | Notes |
|---|---|---|
| Frontend | Vercel | Auto-deploys from GitHub main branch |
| Backend | Render | Web Service, auto-deploys from GitHub |
| Database | Render PostgreSQL | Free tier instance |

## Dev Tools (as you specified)
| Tool | Role in your workflow |
|---|---|
| Google Antigravity | Agentic build tool — feed it the PRD + Architecture + API spec docs to scaffold backend/full-stack logic |
| Cursor | AI-assisted code editor — use for frontend implementation, especially React Flow logic and Tailwind styling |
| Google Stitch | AI UI design tool — generate initial screen mockups/wireframes before implementing in code |

## Suggested Additions
| Tool | Why |
|---|---|
| GitHub | Version control — required for Vercel/Render auto-deploy pipelines |
| Postman or Thunder Client | Test backend API endpoints independently before frontend integration |
| Figma (optional, free) | If Stitch output needs manual refinement before dev handoff |
