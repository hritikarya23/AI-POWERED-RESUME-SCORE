"""Core resume scoring engine integrating semantic matching, skill taxonomy, and ATS heuristics."""

import logging
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from app.models.schemas import (
    ATSAnalysis,
    CompanyProfile,
    CompanyRoadmap,
    ImprovementTip,
    RequirementMatch,
    ScoreResponse,
    SkillCategoryBreakdown,
    SkillMatch,
    SubScores,
)
from app.services.company_intelligence import (
    build_company_roadmap,
    get_company_intelligence,
)
from app.services.ats_analyzer import analyze_ats
from app.services.semantic import SemanticMatcher, split_into_meaningful_sentences
from app.services.skills_db import (
    SKILL_TAXONOMY,
    SKILL_TO_CATEGORY,
    categorize_skills,
    extract_skills,
)

logger = logging.getLogger(__name__)

# Keywords indicating a sentence in JD represents a job requirement or duty
REQUIREMENT_INDICATORS = [
    "experience with", "proficiency in", "responsible for", "must have", "required",
    "requirements", "qualifications", "knowledge of", "ability to", "familiarity with",
    "understanding of", "hands-on", "track record", "proven experience", "degree in",
    "develop", "design", "build", "maintain", "architect", "lead", "collaborate",
    "implement", "optimize", "ensure", "manage"
]


def extract_requirements_from_jd(jd_text: str) -> List[str]:
    """
    Extract discrete requirement and responsibility items from a Job Description.
    """
    sentences = split_into_meaningful_sentences(jd_text)
    requirements = []

    for s in sentences:
        s_lower = s.lower()
        # Check if sentence looks like a bullet or contains requirement signals
        is_req = any(ind in s_lower for ind in REQUIREMENT_INDICATORS)
        # Or if it's a short/medium bullet point describing a qualification
        if is_req or (len(s.split()) >= 4 and len(s.split()) <= 40 and not s.endswith("?")):
            # Filter out generic company intro or perks sentences
            if not any(noise in s_lower for noise in ["we offer", "benefits include", "401k", "equal opportunity", "about us", "who we are"]):
                requirements.append(s)

    # Return top 15 distinct requirements
    return requirements[:15] if requirements else sentences[:8]


def calculate_grade(overall_score: float) -> Tuple[str, str]:
    """
    Map numeric score to descriptive letter grade and summary.
    """
    if overall_score >= 88.0:
        return (
            "A+ (Outstanding Match)",
            "Your resume is an exceptional fit for this role. Core technical skills, semantic alignment, and requirements are comprehensively covered.",
        )
    elif overall_score >= 78.0:
        return (
            "A (Strong Match)",
            "Strong match! Your profile aligns closely with the job requirements, with minor keyword additions recommended to guarantee top ATS ranking.",
        )
    elif overall_score >= 68.0:
        return (
            "B (Good Match)",
            "Solid candidate profile with good foundational overlap. Addressing the missing skills and quantifying key achievements will elevate your application.",
        )
    elif overall_score >= 55.0:
        return (
            "C (Moderate Match)",
            "Moderate alignment. While some transferable skills and concepts are present, several essential requirements and keywords from the job description are missing.",
        )
    else:
        return (
            "D (Needs Improvement)",
            "Low alignment with this specific role. The resume lacks key technical keywords, specific domain experience, and ATS formatting expected for this position.",
        )


