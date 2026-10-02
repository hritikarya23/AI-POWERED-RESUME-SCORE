"""Company Intelligence Engine: Pre-loaded hiring intelligence for world-leading companies
and dynamic AI discovery for any company worldwide."""

import re
from typing import Any, Dict, List, Optional
from app.models.schemas import CompanyProfile, CompanyRoadmap, ExamRound


# Pre-loaded curated knowledge base for the world's most sought-after employers
CURATED_COMPANIES: Dict[str, Dict[str, Any]] = {
    "google": {
        "company_name": "Google (Alphabet)",
        "industry": "Internet, Cloud, AI & Software Products",
        "tier": "Tier-1 Tech / FAANG",
        "headquarters": "Mountain View, CA, USA",
        "overview": "Global technology leader pioneering search, cloud computing, distributed systems, machine learning, and operating systems.",
        "eligibility_criteria": {
            "fresher": {
                "degree": "B.Tech/B.E, M.Tech, MS or PhD in Computer Science, IT, or Mathematics/related quantitative field",
                "cgpa_min": "No strict CGPA cutoff (typically 7.0+ / 70% preferred by campus recruiters)",
                "backlogs": "No active backlogs at time of joining",
                "experience": "0 - 1 Years (New Grad / Campus Hire)",
            },
            "experienced": {
                "degree": "Bachelor's/Master's degree in CS or equivalent practical experience",
                "cgpa_min": "Not applicable (evaluated on engineering depth and track record)",
                "experience": "2+ Years (L3/L4/L5 SWE based on tenure)",
            },
        },
        "coding_expectations": {
            "dsa_difficulty": "LeetCode Medium to Hard",
            "primary_topics": ["Graphs & Trees", "Dynamic Programming", "Tries & Strings", "Binary Search", "Heaps/Priority Queues"],
            "platforms": "Google Coding Environment, Google Meet + Google Docs/CoderPad",
            "clean_code_rules": "Time & space complexity analysis (Big-O), edge cases handling, modular OOP design",
        },
        "project_expectations": {
            "fresher": [
                "Full-stack or systems projects demonstrating high concurrency, networking, or distributed components",
                "Clean open-source contributions or competitive coding rankings (Codeforces, LeetCode 1800+, ICPC, Kickstart)",
                "Deep understanding of CS Fundamentals: OS (Processes/Threads), DBMS, Computer Networks",
            ],
            "experienced": [
                "Large-scale distributed systems handling millions of queries per second (QPS)",
                "Production experience with microservices, multi-region database scaling, and fault tolerance",
                "High-level and low-level architectural leadership and cross-team impact",
            ],
        },
        "exam_pattern": [
            ExamRound(
                round_number=1,
                name="Online Assessment / Screen",
                format="Online Coding Test (HackerEarth/CodeSignal) or 45-min Phone Screen",
                duration="60 - 90 Minutes",
                focus_areas=["DSA Problem Solving", "Array/String/Graph Algorithms", "Time Complexity Analysis"],
                description="2 algorithmic problems testing optimal data structures, edge case coverage, and Big-O efficiency.",
            ),
            ExamRound(
                round_number=2,
                name="Technical Round 1 (Algorithms & Data Structures)",
                format="1-on-1 Virtual Whiteboarding",
                duration="45 Minutes",
                focus_areas=["Complex Graph Traversal", "Dynamic Programming", "Tree Manipulation"],
                description="Live problem solving without code completion; explanation of thought process and tradeoffs.",
            ),
            ExamRound(
                round_number=3,
                name="Technical Round 2 (Algorithms or System Design)",
                format="1-on-1 Deep Technical",
                duration="45 Minutes",
                focus_areas=["Core CS / Concurrency for Freshers", "System Design (HLD/LLD) for Experienced"],
                description="Testing design scalability, microservices, caching, database sharding, or fundamental threading.",
            ),
            ExamRound(
                round_number=4,
                name="Googliness & Leadership",
                format="Behavioral / Cultural Alignment",
                duration="45 Minutes",
                focus_areas=["Navigating Ambiguity", "Collaborative Problem Solving", "Diversity & Inclusion", "Customer Focus"],
                description="Situational questions using the STAR framework to assess constructive teamwork and ethical problem solving.",
            ),
        ],
        "hiring_tips": [
            "Google engineers focus heavily on how you think out loud: articulate brute-force first, then optimize.",
            "Write syntactically correct code in your preferred language (C++, Java, Python, Go); avoid pseudo-code.",
            "Always test your code manually with boundary inputs (null, empty, negative, duplicates) before saying you are done.",
        ],
    },
    "microsoft": {
        "company_name": "Microsoft",
        "industry": "Cloud Computing, Enterprise Software, AI & Consumer Tech",
        "tier": "Tier-1 Tech / FAANG",
        "headquarters": "Redmond, WA, USA",
        "overview": "Pioneering technology multinational empowering organizations with Azure Cloud, Windows, Office 365, Teams, and Copilot AI.",
        "eligibility_criteria": {
            "fresher": {
                "degree": "B.Tech/B.E, M.Tech, MCA, MS in CS/IT/ECE or related branches",
                "cgpa_min": "7.0 CGPA or 70% aggregate throughout 10th, 12th, and College",
                "backlogs": "No active backlogs allowed",
                "experience": "0 - 1 Years",
            },
            "experienced": {
                "degree": "Bachelor's/Master's degree in CS, IT, or equivalent experience",
                "cgpa_min": "Not required",
                "experience": "2+ Years (SDE-1, SDE-2, Senior SDE)",
            },
        },
        "coding_expectations": {
            "dsa_difficulty": "LeetCode Medium",
            "primary_topics": ["Trees & Binary Search Trees", "Linked Lists", "Arrays & Two Pointers", "Hashing", "Recursion & Backtracking"],
            "platforms": "Codility / Microsoft Teams Live Share",
            "clean_code_rules": "Object-Oriented Design (SOLID), clean naming conventions, exception handling",
        },
        "project_expectations": {
            "fresher": [
                "Full-stack applications using modern stacks (React, ASP.NET Core, Java Spring, or Python/FastAPI)",
                "Solid grasp of OOP principles, Design Patterns (Factory, Singleton, Observer), and SQL databases",
                "Projects hosted on Azure or GitHub with active demo links and CI/CD pipelines",
            ],
            "experienced": [
                "Enterprise cloud scale services (Azure/AWS), distributed messaging (Kafka/Event Hubs), low latency APIs",
                "System design tradeoffs, telemetry, observability, and high-availability SLA management",
            ],
        },
        "exam_pattern": [
            ExamRound(
                round_number=1,
                name="Online Assessment (Codility)",
                format="Automated Coding Test",
                duration="75 - 90 Minutes",
                focus_areas=["Array Manipulation", "String Parsing", "Greedy/Sorting Algorithms"],
                description="3 coding questions focusing on correctness, memory efficiency, and corner case testing.",
            ),
            ExamRound(
                round_number=2,
                name="Technical Round 1 (Data Structures)",
                format="1-on-1 Live Coding",
                duration="45 - 60 Minutes",
                focus_areas=["Binary Trees", "HashMaps", "Linked Lists", "OOP Principles"],
                description="Deep dive into algorithmic problem solving and writing modular, production-ready code.",
            ),
            ExamRound(
                round_number=3,
                name="Technical Round 2 (Design & Projects)",
                format="1-on-1 Engineering Architecture",
                duration="45 - 60 Minutes",
                focus_areas=["Low-Level Design (LLD)", "Database Schema Design", "Resume Project Defense"],
                description="Explaining architecture decisions in past projects and designing a scalable modular feature.",
            ),
            ExamRound(
                round_number=4,
                name="AA (As-Appropriate / Partner) Interview",
                format="Executive & Cultural Evaluation",
                duration="45 - 60 Minutes",
                focus_areas=["Growth Mindset", "Customer Empathy", "Handling Conflicts", "System Scaling"],
                description="Discussion with a Partner/Principal Director on career vision, culture, and deep architectural choices.",
            ),
        ],
        "hiring_tips": [
            "Demonstrate a 'Growth Mindset'—Microsoft values curiosity and willingness to learn from failure.",
            "Write production-grade code with clear function signatures, modular classes, and input validations.",
        ],
    },
    "amazon": {
        "company_name": "Amazon",
        "industry": "E-Commerce, Cloud Computing (AWS), AI & Logistics",
        "tier": "Tier-1 Tech / FAANG",
        "headquarters": "Seattle, WA, USA",
        "overview": "World's largest e-commerce and cloud infrastructure powerhouse (AWS), driven by 16 Leadership Principles.",
        "eligibility_criteria": {
            "fresher": {
                "degree": "B.Tech/B.E, M.Tech, MCA in CS/IT/ECE or related fields",
                "cgpa_min": "6.5+ CGPA or 65% aggregate",
                "backlogs": "No active backlogs allowed",
                "experience": "0 - 1 Years (SDE-1 Campus/Off-Campus)",
            },
            "experienced": {
                "degree": "Bachelor's/Master's in CS or equivalent",
                "cgpa_min": "Not applicable",
                "experience": "2 - 5 Years (SDE-2) / 5+ Years (SDE-3)",
            },
        },
        "coding_expectations": {
            "dsa_difficulty": "LeetCode Medium (frequently asked Amazon top 100)",
            "primary_topics": ["Trees & Graphs (BFS/DFS)", "Heaps & Top-K Elements", "Sliding Window", "Dynamic Programming", "LRU Cache"],
            "platforms": "HackerRank / Amazon Chime Live Code",
            "clean_code_rules": "Amazon Leadership Principles integration in every answer, robust boundary tests",
        },
        "project_expectations": {
            "fresher": [
                "End-to-end full stack or cloud-deployed application (e.g. e-commerce store, real-time messaging, API service)",
                "Hands-on usage of databases (PostgreSQL/DynamoDB), AWS services (S3, Lambda, EC2), and Docker",
                "Strong grasp of OOP concepts, Clean Architecture, and unit testing",
            ],
            "experienced": [
                "High-throughput transactional architectures handling millions of daily orders/events",
                "Event-driven microservices with SQS, SNS, Kafka, and distributed cache (Redis/ElastiCache)",
                "Proven leadership, operational excellence, reducing latency, and cost optimization",
            ],
        },
        "exam_pattern": [
            ExamRound(
                round_number=1,
                name="Amazon Online Assessment (OA)",
                format="HackerRank Coding + Work Simulation",
                duration="90 - 120 Minutes",
                focus_areas=["2 Coding Questions (Medium)", "Work Simulation Assessment", "Work Style Survey"],
                description="Solving 2 algorithmic problems followed by simulated day-in-the-life workplace decision scenarios.",
            ),
            ExamRound(
                round_number=2,
                name="Technical Round 1 (Problem Solving & LP)",
                format="1-on-1 Interview",
                duration="60 Minutes",
                focus_areas=["DSA Live Coding", "Leadership Principles: Customer Obsession, Bias for Action"],
                description="25 mins discussing past achievements aligned with LPs, followed by 35 mins coding live.",
            ),
            ExamRound(
                round_number=3,
                name="Technical Round 2 (Design & LP)",
                format="1-on-1 Interview",
                duration="60 Minutes",
                focus_areas=["Object-Oriented Design (LLD)", "Leadership Principles: Ownership, Deliver Results"],
                description="Designing a real-world system (e.g. Locker Management, Parking Lot, Vending Machine).",
            ),
            ExamRound(
                round_number=4,
                name="The Bar Raiser Round",
                format="High-Standard Cross-Org Evaluation",
                duration="60 Minutes",
                focus_areas=["Deep Behavioral Probing", "Leadership Principles: Dive Deep, Have Backbone", "System Scalability"],
                description="Evaluated by an external Amazon Bar Raiser to ensure candidate raises the hiring bar above 50% of peers.",
            ),
        ],
        "hiring_tips": [
            "Prepare 2 distinct stories using the STAR method (Situation, Task, Action, Result) for EVERY one of Amazon's 16 Leadership Principles.",
            "Quantify your results: use exact percentages, request throughput numbers, and measurable business improvements.",
        ],
    },
    "tcs": {
        "company_name": "Tata Consultancy Services (TCS)",
        "industry": "IT Services, Digital Transformation & Enterprise Consulting",
        "tier": "Global IT Services",
        "headquarters": "Mumbai, India",
        "overview": "India's largest IT multinational enterprise operating in 55 countries, offering Ninja, Digital, and Prime engineering packages.",
        "eligibility_criteria": {
            "fresher": {
                "degree": "B.Tech/B.E, M.Tech, MCA, M.Sc (CS/IT) from recognized universities",
                "cgpa_min": "60% or 6.0 CGPA throughout 10th, 12th, Diploma, and Graduation",
                "backlogs": "Maximum 1 active backlog at time of exam, 0 backlogs at joining",
                "experience": "0 - 1 Years (NQT / Campus Recruitment)",
            },
            "experienced": {
                "degree": "Bachelor's / Master's degree in engineering or relevant discipline",
                "cgpa_min": "50% or 5.0 CGPA",
                "experience": "2 - 10+ Years (lateral hires across C2, C3, C4 bands)",
            },
        },
        "coding_expectations": {
            "dsa_difficulty": "Easy to Medium (NQT Digital / Prime)",
            "primary_topics": ["Arrays & Matrix Operations", "String Manipulation", "Number Theory & Math", "Basic Sorting/Searching", "Recursion"],
            "platforms": "TCS iON Assessment Platform",
            "clean_code_rules": "Valid syntax in C, C++, Java, or Python; compiling with all standard test cases within execution time limits",
        },
        "project_expectations": {
            "fresher": [
                "Final-year capstone project or major academic project with clear functional flow",
                "Basic full-stack, Android, Python, or IoT project with database integration (MySQL/SQLite)",
                "Solid clarity on DBMS (SQL queries, normalization), OOPs (Inheritance, Polymorphism), and SDLC models",
            ],
            "experienced": [
                "Enterprise migration, cloud transformation (AWS/Azure/GCP), microservices architecture",
                "Client-facing communication, Agile delivery, production maintenance, and team mentoring",
            ],
        },
        "exam_pattern": [
            ExamRound(
                round_number=1,
                name="TCS NQT (National Qualifier Test)",
                format="TCS iON CBT (Computer-Based Test)",
                duration="120 - 180 Minutes",
                focus_areas=["Numerical Ability", "Verbal Ability", "Reasoning Ability", "Foundation & Advanced Coding"],
                description="Part A: Cognitive Assessment (Aptitude). Part B: Technical Assessment & 2 Coding Questions for Digital/Prime bands.",
            ),
            ExamRound(
                round_number=2,
                name="Technical Interview (TR)",
                format="1-on-1 In-person or Teams Interview",
                duration="30 - 45 Minutes",
                focus_areas=["C/Java/Python Basics", "OOP Concepts", "SQL Queries & Normalization", "Final Year Project Explanation"],
                description="Technical grilling on fundamentals, code tracing, database queries, and role of candidate in college project.",
            ),
            ExamRound(
                round_number=3,
                name="Managerial & HR Interview (MR + HR)",
                format="Discussion with Panel",
                duration="20 - 30 Minutes",
                focus_areas=["Willingness to Relocate", "Shift Flexibility", "Workplace Ethics", "Communication Skills"],
                description="Evaluation of adaptability, verification of documents, commitment to service agreements, and soft skills.",
            ),
        ],
        "hiring_tips": [
            "For TCS Digital / Prime roles, solve BOTH coding questions completely with 100% test cases passed.",
            "Know your final-year college project inside-out: ER diagrams, tech stack choices, database schema, and challenges faced.",
        ],
    },
    "infosys": {
        "company_name": "Infosys",
        "industry": "IT Services & Next-Generation Digital Consulting",
        "tier": "Global IT Services",
        "headquarters": "Bengaluru, India",
        "overview": "Global leader in digital consulting, enterprise services, and AI solutions with Specialist Programmer (SP) and DSE bands.",
        "eligibility_criteria": {
            "fresher": {
                "degree": "B.E/B.Tech, M.E/M.Tech, MCA, M.Sc (CS/Electronics/Mathematics)",
                "cgpa_min": "60% or 6.5 CGPA throughout 10th, 12th, and College",
                "backlogs": "0 active backlogs allowed at the time of recruitment",
                "experience": "0 - 1 Years",
            },
            "experienced": {
                "degree": "B.E/B.Tech/MCA/equivalent",
                "cgpa_min": "50%+",
                "experience": "2 - 12 Years",
            },
        },
        "coding_expectations": {
            "dsa_difficulty": "Medium to Hard (HackWithInfy / SP)",
            "primary_topics": ["Dynamic Programming", "Graph Algorithms", "Greedy Approaches", "Bit Manipulation", "String Algorithms"],
            "platforms": "Infosys Springboard / HackerEarth",
            "clean_code_rules": "Time complexity limits are strictly enforced on large test cases",
        },
        "project_expectations": {
            "fresher": [
                "Meaningful software project in Java, Python, or Web Development (MERN / Spring Boot)",
                "Demonstrated certifications from Infosys Springboard, Coursera, or AWS",
                "Comprehensive understanding of Core Java / Python, OOP, and Relational Databases",
            ],
            "experienced": [
                "Enterprise integration, Spring Cloud, microservices, Angular/React, Kafka, CI/CD",
                "Cloud infrastructure management and domain expertise (Banking, Retail, Healthcare)",
            ],
        },
        "exam_pattern": [
            ExamRound(
                round_number=1,
                name="Infosys Online Test / HackWithInfy",
                format="Aptitude + Coding Exam",
                duration="100 - 180 Minutes",
                focus_areas=["Reasoning Ability", "Technical Data Interpretation", "Pseudocode", "3 Competitive Coding Questions"],
                description="Testing logical dexterity, pseudocode error debugging, and algorithmic coding challenges.",
            ),
            ExamRound(
                round_number=2,
                name="Technical Interview",
                format="1-on-1 Virtual Interview",
                duration="30 - 45 Minutes",
                focus_areas=["Data Structures", "OOP Concepts", "Database Joins & Normalization", "Project Walkthrough"],
                description="Live code explanation, logic building on common algorithms, and project code breakdown.",
            ),
            ExamRound(
                round_number=3,
                name="HR Interview",
                format="Personal Assessment",
                duration="15 - 20 Minutes",
                focus_areas=["Relocation Preferences", "Communication", "Leadership & Teamwork"],
                description="Verification of cultural fit, shift flexibility, and background credentials.",
            ),
        ],
        "hiring_tips": [
            "HackWithInfy or InfyTQ certifications give direct entry into the high-paying Specialist Programmer (SP) role (₹9.5 - 21 LPA).",
            "Strong command over SQL queries (Joins, Group By, Having, Subqueries) is tested in almost every Infosys TR interview.",
        ],
    },
    "wipro": {
        "company_name": "Wipro",
        "industry": "Information Technology, Consulting & Business Process Services",
        "tier": "Global IT Services",
        "headquarters": "Bengaluru, India",
        "overview": "Leading global technology services company delivering innovation across cloud, cybersecurity, and digital consulting.",
        "eligibility_criteria": {
            "fresher": {
                "degree": "B.E./B.Tech (all branches), M.E./M.Tech, 5-year Integrated-M.Tech",
                "cgpa_min": "60% or 6.0 CGPA throughout 10th, 12th, and Graduation",
                "backlogs": "Maximum 1 active backlog allowed at time of assessment",
                "experience": "0 - 1 Years (Elite / Turbo NLTH)",
            },
            "experienced": {
                "degree": "Graduate or Postgraduate in Engineering",
                "cgpa_min": "50%+",
                "experience": "2+ Years",
            },
        },
        "coding_expectations": {
            "dsa_difficulty": "Easy to Medium",
            "primary_topics": ["Arrays & Matrix Traversal", "Strings & Palindromes", "Patterns & Series", "Searching & Sorting"],
            "platforms": "AMCAT / CoCubes / Superset",
            "clean_code_rules": "Writing correct compilable code in Java, C, C++, or Python",
        },
        "project_expectations": {
            "fresher": [
                "Academic project highlighting real-world problem solving with clear architecture",
                "Knowledge of Git, software testing basics, and database CRUD operations",
            ],
            "experienced": [
                "Full-stack development, cloud migration, automated unit testing, enterprise DevOps",
            ],
        },
        "exam_pattern": [
            ExamRound(
                round_number=1,
                name="Wipro Elite NLTH Online Assessment",
                format="CBT on AMCAT/Superset",
                duration="128 Minutes",
                focus_areas=["Quantitative Aptitude", "Logical Reasoning", "Verbal English", "Written Communication (Essay)", "2 Coding Questions"],
                description="Comprehensive screening testing analytical competence, essay writing, and programming aptitude.",
            ),
            ExamRound(
                round_number=2,
                name="Technical Interview (TR)",
                format="Virtual Video Interview",
                duration="30 Minutes",
                focus_areas=["Programming Language Basics", "OOP Principles", "Data Structures", "Project Overview"],
                description="Checking fundamental clarity in candidate's declared favorite language and project architecture.",
            ),
            ExamRound(
                round_number=3,
                name="HR Interview",
                format="Behavioral Assessment",
                duration="15 - 20 Minutes",
                focus_areas=["Relocation Readiness", "Bond Agreement Acceptance", "Interpersonal Skills"],
                description="Ensuring alignment with company values, client shift hours, and joining formalities.",
            ),
        ],
        "hiring_tips": [
            "Wipro's essay writing round is auto-evaluated by an AI tool checking grammar, spelling, and sentence construction.",
            "Solving even 1.5 coding questions with all public and private test cases guarantees interview shortlisting.",
        ],
    },
    "uber": {
        "company_name": "Uber",
        "industry": "Ride-Hailing, Logistics, Mobility & Real-Time Distributed Systems",
        "tier": "Tier-1 Tech / Product",
        "headquarters": "San Francisco, CA, USA",
        "overview": "Global mobility platform connecting millions of riders and drivers in real-time with ultra-low latency distributed tech.",
        "eligibility_criteria": {
            "fresher": {
                "degree": "B.Tech/B.E, M.Tech, MS in CS or related disciplines",
                "cgpa_min": "7.5+ CGPA preferred",
                "backlogs": "0 active backlogs",
                "experience": "0 - 1 Years (SDE-1)",
            },
            "experienced": {
                "degree": "Bachelor's/Master's in CS or equivalent",
                "cgpa_min": "Not applicable",
                "experience": "2 - 5+ Years (SDE-2 / Senior)",
            },
        },
        "coding_expectations": {
            "dsa_difficulty": "LeetCode Medium to Hard",
            "primary_topics": ["Graphs & Shortest Path (Dijkstra, A*)", "Geohashing & Spatial Trees", "Concurrency & Multithreading", "DP", "Design Patterns"],
            "platforms": "CodeSignal / HackerRank",
            "clean_code_rules": "Low-level system design, thread safety, clean interfaces",
        },
        "project_expectations": {
            "fresher": [
                "Real-time projects featuring WebSockets, Redis pub/sub, map integration, or message queues (Kafka)",
                "Solid foundation in multithreading, concurrency locks, and distributed caching",
            ],
            "experienced": [
                "Geospatial routing, dynamic pricing algorithms, ultra-high throughput event processing",
                "Microservice orchestration with Go/Java, Kafka, Cassandra, and Kubernetes",
            ],
        },
        "exam_pattern": [
            ExamRound(
                round_number=1,
                name="CodeSignal Online Assessment",
                format="Automated General Coding Assessment",
                duration="70 - 90 Minutes",
                focus_areas=["4 Coding Questions: Arrays, HashMaps, Complex 2D Matrix, Graph Traversal"],
                description="Rigorous algorithmic challenges benchmarked against competitive global percentiles.",
            ),
            ExamRound(
                round_number=2,
                name="DSA & Problem Solving",
                format="1-on-1 Live Coding",
                duration="60 Minutes",
                focus_areas=["Dynamic Programming", "Graph Algorithms", "Concurrency"],
                description="Writing optimal production-grade code with thorough unit tests and Big-O proof.",
            ),
            ExamRound(
                round_number=3,
                name="System Design (LLD for Fresher / HLD for Exp)",
                format="Architecture Deep Dive",
                duration="60 Minutes",
                focus_areas=["Real-time Location Tracking", "Surge Pricing Engine", "Rate Limiter", "Cache Invalidation"],
                description="Designing modular, fault-tolerant architectures with concrete database schemas and API contracts.",
            ),
            ExamRound(
                round_number=4,
                name="Hiring Manager & Values",
                format="Behavioral & Engineering Mindset",
                duration="45 Minutes",
                focus_areas=["Uber Values (Go Get It, Trip by Trip, See the Forest)", "Handling Failure", "Collaboration"],
                description="Assessing high ownership, technical curiosity, and speed of delivery under pressure.",
            ),
        ],
        "hiring_tips": [
            "Uber loves candidates who understand concurrency, WebSockets, and geospatial data structures (H3, S2, Geohash).",
            "Write modular code with unit tests during live interviews without being asked.",
        ],
    },
    "goldman_sachs": {
        "company_name": "Goldman Sachs",
        "industry": "Investment Banking, Quantitative Finance & FinTech",
        "tier": "Investment Banking / FinTech",
        "headquarters": "New York, NY, USA",
        "overview": "Premier global financial institution engineering high-frequency trading platforms, risk analytics, and enterprise fintech.",
        "eligibility_criteria": {
            "fresher": {
                "degree": "B.Tech/B.E, M.Tech, Dual Degree, MCA in CS/IT/EE/Maths",
                "cgpa_min": "7.0+ CGPA or 70% aggregate",
                "backlogs": "0 active backlogs allowed",
                "experience": "0 - 1 Years (New Analyst)",
            },
            "experienced": {
                "degree": "Bachelor's / Master's degree in quantitative field",
                "cgpa_min": "Not applicable",
                "experience": "2+ Years (Associate / VP)",
            },
        },
        "coding_expectations": {
            "dsa_difficulty": "LeetCode Medium to Hard + Math/Puzzles",
            "primary_topics": ["Arrays & Two Pointers", "Dynamic Programming", "Tree Traversals", "Math, Probability & Puzzles", "HashMaps"],
            "platforms": "HackerRank",
            "clean_code_rules": "Writing memory-efficient, low-latency algorithms with zero runtime exceptions",
        },
        "project_expectations": {
            "fresher": [
                "Projects with strong data structures, financial modeling, or high-throughput transaction processing",
                "Exceptional command of Core Java (Collections, Concurrency, JVM internals) or C++ (pointers, memory management)",
            ],
            "experienced": [
                "Low-latency trading infrastructure, distributed event streams, financial risk engines",
                "Kafka, Spring Boot, microservices, Linux optimization, and database ACID transaction guarantees",
            ],
        },
        "exam_pattern": [
            ExamRound(
                round_number=1,
                name="Goldman Sachs Aptitude & Coding Assessment",
                format="HackerRank Online Test",
                duration="135 Minutes",
                focus_areas=["Quantitative Aptitude", "Advanced CS Concepts", "2 Algorithmic Coding Questions", "Subjective Math/Puzzles"],
                description="Rigorous screening testing discrete math, statistics, computer science fundamentals, and coding speed.",
            ),
            ExamRound(
                round_number=2,
                name="Technical Round 1 (Data Structures & Math)",
                format="1-on-1 Live Coding",
                duration="45 - 60 Minutes",
                focus_areas=["Recursion & DP", "Trees & Graphs", "Probability Puzzles"],
                description="Live problem solving with rigorous mathematical and algorithmic proof.",
            ),
            ExamRound(
                round_number=3,
                name="Technical Round 2 (Core CS & Concurrency)",
                format="Deep Systems Dive",
                duration="45 - 60 Minutes",
                focus_areas=["Java Multithreading / C++ Memory", "DBMS ACID Properties & Indexing", "OS Paging & Deadlocks"],
                description="Interviewer probes deep into runtime memory models, garbage collection, and database transaction isolation levels.",
            ),
            ExamRound(
                round_number=4,
                name="MD / Partner Interview",
                format="Executive & Cultural Fit",
                duration="30 - 45 Minutes",
                focus_areas=["Integrity & Client Confidentiality", "Commercial Awareness", "Long-Term Career Vision"],
                description="Meeting with a Managing Director to assess composure, communication, and high ethical standards.",
            ),
        ],
        "hiring_tips": [
            "Revise mathematical puzzles (GeeksforGeeks standard puzzles) and probability basics alongside DSA.",
            "Master Java Collections framework and Multithreading (Locks, Synchronized, Executors, volatile) or modern C++.",
        ],
    },
}


