from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Reel(Base):
    __tablename__ = "reels"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    transcript: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(100))
    creator: Mapped[str] = mapped_column(String(100))
    duration: Mapped[int] = mapped_column(Integer)  # seconds
    hashtags: Mapped[str] = mapped_column(Text)  # comma-separated
    technical_level: Mapped[str] = mapped_column(String(50))  # Beginner/Intermediate/Advanced
    educational_value: Mapped[float] = mapped_column(Float)  # 0-1
    engagement_score: Mapped[float] = mapped_column(Float)  # 0-1
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    topic: Mapped[str] = mapped_column(String(100))
    subtopic: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    intent: Mapped[str] = mapped_column(String(50))  # entertainment/education/career
    technical_relevance: Mapped[float] = mapped_column(Float)
    career_relevance: Mapped[float] = mapped_column(Float)
    hype_score: Mapped[float] = mapped_column(Float, default=0.0)
    broader_domain: Mapped[str] = mapped_column(String(100))
    related_technologies: Mapped[str] = mapped_column(Text)  # JSON array as string
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    interactions: Mapped[list["Interaction"]] = relationship("Interaction", back_populates="reel")


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reel_id: Mapped[str] = mapped_column(String(50), ForeignKey("reels.id"))
    session_id: Mapped[str] = mapped_column(String(100), default="default")
    watched_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    watch_time: Mapped[int] = mapped_column(Integer, default=0)  # seconds
    liked: Mapped[bool] = mapped_column(Boolean, default=False)
    saved: Mapped[bool] = mapped_column(Boolean, default=False)
    shared: Mapped[bool] = mapped_column(Boolean, default=False)
    replayed: Mapped[bool] = mapped_column(Boolean, default=False)
    skipped: Mapped[bool] = mapped_column(Boolean, default=False)
    commented: Mapped[bool] = mapped_column(Boolean, default=False)
    clicked_creator: Mapped[bool] = mapped_column(Boolean, default=False)
    interaction_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    reel: Mapped["Reel"] = relationship("Reel", back_populates="interactions")


class InterestProfile(Base):
    __tablename__ = "interest_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(100))
    primary_interest: Mapped[str] = mapped_column(String(100))
    secondary_interests: Mapped[str] = mapped_column(Text)  # JSON
    interest_scores: Mapped[str] = mapped_column(Text)  # JSON
    confidence: Mapped[str] = mapped_column(String(20))  # High/Medium/Low
    confidence_score: Mapped[float] = mapped_column(Float)
    reels_analyzed: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(100))
    trigger_reel_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    recommended_reel_id: Mapped[str] = mapped_column(String(50))
    recommended_title: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(100))
    difficulty: Mapped[str] = mapped_column(String(50))
    confidence: Mapped[str] = mapped_column(String(20))
    confidence_score: Mapped[float] = mapped_column(Float)
    relevance_score: Mapped[float] = mapped_column(Float)
    hype_score: Mapped[float] = mapped_column(Float)
    quality_score: Mapped[float] = mapped_column(Float)
    interest_detected: Mapped[str] = mapped_column(String(100))
    recommendation_reason: Mapped[str] = mapped_column(Text)
    interest_evidence: Mapped[str] = mapped_column(Text)  # JSON
    alternative_recommendations: Mapped[str] = mapped_column(Text)  # JSON
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    evidence: Mapped[list["RecommendationEvidence"]] = relationship("RecommendationEvidence", back_populates="recommendation")
    feedback: Mapped[list["Feedback"]] = relationship("Feedback", back_populates="recommendation")


class RecommendationEvidence(Base):
    __tablename__ = "recommendation_evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recommendation_id: Mapped[int] = mapped_column(Integer, ForeignKey("recommendations.id"))
    evidence_type: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    strength: Mapped[float] = mapped_column(Float)

    recommendation: Mapped["Recommendation"] = relationship("Recommendation", back_populates="evidence")


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recommendation_id: Mapped[int] = mapped_column(Integer, ForeignKey("recommendations.id"))
    session_id: Mapped[str] = mapped_column(String(100))
    rating: Mapped[str] = mapped_column(String(20))  # useful/not_useful
    reason: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    recommendation: Mapped["Recommendation"] = relationship("Recommendation", back_populates="feedback")
