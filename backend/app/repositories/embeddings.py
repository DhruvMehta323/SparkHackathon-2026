import json
from app.repositories.base import BaseRepository


class EmbeddingRepository(BaseRepository):
    @staticmethod
    def upsert_embedding(project_id, embedding):
        BaseRepository.execute(
            """
            INSERT INTO project_embeddings (project_id, embedding)
            VALUES (?, ?)
            ON CONFLICT(project_id) DO UPDATE SET
                embedding=excluded.embedding
            """,
            (project_id, json.dumps(embedding))
        )

    @staticmethod
    def get_all_embeddings():
        rows = BaseRepository.fetch_all("SELECT * FROM project_embeddings")
        for r in rows:
            try:
                r["embedding"] = json.loads(r["embedding"])
            except Exception:
                r["embedding"] = []
        return rows
