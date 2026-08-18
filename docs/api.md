# API Documentation

Base URL: `http://localhost:8000/api`

## Endpoints Summary

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | System status & active AI provider |
| `GET` | `/reels` | List all sample preloaded Reels |
| `GET` | `/reels/{id}` | Get specific Reel metadata |
| `POST` | `/interactions` | Record user interaction signal |
| `GET` | `/interactions` | Get interaction history for session |
| `POST` | `/analyze` | Execute full recommendation pipeline |
| `GET` | `/interests` | Get latest inferred interest profile |
| `GET` | `/recommendations` | Get past recommendation list |
| `GET` | `/history` | Audit log of recommendations |
| `POST` | `/feedback` | Submit rating feedback |

---

## Detailed Schemas

### `POST /api/analyze`
**Request Body**:
```json
{
  "session_id": "default"
}
```

**Response**:
```json
{
  "current_reel": "Java Programming Meme",
  "interest_detected": "Software Engineering / Technology",
  "interest_evidence": [
    "High watch completion across programming content",
    "Saved developer career content"
  ],
  "recommended_reel": "DSA Interview Patterns for Software Engineers",
  "category": "DSA",
  "recommendation_reason": "Inferred broader Software Engineering interest instead of repeating Java memes.",
  "difficulty": "Intermediate",
  "confidence": "High",
  "confidence_score": 0.85,
  "relevance_score": 0.92,
  "hype_score": 0.05,
  "quality_score": 0.95
}
```
