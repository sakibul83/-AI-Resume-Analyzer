import spacy

# Load spaCy model once
nlp = spacy.load("en_core_web_sm")


def preprocess_text(text: str) -> str:
    """
    Clean and preprocess text:
    - lowercase
    - remove stopwords
    - remove punctuation
    - lemmatize tokens
    Returns a space-separated string of tokens.
    """
    doc = nlp(text.lower())

    tokens = []
    for token in doc:
        if token.is_stop:
            continue
        if token.is_punct or token.is_space:
            continue
        # Basic filter to skip very short tokens (like 'a', 'x')
        if len(token.text.strip()) <= 1:
            continue
        tokens.append(token.lemma_)

    return " ".join(tokens)


if __name__ == "__main__":
    sample = "Machine Learning Engineers develop models and build AI systems."
    print("Original:", sample)
    print("Processed:", preprocess_text(sample))
