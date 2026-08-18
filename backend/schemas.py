from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# ── Reel Schemas ─────────────────────────────────────────────────────────────

class ReelBase(BaseModel):
    id: str
    title: str
    description: str
    transcript: str
    category: str
    creator: str
    duration: int
    hashtags: str
    technical_level: str
    educational_value: float
    engagement_score: float
    topic: str
    subtopic: Optional[str] = None
    intent: str
    technical_relevance: float
    career_relevance: float
    hype_score: float
    broader_domain: str
    related_technologies: str
    thumbnail_url: Optional[str] = None


class ReelResponse(ReelBase):
    created_at: datetime

    class Config:
        from_attributes = True


# ── Interaction Schemas ────────────────────────────────────────────────────────

class InteractionCreate(BaseModel):
    reel_id: str
    session_id: str = "default"
    watched_percentage: float = Field(ge=0, le=100)
    watch_time: int = Field(ge=0)
    liked: bool = False
    saved: bool = False
    shared: bool = False
    replayed: bool = False
    skipped: bool = False
    commented: bool = False
    clicked_creator: bool = False


class InteractionResponse(InteractionCreate):
    id: int
    interaction_timestamp: datetime

    class Config:
        from_attributes = True


# ── Interest Profile Schemas ───────────────────────────────────────────────────

class InterestProfileResponse(BaseModel):
    session_id: str
    primary_interest: str
    secondary_interests: List[str]
    interest_scores: dict
    confidence: str
    confidence_score: float
    reels_analyzed: int
    created_at: datetime

    class Config:
        from_attributes = True


# ── Analysis Schemas ───────────────────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    session_id: str = "default"
    force_reel_id: Optional[str] = None  # analyze from perspective of a specific reel


class AlternativeRecommendation(BaseModel):
    title: str
    category: str
    difficulty: str
    relevance_score: float
    reason: str


class AnalyzeResponse(BaseModel):
    current_reel: Optional[str] = None
    interest_detected: str
    interest_evidence: List[str]
    recommended_reel: str
    recommended_description: str
    category: str
    recommendation_reason: str
    difficulty: str
    confidence: str
    confidence_score: float
    relevance_score: float
    hype_score: float
    quality_score: float
    alternative_recommendations: List[AlternativeRecommendation]
    interest_scores: dict
    shallow_recommendation: str  # what keyword engine would give
    shallow_reason: str
    recommendation_id: int
    pipeline_stages: List[dict]


# ── Recommendation Schemas ─────────────────────────────────────────────────────

class RecommendationResponse(BaseModel):
    id: int
    session_id: str
    recommended_title: str
    category: str
    difficulty: str
    confidence: str
    confidence_score: float
    relevance_score: float
    interest_detected: str
    recommendation_reason: str
    created_at: datetime

    class Config:
        from_attributes = True


class RecommendationDetailResponse(RecommendationResponse):
    interest_evidence: List[str]
    alternative_recommendations: List[dict]
    hype_score: float
    quality_score: float


# ── Feedback Schemas ───────────────────────────────────────────────────────────

class FeedbackCreate(BaseModel):
    recommendation_id: int
    session_id: str = "default"
    rating: str  # useful / not_useful
    reason: Optional[str] = None  # too_basic / not_relevant / too_advanced / too_repetitive


class FeedbackResponse(FeedbackCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ── Health ─────────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    version: str
    ai_provider: str
    database: str
