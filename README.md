# 🚀 AI-Powered Resume Scorer & Company Interview Engine

An intelligent, production-grade AI platform that evaluates candidate resumes against job descriptions or target global companies, computes a multidimensional match score (0–100%), reveals company-specific exam patterns, eligibility rules, and delivers prioritized, actionable guidance to land top engineering roles.

---

## 🌟 Key Features

1. **📷 OCR Image & Multi-Format Resume Upload**:
   - **Image Resume OCR**: Upload scanned resumes or screenshots in **JPG, JPEG, PNG, WEBP, or BMP** format. Text is extracted using **EasyOCR** neural optical character recognition.
   - **PDF & Word Parsing**: High-fidelity text extraction from **PDF** (`pypdf`) and **Word DOCX** (`python-docx`), preserving formatting, bullet points, and tables.
   - Intelligent text sanitization pipeline to clean encoding glitches, whitespace, and broken line hyphenation.

2. **🏢 Worldwide Company Auto-Discovery Engine**:
   - Simply enter **any target company name** (e.g., *Google, Microsoft, Amazon, TCS, Infosys, Uber, Goldman Sachs, Stripe, Netflix, Spotify, or any company worldwide*).
   - The AI engine automatically discovers:
     - **Exact Exam & Selection Pattern** (Round duration, format, online assessments, technical coding rounds, system design, and behavioral/culture fit).
     - **Eligibility Criteria** (Degree requirements, minimum CGPA/percentage, backlog policies).
     - **Coding & Project Expectations** (LeetCode difficulty distribution, architecture, and expected hands-on system projects).
     - **Round-by-Round Preparation Roadmap** & hiring tips.

3. **🎓 Fresher vs. Experienced Career Adaptation**:
   - **Fresher Mode (0 Years / Campus Hire)**: Recalibrates scoring to heavily emphasize core CS fundamentals (DSA, OS, DBMS, Networks), academic projects, and competitive programming profiles (LeetCode/Codeforces), compensating for lack of formal work history.
   - **Experienced Mode (1 to 15+ Years)**: Emphasizes production distributed systems, microservices, cloud scaling (AWS/GCP/Azure), database sharding, and architecture design.

4. **🧠 Deep Semantic Vector Matching**:
   - Powered by **Sentence-Transformers** (`all-MiniLM-L6-v2`), producing 384-dimensional dense semantic embeddings.
   - Measures true contextual alignment rather than superficial keyword matching.
   - High-availability fallback to TF-IDF cosine similarity ensures 100% uptime.

5. **🎯 Curated 1,500+ Skills Taxonomy**:
   - Rich technical database covering Languages, Frameworks, Cloud & DevOps, Databases, AI/ML, and Engineering Practices.
   - Normalizes aliases automatically (e.g., `k8s` → `Kubernetes`, `postgres` → `PostgreSQL`, `react.js` → `React`).
   - Categorizes skills into Matched, Missing, and Additional/Bonus categories with 1-click copy chips.

6. **📋 Requirement-by-Requirement Decomposition**:
   - Splits job descriptions into distinct responsibilities and qualifications.
   - Performs sentence-level semantic pairing to evaluate candidate evidence.
   - Highlights each requirement as **Strong Match**, **Moderate Match**, or **Missing / Weak**.

7. **🛡️ ATS Format & Impact Analysis**:
   - Scans for standard ATS headers (Summary, Experience, Education, Skills, Projects, Certifications).
   - Evaluates power action verbs vs passive phrases.
   - Quantifies metrics (percentages, revenue, latency reductions, user scale).
   - Audits contact details (Email, Phone, LinkedIn, GitHub).

8. **💡 Google XYZ Formula Bullet Generator**:
   - Automatically drafts bullet points in Google's recommended format:  
     `Accomplished [X] as measured by [Y] by doing [Z]`.

