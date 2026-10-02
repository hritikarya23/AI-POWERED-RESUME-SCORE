"""Unit and integration tests for scoring, skills extraction, and ATS analysis."""

import pytest
from app.services.ats_analyzer import (
    analyze_ats,
    detect_action_verbs,
    detect_quantifiable_metrics,
    detect_sections,
)
from app.services.scorer import score_resume
from app.services.semantic import SemanticMatcher, split_into_meaningful_sentences
from app.services.skills_db import extract_skills


def test_skills_extraction_and_aliases():
    sample_text = """
    Proficient in Python, C++, and Go. Extensive experience with k8s, Docker, and AWS.
    Built REST APIs using FastAPI and postgresql database. Implemented CI/CD pipelines.
    """
    skills = extract_skills(sample_text)

    assert "Python" in skills
    assert "C++" in skills
    assert "Go" in skills
    assert "Kubernetes" in skills  # k8s -> Kubernetes
    assert "PostgreSQL" in skills  # postgresql -> PostgreSQL
    assert "Docker" in skills
    assert "AWS" in skills
    assert "FastAPI" in skills
    assert "CI/CD" in skills
    assert "REST API" in skills


def test_ats_analyzer_components():
    sample_resume = """
    Johnathan Doe
    john.doe@techfirm.io | (555) 345-6789 | github.com/johndoe
    
    PROFESSIONAL SUMMARY
    Accomplished software engineer with 5 years experience designing scalable systems.
    
    WORK EXPERIENCE
    Senior Developer | Acme Corp (2020 - 2024)
    • Architected and deployed microservices reducing API latency by 35% across 2,000,000 requests.
    • Spearheaded database migration that saved $120,000 annually.
    • Led a team of 6 engineers using Agile methodologies.
    
    EDUCATION
    B.S. in Computer Science, Stanford University
    
    TECHNICAL SKILLS
    Python, FastAPI, Docker, PostgreSQL
    """
    ats_result = analyze_ats(sample_resume)

    assert ats_result["score"] >= 75.0
    assert "Experience" in ats_result["sections_found"]
    assert "Education" in ats_result["sections_found"]
    assert "Skills" in ats_result["sections_found"]
    assert ats_result["contact_info"]["has_email"] is True
    assert ats_result["contact_info"]["has_phone"] is True
    assert ats_result["contact_info"]["has_linkedin_github"] is True
    assert ats_result["action_verbs_count"] >= 3
    assert len(ats_result["metrics_found"]) >= 2


def test_semantic_matcher():
    matcher = SemanticMatcher.get_instance()
    text1 = "Senior backend engineer with deep experience in Python, FastAPI, and Kubernetes."
    text2 = "We need an experienced Python developer to build APIs with FastAPI and manage Kubernetes clusters."
    text3 = "Registered nurse providing patient care in pediatric hospital emergency room."

    sim_high = matcher.compute_similarity(text1, text2)
    sim_low = matcher.compute_similarity(text1, text3)

    assert sim_high > 0.50
    assert sim_high > sim_low


def test_score_resume_end_to_end():
    job_description = """
    Senior Python Backend Engineer
    Requirements:
    • 4+ years experience with Python and FastAPI.
    • Strong knowledge of PostgreSQL and Redis caching.
    • Experience containerizing with Docker and deploying to AWS.
    • Proven track record designing scalable REST APIs.
    """

    resume_text = """
    Alex Rivera
    alex.rivera@example.com | (555) 234-5678 | github.com/alexrivera
    
    PROFESSIONAL SUMMARY
    Senior Software Engineer with 5 years experience building distributed backends in Python.
    
    TECHNICAL SKILLS
    Python, FastAPI, PostgreSQL, Redis, Docker, AWS, REST API, Git
    
    EXPERIENCE
    Senior Backend Engineer (2021 - Present)
    • Architected 6 microservices in FastAPI and Docker, handling 10,000 req/sec with sub-50ms latency.
    • Optimized PostgreSQL queries and configured Redis cache, reducing server load by 40%.
    • Deployed cloud services onto AWS EKS and automated CI/CD pipelines.
    
    EDUCATION
    B.S. in Computer Science | UC Berkeley
    """

    response = score_resume(resume_text, job_description)

    assert response.overall_score >= 50.0
    assert response.grade.startswith("A") or response.grade.startswith("B") or response.grade.startswith("C")
    assert response.sub_scores.semantic_similarity > 30.0
    assert response.sub_scores.skill_match > 50.0
    assert len(response.skills_analysis.matched_skills) >= 4
    assert "Python" in response.skills_analysis.matched_skills
    assert "FastAPI" in response.skills_analysis.matched_skills
    assert "PostgreSQL" in response.skills_analysis.matched_skills
    assert len(response.requirements_analysis) > 0
    assert len(response.suggested_bullet_points) > 0


