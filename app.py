import streamlit as st
import pdfplumber
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

skills_db = [
    "python","java","c++","sql","machine learning","deep learning",
    "data analysis","html","css","javascript","react","nodejs",
    "aws","docker","git","excel","power bi","pandas","numpy"
]

def extract_text_from_pdf(file):
    text = ""

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + " "
    except:
        pass

    if len(text.strip()) < 20:
        try:
            file.seek(0)
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text += t + " "
        except:
            pass

    return text.lower()

def extract_skills(text):
    return [skill for skill in skills_db if skill in text]

def score_resume(resume_skills, jd_skills):
    if not jd_skills:
        return 0

    matched = len(set(resume_skills) & set(jd_skills))
    total = len(set(jd_skills))

    return int((matched / total) * 100)

st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")

st.title("📄 AI Resume Screener")
st.caption("Analyze resume fitment against a job description")

resume_files = st.file_uploader(
    "Upload Multiple Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)
jd = st.text_area("Paste Job Description", height=220)

if resume_files and jd:

    jd_text = jd.lower()
    jd_skills = extract_skills(jd_text)

    results = []

    for file in resume_files:
        resume_text = extract_text_from_pdf(file)
        resume_skills = extract_skills(resume_text)

        score = score_resume(resume_skills, jd_skills)
        missing = list(set(jd_skills) - set(resume_skills))

        results.append({
            "name": file.name,
            "score": score,
            "skills": resume_skills,
            "missing": missing
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    st.subheader("🏆 Candidate Ranking")

    for i, candidate in enumerate(results, start=1):
        st.markdown(f"### {i}. {candidate['name']}")
        st.progress(candidate["score"] / 100)
        st.write(f"Score: {candidate['score']}%")
        st.write("Detected Skills:", candidate["skills"])
        st.write("Missing Skills:", candidate["missing"])
        st.divider()