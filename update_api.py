import re

with open("03_API_SPECIFICATION.md", "r", encoding="utf-8") as f:
    content = f.read()

# Add missing fields to /roadmap
content = content.replace('"is_critical_path": true\n    }', '"is_critical_path": true,\n      "required_documents": ["Form-1", "Site plan"],\n      "common_rejection_reasons": ["Incomplete Form-1"]\n    }')

# Replace GET /clearance with the two new ones
new_endpoints = """
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
"""

content = re.sub(r"## 3\. GET `/api/clearance.*?```\n\n---\n", new_endpoints + "\n---\n", content, flags=re.DOTALL)
content = content.replace("## 4. GET `/api/health`", "## 5. GET `/api/health`")

with open("03_API_SPECIFICATION.md", "w", encoding="utf-8") as f:
    f.write(content)
