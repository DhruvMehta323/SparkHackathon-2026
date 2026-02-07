from datetime import datetime
from app.repositories.base import BaseRepository
from app.repositories.projects import ProjectRepository
from app.repositories.rewards import RewardRepository


class EngagementRepository(BaseRepository):

    @staticmethod
    def create_engagement(project_id, user_id, reaction, weight=1.0):
        query = """
        INSERT OR IGNORE INTO engagements
        (project_id, user_id, reaction, weight, created_at)
        VALUES (?, ?, ?, ?, ?)
        """
        rowid = BaseRepository.execute(
            query,
            (project_id, user_id, reaction, weight, datetime.utcnow().isoformat())
        )

        # reward creator for engagement if reaction is like/comment
        try:
            if reaction and reaction.lower() in ("like", "comment"):
                proj = ProjectRepository.get_project(project_id)
                if proj:
                    RewardRepository.add_reward(proj.get("creator_id"), "Engagement Bonus", 1)
        except Exception:
            pass

        return rowid

    @staticmethod
    def get_project_engagements(project_id):
        return BaseRepository.fetch_all(
            "SELECT * FROM engagements WHERE project_id = ?",
            (project_id,)
        )
# app/repositories/engagements.py

from datetime import datetime
from app.repositories.base import BaseRepository
from app.repositories.projects import ProjectRepository
from app.repositories.rewards import RewardRepository


class EngagementRepository(BaseRepository):

    @staticmethod
    def create_engagement(project_id, user_id, reaction, weight=1.0):
        query = """
        INSERT OR IGNORE INTO engagements
        (project_id, user_id, reaction, weight, created_at)
        VALUES (?, ?, ?, ?, ?)
        """
        rowid = BaseRepository.execute(
            query,
            (project_id, user_id, reaction, weight, datetime.utcnow().isoformat())
        )

        # reward creator for engagement if reaction is like/comment
        try:
            if reaction and reaction.lower() in ("like", "comment"):
                proj = ProjectRepository.get_project(project_id)
                if proj:
                    RewardRepository.add_reward(proj.get("creator_id"), "Engagement Bonus", 1)
        except Exception:
            # don't fail engagement on reward errors
            pass

        return rowid

    @staticmethod
    def get_project_engagements(project_id):
        return BaseRepository.fetch_all(
            "SELECT * FROM engagements WHERE project_id = ?",
            (project_id,)
        )

    @staticmethod
    def delete_engagement(engagement_id):
        BaseRepository.execute(
            "DELETE FROM engagements WHERE engagement_id = ?",
            (engagement_id,)
        )
