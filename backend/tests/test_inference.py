"""
Automated tests for the ReelMind AI recommendation engine.

Key test: Given the hackathon "trap" dataset, the system must NOT
recommend another Java Reel. It should infer a broader software
engineering interest and recommend educationally valuable content.
"""

import asyncio
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.local_provider import LocalFallbackProvider
from ai.hype_filter import calculate_hype_score, should_reject, apply_hype_penalty
from ai.content_vectors import REEL_VECTORS, RECOMMENDATION_CANDIDATES
from ai.recommendation_engine import RecommendationEngine


# ── Trap Scenario Test ─────────────────────────────────────────────────────────

TRAP_INTERACTIONS = [
    {
        "reel_id": "reel_002",  # Java meme
        "watched_percentage": 95.0,
        "watch_time": 21,
        "liked": True,
        "saved": False,
        "shared": False,
        "replayed": True,
        "skipped": False,
        "commented": False,
        "clicked_creator": False,
        "reel_title": "Java Programming Meme",
        "vector": REEL_VECTORS.get("reel_002", {}),
    },
    {
        "reel_id": "reel_003",  # Software engineer lifestyle
        "watched_percentage": 92.0,
        "watch_time": 53,
        "liked": True,
        "saved": True,
        "shared": False,
        "replayed": False,
        "skipped": False,
        "commented": False,
        "clicked_creator": True,
        "reel_title": "Software Engineer Day-in-the-Life",
        "vector": REEL_VECTORS.get("reel_003", {}),
    },
    {
        "reel_id": "reel_004",  # Coding interview joke
        "watched_percentage": 88.0,
        "watch_time": 31,
        "liked": True,
        "saved": False,
        "shared": False,
        "replayed": False,
        "skipped": False,
        "commented": True,
        "clicked_creator": False,
        "reel_title": "Coding Interview Joke",
        "vector": REEL_VECTORS.get("reel_004", {}),
    },
    {
        "reel_id": "reel_005",  # Laptop comparison
        "watched_percentage": 90.0,
        "watch_time": 66,
        "liked": False,
        "saved": True,
        "shared": False,
        "replayed": False,
        "skipped": False,
        "commented": False,
        "clicked_creator": False,
        "reel_title": "Laptop Comparison for Developers",
        "vector": REEL_VECTORS.get("reel_005", {}),
    },
]


@pytest.mark.asyncio
async def test_trap_scenario_interest_inference():
    """
    THE CRITICAL TEST:
    Given Java meme + Software engineer lifestyle + Coding interview + Laptop comparison,
    the system must NOT infer 'Java' as the primary interest.
    It should infer a broader software engineering / technology interest.
    """
    provider = LocalFallbackProvider()
    profile = await provider.analyze_interests(TRAP_INTERACTIONS, REEL_VECTORS)

    primary = profile["primary_interest"].lower()

    # Must NOT be just "Java" or "Programming" (narrow)
    assert "java" not in primary, (
        f"TRAP FAILED: System returned narrow 'Java' interest: {primary}"
    )

    # Must be a broader software engineering or technology interest
    broader_interests = [
        "software engineering", "technology", "developer", "career",
        "technical", "computer science", "programming"  # programming is acceptable as secondary
    ]
    is_broader = any(term in primary for term in broader_interests)
    assert is_broader, (
        f"Expected broader interest like 'Software Engineering', got: {primary}"
    )

    print(f"✅ Primary interest correctly inferred: {profile['primary_interest']}")
    print(f"   Secondary interests: {profile['secondary_interests']}")
    print(f"   Confidence: {profile['confidence']} ({profile['confidence_score']:.2f})")


