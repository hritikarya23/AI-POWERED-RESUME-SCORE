"""Semantic similarity engine powered by Sentence-Transformers with TF-IDF fallback."""

import logging
import re
from typing import List, Optional, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

# Preferred SentenceTransformer model
DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"


class SemanticMatcher:
    """
    Computes semantic similarity embeddings using Sentence-Transformers.
    Falls back gracefully to TF-IDF cosine similarity if neural weights are unavailable.
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
        """Attempt to load SentenceTransformer model; fallback to TF-IDF on error."""
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

    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Encode a list of texts into normalized embedding vectors.
        """
        if not texts:
            return np.zeros((0, 384), dtype=np.float32)

        if self.is_neural and self.model is not None:
            embeddings = self.model.encode(
                texts,
                batch_size=32,
                show_progress_bar=False,
                normalize_embeddings=True,
            )
            return np.array(embeddings, dtype=np.float32)
        else:
            # TF-IDF Fallback
            vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)
            try:
                tfidf_matrix = vectorizer.fit_transform(texts)
                return tfidf_matrix.toarray()
            except ValueError:
                # In case of empty or all-stopword texts
                return np.zeros((len(texts), 1), dtype=np.float32)

    def compute_similarity(self, text_a: str, text_b: str) -> float:
        """
        Compute semantic cosine similarity between two texts.
        Returns a float in range [0.0, 1.0].
        """
        if not text_a.strip() or not text_b.strip():
            return 0.0

        if self.is_neural and self.model is not None:
            embeddings = self.encode([text_a, text_b])
            vec_a = embeddings[0].reshape(1, -1)
            vec_b = embeddings[1].reshape(1, -1)
            sim = float(cosine_similarity(vec_a, vec_b)[0][0])
            # Bound within [0.0, 1.0]
            return max(0.0, min(1.0, sim))
        else:
            # TF-IDF Fallback
            vectorizer = TfidfVectorizer(stop_words="english")
            try:
                tfidf_matrix = vectorizer.fit_transform([text_a, text_b])
                sim = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
                return max(0.0, min(1.0, sim))
            except ValueError:
                return 0.0

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

        # Filter out trivial/empty sentences
        clean_requirements = [r.strip() for r in requirements if len(r.strip()) > 10]
        clean_resume = [s.strip() for s in resume_sentences if len(s.strip()) > 10]

        if not clean_requirements:
            return []
        if not clean_resume:
            return [(req, "No relevant experience found in resume", 0.0) for req in clean_requirements]

        if self.is_neural and self.model is not None:
            req_embeddings = self.encode(clean_requirements)
            res_embeddings = self.encode(clean_resume)

            # Compute pairwise cosine similarity matrix: (num_reqs, num_resume_sentences)
            sim_matrix = cosine_similarity(req_embeddings, res_embeddings)

            results = []
            for i, req in enumerate(clean_requirements):
                best_idx = int(np.argmax(sim_matrix[i]))
                best_score = float(sim_matrix[i, best_idx])
                best_text = clean_resume[best_idx]
                results.append((req, best_text, max(0.0, min(1.0, best_score))))
            return results
        else:
            # Fallback per-requirement TF-IDF
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

    # First split on line breaks that look like bullets or distinct items
    lines = text.split("\n")
    candidates = []

    bullet_prefix = re.compile(r'^[\s\t]*[\u2022\u2023\u25E6\u2043\u2219\*\-\+\d+\.\)]\s*')

    for line in lines:
        cleaned_line = bullet_prefix.sub("", line).strip()
        if len(cleaned_line) > 15:
            # If the line contains multiple sentences, split them
            sentence_splits = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])', cleaned_line)
            for s in sentence_splits:
                s_clean = s.strip()
                if len(s_clean) > 15:
                    candidates.append(s_clean)

    # Deduplicate while preserving order
    seen = set()
    unique_candidates = []
    for item in candidates:
        if item.lower() not in seen:
            seen.add(item.lower())
            unique_candidates.append(item)

    return unique_candidates
