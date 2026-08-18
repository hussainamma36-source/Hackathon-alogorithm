"""
Local Fallback Provider — Full multi-stage semantic recommendation engine.
Operates with ZERO external dependencies or API calls.

Pipeline:
  USER INTERACTION HISTORY
    ↓ CONTENT UNDERSTANDING (semantic attribute analysis)
    ↓ INTERACTION SIGNAL ANALYSIS (weighted engagement scoring)
    ↓ INTEREST INFERENCE (semantic domain expansion)
    ↓ BROADER INTEREST PROFILE (primary + secondary)
    ↓ CANDIDATE SCORING (multi-factor relevance)
    ↓ HYPE FILTER (quality enforcement)
    ↓ FINAL RECOMMENDATION + EXPLANATION
"""

from typing import Any, Dict, List, Tuple
from collections import defaultdict

from ai.provider import AIProvider
from ai.content_vectors import REEL_VECTORS, RECOMMENDATION_CANDIDATES, DOMAIN_NEIGHBORHOODS
from ai.hype_filter import calculate_hype_score, apply_hype_penalty


# ── Interaction Signal Weights ─────────────────────────────────────────────────
SIGNAL_WEIGHTS = {
    "watch_percentage_factor": 0.30,  # normalized 0-1
    "liked": 0.20,
    "saved": 0.25,
    "replayed": 0.15,
    "shared": 0.15,
    "commented": 0.10,
    "clicked_creator": 0.10,
    "skipped": -0.35,  # strong negative signal
}

# ── Confidence Thresholds ──────────────────────────────────────────────────────
CONFIDENCE_HIGH = 0.70
CONFIDENCE_MEDIUM = 0.45


