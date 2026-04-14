<img width="1789" height="915" alt="Screenshot 2026-04-12 091650" src="https://github.com/user-attachments/assets/0f999cd3-c08f-4587-9d2e-2847203f16ca" />
<img width="1901" height="914" alt="image" src="https://github.com/user-attachments/assets/880321a5-2d91-404d-8c19-3f417ff47c49" />
<img width="1757" height="816" alt="image" src="https://github.com/user-attachments/assets/9420ba81-5ed9-4780-93be-098dcb560275" />

# AI Resume Screener

An intelligent resume screening web application that evaluates resumes against job descriptions using Natural Language Processing (NLP) and machine learning techniques. This tool helps recruiters, HR teams, and job seekers quickly assess resume-job fit through automated scoring and insights.

## Live Demo
Add your deployed link here:  
`https://resume-screener-quoz3ph5kzfz3zrzmpy5ya.streamlit.app/`

## Features

- Upload Resume (PDF / DOCX)
- Paste Job Description
- Resume vs JD Match Score
- Keyword Extraction
- Missing Skills Detection
- ATS-style Resume Evaluation
- Clean Interactive Dashboard
- Fast Web-based Interface

## Tech Stack

- Python
- Streamlit
- Scikit-learn
- Pandas
- NumPy
- NLP

- TF-IDF Vectorization
- Cosine Similarity

## How It Works

1. User uploads a resume.
2. User enters job description.
3. Text is cleaned and processed.
4. NLP converts text into vectors.
5. Similarity score is calculated.
6. Missing keywords and insights are shown.


## Installation

```bash
pip install -r requirements.txt
streamlit run app.py
