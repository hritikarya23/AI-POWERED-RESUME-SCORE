"""Groq Cloud AI Service powered by Llama 3.3 70B & Llama 3.2 Vision.

Provides lightning-fast LLM inference (<1s) for:
1. Real-time Company Intelligence (live exam pattern, rounds, criteria, projects)
2. Intelligent Resume Scoring & Deep Gap Analysis
3. Vision-based Resume Extraction from Images (JPG/PNG)
"""

import base64
import json
import logging
import os
import re
from typing import Any, Dict, List, Optional
import httpx

logger = logging.getLogger(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_TEXT_MODEL = "llama-3.3-70b-versatile"
DEFAULT_VISION_MODEL = "llama-3.2-11b-vision-preview"


def _load_env_file():
    """Load key-values from .env if present without requiring third-party libraries."""
    for path in [".env", os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")]:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            k, v = k.strip(), v.strip().strip("'\"")
                            if k and k not in os.environ:
                                os.environ[k] = v
            except Exception:
                pass


def get_groq_api_key() -> Optional[str]:
    """Retrieve Groq API key from environment variables or .env file."""
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key:
        _load_env_file()
        key = os.environ.get("GROQ_API_KEY", "").strip()
    return key or None


def is_groq_available() -> bool:
    """Check if Groq API key is configured."""
    return bool(get_groq_api_key())


def clean_json_response(raw_text: str) -> str:
    """Extract valid JSON from LLM response markdown blocks."""
    raw_text = raw_text.strip()
    # Match ```json ... ``` blocks
    json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw_text)
    if json_match:
        return json_match.group(1).strip()
    return raw_text


def fetch_company_intelligence_groq(
    company_name: str,
    experience_type: str = "fresher",
    years_of_experience: float = 0.0,
    target_role: str = "Software Engineer",
) -> Optional[Dict[str, Any]]:
    """
    Fetch live, comprehensive exam pattern, rounds, eligibility, and projects from Groq Llama 3.3.
    """
    api_key = get_groq_api_key()
    if not api_key:
        return None

    is_fresher = experience_type.lower() == "fresher" or years_of_experience < 1.0
    exp_context = (
        f"Fresher / Entry-Level (0 years experience, campus or off-campus graduate)"
        if is_fresher
        else f"Experienced Professional ({years_of_experience} years of experience)"
    )

    system_prompt = (
        "You are an elite Tech Hiring Director and Principal Technical Recruiter with deep, real-time insider "
        "knowledge of global recruitment processes for every tech company worldwide (FAANG, Fortune 500, Product Unicorns, IT Giants, and startups). "
        "You return strictly valid JSON with no markdown wrapping or preamble."
    )

    user_prompt = f"""
Provide comprehensive, authentic hiring intelligence for:
- Target Company: {company_name}
- Target Role: {target_role}
- Candidate Seniority: {exp_context}

Return ONLY a JSON object matching this exact structure:
{{
  "company_name": "{company_name}",
  "industry": "Industry classification",
  "headquarters": "Primary HQ location",
  "hiring_bar": "Extremely High | High | Moderate",
  "difficulty_level": "Hard | Medium-Hard | Medium",
  "eligibility_criteria": {{
    "degrees_accepted": ["B.Tech/B.E.", "M.Tech", "MCA", "B.Sc/BCA"],
    "minimum_cgpa_or_percentage": "Minimum GPA/Percentage or 'No strict cutoff'",
    "backlog_policy": "Policy on active/cleared backlogs",
    "experience_required": "{exp_context}",
    "batch_eligibility": "Recent graduating batches or any relevant batch",
    "key_prerequisites": ["List of 3-5 mandatory prerequisite skills or qualifications"]
  }},
  "exam_pattern": {{
    "platform": "HackerRank | CodeSignal | LeetCode | Mettl | Glider | Internal",
    "total_duration": "Duration e.g. 90-120 Minutes",
    "rounds_count": 4,
    "sections": [
      {{
        "section_name": "Section name (e.g., Coding Assessment, Aptitude, CS Fundamentals)",
        "question_count": "e.g. 2-3 Questions",
        "topics_covered": ["Topic 1", "Topic 2", "Topic 3"],
        "recommended_time_mins": 45,
        "difficulty": "Easy | Medium | Hard"
      }}
    ],
    "negative_marking": false,
    "passing_cutoff": "Estimated cutoff e.g. 80-85%"
  }},
  "interview_rounds": [
    {{
      "round_number": 1,
      "round_name": "Round name (e.g. Online Assessment, Technical Screening, System Design)",
      "round_type": "Coding | Technical | System Design | Behavioral / HR",
      "duration_minutes": 60,
      "focus_areas": ["Focus area 1", "Focus area 2"],
      "typical_questions": ["Realistic question 1", "Realistic question 2"],
      "evaluation_criteria": "What interviewers look for"
    }}
  ],
  "expected_coding_projects": [
    {{
      "title": "Specific impressive project title relevant to this company's tech stack",
      "complexity": "Advanced | Production-Grade | Full-Stack",
      "suggested_tech_stack": ["Tech1", "Tech2", "Tech3"],
      "key_features_to_include": ["Key architectural feature 1", "Feature 2"],
      "why_it_impresses": "Why this specific project stands out to hiring managers at {company_name}"
    }}
  ],
  "insider_tips": [
    "Crucial insider tip 1 to crack {company_name}",
    "Crucial insider tip 2",
    "Crucial insider tip 3"
  ]
}}
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": DEFAULT_TEXT_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 2500,
        "response_format": {"type": "json_object"},
    }

    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.post(GROQ_API_URL, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                return json.loads(clean_json_response(content))
            else:
                logger.error("Groq API error %d: %s", resp.status_code, resp.text[:200])
                return None
    except Exception as e:
        logger.error("Failed to query Groq for company intelligence: %s", e)
        return None


def extract_text_from_image_groq(image_bytes: bytes, filename: str) -> Optional[str]:
    """
    Extract accurate text and structure from a resume image (JPG/PNG) using Groq Llama 3.2 Vision.
    """
    api_key = get_groq_api_key()
    if not api_key:
        return None

    lower = filename.lower()
    if lower.endswith(".png"):
        mime_type = "image/png"
    elif lower.endswith(".webp"):
        mime_type = "image/webp"
    else:
        mime_type = "image/jpeg"

    b64_image = base64.b64encode(image_bytes).decode("utf-8")
    data_uri = f"data:{mime_type};base64,{b64_image}"

    system_prompt = (
        "You are an expert OCR and resume document transcription engine. "
        "Extract every single word, section, bullet point, date, and contact detail from the provided resume image. "
        "Maintain the layout structure, bullet points, headers, and exact spelling. "
        "Do not summarize or add markdown commentary; return ONLY the extracted text."
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": DEFAULT_VISION_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all text from this resume image accurately:"},
                    {"type": "image_url", "image_url": {"url": data_uri}},
                ],
            },
        ],
        "temperature": 0.1,
        "max_tokens": 3000,
    }

    try:
        with httpx.Client(timeout=25.0) as client:
            resp = client.post(GROQ_API_URL, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                logger.error("Groq Vision error %d: %s", resp.status_code, resp.text[:200])
                return None
    except Exception as e:
        logger.error("Failed to run Groq Vision extraction: %s", e)
        return None
