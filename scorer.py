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

    matched_weight = 0
    total_weight = 0

    for skill in jd_skills:
        weight = skill_weights.get(skill, 5)
        total_weight += weight

        if skill in resume_skills:
            matched_weight += weight

    return int((matched_weight / total_weight) * 100)


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

skill_weights = {
    # High Priority
    "python": 10,
    "java": 10,
    "sql": 10,
    "react": 9,
    "nodejs": 9,
    "aws": 9,
    "docker": 9,
    "machine learning": 10,
    "photoshop": 9,
    "illustrator": 9,
    "inventory management": 9,

    # Medium Priority
    "html": 6,
    "css": 6,
    "javascript": 7,
    "git": 7,
    "excel": 6,
    "figma": 7,
    "warehouse": 7,
    "logistics": 7,

    # Lower Priority
    "communication": 3,
    "teamwork": 3,
    "problem solving": 4,
    "adaptability": 2,
    "computer knowledge": 2
}