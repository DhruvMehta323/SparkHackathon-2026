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
