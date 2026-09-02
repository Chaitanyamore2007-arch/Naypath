# Database Schema — SWĪKRIT (PostgreSQL)

## Table: `roadmaps`

Caches generated roadmaps — doubles as your demo-day fallback cache.

| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| profile_hash | TEXT (unique, indexed) | hash of industry_type+district+investment_scale — used for cache lookup |
| industry_type | TEXT | |
| district | TEXT | |
| investment_scale_crores | NUMERIC | |
| roadmap_json | JSONB | full generated roadmap response |
| created_at | TIMESTAMP | default now() |

## Table: `clearances`

Static reference data — the regulatory knowledge base structured for lookup (also mirrored in ChromaDB for semantic search).

| Column | Type | Notes |
|---|---|---|
| id | TEXT (PK) | e.g. `clr_001` |
| name | TEXT | |
| department | TEXT | |
| applicable_industries | TEXT[] | array of industry types this applies to |
| required_documents | JSONB | list of document names |
| estimated_days_min | INT | |
| estimated_days_max | INT | |
| estimated_fee_inr | NUMERIC | |
| typical_rejection_reasons | JSONB | |

## Table: `audits`

Stores document gap-audit results.

| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| roadmap_id | UUID (FK → roadmaps.id) | |
| gaps_json | JSONB | full gap report |
| compliant_count | INT | |
| gap_count | INT | |
| created_at | TIMESTAMP | default now() |

## Table: `sessions` (optional — for judge/demo tracking)

| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| roadmap_id | UUID (FK) | |
| user_agent | TEXT | |
| created_at | TIMESTAMP | |

---

## ChromaDB Collections (Vector Store — separate from PostgreSQL)

**Collection: `maharashtra_regulations`**

Each document chunk stored with metadata:
```json
{
  "text": "<chunk of regulation text>",
  "metadata": {
    "source_department": "MPCB",
    "applicable_industry": ["chemical", "pharmaceutical"],
    "regulation_reference": "MPCB Consent Guideline 4.2",
    "source_url": "<public government document URL>"
  }
}
```

Populate this BEFORE the hackathon starts by scraping/chunking public PDFs from:
- Maharashtra Pollution Control Board (mpcb.gov.in)
- MIDC official portal
- Maharashtra Fire Services
- Factories Act (Maharashtra rules)

Recommended chunk size: 500–800 tokens with 100-token overlap, using LangChain's `RecursiveCharacterTextSplitter`.
