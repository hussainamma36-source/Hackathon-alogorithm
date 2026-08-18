"""
Database seeder — populates the database with 8 sample Reels
and realistic interaction data.
"""

import json
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Reel, Interaction


SAMPLE_REELS = [
    {
        "id": "reel_001",
        "title": "Funny College Life: When Exams Hit Different 😂",
        "description": "A relatable college life reel showing the chaos of exam season, all-nighters, and campus food drama. Pure entertainment.",
        "transcript": "It's 3am, the exam is in 5 hours, and I just realized I've been studying the wrong chapter. Classic college experience. The library is full, the vending machine only has Doritos, and somehow, we will survive. Tag your study group below!",
        "category": "Entertainment",
        "creator": "CampusVibes",
        "duration": 28,
        "hashtags": "college,student,examseason,campuslife,funny,relatable",
        "technical_level": "None",
        "educational_value": 0.05,
        "engagement_score": 0.75,
        "topic": "College Life",
        "subtopic": "Exam Season Humor",
        "intent": "entertainment",
        "technical_relevance": 0.05,
        "career_relevance": 0.02,
        "hype_score": 0.10,
        "broader_domain": "lifestyle",
        "related_technologies": json.dumps([]),
    },
    {
        "id": "reel_002",
        "title": "Java OOP: When Your Code Actually Works 🎉",
        "description": "A relatable Java programming meme showing the emotions of a developer when object-oriented code finally compiles without errors.",
        "transcript": "When you finally get polymorphism to work and your inheritance chain doesn't throw a NullPointerException... *chef's kiss*. Java developers, you know the feeling. That moment when the JVM just lets you live for once. Drop a like if you've been personally victimized by Java's verbosity.",
        "category": "Programming",
        "creator": "JavaDevMemes",
        "duration": 22,
        "hashtags": "java,programming,oop,developer,coding,meme,softwaredeveloper",
        "technical_level": "Beginner",
        "educational_value": 0.45,
        "engagement_score": 0.82,
        "topic": "Java Programming",
        "subtopic": "Object-Oriented Programming",
        "intent": "entertainment_with_education",
        "technical_relevance": 0.75,
        "career_relevance": 0.60,
        "hype_score": 0.15,
        "broader_domain": "programming",
        "related_technologies": json.dumps(["Java", "OOP", "JVM"]),
    },
    {
        "id": "reel_003",
        "title": "Day in the Life of a Software Engineer at Big Tech",
        "description": "Follow along a real day at a top tech company — standups, code reviews, lunch, deep work sessions, and work-life balance reality check.",
        "transcript": "It's 9am and our standup just started. I pushed a PR at 11pm last night that's got 3 comments already. After standup, I've got 2 hours of deep work on this new microservice. Then lunch, then code review for two junior devs. The reality is, it's not all ping pong tables. There's real, complex problem solving every day. But also, the ping pong table is nice.",
        "category": "Career",
        "creator": "TechLifeTV",
        "duration": 58,
        "hashtags": "softwareengineer,bigtech,dayinthelife,techcareer,developer,coding,worklifebalance",
        "technical_level": "None",
        "educational_value": 0.65,
        "engagement_score": 0.88,
        "topic": "Software Engineer Lifestyle",
        "subtopic": "Tech Career Reality",
        "intent": "career_insight",
        "technical_relevance": 0.70,
        "career_relevance": 0.90,
        "hype_score": 0.20,
        "broader_domain": "developer_career",
        "related_technologies": json.dumps(["Software Engineering", "Microservices"]),
    },
    {
        "id": "reel_004",
        "title": "POV: Your Coding Interview Asks You to Reverse a Linked List",
        "description": "A coding interview joke that hits too close to home for every developer who has sweated through technical whiteboard interviews.",
        "transcript": "Interviewer: Can you reverse a linked list on the whiteboard? Me internally: I've been reversing linked lists in LeetCode for 6 months and STILL panic. Me externally: Sure, no problem. *writes wrong solution* Interviewer: Take your time. Me: *deletes everything* Me again: Actually, can I use Python? Every. Single. Interview.",
        "category": "Career",
        "creator": "LeetCodeLaughs",
        "duration": 35,
        "hashtags": "codinginterview,linkedlist,leetcode,dsa,faang,technicalinterview,softwareengineer",
        "technical_level": "Intermediate",
        "educational_value": 0.60,
        "engagement_score": 0.85,
        "topic": "Coding Interview",
        "subtopic": "Data Structures",
        "intent": "entertainment_with_education",
        "technical_relevance": 0.80,
        "career_relevance": 0.85,
        "hype_score": 0.10,
        "broader_domain": "technical_interviews",
        "related_technologies": json.dumps(["DSA", "LeetCode", "Algorithms"]),
    },
    {
        "id": "reel_005",
        "title": "Best Laptops for Developers in 2024: MacBook vs ThinkPad vs Framework",
        "description": "An honest comparison of the top developer laptops. Build quality, battery, performance, Linux support, and value for money — no sponsorships.",
        "transcript": "Let's compare the MacBook Pro M3, ThinkPad X1 Carbon, and Framework 16 for developers. MacBook wins on battery and build quality but is expensive and closed ecosystem. ThinkPad is legendary keyboard, great Linux support, replaceable parts. Framework is the modular dream — right-to-repair, upgradeable RAM. For most developers I'd say M3 for Mac users, ThinkPad X1 for Linux purists. Budget pick: the Framework is compelling if you're comfortable with setup.",
        "category": "Hardware",
        "creator": "DevGearReview",
        "duration": 74,
        "hashtags": "laptop,developer,macbook,thinkpad,framework,techreview,programming,devtools",
        "technical_level": "Beginner",
        "educational_value": 0.55,
        "engagement_score": 0.78,
        "topic": "Laptop Comparison",
        "subtopic": "Developer Hardware",
        "intent": "consumer_guide",
        "technical_relevance": 0.65,
        "career_relevance": 0.40,
        "hype_score": 0.20,
        "broader_domain": "computer_hardware",
        "related_technologies": json.dumps(["MacBook M3", "ThinkPad", "Framework"]),
    },
    {
        "id": "reel_006",
        "title": "How Neural Networks Actually Learn: Backpropagation Explained",
        "description": "A clear educational breakdown of how neural networks use backpropagation and gradient descent to learn from data — no PhD required.",
        "transcript": "Forget the magic. Here's how neural networks actually learn. Step 1: forward pass — data flows through layers producing a prediction. Step 2: calculate the error against the real answer. Step 3: backpropagate — send the error signal backwards through the network, adjusting weights using gradient descent. The learning rate controls how big each adjustment is. Too large and it oscillates. Too small and it learns slowly. That's it. That's the entire learning algorithm. Everything else — CNNs, Transformers, LSTMs — is just a variation of this.",
        "category": "AI/ML",
        "creator": "NeuralNinjas",
        "duration": 91,
        "hashtags": "machinelearning,neuralnetwork,deeplearning,ai,python,backpropagation,gradientdescent",
        "technical_level": "Intermediate",
        "educational_value": 0.92,
        "engagement_score": 0.80,
        "topic": "Machine Learning",
        "subtopic": "Neural Networks",
        "intent": "education",
        "technical_relevance": 0.95,
        "career_relevance": 0.85,
        "hype_score": 0.08,
        "broader_domain": "ai_ml",
        "related_technologies": json.dumps(["Neural Networks", "PyTorch", "Python", "Deep Learning"]),
    },
    {
        "id": "reel_007",
        "title": "The Zero-Day Exploit That Took Down 3 Major Banks",
        "description": "Breaking down a real-world zero-day exploit — how attackers found the vulnerability, how it was used, and what defenders could have done differently.",
        "transcript": "In 2023, three European banks had their transaction systems breached through a zero-day in their third-party authentication library. The attacker discovered an unpatched buffer overflow vulnerability in a widely used JWT validation library. By sending a crafted token, they could bypass authentication entirely. The fix was a 3-line patch. The damage was millions in fraudulent transactions and months of regulatory scrutiny. Lesson: your security is only as strong as your least-updated dependency.",
        "category": "Cybersecurity",
        "creator": "SecureBytes",
        "duration": 67,
        "hashtags": "cybersecurity,zeroday,hacking,security,banking,exploit,infosec",
        "technical_level": "Intermediate",
        "educational_value": 0.88,
        "engagement_score": 0.83,
        "topic": "Cybersecurity",
        "subtopic": "Zero-Day Exploits",
        "intent": "education",
        "technical_relevance": 0.90,
        "career_relevance": 0.80,
        "hype_score": 0.10,
        "broader_domain": "cybersecurity",
        "related_technologies": json.dumps(["JWT", "Authentication", "Security"]),
    },
    {
        "id": "reel_008",
        "title": "How Kubernetes Orchestrates Your Containers: A Visual Guide",
        "description": "Step-by-step visual explanation of how Kubernetes manages containerized workloads — Pods, Nodes, Deployments, Services, and auto-scaling.",
        "transcript": "Let's demystify Kubernetes. You have your application running in containers — think Docker. You need to run many copies across multiple servers. Kubernetes is the orchestrator that decides where each container runs, restarts failing ones, scales up under load, and manages networking between them. A Pod is the smallest unit — usually one container. Nodes are the machines. A Deployment tells Kubernetes 'I want 5 replicas of this pod.' A Service exposes them behind a stable address. That's the core. Everything else — Ingress, ConfigMaps, Helm charts — is configuration on top of this model.",
        "category": "Cloud",
        "creator": "CloudNativeTV",
        "duration": 83,
        "hashtags": "kubernetes,docker,cloud,devops,containers,k8s,cloudnative,microservices",
        "technical_level": "Intermediate",
        "educational_value": 0.93,
        "engagement_score": 0.81,
        "topic": "Cloud Computing",
        "subtopic": "Container Orchestration",
        "intent": "education",
        "technical_relevance": 0.95,
        "career_relevance": 0.90,
        "hype_score": 0.05,
        "broader_domain": "cloud_computing",
        "related_technologies": json.dumps(["Kubernetes", "Docker", "AWS", "DevOps"]),
    },
]

