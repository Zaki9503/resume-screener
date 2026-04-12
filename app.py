import streamlit as st
from parser import extract_text_from_pdf
from scorer import extract_skills, score_resume, semantic_score, apply_dynamic_rules
from skills_db import skills_db

st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")

def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    load_css()

    st.title("📄 AI Resume Screener Dashboard")
    st.caption("AI-powered ATS ranking and candidate shortlisting")
    resume_files = st.file_uploader(
        "Upload Multiple Resumes (PDF)",
        type=["pdf"],
        accept_multiple_files=True
    )
    jd = st.text_area("Paste Job Description", height=220)

    if resume_files and jd:

        jd_text = jd.lower()
        jd_skills = extract_skills(jd_text, skills_db)

        results = []

        for file in resume_files:
            resume_text = extract_text_from_pdf(file)
            #st.write(file.name)
            #st.write(resume_text[:2000])
            resume_skills = extract_skills(resume_text, skills_db)

            skill_score = score_resume(resume_skills, jd_skills)
            ai_score = semantic_score(resume_text, jd_text)

            raw = (skill_score * 0.7) + (ai_score * 0.3)
            score = min(100, int(raw * 1.08))
            score = apply_dynamic_rules(score, resume_skills, jd_skills)
            missing = sorted(list(set(jd_skills) - set(resume_skills)))
            results.append({
                "name": file.name,
                "score": score,
                "skill_score": skill_score,
                "ai_score": ai_score,
                "skills": resume_skills,
                "missing": missing
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)

        top_score = results[0]["score"]
        total_candidates = len(results)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f'<div class="metric-card"><h3>{total_candidates}</h3><p>Total Candidates</p></div>', unsafe_allow_html=True)

        with c2:
            st.markdown(f'<div class="metric-card"><h3>{top_score}%</h3><p>Top Score</p></div>', unsafe_allow_html=True)

        with c3:
            strong = len([r for r in results if r["score"] >= 60])
            st.markdown(f'<div class="metric-card"><h3>{strong}</h3><p>Strong Matches</p></div>', unsafe_allow_html=True)
        
        st.subheader("🏆 Candidate Ranking")

        for i, candidate in enumerate(results, start=1):

            if candidate["score"] >= 70:
                status = "Strong Match"
                color = "green"
            elif candidate["score"] >= 45:
                status = "Moderate"
                color = "orange"
            else:
                status = "Weak"
                color = "red"

            st.markdown(f"""
            <div class="rank-card">
            <h4>#{i} - {candidate["name"]}</h4>
            <p><b>Final Score:</b> {candidate["score"]}%</p>
            <p><b>Status:</b> <span class="{color}">{status}</span></p>
            <p><b>Skill Match:</b> {candidate["skill_score"]}% | <b>AI Score:</b> {candidate["ai_score"]}%</p>
            </div>
            """, unsafe_allow_html=True)

            st.progress(candidate["score"] / 100)

            with st.expander(f"View Skill Details - {candidate['name']}"):
                st.markdown("### Detected Skills")
                if candidate["skills"]:
                    st.markdown(" • " + "\n • ".join(candidate["skills"]))
                else:
                    st.write("None")

                st.markdown("### Missing Skills")
                if candidate["missing"]:
                    st.markdown(" • " + "\n • ".join(candidate["missing"]))
                else:
                    st.write("None")

if __name__ == "__main__":
    main()