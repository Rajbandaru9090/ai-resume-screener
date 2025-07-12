import os
from docx import Document

def extract_text_from_docx(path):
    doc = Document(path)
    full_text = [para.text for para in doc.paragraphs]
    return "\n".join(full_text)

folder = r"C:\Users\Raj bandaru\Desktop\project 2\resumes"

all_texts = {}

for filename in os.listdir(folder):
    if filename.endswith(".docx"):
        path = os.path.join(folder, filename)
        text = extract_text_from_docx(path)
        all_texts[filename] = text

save_folder = r"C:\Users\Raj bandaru\Desktop\project 2\data"
os.makedirs(save_folder, exist_ok=True)
save_path = os.path.join(save_folder, "raw_resume_texts.txt")

with open(save_path, "w", encoding="utf-8") as f:
    for name, txt in all_texts.items():
        f.write(f"\n\n==={name}===\n{txt}\n")

print(f"✅ Saved extracted resumes to: {save_path}")

# Print sample
for name, txt in all_texts.items():
    print(f"\n\n=== {name} ===\n{txt[:500]}")
