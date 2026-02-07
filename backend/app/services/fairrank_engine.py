import math
from datetime import datetime
from app.core.logger import get_logger
from app.repositories.projects import ProjectRepository
from app.repositories.engagements import EngagementRepository
from app.repositories.fairrank import FairRankRepository
from app.repositories.platform_stats import PlatformStatsRepository
from app.repositories.rewards import RewardRepository

logger = get_logger(__name__)


class FairRankEngine:
    @staticmethod
    def compute_gini(values):
        sorted_vals = sorted(values)
        n = len(values)
        if n == 0:
            return 0
        cumulative = 0
        for i, val in enumerate(sorted_vals):
            cumulative += (i + 1) * val
        total = sum(sorted_vals)
        if total == 0:
            return 0
        return (2 * cumulative) / (n * total) - (n + 1) / n

    @staticmethod
    def run():
        logger.info("Starting FairRankEngine.run()")
        try:
            projects = ProjectRepository.get_all_projects()
            project_data = []
            now = datetime.utcnow()

            raw_engagements = {}
            exposures = {}
            freshness_map = {}
            for p in projects:
                engagements = EngagementRepository.get_project_engagements(p["project_id"])
                raw_eng = sum(e.get("weight", 0) for e in engagements)
                raw_engagements[p["project_id"]] = raw_eng
                exposure = p.get("impressions", 0)
                exposures[p["project_id"]] = exposure
                age_days = (now - datetime.fromisoformat(p.get("created_at"))).days + 1
                freshness_map[p["project_id"]] = 1.0 / max(1, age_days)

            eng_vals = list(raw_engagements.values())
            exp_vals = list(exposures.values())

            def normalize_list(vals):
                if not vals:
                    return {}
                vmin, vmax = min(vals), max(vals)
                if vmin == vmax:
                    return {k: 0.5 for k in raw_engagements.keys()}
                return {k: (v - vmin) / (vmax - vmin) for k, v in zip(raw_engagements.keys(), vals)}

            normalized_eng = normalize_list(eng_vals)
            normalized_exp = normalize_list(exp_vals)

            for p in projects:
                pid = p["project_id"]
                engagement_score = normalized_eng.get(pid, 0.0)
                freshness = freshness_map.get(pid, 0.0)
                underexposed_boost = min(1.0, max(0.0, 1.0 - normalized_exp.get(pid, 0.0)))
                diversity_boost = 1.0
                raw_score = (0.6 * engagement_score + 0.15 * freshness + 0.15 * underexposed_boost + 0.10 * diversity_boost)
                project_data.append((pid, engagement_score, freshness, diversity_boost, underexposed_boost, raw_score))

            gini = FairRankEngine.compute_gini(list(raw_engagements.values()))
            avg_score = sum(d[-1] for d in project_data) / len(project_data) if project_data else 0

            for data in project_data:
                FairRankRepository.upsert_score(*data)

            try:
                creator_map = {p["project_id"]: p.get("creator_id") for p in projects}
                sorted_projects = sorted(project_data, key=lambda d: d[-1], reverse=True)
                top_n = 10
                for entry in sorted_projects[:top_n]:
                    pid = entry[0]
                    cid = creator_map.get(pid)
                    if cid:
                        RewardRepository.add_reward(cid, "FairRank Boost", 10)
            except Exception:
                logger.exception("Failed to award FairRank boosts")

            PlatformStatsRepository.update_stats(
                len(set(p["creator_id"] for p in projects)),
                len(projects),
                0,
                avg_score,
                gini,
            )

            logger.info("FairRankEngine completed: projects=%d gini=%.4f avg_score=%.4f", len(projects), gini, avg_score)
            return True
        except Exception:
            logger.exception("FairRankEngine.run failed")
            raise
import math
from datetime import datetime
from app.core.logger import get_logger
from app.repositories.projects import ProjectRepository
from app.repositories.engagements import EngagementRepository
from app.repositories.fairrank import FairRankRepository
from app.repositories.platform_stats import PlatformStatsRepository
from app.repositories.rewards import RewardRepository

logger = get_logger(__name__)


