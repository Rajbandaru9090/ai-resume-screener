import streamlit as st
import pandas as pd
import openai
import pdfplumber
import docx2txt
import plotly.graph_objects as go
from datetime import datetime
import re
import json
from sklearn.feature_extraction.text import CountVectorizer

# ========== 🔐 LOAD API KEY FROM SECRETS ==========
openai.api_key = st.secrets["openai_api_key"]

# ========== ⚙️ PAGE CONFIG ==========
st.set_page_config(page_title="🧠 AI Resume Screener (Dark Theme)", layout="wide", page_icon="🧬")
st.markdown("""
    <style>
    body, .main, .block-container {
        background-color: #1e1e1e;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #333333;
        color: white;
    }
    .stTextArea textarea {
        background-color: #333333;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 AI Resume Screener (Advanced + Visual AI)")

# ========== 📄 JOB DESCRIPTION ==========
st.subheader("📄 Job Description")
job_description = st.text_area(
    "Paste the job description here:",
    height=200,
    placeholder="Paste responsibilities, qualifications, and required skills..."
)

# ========== 📤 RESUME UPLOAD ==========
st.subheader("📤 Upload Resumes (PDF, DOCX, or TXT)")
uploaded_files = st.file_uploader(
    "Upload resumes:",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

# ========== 📥 TEXT EXTRACTION ==========
def extract_text(file):
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    return ""

resume_data = []
if uploaded_files:
    for file in uploaded_files:
        text = extract_text(file)
        resume_data.append({"filename": file.name, "text": text})

# ========== 🔍 EXTRACT SKILLS ==========
def extract_keywords(text, top_n=10):
    text = re.sub(r"[^a-zA-Z ]", "", text)
    vectorizer = CountVectorizer(stop_words='english', max_features=top_n)
    vecs = vectorizer.fit_transform([text])
    return vectorizer.get_feature_names_out()

# ========== 🤖 GPT SCORING ==========
def score_resume_with_gpt(resume_text, job_desc):
    job_keywords = extract_keywords(job_desc, top_n=15)
    resume_keywords = extract_keywords(resume_text, top_n=30)
    matched = list(set(job_keywords) & set(resume_keywords))
    missing = list(set(job_keywords) - set(resume_keywords))

    prompt = f"""
You are a senior AI hiring assistant. Evaluate the following resume in relation to the provided job description.

Provide the following in detailed JSON:
1. A **score out of 10** based on how many job skills match the resume.
2. A **5-sentence summary** highlighting:
   - Clear skill matches with examples
   - Major mismatches
   - Specific tools or projects mentioned
   - Relevance to job role
   - Overall verdict
3. A list of matched skills
4. A list of missing skills

Respond in this JSON format:
{{
  "score": 7.5,
  "reason": "...5 detailed sentences...",
  "matched_skills": ["python", "sql"],
  "missing_skills": ["aws", "docker"]
}}

### JOB KEYWORDS:
{', '.join(job_keywords)}

### RESUME KEYWORDS:
{', '.join(resume_keywords)}
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        reply = response.choices[0].message.content
        result = json.loads(reply.strip())
        return result["score"], result["reason"], result["matched_skills"], result["missing_skills"]
    except Exception as e:
        return 0, f"Error: {e}", [], []

# ========== 🧠 SCORING ==========
if st.button("🚀 Run Resume Fit Evaluation") and job_description and resume_data:
    results = []
    progress = st.progress(0)
    for i, r in enumerate(resume_data):
        score, reason, matched, missing = score_resume_with_gpt(r["text"], job_description)
        results.append({
            "name": r["filename"],
            "fit_score": round(score, 2),
            "gpt_summary": reason,
            "matched_skills": ", ".join(matched),
            "missing_skills": ", ".join(missing),
            "matched_list": matched,
            "missing_list": missing
        })
        progress.progress((i + 1) / len(resume_data))

    df = pd.DataFrame(results).sort_values(by="fit_score", ascending=False).reset_index(drop=True)

    st.success("✅ Resume analysis complete!")
    st.subheader("📊 Candidate Overview")
    st.dataframe(df[["name", "fit_score", "matched_skills", "missing_skills"]], use_container_width=True)

    st.subheader("🧠 GPT Summary")
    for _, row in df.iterrows():
        with st.expander(f"{row['name']} — Score: {row['fit_score']}"):
            st.markdown(f"**Matched Skills:** {row['matched_skills']}")
            st.markdown(f"**Missing Skills:** {row['missing_skills']}")
            st.info(row["gpt_summary"])

    # ========== 📈 Radar Charts ==========
    st.subheader("📌 Skill Match Radar Visualization")
    for index, row in df.iterrows():
        skills = list(set(row["matched_list"] + row["missing_list"]))
        values = [1 if skill in row["matched_list"] else 0 for skill in skills]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=skills,
            fill='toself',
            name=row['name']
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title=f"Skill Radar for {row['name']}",
            paper_bgcolor='#1e1e1e',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)

    # ========== 📥 DOWNLOAD ==========
    st.download_button(
        label="⬇️ Download Ranked Results",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=f"ranked_resumes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )
else:
    st.warning("Please enter a job description and upload resumes to continue.")
