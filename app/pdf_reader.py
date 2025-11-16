import io
from typing import Union

import pdfplumber


def extract_text_from_pdf(file: Union[str, io.BytesIO]) -> str:
    """
    Extract text from a PDF.
    
    Supports:
    - file path as string
    - file-like object (e.g. Streamlit's UploadedFile)
    """
    text_chunks = []

    # If it's a file path
    if isinstance(file, str):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text_chunks.append(page_text)
    else:
        # Assume it's a file-like object
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text_chunks.append(page_text)

    full_text = "\n".join(text_chunks)
    # Clean extra whitespace
    return " ".join(full_text.split())


if __name__ == "__main__":
    # Simple test (make sure data/sample_resume.pdf exists)
    sample_path = "data/sample_resume.pdf"
    try:
        text = extract_text_from_pdf(sample_path)
        print("First 500 characters from PDF:")
        print(text[:500])
    except Exception as e:
        print(f"Error reading PDF: {e}")
