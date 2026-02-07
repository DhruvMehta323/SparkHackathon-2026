from datetime import datetime
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):

    @staticmethod
    def create_user(name, user_type, verified=0):
        query = """
        INSERT INTO users (name, user_type, verified, created_at)
        VALUES (?, ?, ?, ?)
        """
        return BaseRepository.execute(
            query,
            (name, user_type, verified, datetime.utcnow().isoformat())
        )

    @staticmethod
    def get_user(user_id):
        return BaseRepository.fetch_one(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )

    @staticmethod
    def get_all_users():
        return BaseRepository.fetch_all(
            "SELECT * FROM users"
        )
