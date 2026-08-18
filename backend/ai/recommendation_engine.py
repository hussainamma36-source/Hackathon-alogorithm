"""
Recommendation Engine — Orchestrates the full AI pipeline.

This module ties together:
  - Content vector lookups
  - AI provider (local or LLM)
  - Hype filter
  - Response construction
  - Shallow keyword engine (for trap demo comparison)
"""

from typing import Any, Dict, List, Optional

from ai.provider import get_provider
from ai.content_vectors import REEL_VECTORS, RECOMMENDATION_CANDIDATES
from ai.hype_filter import calculate_hype_score


class RecommendationEngine:
    """Orchestrates the full recommendation pipeline."""

    def __init__(self):
        self.provider = get_provider()

    async def analyze(
        self,
        interactions: List[Dict[str, Any]],
        session_id: str = "default",
    ) -> Dict[str, Any]:
        """
        Full pipeline:
        1. Fetch reel vectors for all interacted reels
        2. Run AI provider's interest analysis
        3. Run AI provider's candidate scoring
        4. Construct final response with shallow comparison
        """

        # Enrich interactions with reel titles
        enriched = []
        for interaction in interactions:
            reel_id = interaction.get("reel_id", "")
            vector = REEL_VECTORS.get(reel_id, {})
            enriched.append({
                **interaction,
                "reel_title": self._get_reel_title(reel_id),
                "vector": vector,
            })

        # ── Step 1: Interest analysis ──────────────────────────────────────────
        interest_profile = await self.provider.analyze_interests(
            enriched, REEL_VECTORS
        )

        # ── Step 2: Generate recommendation ───────────────────────────────────
        result = await self.provider.generate_recommendation(
            interest_profile,
            RECOMMENDATION_CANDIDATES,
            enriched,
        )

        # ── Step 3: Shallow engine comparison ─────────────────────────────────
        shallow = self._shallow_keyword_recommendation(interactions)

        # ── Step 4: Package full response ─────────────────────────────────────
        recommended = result["recommended"]

        return {
            "interest_profile": interest_profile,
            "recommended": recommended,
            "relevance_score": result["relevance_score"],
            "hype_score": result.get("hype_score", recommended.get("hype_score", 0.1)),
            "quality_score": result.get("quality_score", 1.0 - recommended.get("hype_score", 0.1)),
            "reason": result["reason"],
            "pipeline_stages": result.get("pipeline_stages", []),
            "alternatives": result.get("alternatives", []),
            "shallow_recommendation": shallow["title"],
            "shallow_reason": shallow["reason"],
            "provider": self.provider.provider_name,
        }

    def _get_reel_title(self, reel_id: str) -> str:
        titles = {
            "reel_001": "Funny College Life Reel",
            "reel_002": "Java Programming Meme",
            "reel_003": "Software Engineer Day-in-the-Life",
            "reel_004": "Coding Interview Joke",
            "reel_005": "Laptop Comparison for Developers",
            "reel_006": "AI/ML Educational Reel",
            "reel_007": "Cybersecurity News Reel",
            "reel_008": "Cloud Computing Tutorial",
        }
        return titles.get(reel_id, reel_id)

    def _shallow_keyword_recommendation(self, interactions: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Simulate what a naive keyword-matching system would recommend.
        This is used for the trap demo comparison.
        """
        # Find most interacted reel
        best_interaction = max(
            interactions,
            key=lambda i: i.get("watched_percentage", 0),
            default=None,
        )

        if not best_interaction:
            return {"title": "Generic Tech Reel", "reason": "No interaction data"}

        reel_id = best_interaction.get("reel_id", "")

        # Naive keyword maps: just repeat the same content type
        shallow_map = {
            "reel_001": {
                "title": "Another Funny College Life Reel",
                "reason": "Matched keyword: 'college' from most watched reel",
            },
            "reel_002": {
                "title": "Another Java Programming Meme Compilation",
                "reason": "Matched keyword: 'Java' from most watched reel",
            },
            "reel_003": {
                "title": "More Software Engineer Vlogs",
                "reason": "Matched keyword: 'software engineer' from most watched reel",
            },
            "reel_004": {
                "title": "More Coding Interview Jokes",
                "reason": "Matched keyword: 'coding interview' from most watched reel",
            },
            "reel_005": {
                "title": "Another Laptop Comparison",
                "reason": "Matched keyword: 'laptop' from most watched reel",
            },
            "reel_006": {
                "title": "More AI Tools Listicle",
                "reason": "Matched keyword: 'AI' from most watched reel",
            },
            "reel_007": {
                "title": "More Cybersecurity News",
                "reason": "Matched keyword: 'cybersecurity' from most watched reel",
            },
            "reel_008": {
                "title": "More Cloud Tutorial",
                "reason": "Matched keyword: 'cloud' from most watched reel",
            },
        }

        return shallow_map.get(reel_id, {
            "title": "Generic Tech Content",
            "reason": "Keyword matched from interaction history",
        })
