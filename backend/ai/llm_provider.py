"""
LLM Provider — Uses external AI APIs when AI_API_KEY is configured.
Falls back to LocalFallbackProvider if the API call fails.
"""

import json
from typing import Any, Dict, List

from ai.provider import AIProvider
from ai.content_vectors import RECOMMENDATION_CANDIDATES


class LLMProvider(AIProvider):
    """
    AI provider that uses an external LLM for semantic reasoning.
    Supports OpenAI, Google Gemini, and Anthropic via env config.
    """

    @property
    def provider_name(self) -> str:
        from config import settings
        return f"llm_{settings.AI_PROVIDER}"

    def _get_client(self):
        from config import settings
        provider = settings.effective_ai_provider

        if provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=settings.AI_API_KEY)
            return ("gemini", genai.GenerativeModel(settings.AI_MODEL or "gemini-1.5-flash"))
        elif provider == "anthropic":
            import anthropic
            return ("anthropic", anthropic.Anthropic(api_key=settings.AI_API_KEY))
        else:
            import openai
            return ("openai", openai.AsyncOpenAI(api_key=settings.AI_API_KEY))

    async def analyze_interests(
        self,
        interaction_history: List[Dict[str, Any]],
        reel_vectors: Dict[str, Any],
    ) -> Dict[str, Any]:
        try:
            return await self._llm_analyze(interaction_history, reel_vectors)
        except Exception as e:
            # Fall back to local provider
            from ai.local_provider import LocalFallbackProvider
            return await LocalFallbackProvider().analyze_interests(interaction_history, reel_vectors)

    async def generate_recommendation(
        self,
        interest_profile: Dict[str, Any],
        candidates: List[Dict[str, Any]],
        interaction_history: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        try:
            return await self._llm_recommend(interest_profile, candidates, interaction_history)
        except Exception:
            from ai.local_provider import LocalFallbackProvider
            return await LocalFallbackProvider().generate_recommendation(
                interest_profile, candidates, interaction_history
            )

    async def _llm_analyze(self, interaction_history, reel_vectors) -> Dict[str, Any]:
        from config import settings

        history_summary = json.dumps(interaction_history, indent=2, default=str)

        prompt = f"""
You are an AI agent that analyzes student Reel interaction history to infer their broader technology interests.

INTERACTION HISTORY:
{history_summary}

TASK:
1. Analyze the interaction signals (watch_percentage, liked, saved, replayed, etc.)
2. Look beyond surface topics — infer the DEEPER interest pattern
3. If a student watches Java memes + coding interview jokes + software engineer lifestyles, 
   their deeper interest is "Software Engineering" NOT just "Java"

Respond with ONLY valid JSON in this exact format:
{{
  "primary_interest": "Software Engineering",
  "secondary_interests": ["Programming", "Technical Interview Prep", "Developer Career"],
  "interest_scores": {{
    "Software Engineering": 0.85,
    "Programming": 0.72,
    "Technical Interview Prep": 0.65
  }},
  "confidence": "High",
  "confidence_score": 0.82,
  "evidence": [
    "Strong engagement with programming and career content across multiple Reels",
    "Saved and replayed content indicates lasting interest"
  ],
  "raw_domain_scores": {{
    "software_engineering": 0.85,
    "programming": 0.72
  }}
}}
"""

        provider_type, client = self._get_client()
        response_text = ""

        if provider_type == "gemini":
            response = client.generate_content(prompt)
            response_text = response.text
        elif provider_type == "anthropic":
            message = client.messages.create(
                model=settings.AI_MODEL or "claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            response_text = message.content[0].text
        else:
            response = await client.chat.completions.create(
                model=settings.AI_MODEL or "gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
            )
            response_text = response.choices[0].message.content

        # Clean markdown code blocks if present
        response_text = response_text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]

        return json.loads(response_text)

    async def _llm_recommend(self, interest_profile, candidates, interaction_history) -> Dict[str, Any]:
        from config import settings

        candidates_summary = json.dumps(
            [{k: v for k, v in c.items() if k != "quality_indicators"} for c in candidates],
            indent=2,
        )

        prompt = f"""
You are an AI recommendation agent. Given a student's interest profile and a list of tech content candidates, 
select the BEST recommendation.

INTEREST PROFILE:
{json.dumps(interest_profile, indent=2)}

CANDIDATES:
{candidates_summary}

RULES:
- Do NOT recommend content just because it matches a surface keyword (e.g., do not just recommend Java content to someone who watched a Java meme)
- Prefer content that EXPANDS the student's interest into adjacent, useful technical topics
- Penalize any candidate with hype_score > 0.4
- Prioritize educational_value and career_relevance
- Select the candidate that best serves the student's broader technical growth

Respond with ONLY valid JSON:
{{
  "recommended_id": "rec_001",
  "relevance_score": 0.87,
  "reason": "Detailed explanation of why this recommendation serves the student's broader interest...",
  "alternatives": [
    {{"id": "rec_002", "reason": "...", "score": 0.75}},
    {{"id": "rec_003", "reason": "...", "score": 0.68}}
  ]
}}
"""

        provider_type, client = self._get_client()
        response_text = ""

        if provider_type == "gemini":
            response = client.generate_content(prompt)
            response_text = response.text
        elif provider_type == "anthropic":
            message = client.messages.create(
                model=settings.AI_MODEL or "claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            response_text = message.content[0].text
        else:
            response = await client.chat.completions.create(
                model=settings.AI_MODEL or "gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
            )
            response_text = response.choices[0].message.content

        response_text = response_text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]

        result = json.loads(response_text)

        # Map back to full candidate
        recommended_id = result.get("recommended_id", "rec_001")
        recommended = next((c for c in candidates if c["id"] == recommended_id), candidates[0])

        return {
            "recommended": recommended,
            "relevance_score": result.get("relevance_score", 0.75),
            "hype_score": recommended.get("hype_score", 0.1),
            "quality_score": 1.0 - recommended.get("hype_score", 0.1),
            "reason": result.get("reason", "AI-generated recommendation"),
            "pipeline_stages": [],
            "alternatives": result.get("alternatives", []),
            "score_breakdown": {},
        }
