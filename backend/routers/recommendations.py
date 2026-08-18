import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import Recommendation
from schemas import RecommendationResponse, RecommendationDetailResponse

router = APIRouter()


@router.get("/recommendations", response_model=List[RecommendationResponse])
async def get_recommendations(
    session_id: str = "default",
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Recommendation)
        .where(Recommendation.session_id == session_id)
        .order_by(Recommendation.created_at.desc())
    )
    return result.scalars().all()


@router.get("/recommendations/{rec_id}", response_model=RecommendationDetailResponse)
async def get_recommendation(
    rec_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Recommendation).where(Recommendation.id == rec_id)
    )
    rec = result.scalar_one_or_none()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    return RecommendationDetailResponse(
        id=rec.id,
        session_id=rec.session_id,
        recommended_title=rec.recommended_title,
        category=rec.category,
        difficulty=rec.difficulty,
        confidence=rec.confidence,
        confidence_score=rec.confidence_score,
        relevance_score=rec.relevance_score,
        hype_score=rec.hype_score,
        quality_score=rec.quality_score,
        interest_detected=rec.interest_detected,
        recommendation_reason=rec.recommendation_reason,
        interest_evidence=json.loads(rec.interest_evidence or "[]"),
        alternative_recommendations=json.loads(rec.alternative_recommendations or "[]"),
        created_at=rec.created_at,
    )
