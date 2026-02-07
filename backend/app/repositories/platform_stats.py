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
