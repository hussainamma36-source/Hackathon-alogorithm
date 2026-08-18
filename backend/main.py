from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import init_db, AsyncSessionLocal
from seed import seed_database

from routers import health, reels, interactions, analyze, interests, recommendations, history, feedback


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    async with AsyncSessionLocal() as db:
        await seed_database(db)
    yield
    # Shutdown (nothing needed for SQLite)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Reel recommendation engine for students",
    lifespan=lifespan,
)

# CORS — Allow all origins, methods, and headers for seamless local & deployed connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(reels.router, prefix="/api", tags=["Reels"])
app.include_router(interactions.router, prefix="/api", tags=["Interactions"])
app.include_router(analyze.router, prefix="/api", tags=["Analysis"])
app.include_router(interests.router, prefix="/api", tags=["Interests"])
app.include_router(recommendations.router, prefix="/api", tags=["Recommendations"])
app.include_router(history.router, prefix="/api", tags=["History"])
app.include_router(feedback.router, prefix="/api", tags=["Feedback"])


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "tagline": "Turn your scrolling into smarter learning.",
        "docs": "/docs",
    }
