from sentence_transformers import SentenceTransformer, util
import streamlit as st

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

def extract_skills(text, skills_db):
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
    return max(0, int(score * 100))

def apply_dynamic_rules(score, resume_skills, jd_skills):
    critical = jd_skills[:3]
    bonus = jd_skills[3:]

    for skill in critical:
        if skill not in resume_skills:
            score -= 10

    for skill in bonus:
        if skill in resume_skills:
            score += 2

    return max(0, min(100, int(score)))