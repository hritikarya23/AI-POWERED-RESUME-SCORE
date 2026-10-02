"""FastAPI route handlers for resume scoring, document text extraction, and sample datasets."""

import json
import logging
from typing import List, Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.models.schemas import (
    CompanyProfile,
    ExtractTextResponse,
    SampleRole,
    ScoreRequest,
    ScoreResponse,
)
from app.services.company_intelligence import get_company_intelligence
from app.services.extractor import ExtractionError, extract_text_from_file
from app.services.scorer import score_resume
from app.services.semantic import SemanticMatcher

logger = logging.getLogger(__name__)

router = APIRouter()

# Pre-configured sample roles for instant testing and demonstration
SAMPLE_ROLES: List[SampleRole] = [
    SampleRole(
        id="backend-engineer",
        title="Senior Python & Cloud Backend Engineer",
        company="Nexora Cloud Systems",
        level="Senior (5+ Years)",
        job_description="""
We are seeking a Senior Python & Cloud Backend Engineer to architect, build, and scale our core SaaS platform.

Responsibilities:
• Architect, deploy, and maintain high-performance asynchronous microservices using Python and FastAPI.
• Design robust relational schemas and optimize complex queries using PostgreSQL and Redis caching.
• Containerize services using Docker and orchestrate deployments via Kubernetes on AWS (EKS, Lambda, S3, RDS).
• Build and maintain automated CI/CD deployment pipelines using GitHub Actions.
• Collaborate with frontend and mobile teams to define and implement secure RESTful and GraphQL APIs.
• Drive code quality through test-driven development (TDD), comprehensive unit testing (Pytest), and peer code reviews.

Requirements:
• 5+ years of software engineering experience with Python and asynchronous web frameworks (FastAPI or Django).
• Strong hands-on experience with PostgreSQL, indexing strategies, and distributed caching with Redis.
• Proven production experience with Docker, Kubernetes, and AWS cloud infrastructure.
• Experience designing and managing scalable REST APIs and microservice architectures.
• Track record of writing maintainable, clean code with automated unit and integration tests.
• Bachelor's degree in Computer Science, Software Engineering, or equivalent practical experience.
        """.strip(),
        sample_resume="""
Alex Rivera
alex.rivera@example.com | (555) 234-5678 | San Francisco, CA
linkedin.com/in/alexrivera-dev | github.com/alexrivera

PROFESSIONAL SUMMARY
Senior Software Engineer with 6 years of experience building high-scale distributed backend systems, REST APIs, and cloud services in Python and Go. Proven track record of architecting microservices that handle millions of daily transactions with 99.99% uptime.

TECHNICAL SKILLS
• Languages: Python, Go, SQL, Bash
• Frameworks: FastAPI, Django, Flask, Pytest
• Cloud & DevOps: AWS (EC2, S3, RDS, Lambda), Docker, Kubernetes, Terraform, GitHub Actions, CI/CD
• Databases & Storage: PostgreSQL, Redis, MySQL, MongoDB
• Architecture: Microservices, REST API, System Design, TDD, Agile/Scrum

PROFESSIONAL EXPERIENCE
Senior Backend Engineer | CloudScale Tech (2022 - Present)
• Architected and deployed 8 asynchronous microservices using FastAPI and Docker, handling 15,000 requests per second with sub-40ms latency.
• Optimized PostgreSQL query performance and designed Redis caching layer, decreasing database load by 45% and saving $3,200 monthly in cloud costs.
• Spearheaded migration of legacy monolithic workloads to Kubernetes on AWS EKS, improving deployment frequency from bi-weekly to multiple times daily.
• Established CI/CD automation with GitHub Actions and Pytest, boosting automated test coverage from 62% to 94%.
• Mentored 4 junior engineers on distributed systems architecture, design patterns, and rigorous code review practices.

Backend Software Engineer | DataStream Labs (2019 - 2022)
• Engineered RESTful APIs in Python/Django serving over 1.2M active monthly users.
• Designed automated data processing pipelines that ingested and normalized 20M+ records daily into PostgreSQL.
• Automated deployment and staging environments using Docker, Terraform, and AWS EC2.

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley (2015 - 2019)
        """.strip(),
    ),
    SampleRole(
        id="ml-engineer",
        title="Machine Learning & Generative AI Engineer",
        company="Aether AI Labs",
        level="Mid-Senior",
        job_description="""
Aether AI Labs is looking for a Machine Learning & GenAI Engineer to build state-of-the-art NLP, RAG, and LLM applications.

Key Responsibilities:
• Develop, fine-tune, and deploy transformer-based LLMs using PyTorch and HuggingFace.
• Build scalable Retrieval-Augmented Generation (RAG) pipelines integrating vector databases such as Pinecone, ChromaDB, or Qdrant.
• Design and maintain production ML inference endpoints using Python and FastAPI containerized in Docker.
• Optimize model latency and memory footprints using quantization techniques (LoRA, QLoRA, ONNX).
• Collaborate with product managers and software engineers to translate business requirements into production AI capabilities.

Requirements:
• 3+ years experience developing and deploying machine learning models in production.
• Deep proficiency in Python, PyTorch, Scikit-Learn, and HuggingFace Transformers.
• Hands-on experience developing RAG architectures, prompt engineering, and semantic vector search.
• Experience with containerization (Docker) and REST API development (FastAPI).
• Familiarity with cloud platforms (GCP or AWS) and MLOps tools.
• Degree in Computer Science, Data Science, AI, or related quantitative field.
        """.strip(),
        sample_resume="""
Maya Chen
maya.chen@email.com | (555) 789-0123 | Seattle, WA
github.com/mayachen-ai | linkedin.com/in/mayachen-ml

SUMMARY
Data Scientist & Machine Learning Engineer with 4 years of experience building predictive models and statistical solutions in Python. Proficient in classical ML, data engineering, and deep learning with PyTorch.

SKILLS
• Languages: Python, SQL, R
• Machine Learning: PyTorch, Scikit-Learn, Pandas, NumPy, SciPy, TensorFlow
• Tools & Cloud: Docker, Git, AWS (S3, EC2), Jupyter, Linux
• Concepts: Feature Engineering, Data Modeling, Classification, Regression, NLP

EXPERIENCE
Machine Learning Engineer | Apex Data Corp (2021 - Present)
• Developed and deployed classification and regression models in Python and Scikit-Learn, improving customer churn prediction accuracy by 22%.
• Built customer sentiment NLP pipeline using PyTorch and HuggingFace, processing 500,000 reviews monthly.
• Containerized ML inference services with Docker and deployed onto AWS EC2 instances.
• Collaborated with data engineering team to design ETL pipelines in SQL and Pandas.

Data Analyst | Insight Metrics (2020 - 2021)
• Performed exploratory data analysis on 10M+ rows of user telemetry data.
• Built automated dashboards in Tableau and automated weekly KPI reporting scripts in Python.

EDUCATION
Master of Science in Data Science | University of Washington (2020)
Bachelor of Science in Statistics | University of Washington (2018)
        """.strip(),
    ),
    SampleRole(
        id="frontend-dev",
        title="Full-Stack / React Developer",
        company="Prism Digital",
        level="Mid-Level",
        job_description="""
We are seeking a versatile Full-Stack Developer with strong expertise in React, TypeScript, and Node.js.

Responsibilities:
• Develop interactive, accessible, and responsive user interfaces using React, Next.js, and TypeScript.
• Build and maintain robust backend APIs using Node.js, Express, and MongoDB.
• Implement state management with Redux or Zustand and style components using Tailwind CSS.
• Write unit and end-to-end tests using Jest and Cypress.
• Collaborate in an Agile team with designers and engineers to ship weekly releases.

Requirements:
• 3+ years of professional web development experience with React and TypeScript.
• Solid background in Node.js, Express, and REST APIs or GraphQL.
• Experience with MongoDB or PostgreSQL databases.
• Strong command of modern CSS, Tailwind CSS, and web accessibility standards.
• Familiarity with Git, GitHub Actions, and CI/CD pipelines.
        """.strip(),
        sample_resume="""
Jordan Lee
jordan.lee@domain.com | (555) 456-7890 | Austin, TX
linkedin.com/in/jordanlee-dev

PROFESSIONAL SUMMARY
Passionate Frontend Developer with 3 years of experience building responsive, user-centered web applications in React and JavaScript. Adept at creating intuitive UIs, modular components, and connecting frontend clients to RESTful services.

TECHNICAL SKILLS
• Frontend: React, JavaScript, HTML5, CSS3, Tailwind CSS, Bootstrap, Redux
• Backend: Node.js, Express, REST API
• Databases: MongoDB
• Tools: Git, GitHub, Webpack, Postman, Jest

WORK EXPERIENCE
Frontend Developer | WebCraft Studios (2022 - Present)
• Built 12 responsive web applications using React and Tailwind CSS, increasing mobile user engagement by 30%.
• Integrated React frontend with Node.js and Express REST APIs to enable real-time user authentication and data persistence.
• Implemented Redux store for state management across 40+ dynamic components.
• Increased automated unit test coverage to 80% using Jest.

Junior Web Developer | PixelSpark Interactive (2021 - 2022)
• Developed landing pages and email templates using HTML5, CSS3, and JavaScript.
• Fixed cross-browser compatibility bugs and improved page load speeds by 25%.

EDUCATION
Bachelor of Arts in Interactive Media & Web Design
Texas State University (2017 - 2021)
        """.strip(),
    ),
]



