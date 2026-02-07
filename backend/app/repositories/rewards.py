from datetime import datetime
from app.repositories.base import BaseRepository


def compute_level(points: float) -> int:
    if points < 10:
        return 1
    elif points < 30:
        return 2
    elif points < 60:
        return 3
    elif points < 100:
        return 4
    else:
        return 5


class RewardRepository(BaseRepository):
    @staticmethod
    def add_reward(creator_id, reward_type, value):
        BaseRepository.execute(
            """
            INSERT INTO creator_rewards (creator_id, reward_type, value, awarded_at)
            VALUES (?, ?, ?, ?)
            """,
            (creator_id, reward_type, value, datetime.utcnow().isoformat()),
        )

        row = BaseRepository.fetch_one(
            "SELECT COALESCE(SUM(value), 0) as total FROM creator_rewards WHERE creator_id = ?",
            (creator_id,)
        )
        total = row.get("total") if row else 0
        level = compute_level(total or 0)

        BaseRepository.execute(
            "UPDATE creator_profiles SET points = ?, level = ? WHERE creator_id = ?",
            (total, level, creator_id),
        )

        return {"creator_id": creator_id, "points": total, "level": level}