# Default interaction data representing the "hackathon trap" scenario
TRAP_INTERACTIONS = [
    {
        "reel_id": "reel_002",  # Java meme
        "watched_percentage": 95.0,
        "watch_time": 21,
        "liked": True,
        "saved": False,
        "shared": False,
        "replayed": True,
        "skipped": False,
        "commented": False,
        "clicked_creator": False,
    },
    {
        "reel_id": "reel_003",  # Software engineer lifestyle
        "watched_percentage": 92.0,
        "watch_time": 53,
        "liked": True,
        "saved": True,
        "shared": False,
        "replayed": False,
        "skipped": False,
        "commented": False,
        "clicked_creator": True,
    },
    {
        "reel_id": "reel_004",  # Coding interview joke
        "watched_percentage": 88.0,
        "watch_time": 31,
        "liked": True,
        "saved": False,
        "shared": False,
        "replayed": False,
        "skipped": False,
        "commented": True,
        "clicked_creator": False,
    },
    {
        "reel_id": "reel_005",  # Laptop comparison
        "watched_percentage": 90.0,
        "watch_time": 66,
        "liked": False,
        "saved": True,
        "shared": False,
        "replayed": False,
        "skipped": False,
        "commented": False,
        "clicked_creator": False,
    },
    {
        "reel_id": "reel_001",  # College life
        "watched_percentage": 45.0,
        "watch_time": 13,
        "liked": False,
        "saved": False,
        "shared": False,
        "replayed": False,
        "skipped": True,
        "commented": False,
        "clicked_creator": False,
    },
]


async def seed_database(db: AsyncSession):
    """Seed the database with sample reels and interactions if empty."""

    # Check if already seeded
    result = await db.execute(select(Reel).limit(1))
    if result.scalar_one_or_none():
        return  # Already seeded

    # Insert reels
    for reel_data in SAMPLE_REELS:
        reel = Reel(**reel_data)
        db.add(reel)

    await db.flush()

    # Insert default trap interactions
    base_time = datetime.utcnow() - timedelta(hours=2)
    for i, interaction_data in enumerate(TRAP_INTERACTIONS):
        interaction = Interaction(
            **interaction_data,
            session_id="demo",
            interaction_timestamp=base_time + timedelta(minutes=i * 8),
        )
        db.add(interaction)

    await db.commit()