POPULAR_COMPANIES = {
    "FAANG & Big Tech": ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix"],
    "Product & Unicorns": ["Uber", "Zomato", "Swiggy", "Flipkart", "Adobe", "Atlassian", "Salesforce", "NVIDIA", "Oracle", "Cisco"],
    "FinTech & Investment Banking": ["Goldman Sachs", "JPMorgan Chase", "Morgan Stanley", "DE Shaw", "Bloomberg"],
    "Global IT Services": ["TCS", "Infosys", "Wipro", "Accenture", "Capgemini", "Cognizant", "IBM"],
}


@router.post("/score", response_model=ScoreResponse)
async def score_resume_endpoint(request: ScoreRequest):
    """
    Score resume text against job description or target company profile.
    """
    if len(request.resume_text.strip()) < 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text is too short. Please provide at least 20 characters.",
        )

    has_jd = request.job_description and len(request.job_description.strip()) >= 20
    has_company = request.target_company and len(request.target_company.strip()) > 1

    if not has_jd and not has_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide either a Target Company Name or a Job Description.",
        )

    try:
        response = score_resume(
            resume_text=request.resume_text,
            job_description=request.job_description,
            target_company=request.target_company,
            experience_type=request.experience_type or "fresher",
            years_of_experience=request.years_of_experience or 0.0,
            target_role=request.target_role or "Software Engineer",
            custom_weights=request.weights,
        )
        return response
    except Exception as e:
        logger.error("Error scoring resume: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while scoring the resume: {str(e)}",
        )


