"""
Content Vectors — Semantic representations of all Reels and recommendation candidates.

This module defines the semantic attribute space used by the recommendation engine.
It deliberately avoids simple keyword matching by mapping content to:
  - Broader domain neighborhoods
  - Intent classifications
  - Topic relatedness scores
  - Technology concept clusters
"""

from typing import Dict, List, Any

# ── Domain Neighborhoods ──────────────────────────────────────────────────────
# Each domain has a set of closely related domains (semantic neighbors).
# Used to expand user interests beyond the literal content they watched.

DOMAIN_NEIGHBORHOODS: Dict[str, List[str]] = {
    "software_engineering": [
        "programming", "developer_career", "system_design", "computer_science",
        "software_architecture", "backend_development", "devops", "algorithms"
    ],
    "programming": [
        "software_engineering", "algorithms", "data_structures", "computer_science",
        "backend_development", "web_development", "open_source"
    ],
    "developer_career": [
        "software_engineering", "technical_interviews", "programming", "workplace_culture",
        "computer_science", "professional_development"
    ],
    "technical_interviews": [
        "algorithms", "data_structures", "developer_career", "programming",
        "software_engineering", "problem_solving"
    ],
    "algorithms": [
        "data_structures", "programming", "computer_science", "technical_interviews",
        "software_engineering", "mathematics"
    ],
    "data_structures": [
        "algorithms", "programming", "computer_science", "software_engineering"
    ],
    "computer_hardware": [
        "computer_science", "software_engineering", "cloud_computing",
        "gpu_computing", "performance_optimization"
    ],
    "ai_ml": [
        "data_science", "python_programming", "cloud_computing", "mathematics",
        "software_engineering", "research"
    ],
    "cloud_computing": [
        "devops", "software_engineering", "computer_hardware", "system_design",
        "backend_development", "infrastructure"
    ],
    "cybersecurity": [
        "networking", "software_engineering", "computer_science", "cryptography",
        "backend_development", "infrastructure"
    ],
    "system_design": [
        "software_architecture", "backend_development", "cloud_computing",
        "software_engineering", "databases", "scalability"
    ],
    "web_development": [
        "programming", "software_engineering", "frontend_development",
        "backend_development", "javascript"
    ],
    "data_science": [
        "ai_ml", "statistics", "python_programming", "research"
    ],
    "college_life": [
        "student_humor", "entertainment", "lifestyle"
    ],
    "lifestyle": [
        "entertainment", "college_life", "humor"
    ],
}

# ── Technology Concept Clusters ───────────────────────────────────────────────
# Maps reel topics to the broader technology ecosystem they belong to.

TECH_CLUSTERS: Dict[str, str] = {
    "Java": "programming",
    "Python": "programming",
    "JavaScript": "web_development",
    "TypeScript": "web_development",
    "C++": "programming",
    "Go": "backend_development",
    "Rust": "programming",
    "DSA": "algorithms",
    "LeetCode": "technical_interviews",
    "System Design": "system_design",
    "AWS": "cloud_computing",
    "GCP": "cloud_computing",
    "Azure": "cloud_computing",
    "Docker": "devops",
    "Kubernetes": "devops",
    "Machine Learning": "ai_ml",
    "Deep Learning": "ai_ml",
    "LLM": "ai_ml",
    "Neural Network": "ai_ml",
    "Cybersecurity": "cybersecurity",
    "Networking": "cybersecurity",
    "SQL": "databases",
    "NoSQL": "databases",
    "API": "backend_development",
    "REST": "backend_development",
    "GraphQL": "backend_development",
    "Laptop": "computer_hardware",
    "GPU": "computer_hardware",
    "CPU": "computer_hardware",
    "Software Engineer": "developer_career",
    "Developer": "developer_career",
    "Coding Interview": "technical_interviews",
    "Resume": "developer_career",
    "GitHub": "software_engineering",
    "Open Source": "open_source",
}

# ── Reel Content Vectors ───────────────────────────────────────────────────────
# Full semantic representation for each of the 8 sample reels.
# These supplement the database metadata for richer semantic analysis.

