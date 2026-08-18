import json
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import Recommendation
from schemas import RecommendationResponse

router = APIRouter()


@router.get("/history", response_model=List[RecommendationResponse])
async def get_history(
    session_id: str = "default",
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Recommendation)
        .where(Recommendation.session_id == session_id)
        .order_by(Recommendation.created_at.desc())
        .limit(50)
    )
    return result.scalars().all()