class FairRankEngine:
    """Compute fair-rank scores for projects and update platform stats.

    The engine reads projects and their engagements, computes a simple
    combination score (engagement, freshness, exposure boost, diversity),
    writes per-project final scores into `fair_rank_scores` and updates
    `platform_stats`.

    Notes for debugging: logs the Gini coefficient and average score. The
    scoring formula is intentionally simple; tune weights for production.
    """

    @staticmethod
    def compute_gini(values):
        """Return the Gini coefficient for a list of non-negative numbers.

        Gini is 0 when all values are equal and approaches 1 when inequality
        is high. If total is zero, returns 0.
        """
        sorted_vals = sorted(values)
        n = len(values)
        if n == 0:
            return 0
        cumulative = 0
        for i, val in enumerate(sorted_vals):
            cumulative += (i + 1) * val
        total = sum(sorted_vals)
        if total == 0:
            return 0
        return (2 * cumulative) / (n * total) - (n + 1) / n

    @staticmethod
    def run():
        """Run the fair-rank computation end-to-end and persist results.

        Logs progress at DEBUG level and raises on unexpected errors.
        """
        logger.info("Starting FairRankEngine.run()")
        try:
            projects = ProjectRepository.get_all_projects()
            engagement_scores = []
            project_data = []

            now = datetime.utcnow()

            # First pass: collect raw engagement and exposure values
            raw_engagements = {}
            exposures = {}
            freshness_map = {}
            for p in projects:
                engagements = EngagementRepository.get_project_engagements(p["project_id"])
                raw_eng = sum(e.get("weight", 0) for e in engagements)
                raw_engagements[p["project_id"]] = raw_eng

                exposure = p.get("impressions", 0)
                exposures[p["project_id"]] = exposure

                age_days = (now - datetime.fromisoformat(p["created_at"])).days + 1
                freshness_map[p["project_id"]] = 1.0 / max(1, age_days)

            # Normalize engagement and exposure to [0,1] to avoid skew
            eng_vals = list(raw_engagements.values())
            exp_vals = list(exposures.values())

            def normalize_list(vals):
                if not vals:
                    return {}
                vmin, vmax = min(vals), max(vals)
                if vmin == vmax:
                    return {i: 0.5 for i in range(len(vals))}
                return {k: (v - vmin) / (vmax - vmin) for k, v in zip(raw_engagements.keys(), vals)}

            normalized_eng = normalize_list(eng_vals)
            normalized_exp = normalize_list(exp_vals)

            # Second pass: compute boosts and final scores using normalized values
            for p in projects:
                pid = p["project_id"]
                engagement_score = normalized_eng.get(pid, 0.0)

                freshness = freshness_map.get(pid, 0.0)

                exposure = exposures.get(pid, 0)
                # underexposed boost: higher when exposure is low, capped [0,1]
                underexposed_boost = min(1.0, max(0.0, 1.0 - normalized_exp.get(pid, 0.0)))

                # diversity placeholder
                diversity_boost = 1.0

                # Compose final score from normalized components with caps
                raw_score = (
                    0.6 * engagement_score
                    + 0.15 * freshness
                    + 0.15 * underexposed_boost
                    + 0.10 * diversity_boost
                )

                project_data.append((pid, engagement_score, freshness, diversity_boost, underexposed_boost, raw_score))

            gini = FairRankEngine.compute_gini(engagement_scores)

            avg_score = sum(d[-1] for d in project_data) / len(project_data) if project_data else 0

            for data in project_data:
                FairRankRepository.upsert_score(*data)

            # Award top-N projects with a FairRank boost
            try:
                # map project_id to creator_id
                creator_map = {p["project_id"]: p.get("creator_id") for p in projects}
                sorted_projects = sorted(project_data, key=lambda d: d[-1], reverse=True)
                top_n = 10
                for entry in sorted_projects[:top_n]:
                    pid = entry[0]
                    cid = creator_map.get(pid)
                    if cid:
                        RewardRepository.add_reward(cid, "FairRank Boost", 10)
            except Exception:
                logger.exception("Failed to award FairRank boosts")

            PlatformStatsRepository.update_stats(
                len(set(p["creator_id"] for p in projects)),
                len(projects),
                len([e for e in engagement_scores if e < 5]),
                avg_score,
                gini,
            )

            logger.info("FairRankEngine completed: projects=%d gini=%.4f avg_score=%.4f",
                        len(projects), gini, avg_score)
            return True
        except Exception:
            logger.exception("FairRankEngine.run failed")
            raise
