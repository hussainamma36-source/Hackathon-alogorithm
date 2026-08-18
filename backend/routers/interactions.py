from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from database import get_db
from models import Interaction, Reel
from schemas import InteractionCreate, InteractionResponse

router = APIRouter()


@router.post("/interactions", response_model=InteractionResponse)
async def create_interaction(
    payload: InteractionCreate,
    db: AsyncSession = Depends(get_db),
):
    # Validate reel exists
    result = await db.execute(select(Reel).where(Reel.id == payload.reel_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=f"Reel '{payload.reel_id}' not found")

    # Upsert: remove previous interaction from same session for same reel
    existing = await db.execute(
        select(Interaction).where(
            and_(
                Interaction.reel_id == payload.reel_id,
                Interaction.session_id == payload.session_id,
            )
        )
    )
    old = existing.scalar_one_or_none()
    if old:
        await db.delete(old)
        await db.flush()

    interaction = Interaction(**payload.model_dump())
    db.add(interaction)
    await db.commit()
    await db.refresh(interaction)
    return interaction


@router.get("/interactions", response_model=List[InteractionResponse])
async def get_interactions(
    session_id: str = "default",
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Interaction)
        .where(Interaction.session_id == session_id)
        .order_by(Interaction.interaction_timestamp)
    )
    return result.scalars().all()
