from app.repositories.base import BaseRepository


class CreatorRepository(BaseRepository):

    @staticmethod
    def create_creator_profile(user_id, role, skills, availability, location, bio):
        query = """
        INSERT INTO creator_profiles
        (creator_id, role, skills, availability, location, bio)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        return BaseRepository.execute(
            query,
            (user_id, role, skills, availability, location, bio)
        )

    @staticmethod
    def get_creator(creator_id):
        return BaseRepository.fetch_one(
            "SELECT * FROM creator_profiles WHERE creator_id = ?",
            (creator_id,)
        )

    @staticmethod
    def update_points(creator_id, points):
        BaseRepository.execute(
            "UPDATE creator_profiles SET points = ? WHERE creator_id = ?",
            (points, creator_id)
        )

    @staticmethod
    def get_all_creators():
        return BaseRepository.fetch_all(
            "SELECT * FROM creator_profiles"
        )
# app/repositories/creators.py

from app.repositories.base import BaseRepository


class CreatorRepository(BaseRepository):

    @staticmethod
    def create_creator_profile(user_id, role, skills, availability, location, bio):
        query = """
        INSERT INTO creator_profiles
        (creator_id, role, skills, availability, location, bio)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        return BaseRepository.execute(
            query,
            (user_id, role, skills, availability, location, bio)
        )

    @staticmethod
    def get_creator(creator_id):
        return BaseRepository.fetch_one(
            "SELECT * FROM creator_profiles WHERE creator_id = ?",
            (creator_id,)
        )

    @staticmethod
    def update_points(creator_id, points):
        BaseRepository.execute(
            "UPDATE creator_profiles SET points = ? WHERE creator_id = ?",
            (points, creator_id)
        )

    @staticmethod
    def delete_creator(creator_id):
        BaseRepository.execute(
            "DELETE FROM creator_profiles WHERE creator_id = ?",
            (creator_id,)
        )

    @staticmethod
    def get_all_creators():
        return BaseRepository.fetch_all(
            "SELECT * FROM creator_profiles"
        )
    
    @staticmethod
    def update_creator(creator_id, name=None, role=None, skills=None, bio=None, location=None, availability=None):
        """Update creator profile fields"""
        updates = []
        params = []
        
        # Note: name is in users table, not creator_profiles
        # We'll only update creator_profiles fields here
        
        if role:
            updates.append("role = ?")
            params.append(role)
        if skills:
            updates.append("skills = ?")
            # Skills should be comma-separated string
            params.append(skills if isinstance(skills, str) else ",".join(skills))
        if bio:
            updates.append("bio = ?")
            params.append(bio)
        if location:
            updates.append("location = ?")
            params.append(location)
        if availability:
            updates.append("availability = ?")
            params.append(availability)
        
        if not updates:
            return
        
        params.append(creator_id)
        
        query = f"UPDATE creator_profiles SET {', '.join(updates)} WHERE creator_id = ?"
        BaseRepository.execute(query, tuple(params))
    
    @staticmethod
    def count_creators(skill_filter=None):
        """Count total creators, optionally filtered by skills"""
        if skill_filter:
            # skill_filter is a list like ["Editing", "Color Grading"]
            # Check if any skill matches
            conditions = []
            params = []
            for skill in skill_filter:
                conditions.append("skills LIKE ?")
                params.append(f"%{skill}%")
            
            query = f"SELECT COUNT(*) FROM creator_profiles WHERE {' OR '.join(conditions)}"
            result = BaseRepository.fetch_one(query, tuple(params))
        else:
            result = BaseRepository.fetch_one("SELECT COUNT(*) FROM creator_profiles")
        
        return result[0] if result else 0
