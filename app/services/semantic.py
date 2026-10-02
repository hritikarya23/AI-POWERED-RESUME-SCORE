"""Semantic similarity engine powered by Sentence-Transformers with pure Python & TF-IDF fallbacks."""

import logging
import math
import os
import re
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)

# Preferred SentenceTransformer model
DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"

# Safe optional imports for serverless environments
try:
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except Exception:
    np = None
    TfidfVectorizer = None
    cosine_similarity = None
    HAS_SKLEARN = False


def _pure_python_similarity(text_a: str, text_b: str) -> float:
    """Zero-dependency pure Python cosine similarity using token frequency vectors."""
    from collections import Counter

    tokens_a = re.findall(r"\b[a-zA-Z0-9_+#.-]{2,}\b", text_a.lower())
    tokens_b = re.findall(r"\b[a-zA-Z0-9_+#.-]{2,}\b", text_b.lower())

    if not tokens_a or not tokens_b:
        return 0.0

    counts_a = Counter(tokens_a)
    counts_b = Counter(tokens_b)

    common = set(counts_a.keys()) & set(counts_b.keys())
    if not common:
        return 0.0

    dot_product = sum(counts_a[t] * counts_b[t] for t in common)
    norm_a = math.sqrt(sum(v * v for v in counts_a.values()))
    norm_b = math.sqrt(sum(v * v for v in counts_b.values()))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    return max(0.0, min(1.0, dot_product / (norm_a * norm_b)))


class SemanticMatcher:
    """
    Computes semantic similarity embeddings using Sentence-Transformers.
    Falls back gracefully to TF-IDF or pure Python cosine similarity if neural weights are unavailable.
    """
    _instance: Optional["SemanticMatcher"] = None

    def __init__(self, model_name: str = DEFAULT_MODEL_NAME):
        self.model_name = model_name
        self.model = None
        self.is_neural = False
        self._initialize_model()

    @classmethod
    def get_instance(cls) -> "SemanticMatcher":
        """Get or initialize singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _initialize_model(self) -> None:
        """Attempt to load SentenceTransformer model; fallback gracefully on error or serverless."""
        if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
            logger.info("Serverless environment detected (Vercel). Using fast in-memory similarity engine.")
            self.model = None
            self.is_neural = False
            return

        try:
            from sentence_transformers import SentenceTransformer
            logger.info("Loading SentenceTransformer model '%s'...", self.model_name)
            self.model = SentenceTransformer(self.model_name)
            self.is_neural = True
            logger.info("SentenceTransformer model loaded successfully.")
        except Exception as e:
            logger.warning(
                "Could not load SentenceTransformer ('%s'). Falling back to TF-IDF vectorizer: %s",
                self.model_name,
                e,
            )
            self.model = None
            self.is_neural = False

    def encode(self, texts: List[str]):
        """Encode a list of texts into normalized embedding vectors."""
        if not texts:
            return []

        if self.is_neural and self.model is not None:
            embeddings = self.model.encode(
                texts,
                batch_size=32,
                show_progress_bar=False,
                normalize_embeddings=True,
            )
            return np.array(embeddings, dtype=np.float32) if np is not None else embeddings
        elif HAS_SKLEARN and TfidfVectorizer is not None:
            vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)
            try:
                tfidf_matrix = vectorizer.fit_transform(texts)
                return tfidf_matrix.toarray()
            except ValueError:
                return []
        return []

    def compute_similarity(self, text_a: str, text_b: str) -> float:
        """
        Compute semantic cosine similarity between two texts.
        Returns a float in range [0.0, 1.0].
        """
        if not text_a.strip() or not text_b.strip():
            return 0.0

        if self.is_neural and self.model is not None and HAS_SKLEARN:
            embeddings = self.encode([text_a, text_b])
            vec_a = embeddings[0].reshape(1, -1)
            vec_b = embeddings[1].reshape(1, -1)
            sim = float(cosine_similarity(vec_a, vec_b)[0][0])
            return max(0.0, min(1.0, sim))

        if HAS_SKLEARN and TfidfVectorizer is not None and cosine_similarity is not None:
            try:
                vectorizer = TfidfVectorizer(stop_words="english")
                tfidf_matrix = vectorizer.fit_transform([text_a, text_b])
                sim = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
                return max(0.0, min(1.0, sim))
            except Exception:
                pass

        return _pure_python_similarity(text_a, text_b)

    def match_requirements_to_resume(
        self,
        requirements: List[str],
        resume_sentences: List[str],
    ) -> List[Tuple[str, str, float]]:
        """
        Match each requirement against all resume sentences/bullets to find the closest match.
        Returns list of tuples: (requirement, best_matching_sentence, similarity_score).
        """
        if not requirements:
            return []

        if not resume_sentences:
            return [(req, "", 0.0) for req in requirements]

        clean_requirements = [r.strip() for r in requirements if len(r.strip()) > 10]
        clean_resume = [s.strip() for s in resume_sentences if len(s.strip()) > 10]

        if not clean_requirements:
            return []
        if not clean_resume:
            return [(req, "No relevant experience found in resume", 0.0) for req in clean_requirements]

        if self.is_neural and self.model is not None and HAS_SKLEARN and np is not None:
            req_embeddings = self.encode(clean_requirements)
            res_embeddings = self.encode(clean_resume)
            sim_matrix = cosine_similarity(req_embeddings, res_embeddings)

            results = []
            for i, req in enumerate(clean_requirements):
                best_idx = int(np.argmax(sim_matrix[i]))
                best_score = float(sim_matrix[i, best_idx])
                best_text = clean_resume[best_idx]
                results.append((req, best_text, max(0.0, min(1.0, best_score))))
            return results
        else:
            results = []
            for req in clean_requirements:
                best_score = 0.0
                best_text = "No relevant experience found in resume"
                for sentence in clean_resume:
                    score = self.compute_similarity(req, sentence)
                    if score > best_score:
                        best_score = score
                        best_text = sentence
                results.append((req, best_text, best_score))
            return results


def split_into_meaningful_sentences(text: str) -> List[str]:
    """
    Split text into meaningful bullet points, sentences, or requirements.
    Preserves bullet structure and filters noise.
    """
    if not text:
        return []

    lines = text.split("\n")
    candidates = []
    bullet_prefix = re.compile(r'^[\s\t]*[\u2022\u2023\u25E6\u2043\u2219\*\-\+\d+\.\)]\s*')

    for line in lines:
        cleaned_line = bullet_prefix.sub("", line).strip()
        if len(cleaned_line) > 15:
            sentence_splits = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])', cleaned_line)
            for s in sentence_splits:
                s_clean = s.strip()
                if len(s_clean) > 15:
                    candidates.append(s_clean)

    seen = set()
    unique_candidates = []
    for item in candidates:
        if item.lower() not in seen:
            seen.add(item.lower())
            unique_candidates.append(item)

    return unique_candidates
