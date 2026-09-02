# Ready-to-Use Prompts — SWĪKRIT

Copy-paste these into each tool along with the relevant document(s) attached.

---

## For Google Antigravity (Backend / Full-Stack Scaffolding)

Attach: `01_PRD.md`, `02_SYSTEM_ARCHITECTURE.md`, `03_API_SPECIFICATION.md`, `04_DATABASE_SCHEMA.md`

```
Build the backend for SWĪKRIT, a FastAPI application, following the attached
System Architecture, API Specification, and Database Schema documents exactly.

Requirements:
1. Implement all four endpoints from the API Specification with the exact
   request/response JSON shapes shown.
2. Use LangChain + ChromaDB for the RAG pipeline as described in the
   Architecture doc, Section 3 (Data Flow).
3. Use SQLAlchemy with async PostgreSQL support, matching the schema in
   04_DATABASE_SCHEMA.md exactly — create the migration/init script.
4. Implement the fallback strategy from Architecture doc Section 4:
   cache-first lookups, 8-second timeouts on AI calls, and a static JSON
   fallback response if any AI call times out.
5. Integrate three AI providers: Groq (LLaMA-3.3-70B) for roadmap generation,
   Anthropic Claude Haiku for document gap-audit reasoning, and Gemini 1.5
   Flash for native PDF ingestion. Read API keys from environment variables
   only — never hardcode.
6. Add CORS middleware allowing only the frontend origin (from an env var).
7. Include a requirements.txt and a README with local run instructions.

Do not use any deep learning model training — only API calls to hosted LLMs
and standard RAG retrieval. Keep the codebase readable for a team of
first/second-year engineering students.
```

---

## For Google Stitch (UI Generation)

Attach: `07_UI_UX_DESIGN_BRIEF.md`

```
Generate UI screens for SWĪKRIT, a Maharashtra government industrial
compliance platform, following the attached design brief exactly.

Generate these 4 screens in order:
1. Landing/input screen with the industry profile form
2. Roadmap visualization screen with a node-graph style layout
   (this will later be implemented with React Flow — style the nodes as
   rounded rectangles with department color-coding and dependency lines)
3. Clearance detail panel (slide-in drawer style)
4. Document upload and gap-audit results screen

Use the color palette and tone described in the brief: deep navy/indigo
primary, amber accent for critical-path/high-severity items, clean sans-serif
typography. This is a serious institutional tool, not a playful consumer app.
Desktop-first design at 1440px width.
```

---

## For Cursor (Frontend Implementation)

Attach: `05_TECH_STACK.md`, `03_API_SPECIFICATION.md`, Stitch-exported design screens/images

```
Implement the SWĪKRIT frontend in React + Vite + Tailwind CSS, using the
attached Stitch design screens as the visual reference and the API
Specification for backend integration.

Key requirements:
1. Use React Flow for the roadmap visualization screen — build actual
   interactive nodes and edges from the /api/roadmap response shape shown
   in the API spec, not a static image. Nodes should be draggable, and
   clicking a node should open the clearance detail panel by calling
   /api/clearance/{id}.
2. Use ShadCN/UI components for forms, modals, and buttons where it speeds
   up development, styled to match the Stitch design's navy/amber palette.
3. Use Framer Motion for the roadmap-generation loading state — a progress
   indicator, not a generic spinner.
4. Implement the document upload screen with drag-and-drop, calling
   POST /api/audit as a multipart form request.
5. All backend calls go through Axios with the base URL read from
   VITE_API_BASE_URL environment variable — never hardcode the backend URL.
6. Handle loading, error, and empty states for every screen.
7. Keep components modular: separate files for RoadmapGraph, ClearanceDetail,
   DocumentAudit, and IndustryProfileForm.

Build this to deploy cleanly on Vercel with zero extra configuration.
```

---

## General Tip for All Three Tools

When you attach multiple documents to a single tool, always tell it explicitly
which document governs which decision (e.g. "follow the API spec exactly for
JSON shapes, follow the design brief for visual style only — don't let visual
mockups override the data structure"). AI coding tools sometimes blend
conflicting instructions from different documents if you don't rank them.
