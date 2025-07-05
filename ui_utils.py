import streamlit as st

# Progress Bar for Overall Matching Percentage
def display_matching_progress(overall_score):
    st.write(f"### 🎯 Overall Matching Score: {overall_score:.2f}%")
    
    progress_color = "green" if overall_score >= 75 else "orange" if overall_score >= 50 else "red"

    st.progress(overall_score / 100, text="Matching Percentage")

    st.info(f"High Score (>75%): Excellent fit! Medium (50-75%): Consider improving. Low (<50%): Significant skill gaps.")

# Section Divider with Title
def section_title(title, icon="📝"):
    st.markdown(f"---\n## {icon} {title}")

# Theme Toggle for Dark Mode
def apply_theme_toggle():
    with st.sidebar:
        st.write("⚙️ **Theme Settings**")
        dark_mode = st.toggle("🌙 Dark Mode", value=False)

    if dark_mode:
        st.markdown("""
            <style>
                body { background-color: #0e1117; color: white; }
                .stApp { background-color: #0e1117; }
            </style>
        """, unsafe_allow_html=True)

# Informative Notes about Matching Logic
def show_matching_notes():
    with st.expander("ℹ️ How Matching Works"):
        st.write("""
        - **TF-IDF Score:** Measures keyword similarity between Resume & Job Description.
        - **BERT Semantic Similarity:** Measures contextual and sentence-level relevance.
        - **Overall Score:** Weighted combination of both, helps judge your fit for the role.
        - **Skill Gap Analysis:** Detects missing technical & soft skills from the job description.
        """)