REEL_VECTORS: Dict[str, Dict[str, Any]] = {
    "reel_001": {
        "id": "reel_001",
        "primary_domain": "lifestyle",
        "secondary_domains": ["college_life", "entertainment"],
        "tech_relevance": 0.05,
        "career_relevance": 0.02,
        "educational_value": 0.08,
        "hype_score": 0.10,
        "difficulty": "None",
        "intent": "entertainment",
        "concept_tags": ["college", "student_life", "humor", "relatable"],
        "tech_concepts": [],
        "broader_interest_signals": ["student", "campus_life"],
        "expansion_domains": ["student_humor", "lifestyle"],
    },
    "reel_002": {
        "id": "reel_002",
        "primary_domain": "programming",
        "secondary_domains": ["software_engineering", "developer_career"],
        "tech_relevance": 0.75,
        "career_relevance": 0.60,
        "educational_value": 0.45,
        "hype_score": 0.15,
        "difficulty": "Beginner",
        "intent": "entertainment_with_education",
        "concept_tags": ["java", "programming_meme", "coding", "oop", "developer_humor"],
        "tech_concepts": ["Java", "OOP", "Programming"],
        "broader_interest_signals": ["programming", "developer_community", "software_engineering"],
        "expansion_domains": ["programming", "software_engineering", "developer_career"],
    },
    "reel_003": {
        "id": "reel_003",
        "primary_domain": "developer_career",
        "secondary_domains": ["software_engineering", "workplace_culture"],
        "tech_relevance": 0.70,
        "career_relevance": 0.90,
        "educational_value": 0.65,
        "hype_score": 0.20,
        "difficulty": "None",
        "intent": "career_insight",
        "concept_tags": ["software_engineer", "day_in_life", "tech_job", "big_tech", "developer_lifestyle"],
        "tech_concepts": ["Software Engineer", "Developer"],
        "broader_interest_signals": ["tech_career", "developer_lifestyle", "software_engineering"],
        "expansion_domains": ["developer_career", "software_engineering", "technical_interviews"],
    },
    "reel_004": {
        "id": "reel_004",
        "primary_domain": "technical_interviews",
        "secondary_domains": ["developer_career", "programming", "algorithms"],
        "tech_relevance": 0.80,
        "career_relevance": 0.85,
        "educational_value": 0.60,
        "hype_score": 0.10,
        "difficulty": "Intermediate",
        "intent": "entertainment_with_education",
        "concept_tags": ["coding_interview", "leetcode", "whiteboard", "dsa", "faang"],
        "tech_concepts": ["Coding Interview", "LeetCode", "DSA", "Algorithms"],
        "broader_interest_signals": ["technical_interviews", "algorithms", "developer_career"],
        "expansion_domains": ["technical_interviews", "algorithms", "data_structures", "developer_career"],
    },
    "reel_005": {
        "id": "reel_005",
        "primary_domain": "computer_hardware",
        "secondary_domains": ["software_engineering", "performance_optimization"],
        "tech_relevance": 0.65,
        "career_relevance": 0.40,
        "educational_value": 0.55,
        "hype_score": 0.20,
        "difficulty": "Beginner",
        "intent": "consumer_guide",
        "concept_tags": ["laptop", "developer_laptop", "macbook", "thinkpad", "tech_specs", "ram", "cpu"],
        "tech_concepts": ["Laptop", "CPU", "GPU"],
        "broader_interest_signals": ["computer_hardware", "developer_tools", "software_engineering"],
        "expansion_domains": ["computer_hardware", "software_engineering"],
    },
    "reel_006": {
        "id": "reel_006",
        "primary_domain": "ai_ml",
        "secondary_domains": ["data_science", "cloud_computing", "software_engineering"],
        "tech_relevance": 0.95,
        "career_relevance": 0.85,
        "educational_value": 0.90,
        "hype_score": 0.15,
        "difficulty": "Intermediate",
        "intent": "education",
        "concept_tags": ["machine_learning", "neural_networks", "deep_learning", "python", "model_training"],
        "tech_concepts": ["Machine Learning", "Neural Network", "Python", "AI"],
        "broader_interest_signals": ["ai_ml", "data_science", "software_engineering"],
        "expansion_domains": ["ai_ml", "data_science", "cloud_computing"],
    },
    "reel_007": {
        "id": "reel_007",
        "primary_domain": "cybersecurity",
        "secondary_domains": ["networking", "software_engineering"],
        "tech_relevance": 0.90,
        "career_relevance": 0.80,
        "educational_value": 0.85,
        "hype_score": 0.10,
        "difficulty": "Intermediate",
        "intent": "education",
        "concept_tags": ["cybersecurity", "hacking", "data_breach", "encryption", "zero_day"],
        "tech_concepts": ["Cybersecurity", "Networking", "Encryption"],
        "broader_interest_signals": ["cybersecurity", "networking", "software_security"],
        "expansion_domains": ["cybersecurity", "networking", "software_engineering"],
    },
    "reel_008": {
        "id": "reel_008",
        "primary_domain": "cloud_computing",
        "secondary_domains": ["devops", "system_design", "backend_development"],
        "tech_relevance": 0.95,
        "career_relevance": 0.90,
        "educational_value": 0.92,
        "hype_score": 0.05,
        "difficulty": "Intermediate",
        "intent": "education",
        "concept_tags": ["cloud", "aws", "kubernetes", "docker", "microservices", "devops"],
        "tech_concepts": ["AWS", "Docker", "Kubernetes", "Cloud Computing"],
        "broader_interest_signals": ["cloud_computing", "devops", "system_design"],
        "expansion_domains": ["cloud_computing", "devops", "system_design", "backend_development"],
    },
}

