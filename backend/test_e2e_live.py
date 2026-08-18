"""
End-to-End Live Verification Script for ReelMind AI API & Recommendation Pipeline.
Tests the actual running FastAPI backend server at http://127.0.0.1:8000.
"""

import httpx
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api"
SESSION_ID = "live_e2e_test_session"


def log(msg, symbol="[INFO]"):
    print(f"{symbol} {msg}")


def main():
    print("=" * 70)
    print("REELMIND AI -- LIVE END-TO-END VERIFICATION SUITE")
    print("=" * 70)

    client = httpx.Client(timeout=10.0)

    # 1. Health check
    log("Testing GET /api/health...", "[1]")
    res = client.get(f"{BASE_URL}/health")
    assert res.status_code == 200, f"Health failed: {res.text}"
    health_data = res.json()
    log(f"Health OK! Provider: {health_data['ai_provider']}, DB: {health_data['database']}", "[OK]")

    # 2. Get Reels
    log("Testing GET /api/reels...", "[2]")
    res = client.get(f"{BASE_URL}/reels")
    assert res.status_code == 200, f"Get Reels failed: {res.text}"
    reels = res.json()
    assert len(reels) >= 8, f"Expected 8 sample reels, got {len(reels)}"
    log(f"Fetched {len(reels)} preloaded Reels successfully", "[OK]")

    # 3. Post Trap Interaction Data
    log("Testing POST /api/interactions (Hackathon Trap Scenario)...", "[3]")
    trap_data = [
        # Java meme
        {"reel_id": "reel_002", "session_id": SESSION_ID, "watched_percentage": 95.0, "watch_time": 21, "liked": True, "replayed": True},
        # Software engineer lifestyle
        {"reel_id": "reel_003", "session_id": SESSION_ID, "watched_percentage": 92.0, "watch_time": 53, "liked": True, "saved": True, "clicked_creator": True},
        # Coding interview joke
        {"reel_id": "reel_004", "session_id": SESSION_ID, "watched_percentage": 88.0, "watch_time": 31, "liked": True, "commented": True},
        # Laptop comparison
        {"reel_id": "reel_005", "session_id": SESSION_ID, "watched_percentage": 90.0, "watch_time": 66, "saved": True},
        # College life (skipped)
        {"reel_id": "reel_001", "session_id": SESSION_ID, "watched_percentage": 45.0, "watch_time": 13, "skipped": True},
    ]

    for interaction in trap_data:
        res = client.post(f"{BASE_URL}/interactions", json=interaction)
        assert res.status_code == 200, f"Interaction failed: {res.text}"

    log(f"Posted {len(trap_data)} interaction signals to session '{SESSION_ID}'", "[OK]")

    # 4. Fetch interactions
    log("Testing GET /api/interactions...", "[4]")
    res = client.get(f"{BASE_URL}/interactions", params={"session_id": SESSION_ID})
    assert res.status_code == 200
    saved_interactions = res.json()
    assert len(saved_interactions) == len(trap_data)
    log(f"Retrieved {len(saved_interactions)} saved interactions from DB", "[OK]")

    # 5. Run Full AI Pipeline
    log("Testing POST /api/analyze (Full Recommendation Pipeline)...", "[5]")
    res = client.post(f"{BASE_URL}/analyze", json={"session_id": SESSION_ID})
    assert res.status_code == 200, f"Analyze failed: {res.text}"
    analysis = res.json()

    print("\n" + "-" * 70)
    print("ANALYZE RESPONSE VERIFICATION:")
    print("-" * 70)
    print(f"  * CURRENT REEL:                {analysis['current_reel']}")
    print(f"  * INTEREST DETECTED:           {analysis['interest_detected']}")
    print(f"  * RECOMMENDED TECH REEL:       {analysis['recommended_reel']}")
    print(f"  * CATEGORY:                    {analysis['category']}")
    print(f"  * DIFFICULTY:                  {analysis['difficulty']}")
    print(f"  * CONFIDENCE:                  {analysis['confidence']} ({analysis['confidence_score']:.2f})")
    print(f"  * RELEVANCE SCORE:             {analysis['relevance_score']:.2f}")
    print(f"  * HYPE SCORE:                  {analysis['hype_score']:.2f}")
    print(f"  * QUALITY SCORE:               {analysis['quality_score']:.2f}")
    print(f"  * SHALLOW COMPARISON (TRAP):  {analysis['shallow_recommendation']}")
    print(f"  * WHY THIS RECOMMENDATION:\n    {analysis['recommendation_reason']}")
    print("  * EVIDENCE LOG:")
    for ev in analysis['interest_evidence']:
        print(f"    - {ev}")
    print("-" * 70 + "\n")

    # Verify Required Conceptual Fields & Trap Conditions
    assert "java" not in analysis['interest_detected'].lower(), (
        f"TRAP FAILED: AI detected narrow 'Java' interest: {analysis['interest_detected']}"
    )
    assert any(term in analysis['interest_detected'].lower() for term in ["software", "engineering", "technology", "developer", "career", "programming"]), (
        f"Expected broader technology/software engineering interest, got: {analysis['interest_detected']}"
    )
    assert analysis['recommended_reel'] != "Another Java Programming Meme Compilation", (
        "TRAP FAILED: Engine returned shallow Java recommendation!"
    )
    assert len(analysis['interest_evidence']) >= 2, "Expected evidence from multiple interactions"
    assert analysis['category'] in ["AI", "DSA", "Java", "HLD", "Cybersecurity", "Cloud", "Hardware", "Career", "Other"]
    assert analysis['difficulty'] in ["Beginner", "Intermediate", "Advanced"]
    assert analysis['confidence'] in ["High", "Medium", "Low"]
    assert analysis['recommendation_reason'], "Expected human-readable explanation"

    log("TRAP SCENARIO VERIFIED: AI correctly inferred Software Engineering / Technology (NOT narrow Java)!", "[SUCCESS]")

    # 6. Fetch Interest Profile
    log("Testing GET /api/interests...", "[6]")
    res = client.get(f"{BASE_URL}/interests", params={"session_id": SESSION_ID})
    assert res.status_code == 200
    profile = res.json()
    log(f"Fetched Interest Profile. Primary: {profile['primary_interest']}, Secondary: {profile['secondary_interests']}", "[OK]")

    # 7. Fetch History
    log("Testing GET /api/history...", "[7]")
    res = client.get(f"{BASE_URL}/history", params={"session_id": SESSION_ID})
    assert res.status_code == 200
    history = res.json()
    assert len(history) >= 1
    log(f"Fetched Recommendation History: {len(history)} record(s)", "[OK]")

    # 8. Submit Feedback
    log("Testing POST /api/feedback...", "[8]")
    rec_id = analysis['recommendation_id']
    res = client.post(f"{BASE_URL}/feedback", json={
        "recommendation_id": rec_id,
        "session_id": SESSION_ID,
        "rating": "useful"
    })
    assert res.status_code == 200
    log(f"Submitted feedback for recommendation #{rec_id} successfully", "[OK]")

    print("\n" + "=" * 70)
    print("ALL LIVE END-TO-END VERIFICATION CHECKS PASSED PERFECTLY!")
    print("=" * 70)



if __name__ == "__main__":
    main()
