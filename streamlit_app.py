import streamlit as st
import pandas as pd
import subprocess
import os

# ---------------------------
# 📌 PAGE CONFIGURATION
# ---------------------------
st.set_page_config(page_title="AI Resume Screener", layout="wide")

st.title("🤖 AI-Powered Resume Screener")

# ---------------------------
# 📄 JOB DESCRIPTION INPUT
# ---------------------------
st.subheader("📄 Job Description")
job_description = st.text_area(
    "Paste the job description here (required to compute fit scores):",
    height=200,
    placeholder="Enter the responsibilities, skills, and qualifications here..."
)

# Save JD to file
jd_path = "job_description.txt"
if job_description.strip():
    with open(jd_path, "w", encoding="utf-8") as f:
        f.write(job_description)
    st.success("✅ Job description received and saved.")
else:
    st.warning("⚠️ Please enter a job description before continuing.")

# ---------------------------
# 🧠 RUN GPT RANKING PIPELINE
# ---------------------------
if job_description.strip():
    if st.button("🔁 Run Resume Ranking (GPT)"):
        with st.spinner("Running GPT-based ranking pipeline..."):
            result = subprocess.run(["python", "rank.py", jd_path], capture_output=True, text=True)

        if result.returncode == 0:
            st.success("✅ Resume ranking completed! Upload the new ranked CSV below.")
            st.code(result.stdout)
        else:
            st.error("❌ GPT scoring failed.")
            st.code(result.stderr)

# ---------------------------
# 📤 UPLOAD RANKED CSV
# ---------------------------
st.markdown("### 📁 Upload ranked_resumes_gpt.csv to view results")
uploaded_file = st.file_uploader("Upload your ranked_resumes_gpt.csv", type=["csv"])

if uploaded_file is not None:
    # ---------------------------
    # 📊 DATA LOADING
    # ---------------------------
    df = pd.read_csv(uploaded_file)

    # Rename columns if needed
    df.rename(columns={
        "Name": "name",
        "Score": "fit_score",
        "Reason": "gpt_summary"
    }, inplace=True)

    # ---------------------------
    # 📈 OVERVIEW STATS
    # ---------------------------
    st.subheader("📊 Overview")
    st.markdown(f"**Total Candidates:** {len(df)}")
    st.markdown(f"**Columns Available:** {', '.join(df.columns)}")

    # ---------------------------
    # 🔍 FILTERING BY SCORE
    # ---------------------------
    df_sorted = df.sort_values(by="fit_score", ascending=False).reset_index(drop=True)

    st.subheader("🔍 Filter Candidates by Fit Score")
    min_score = st.slider("Minimum Fit Score", min_value=0.0, max_value=10.0, value=5.0, step=0.5)
    df_filtered = df_sorted[df_sorted["fit_score"] >= min_score]

    # ---------------------------
    # 📋 DISPLAY TOP MATCHES
    # ---------------------------
    st.subheader("📋 Top Candidates")
    st.dataframe(df_filtered[["name", "fit_score", "gpt_summary"]], use_container_width=True)

    # ---------------------------
    # 🔎 CANDIDATE DETAIL VIEW
    # ---------------------------
    if len(df_filtered) > 0:
        st.subheader("🔎 Candidate Details")

        selected_index = st.selectbox("Select a candidate to view more:", df_filtered.index)
        candidate = df_filtered.loc[selected_index]

        st.markdown(f"**👤 Name:** {candidate['name']}")
        st.markdown(f"**✅ Fit Score:** {round(candidate['fit_score'], 2)}")
        st.markdown("**💬 GPT Summary:**")
        st.info(candidate['gpt_summary'])
    else:
        st.info("No candidates match the current fit score threshold.")

    # ---------------------------
    # 📥 DOWNLOAD CSV
    # ---------------------------
    st.subheader("⬇️ Download Ranked Results")
    csv = df_sorted.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="ranked_resumes_gpt.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Please upload the `ranked_resumes_gpt.csv` file generated after GPT scoring.")
