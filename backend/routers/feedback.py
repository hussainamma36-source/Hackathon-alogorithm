from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import Feedback, Recommendation
from schemas import FeedbackCreate, FeedbackResponse

router = APIRouter()


@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    payload: FeedbackCreate,
    db: AsyncSession = Depends(get_db),
):
    # Validate recommendation exists
    result = await db.execute(
        select(Recommendation).where(Recommendation.id == payload.recommendation_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Recommendation not found")

    valid_ratings = {"useful", "not_useful"}
    if payload.rating not in valid_ratings:
        raise HTTPException(status_code=400, detail=f"Rating must be one of: {valid_ratings}")

    valid_reasons = {None, "too_basic", "not_relevant", "too_advanced", "too_repetitive"}
    if payload.reason not in valid_reasons:
        raise HTTPException(status_code=400, detail=f"Reason must be one of: {valid_reasons}")

    feedback = Feedback(**payload.model_dump())
    db.add(feedback)
    await db.commit()
    await db.refresh(feedback)
    return feedback
