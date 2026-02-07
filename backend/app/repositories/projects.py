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
    def get_all_projects(limit=None, offset=0, stage_filter=None):
        """Get all projects with optional pagination and stage filter"""
        query = "SELECT * FROM projects"
        params = []
        
        if stage_filter:
            query += " WHERE stage = ?"
            params.append(stage_filter)
        
        query += " ORDER BY created_at DESC"
        
        if limit:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])
        
        # Fix: Only pass params if there are any
        if params:
            return BaseRepository.fetch_all(query, tuple(params))
        else:
            return BaseRepository.fetch_all(query)
        
    @staticmethod
    def update_impressions(project_id, impressions):
        BaseRepository.execute(
            "UPDATE projects SET impressions = ? WHERE project_id = ?",
            (impressions, project_id)
        )

    
    @staticmethod
    def update_project(project_id, title=None, abstract=None, stage=None):
        """Update project fields"""
        updates = []
        params = []
        
        if title:
            updates.append("title = ?")
            params.append(title)
        if abstract:
            updates.append("abstract = ?")
            params.append(abstract)
        if stage:
            updates.append("stage = ?")
            params.append(stage)
        
        if not updates:
            return
        
        updates.append("updated_at = datetime('now')")
        params.append(project_id)
        
        query = f"UPDATE projects SET {', '.join(updates)} WHERE project_id = ?"
        BaseRepository.execute(query, tuple(params))
    
    @staticmethod
    def count_projects(stage_filter=None):
        """Count total projects"""
        query = "SELECT COUNT(*) FROM projects"
        params = None
        
        if stage_filter:
            query += " WHERE stage = ?"
            params = (stage_filter,)
        
        result = BaseRepository.fetch_one(query, params)
        return result[0] if result else 0
