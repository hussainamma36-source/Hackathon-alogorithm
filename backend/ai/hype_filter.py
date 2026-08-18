"""
Hype Filter — Detects and penalizes low-quality, clickbait, or hype-driven content.

The hype filter distinguishes between:
  USEFUL: "How LLM applications are architectured"
  HYPE:   "10 AI tools that will get you a job instantly"

It uses pattern matching + contextual scoring, NOT simple keyword blocking.
High-quality content about the same topics (AI, career) is NOT penalized.
"""

import re
from typing import Tuple, List


# ── Hype Phrase Patterns ───────────────────────────────────────────────────────
HYPE_PATTERNS = [
    # Instant/guaranteed results
    (r"\bget\s+(?:you\s+)?a\s+job\s+instantly\b", 0.9),
    (r"\bguaranteed?\s+job\b", 0.95),
    (r"\bguaranteed?\s+career\b", 0.90),
    (r"\b100%\s+guaranteed?\b", 0.90),
    (r"\binstant\s+job\b", 0.85),
    (r"\bno\s+skills?\s+required\b", 0.90),
    (r"\bno\s+experience\s+needed\b", 0.80),
    (r"\bno\s+degree\s+needed\b", 0.30),  # softer — this can be legitimate
    
    # Unrealistic timeframes
    (r"\b(?:expert|pro|master)\s+in\s+\d+\s+days?\b", 0.85),
    (r"\blearn\s+\w+\s+in\s+\d+\s+(hours?|days?|weeks?)\b", 0.60),
    (r"\b\d+\s+days?\s+to\s+(?:get|land|find)\s+(?:you\s+)?a\s+job\b", 0.85),
    (r"\bbecome\s+an?\s+expert\s+in\b", 0.70),
    
    # Listicle hype
    (r"\b\d+\s+(?:ai\s+)?(?:tools?|apps?|websites?)\s+that\s+will\b", 0.75),

    (r"\b\d+\s+(?:secret|hidden|unknown)\s+\w+\b", 0.65),
    (r"\bthis\s+one\s+trick\b", 0.85),
    (r"\bthey\s+don't\s+want\s+you\s+to\s+know\b", 0.90),
    (r"\bchange\s+your\s+life\b", 0.65),
    (r"\bwill\s+blow\s+your\s+mind\b", 0.70),
    
    # Passive income / shortcuts
    (r"\bpassive\s+income\b", 0.70),
    (r"\bmake\s+money\s+online\b", 0.80),
    (r"\beach\s+\$\d+\b", 0.75),
    (r"\bquick\s+money\b", 0.85),
    
    # Soft hype (partial penalties)
    (r"\bhustle\s+culture\b", 0.35),
    (r"\bgrind\s+to\s+success\b", 0.40),
    (r"\bside\s+hustle\b", 0.30),
]

# Quality signals that REDUCE hype score
QUALITY_SIGNALS = [
    r"\barchitecture\b",
    r"\bfundamentals?\b",
    r"\bprinciples?\b",
    r"\bin-depth\b",
    r"\bdeep\s+dive\b",
    r"\bcomprehensive\b",
    r"\bproduction\b",
    r"\bscalabilit",
    r"\btrade-?offs?\b",
    r"\bbest\s+practices?\b",
    r"\bsystem\s+design\b",
    r"\bdata\s+structures?\b",
    r"\balgorithms?\b",
    r"\bsecurity\b",
    r"\bperformance\b",
    r"\boptimization\b",
]


def calculate_hype_score(title: str, description: str = "") -> Tuple[float, List[str]]:
    """
    Calculate a hype score from 0.0 (not hypy) to 1.0 (extremely hypy).
    Returns (hype_score, list_of_matched_patterns).
    """
    text = (title + " " + description).lower()
    
    matched_patterns: List[str] = []
    raw_hype = 0.0
    
    for pattern, weight in HYPE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            raw_hype += weight
            matched_patterns.append(pattern)
    
    # Count quality signals
    quality_count = sum(
        1 for sig in QUALITY_SIGNALS
        if re.search(sig, text, re.IGNORECASE)
    )
    
    # Each quality signal reduces hype by 0.15
    quality_reduction = quality_count * 0.15
    
    final_hype = max(0.0, min(1.0, raw_hype - quality_reduction))
    
    return final_hype, matched_patterns


def should_reject(hype_score: float, threshold: float = 0.80) -> bool:
    """Reject content above hype threshold."""
    return hype_score >= threshold


def apply_hype_penalty(base_score: float, hype_score: float) -> float:
    """
    Apply a scaled penalty to a recommendation score based on hype level.
    Low hype → minimal penalty. High hype → heavy penalty.
    """
    if hype_score < 0.20:
        return base_score  # No penalty for quality content
    elif hype_score < 0.40:
        return base_score * 0.90  # 10% penalty
    elif hype_score < 0.60:
        return base_score * 0.75  # 25% penalty
    elif hype_score < 0.80:
        return base_score * 0.55  # 45% penalty
    else:
        return base_score * 0.20  # 80% penalty for extreme hype
