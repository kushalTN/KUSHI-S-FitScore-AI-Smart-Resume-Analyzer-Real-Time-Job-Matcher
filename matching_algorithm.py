import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer

# Load BERT Model
def load_bert_model(model_path='models/bert_model'):
    return SentenceTransformer(model_path)

# TF-IDF Similarity
def calculate_tfidf_similarity(resume_text, jd_text):
    corpus = [resume_text, jd_text]
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(corpus)

    # Explicit dense conversion to avoid Pylance complaints
    dense_vectors = np.array(vectors.todense())

    similarity = np.dot(dense_vectors[0], dense_vectors[1]) / (
        np.linalg.norm(dense_vectors[0]) * np.linalg.norm(dense_vectors[1]) + 1e-10
    )
    return round(similarity * 100, 2)

# Cosine Similarity for BERT
def calculate_bert_similarity(resume_text, jd_text, model):
    embeddings = model.encode([resume_text, jd_text])
    sim = cosine_similarity(embeddings[0], embeddings[1])
    return round(sim * 100, 2)

def cosine_similarity(vec1, vec2):
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / norm1 / norm2
