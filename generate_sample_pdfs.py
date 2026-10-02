"""Script to generate realistic sample PDF resumes for testing and demonstrations."""

from pathlib import Path
from fpdf import FPDF


def build_pdf(dest_path: Path, title: str, subtitle: str, contact: str, summary: str, skills_dict: dict, experience: list, education: list):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Header
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(text=title, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(text=subtitle, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(text=contact, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Section Helper
    def add_section_header(name: str):
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(text=name, new_x="LMARGIN", new_y="NEXT")
        y = pdf.get_y()
        pdf.set_draw_color(203, 213, 225)
        pdf.line(10, y, 200, y)
        pdf.ln(2)

    # Summary
    add_section_header("PROFESSIONAL SUMMARY")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(w=190, h=5, text=summary, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Skills
    add_section_header("TECHNICAL SKILLS")
    for cat, items in skills_dict.items():
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(w=45, h=5, text=cat)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(w=145, h=5, text=items, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Experience
    add_section_header("WORK EXPERIENCE")
    for job in experience:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(w=140, h=5, text=job["role_company"])
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(w=50, h=5, text=job["dates"], align="R", new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(51, 65, 85)
        for b in job["bullets"]:
            pdf.multi_cell(w=190, h=4.8, text=f"-  {b}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    # Education
    add_section_header("EDUCATION")
    for edu in education:
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(w=140, h=5, text=edu["degree"])
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(w=50, h=5, text=edu["dates"], align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(text=edu["school"], new_x="LMARGIN", new_y="NEXT")

    pdf.output(str(dest_path))
    print(f"Successfully generated: {dest_path}")


def generate_all_samples():
    out_dir = Path("sample_resumes")
    out_dir.mkdir(exist_ok=True)

    # 1. Backend Engineer
    build_pdf(
        dest_path=out_dir / "alex_rivera_backend_engineer.pdf",
        title="ALEX RIVERA",
        subtitle="Senior Python & Cloud Systems Engineer",
        contact="alex.rivera@example.com  |  (555) 234-5678  |  San Francisco, CA  |  github.com/alexrivera",
        summary=(
            "Senior Software Engineer with 6 years of experience building high-scale distributed backend systems, "
            "REST APIs, and cloud services in Python and Go. Proven track record of architecting microservices that "
            "handle millions of daily transactions with 99.99% uptime, optimizing database latency, and driving TDD best practices."
        ),
        skills_dict={
            "Languages:": "Python, Go, SQL, Bash, TypeScript",
            "Frameworks & Tools:": "FastAPI, Django, Flask, Pytest, Celery",
            "Cloud & DevOps:": "AWS (EC2, S3, RDS, Lambda, EKS), Docker, Kubernetes, Terraform, GitHub Actions, CI/CD",
            "Databases & Storage:": "PostgreSQL, Redis, MySQL, MongoDB, Elasticsearch",
            "Architecture & Practices:": "Microservices, REST API, System Design, Test-Driven Development (TDD), Agile",
        },
        experience=[
            {
                "role_company": "Senior Backend Engineer  |  CloudScale Tech",
                "dates": "2022 - Present",
                "bullets": [
                    "Architected and deployed 8 asynchronous microservices using FastAPI and Docker, handling 15,000 requests per second with sub-40ms latency.",
                    "Optimized PostgreSQL query performance and designed Redis caching layer, decreasing database load by 45% and saving $3,200 monthly in cloud costs.",
                    "Spearheaded migration of legacy monolithic workloads to Kubernetes on AWS EKS, improving deployment frequency from bi-weekly to multiple times daily.",
                    "Established CI/CD automation with GitHub Actions and Pytest, boosting automated test coverage from 62% to 94%.",
                    "Mentored 4 junior engineers on distributed systems architecture, design patterns, and rigorous code review practices.",
                ],
            },
            {
                "role_company": "Backend Software Engineer  |  DataStream Labs",
                "dates": "2019 - 2022",
                "bullets": [
                    "Engineered RESTful APIs in Python and Django serving over 1.2M active monthly users.",
                    "Designed automated ETL data processing pipelines that ingested and normalized 20M+ records daily into PostgreSQL.",
                    "Automated deployment and staging environments using Docker, Terraform, and AWS EC2.",
                ],
            },
        ],
        education=[
            {
                "degree": "Bachelor of Science in Computer Science",
                "school": "University of California, Berkeley",
                "dates": "2015 - 2019",
            }
        ],
    )

    # 2. ML Engineer
    build_pdf(
        dest_path=out_dir / "maya_chen_ml_engineer.pdf",
        title="MAYA CHEN",
        subtitle="Machine Learning Engineer & Data Scientist",
        contact="maya.chen@email.com  |  (555) 789-0123  |  Seattle, WA  |  github.com/mayachen-ai",
        summary=(
            "Data Scientist & Machine Learning Engineer with 4 years of experience building predictive models and statistical "
            "solutions in Python. Proficient in classical ML, deep learning with PyTorch, feature engineering, and cloud deployment."
        ),
        skills_dict={
            "Languages:": "Python, SQL, R, Bash",
            "Machine Learning & AI:": "PyTorch, Scikit-Learn, TensorFlow, Pandas, NumPy, SciPy, HuggingFace",
            "Cloud & Infrastructure:": "Docker, AWS (S3, EC2), Linux, Git, Jupyter",
            "Concepts & Methods:": "Feature Engineering, Classification, Regression, Natural Language Processing, MLOps",
        },
        experience=[
            {
                "role_company": "Machine Learning Engineer  |  Apex Data Corp",
                "dates": "2021 - Present",
                "bullets": [
                    "Developed and deployed classification and regression models in Python and Scikit-Learn, improving customer churn prediction accuracy by 22%.",
                    "Built customer sentiment NLP pipeline using PyTorch and HuggingFace, processing 500,000 reviews monthly.",
                    "Containerized ML inference services with Docker and deployed onto AWS EC2 instances.",
                    "Collaborated with data engineering team to design ETL pipelines in SQL and Pandas.",
                ],
            }
        ],
        education=[
            {
                "degree": "Master of Science in Data Science",
                "school": "University of Washington",
                "dates": "2020",
            },
            {
                "degree": "Bachelor of Science in Statistics",
                "school": "University of Washington",
                "dates": "2018",
            },
        ],
    )


if __name__ == "__main__":
    generate_all_samples()