def test_score_resume_with_target_company_fresher():
    resume_text = """
    Rahul Sharma
    rahul.sharma@example.com | +91 9876543210 | github.com/rahulsharma | leetcode.com/rahul
    
    EDUCATION
    B.Tech in Computer Science and Engineering, IIT Delhi (2020 - 2024), CGPA: 8.8/10
    Relevant Coursework: Data Structures & Algorithms, OS, DBMS, Computer Networks
    
    TECHNICAL SKILLS
    Languages: C++, Python, Java
    Core: Data Structures, Algorithms, OOP, System Design, Git, Linux
    Frameworks: FastAPI, Docker
    
    PROJECTS
    • Distributed Key-Value Store: Implemented Raft consensus in C++ with 99.9% fault tolerance.
    • AI Resume Analyzer: Built NLP-driven resume scoring tool using Python and Transformers.
    """

    response = score_resume(
        resume_text=resume_text,
        job_description="",  # Auto-discovered from company
        target_company="Google",
        experience_type="fresher",
        years_of_experience=0,
        target_role="Software Engineer",
    )

    assert response.overall_score > 0
    assert response.experience_type == "fresher"
    assert response.company_profile is not None
    assert "Google" in response.company_profile.company_name
    assert len(response.company_profile.exam_pattern) >= 3
    assert response.company_roadmap is not None
    assert "Google" in response.company_roadmap.company_name
    assert response.company_roadmap.eligibility_status in ["Eligible", "Conditionally Eligible", "Action Required", "Gaps Identified"]
    assert len(response.company_roadmap.preparation_roadmap) > 0


def test_score_resume_with_target_company_experienced():
    resume_text = """
    Priya Patel
    priya.patel@example.com | (555) 789-0123 | linkedin.com/in/priyapatel
    
    EXPERIENCE
    Lead Backend Engineer | CloudScale Inc. (2020 - Present)
    • Architected high-throughput microservices using AWS, Kafka, and Go handling 50k req/sec.
    • Spearheaded database partitioning across DynamoDB and PostgreSQL reducing p99 latency by 45%.
    • Mentored 8 junior and mid-level developers in distributed systems best practices.
    
    SKILLS
    Go, Python, AWS, Docker, Kubernetes, Kafka, PostgreSQL, Distributed Systems, Microservices
    """

    response = score_resume(
        resume_text=resume_text,
        job_description="",
        target_company="Amazon",
        experience_type="experienced",
        years_of_experience=5,
        target_role="Software Development Engineer II",
    )

    assert response.overall_score > 0
    assert response.experience_type == "experienced"
    assert response.company_profile is not None
    assert "Amazon" in response.company_profile.company_name
    assert response.company_roadmap is not None
    assert len(response.company_roadmap.preparation_roadmap) >= 2


def test_score_resume_unknown_company_worldwide_discovery():
    resume_text = """
    Alex Chen
    alex.chen@domain.io | github.com/alexchen
    Skills: Python, React, TypeScript, GraphQL, Docker, PostgreSQL
    Projects: Fullstack streaming music application deployed on Kubernetes.
    """

    # Testing dynamic discovery for a non-hardcoded company
    response = score_resume(
        resume_text=resume_text,
        job_description="",
        target_company="Stripe",
        experience_type="experienced",
        years_of_experience=3,
        target_role="Backend Engineer",
    )

    assert response.company_profile is not None
    assert "Stripe" in response.company_profile.company_name
    assert len(response.company_profile.exam_pattern) >= 2
    assert response.company_roadmap is not None