def generate_improvement_tips(
    missing_skills: List[str],
    matched_skills: List[str],
    unmatched_requirements: List[RequirementMatch],
    ats_data: Dict[str, Any],
    sub_scores: Dict[str, float],
    experience_type: str = "fresher",
    years_of_experience: float = 0.0,
    company_name: Optional[str] = None,
) -> List[ImprovementTip]:
    """
    Synthesize prioritized, actionable advice tailored to this candidate, experience level, and target employer.
    """
    tips: List[ImprovementTip] = []
    is_fresher = experience_type.lower() == "fresher" or years_of_experience < 1.5

    # 1. Missing Core Skills (High Priority)
    if missing_skills:
        top_missing = missing_skills[:5]
        tips.append(
            ImprovementTip(
                category="Skills & Keywords",
                priority="high",
                title=f"Incorporate Missing Key Technologies ({', '.join(top_missing[:3])})",
                description=(
                    f"The target role explicitly expects: {', '.join(top_missing)}. "
                    "Recruiter search filters and ATS parsers scan for these exact keywords."
                ),
                action_item=(
                    f"Add {', '.join(top_missing)} to your Skills section and highlight hands-on experience "
                    "with them in your project or work experience bullet points."
                ),
            )
        )

    # 2. Fresher vs Experienced Specific Guidance
    if is_fresher:
        tips.append(
            ImprovementTip(
                category="Campus & Fresher Strategy",
                priority="high",
                title="Highlight Competitive Programming & Coding Profiles",
                description="For campus hiring and entry-level shortlisting, verified DSA ratings (LeetCode, HackerRank, Codeforces) heavily increase interview call rates.",
                action_item="Add your profile handle and achievements (e.g. 'Solved 350+ LeetCode problems | Contest Rating 1680 | 5-Star on HackerRank') under your header or achievements section.",
            )
        )
        tips.append(
            ImprovementTip(
                category="Coursework & Foundations",
                priority="medium",
                title="Prominently Feature Core CS Fundamentals",
                description="Technical interviewers grill freshers on fundamental computer science principles.",
                action_item="List relevant subjects in a 'Coursework' section: Data Structures & Algorithms, Object-Oriented Programming (OOP), DBMS, Operating Systems, Computer Networks.",
            )
        )
    else:
        tips.append(
            ImprovementTip(
                category="Experienced Professional Impact",
                priority="high",
                title="Emphasize System Architecture & Scalability",
                description=f"For candidates with {int(years_of_experience)}+ years of experience, hiring managers evaluate architectural ownership and business metrics.",
                action_item="Detail microservices design, throughput numbers (QPS), distributed caching, and leadership in code reviews or system design.",
            )
        )

    # 3. Unaddressed or Weak Job Requirements (High / Medium Priority)
    weak_reqs = [r for r in unmatched_requirements if r.status == "Missing / Weak"]
    if weak_reqs:
        example_req = weak_reqs[0].requirement
        tips.append(
            ImprovementTip(
                category="Experience Alignment",
                priority="high",
                title="Address Key Unfulfilled Job Requirements",
                description=(
                    f"Your resume does not clearly demonstrate experience with: '{example_req[:100]}...'. "
                    f"There are {len(weak_reqs)} requirements with low semantic matching."
                ),
                action_item=(
                    "Add a bullet point under your relevant work experience or projects detailing how you have solved "
                    "similar challenges or applied equivalent methodologies."
                ),
            )
        )

    # 4. Measurable Impact & Metrics
    if ats_data.get("quantification_score", 0) < 50.0:
        tips.append(
            ImprovementTip(
                category="Quantifiable Impact",
                priority="high" if ats_data.get("quantification_score", 0) < 30.0 else "medium",
                title="Quantify Accomplishments with Numbers and Percentages",
                description=(
                    f"Only {len(ats_data.get('metrics_found', []))} quantifiable metrics were detected. "
                    "Recruiters favor resumes with clear, measurable outcomes."
                ),
                action_item=(
                    "Use Google's XYZ formula: 'Accomplished [X] as measured by [Y] by doing [Z]'. "
                    "For example: 'Reduced API response latency by 35% through Redis caching and query optimization'."
                ),
            )
        )

    # 5. Weak / Passive Action Verbs
    weak_verbs = ats_data.get("weak_verbs_found", [])
    if weak_verbs:
        tips.append(
            ImprovementTip(
                category="Action Verbs & Phrasing",
                priority="medium",
                title="Replace Passive Verbs with High-Impact Action Verbs",
                description=(
                    f"Detected passive or weak phrases: {', '.join(weak_verbs[:4])}. "
                    "Passive phrasing diminishes the perceived ownership of your contributions."
                ),
                action_item=(
                    "Replace phrases like 'responsible for' or 'helped with' with active power verbs like "
                    "'Spearheaded', 'Architected', 'Streamlined', 'Engineered', or 'Deployed'."
                ),
            )
        )

    # 6. Missing Sections Check
    missing_sections = ats_data.get("sections_missing", [])
    important_missing = [s for s in missing_sections if s in ["Summary / Objective", "Projects", "Certifications"]]
    if important_missing:
        tips.append(
            ImprovementTip(
                category="ATS & Structure",
                priority="medium",
                title=f"Add Dedicated '{important_missing[0]}' Section",
                description=(
                    f"A standard '{important_missing[0]}' section was not detected. Standard headings help ATS parsers "
                    "correctly categorize your qualifications."
                ),
                action_item=(
                    f"Create a distinct section labeled '{important_missing[0]}' with clear heading styling."
                ),
            )
        )

    return tips


