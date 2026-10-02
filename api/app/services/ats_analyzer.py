"""ATS structure, action verbs, and quantifiable metrics analyzer."""

import re
from typing import Any, Dict, List, Set


# Standard ATS Resume Sections
STANDARD_SECTIONS = {
    "Summary / Objective": [
        r"\b(?:professional\s+)?summary\b",
        r"\bobjective\b",
        r"\bprofile\b",
        r"\babout\s+me\b",
    ],
    "Experience": [
        r"\b(?:work\s+)?experience\b",
        r"\bemployment\s+history\b",
        r"\bprofessional\s+experience\b",
        r"\bwork\s+history\b",
    ],
    "Education": [
        r"\beducation\b",
        r"\bacademic\s+(?:background|history)\b",
        r"\bqualifications\b",
        r"\bdegrees\b",
    ],
    "Skills": [
        r"\b(?:technical\s+)?skills\b",
        r"\bcore\s+competencies\b",
        r"\btechnologies\b",
        r"\btools\s+(?:&|and)\s+technologies\b",
    ],
    "Projects": [
        r"\bprojects\b",
        r"\bkey\s+projects\b",
        r"\bpersonal\s+projects\b",
        r"\bportfolio\b",
    ],
    "Certifications": [
        r"\bcertifications?\b",
        r"\blicenses?\b",
        r"\bcertificates?\b",
        r"\bcourses?\b",
    ],
}

# Strong impact-driven action verbs (ATS favorites)
STRONG_ACTION_VERBS = [
    "accelerated", "accomplished", "achieved", "acquired", "administered", "advanced",
    "analyzed", "architected", "automated", "boosted", "built", "centralized", "championed",
    "coached", "collaborated", "consolidated", "constructed", "coordinated", "created",
    "decreased", "delivered", "deployed", "designed", "developed", "devised", "directed",
    "doubled", "drove", "eliminated", "enabled", "engineered", "enhanced", "established",
    "evaluated", "executed", "expanded", "expedited", "fabricated", "facilitated", "forecasted",
    "formulated", "founded", "generated", "guided", "headed", "implemented", "improved",
    "increased", "initiated", "innovated", "inspected", "instituted", "integrated", "introduced",
    "invented", "launched", "lead", "led", "managed", "maximized", "mentored", "migrated",
    "minimized", "modernized", "negotiated", "optimized", "orchestrated", "overhauled", "oversaw",
    "pioneered", "planned", "produced", "programmed", "promoted", "reduced", "reengineered",
    "refactored", "resolved", "restructured", "revamped", "scaled", "secured", "simplified",
    "spearheaded", "standardized", "streamlined", "strengthened", "surpassed", "transformed",
    "tripled", "unified", "upgraded", "validated"
]

# Weak or passive phrases to avoid
WEAK_PASSIVE_PHRASES = [
    "helped", "assisted", "worked on", "handled", "was responsible for", "responsible for",
    "participated in", "attempted", "contributed to", "involved in", "duties included",
    "tried to", "part of team that"
]

# Regex patterns for contact information
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
PHONE_PATTERN = re.compile(r'(?:\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}')
LINKEDIN_GITHUB_PATTERN = re.compile(r'(?:linkedin\.com\/in\/|github\.com\/)[A-Za-z0-9_-]+', re.IGNORECASE)

# Regex pattern for quantifiable metrics (percentages, dollar amounts, multiples, numbers with units)
METRIC_PATTERNS = [
    re.compile(r'\b\d+(?:\.\d+)?%'),                                   # e.g., 25%, 99.9%
    re.compile(r'[\$€£¥]\s*\d+(?:,\d{3})*(?:\.\d+)?(?:\s*[kKmMbB])?'),  # e.g., $100K, $2.5M
    re.compile(r'\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:users|clients|customers|requests|queries|nodes|servers|engineers|people|members)\b', re.IGNORECASE),
    re.compile(r'\b(?:reduced|increased|boosted|saved|grew|cut|sped up)\b.*?\b\d+(?:\.\d+)?%?', re.IGNORECASE),
    re.compile(r'\b\d+x\b'),                                            # e.g., 10x, 3x faster
]


def detect_sections(text: str) -> Dict[str, Any]:
    """Check for standard resume section headings."""
    found = []
    missing = []

    text_lower = text.lower()
    for section_name, patterns in STANDARD_SECTIONS.items():
        matched = False
        for pat in patterns:
            if re.search(pat, text_lower):
                matched = True
                break
        if matched:
            found.append(section_name)
        else:
            missing.append(section_name)

    return {"found": found, "missing": missing}


