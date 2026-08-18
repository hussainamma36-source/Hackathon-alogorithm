# AI Recommendation Engine & Interest Inference

## Core Philosophy

"We don't recommend what you watched. We infer why you engaged with it."

---

## The Built-In Trap Problem

A naive keyword-matching algorithm operates as follows:
- User watches: **Java programming meme**
- Shallow rule: `if "Java" in text -> recommend Java`
- Output: **"Another Java Meme"**

### Why This Fails Students
Keyword matching traps students in content echo chambers. Watching a Java meme does not mean a student only wants Java memes; it indicates they are engaged in programming and developer culture.

---

## ReelMind AI Approach: Semantic Neighborhood Expansion

ReelMind AI analyzes multi-reel interaction signals across 5 primary factors:

1. **Interaction Weighted Scoring**:
   - `watched_percentage` (30%)
   - `saved` (25%) — strong signal of lasting value
   - `liked` (20%)
   - `replayed` (15%)
   - `skipped` (-35%) — strong penalty signal

2. **Domain Neighborhood Traversal**:
   When a user interacts with Java memes + coding interview jokes + software engineer lifestyle + laptop specs, the agent traverses the semantic neighborhood:
   `Java` -> `Programming` -> `Developer Career` -> `Technical Interviews` -> `Software Engineering`

   Resulting Inferred Interest: **Software Engineering / Technology**

3. **Candidate Scoring Matrix**:
   `Score = (DomainMatch * 0.30) + (EduValue * 0.20) + (CareerRelevance * 0.15) + (TechDepth * 0.15) + (ExpansionValue * 0.10) + (Quality * 0.10)`

4. **Dedicated Hype & Clickbait Filter**:
   Down-ranks content containing exaggerated claims:
   - "Get a job in 7 days"
   - "Guaranteed job"
   - "10 AI tools that will get you hired instantly"
