from datetime import datetime
from app.repositories.base import BaseRepository


class PlatformStatsRepository(BaseRepository):

    @staticmethod
    def update_stats(total_creators, total_projects, underexposed_count, avg_fairrank, exposure_gini):
        BaseRepository.execute(
            """
            INSERT INTO platform_stats (id, total_creators, total_projects, underexposed_count, avg_fairrank, exposure_gini, updated_at)
            VALUES (1, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                total_creators=excluded.total_creators,
                total_projects=excluded.total_projects,
                underexposed_count=excluded.underexposed_count,
                avg_fairrank=excluded.avg_fairrank,
                exposure_gini=excluded.exposure_gini,
                updated_at=excluded.updated_at
            """,
            (total_creators, total_projects, underexposed_count, avg_fairrank, exposure_gini, datetime.utcnow().isoformat())
        )
    
    @staticmethod
    def count_projects():
        """Count total projects"""
        result = BaseRepository.fetch_one("SELECT COUNT(*) FROM projects")
        return result[0] if result else 0
    
    @staticmethod
    def count_creators():
        """Count total creators"""
        result = BaseRepository.fetch_one("SELECT COUNT(*) FROM creator_profiles")
        return result[0] if result else 0
    
    @staticmethod
    def count_engagements():
        """Count total engagements"""
        result = BaseRepository.fetch_one("SELECT COUNT(*) FROM engagements")
        return result[0] if result else 0
    
    @staticmethod
    def count_underexposed_projects(threshold=100):
        """Count projects with impressions below threshold"""
        result = BaseRepository.fetch_one(
            "SELECT COUNT(*) FROM projects WHERE impressions < ?",
            (threshold,)
        )
        return result[0] if result else 0
    
    @staticmethod
    def get_avg_fairrank():
        """Get average FairRank score - handles empty table"""
        result = BaseRepository.fetch_one("SELECT AVG(final_score) FROM fair_rank_scores")
        # Handle NULL when table is empty
        if result and result[0] is not None:
            return float(result[0])
        return 0.0
    
    @staticmethod
    def get_exposure_distribution():
        """Get histogram of impression counts"""
        query = """
        SELECT 
            CASE 
                WHEN impressions BETWEEN 0 AND 50 THEN '0-50'
                WHEN impressions BETWEEN 51 AND 100 THEN '51-100'
                WHEN impressions BETWEEN 101 AND 200 THEN '101-200'
                WHEN impressions BETWEEN 201 AND 500 THEN '201-500'
                ELSE '500+'
            END as bucket,
            COUNT(*) as count
        FROM projects
        GROUP BY bucket
        """
        rows = BaseRepository.fetch_all(query)
        
        # Return empty dict if no projects
        if not rows:
            return {}
        
        distribution = {}
        for row in rows:
            distribution[row[0]] = row[1]
        
        return distribution