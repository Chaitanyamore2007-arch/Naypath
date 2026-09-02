# Deployment Guide — SWĪKRIT

## Prerequisites
- GitHub repository with two folders: `/frontend` and `/backend` (monorepo) or two separate repos
- Vercel account (free tier)
- Render account (free tier)
- All API keys ready: Groq, Anthropic (Claude), Google (Gemini), Tavily

---

## Part 1: Backend Deployment (Render)

1. Push your FastAPI backend code to GitHub.
2. On Render: New → Web Service → connect your GitHub repo → select `/backend` as root directory (if monorepo).
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (from API spec doc, Section "Environment Variables Required") in Render's dashboard under Environment.
6. Add a Render PostgreSQL instance (New → PostgreSQL, free tier) and copy its connection string into `DATABASE_URL`.
7. Deploy. Note your backend URL: `https://<your-app-name>.onrender.com`

**Important for demo day:** Render free tier services spin down after inactivity and take ~30–60 seconds to wake up on the first request. Ping your backend's `/api/health` endpoint 5 minutes before your presentation slot to warm it up.

---

## Part 2: Frontend Deployment (Vercel)

1. Push your React frontend code to GitHub.
2. On Vercel: New Project → import your GitHub repo → select `/frontend` as root directory (if monorepo).
3. Framework preset: Vite.
4. Add environment variable: `VITE_API_BASE_URL=https://<your-backend>.onrender.com/api`
5. Deploy. Vercel gives you a live URL instantly: `https://<your-app>.vercel.app`

---

## Part 3: ChromaDB Persistence

Render's free tier has ephemeral disk by default — if the service restarts, your ChromaDB data can be lost. Two options:

- **Simple (recommended for hackathon):** Run the ChromaDB population script as part of your backend's startup routine (`on_startup` event in FastAPI) so it rebuilds automatically every time the service starts. Since your regulation dataset is small (a few hundred chunks), this takes under 30 seconds.
- **Persistent (if time allows):** Attach a Render Disk (paid, but cheap) to persist `CHROMA_PERSIST_DIR` across restarts.

---

## Part 4: Pre-Demo Checklist

- [ ] Backend health check returns 200 OK
- [ ] Frontend loads and connects to backend (check browser console for CORS errors)
- [ ] Run your exact demo scenario once, 10 minutes before presenting, to warm the cache
- [ ] Verify PDF upload works with your actual demo PDF file
- [ ] Test on the venue's wifi if possible — have mobile hotspot as backup
- [ ] Take screenshots of a fully working roadmap as an offline fallback slide, in case live demo fails entirely

---

## Part 5: CORS Configuration (Backend)

In your FastAPI `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-app.vercel.app", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
