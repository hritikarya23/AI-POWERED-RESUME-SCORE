"""Curated technical and soft skills taxonomy with domain categorization and alias mapping."""

import re
from typing import Dict, List, Set, Tuple


# Skill taxonomy grouped by category
SKILL_TAXONOMY: Dict[str, List[str]] = {
    "Languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "C", "Go", "Golang",
        "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "SQL", "PL/SQL",
        "Bash", "Shell", "PowerShell", "HTML", "HTML5", "CSS", "CSS3", "Sass",
        "Dart", "Elixir", "Haskell", "Perl", "Lua", "MATLAB", "Solidity"
    ],
    "Frameworks & Libraries": [
        "React", "React.js", "Next.js", "Angular", "Vue.js", "Vue", "Svelte",
        "Node.js", "Express", "Express.js", "NestJS", "FastAPI", "Django", "Flask",
        "Spring Boot", "Spring", "ASP.NET", ".NET Core", "Ruby on Rails", "Laravel",
        "PyTorch", "TensorFlow", "Keras", "Scikit-Learn", "Pandas", "NumPy",
        "SciPy", "spaCy", "NLTK", "HuggingFace", "Transformers", "LangChain",
        "LlamaIndex", "Tailwind CSS", "Bootstrap", "Material-UI", "Redux", "Zustand",
        "GraphQL", "Apollo", "gRPC", "OpenAPI", "JQuery", "Playwright", "Selenium",
        "Cypress", "Jest", "Pytest", "Mocha"
    ],
    "Cloud & DevOps": [
        "AWS", "Amazon Web Services", "Azure", "Microsoft Azure", "Google Cloud Platform", "GCP",
        "Docker", "Kubernetes", "K8s", "Terraform", "Ansible", "Puppet", "Chef",
        "Jenkins", "GitHub Actions", "GitLab CI", "CircleCI", "ArgoCD", "Helm",
        "Prometheus", "Grafana", "Datadog", "CloudWatch", "Linux", "Unix",
        "Ubuntu", "Debian", "Nginx", "Apache", "Serverless", "AWS Lambda",
        "ECS", "EKS", "GKE", "CloudFormation", "OpenShift"
    ],
    "Databases & Storage": [
        "PostgreSQL", "Postgres", "MySQL", "MongoDB", "Redis", "SQLite",
        "Elasticsearch", "OpenSearch", "Cassandra", "DynamoDB", "Neo4j",
        "Snowflake", "BigQuery", "Amazon Redshift", "Oracle Database", "MSSQL",
        "Microsoft SQL Server", "Couchbase", "Supabase", "Firebase",
        "Pinecone", "ChromaDB", "Milvus", "Weaviate", "Qdrant"
    ],
    "Data & AI": [
        "Machine Learning", "Deep Learning", "Artificial Intelligence", "Generative AI",
        "Large Language Models", "LLMs", "RAG", "Retrieval-Augmented Generation",
        "Natural Language Processing", "NLP", "Computer Vision", "Object Detection",
        "Data Engineering", "ETL", "ELT", "Apache Spark", "PySpark", "Apache Kafka",
        "Apache Airflow", "dbt", "Data Modeling", "Feature Engineering", "MLOps",
        "Tableau", "Power BI", "Data Visualization", "Fine-Tuning", "LoRA",
        "Prompt Engineering", "Reinforcement Learning"
    ],
    "Practices & Architecture": [
        "REST API", "RESTful APIs", "Microservices", "System Design", "Distributed Systems",
        "Agile", "Scrum", "Kanban", "Test-Driven Development", "TDD",
        "Continuous Integration", "Continuous Deployment", "CI/CD",
        "Object-Oriented Programming", "OOP", "Design Patterns", "Clean Code",
        "Event-Driven Architecture", "Domain-Driven Design", "DDD", "Git", "GitHub",
        "GitLab", "Bitbucket", "WebSockets", "OAuth", "JWT", "Cybersecurity", "Penetration Testing"
    ],
    "Soft Skills & Leadership": [
        "Leadership", "Mentorship", "Team Management", "Cross-Functional Collaboration",
        "Technical Leadership", "Project Management", "Stakeholder Management",
        "Problem Solving", "Critical Thinking", "Communication", "Strategic Planning",
        "Agile Coaching", "Customer Empathy", "Time Management", "Code Reviews"
    ]
}