def normalize_company_key(name: str) -> str:
    """Normalize user input to match curated dictionary keys."""
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', name.lower().strip())
    if "google" in cleaned or "alphabet" in cleaned:
        return "google"
    if "microsoft" in cleaned or "msft" in cleaned:
        return "microsoft"
    if "amazon" in cleaned or "aws" in cleaned:
        return "amazon"
    if "tcs" in cleaned or "tata" in cleaned:
        return "tcs"
    if "infosys" in cleaned or "infy" in cleaned:
        return "infosys"
    if "wipro" in cleaned:
        return "wipro"
    if "uber" in cleaned:
        return "uber"
    if "goldman" in cleaned or "gs" in cleaned:
        return "goldman_sachs"
    return cleaned


def generate_dynamic_company_profile(
    company_name: str,
    experience_type: str = "fresher",
    years_of_experience: float = 0.0,
    target_role: str = "Software Engineer",
) -> CompanyProfile:
    """
    Intelligent dynamic AI discovery engine for ANY company in the world!
    Infers tier, hiring bar, exam pattern, eligibility, and expectations automatically.
    """
    is_fresher = experience_type.lower() == "fresher" or years_of_experience < 1.5

    # Determine company archetype
    lower_name = company_name.lower()
    if any(k in lower_name for k in ["bank", "capital", "financial", "fintech", "securities", "pay", "credit", "crypto"]):
        industry = "Banking, Financial Services & FinTech"
        tier = "Investment Banking / FinTech"
        dsa_focus = ["Arrays", "Dynamic Programming", "HashMaps", "ACID Transactions", "Low-Latency Queues"]
        dsa_diff = "LeetCode Medium"
        project_points = [
            "Financial transactions, payment gateway integration, or high-throughput order matching engines",
            "Secure REST APIs with JWT/OAuth, distributed caching, and zero data-loss transactional integrity",
        ]
    elif any(k in lower_name for k in ["consult", "services", "tech", "infotech", "solutions", "global", "systems"]):
        industry = "IT Services & Enterprise Consulting"
        tier = "Global IT Services"
        dsa_focus = ["Arrays & Strings", "Basic Sorting & Searching", "Matrix Operations", "Recursion"]
        dsa_diff = "Easy to Medium"
        project_points = [
            "Full-stack web application with complete CRUD operations and database integration",
            "Demonstrated knowledge of SDLC, Agile methodology, automated unit testing, and Git version control",
        ]
    else:
        # Default: Product / SaaS Tech Firm
        industry = "Technology, Cloud & Software Products"
        tier = "Product & High-Growth Technology"
        dsa_focus = ["Trees & Graphs", "Dynamic Programming", "System Design", "REST APIs", "Concurrency"]
        dsa_diff = "LeetCode Medium to Hard"
        project_points = [
            "Production-grade full-stack or backend SaaS application deployed on Cloud (AWS/GCP/Azure)",
            "Microservices architecture, caching layers (Redis), containerization with Docker, and clean GitHub repo",
        ]

    role_title = f"{target_role}" if not is_fresher else f"Junior {target_role} (Campus / New Grad)"

    # Synthesize Exam Pattern
    exam_pattern = [
        ExamRound(
            round_number=1,
            name="Online Assessment (OA)",
            format="Automated Coding & Aptitude Test (HackerRank/Codility)",
            duration="75 - 90 Minutes",
            focus_areas=["DSA Coding Questions", "Problem Solving Speed", "Core Computer Science Fundamentals"],
            description=f"Initial technical screening testing algorithmic fluency in {', '.join(dsa_focus[:3])}.",
        ),
        ExamRound(
            round_number=2,
            name="Technical Round 1 (Data Structures & Algorithms)",
            format="1-on-1 Live Coding Video Interview",
            duration="45 - 60 Minutes",
            focus_areas=["Live Problem Solving", "Time & Space Complexity", "Code Optimization"],
            description="Interactive coding session where interviewers evaluate how you communicate your thought process.",
        ),
        ExamRound(
            round_number=3,
            name="Technical Round 2 (" + ("Projects & Core CS" if is_fresher else "System Design & Architecture") + ")",
            format="Deep Architecture & Code Review",
            duration="45 - 60 Minutes",
            focus_areas=["Low-Level / High-Level Design", "Database Schemas", "Past Project Defensibility"],
            description="Deep dive into your resume projects, component interactions, trade-offs, and scalability choices.",
        ),
        ExamRound(
            round_number=4,
            name="Managerial & Cultural Fit",
            format="Discussion with Hiring Manager",
            duration="30 - 45 Minutes",
            focus_areas=["Workplace Values", "Ownership & Teamwork", "Adaptability & Communication"],
            description="Assessing how you handle ambiguous situations, resolve conflicts, and drive continuous improvement.",
        ),
    ]

    eligibility = {
        "degree": "B.Tech/B.E, M.Tech, MCA, or relevant STEM degree in Computer Science / IT / Electrical Engineering",
        "cgpa_min": "60% or 6.5 CGPA minimum across academic history" if is_fresher else "Not strictly evaluated; evaluated on hands-on industry track record",
        "backlogs": "0 active backlogs allowed at the time of joining" if is_fresher else "N/A",
        "experience": "0 - 1 Years (New Grad / Entry Level)" if is_fresher else f"{int(years_of_experience)}+ Years professional industry experience",
    }

    coding_expectations = {
        "dsa_difficulty": dsa_diff,
        "primary_topics": dsa_focus,
        "platforms": "HackerRank / CodeSignal / LeetCode",
        "clean_code_rules": "Clean code structure, zero edge-case bugs, Big-O explanation, modular OOP design",
    }

    hiring_tips = [
        f"Master the core DSA topics: {', '.join(dsa_focus[:4])} with clean implementation.",
        "Be ready to defend every bullet point on your resume: interviewers test the 'Why' behind every technical choice.",
        "Use the STAR method (Situation, Task, Action, Result) for all situational and behavioral interview questions.",
    ]

    # Synthesized Target Job Description
    target_jd = f"""
Position: {role_title} at {company_name}
Industry: {industry}
Experience Requirement: {eligibility['experience']}

Overview:
We are seeking a talented {role_title} to join {company_name}. In this role, you will design, develop, test, and maintain robust, high-performance software applications.

Responsibilities:
• Architect, implement, and maintain scalable software features using modern programming languages (Python, Java, C++, or JavaScript/TypeScript).
• Write clean, modular, maintainable, and well-tested code following best engineering practices.
• Design efficient database schemas, optimize queries, and integrate RESTful/gRPC APIs.
• Participate in design and code reviews, collaborating closely with cross-functional product, design, and engineering teams.
• Solve challenging computational and algorithmic problems with attention to performance, scalability, and security.

Requirements:
• Education: {eligibility['degree']}.
• Experience: {eligibility['experience']}.
• Strong foundation in Data Structures and Algorithms ({', '.join(dsa_focus)}).
• Hands-on proficiency in one or more core languages: Python, Java, C++, TypeScript, Go, or C#.
• Working knowledge of databases (PostgreSQL, MySQL, MongoDB, or Redis) and cloud fundamentals (AWS, GCP, or Azure).
• Excellent problem-solving, analytical, and collaborative communication skills.
    """.strip()

    return CompanyProfile(
        company_name=company_name,
        industry=industry,
        tier=tier,
        headquarters="Global / Multiple Locations",
        overview=f"Leading organization operating in {industry}, known for high standards of engineering excellence and digital innovation.",
        target_role=role_title,
        experience_level_assumed="Fresher / Entry Level" if is_fresher else f"Experienced ({years_of_experience} yrs)",
        exam_pattern=exam_pattern,
        eligibility_criteria=eligibility,
        coding_expectations=coding_expectations,
        project_expectations=project_points,
        hiring_tips=hiring_tips,
        target_job_description=target_jd,
    )


