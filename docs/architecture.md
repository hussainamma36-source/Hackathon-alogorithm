# ReelMind AI — Architecture Documentation

## System Overview

ReelMind AI is an explainable, multi-stage recommendation agent designed to analyze student short-form Reel viewing interactions, infer broader technical interests, and recommend high-value educational technology content.

```
USER INTERACTION HISTORY
        │
        ▼
CONTENT UNDERSTANDING (Semantic Domain Mapping & Vectors)
        │
        ▼
INTERACTION SIGNAL ANALYSIS (Multi-signal Weighted Matrix)
        │
        ▼
INTEREST INFERENCE (Semantic Neighborhood Traversal)
        │
        ▼
BROADER INTEREST PROFILE (Primary & Secondary Inferred Domains)
        │
        ▼
CANDIDATE TECH CONTENT GENERATION (8 Curated Tech Domains)
        │
        ▼
RELEVANCE SCORING (Domain Match + Edu Value + Career Relevance)
        │
        ▼
QUALITY / HYPE FILTER (Clickbait & Unrealistic Guarantee Penalty)
        │
        ▼
FINAL RECOMMENDATION + EXPLANATION
```

---

## Backend Component Architecture

- **FastAPI Core**: RESTful API framework with async request routing.
- **SQLAlchemy 2.0 (Async)**: Object-relational mapping supporting SQLite (development) and PostgreSQL (production).
- **AI Recommendation Engine**:
  - `LocalFallbackProvider`: Zero-dependency, multi-stage semantic vector engine.
  - `LLMProvider`: Optional integration with OpenAI (GPT-4o), Google Gemini, or Anthropic Claude.
  - `HypeFilter`: Regex and quality signal pattern evaluator.
- **Database Seeder**: Seeds initial 8 sample reels and standard hackathon trap interaction history.

---

## Frontend Architecture

- **Framework**: React 18 + TypeScript + Vite.
- **Styling**: Modern CSS design system with CSS custom properties, glassmorphism, HSL color tokens, and responsive layout grid.
- **State Management**: Zustand store managing active session interactions, live analysis loading stages, and recommendation history.
- **Data Visualization**: Recharts for interest profiles and content quality distribution.

---

## Database Schema (ORM)

1. `reels`: Stores reel metadata, technical levels, educational values, and vector tags.
2. `interactions`: Stores detailed user interaction signals (`watched_percentage`, `liked`, `saved`, `replayed`, `skipped`, etc.).
3. `interest_profiles`: Inferred primary/secondary interests and confidence levels.
4. `recommendations`: Generated output records, scores, explanations, and evidence logs.
5. `feedback`: User rating feedback (useful / too basic / not relevant).
