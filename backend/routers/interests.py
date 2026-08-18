import json
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import InterestProfile
from schemas import InterestProfileResponse

router = APIRouter()


@router.get("/interests", response_model=InterestProfileResponse)
async def get_interests(
    session_id: str = "default",
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(InterestProfile)
        .where(InterestProfile.session_id == session_id)
        .order_by(InterestProfile.created_at.desc())
        .limit(1)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        return InterestProfileResponse(
            session_id=session_id,
            primary_interest="Not yet analyzed",
            secondary_interests=[],
            interest_scores={},
            confidence="Low",
            confidence_score=0.0,
            reels_analyzed=0,
            created_at=__import__("datetime").datetime.utcnow(),
        )

    return InterestProfileResponse(
        session_id=profile.session_id,
        primary_interest=profile.primary_interest,
        secondary_interests=json.loads(profile.secondary_interests or "[]"),
        interest_scores=json.loads(profile.interest_scores or "{}"),
        confidence=profile.confidence,
        confidence_score=profile.confidence_score,
        reels_analyzed=profile.reels_analyzed,
        created_at=profile.created_at,
    )