# ── Recommendation Candidates ─────────────────────────────────────────────────
# 8 high-quality tech recommendation candidates.
# These are evaluated against the inferred interest profile.

RECOMMENDATION_CANDIDATES: List[Dict[str, Any]] = [
    {
        "id": "rec_001",
        "title": "DSA Interview Patterns for Software Engineers",
        "description": "Master the 15 most critical data structures and algorithm patterns asked in FAANG interviews. Covers arrays, graphs, dynamic programming, and sliding window with real examples.",
        "category": "DSA",
        "difficulty": "Intermediate",
        "educational_value": 0.95,
        "hype_score": 0.05,
        "technical_depth": 0.90,
        "career_relevance": 0.95,
        "primary_domain": "algorithms",
        "related_interests": ["technical_interviews", "programming", "developer_career", "data_structures"],
        "related_domains": ["algorithms", "data_structures", "technical_interviews", "software_engineering"],
        "expansion_value": 0.85,  # how much this expands vs repeats user's existing interests
        "quality_indicators": ["structured_curriculum", "practical_examples", "career_aligned"],
    },
    {
        "id": "rec_002",
        "title": "Introduction to System Design: Scalability Fundamentals",
        "description": "Learn how to design systems that scale to millions of users. Covers load balancing, caching, databases, microservices, and distributed systems from first principles.",
        "category": "HLD",
        "difficulty": "Intermediate",
        "educational_value": 0.93,
        "hype_score": 0.05,
        "technical_depth": 0.88,
        "career_relevance": 0.92,
        "primary_domain": "system_design",
        "related_interests": ["software_engineering", "cloud_computing", "backend_development", "algorithms"],
        "related_domains": ["system_design", "software_architecture", "cloud_computing", "backend_development"],
        "expansion_value": 0.90,
        "quality_indicators": ["conceptual_depth", "real_world_examples", "career_aligned"],
    },
    {
        "id": "rec_003",
        "title": "Backend Engineering: Building APIs That Scale",
        "description": "Deep dive into backend architecture patterns. REST vs GraphQL, authentication flows, database optimization, caching strategies, and API security fundamentals.",
        "category": "Career",
        "difficulty": "Intermediate",
        "educational_value": 0.90,
        "hype_score": 0.08,
        "technical_depth": 0.85,
        "career_relevance": 0.88,
        "primary_domain": "backend_development",
        "related_interests": ["programming", "software_engineering", "system_design", "web_development"],
        "related_domains": ["backend_development", "system_design", "software_engineering", "web_development"],
        "expansion_value": 0.80,
        "quality_indicators": ["practical_focus", "industry_standards", "code_examples"],
    },
    {
        "id": "rec_004",
        "title": "How Cloud Applications Are Architected",
        "description": "Understand how modern applications leverage cloud infrastructure. AWS/GCP services, containerization, serverless functions, and cloud-native design patterns explained visually.",
        "category": "Cloud",
        "difficulty": "Intermediate",
        "educational_value": 0.92,
        "hype_score": 0.08,
        "technical_depth": 0.87,
        "career_relevance": 0.90,
        "primary_domain": "cloud_computing",
        "related_interests": ["software_engineering", "system_design", "devops", "computer_hardware"],
        "related_domains": ["cloud_computing", "devops", "system_design", "backend_development"],
        "expansion_value": 0.88,
        "quality_indicators": ["conceptual_clarity", "architecture_focused", "career_aligned"],
    },
    {
        "id": "rec_005",
        "title": "Secure Authentication: From Basics to OAuth 2.0",
        "description": "Understand how modern authentication works: sessions, JWT tokens, OAuth 2.0 flows, multi-factor authentication, and common security vulnerabilities developers must know.",
        "category": "Cybersecurity",
        "difficulty": "Intermediate",
        "educational_value": 0.91,
        "hype_score": 0.05,
        "technical_depth": 0.88,
        "career_relevance": 0.87,
        "primary_domain": "cybersecurity",
        "related_interests": ["software_engineering", "backend_development", "networking"],
        "related_domains": ["cybersecurity", "backend_development", "software_engineering"],
        "expansion_value": 0.85,
        "quality_indicators": ["security_focused", "practical_implementation", "industry_standard"],
    },
    {
        "id": "rec_006",
        "title": "How GPUs Accelerate AI: Inside the Hardware",
        "description": "Explore why GPUs are essential for AI workloads. Covers parallel processing, CUDA architecture, VRAM, tensor operations, and the difference between consumer and data-center GPUs.",
        "category": "AI",
        "difficulty": "Intermediate",
        "educational_value": 0.89,
        "hype_score": 0.10,
        "technical_depth": 0.85,
        "career_relevance": 0.82,
        "primary_domain": "ai_ml",
        "related_interests": ["computer_hardware", "ai_ml", "data_science", "software_engineering"],
        "related_domains": ["ai_ml", "computer_hardware", "data_science"],
        "expansion_value": 0.88,
        "quality_indicators": ["hardware_software_bridge", "conceptual_depth", "timely_topic"],
    },
    {
        "id": "rec_007",
        "title": "Understanding LLM Application Architecture",
        "description": "How are LLM-powered applications actually built? Covers retrieval-augmented generation, prompt engineering patterns, context windows, embedding databases, and production deployment considerations.",
        "category": "AI",
        "difficulty": "Advanced",
        "educational_value": 0.94,
        "hype_score": 0.12,
        "technical_depth": 0.92,
        "career_relevance": 0.90,
        "primary_domain": "ai_ml",
        "related_interests": ["software_engineering", "backend_development", "system_design", "data_science"],
        "related_domains": ["ai_ml", "system_design", "backend_development", "software_engineering"],
        "expansion_value": 0.92,
        "quality_indicators": ["architecture_focused", "avoids_hype", "technically_rigorous"],
    },
    {
        "id": "rec_008",
        "title": "Java Backend Architecture: Spring Boot in Production",
        "description": "Build production-grade Java backends with Spring Boot. Covers dependency injection, REST APIs, JPA, transaction management, security, and common patterns used in enterprise applications.",
        "category": "Java",
        "difficulty": "Intermediate",
        "educational_value": 0.88,
        "hype_score": 0.05,
        "technical_depth": 0.85,
        "career_relevance": 0.85,
        "primary_domain": "programming",
        "related_interests": ["programming", "backend_development", "software_engineering"],
        "related_domains": ["programming", "backend_development", "software_engineering"],
        "expansion_value": 0.65,  # lower — closest to what user already watched
        "quality_indicators": ["language_specific", "production_ready", "enterprise_patterns"],
    },
]
