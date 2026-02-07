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

    @staticmethod
    def get_project_stats(project_id):
        """Get aggregated engagement statistics for a project"""
        query = """
        SELECT 
            COUNT(*) as total_reactions,
            SUM(CASE WHEN reaction = 'like' THEN 1 ELSE 0 END) as likes,
            SUM(CASE WHEN reaction = 'insightful' THEN 1 ELSE 0 END) as insightful,
            SUM(CASE WHEN reaction = 'inspiring' THEN 1 ELSE 0 END) as inspiring
        FROM engagements
        WHERE project_id = ?
        """
        row = BaseRepository.fetch_one(query, (project_id,))
        
        # Get impressions from projects table
        project = ProjectRepository.get_project(project_id)
        impressions = project.get("impressions", 0) if project else 0
        
        if row:
            total_reactions = row[0] or 0
            engagement_score = total_reactions / max(impressions, 1) if impressions > 0 else 0.0
            
            return {
                "project_id": project_id,
                "total_reactions": total_reactions,
                "likes": row[1] or 0,
                "insightful": row[2] or 0,
                "inspiring": row[3] or 0,
                "impressions": impressions,
                "engagement_score": engagement_score
            }
        
        return None
