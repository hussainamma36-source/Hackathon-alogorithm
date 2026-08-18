<<<<<<< HEAD
# ReelMind AI — "Turn your scrolling into smarter learning."

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%20%7C%20TypeScript-61DAFB.svg)](https://reactjs.org/)
[![AI Engine](https://img.shields.io/badge/AI-Multi--Stage%20Semantic-purple.svg)]()

Production-ready full-stack AI recommendation agent built for the hackathon problem statement: **"THE ALGORITHM KNOWS YOU TOO WELL"**.

ReelMind AI analyzes student short-form Reel interaction history, infers underlying technology interests, and recommends engaging educational technology content — demonstrating **context-aware AI inference** over shallow keyword matching.

---

## Key Features

1. **Context-Aware Interest Inference**: Infers broader technology domains (e.g. `Software Engineering / Technology`) from multi-reel interaction patterns instead of narrow keyword echo chambers (e.g. `Java`).
2. **Built-in Trap Demonstration**: Live side-by-side comparison ("Why Context Beats Keywords") showcasing shallow keyword matching vs. ReelMind AI agent recommendations.
3. **Multi-Stage Explainable Recommendation Pipeline**:
   `USER INTERACTION HISTORY` ➔ `CONTENT UNDERSTANDING` ➔ `INTERACTION SIGNAL ANALYSIS` ➔ `INTEREST INFERENCE` ➔ `BROADER INTEREST PROFILE` ➔ `CANDIDATE GENERATION` ➔ `RELEVANCE SCORING` ➔ `HYPE FILTER` ➔ `FINAL RECOMMENDATION`
4. **Hype & Clickbait Filter**: Rejects low-quality listicles ("10 AI tools guaranteed to get you hired") in favor of high educational value content.
5. **Zero-Dependency Local Fallback**: Operates out of the box with zero external API key requirements. Automatically upgrades if `AI_API_KEY` is provided.

---

## Tech Stack

- **Frontend**: React 18, TypeScript, Vite, Custom CSS Design System, Recharts, Zustand, Axios.
- **Backend**: Python 3.12, FastAPI, Async SQLAlchemy 2.0, Pydantic v2.
- **Database**: SQLite (default zero-config local), PostgreSQL (production-ready).
- **Testing**: Pytest, Pytest-Asyncio.

---

## Quick Start (Local Setup)

### 1. Backend Setup

```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/Mac:
# source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8000
```
Backend API runs at: `http://localhost:8000` (Docs: `http://localhost:8000/docs`)

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
Frontend Web App runs at: `http://localhost:5173`

---

## Running Automated Tests

```bash
cd backend
pytest tests/ -v
```

Tests verify:
- Trap scenario interest inference (Java meme + lifestyle -> Software Engineering)
- Hype filter detection and score penalties
- Multi-dimensional interest vector scoring
- Signal weights (save, like, skip)

---

## Docker Deployment

```bash
docker-compose up --build
```

---

## Required Output Fields Verified

Every recommendation response contains:
- `CURRENT REEL`: Reference reel
- `INTEREST DETECTED`: Primary inferred technology domain
- `WHY`: Evidence from content and interaction history
- `RECOMMENDED TECH REEL`: Useful educational technology title
- `CATEGORY`: AI / DSA / Java / HLD / Cybersecurity / Cloud / Hardware / Career
- `WHY THIS RECOMMENDATION`: Human-readable connection explanation
- `DIFFICULTY`: Beginner / Intermediate / Advanced
- `CONFIDENCE`: High / Medium / Low
=======
# Hackathon-alogorithm
>>>>>>> f816d92d72a544544189c208f0ba62d1f60144a9
