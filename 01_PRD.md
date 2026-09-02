# PRD — SWĪKRIT
### Maharashtra Industrial Compliance Intelligence Engine
**SIH 2026 | Problem Statement SIH26130 | Government of Maharashtra**

---

## 1. Problem Statement

Industrial approvals in Maharashtra require entrepreneurs to navigate multiple departments (Pollution Control Board, MIDC, Fire Department, Factories Act authorities, local municipal bodies) with no unified view of the full compliance journey. Applicants discover requirements sequentially, causing rejection loops, delays of 3–6 months, and lost investment confidence — directly hurting Maharashtra's Ease of Doing Business (EoDB) ranking.

## 2. Vision Statement

SWĪKRIT gives an industrialist their complete, personalised compliance roadmap in under 15 seconds — before they submit a single document — by combining a structured regulatory knowledge graph with AI-driven document auditing.

## 3. Target Users

| User | Need |
|---|---|
| First-time industrial applicant | Doesn't know which departments to approach or in what order |
| SME owner expanding operations | Needs to know incremental compliance for new units |
| Government approval officer (secondary) | Wants a dashboard view of pending applications and bottlenecks |

## 4. Core User Stories

1. As an entrepreneur, I enter my industry type, district, and investment scale, and receive a visual roadmap of every required clearance in the correct sequence.
2. As an entrepreneur, I upload my existing documents (factory plan, land deed) and receive a gap report showing exactly what's missing or non-compliant before I submit anywhere.
3. As an entrepreneur, I click any clearance node to see required documents, fees, estimated timeline, and the responsible department's contact details.
4. As an entrepreneur, I see a Gantt-style timeline showing the critical path and total estimated approval duration.
5. (Stretch) As a government officer, I view aggregate data on which clearances cause the most delays statewide.

## 5. Scope — MVP (36-Hour Hackathon Build)

**In scope:**
- Industry profile input form (type, district, investment scale, unit size)
- AI-generated compliance roadmap (React Flow visual graph)
- Document upload + AI gap audit (PDF only, max 3 documents)
- Clearance detail panel (documents, fees, timeline, department contact)
- Gantt-style critical path timeline view
- Regulatory knowledge base covering 4 core departments: MPCB (Pollution), MIDC (Land), Fire NOC, Factories Act licensing

**Out of scope for MVP (mention as "roadmap" in pitch):**
- Real-time application status tracking (requires government API integration — not available to us)
- Multi-language support (Marathi/Hindi) — mention as Phase 2
- Payment gateway integration for fees
- Officer-side dashboard (only mock/stub for demo)
- Mobile native app

## 6. Success Metrics (for judges)

- Roadmap generation time: under 15 seconds
- Coverage: minimum 4 departments, 10+ distinct clearance types modeled
- Document audit accuracy: correctly flags at least 3 realistic gap scenarios in demo
- Demo completion: full flow (input → roadmap → document audit → gap report) in under 3 minutes

## 7. Non-Functional Requirements

- Must run on a live URL (Vercel + Render) reachable without VPN, for judge access after the pitch
- Must degrade gracefully if AI API rate limits are hit during demo (see fallback strategy in Architecture doc)
- Must be usable on a standard laptop browser (Chrome/Edge) at 1366×768 minimum resolution

## 8. Assumptions

- Regulatory data is sourced from publicly available Maharashtra government documents (MPCB, MIDC, Fire Department, Factories Act) — no private or restricted data is used
- The knowledge graph is pre-built before the hackathon clock starts (data collection is prep work, not part of the 36-hour build)
- Team has 6 members with web development and API integration skills; no custom ML model training is attempted

## 9. Risks

| Risk | Mitigation |
|---|---|
| RAG pipeline returns inaccurate regulation matches | Pre-validate with 10 test queries before demo day; hardcode fallback for the exact demo scenario |
| Live AI API fails during judge demo | Cache the exact demo query's response locally as a fallback trigger |
| React Flow visualization breaks on unusual screen sizes | Test on the actual judging room projector resolution beforehand if possible |
