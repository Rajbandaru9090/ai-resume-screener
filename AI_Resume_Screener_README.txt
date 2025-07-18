
# 🤖 AI-Powered Resume Screener (GPT + Streamlit)
https://ai-resume-screener-gkoqrvoaywyqr39qmxqrtt.streamlit.app/
This project is an intelligent resume screening web app powered by OpenAI GPT models. It allows you to upload multiple resumes and a job description, then automatically scores and ranks candidates based on their fit for the job — all in a clean and interactive Streamlit interface.

---

## 🚀 Demo Features

✅ Paste or upload a **job description**  
✅ Upload candidate **resumes (PDF or text)**  
✅ Run **GPT-based resume scoring** using `rank.py`  
✅ Upload the generated **ranked CSV** and explore results  
✅ Filter candidates by **fit score threshold**  
✅ View detailed **GPT summaries** for each match  
✅ Download final **ranked CSV** of all candidates

---

## 📂 Project Structure

project 2/
│
├── resumes/                # Folder containing raw resumes (PDF or .txt)
├── data/                   # Optional for outputs or inputs
├── .env                    # OpenAI API key (secure)
├── job_description.txt     # JD provided by user
├── rank.py                 # Main GPT scoring logic
├── extract.py              # Resume parsing logic (optional)
├── streamlit_app.py        # Streamlit frontend app
├── requirements.txt        # Python dependencies

---

## ⚙️ How It Works

1. **Paste a job description** inside the app.
2. `rank.py` uses GPT-3.5/4 to:
   - Read resumes
   - Compare skills, experience, keywords with JD
   - Score each candidate (0–10)
   - Generate a summary explaining the score
3. Upload the generated `ranked_resumes_gpt.csv` back into the app.
4. View results in table form with filters and download options.

---

## 🧠 GPT Prompting Logic (inside `rank.py`)

Each resume is matched to the JD using structured GPT prompts like:

You're a technical recruiter. Score the following resume out of 10 based on this job description. 
Then explain in 1-2 lines why this candidate fits or doesn't.

Job Description:
...

Resume:
...

Return JSON like: {"score": 8.5, "reason": "Strong Python and AWS experience"}

---

## 🛠 Tech Stack

| Layer       | Tech Used                |
|------------|--------------------------|
| UI         | Streamlit                |
| AI Model   | OpenAI GPT (via API)     |
| Backend    | Python (subprocess, pandas) |
| Data Files | CSV + TXT/PDF Resumes    |
| Auth       | `.env` for API Key       |

---

## 📦 Installation & Running

### 1. Clone the repo:
git clone https://github.com/your-username/ai-resume-screener.git
cd ai-resume-screener

### 2. Install requirements:
pip install -r requirements.txt

### 3. Add your `.env` file with:
OPENAI_API_KEY=sk-...

### 4. Launch the app:
python -m streamlit run streamlit_app.py

---

## 📤 Output Example

After GPT processing, your `ranked_resumes_gpt.csv` will look like:

| name        | fit_score | gpt_summary                           |
|-------------|-----------|----------------------------------------|
| Alice Singh | 8.5       | Strong experience in Python & SQL      |
| Bob Patel   | 5.0       | Lacks ML skills but has cloud exposure |

---

## 💡 Use Cases

- Fast internal resume screening
- Shortlisting candidates for internships/jobs
- Educational tool for job matching automation
- HR tech demo for startups

---

## ✅ To Do (Optional Enhancements)

- 🧠 Add LLM fine-tuning or embedding
- 📥 Resume PDF parsing with OCR/NLP
- 🛢️ Store results in PostgreSQL
- 📊 Add visual charts for skill match
- 🧪 Unit testing on parsing + scoring

---

## 📬 Contact

Feel free to reach out if you'd like to collaborate or learn more!

> Built by [Your Name]  
> 🏫 Florida Atlantic University | 📍 USA  
> ✉️ your.email@example.com | 🌐 linkedin.com/in/yourname
