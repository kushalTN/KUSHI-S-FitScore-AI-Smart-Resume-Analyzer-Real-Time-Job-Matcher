from scripts.skill_extraction import extract_skills
from scripts.matching_algorithm import calculate_tfidf_similarity, calculate_bert_similarity
import random

# Example suggestion mappings (expand for real-world use)
COURSE_SUGGESTIONS = {
    "Python": ["Complete 'Python for Everybody' by Coursera", "Python Certification on Udemy"],
    "Machine Learning": ["ML Specialization by Andrew Ng", "ML Bootcamp on edX"],
    "Communication": ["Effective Communication Skills Course", "Public Speaking Workshop"]
}

CERTIFICATION_SUGGESTIONS = {
    "AWS": ["AWS Certified Cloud Practitioner"],
    "Project Management": ["PMP Certification"],
    "Data Science": ["Data Science Professional Certificate by IBM"]
}

def analyze_resume(resume_text, jd_text, tech_skills, soft_skills, bert_model):
    combined_skills = tech_skills + soft_skills

    jd_skills = extract_skills(jd_text, combined_skills)
    resume_skills = extract_skills(resume_text, combined_skills)

    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    tfidf_score = calculate_tfidf_similarity(resume_text, jd_text)
    bert_score = calculate_bert_similarity(resume_text, jd_text, bert_model)

    overall_score = round((tfidf_score * 0.6) + (bert_score * 0.4), 2)  # Weighted score

    suggestions = generate_improvement_suggestions(missing)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "tfidf_score": tfidf_score,
        "bert_score": bert_score,
        "overall_score": overall_score,
        "suggestions": suggestions
    }

def generate_improvement_suggestions(missing_skills):
    suggestions = []
    for skill in missing_skills:
        course = COURSE_SUGGESTIONS.get(skill)
        cert = CERTIFICATION_SUGGESTIONS.get(skill)

        if course:
            suggestions.append(f"Recommended Course: {random.choice(course)}")
        if cert:
            suggestions.append(f"Suggested Certification: {random.choice(cert)}")

    if not suggestions:
        suggestions.append("Consider general upskilling relevant to the role.")

    return suggestions