def get_company_intelligence(
    company_name: str,
    experience_type: str = "fresher",
    years_of_experience: float = 0.0,
    target_role: str = "Software Engineer",
) -> CompanyProfile:
    """
    Look up company in curated database or dynamically discover ANY company worldwide.
    Adapts details based on whether candidate is Fresher or Experienced.
    """
    key = normalize_company_key(company_name)
    is_fresher = experience_type.lower() == "fresher" or years_of_experience < 1.5

    # Check if Groq API is available for live real-time global intelligence
    try:
        from app.services.groq_service import is_groq_available, fetch_company_intelligence_groq
        if is_groq_available():
            groq_info = fetch_company_intelligence_groq(
                company_name=company_name,
                experience_type=experience_type,
                years_of_experience=years_of_experience,
                target_role=target_role,
            )
            if groq_info and isinstance(groq_info, dict):
                # Map Groq result into CompanyProfile
                exam_rounds = []
                for i, r in enumerate(groq_info.get("interview_rounds", [])):
                    exam_rounds.append(
                        ExamRound(
                            round_number=r.get("round_number", i + 1),
                            name=r.get("round_name", f"Round {i + 1}"),
                            format=r.get("round_type", "Technical Evaluation"),
                            duration=f"{r.get('duration_minutes', 60)} Minutes",
                            focus_areas=r.get("focus_areas", ["Problem Solving", "Core CS"]),
                            description=f"Evaluation Criteria: {r.get('evaluation_criteria', 'Evaluated on technical excellence.')}. Questions: {', '.join(r.get('typical_questions', [])[:2])}",
                        )
                    )
                
                project_pts = []
                for p in groq_info.get("expected_coding_projects", []):
                    techs = ", ".join(p.get("suggested_tech_stack", []))
                    project_pts.append(f"{p.get('title', 'Project')}: ({p.get('complexity', 'Advanced')}) using [{techs}]. {p.get('why_it_impresses', '')}")

                # Build dynamic JD from Groq info
                el = groq_info.get("eligibility_criteria", {})
                target_jd = f"""
Company: {groq_info.get('company_name', company_name)}
Role: {target_role}
Industry: {groq_info.get('industry', 'Technology')}
Hiring Bar: {groq_info.get('hiring_bar', 'High')} | Difficulty: {groq_info.get('difficulty_level', 'Hard')}

Eligibility:
• Degrees: {', '.join(el.get('degrees_accepted', ['B.Tech/BE/MCA']))}
• Minimum Marks: {el.get('minimum_cgpa_or_percentage', '60% or 6.5 CGPA')}
• Experience: {el.get('experience_required', 'Fresher' if is_fresher else f'{years_of_experience} yrs')}
• Backlogs: {el.get('backlog_policy', 'No active backlogs')}

Key Prerequisites:
{chr(10).join(['• ' + req for req in el.get('key_prerequisites', [])])}
""".strip()

                return CompanyProfile(
                    company_name=groq_info.get("company_name", company_name),
                    industry=groq_info.get("industry", "Technology"),
                    tier=groq_info.get("hiring_bar", "Tier-1 / High Growth"),
                    headquarters=groq_info.get("headquarters", "Global"),
                    overview=f"Hiring Bar: {groq_info.get('hiring_bar', 'High')}. Exam Platform: {groq_info.get('exam_pattern', {}).get('platform', 'Online Coding Platform')}",
                    target_role=target_role,
                    experience_level_assumed="Fresher / Entry Level" if is_fresher else f"Experienced ({years_of_experience} yrs)",
                    exam_pattern=exam_rounds if exam_rounds else [
                        ExamRound(
                            round_number=1,
                            name="Online Assessment / Coding Screen",
                            format=groq_info.get("exam_pattern", {}).get("platform", "Coding Platform"),
                            duration=groq_info.get("exam_pattern", {}).get("total_duration", "90 Minutes"),
                            focus_areas=["DSA", "Problem Solving"],
                            description="Algorithmic problem solving and domain technical screening.",
                        )
                    ],
                    eligibility_criteria=el,
                    coding_expectations={
                        "dsa_difficulty": groq_info.get("difficulty_level", "Medium-Hard"),
                        "primary_topics": ["Data Structures", "Algorithms", "System Architecture"],
                        "platforms": groq_info.get("exam_pattern", {}).get("platform", "Online Assessment"),
                        "clean_code_rules": "Time & space complexity optimization, modular code, edge case testing",
                    },
                    project_expectations=project_pts if project_pts else ["Production-grade full-stack / backend projects"],
                    hiring_tips=groq_info.get("insider_tips", []),
                    target_job_description=target_jd,
                )
    except Exception:
        pass

    if key in CURATED_COMPANIES:
        data = CURATED_COMPANIES[key]
        exp_key = "fresher" if is_fresher else "experienced"

        eligibility = data["eligibility_criteria"].get(exp_key, data["eligibility_criteria"]["fresher"])
        project_points = data["project_expectations"].get(exp_key, data["project_expectations"]["fresher"])

        role_title = f"{target_role}" if not is_fresher else f"Junior {target_role} (Campus / New Grad)"

        # Generate custom JD for this curated company
        target_jd = f"""
Company: {data['company_name']}
Role: {role_title}
Industry: {data['industry']}
Target Level: {'Fresher / Entry Level (0-1 Years)' if is_fresher else f'Experienced Professional ({int(years_of_experience)}+ Years)'}

About the Role:
{data['company_name']} is hiring a {role_title}. You will design, build, and deploy world-class systems with high availability and reliability.

Key Responsibilities:
• Build resilient, scalable software components and services.
• Solve complex algorithmic challenges and design optimal data structures.
• Collaborate with global engineering teams to deliver high-impact product features.
• Champion clean code, automated testing, and continuous delivery.

Eligibility & Requirements:
• Degree: {eligibility.get('degree', 'B.Tech/B.E/MCA/MS')}
• Experience: {eligibility.get('experience', '0-1 Years')}
• Core Skills: Data Structures, Algorithms ({', '.join(data['coding_expectations']['primary_topics'][:4])}), Clean Code.
• Hands-on experience with modern tech stack, databases, and version control.
        """.strip()

        return CompanyProfile(
            company_name=data["company_name"],
            industry=data["industry"],
            tier=data["tier"],
            headquarters=data["headquarters"],
            overview=data["overview"],
            target_role=role_title,
            experience_level_assumed="Fresher / Entry Level" if is_fresher else f"Experienced ({years_of_experience} yrs)",
            exam_pattern=data["exam_pattern"],
            eligibility_criteria=eligibility,
            coding_expectations=data["coding_expectations"],
            project_expectations=project_points,
            hiring_tips=data["hiring_tips"],
            target_job_description=target_jd,
        )

    # Dynamic Universal Discovery for any other company
    return generate_dynamic_company_profile(
        company_name=company_name,
        experience_type=experience_type,
        years_of_experience=years_of_experience,
        target_role=target_role,
    )


