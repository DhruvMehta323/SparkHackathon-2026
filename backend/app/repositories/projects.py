from datetime import datetime
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository):

    @staticmethod
    def create_project(creator_id, title, abstract, stage):
        query = """
        INSERT INTO projects
        (creator_id, title, abstract, stage, created_at)
        VALUES (?, ?, ?, ?, ?)
        """
        return BaseRepository.execute(
            query,
            (creator_id, title, abstract, stage, datetime.utcnow().isoformat())
        )

    @staticmethod
    def get_project(project_id):
        return BaseRepository.fetch_one(
            "SELECT * FROM projects WHERE project_id = ?",
            (project_id,)
        )

    @staticmethod
    def get_all_projects():
        return BaseRepository.fetch_all(
            "SELECT * FROM projects"
        )

    @staticmethod
    def update_impressions(project_id, impressions):
        BaseRepository.execute(
            "UPDATE projects SET impressions = ? WHERE project_id = ?",
            (impressions, project_id)
        )