def detect_action_verbs(text: str) -> Dict[str, Any]:
    """Identify presence of strong impact action verbs and flag weak/passive verbs."""
    text_lower = text.lower()

    found_strong = set()
    for verb in STRONG_ACTION_VERBS:
        # Match word boundary
        if re.search(rf'\b{re.escape(verb)}\b', text_lower):
            found_strong.add(verb.capitalize())

    found_weak = set()
    for phrase in WEAK_PASSIVE_PHRASES:
        if re.search(rf'\b{re.escape(phrase)}\b', text_lower):
            found_weak.add(phrase)

    return {
        "strong_count": len(found_strong),
        "strong_verbs": sorted(list(found_strong)),
        "weak_verbs": sorted(list(found_weak)),
    }


def detect_quantifiable_metrics(text: str) -> List[str]:
    """Find specific quantifiable achievements and measurable numbers in the resume."""
    metrics_found = set()

    for pattern in METRIC_PATTERNS:
        matches = pattern.findall(text)
        for m in matches:
            if isinstance(m, str):
                cleaned = m.strip()
                if len(cleaned) > 1 and cleaned not in metrics_found:
                    metrics_found.add(cleaned)

    return sorted(list(metrics_found))


def analyze_contact_info(text: str) -> Dict[str, bool]:
    """Check whether candidate contact essentials exist."""
    return {
        "has_email": bool(EMAIL_PATTERN.search(text)),
        "has_phone": bool(PHONE_PATTERN.search(text)),
        "has_linkedin_github": bool(LINKEDIN_GITHUB_PATTERN.search(text)),
    }


def analyze_ats(text: str) -> Dict[str, Any]:
    """
    Perform a complete ATS (Applicant Tracking System) scan of the resume text.
    Evaluates sections, action verbs, impact quantification, contact details, and length.
    Returns a unified ATS score (0 - 100) and detailed diagnostic breakdown.
    """
    words = text.split()
    word_count = len(words)
    estimated_pages = max(1, (word_count + 399) // 400)

    # 1. Section Analysis (30 points max)
    sections_res = detect_sections(text)
    essential_sections = {"Experience", "Education", "Skills"}
    found_set = set(sections_res["found"])
    essential_found = len(essential_sections.intersection(found_set))
    other_found = len(found_set - essential_sections)
    # 3 essentials = 20 pts, up to 2 other sections = 10 pts
    section_score = (essential_found / 3.0) * 20.0 + min(10.0, other_found * 5.0)

    # 2. Action Verbs Analysis (25 points max)
    verbs_res = detect_action_verbs(text)
    strong_count = verbs_res["strong_count"]
    # 8+ strong action verbs yields full points
    verb_score = min(25.0, (strong_count / 8.0) * 25.0)
    # Penalize slightly for passive phrases
    weak_count = len(verbs_res["weak_verbs"])
    verb_score = max(0.0, verb_score - (weak_count * 2.5))

    # 3. Measurable Impact & Quantification (25 points max)
    metrics = detect_quantifiable_metrics(text)
    # 5+ metrics yields full points
    quant_score = min(25.0, (len(metrics) / 5.0) * 25.0)

    # 4. Contact Information (10 points max)
    contact = analyze_contact_info(text)
    contact_score = 0.0
    if contact["has_email"]:
        contact_score += 4.0
    if contact["has_phone"]:
        contact_score += 3.0
    if contact["has_linkedin_github"]:
        contact_score += 3.0

    # 5. Length & Formatting (10 points max)
    length_score = 10.0
    if word_count < 200:
        length_score = 3.0
    elif word_count < 300:
        length_score = 6.0
    elif word_count > 1500:
        length_score = 6.0

    total_ats_score = round(section_score + verb_score + quant_score + contact_score + length_score, 1)
    total_ats_score = max(0.0, min(100.0, total_ats_score))

    # Normalize quantification score to 0-100 for display
    quant_display = round((len(metrics) / 5.0) * 100.0, 1)
    quant_display = min(100.0, quant_display)

    return {
        "score": total_ats_score,
        "sections_found": sections_res["found"],
        "sections_missing": sections_res["missing"],
        "action_verbs_count": strong_count,
        "action_verbs_found": verbs_res["strong_verbs"][:15],
        "weak_verbs_found": verbs_res["weak_verbs"],
        "quantification_score": quant_display,
        "metrics_found": metrics[:10],
        "contact_info": contact,
        "word_count": word_count,
        "estimated_pages": estimated_pages,
    }
