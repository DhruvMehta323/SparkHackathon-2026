from datetime import datetime
from app.repositories.creators import CreatorRepository
from app.repositories.base import BaseRepository
from app.repositories.rewards import RewardRepository, compute_level
from app.core.logger import get_logger

logger = get_logger(__name__)


class GamificationService:
    LEVEL_THRESHOLDS = [0, 100, 300, 700, 1500]

    @staticmethod
    def level_for_points(points: int) -> int:
        level = 1
        for i, thresh in enumerate(GamificationService.LEVEL_THRESHOLDS):
            if points >= thresh:
                level = i + 1
        return level

    @staticmethod
    def award_points(creator_id: int, points: int, reason: str = ""):
        try:
            res = RewardRepository.add_reward(creator_id, "generic", points)
            logger.info("Awarded %s points to creator %s (reason=%s) -> %s", points, creator_id, reason, res)
            return res
        except Exception:
            logger.exception("Failed to award points to %s", creator_id)
            raise
