import os
import csv
import sys
from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------
# ✅ Load API Key
# ---------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("API key not loaded. Check your .env file!")
    exit()

client = OpenAI(api_key=api_key)
print(" API Key loaded:", api_key[:10], "********")

# ---------------------------
# 📥 Input JD from CLI
# ---------------------------
if len(sys.argv) < 2:
    print(" Please provide the job description file path (e.g., 'job_description.txt')")
    exit()

jd_path = sys.argv[1]
try:
    with open(jd_path, "r", encoding="utf-8") as f:
        job_description = f.read()
except Exception as e:
    print(f" Error reading job description: {e}")
    exit()

# ---------------------------
# 📄 Resume Input/Output
# ---------------------------
input_path = r"C:\Users\Raj bandaru\Desktop\project 2\data\raw_resume_texts.txt"
output_path = r"C:\Users\Raj bandaru\Desktop\project 2\data\ranked_resumes_gpt.csv"

# ---------------------------
#  GPT Scoring Function
# ---------------------------
def gpt_score_resume(resume_text):
    prompt = f"""
You are a recruiter evaluating resumes for the following job position.

Job Description:
\"\"\"
{job_description}
\"\"\"

Evaluate the resume below and:
- Score it from 1 to 10
- Justify in 1–2 lines why the candidate is or isn’t a good fit

Resume:
\"\"\"
{resume_text}
\"\"\"

Output format:
Score: <number>
Reason: <short text>
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content

# ---------------------------
# 🔄 Load & Score Resumes
# ---------------------------
try:
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read().split("=== ")
except FileNotFoundError:
    print(" Resume input file not found!")
    exit()

print(f" Total resume sections found: {len(content)}")

results = []

for section in content:
    if not section.strip():
        continue
    parts = section.strip().split(" ===\n", 1)
    if len(parts) != 2:
        continue
    name, resume_text = parts
    print(f" Scoring {name.strip()}...")

    try:
        gpt_result = gpt_score_resume(resume_text)
        print(" GPT Response:\n", gpt_result)

        score_line = [line for line in gpt_result.splitlines() if line.lower().startswith("score")][0]
        reason_line = [line for line in gpt_result.splitlines() if line.lower().startswith("reason")][0]
        score = int(score_line.split(":")[1].strip())
        reason = reason_line.split(":", 1)[1].strip()

        results.append((name.strip(), score, reason))
        print(f" {name.strip()} scored: {score} - {reason}")

    except Exception as e:
        print(f" Error scoring {name.strip()}: {e}")

# ---------------------------
# 💾 Save CSV Output
# ---------------------------
try:
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Score", "Reason"])
        writer.writerows(results)
    print(f" GPT-ranked resumes saved to: {output_path}")
except Exception as e:
    print(" Error saving CSV:", e)