# Normalization mapping: maps variations, acronyms, and aliases to canonical names
ALIAS_MAP: Dict[str, str] = {
    "golang": "Go",
    "k8s": "Kubernetes",
    "js": "JavaScript",
    "ts": "TypeScript",
    "py": "Python",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "react.js": "React",
    "reactjs": "React",
    "node": "Node.js",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "vue": "Vue.js",
    "vuejs": "Vue.js",
    "aws": "AWS",
    "amazon web services": "AWS",
    "gcp": "Google Cloud Platform",
    "google cloud": "Google Cloud Platform",
    "azure": "Azure",
    "microsoft azure": "Azure",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "continuous integration": "CI/CD",
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "ai": "Artificial Intelligence",
    "genai": "Generative AI",
    "gen ai": "Generative AI",
    "llm": "Large Language Models (LLMs)",
    "llms": "Large Language Models (LLMs)",
    "large language models": "Large Language Models (LLMs)",
    "rag": "RAG (Retrieval-Augmented Generation)",
    "retrieval augmented generation": "RAG (Retrieval-Augmented Generation)",
    "retrieval-augmented generation": "RAG (Retrieval-Augmented Generation)",
    "nlp": "Natural Language Processing (NLP)",
    "natural language processing": "Natural Language Processing (NLP)",
    "cv": "Computer Vision",
    "tdd": "Test-Driven Development (TDD)",
    "test driven development": "Test-Driven Development (TDD)",
    "oop": "Object-Oriented Programming (OOP)",
    "rest": "REST API",
    "restful": "REST API",
    "rest api": "REST API",
    "rest apis": "REST API",
    "restful apis": "REST API",
    "tailwind": "Tailwind CSS",
    "tailwindcss": "Tailwind CSS",
    "tf": "TensorFlow",
    "pytorch": "PyTorch",
    "scikit-learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "spacy": "spaCy",
    "huggingface": "HuggingFace",
    "mongo": "MongoDB",
    "express": "Express.js",
    "spring": "Spring Boot",
    "dotnet": "ASP.NET / .NET",
    ".net": "ASP.NET / .NET",
    ".net core": "ASP.NET / .NET",
    "nextjs": "Next.js",
    "next": "Next.js",
    "kafka": "Apache Kafka",
    "spark": "Apache Spark",
    "airflow": "Apache Airflow",
    "elastic search": "Elasticsearch",
}

# Reverse lookup from canonical skill name to its category
SKILL_TO_CATEGORY: Dict[str, str] = {}
for category, skills in SKILL_TAXONOMY.items():
    for skill in skills:
        canonical = ALIAS_MAP.get(skill.lower(), skill)
        SKILL_TO_CATEGORY[canonical] = category


def build_skill_patterns() -> List[Tuple[re.Pattern, str]]:
    """
    Build compiled regex patterns for all skills and aliases.
    Skills with special characters (like C++, C#, .NET, CI/CD) are handled accurately.
    Multi-word skills are ordered first to prevent greedy sub-term matches.
    """
    all_terms: Dict[str, str] = {}

    # Register taxonomy skills
    for category, skills in SKILL_TAXONOMY.items():
        for skill in skills:
            canonical = ALIAS_MAP.get(skill.lower(), skill)
            all_terms[skill.lower()] = canonical

    # Register aliases
    for alias, canonical in ALIAS_MAP.items():
        all_terms[alias.lower()] = canonical

    # Sort descending by length so longer phrases match before sub-tokens
    sorted_terms = sorted(all_terms.keys(), key=lambda t: len(t), reverse=True)

    patterns = []
    for term in sorted_terms:
        canonical = all_terms[term]
        # Handle specific special character terms
        if term in ("c++", "c#", ".net", ".net core"):
            escaped = re.escape(term)
            pattern = re.compile(rf'(?:^|[\s,;/()\[\]]){escaped}(?:[\s,;/()\[\]]|$)', re.IGNORECASE)
        elif term in ("c", "r"):
            # Single-letter programming languages require strict boundary checks
            escaped = re.escape(term)
            pattern = re.compile(rf'(?:^|[\s,;/()\[\]]){escaped}(?:[\s,;/()\[\]]|$)', re.IGNORECASE)
        elif "/" in term:
            escaped = re.escape(term)
            pattern = re.compile(rf'(?:^|[\s,;()\[\]]){escaped}(?:[\s,;()\[\]]|$)', re.IGNORECASE)
        else:
            escaped = re.escape(term)
            pattern = re.compile(rf'\b{escaped}\b', re.IGNORECASE)

        patterns.append((pattern, canonical))

    return patterns


COMPILED_PATTERNS = build_skill_patterns()


def extract_skills(text: str) -> Set[str]:
    """
    Extract all detected skills from text, returning canonical skill names.
    """
    if not text:
        return set()

    found_skills: Set[str] = set()

    # Pre-pad text with spaces for boundary regexes
    padded_text = f" {text} "

    for pattern, canonical in COMPILED_PATTERNS:
        if pattern.search(padded_text):
            found_skills.add(canonical)

    return found_skills


def categorize_skills(skills: Set[str]) -> Dict[str, List[str]]:
    """Group extracted skills into taxonomy categories."""
    categorized: Dict[str, List[str]] = {cat: [] for cat in SKILL_TAXONOMY.keys()}
    categorized["Other Skills"] = []

    for skill in sorted(skills):
        cat = SKILL_TO_CATEGORY.get(skill, "Other Skills")
        if cat in categorized:
            categorized[cat].append(skill)
        else:
            categorized["Other Skills"].append(skill)

    # Filter out empty categories
    return {k: v for k, v in categorized.items() if v}