@pytest.mark.asyncio
async def test_trap_scenario_recommendation():
    """
    The recommendation for the trap dataset must NOT be another Java Reel.
    It should recommend something like DSA, System Design, Backend, etc.
    """
    provider = LocalFallbackProvider()
    profile = await provider.analyze_interests(TRAP_INTERACTIONS, REEL_VECTORS)
    result = await provider.generate_recommendation(profile, RECOMMENDATION_CANDIDATES, TRAP_INTERACTIONS)

    recommended = result["recommended"]
    title = recommended["title"].lower()
    category = recommended["category"].lower()

    # Must NOT recommend the Java-specific candidate (rec_008) as the top result
    # (it's acceptable as an alternative but not the top recommendation)
    assert recommended["id"] != "rec_008" or result["relevance_score"] < 0.7, (
        f"TRAP FAILED: System recommended Java content as top result: {recommended['title']}"
    )

    print(f"✅ Recommended: {recommended['title']}")
    print(f"   Category: {recommended['category']}, Difficulty: {recommended['difficulty']}")
    print(f"   Score: {result['relevance_score']:.3f}")
    print(f"   Reason: {result['reason'][:200]}...")


@pytest.mark.asyncio
async def test_interest_scores_are_multidimensional():
    """Interest scores should reflect multiple domains, not just one."""
    provider = LocalFallbackProvider()
    profile = await provider.analyze_interests(TRAP_INTERACTIONS, REEL_VECTORS)

    scores = profile.get("interest_scores", {})
    # Should have at least 3 distinct interests
    assert len(scores) >= 3, (
        f"Expected at least 3 interest dimensions, got: {len(scores)}: {scores}"
    )
    print(f"✅ Interest scores cover {len(scores)} dimensions: {list(scores.keys())}")


@pytest.mark.asyncio
async def test_confidence_is_high_for_strong_interactions():
    """With 4 high-engagement interactions, confidence should be High or Medium."""
    provider = LocalFallbackProvider()
    profile = await provider.analyze_interests(TRAP_INTERACTIONS, REEL_VECTORS)

    assert profile["confidence"] in ("High", "Medium"), (
        f"Expected High or Medium confidence for strong interactions, got: {profile['confidence']}"
    )
    print(f"✅ Confidence: {profile['confidence']} ({profile['confidence_score']:.2f})")


# ── Hype Filter Tests ──────────────────────────────────────────────────────────

def test_hype_filter_detects_extreme_hype():
    """Clearly hype content should get a high hype score."""
    hype_title = "10 AI tools that will get you a job instantly"
    score, patterns = calculate_hype_score(hype_title)
    assert score > 0.50, f"Expected high hype score, got: {score}"
    print(f"✅ Hype score for '{hype_title}': {score:.2f}")


def test_hype_filter_does_not_penalize_quality():
    """High-quality technical content should have a low hype score."""
    quality_title = "System Design Fundamentals: Scalability Principles"
    quality_desc = "Deep dive into distributed systems architecture, trade-offs, and best practices"
    score, _ = calculate_hype_score(quality_title, quality_desc)
    assert score < 0.30, f"Expected low hype score for quality content, got: {score}"
    print(f"✅ Hype score for quality content: {score:.2f}")


def test_hype_filter_penalizes_guarantee_claims():
    """Guaranteed job/career claims must be penalized."""
    hype_title = "Guaranteed career in tech: 100% guaranteed results"
    score, _ = calculate_hype_score(hype_title)
    assert score > 0.70, f"Expected very high hype score for guarantee claims, got: {score}"
    print(f"✅ Hype score for guarantee claims: {score:.2f}")


def test_hype_penalty_applied_correctly():
    """High hype scores should heavily penalize the recommendation score."""
    base_score = 0.80
    penalized = apply_hype_penalty(base_score, hype_score=0.85)
    assert penalized < base_score * 0.50, (
        f"Expected >50% reduction for extreme hype, got: {penalized:.3f} vs base {base_score}"
    )
    print(f"✅ Hype penalty: {base_score:.2f} → {penalized:.2f} (extreme hype content)")


