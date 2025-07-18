# 🧠 AI Resume Screener with GPT-4 | Skill Match, Visual Analysis, Batch Scoring

[![Streamlit](https://img.shields.io/badge/Live_App-Open-green?logo=streamlit)](https://ai-resume-screener-gkoqrvoaywyqr39qmxqrtt.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**An AI-powered Resume Screener** that uses OpenAI GPT to match multiple resumes to a given job description, analyze skill match, and generate smart visual insights. Built for recruiters and candidates to save hours of manual screening time.

---

## 🎯 What It Does

✅ Upload multiple **PDF / DOCX / TXT resumes**  
✅ Paste any **Job Description (JD)**  
✅ GPT-4 compares **skills, experience, and keywords**  
✅ Outputs:
- 🔢 Smart match **score**
- 🧠 **Explanation** for each score
- 📊 **Skill match heatmap / radar chart**
- 🧾 **Filterable match table** (matched/missing skills)
- 📥 **Download CSV** of all results  
✅ Works on **batch** of resumes (up to 10+ in one go)


## 🛠️ Tech Stack

| Layer     | Tools Used                            |
|-----------|----------------------------------------|
| Backend   | OpenAI GPT-4 API, Python               |
| Frontend  | Streamlit, Plotly, pandas              |
| Parsing   | PyMuPDF, python-docx, os, re           |
| Visuals   | Plotly (Radar/Heatmap), Streamlit UI   |
| Export    | pandas to_csv, DataFrames              |
| Hosting   | Streamlit Cloud / Local Deployment     |


---

## 🧠 GPT Logic

> _“Score each resume from 0–100 based on how well it matches this JD. Output the matched skills, missing skills, and justification for your score.”_

The system parses resumes, extracts text, and prompts **OpenAI GPT-4** to generate:
- A **match score**
- **Matched/missing skills**
- A natural language **explanation**
- Skill insights for visualization

---

## 📊 Visuals

- ✅ **Radar Chart** of skill match
- ✅ **Bar/Heatmap** of match scores
- ✅ **Interactive Table** with filters and highlights
- ✅ Export to **CSV**






