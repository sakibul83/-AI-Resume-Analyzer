import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from app.pdf_reader import extract_text_from_pdf
from app.scoring import compute_scores

def get_text_from_job_input(option: str, jd_file, jd_text: str) -> str:
    """
    Helper function to get job description text from either:
    - uploaded PDF
    - pasted text
    """
    if option == "Upload PDF":
        if jd_file is None:
            st.warning("Please upload a Job Description PDF.")
            return ""
        # Use the uploaded file directly (Streamlit's UploadedFile)
        return extract_text_from_pdf(jd_file)

    # "Paste Text"
    if not jd_text.strip():
        st.warning("Please paste the Job Description text.")
        return ""
    return jd_text


def main():
    st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

    st.title("🧠 AI Resume Analyzer / CV Matcher")
    st.write(
        "Upload your resume and a job description. "
        "This tool will analyze how well your resume matches the job."
    )

    st.markdown("---")

    # --- Layout: left (inputs), right (results)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. Upload your Resume (PDF)")

        cv_file = st.file_uploader("Resume PDF", type=["pdf"])

        st.subheader("2. Provide Job Description")

        job_desc_option = st.radio(
            "How would you like to provide the Job Description?",
            ("Upload PDF", "Paste Text"),
        )

        jd_file = None
        jd_text = ""

        if job_desc_option == "Upload PDF":
            jd_file = st.file_uploader("Job Description PDF", type=["pdf"])
        else:
            jd_text = st.text_area("Paste Job Description text here", height=200)

        analyze_button = st.button("🔍 Analyze Resume", type="primary")

    with col2:
        st.subheader("Results")

        if analyze_button:
            if cv_file is None:
                st.error("Please upload your Resume PDF first.")
                return

            # Extract resume text from PDF
            try:
                resume_text = extract_text_from_pdf(cv_file)
            except Exception as e:
                st.error(f"Error reading Resume PDF: {e}")
                return

            # Get job text based on option
            job_text = get_text_from_job_input(job_desc_option, jd_file, jd_text)
            if not job_text:
                return

            # Compute scores
            try:
                scores = compute_scores(resume_text, job_text)
            except Exception as e:
                st.error(f"Error computing scores: {e}")
                return

            final_score = scores["final_score"]
            keyword_score = scores["keyword_score"]
            similarity_score = scores["similarity_score"]

            st.metric("Overall Match Score", f"{final_score} / 100")

            st.write("### Score Breakdown")
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**Keyword Match Score:** {keyword_score} / 100")
                st.progress(keyword_score / 100.0)
            with col_b:
                st.write(f"**Semantic Similarity Score:** {similarity_score} / 100")
                st.progress(similarity_score / 100.0)

            st.markdown("---")

            st.write("### Matched Keywords")
            if scores["matched_keywords"]:
                st.write(", ".join(scores["matched_keywords"]))
            else:
                st.write("_No significant keyword matches found._")

            st.write("### Missing Important Keywords")
            if scores["missing_keywords"]:
                st.write(", ".join(scores["missing_keywords"]))
            else:
                st.write("_You covered most of the important keywords!_")

            st.markdown("---")

            with st.expander("Show processed texts (for debugging / curiosity)"):
                st.write("#### Processed Resume Text")
                st.text(scores["processed_resume"])
                st.write("#### Processed Job Description Text")
                st.text(scores["processed_job"])

    st.markdown("---")
    st.caption("Built with ❤️ using Python, spaCy, scikit-learn, pdfplumber, and Streamlit.")


if __name__ == "__main__":
    main()