9. **⚡ Responsive Dark-Slate Modern UI & REST API**:
   - Drag-and-drop file upload zone supporting PDF, DOCX, TXT, and JPG/PNG images.
   - Live company search with popular company chips (FAANG, Unicorns, FinTech, IT Services).
   - Animated SVG score gauge, printable PDF reports, and one-click JSON exports.

---

## 🏗️ Architecture & Project Structure

```
ai powered resume scorer/
├── app/
│   ├── main.py                     # FastAPI application, CORS, static routes, lifespan
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py            # Endpoints: /api/score, /api/score-upload, /api/company-intel, /api/popular-companies
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py              # Pydantic schemas (ScoreResponse, CompanyProfile, CompanyRoadmap, etc.)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── extractor.py            # PDF, DOCX, TXT, and EasyOCR image extractor
│   │   ├── company_intelligence.py # Curated & worldwide dynamic AI company intelligence engine
│   │   ├── skills_db.py            # 1,500+ technical skills taxonomy & alias dictionary
│   │   ├── semantic.py             # Sentence-Transformers embeddings & similarity engine
│   │   ├── ats_analyzer.py         # ATS heuristics, power verbs, metric detection
│   │   └── scorer.py               # Composite scoring algorithm & recommendation generator
│   └── static/
│       ├── index.html              # Modern single-page web dashboard
│       ├── css/
│       │   └── style.css           # Premium dark theme, responsive grid, animations
│       └── js/
│           └── app.js              # Frontend controller, OCR handler, company auto-discovery
├── sample_resumes/                 # Pre-generated test resumes (PDF & TXT)
│   ├── alex_rivera_backend_engineer.pdf
│   └── maya_chen_ml_engineer.pdf
├── tests/
│   ├── test_api.py                 # FastAPI route & integration tests
│   ├── test_extractor.py           # Document & Image OCR extraction unit tests
│   └── test_scorer.py              # Scoring engine, company intelligence & semantic tests
├── pyproject.toml                  # Python package configuration
├── requirements.txt                # Pip dependency specifications
├── run.bat                         # One-click Windows runner
└── README.md                       # Documentation
```

---

## 📊 Scoring Methodology

Scores are computed adaptively based on candidate experience level:

### 🎓 Fresher Formula (0 - 1 Years)
$$\text{Overall Score} = (0.40 \times \text{Skills}) + (0.30 \times \text{Semantic}) + (0.20 \times \text{Requirements}) + (0.10 \times \text{ATS Health})$$
*Freshers receive bonus ATS recognition when comprehensive Projects and Education sections are present.*

### 💼 Experienced Formula (2+ Years)
$$\text{Overall Score} = (0.35 \times \text{Semantic}) + (0.35 \times \text{Skills}) + (0.20 \times \text{Requirements}) + (0.10 \times \text{ATS Health})$$

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10, 3.11, or 3.12 installed.
- Git installed.

### 2. Clone Repository & Setup Environment
```bash
git clone https://github.com/hritikarya23/AI-POWERED-RESUME-SCORE.git
cd AI-POWERED-RESUME-SCORE

# Create virtual environment
python -m venv .venv

# Activate on Windows:
.venv\Scripts\activate
# Or on macOS/Linux:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Open your browser and navigate to: **`http://127.0.0.1:8000`**

### 4. Run Unit & Integration Tests
```bash
pytest -v
```

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/score-upload` | Upload resume file (**PDF, DOCX, TXT, JPG, PNG**) with company name or custom JD |
| `POST` | `/api/score` | Score raw resume text against job description or company name |
| `GET` | `/api/company-intel` | Instant discovery of exam pattern, eligibility & criteria for any company |
| `GET` | `/api/popular-companies` | List of curated top global tech employers |
| `POST` | `/api/extract-text` | Standalone document and image OCR text extraction |
| `GET` | `/api/sample-data` | Pre-configured sample role pairs for instant testing |
| `GET` | `/api/health` | Service health status and semantic engine info |

---

## 📄 License
This project is open-source under the MIT License.
