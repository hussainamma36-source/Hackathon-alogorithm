# ReelMind AI — Production Deployment Guide

This guide provides step-by-step instructions to deploy ReelMind AI to production environments (Vercel, Render, and Neon/Supabase PostgreSQL).

---

## 1. Database Deployment (PostgreSQL)

### Option A: Neon PostgreSQL (Recommended — Free & Fast)
1. Go to [neon.tech](https://neon.tech) and create a free PostgreSQL database project named `reelmind-db`.
2. Copy the Connection String from the dashboard. It will look like:
   `postgres://reelmind_user:password@ep-cool-pool-123456.us-east-2.aws.neon.tech/reelmind?sslmode=require`
3. Convert to async format (if needed, the backend automatically normalizes `postgres://` to `postgresql+asyncpg://`):
   `postgresql+asyncpg://reelmind_user:password@ep-cool-pool-123456.us-east-2.aws.neon.tech/reelmind?sslmode=require`

### Option B: Supabase PostgreSQL
1. Go to [supabase.com](https://supabase.com) and create a project.
2. In Project Settings -> Database -> Connection String (URI), copy the connection string.

---

## 2. Backend Deployment (Render / Railway / Fly.io)

### Deploying Backend to Render
1. Push your project to GitHub.
2. Log in to [render.com](https://render.com) and click **New +** -> **Web Service**.
3. Connect your GitHub repository.
4. Set the following fields:
   - **Name**: `reelmind-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   - `DATABASE_URL`: `<your-neon-or-render-postgres-url>`
   - `AI_PROVIDER`: `local` (or `openai` / `gemini` if providing API key)
   - `AI_API_KEY`: `<optional-api-key>`
   - `CORS_ORIGINS`: `*`
6. Click **Create Web Service**.
7. Once deployed, note your deployed Backend URL (e.g., `https://reelmind-backend.onrender.com`).
8. Verify health: `https://reelmind-backend.onrender.com/api/health`

---

## 3. Frontend Deployment (Vercel / Netlify)

### Deploying Frontend to Vercel
1. Log in to [vercel.com](https://vercel.com) and click **Add New** -> **Project**.
2. Import your GitHub repository.
3. Set the following fields:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Add Environment Variable:
   - `VITE_API_BASE_URL`: `https://reelmind-backend.onrender.com` (Use your deployed Backend URL)
5. Click **Deploy**.
6. Once deployed, Vercel gives you your live production URL (e.g., `https://reelmind-ai.vercel.app`).

---

## 4. Post-Deployment End-to-End Verification Checklist

Once both Backend and Frontend are deployed:

1. **Verify Backend Health**:
   Open `https://<your-backend-url>/api/health` in your browser. Verify it returns:
   `{"status":"ok","version":"1.0.0","ai_provider":"local_semantic_engine","database":"postgresql"}`

2. **Verify Frontend Application**:
   Open `https://<your-frontend-url>` in your browser.

3. **Check Browser Console**:
   Ensure no CORS errors or connection errors appear in F12 Developer Tools -> Console.

4. **Test Hackathon Trap Scenario**:
   - Click **"Load Hackathon Demo Data"**
   - Click **"Analyze My Interests"**
   - Verify Detected Interest: `Software Engineering / Technology` (NOT narrow Java)
   - Verify Recommended Content: `DSA Interview Patterns for Software Engineers`
   - Verify Category (`DSA`), Difficulty (`Intermediate`), Confidence (`High`), and Explanation.

5. **Test Interactive Feedback**:
   - Click **"👍 Useful"** button on the recommendation card.
   - Check **"Recommendation History"** tab to verify audit log persistence.
