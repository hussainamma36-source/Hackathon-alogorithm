"""
Abstract AI Provider Base Class.
All providers must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AIProvider(ABC):
    """
    Abstract base class for AI recommendation providers.
    Implementations: LocalFallbackProvider, LLMProvider.
    """

    @abstractmethod
    async def analyze_interests(
        self,
        interaction_history: List[Dict[str, Any]],
        reel_vectors: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze user interaction history and return an interest profile.
        
        Returns:
            {
                "primary_interest": str,
                "secondary_interests": List[str],
                "interest_scores": Dict[str, float],
                "confidence": str,  # High/Medium/Low
                "confidence_score": float,
                "evidence": List[str],
            }
        """
        pass

    @abstractmethod
    async def generate_recommendation(
        self,
        interest_profile: Dict[str, Any],
        candidates: List[Dict[str, Any]],
        interaction_history: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generate a final recommendation from scored candidates.
        
        Returns:
            {
                "recommended": Dict,  # chosen candidate
                "relevance_score": float,
                "reason": str,
                "pipeline_stages": List[Dict],
                "alternatives": List[Dict],
            }
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass


def get_provider() -> AIProvider:
    """Factory function — returns the appropriate provider based on env config."""
    from config import settings

    if settings.AI_API_KEY and settings.effective_ai_provider != "local":
        try:
            from ai.llm_provider import LLMProvider
            return LLMProvider()
        except Exception:
            pass  # Fall through to local provider

    from ai.local_provider import LocalFallbackProvider
    return LocalFallbackProvider()
