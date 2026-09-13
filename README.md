# Naypath (SWĀKRIT) - Smart India Hackathon 2026 🏆

![Hackathon](https://img.shields.io/badge/Smart_India_Hackathon-2026-orange?style=for-the-badge&logo=codeforces)
![Problem Statement](https://img.shields.io/badge/PS_ID-SIH26130-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**Team:** Hexacore  
**Theme:** Smart Automation (MSME & Industrial Governance)  
**Problem Statement:** Efficiency in streamlining industrial approvals, compliance processes, and access to government support services.

---

## 📖 Overview
Approval delay is the single largest entry barrier for a small industrial unit. Weeks are lost re-uploading identical documents across 5+ separate department portals (Pollution, Labour, Fire, Factory, GST, Municipal) and chasing files that are stuck somewhere invisible.

**Naypath (SWĀKRIT)** is a smart single-window system for industrial approvals and compliance. It acts as an AI-driven layer on top of existing portals (like NSWS and MAITRI) to provide:
- **Instant Eligibility Discovery:** NLP-driven approval matching to tell you exactly what you need.
- **Unified Document Vault:** Upload documents once, reuse them for every department.
- **Live Tracking & SLA Escalation:** See the exact status of your application across all departments, with automated escalation when a department misses its deadline.
- **Compliance Calendar:** Never miss a renewal date again.

## 🚀 Key Features

* **< 15 sec Instant Roadmap:** Describe your business in plain language (English or Regional) and get a comprehensive, statutory-backed checklist of required permits instantly.
* **1 Profile, 4+ Departments:** No more repetitive form filling. The unified profile auto-fills forms across multiple departments.
* **Document Audit:** AI automatically checks uploaded documents for gaps and issues *before* submission to prevent rejections.
* **Cached Fallback & RAG Grounding:** Handles state API rate-limits and guarantees zero AI hallucination by backing every checklist item with the exact statute citation.

## 💻 Tech Stack

### Frontend
- **React + Vite** for blazing fast performance
- **TailwindCSS** for responsive UI
- Vercel Deployment

### Backend
- **FastAPI (Python)** for high-performance API routing
- **PostgreSQL** (Database) & **Redis / Celery** (Queues)
- Render Deployment

### AI & Data
- **ChromaDB** for Vector embeddings
- **RAG Retrieval** over 1,600+ chunks of statutory documents
- **IndicBERT / mBERT** fine-tuned for regional language NLP

## ⚙️ Local Development

### Backend Setup
```bash
cd nyapath-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd clearpath-ai-prototype
npm install
npm run dev
```

---
*Built with ❤️ by Team Hexacore for SIH 2026*
