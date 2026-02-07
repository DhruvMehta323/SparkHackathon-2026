from datetime import datetime
from app.repositories.base import BaseRepository
from app.repositories.rewards import RewardRepository


class CollabRepository(BaseRepository):

    @staticmethod
    def create_request(requester_id, project_id, role_needed, skills_needed, location_pref):
        query = """
        INSERT INTO collab_requests
        (requester_id, project_id, role_needed, skills_needed, location_pref, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        return BaseRepository.execute(
            query,
            (requester_id, project_id, role_needed, skills_needed, location_pref, datetime.utcnow().isoformat())
        )

    @staticmethod
    def insert_match(request_id, creator_id, score):
        query = """
        INSERT INTO collab_matches
        (request_id, creator_id, match_score)
        VALUES (?, ?, ?)
        ON CONFLICT(request_id, creator_id) DO UPDATE SET
            match_score=excluded.match_score
        """
        BaseRepository.execute(query, (request_id, creator_id, score))
        try:
            RewardRepository.add_reward(creator_id, "Collaboration Bonus", 5)
        except Exception:
            pass

    @staticmethod
    def get_request(request_id):
        return BaseRepository.fetch_one(
            "SELECT * FROM collab_requests WHERE request_id = ?",
            (request_id,)
        )
from datetime import datetime
from app.repositories.base import BaseRepository
from app.repositories.rewards import RewardRepository


class CollabRepository(BaseRepository):

    @staticmethod
    def create_request(requester_id, project_id,
                       role_needed, skills_needed, location_pref):

        query = """
        INSERT INTO collab_requests
        (requester_id, project_id, role_needed,
         skills_needed, location_pref, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        return BaseRepository.execute(
            query,
            (requester_id, project_id,
             role_needed, skills_needed,
             location_pref,
             datetime.utcnow().isoformat())
        )

    @staticmethod
    def insert_match(request_id, creator_id, score):
        query = """
        INSERT INTO collab_matches
        (request_id, creator_id, match_score)
        VALUES (?, ?, ?)
        ON CONFLICT(request_id, creator_id) DO UPDATE SET
            match_score=excluded.match_score
        """
        BaseRepository.execute(query, (request_id, creator_id, score))
        # award collaboration bonus when match is created
        try:
            RewardRepository.add_reward(creator_id, "Collaboration Bonus", 5)
        except Exception:
            pass

    @staticmethod
    def get_request(request_id):
        return BaseRepository.fetch_one(
            "SELECT * FROM collab_requests WHERE request_id = ?",
            (request_id,)
        )
    
    @staticmethod
    def get_matches_for_request(request_id):
        """Get all matches for a collaboration request with creator details"""
        query = """
        SELECT 
            m.creator_id,
            u.name,
            m.match_score,
            c.skills,
            c.location,
            c.availability
        FROM collab_matches m
        JOIN creator_profiles c ON m.creator_id = c.creator_id
        JOIN users u ON c.creator_id = u.user_id
        WHERE m.request_id = ?
        ORDER BY m.match_score DESC
        """
        rows = BaseRepository.fetch_all(query, (request_id,))
        
        # Convert to format expected by API
        matches = []
        for row in rows:
            matches.append({
                "creator_id": row[0],
                "creator_name": row[1],
                "match_score": row[2],
                "explanation": f"Match score: {row[2]:.2f}",
                "skills": row[3].split(",") if row[3] else [],
                "location": row[4],
                "availability": row[5]
            })
        return matches
