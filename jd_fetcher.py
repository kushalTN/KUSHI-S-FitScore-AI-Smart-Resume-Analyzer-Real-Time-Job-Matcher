def get_job_description(role):
    """Returns a sample JD if available, else indicates missing."""
    jd_library = {
        "Data Scientist": """
We are seeking a Data Scientist with expertise in machine learning, data analysis, and statistical modeling. Responsibilities include building predictive models, data visualization, and deriving actionable insights. Preferred skills: Python, SQL, scikit-learn, TensorFlow, data wrangling, and strong communication skills.
""",
        "AI Engineer": """
Join our AI team to develop intelligent systems using machine learning and deep learning. You will work on NLP, computer vision, and large language models. Preferred skills: Python, PyTorch, TensorFlow, BERT, GPT, NLP fundamentals, and deployment experience.
""",
        "Business Analyst": """
We are looking for a Business Analyst to gather requirements, analyze data, and support decision-making. Responsibilities include stakeholder communication, process improvement, and data-driven insights. Preferred skills: Excel, SQL, data visualization tools, analytical thinking, and business acumen.
""",
        "Graphic Designer": """
Seeking a creative Graphic Designer with experience in branding, marketing materials, and digital content creation. Responsibilities include graphic design, layout creation, and collaboration with marketing teams. Preferred skills: Adobe Suite, creativity, communication skills, attention to detail.
""",
        "Accountant": """
We are hiring an Accountant to manage financial records, prepare reports, and ensure compliance with tax regulations. Responsibilities include bookkeeping, budgeting, and financial analysis. Preferred skills: Accounting software (Tally, QuickBooks), Excel, financial reporting, attention to detail, and knowledge of GAAP.
""",
        "Teacher": """
We are seeking a passionate Teacher to deliver engaging lessons and support student development. Responsibilities include lesson planning, classroom management, and student assessment. Preferred skills: Subject expertise, communication skills, empathy, instructional design, and adaptability.
"""
    }
    
    # Use .title() to handle case-insensitive matches
    return jd_library.get(role.title(), "Sample JD not available for this role.")
