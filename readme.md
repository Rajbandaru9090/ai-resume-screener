AI-Powered Resume Screener (GPT + Streamlit)

This project is an intelligent resume screening web app powered by OpenAI GPT models. It allows you to upload multiple resumes and a job description, then automatically scores and ranks candidates based on their fit for the job — all in a clean and interactive Streamlit interface.



Demo Features

 1.Paste or upload a **job description**
 2.Upload candidate **resumes (PDF or text)**
 3.Run **GPT-based resume scoring** using `rank.py`
 4.Upload the generated **ranked CSV** and explore results
 5.Filter candidates by **fit score threshold**
 6.View detailed **GPT summaries** for each match
 7.Download final **ranked CSV** of all candidates


 How It Works

1. **Paste a job description** inside the app.
2. rank.py uses GPT-3.5/4 to:
   - Read resumes
   - Compare skills, experience, keywords with JD
   - Score each candidate (0–10)
   - Generate a summary explaining the score
3. Upload the generated `ranked\_resumes\_gpt.csv` back into the app.
4. View results in table form with filters and download options.


GPT Prompting Logic (inside rank.py)

Each resume is matched to the JD using structured GPT prompts like:

You're a technical recruiter. Score the following resume out of 10 based on this job description.
Then explain in 1-2 lines why this candidate fits or doesn't.

Job Description:

Resume:


Return JSON like: {"score": 8.5, "reason": "Strong Python and AWS experience"}


 Tech Stack

| Layer       | Tech Used                |
|------------|--------------------------|
| UI         | Streamlit                |
| AI Model   | OpenAI GPT (via API)     |
| Backend    | Python (subprocess, pandas) |
| Data Files | CSV + TXT/PDF Resumes    |
| Auth       | .env for API Key       |

---

 Installation & Running

 1. Clone the repo:
git clone https://github.com/your-username/ai-resume-screener.git
cd ai-resume-screener

2. Install requirements:
pip install -r requirements.txt

3. Add your `.env` file with:
OPENAI_API_KEY=sk-...

4. Launch the app:
python -m streamlit run streamlit_app.py



 Output Example

After GPT processing, your `ranked\_resumes\_gpt.csv` will look like:

| name        | fit_score | gpt_summary                           |
|-------------|-----------|----------------------------------------|
| Alice Singh | 8.5       | Strong experience in Python & SQL      |
| Bob Patel   | 5.0       | Lacks ML skills but has cloud exposure |


 Use Cases

- Fast internal resume screening
- Shortlisting candidates for internships/jobs
- Educational tool for job matching automation
- HR tech demo for startups