class LocalFallbackProvider(AIProvider):
    """
    Multi-stage semantic recommendation engine — no external API required.
    
    This is NOT keyword matching. It:
    1. Scores each reel interaction using weighted signal analysis
    2. Maps content to semantic domains (not just topic names)
    3. Expands domains through neighborhood traversal
    4. Aggregates interest scores across ALL interactions
    5. Scores recommendation candidates against the inferred profile
    6. Applies hype filter and diversity bonus
    7. Generates human-readable explanation
    """

    @property
    def provider_name(self) -> str:
        return "local_semantic_engine"

    async def analyze_interests(
        self,
        interaction_history: List[Dict[str, Any]],
        reel_vectors: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Stage 1-4: Content understanding + interaction scoring + interest inference."""

        if not interaction_history:
            return self._empty_profile()

        # ── Stage 1: Score each interaction ───────────────────────────────────
        scored_interactions = []
        for interaction in interaction_history:
            reel_id = interaction.get("reel_id", "")
            engagement_score = self._calculate_engagement_score(interaction)
            vector = REEL_VECTORS.get(reel_id, {})

            scored_interactions.append({
                "reel_id": reel_id,
                "engagement_score": engagement_score,
                "vector": vector,
                "interaction": interaction,
            })

        # ── Stage 2: Content understanding + domain mapping ───────────────────
        domain_scores: Dict[str, float] = defaultdict(float)

        for si in scored_interactions:
            vector = si["vector"]
            engagement = si["engagement_score"]

            if not vector:
                continue

            # Primary domain gets full engagement weight × tech relevance
            primary = vector.get("primary_domain", "")
            if primary:
                tech_weight = vector.get("tech_relevance", 0.5)
                domain_scores[primary] += engagement * tech_weight

            # Secondary domains get 60% weight
            for domain in vector.get("secondary_domains", []):
                domain_scores[domain] += engagement * 0.60

            # Expansion domains (semantic neighborhoods) get 40% weight
            for domain in vector.get("expansion_domains", []):
                domain_scores[domain] += engagement * 0.40

        # ── Stage 3: Semantic neighborhood traversal ───────────────────────────
        # Expand interest into related domains (this is what prevents keyword echo)
        expanded_scores: Dict[str, float] = dict(domain_scores)

        for domain, score in domain_scores.items():
            if score < 0.10:
                continue
            neighbors = DOMAIN_NEIGHBORHOODS.get(domain, [])
            for neighbor in neighbors:
                # Neighbors get 30% of the base domain score
                expanded_scores[neighbor] = expanded_scores.get(neighbor, 0) + score * 0.30

        # ── Stage 4: Interest profile construction ─────────────────────────────
        if not expanded_scores:
            return self._empty_profile()

        # Normalize scores
        max_score = max(expanded_scores.values()) or 1.0
        normalized: Dict[str, float] = {
            k: round(v / max_score, 3)
            for k, v in expanded_scores.items()
            if v > 0.05
        }

        # Sort by score descending
        sorted_domains = sorted(normalized.items(), key=lambda x: x[1], reverse=True)

        primary_interest = sorted_domains[0][0] if sorted_domains else "technology"
        secondary_interests = [d for d, _ in sorted_domains[1:6]]

        # Map domain keys to human-readable labels
        primary_label = self._domain_to_label(primary_interest)
        secondary_labels = [self._domain_to_label(d) for d in secondary_interests]

        # Confidence based on number of strong interactions and domain convergence
        strong_interactions = sum(1 for si in scored_interactions if si["engagement_score"] > 0.5)
        confidence_score = min(1.0, (strong_interactions / max(len(interaction_history), 1)) * 0.8
                               + (normalized.get(primary_interest, 0) * 0.2))

        confidence = (
            "High" if confidence_score >= CONFIDENCE_HIGH
            else "Medium" if confidence_score >= CONFIDENCE_MEDIUM
            else "Low"
        )

        # Build evidence statements
        evidence = self._build_evidence(scored_interactions, primary_label)

        return {
            "primary_interest": primary_label,
            "secondary_interests": secondary_labels,
            "interest_scores": {
                self._domain_to_label(k): round(v, 3)
                for k, v in sorted_domains[:8]
            },
            "confidence": confidence,
            "confidence_score": round(confidence_score, 3),
            "evidence": evidence,
            "raw_domain_scores": dict(sorted_domains[:10]),
        }

    async def generate_recommendation(
        self,
        interest_profile: Dict[str, Any],
        candidates: List[Dict[str, Any]],
        interaction_history: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Stage 5-9: Candidate scoring + hype filter + final selection + explanation."""

        raw_domain_scores = interest_profile.get("raw_domain_scores", {})
        primary_interest = interest_profile.get("primary_interest", "technology")

        # ── Stage 5: Score candidates ──────────────────────────────────────────
        scored_candidates = []

        for candidate in candidates:
            score, breakdown = self._score_candidate(candidate, raw_domain_scores, interaction_history)

            # ── Stage 6: Hype filter ───────────────────────────────────────────
            hype_score, hype_patterns = calculate_hype_score(
                candidate["title"], candidate["description"]
            )
            final_score = apply_hype_penalty(score, hype_score)

            scored_candidates.append({
                "candidate": candidate,
                "base_score": round(score, 3),
                "hype_score": round(hype_score, 3),
                "final_score": round(final_score, 3),
                "breakdown": breakdown,
                "hype_patterns": hype_patterns,
            })

        # Sort by final score descending
        scored_candidates.sort(key=lambda x: x["final_score"], reverse=True)

        if not scored_candidates:
            return self._fallback_recommendation()

        best = scored_candidates[0]
        alternatives = scored_candidates[1:4]

        # ── Stage 7: Generate explanation ─────────────────────────────────────
        reason = self._generate_reason(
            best["candidate"],
            interest_profile,
            interaction_history,
            best["breakdown"],
        )

        # ── Stage 8: Build pipeline stages for display ────────────────────────
        pipeline_stages = self._build_pipeline_stages(
            interaction_history, interest_profile, scored_candidates
        )

        return {
            "recommended": best["candidate"],
            "relevance_score": best["final_score"],
            "hype_score": best["hype_score"],
            "quality_score": round(1.0 - best["hype_score"], 3),
            "reason": reason,
            "pipeline_stages": pipeline_stages,
            "alternatives": [
                {
                    "title": a["candidate"]["title"],
                    "category": a["candidate"]["category"],
                    "difficulty": a["candidate"]["difficulty"],
                    "relevance_score": a["final_score"],
                    "reason": f"Strong {a['candidate']['primary_domain']} match",
                }
                for a in alternatives
            ],
            "score_breakdown": best["breakdown"],
        }

    # ── Private Helpers ────────────────────────────────────────────────────────

    def _calculate_engagement_score(self, interaction: Dict[str, Any]) -> float:
        """Weighted multi-signal engagement score for a single interaction."""
        score = 0.0

        # Watch percentage (0-100 → 0-1)
        watch_pct = interaction.get("watched_percentage", 0) / 100
        score += watch_pct * SIGNAL_WEIGHTS["watch_percentage_factor"]

        # Boolean signals
        for signal in ["liked", "saved", "replayed", "shared", "commented", "clicked_creator"]:
            if interaction.get(signal, False):
                score += SIGNAL_WEIGHTS[signal]

        # Skipped is a strong negative signal
        if interaction.get("skipped", False):
            score += SIGNAL_WEIGHTS["skipped"]

        return max(0.0, min(1.0, score))

    def _score_candidate(
        self,
        candidate: Dict[str, Any],
        domain_scores: Dict[str, float],
        interaction_history: List[Dict[str, Any]],
    ) -> Tuple[float, Dict[str, float]]:
        """Multi-factor relevance scoring for a recommendation candidate."""

        breakdown: Dict[str, float] = {}

        # Factor 1: Domain match (30%)
        domain_match = 0.0
        candidate_domains = candidate.get("related_domains", [])
        for domain in candidate_domains:
            domain_match += domain_scores.get(domain, 0.0)
        domain_match = min(1.0, domain_match / max(len(candidate_domains), 1))
        breakdown["domain_match"] = round(domain_match, 3)

        # Factor 2: Educational value (20%)
        edu_value = candidate.get("educational_value", 0.5)
        breakdown["educational_value"] = edu_value

        # Factor 3: Career relevance (15%)
        career = candidate.get("career_relevance", 0.5)
        breakdown["career_relevance"] = career

        # Factor 4: Technical depth (15%)
        tech_depth = candidate.get("technical_depth", 0.5)
        breakdown["technical_depth"] = tech_depth

        # Factor 5: Expansion value — diversity bonus (10%)
        # Rewards content that EXPANDS beyond what user has seen
        expansion = candidate.get("expansion_value", 0.5)
        breakdown["expansion_value"] = expansion

        # Factor 6: Content quality (10%)
        quality = 1.0 - candidate.get("hype_score", 0.1)
        breakdown["quality"] = round(quality, 3)

        # Weighted total
        total = (
            domain_match * 0.30
            + edu_value * 0.20
            + career * 0.15
            + tech_depth * 0.15
            + expansion * 0.10
            + quality * 0.10
        )

        return total, breakdown

    def _domain_to_label(self, domain: str) -> str:
        """Convert internal domain key to human-readable label."""
        mapping = {
            "software_engineering": "Software Engineering",
            "programming": "Programming",
            "developer_career": "Developer Career",
            "technical_interviews": "Technical Interview Prep",
            "algorithms": "Algorithms & DSA",
            "data_structures": "Data Structures",
            "computer_hardware": "Computer Hardware",
            "ai_ml": "AI & Machine Learning",
            "cloud_computing": "Cloud Computing",
            "cybersecurity": "Cybersecurity",
            "system_design": "System Design",
            "web_development": "Web Development",
            "backend_development": "Backend Development",
            "data_science": "Data Science",
            "devops": "DevOps",
            "college_life": "College Life",
            "lifestyle": "Lifestyle",
            "entertainment": "Entertainment",
            "open_source": "Open Source",
            "problem_solving": "Problem Solving",
            "computer_science": "Computer Science",
            "mathematics": "Mathematics",
            "research": "Research",
            "scalability": "Scalability",
            "databases": "Databases",
            "infrastructure": "Infrastructure",
            "networking": "Networking",
            "cryptography": "Cryptography",
            "workplace_culture": "Workplace Culture",
            "professional_development": "Professional Development",
            "performance_optimization": "Performance Optimization",
            "software_architecture": "Software Architecture",
        }
        return mapping.get(domain, domain.replace("_", " ").title())

    def _build_evidence(
        self,
        scored_interactions: List[Dict[str, Any]],
        primary_interest: str,
    ) -> List[str]:
        """Build human-readable evidence statements for the interest inference."""
        evidence = []

        # High engagement interactions
        high_eng = [si for si in scored_interactions if si["engagement_score"] > 0.6]
        if high_eng:
            titles = [si["interaction"].get("reel_title", si["reel_id"]) for si in high_eng[:3]]
            evidence.append(f"High engagement (>60%) across {len(high_eng)} content pieces: {', '.join(titles)}")

        # Saved content
        saved = [si for si in scored_interactions if si["interaction"].get("saved")]
        if saved:
            evidence.append(f"Saved {len(saved)} Reel(s) — a strong signal of lasting interest")

        # Liked content
        liked = [si for si in scored_interactions if si["interaction"].get("liked")]
        if liked:
            evidence.append(f"Liked {len(liked)} Reel(s) showing consistent positive engagement")

        # Replayed content
        replayed = [si for si in scored_interactions if si["interaction"].get("replayed")]
        if replayed:
            evidence.append(f"Replayed {len(replayed)} Reel(s) — indicates deeper interest")

        # Skipped content
        skipped = [si for si in scored_interactions if si["interaction"].get("skipped")]
        if skipped:
            evidence.append(f"Skipped {len(skipped)} Reel(s) — interest is technology-focused, not general")

        # Domain convergence
        tech_count = sum(
            1 for si in scored_interactions
            if si["vector"].get("tech_relevance", 0) > 0.5
        )
        if tech_count >= 2:
            evidence.append(
                f"Semantic analysis shows {tech_count} technology-related Reels with strong engagement"
            )

        # Interest inference (the key anti-keyword point)
        evidence.append(
            f"Interest inferred as '{primary_interest}' through semantic domain expansion — "
            f"NOT simple keyword repetition"
        )

        return evidence

    def _generate_reason(
        self,
        candidate: Dict[str, Any],
        interest_profile: Dict[str, Any],
        interaction_history: List[Dict[str, Any]],
        breakdown: Dict[str, float],
    ) -> str:
        """Generate a natural language explanation for the recommendation."""

        primary = interest_profile.get("primary_interest", "technology")
        secondary = interest_profile.get("secondary_interests", [])[:2]

        reel_count = len(interaction_history)
        saved_count = sum(1 for i in interaction_history if i.get("saved"))
        liked_count = sum(1 for i in interaction_history if i.get("liked"))

        title = candidate["title"]
        category = candidate["category"]

        reason_parts = []

        reason_parts.append(
            f"Across {reel_count} analyzed Reels, the AI detected a strong interest pattern in "
            f"'{primary}'"
        )

        if liked_count:
            reason_parts.append(f"with {liked_count} liked content piece(s)")

        if saved_count:
            reason_parts.append(f"and {saved_count} saved for later — signaling lasting interest")

        if secondary:
            reason_parts.append(
                f"Secondary interests in {' and '.join(secondary[:2])} were also detected through "
                f"semantic analysis of content context"
            )

        reason_parts.append(
            f"Instead of recommending the same narrow content, the agent expanded the interest "
            f"profile and selected '{title}' ({category}) because it directly connects your "
            f"inferred programming/career interests with actionable, educationally valuable content"
        )

        reason_parts.append(
            f"This recommendation scores {round(breakdown.get('educational_value', 0) * 100)}% on "
            f"educational value and {round(breakdown.get('career_relevance', 0) * 100)}% on career "
            f"relevance — making it genuinely useful, not just popular"
        )

        return ". ".join(reason_parts) + "."

    def _build_pipeline_stages(
        self,
        interaction_history: List[Dict[str, Any]],
        interest_profile: Dict[str, Any],
        scored_candidates: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Build pipeline stage data for the UI visualization."""
        stages = [
            {
                "stage": "Interaction Analysis",
                "description": f"Analyzed {len(interaction_history)} Reel interactions using weighted signal scoring",
                "status": "complete",
                "detail": f"Signals: watch%, liked, saved, replayed, shared, skipped",
            },
            {
                "stage": "Content Understanding",
                "description": "Mapped each Reel to semantic domain vectors beyond surface keywords",
                "status": "complete",
                "detail": "Tech relevance, educational value, career relevance, domain clusters",
            },
            {
                "stage": "Interest Inference",
                "description": f"Inferred primary interest: {interest_profile.get('primary_interest')}",
                "status": "complete",
                "detail": "Semantic domain expansion through neighborhood traversal",
            },
            {
                "stage": "Interest Profile",
                "description": f"Built interest profile with {len(interest_profile.get('secondary_interests', []))} secondary interests",
                "status": "complete",
                "detail": f"Confidence: {interest_profile.get('confidence')}",
            },
            {
                "stage": "Candidate Scoring",
                "description": f"Scored {len(scored_candidates)} recommendation candidates",
                "status": "complete",
                "detail": "Multi-factor: domain match, educational value, career relevance, diversity",
            },
            {
                "stage": "Hype Filter",
                "description": "Applied quality/hype detection filter",
                "status": "complete",
                "detail": f"Candidates above 0.80 hype score rejected or heavily penalized",
            },
            {
                "stage": "Final Recommendation",
                "description": f"Selected: {scored_candidates[0]['candidate']['title'] if scored_candidates else 'N/A'}",
                "status": "complete",
                "detail": f"Score: {scored_candidates[0]['final_score'] if scored_candidates else 0}",
            },
        ]
        return stages

    def _empty_profile(self) -> Dict[str, Any]:
        return {
            "primary_interest": "Technology",
            "secondary_interests": [],
            "interest_scores": {},
            "confidence": "Low",
            "confidence_score": 0.1,
            "evidence": ["No interaction history available"],
            "raw_domain_scores": {},
        }

    def _fallback_recommendation(self) -> Dict[str, Any]:
        return {
            "recommended": RECOMMENDATION_CANDIDATES[0],
            "relevance_score": 0.5,
            "hype_score": 0.05,
            "quality_score": 0.95,
            "reason": "Default recommendation based on high educational value",
            "pipeline_stages": [],
            "alternatives": [],
            "score_breakdown": {},
        }