def generate_suggested_bullets(
    missing_skills: List[str],
    matched_skills: List[str],
    weak_requirements: List[RequirementMatch],
) -> List[str]:
    """
    Generate tailored bullet point suggestions following the Google XYZ formula.
    """
    suggestions = []

    # Prioritize missing skills to close gaps, otherwise use matched skills to strengthen impact
    skills_to_use = missing_skills[:4] if missing_skills else matched_skills[:4]

    if "Docker" in skills_to_use or "Kubernetes" in skills_to_use:
        suggestions.append(
            "Containerized and deployed microservices using Docker and Kubernetes, achieving 99.9% uptime and cutting deployment cycle times by 40%."
        )
    if "PostgreSQL" in skills_to_use or "SQL" in skills_to_use:
        suggestions.append(
            "Architected high-throughput relational data models in PostgreSQL, optimizing query indexing to reduce read latency by 45% across 5M+ records."
        )
    if "AWS" in skills_to_use or "Google Cloud Platform" in skills_to_use or "Azure" in skills_to_use:
        cloud = "AWS" if "AWS" in skills_to_use else ("Google Cloud Platform" if "Google Cloud Platform" in skills_to_use else "Azure")
        suggestions.append(
            f"Engineered and automated cloud infrastructure on {cloud} using Terraform and CI/CD pipelines, reducing cloud hosting costs by 22%."
        )
    if "FastAPI" in skills_to_use or "Django" in skills_to_use or "Python" in skills_to_use:
        suggestions.append(
            "Designed and implemented high-performance asynchronous REST APIs in Python/FastAPI, handling over 10,000 requests per minute with sub-50ms latency."
        )
    if any(s in skills_to_use for s in ["Machine Learning", "PyTorch", "NLP", "LLMs"]):
        suggestions.append(
            "Spearheaded development of a production NLP/Machine Learning pipeline with PyTorch, boosting classification accuracy from 82% to 94%."
        )
    if "React" in skills_to_use or "TypeScript" in skills_to_use:
        suggestions.append(
            "Developed responsive, accessible web interfaces using React and TypeScript, improving Core Web Vitals and user conversion by 18%."
        )

    # If any weak requirements exist, synthesize a targeted requirement bullet
    unaddressed = [r for r in weak_requirements if r.status == "Missing / Weak"]
    if unaddressed and len(suggestions) < 3:
        req_clean = re.sub(r'^[•\-\*\d\.\s]+', '', unaddressed[0].requirement).strip()
        suggestions.append(
            f"Spearheaded initiatives aligned with {req_clean[:80]}, collaborating with cross-functional partners to deliver projects 2 weeks ahead of schedule."
        )

    # General fallback suggestions if specific skill bullets were not triggered
    if len(suggestions) < 2:
        top_skills = (missing_skills + matched_skills)[:2]
        skill_sample = ", ".join(top_skills) if top_skills else "core technologies"
        suggestions.append(
            f"Spearheaded integration of {skill_sample} into production workflows, enhancing system scalability and decreasing delivery turnaround by 30%."
        )
        suggestions.append(
            f"Optimized automated CI/CD and deployment pipelines, reducing release rollback rates by 35% and accelerating feature turnaround."
        )

    return suggestions[:4]


