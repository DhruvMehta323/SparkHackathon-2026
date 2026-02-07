from app.core.logger import get_logger
from app.repositories.creators import CreatorRepository
from app.repositories.collab import CollabRepository

logger = get_logger(__name__)


class MatchingEngine:
    @staticmethod
    def skill_overlap(skills1, skills2):
        if not skills1 or not skills2:
            return 0
        s1 = set(s.strip().lower() for s in skills1.split(",") if s.strip())
        s2 = set(s.strip().lower() for s in skills2.split(",") if s.strip())
        return len(s1 & s2)

    @staticmethod
    def run(request_id):
        logger.info("Running MatchingEngine for request_id=%s", request_id)
        request = CollabRepository.get_request(request_id)
        creators = CreatorRepository.get_all_creators()
        if not request:
            logger.warning("No collab request found for id=%s", request_id)
            return
        for c in creators:
            try:
                skill_score = MatchingEngine.skill_overlap(request.get("skills_needed"), c.get("skills"))
                location_score = 1 if request.get("location_pref") == c.get("location") else 0
                total_score = skill_score * 2 + location_score
                CollabRepository.insert_match(request_id, c["creator_id"], total_score)
            except Exception:
                logger.exception("Failed to compute/insert match for creator_id=%s", c.get("creator_id"))
                raise
from app.core.logger import get_logger
from app.repositories.creators import CreatorRepository
from app.repositories.collab import CollabRepository

logger = get_logger(__name__)


class MatchingEngine:
    """Simple matching engine that scores creators against a collaboration

    request using skill overlap and location preference. Each match is
    written to the `collab_matches` table.
    """

    @staticmethod
    def skill_overlap(skills1, skills2):
        """Return the number of overlapping skills between two comma-separated strings."""
        if not skills1 or not skills2:
            return 0
        s1 = set(s.strip().lower() for s in skills1.split(",") if s.strip())
        s2 = set(s.strip().lower() for s in skills2.split(",") if s.strip())
        return len(s1 & s2)

    @staticmethod
    def run(request_id):
        logger.info("Running MatchingEngine for request_id=%s", request_id)
        request = CollabRepository.get_request(request_id)
        creators = CreatorRepository.get_all_creators()

        if not request:
            logger.warning("No collab request found for id=%s", request_id)
            return

        for c in creators:
            try:
                skill_score = MatchingEngine.skill_overlap(
                    request.get("skills_needed"),
                    c.get("skills"),
                )

                location_score = 1 if request.get("location_pref") == c.get("location") else 0

                total_score = skill_score * 2 + location_score

                CollabRepository.insert_match(request_id, c["creator_id"], total_score)
            except Exception:
                logger.exception("Failed to compute/insert match for creator_id=%s", c.get("creator_id"))
                raise
