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
    
    @staticmethod
    def get_ranked_feed(limit=20, offset=0):
        """Get projects ranked by FairRank with project details for API feed"""
        query = """
        SELECT 
            p.project_id,
            p.title,
            p.abstract,
            p.creator_id,
            p.stage,
            p.created_at,
            p.impressions,
            f.final_score,
            f.engagement_score,
            f.freshness_boost,
            f.underexposed_boost
        FROM projects p
        JOIN fair_rank_scores f ON p.project_id = f.project_id
        ORDER BY f.final_score DESC
        """
        
        try:
            rows = BaseRepository.fetch_all(query)
        except Exception as e:
            print(f"Error fetching ranked feed: {e}")
            return []
        
        # Convert to format expected by API
        results = []
        for row in rows:
            try:
                results.append({
                    "project": {
                        "id": row[0],
                        "title": row[1],
                        "abstract": row[2],
                        "creator_id": row[3],
                        "stage": row[4],
                        "created_at": row[5],
                        "impressions": row[6]
                    },
                    "fairrank": {
                        "score": row[7],
                        "engagement_score": row[8],
                        "freshness_score": row[9],
                        "underexposed_boost": row[10]
                    }
                })
            except Exception as e:
                print(f"Error processing row: {e}, row: {row}")
                continue
        
        return results
    
    @staticmethod
    def count_ranked_projects():
        """Count total projects with FairRank scores"""
        try:
            result = BaseRepository.fetch_one("SELECT COUNT(*) FROM fair_rank_scores")
            return result[0] if result else 0
        except:
            return 0