@router.post("/score-upload", response_model=ScoreResponse)
async def score_resume_upload(
    resume_file: UploadFile = File(..., description="Resume document (.pdf, .docx, .txt, .jpg, .png)"),
    job_description: Optional[str] = Form(None, description="Optional job description text"),
    target_company: Optional[str] = Form(None, description="Optional target company name"),
    experience_type: Optional[str] = Form("fresher", description="'fresher' or 'experienced'"),
    years_of_experience: Optional[float] = Form(0.0, description="Years of experience"),
    target_role: Optional[str] = Form("Software Engineer", description="Target role title"),
    weights: Optional[str] = Form(None, description="Optional JSON string of custom weights"),
):
    """
    Directly upload a resume file (PDF, DOCX, TXT, or Image: JPG/PNG) with company or JD.
    """
    if not resume_file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file has no filename.")

    has_jd = job_description and len(job_description.strip()) >= 20
    has_company = target_company and len(target_company.strip()) > 1

    if not has_jd and not has_company:
        raise HTTPException(
            status_code=400,
            detail="Please provide either a Target Company Name or a Job Description.",
        )

    # Validate file size (max 20MB for high-res images/PDFs)
    file_bytes = await resume_file.read()
    if len(file_bytes) > 20 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds maximum limit of 20MB.")

    try:
        extracted = extract_text_from_file(file_bytes, resume_file.filename)
        resume_text = extracted["text"]
    except ExtractionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")

    parsed_weights = None
    if weights:
        try:
            parsed_weights = json.loads(weights)
        except Exception:
            pass

    try:
        response = score_resume(
            resume_text=resume_text,
            job_description=job_description,
            target_company=target_company,
            experience_type=experience_type or "fresher",
            years_of_experience=years_of_experience or 0.0,
            target_role=target_role or "Software Engineer",
            custom_weights=parsed_weights,
        )
        return response
    except Exception as e:
        logger.error("Error scoring uploaded resume: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scoring error: {str(e)}",
        )


@router.get("/company-intel", response_model=CompanyProfile)
async def get_company_intel(
    company: str,
    experience_type: str = "fresher",
    years: float = 0.0,
    role: str = "Software Engineer",
):
    """
    Instant discovery of exam pattern, eligibility, and expectations for ANY company worldwide.
    """
    if not company or len(company.strip()) < 1:
        raise HTTPException(status_code=400, detail="Please provide a valid company name.")

    profile = get_company_intelligence(
        company_name=company.strip(),
        experience_type=experience_type,
        years_of_experience=years,
        target_role=role,
    )
    return profile


@router.get("/popular-companies")
async def get_popular_companies():
    """
    Get categorized list of world-renowned employers.
    """
    return POPULAR_COMPANIES


@router.post("/extract-text", response_model=ExtractTextResponse)
async def extract_text_endpoint(
    file: UploadFile = File(..., description="Document file to extract text from (.pdf, .docx, .txt)")
):
    """
    Extract text and document statistics from an uploaded PDF, DOCX, or TXT file.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected.")

    file_bytes = await file.read()
    if len(file_bytes) > 15 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds maximum size of 15MB.")

    try:
        extracted = extract_text_from_file(file_bytes, file.filename)
        return ExtractTextResponse(
            filename=extracted["filename"],
            text=extracted["text"],
            page_count=extracted["page_count"],
            word_count=extracted["word_count"],
            char_count=extracted["char_count"],
        )
    except ExtractionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {str(e)}")


@router.get("/sample-data", response_model=List[SampleRole])
async def get_sample_data():
    """
    Retrieve pre-configured sample roles (job description and matching resume pairs).
    """
    return SAMPLE_ROLES


@router.get("/health")
async def health_check():
    """
    Health and diagnostic endpoint.
    """
    matcher = SemanticMatcher.get_instance()
    return {
        "status": "healthy",
        "service": "AI-Powered Resume Scorer",
        "version": "1.0.0",
        "semantic_engine": "SentenceTransformer" if matcher.is_neural else "TF-IDF Fallback",
        "model_name": matcher.model_name if matcher.is_neural else "None",
    }
