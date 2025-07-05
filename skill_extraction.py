import json
import re

# Load all skills from skill_library.json
def load_skill_library():
    with open("data/skill_library.json", "r", encoding="utf-8") as f:
        skill_data = json.load(f)
    
    tech_skills = skill_data.get("technical_skills", [])
    soft_skills = skill_data.get("soft_skills", [])
    
    return tech_skills, soft_skills


def extract_skills(text, skill_list):
    found = []
    text_lower = text.lower()
    for skill in skill_list:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
            found.append(skill)
    return found

def skill_gap_analysis(resume_text, jd_text, tech_skills, soft_skills):
    combined_skills = tech_skills + soft_skills
    jd_skills = extract_skills(jd_text, combined_skills)
    resume_skills = extract_skills(resume_text, combined_skills)
    
    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))
    
    return matched, missing
