import json
import random
import math
import hashlib
from app.core.logger import get_logger
from app.repositories.projects import ProjectRepository
from app.repositories.embeddings import EmbeddingRepository
from app.repositories.similarity import SimilarityRepository

logger = get_logger(__name__)


class SimilarityEngine:
    VECTOR_DIM = 8

    @staticmethod
    def generate_dummy_embeddings(dim: int = None):
        dim = dim or SimilarityEngine.VECTOR_DIM
        logger.info("Generating dummy embeddings dim=%d", dim)
        projects = ProjectRepository.get_all_projects()

        for p in projects:
            text = "{} {}".format(p.get("title") or "", p.get("abstract") or "")
            vector = SimilarityEngine.text_to_embedding(text, dim)
            EmbeddingRepository.upsert_embedding(p["project_id"], vector)

    @staticmethod
    def text_to_embedding(text: str, dim: int):
        vec = [0.0] * dim
        if not text:
            return vec
        tokens = [t.strip().lower() for t in text.split() if t.strip()]
        for t in tokens:
            h = hashlib.md5(t.encode("utf-8")).hexdigest()
            for k in range(0, len(h), 4):
                chunk = h[k : k + 4]
                try:
                    val = int(chunk, 16)
                except Exception:
                    val = 0
                idx = val % dim
                vec[idx] += (val % 100) / 100.0
        norm = math.sqrt(sum(x * x for x in vec))
        if norm == 0:
            return vec
        return [x / norm for x in vec]

    @staticmethod
    def cosine_similarity(v1, v2):
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    @staticmethod
    def compute_all_similarities():
        logger.info("Computing all pairwise similarities")
        try:
            embeddings = EmbeddingRepository.get_all_embeddings()
            parsed = {e["project_id"]: e["embedding"] for e in embeddings}
            project_ids = list(parsed.keys())
            for i in range(len(project_ids)):
                for j in range(i + 1, len(project_ids)):
                    p1 = project_ids[i]
                    p2 = project_ids[j]
                    sim = SimilarityEngine.cosine_similarity(parsed[p1], parsed[p2])
                    SimilarityRepository.upsert_similarity(p1, p2, float(sim))
            logger.info("Similarity computation complete: pairs=%d", max(0, len(project_ids) * (len(project_ids) - 1) // 2))
        except Exception:
            logger.exception("compute_all_similarities failed")
            raise
import json
import random
import math
import hashlib
from app.core.logger import get_logger
from app.repositories.projects import ProjectRepository
from app.repositories.embeddings import EmbeddingRepository
from app.repositories.similarity import SimilarityRepository

logger = get_logger(__name__)


class SimilarityEngine:
    """Generate or compute embeddings and populate project similarity table.

    - `generate_dummy_embeddings` creates pseudo-random vectors for each
      project and persists them via `EmbeddingRepository.upsert_embedding`.
    - `compute_all_similarities` loads embeddings and writes pairwise
      similarities into `project_similarity` using `SimilarityRepository`.
    """

    VECTOR_DIM = 8

    @staticmethod
    def generate_dummy_embeddings(dim: int = None):
        dim = dim or SimilarityEngine.VECTOR_DIM
        logger.info("Generating dummy embeddings dim=%d", dim)
        projects = ProjectRepository.get_all_projects()

        for p in projects:
            text = "{} {}".format(p.get("title") or "", p.get("description") or "")
            vector = SimilarityEngine.text_to_embedding(text, dim)
            # EmbeddingRepository handles JSON serialization
            EmbeddingRepository.upsert_embedding(p["project_id"], vector)

    @staticmethod
    def text_to_embedding(text: str, dim: int):
        """Deterministic, simple embedding: hash tokens to dimensions.

        This is not a neural embedding but produces stable vectors for the
        same text and is easy to debug and unit-test.
        """
        vec = [0.0] * dim
        if not text:
            return vec

        tokens = [t.strip().lower() for t in text.split() if t.strip()]
        for t in tokens:
            h = hashlib.md5(t.encode("utf-8")).hexdigest()
            # use chunks of the hex digest to produce several pseudo-random ints
            for k in range(0, len(h), 4):
                chunk = h[k : k + 4]
                try:
                    val = int(chunk, 16)
                except Exception:
                    val = 0
                idx = val % dim
                vec[idx] += (val % 100) / 100.0

        # normalize
        norm = math.sqrt(sum(x * x for x in vec))
        if norm == 0:
            return vec
        return [x / norm for x in vec]

    @staticmethod
    def cosine_similarity(v1, v2):
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot / (norm1 * norm2)

    @staticmethod
    def compute_all_similarities():
        logger.info("Computing all pairwise similarities")
        try:
            embeddings = EmbeddingRepository.get_all_embeddings()

            parsed = {e["project_id"]: e["embedding"] for e in embeddings}
            project_ids = list(parsed.keys())

            for i in range(len(project_ids)):
                for j in range(i + 1, len(project_ids)):
                    p1 = project_ids[i]
                    p2 = project_ids[j]

                    sim = SimilarityEngine.cosine_similarity(parsed[p1], parsed[p2])

                    # store an undirected similarity; repository ensures uniqueness
                    SimilarityRepository.upsert_similarity(p1, p2, float(sim))

            logger.info("Similarity computation complete: pairs=%d",
                        max(0, len(project_ids) * (len(project_ids) - 1) // 2))
        except Exception:
            logger.exception("compute_all_similarities failed")
            raise
