"""Data models and Pydantic schemas for the AI-Powered Resume Scorer."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ScoreRequest(BaseModel):
    """Request payload for scoring text resume against job description or target company."""
    resume_text: str = Field(..., min_length=20, description="Extracted resume text")
    job_description: Optional[str] = Field(
        default=None,
        description="Optional manual job description text. If empty, automatically discovered from target_company!",
    )
    target_company: Optional[str] = Field(
        default=None,
        description="Target company name (e.g. Google, Microsoft, Amazon, TCS, Infosys, or any company worldwide)",
    )
    experience_type: Optional[str] = Field(
        default="fresher",
        description="'fresher' (Campus / Entry Level) or 'experienced' (Working Professional)",
    )
    years_of_experience: Optional[float] = Field(
        default=0.0,
        ge=0.0,
        le=50.0,
        description="Years of professional experience (0 for freshers)",
    )
    target_role: Optional[str] = Field(
        default="Software Engineer",
        description="Target engineering role (e.g. SDE-1, Full Stack, Backend, Data Scientist)",
    )
    weights: Optional[Dict[str, float]] = Field(
        default=None,
        description="Optional custom weights for scoring components (semantic, skills, requirements, ats)",
    )


class SkillCategoryBreakdown(BaseModel):
    """Categorized breakdown of matched and missing skills."""
    matched: List[str] = Field(default_factory=list)
    missing: List[str] = Field(default_factory=list)


class SkillMatch(BaseModel):
    """Skills and keyword overlap evaluation."""
    score: float = Field(..., ge=0.0, le=100.0, description="Skill match score (0-100)")
    matched_skills: List[str] = Field(default_factory=list, description="Skills present in both JD and Resume")
    missing_skills: List[str] = Field(default_factory=list, description="Skills in JD but missing in Resume")
    additional_skills: List[str] = Field(default_factory=list, description="Relevant skills in Resume not in JD")
    categories: Dict[str, SkillCategoryBreakdown] = Field(
        default_factory=dict,
        description="Skills categorized by domain (e.g. Languages, Cloud, Frameworks)",
    )


class RequirementMatch(BaseModel):
    """Semantic match of an individual job requirement against resume bullet points."""
    requirement: str
    best_matching_resume_text: str
    similarity: float = Field(..., ge=0.0, le=100.0)
    status: str = Field(..., description="'Strong Match', 'Moderate Match', or 'Missing / Weak'")


class ATSAnalysis(BaseModel):
    """ATS readability, structural health, and impact metrics analysis."""
    score: float = Field(..., ge=0.0, le=100.0)
    sections_found: List[str] = Field(default_factory=list)
    sections_missing: List[str] = Field(default_factory=list)
    action_verbs_count: int = 0
    action_verbs_found: List[str] = Field(default_factory=list)
    weak_verbs_found: List[str] = Field(default_factory=list)
    quantification_score: float = Field(default=0.0, ge=0.0, le=100.0)
    metrics_found: List[str] = Field(default_factory=list)
    contact_info: Dict[str, bool] = Field(default_factory=dict)
    word_count: int = 0
    estimated_pages: int = 1


class ImprovementTip(BaseModel):
    """Specific, actionable improvement tip."""
    category: str = Field(..., description="e.g. 'Skills & Keywords', 'Quantifiable Impact', 'ATS & Structure'")
    priority: str = Field(..., description="'high', 'medium', or 'low'")
    title: str
    description: str
    action_item: Optional[str] = None


class SubScores(BaseModel):
    """Individual breakdown scores (0-100)."""
    semantic_similarity: float = Field(..., ge=0.0, le=100.0)
    skill_match: float = Field(..., ge=0.0, le=100.0)
    requirement_coverage: float = Field(..., ge=0.0, le=100.0)
    ats_health: float = Field(..., ge=0.0, le=100.0)


class ExamRound(BaseModel):
    round_number: int
    name: str
    format: str
    duration: str
    focus_areas: List[str]
    description: str


class CompanyProfile(BaseModel):
    company_name: str
    industry: str
    tier: str
    headquarters: str
    overview: str
    target_role: str
    experience_level_assumed: str
    exam_pattern: List[ExamRound]
    eligibility_criteria: Dict[str, Any]
    coding_expectations: Dict[str, Any]
    project_expectations: List[str]
    hiring_tips: List[str]
    target_job_description: str


class CompanyRoadmap(BaseModel):
    company_name: str
    eligibility_status: str  # "Eligible", "Conditionally Eligible", "Action Required"
    eligibility_details: List[str]
    resume_gaps_for_company: List[str]
    preparation_roadmap: List[Dict[str, str]]
    must_have_additions: List[str]


class ScoreResponse(BaseModel):
    """Complete score evaluation report."""
    overall_score: float = Field(..., ge=0.0, le=100.0)
    grade: str = Field(..., description="Letter grade with description (e.g. 'A (Strong Match)')")
    summary: str = Field(..., description="Executive summary of candidate fit")
    sub_scores: SubScores
    skills_analysis: SkillMatch
    requirements_analysis: List[RequirementMatch]
    ats_analysis: ATSAnalysis
    improvement_tips: List[ImprovementTip]
    suggested_bullet_points: List[str] = Field(
        default_factory=list,
        description="Tailored bullet points that can be adapted and added to the resume",
    )
    experience_type: str = "fresher"
    years_of_experience: float = 0.0
    company_profile: Optional[CompanyProfile] = None
    company_roadmap: Optional[CompanyRoadmap] = None


class ExtractTextResponse(BaseModel):
    """Response payload for document text extraction."""
    filename: str
    text: str
    page_count: int
    word_count: int
    char_count: int


class SampleRole(BaseModel):
    """Pre-loaded sample job description and resume pair for quick demonstration."""
    id: str
    title: str
    company: str
    level: str
    job_description: str
    sample_resume: str
