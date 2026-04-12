import streamlit as st
import pdfplumber
import PyPDF2
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

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

def semantic_score(resume_text, jd_text):
    emb1 = model.encode(resume_text, convert_to_tensor=True)
    emb2 = model.encode(jd_text, convert_to_tensor=True)

    score = util.cos_sim(emb1, emb2).item()

    if score < 0:
        score = 0

    return int(score * 100)

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

        skill_score = score_resume(resume_skills, jd_skills)
        ai_score = semantic_score(resume_text, jd_text)

        score = int((skill_score * 0.6) + (ai_score * 0.4))

        missing = list(set(jd_skills) - set(resume_skills))
        results.append({
            "name": file.name,
            "score": score,
            "skill_score": skill_score,
            "ai_score": ai_score,
            "skills": resume_skills,
            "missing": missing
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    st.subheader("🏆 Candidate Ranking")

    for i, candidate in enumerate(results, start=1):
        st.markdown(f"### {i}. {candidate['name']}")
        st.progress(candidate["score"] / 100)
        st.write(f"Final Score: {candidate['score']}%")
        st.write(f"Skill Match: {candidate['skill_score']}% | AI Semantic: {candidate['ai_score']}%")
        st.write("Missing Skills:", candidate["missing"])
        st.divider()