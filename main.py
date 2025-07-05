import streamlit as st
import os
import sys
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.text_extraction import extract_text_from_file
from scripts.skill_extraction import load_skill_library, skill_gap_analysis
from scripts.matching_algorithm import calculate_tfidf_similarity, calculate_bert_similarity, load_bert_model
from scripts.report_generator import generate_csv_report, generate_pdf_report
from scripts.jd_fetcher import get_job_description
from scripts.ui_utils import display_matching_progress, section_title, apply_theme_toggle, show_matching_notes

# ---------------- Setup ----------------
os.makedirs("data/sample_resumes", exist_ok=True)
os.makedirs("data/job_descriptions", exist_ok=True)
st.set_page_config(page_title="KUSHI'S FitScore AI", page_icon="💼", layout="centered")
apply_theme_toggle()

# Branding
if os.path.exists("data/logo.png"):
    logo = Image.open("data/logo.png")
    st.image(logo, width=90)
st.title("🎯 KUSHI'S FitScore AI — Smart Resume Analyzer & Job Matcher")

# Load Skills & BERT
tech_skills, soft_skills = load_skill_library()
bert_model = load_bert_model()

st.markdown("---")

# ---------------- Resume Upload ----------------
section_title("Upload Resumes", "📂")
uploaded_files = st.file_uploader("Upload up to 50 Resumes (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"], accept_multiple_files=True)
if uploaded_files:
    st.success(f"{len(uploaded_files)} Resume(s) Uploaded Successfully!")

st.markdown("---")

# ---------------- Job Description ----------------
section_title("Job Description", "📝")
job_title = st.text_input("Job Title (Optional)")
job_description_text = st.text_area("Paste Job Description", height=200)
jd_file = st.file_uploader("Or Upload JD File (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])

jd_path = None  # ✅ Initialize jd_path to avoid unbound variable

if jd_file:
    jd_path = os.path.join("data/job_descriptions", jd_file.name)
    with open(jd_path, "wb") as f:
        f.write(jd_file.read())
    st.success(f"Job Description saved as {jd_file.name}")    
else:
        st.warning("Please paste text or upload a valid Job Description file.")

st.markdown("---")


# Real-Time JD Fetch
with st.expander("🌐 Fetch JD (API Based)"):
    role = st.text_input("Role for JD Fetch (e.g., Data Scientist)")
    location = st.text_input("Location (Optional)")
    if st.button("Fetch JD"):
        jd_fetched = get_job_description(role)
        if jd_fetched:
            st.success("JD Fetched Successfully.")
            job_description_text = jd_fetched
            st.text_area("Fetched JD", jd_fetched, height=200)
        else:
            st.warning("JD fetch failed. Enter manually.")

st.markdown("---")

# ---------------- Resume Analysis ----------------
section_title("Resume Analysis & Suggestions", "🔍")
show_matching_notes()

if uploaded_files and (job_description_text or jd_file):
    
    if jd_file and jd_path:
        jd_text = extract_text_from_file(jd_path)
    else:
        jd_text = job_description_text

    for file in uploaded_files:
        st.divider()
        st.subheader(f"📄 {file.name}")
        
        resume_path = os.path.join("data/sample_resumes", file.name)
        with open(resume_path, "wb") as f:
            f.write(file.read())
        resume_text = extract_text_from_file(resume_path)


        if st.button(f"🔧 Generate Missing Skills - {file.name}"):
            matched, missing = skill_gap_analysis(resume_text, jd_text, tech_skills, soft_skills)
            tfidf_score = calculate_tfidf_similarity(resume_text, jd_text)
            bert_score = calculate_bert_similarity(resume_text, jd_text, bert_model)
            overall_score = round((tfidf_score + bert_score) / 2, 2)

            st.success(f"TF-IDF: {tfidf_score}% | BERT: {bert_score}% | Overall Match: {overall_score}%")
            display_matching_progress(overall_score)

            st.write("✅ Matched Skills:", matched if matched else "None Found")
            st.write("⚠️ Missing Skills:", missing if missing else "No Missing Skills")

            with st.expander("💡 Suggestions for Improvement"):
                st.write("Consider adding missing skills via courses, certifications, or project work to strengthen your resume.")

            csv_path = f"data/{file.name}_report.csv"
            pdf_path = f"data/{file.name}_report.pdf"
            generate_csv_report(file.name, matched, missing, tfidf_score, bert_score, csv_path)
            generate_pdf_report(file.name, matched, missing, tfidf_score, bert_score, pdf_path)

            with open(csv_path, "rb") as f:
                st.download_button("📥 Download CSV Report", f, file_name=os.path.basename(csv_path))
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download PDF Report", f, file_name=os.path.basename(pdf_path))

st.markdown("---")

# ---------------- Personal Resume Analyzer ----------------
section_title("Personal Resume Analyzer", "🧑‍💼")
personal_resume = st.file_uploader("Upload Your Resume", type=["pdf", "docx", "txt"], key="personal")
personal_jd = st.text_area("Paste Job Description for Your Role", height=200, key="personal_jd")

if st.button("Analyze My Resume"):
    if personal_resume and personal_jd:
        path = os.path.join("data/sample_resumes", personal_resume.name)
        with open(path, "wb") as f:
            f.write(personal_resume.read())
        resume_text = extract_text_from_file(path)

        matched, missing = skill_gap_analysis(resume_text, personal_jd, tech_skills, soft_skills)
        tfidf_score = calculate_tfidf_similarity(resume_text, personal_jd)
        bert_score = calculate_bert_similarity(resume_text, personal_jd, bert_model)
        overall_score = round((tfidf_score + bert_score) / 2, 2)

        st.success(f"TF-IDF: {tfidf_score}% | BERT: {bert_score}% | Overall: {overall_score}%")
        display_matching_progress(overall_score)
        st.write("Matched Skills:", matched if matched else "None")
        st.write("Missing Skills:", missing if missing else "None")

st.markdown("---")

# ---------------- Notes ----------------
with st.expander("ℹ️ Notes on Matching Process"):
    st.write("""
    - **TF-IDF**: Measures text similarity based on keyword frequency.
    - **BERT**: Uses deep semantic understanding for advanced matching.
    - **Skill Gap**: Identifies missing skills by comparing resume with job requirements.
    - Works for **all domains** including IT, Non-IT, Arts, Business, Medical, and more.
    """)

