from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import Reel
from schemas import ReelResponse

router = APIRouter()


@router.get("/reels", response_model=List[ReelResponse])
async def get_reels(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Reel).order_by(Reel.created_at))
    return result.scalars().all()


@router.get("/reels/{reel_id}", response_model=ReelResponse)
async def get_reel(reel_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Reel).where(Reel.id == reel_id))
    reel = result.scalar_one_or_none()
    if not reel:
        raise HTTPException(status_code=404, detail=f"Reel '{reel_id}' not found")
    return reel
