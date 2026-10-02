"""Integration tests for FastAPI endpoints."""

import io
from fastapi.testclient import TestClient
import pytest

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "semantic_engine" in data


def test_sample_data_endpoint():
    response = client.get("/api/sample-data")
    assert response.status_code == 200
    roles = response.json()
    assert len(roles) >= 3
    assert any(r["id"] == "backend-engineer" for r in roles)


def test_score_endpoint_success():
    payload = {
        "resume_text": """
        Jane Doe | jane@example.com | (555) 123-4567
        EXPERIENCE: Senior Python developer with 5 years building scalable FastAPI APIs and Docker containers on AWS.
        SKILLS: Python, FastAPI, Docker, AWS, PostgreSQL, Redis, Git.
        EDUCATION: B.S. in Computer Science.
        """,
        "job_description": """
        We need a Senior Python Backend Developer.
        Requirements:
        • 4+ years of Python and FastAPI.
        • Experience with AWS, Docker, and PostgreSQL databases.
        """,
    }
    response = client.post("/api/score", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "overall_score" in data
    assert "grade" in data
    assert "sub_scores" in data
    assert "skills_analysis" in data
    assert "Python" in data["skills_analysis"]["matched_skills"]


def test_score_endpoint_validation_error():
    # Too short resume text
    response = client.post("/api/score", json={"resume_text": "short", "job_description": "short"})
    assert response.status_code == 422 or response.status_code == 400


def test_extract_text_endpoint():
    file_content = b"Resume text content with Python, FastAPI, and Kubernetes skills."
    response = client.post(
        "/api/extract-text",
        files={"file": ("test_resume.txt", io.BytesIO(file_content), "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test_resume.txt"
    assert "Kubernetes" in data["text"]
    assert data["word_count"] > 0


def test_score_upload_endpoint():
    file_content = b"Alex Developer | alex@test.com\nExperience with Python, FastAPI, Docker, and AWS.\nSkills: Python, FastAPI, Docker, AWS, SQL."
    response = client.post(
        "/api/score-upload",
        files={"resume_file": ("resume.txt", io.BytesIO(file_content), "text/plain")},
        data={"job_description": "Looking for Python and FastAPI developer with Docker and AWS experience."},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["overall_score"] > 50
    assert "Python" in data["skills_analysis"]["matched_skills"]


def test_score_upload_real_pdf_file():
    with open("sample_resumes/alex_rivera_backend_engineer.pdf", "rb") as f:
        pdf_bytes = f.read()

    response = client.post(
        "/api/score-upload",
        files={"resume_file": ("alex_rivera_backend_engineer.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
        data={
            "job_description": "We are seeking a Senior Python Backend Engineer with FastAPI, Docker, Kubernetes, AWS, and PostgreSQL experience.",
            "experience_type": "experienced",
            "years_of_experience": "5",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["overall_score"] >= 50
    assert "FastAPI" in data["skills_analysis"]["matched_skills"]
    assert "Docker" in data["skills_analysis"]["matched_skills"]
    assert "Kubernetes" in data["skills_analysis"]["matched_skills"]


def test_root_serves_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "AI-Powered Resume Scorer" in response.text


def test_popular_companies_endpoint():
    response = client.get("/api/popular-companies")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    assert any("Google" in companies for companies in data.values())


def test_company_intel_endpoint():
    response = client.get("/api/company-intel", params={"company": "Google", "experience_type": "fresher", "years": 0})
    assert response.status_code == 200
    data = response.json()
    assert "Google" in data["company_name"]
    assert "exam_pattern" in data
    assert len(data["exam_pattern"]) >= 3
    assert "eligibility_criteria" in data


def test_score_endpoint_with_target_company_only():
    payload = {
        "resume_text": """
        Rahul Sharma | rahul@domain.com | (555) 987-6543
        SKILLS: C++, Python, Data Structures, Algorithms, Docker, Linux, Git
        EDUCATION: B.Tech in Computer Science, GPA: 8.5/10
        PROJECTS: High Performance Web Server in C++ with epoll and multithreading.
        """,
        "job_description": "",
        "target_company": "Google",
        "experience_type": "fresher",
        "years_of_experience": 0,
        "target_role": "Software Engineer",
    }
    response = client.post("/api/score", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["overall_score"] > 0
    assert data["experience_type"] == "fresher"
    assert data["company_profile"] is not None
    assert data["company_roadmap"] is not None
    assert "Google" in data["company_roadmap"]["company_name"]


def test_score_upload_image_file():
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (900, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((20, 30), "John Doe - Software Engineer", fill=(0, 0, 0))
    draw.text((20, 80), "Skills: Python, FastAPI, Docker, AWS, PostgreSQL", fill=(0, 0, 0))
    draw.text((20, 130), "Experience: 4 years developing distributed backend systems.", fill=(0, 0, 0))
    
    stream = io.BytesIO()
    img.save(stream, format="JPEG")
    img_bytes = stream.getvalue()

    response = client.post(
        "/api/score-upload",
        files={"resume_file": ("resume_scanned.jpg", io.BytesIO(img_bytes), "image/jpeg")},
        data={
            "target_company": "Amazon",
            "experience_type": "experienced",
            "years_of_experience": "4",
            "target_role": "Software Development Engineer II",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["overall_score"] > 0
    assert "Amazon" in data["company_profile"]["company_name"]
    assert data["company_roadmap"] is not None


