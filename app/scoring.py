from typing import List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.text_preprocess import preprocess_text


def extract_keywords(job_text: str, top_n: int = 25) -> List[str]:
    """
    Extract simple keyword candidates from the job description.
    For now:
    - preprocess the text
    - sort by frequency
    - return top N unique tokens
    """
    processed = preprocess_text(job_text)
    tokens = processed.split()

    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1

    # Sort by frequency (high → low)
    sorted_tokens = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    keywords = [t[0] for t in sorted_tokens[:top_n]]
    return keywords


def compute_scores(resume_text: str, job_text: str) -> Dict:
    """
    Compute:
    - keyword match score
    - cosine similarity score (TF-IDF)
    - combined final score
    - matched & missing keywords
    """
    # Preprocess texts
    processed_resume = preprocess_text(resume_text)
    processed_job = preprocess_text(job_text)

    # 1) Keyword-based scoring
    job_keywords = extract_keywords(job_text, top_n=25)
    resume_tokens = set(processed_resume.split())

    matched = [kw for kw in job_keywords if kw in resume_tokens]
    missing = [kw for kw in job_keywords if kw not in resume_tokens]

    if len(job_keywords) > 0:
        keyword_score = int(round(len(matched) / len(job_keywords) * 100))
    else:
        keyword_score = 0

    # 2) TF-IDF cosine similarity
    texts = [processed_resume, processed_job]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    similarity_score = int(round(similarity * 100))

    # 3) Final combined score (simple average)
    final_score = int(round((keyword_score + similarity_score) / 2))

    return {
        "final_score": final_score,
        "keyword_score": keyword_score,
        "similarity_score": similarity_score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "processed_resume": processed_resume,
        "processed_job": processed_job,
    }


if __name__ == "__main__":
    sample_resume = """
    I am a Machine Learning Engineer with experience in Python, NLP, and building AI-powered applications.
    I have worked with scikit-learn, TensorFlow, and data preprocessing.
    """

    sample_job = """
    We are looking for a Machine Learning Engineer with strong skills in Python, NLP, scikit-learn,
    and experience building AI applications and data pipelines.
    """

    scores = compute_scores(sample_resume, sample_job)
    print("Scores:", scores)
