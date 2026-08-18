from fastapi import APIRouter
from schemas import HealthResponse
from config import settings
from ai.provider import get_provider

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health():
    provider = get_provider()
    db_type = "sqlite" if "sqlite" in settings.DATABASE_URL else "postgresql"
    return HealthResponse(
        status="ok",
        version=settings.APP_VERSION,
        ai_provider=provider.provider_name,
        database=db_type,
    )
