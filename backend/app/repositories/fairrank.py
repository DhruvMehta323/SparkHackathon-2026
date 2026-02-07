from datetime import datetime
from app.repositories.base import BaseRepository


class FairRankRepository(BaseRepository):

    @staticmethod
    def upsert_score(project_id, engagement, freshness, diversity, underexposed, final):
        query = """
        INSERT INTO fair_rank_scores
        (project_id, engagement_score, freshness_boost, diversity_boost, underexposed_boost, final_score, computed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(project_id) DO UPDATE SET
            engagement_score=excluded.engagement_score,
            freshness_boost=excluded.freshness_boost,
            diversity_boost=excluded.diversity_boost,
            underexposed_boost=excluded.underexposed_boost,
            final_score=excluded.final_score,
            computed_at=excluded.computed_at
        """
        BaseRepository.execute(
            query,
            (project_id, engagement, freshness, diversity, underexposed, final, datetime.utcnow().isoformat())
        )

    @staticmethod
    def get_ranked_projects():
        return BaseRepository.fetch_all(
            "SELECT * FROM fair_rank_scores ORDER BY final_score DESC"
        )
