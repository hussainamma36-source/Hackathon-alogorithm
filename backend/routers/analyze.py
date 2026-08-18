import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import Interaction, Recommendation, RecommendationEvidence, InterestProfile
from schemas import AnalyzeRequest, AnalyzeResponse, AlternativeRecommendation
from ai.recommendation_engine import RecommendationEngine

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    payload: AnalyzeRequest,
    db: AsyncSession = Depends(get_db),
):
    # Fetch all interactions for session
    result = await db.execute(
        select(Interaction)
        .where(Interaction.session_id == payload.session_id)
        .order_by(Interaction.interaction_timestamp)
    )
    interactions = result.scalars().all()

    if not interactions:
        raise HTTPException(
            status_code=400,
            detail="No interactions found for this session. Please interact with some Reels first.",
        )

    # Convert to dicts
    interaction_dicts = [
        {
            "reel_id": i.reel_id,
            "watched_percentage": i.watched_percentage,
            "watch_time": i.watch_time,
            "liked": i.liked,
            "saved": i.saved,
            "shared": i.shared,
            "replayed": i.replayed,
            "skipped": i.skipped,
            "commented": i.commented,
            "clicked_creator": i.clicked_creator,
        }
        for i in interactions
    ]

    # Run recommendation engine
    engine = RecommendationEngine()
    analysis = await engine.analyze(interaction_dicts, payload.session_id)

    interest_profile = analysis["interest_profile"]
    recommended = analysis["recommended"]

    # Determine current reel (most engaged one)
    most_engaged = max(interaction_dicts, key=lambda x: x["watched_percentage"])
    current_reel_map = {
        "reel_001": "Funny College Life Reel",
        "reel_002": "Java Programming Meme",
        "reel_003": "Software Engineer Day-in-the-Life",
        "reel_004": "Coding Interview Joke",
        "reel_005": "Laptop Comparison for Developers",
        "reel_006": "AI/ML Educational Reel",
        "reel_007": "Cybersecurity News Reel",
        "reel_008": "Cloud Computing Tutorial",
    }
    current_reel = current_reel_map.get(most_engaged["reel_id"], most_engaged["reel_id"])

    # Confidence
    confidence_score = interest_profile.get("confidence_score", 0.5)
    confidence = interest_profile.get("confidence", "Medium")

    # Save interest profile
    profile_record = InterestProfile(
        session_id=payload.session_id,
        primary_interest=interest_profile.get("primary_interest", "Technology"),
        secondary_interests=json.dumps(interest_profile.get("secondary_interests", [])),
        interest_scores=json.dumps(interest_profile.get("interest_scores", {})),
        confidence=confidence,
        confidence_score=confidence_score,
        reels_analyzed=len(interactions),
    )
    db.add(profile_record)
    await db.flush()

    # Save recommendation
    rec_record = Recommendation(
        session_id=payload.session_id,
        trigger_reel_id=most_engaged["reel_id"],
        recommended_reel_id=recommended["id"],
        recommended_title=recommended["title"],
        category=recommended["category"],
        difficulty=recommended["difficulty"],
        confidence=confidence,
        confidence_score=confidence_score,
        relevance_score=analysis["relevance_score"],
        hype_score=analysis["hype_score"],
        quality_score=analysis["quality_score"],
        interest_detected=interest_profile.get("primary_interest", "Technology"),
        recommendation_reason=analysis["reason"],
        interest_evidence=json.dumps(interest_profile.get("evidence", [])),
        alternative_recommendations=json.dumps(analysis.get("alternatives", [])),
    )
    db.add(rec_record)
    await db.flush()

    # Save evidence records
    for evidence_text in interest_profile.get("evidence", []):
        ev = RecommendationEvidence(
            recommendation_id=rec_record.id,
            evidence_type="interaction_pattern",
            description=evidence_text,
            strength=confidence_score,
        )
        db.add(ev)

    await db.commit()
    await db.refresh(rec_record)

    # Build alternatives
    alternatives = [
        AlternativeRecommendation(
            title=a.get("title", ""),
            category=a.get("category", ""),
            difficulty=a.get("difficulty", "Intermediate"),
            relevance_score=a.get("relevance_score", a.get("score", 0.5)),
            reason=a.get("reason", ""),
        )
        for a in analysis.get("alternatives", [])
    ]

    return AnalyzeResponse(
        current_reel=current_reel,
        interest_detected=interest_profile.get("primary_interest", "Technology"),
        interest_evidence=interest_profile.get("evidence", []),
        recommended_reel=recommended["title"],
        recommended_description=recommended["description"],
        category=recommended["category"],
        recommendation_reason=analysis["reason"],
        difficulty=recommended["difficulty"],
        confidence=confidence,
        confidence_score=confidence_score,
        relevance_score=analysis["relevance_score"],
        hype_score=analysis["hype_score"],
        quality_score=analysis["quality_score"],
        alternative_recommendations=alternatives,
        interest_scores=interest_profile.get("interest_scores", {}),
        shallow_recommendation=analysis.get("shallow_recommendation", ""),
        shallow_reason=analysis.get("shallow_reason", ""),
        recommendation_id=rec_record.id,
        pipeline_stages=analysis.get("pipeline_stages", []),
    )