def test_no_penalty_for_quality_content():
    """Low hype content should receive no or minimal penalty."""
    base_score = 0.85
    result = apply_hype_penalty(base_score, hype_score=0.10)
    assert result == base_score, (
        f"Expected no penalty for quality content, got: {result} vs {base_score}"
    )
    print(f"✅ No penalty applied for quality content: {result:.2f}")


# ── Scoring Tests ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_saved_content_boosts_score():
    """Saving a reel should significantly boost the engagement score."""
    provider = LocalFallbackProvider()

    interaction_with_save = {
        "reel_id": "reel_002",
        "watched_percentage": 50.0,
        "watch_time": 11,
        "liked": False,
        "saved": True,  # strong signal
        "shared": False,
        "replayed": False,
        "skipped": False,
        "commented": False,
        "clicked_creator": False,
    }
    interaction_without_save = {**interaction_with_save, "saved": False}

    score_with = provider._calculate_engagement_score(interaction_with_save)
    score_without = provider._calculate_engagement_score(interaction_without_save)

    assert score_with > score_without, "Saved content should score higher"
    print(f"✅ Score with save: {score_with:.3f}, without: {score_without:.3f}")


@pytest.mark.asyncio
async def test_skipped_content_penalized():
    """Skipping a reel should significantly reduce the engagement score."""
    provider = LocalFallbackProvider()

    skipped = {
        "reel_id": "reel_001",
        "watched_percentage": 30.0,
        "watch_time": 8,
        "liked": False,
        "saved": False,
        "shared": False,
        "replayed": False,
        "skipped": True,
        "commented": False,
        "clicked_creator": False,
    }
    not_skipped = {**skipped, "skipped": False}

    score_skipped = provider._calculate_engagement_score(skipped)
    score_not_skipped = provider._calculate_engagement_score(not_skipped)

    assert score_skipped < score_not_skipped, "Skipped content should score lower"
    print(f"✅ Score skipped: {score_skipped:.3f}, not skipped: {score_not_skipped:.3f}")


# ── Recommendation Diversity Test ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_recommendation_diversity():
    """
    Given only Java-content interactions, the top recommendation should
    still expand the user's interest rather than just repeating Java.
    """
    provider = LocalFallbackProvider()

    java_only_interactions = [
        {
            "reel_id": "reel_002",
            "watched_percentage": 95.0,
            "watch_time": 21,
            "liked": True,
            "saved": True,
            "shared": False,
            "replayed": True,
            "skipped": False,
            "commented": True,
            "clicked_creator": True,
            "reel_title": "Java Programming Meme",
            "vector": REEL_VECTORS.get("reel_002", {}),
        }
    ]

    profile = await provider.analyze_interests(java_only_interactions, REEL_VECTORS)
    result = await provider.generate_recommendation(profile, RECOMMENDATION_CANDIDATES, java_only_interactions)

    # Top recommendation should expand into adjacent domains
    recommended = result["recommended"]
    # It's ok to recommend Java Architecture, but it should have high educational value
    assert recommended.get("educational_value", 0) > 0.75, (
        f"Expected high educational value recommendation, got: {recommended['title']} "
        f"(edu_value: {recommended.get('educational_value')})"
    )
    print(f"✅ Diversity recommendation for Java-only: {recommended['title']}")
    print(f"   Expansion value: {recommended.get('expansion_value', 'N/A')}")


if __name__ == "__main__":
    # Run tests directly
    asyncio.run(test_trap_scenario_interest_inference())
    asyncio.run(test_trap_scenario_recommendation())
    asyncio.run(test_interest_scores_are_multidimensional())
    asyncio.run(test_confidence_is_high_for_strong_interactions())
    test_hype_filter_detects_extreme_hype()
    test_hype_filter_does_not_penalize_quality()
    test_hype_filter_penalizes_guarantee_claims()
    test_hype_penalty_applied_correctly()
    test_no_penalty_for_quality_content()
    asyncio.run(test_saved_content_boosts_score())
    asyncio.run(test_skipped_content_penalized())
    asyncio.run(test_recommendation_diversity())
    print("\n✅ All tests passed!")
