from app.repositories.base import BaseRepository


class SimilarityRepository(BaseRepository):

    @staticmethod
    def upsert_similarity(a, b, score):
        BaseRepository.execute(
            """
            INSERT INTO project_similarity (project_a, project_b, similarity, posted_first)
            VALUES (?, ?, ?, 0)
            ON CONFLICT(project_a, project_b) DO UPDATE SET similarity=excluded.similarity
            """,
            (a, b, score)
        )

    @staticmethod
    def get_similar_projects(project_id):
        return BaseRepository.fetch_all(
            "SELECT * FROM project_similarity WHERE project_a = ? OR project_b = ?",
            (project_id, project_id)
        )
from app.repositories.base import BaseRepository


class SimilarityRepository(BaseRepository):

    @staticmethod
    def upsert_similarity(a, b, score):
        query = """
        INSERT INTO project_similarity
        (project_a, project_b, similarity, posted_first)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(project_a, project_b) DO UPDATE SET
            similarity=excluded.similarity
        """
        BaseRepository.execute(query, (a, b, score, min(a, b)))

    @staticmethod
    def get_similar_projects(project_id):
        return BaseRepository.fetch_all(
            """
            SELECT * FROM project_similarity
            WHERE project_a = ? OR project_b = ?
            ORDER BY similarity DESC
            """,
            (project_id, project_id)
        )