def score_resume(
    resume_text: str,
    job_description: Optional[str] = None,
    target_company: Optional[str] = None,
    experience_type: str = "fresher",
    years_of_experience: float = 0.0,
    target_role: str = "Software Engineer",
    custom_weights: Optional[Dict[str, float]] = None,
) -> ScoreResponse:
    """
    Main orchestrator for scoring a resume against a job description or automatically discovered company profile.
    Dynamically adjusts criteria for Freshers vs Experienced candidates.
    """
    matcher = SemanticMatcher.get_instance()
    is_fresher = experience_type.lower() == "fresher" or years_of_experience < 1.5

    # 1. Company Profile Discovery (if company provided or JD omitted)
    company_profile: Optional[CompanyProfile] = None
    if target_company and target_company.strip():
        company_profile = get_company_intelligence(
            company_name=target_company.strip(),
            experience_type=experience_type,
            years_of_experience=years_of_experience,
            target_role=target_role,
        )
        if not job_description or len(job_description.strip()) < 20 or "target level" in job_description.lower():
            job_description = company_profile.target_job_description
    elif not job_description or len(job_description.strip()) < 20:
        # Fallback to general tech company profile
        company_profile = get_company_intelligence(
            company_name="Technology Organization",
            experience_type=experience_type,
            years_of_experience=years_of_experience,
            target_role=target_role,
        )
        job_description = company_profile.target_job_description

    # 2. Overall Semantic Similarity (Cosine Similarity via SentenceTransformer)
    semantic_sim = matcher.compute_similarity(resume_text, job_description)
    semantic_score = round(semantic_sim * 100.0, 1)

    # 3. Skills Extraction and Alignment
    jd_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)

    matched_skills = sorted(list(jd_skills.intersection(resume_skills)))
    missing_skills = sorted(list(jd_skills - resume_skills))
    additional_skills = sorted(list(resume_skills - jd_skills))

    if jd_skills:
        skill_match_ratio = len(matched_skills) / len(jd_skills)
        additional_boost = min(0.08, len(additional_skills) * 0.01)
        raw_skill_score = min(1.0, skill_match_ratio + additional_boost)
        skill_score = round(raw_skill_score * 100.0, 1)
    else:
        skill_score = semantic_score

    # Categorize skills for rich UI breakdown
    jd_cat = categorize_skills(jd_skills)
    res_cat = categorize_skills(resume_skills)
    all_categories = sorted(list(set(jd_cat.keys()).union(set(res_cat.keys()))))

    categories_breakdown: Dict[str, SkillCategoryBreakdown] = {}
    for cat in all_categories:
        cat_matched = [s for s in matched_skills if SKILL_TO_CATEGORY.get(s) == cat]
        cat_missing = [s for s in missing_skills if SKILL_TO_CATEGORY.get(s) == cat]
        if cat_matched or cat_missing:
            categories_breakdown[cat] = SkillCategoryBreakdown(
                matched=cat_matched,
                missing=cat_missing,
            )

    skills_analysis = SkillMatch(
        score=skill_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        additional_skills=additional_skills[:12],
        categories=categories_breakdown,
    )

    # 4. Requirement-by-Requirement Semantic Matching
    jd_requirements = extract_requirements_from_jd(job_description)
    resume_sentences = split_into_meaningful_sentences(resume_text)

    req_matches_raw = matcher.match_requirements_to_resume(jd_requirements, resume_sentences)

    requirements_analysis: List[RequirementMatch] = []
    strong_or_moderate_count = 0

    for req, best_match, sim in req_matches_raw:
        sim_percent = round(sim * 100.0, 1)
        if sim >= 0.65:
            status = "Strong Match"
            strong_or_moderate_count += 1
        elif sim >= 0.45:
            status = "Moderate Match"
            strong_or_moderate_count += 1
        else:
            status = "Missing / Weak"

        requirements_analysis.append(
            RequirementMatch(
                requirement=req,
                best_matching_resume_text=best_match,
                similarity=sim_percent,
                status=status,
            )
        )

    if jd_requirements:
        req_coverage_score = round((strong_or_moderate_count / len(jd_requirements)) * 100.0, 1)
    else:
        req_coverage_score = semantic_score

    # 5. ATS & Structural Health Analysis (with Fresher accommodations)
    ats_dict = analyze_ats(resume_text)
    ats_health_score = ats_dict["score"]

    if is_fresher and "Projects" in ats_dict.get("sections_found", []):
        # Compensate freshers for shorter work experience if they have projects
        ats_health_score = min(100.0, ats_health_score + 10.0)

    ats_analysis = ATSAnalysis(
        score=ats_health_score,
        sections_found=ats_dict["sections_found"],
        sections_missing=ats_dict["sections_missing"],
        action_verbs_count=ats_dict["action_verbs_count"],
        action_verbs_found=ats_dict["action_verbs_found"],
        weak_verbs_found=ats_dict["weak_verbs_found"],
        quantification_score=ats_dict["quantification_score"],
        metrics_found=ats_dict["metrics_found"],
        contact_info=ats_dict["contact_info"],
        word_count=ats_dict["word_count"],
        estimated_pages=ats_dict["estimated_pages"],
    )

    # 6. Combined Overall Score Calculation
    # Freshers have higher weight on Skills & Projects, Experienced on System Context
    if is_fresher:
        w_sem = 0.30
        w_skl = 0.40
        w_req = 0.20
        w_ats = 0.10
    else:
        w_sem = 0.35
        w_skl = 0.35
        w_req = 0.20
        w_ats = 0.10

    if custom_weights:
        w_sem = custom_weights.get("semantic", w_sem)
        w_skl = custom_weights.get("skills", w_skl)
        w_req = custom_weights.get("requirements", w_req)
        w_ats = custom_weights.get("ats", w_ats)
        total_w = w_sem + w_skl + w_req + w_ats
        if total_w > 0:
            w_sem /= total_w
            w_skl /= total_w
            w_req /= total_w
            w_ats /= total_w

    raw_overall = (
        (semantic_score * w_sem) +
        (skill_score * w_skl) +
        (req_coverage_score * w_req) +
        (ats_health_score * w_ats)
    )

    # 6b. Company-Specific Hiring Bar & Tier Calibration
    company_adjustment = 0.0
    if company_profile:
        tier_lower = str(company_profile.tier).lower()
        overview_lower = str(company_profile.overview).lower()
        resume_lower = resume_text.lower()

        has_dsa_platform = any(cp in resume_lower for cp in ["leetcode", "codeforces", "codechef", "hackerrank", "geeksforgeeks"])
        has_distributed_tech = any(k in resume_lower for k in ["distributed", "microservices", "kafka", "redis", "concurrency", "multithreading"])
        has_devops_cloud = any(k in resume_lower for k in ["docker", "kubernetes", "aws", "gcp", "azure", "ci/cd"])
        has_web_apis = any(k in resume_lower for k in ["rest api", "restful", "fastapi", "flask", "django", "express", "spring", "react", "node"])

        is_tier1 = any(k in tier_lower for k in ["faang", "tier-1", "tier 1", "extremely high"]) or "extremely high" in overview_lower
        is_startup = any(k in tier_lower for k in ["startup", "unicorn", "product", "high-growth", "high growth"])
        is_services = any(k in tier_lower for k in ["services", "consulting", "global it"])

        if is_tier1:
            # High algorithmic bar: reward DSA/scale, penalize lack of algorithms
            if has_dsa_platform:
                company_adjustment += 3.0
            else:
                company_adjustment -= 5.0
            if has_distributed_tech:
                company_adjustment += 3.0
            else:
                company_adjustment -= 4.0
        elif is_startup:
            # Startup / Product bar: reward practical APIs, databases, Docker, speed
            if has_web_apis:
                company_adjustment += 4.0
            if has_devops_cloud or has_distributed_tech:
                company_adjustment += 3.0
            if "github.com" in resume_lower:
                company_adjustment += 2.0
        elif is_services:
            # IT Services bar: strong credit for degree, core programming fundamentals, and clean ATS layout
            if any(deg in resume_lower for deg in ["b.tech", "b.e", "bachelor", "computer science", "information technology", "mca"]):
                company_adjustment += 5.0
            if ats_health_score >= 70:
                company_adjustment += 3.0

    overall_score = round(max(5.0, min(99.0, raw_overall + company_adjustment)), 1)

    grade, summary = calculate_grade(overall_score)

    sub_scores_map = {
        "semantic_similarity": semantic_score,
        "skill_match": skill_score,
        "requirement_coverage": req_coverage_score,
        "ats_health": ats_health_score,
    }

    # 7. Actionable Improvement Tips (Customized for Fresher vs Exp)
    improvement_tips = generate_improvement_tips(
        missing_skills=missing_skills,
        matched_skills=matched_skills,
        unmatched_requirements=requirements_analysis,
        ats_data=ats_dict,
        sub_scores=sub_scores_map,
        experience_type=experience_type,
        years_of_experience=years_of_experience,
        company_name=company_profile.company_name if company_profile else None,
    )

    # 8. Suggested Tailored Bullets
    suggested_bullets = generate_suggested_bullets(
        missing_skills=missing_skills,
        matched_skills=matched_skills,
        weak_requirements=requirements_analysis,
    )

    # 9. Company Acceptance Roadmap & Gap Analysis
    company_roadmap = None
    if company_profile:
        company_roadmap = build_company_roadmap(
            resume_text=resume_text,
            company_profile=company_profile,
            experience_type=experience_type,
            years_of_experience=years_of_experience,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            ats_data=ats_dict,
        )

    return ScoreResponse(
        overall_score=overall_score,
        grade=grade,
        summary=summary,
        sub_scores=SubScores(**sub_scores_map),
        skills_analysis=skills_analysis,
        requirements_analysis=requirements_analysis,
        ats_analysis=ats_analysis,
        improvement_tips=improvement_tips,
        suggested_bullet_points=suggested_bullets,
        experience_type=experience_type,
        years_of_experience=years_of_experience,
        company_profile=company_profile,
        company_roadmap=company_roadmap,
    )