def build_company_roadmap(
    resume_text: str,
    company_profile: CompanyProfile,
    experience_type: str,
    years_of_experience: float,
    matched_skills: List[str],
    missing_skills: List[str],
    ats_data: Dict[str, Any],
) -> CompanyRoadmap:
    """
    Build a custom, step-by-step company acceptance roadmap and gap analysis.
    Tells the candidate exactly what is missing in their resume to qualify for this company.
    """
    is_fresher = experience_type.lower() == "fresher" or years_of_experience < 1.5
    resume_lower = resume_text.lower()

    gaps: List[str] = []
    must_haves: List[str] = []
    eligibility_notes: List[str] = []

    # 1. Eligibility Checks
    eligibility_notes.append(f"Target Role: {company_profile.target_role}")
    eligibility_notes.append(f"Degree Requirement: {company_profile.eligibility_criteria.get('degree', 'B.Tech/MCA/Graduation')}")
    if is_fresher:
        cgpa_info = company_profile.eligibility_criteria.get('cgpa_min', '60% / 6.5 CGPA')
        eligibility_notes.append(f"Minimum Marks / CGPA: {cgpa_info}")
        eligibility_notes.append("Backlog Criterion: " + str(company_profile.eligibility_criteria.get('backlogs', '0 active backlogs')))
    else:
        eligibility_notes.append(f"Experience Level: Requires {int(years_of_experience)}+ Years of verified relevant experience")

    # 2. Check for LeetCode / Coding Platform Handles (Huge for tech companies)
    has_coding_profile = any(cp in resume_lower for cp in ["leetcode", "codeforces", "hackerrank", "codechef", "kaggle", "geeksforgeeks"])
    if is_fresher and not has_coding_profile and company_profile.tier in ["Tier-1 Tech / FAANG", "Product & High-Growth"]:
        gaps.append(
            f"{company_profile.company_name} highly values competitive programming and problem solving. "
            "Your resume lacks links to coding platforms like LeetCode, Codeforces, or HackerRank."
        )
        must_haves.append("Add your LeetCode / Codeforces profile link with contest rating and problem count (e.g., 'Solved 450+ LeetCode problems, Contest Rating 1820').")

    # 3. Check for GitHub / Open Source Link
    has_github = "github.com" in resume_lower or "gitlab.com" in resume_lower
    if not has_github:
        gaps.append("Missing live GitHub / Portfolio URL. Technical recruiters verify project code quality before scheduling interview rounds.")
        must_haves.append("Include active GitHub repository links for your top 2 projects with clean README documentation.")

    # 4. Check for Core Projects Expected by this Company
    expected_projects = company_profile.project_expectations
    if expected_projects:
        gaps.append(f"Company Expectation: {company_profile.company_name} expects {expected_projects[0]}")
        must_haves.append(f"Highlight a project directly featuring: {expected_projects[0]}")

    # 5. Core CS Fundamentals for Freshers
    if is_fresher:
        cs_terms = ["data structures", "algorithms", "dbms", "database", "operating systems", "computer networks", "oop", "object oriented"]
        found_cs = [term for term in cs_terms if term in resume_lower]
        if len(found_cs) < 3:
            gaps.append("Core CS Coursework (OOPs, DBMS, Operating Systems, Computer Networks) is not clearly emphasized.")
            must_haves.append("Add a 'Relevant Coursework' section listing: Data Structures & Algorithms, DBMS, Operating Systems, OOPs, Computer Networks.")

    # 6. Scalability / System Design for Experienced
    if not is_fresher:
        arch_terms = ["distributed", "system design", "microservices", "scalability", "kafka", "caching", "redis", "throughput", "latency"]
        found_arch = [term for term in arch_terms if term in resume_lower]
        if len(found_arch) < 2:
            gaps.append(f"For an experienced hire, {company_profile.company_name} expects proven system design, microservices, and high-concurrency scaling experience.")
            must_haves.append("Include bullet points quantifying throughput (e.g. 'Handled 5,000 requests/sec', 'Designed Kafka event queue reducing processing lag by 40%').")

    # 7. Step-by-Step Round-by-Round Preparation Roadmap
    roadmap_steps: List[Dict[str, str]] = []
    for rnd in company_profile.exam_pattern:
        roadmap_steps.append({
            "round": f"Round {rnd.round_number}: {rnd.name}",
            "strategy": f"Focus on {', '.join(rnd.focus_areas)}. {rnd.description}",
            "duration": rnd.duration,
            "format": rnd.format,
        })

    # Status Determination
    status = "Eligible"
    if len(gaps) >= 3:
        status = "Action Required"
    elif len(gaps) >= 1:
        status = "Conditionally Eligible"

    return CompanyRoadmap(
        company_name=company_profile.company_name,
        eligibility_status=status,
        eligibility_details=eligibility_notes,
        resume_gaps_for_company=gaps,
        preparation_roadmap=roadmap_steps,
        must_have_additions=must_haves,
    )
