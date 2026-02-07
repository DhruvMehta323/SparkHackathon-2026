from app.repositories.users import UserRepository
from app.repositories.creators import CreatorRepository
from app.repositories.projects import ProjectRepository
from app.repositories.engagements import EngagementRepository
from app.services.fairrank_engine import FairRankEngine
from app.services.similarity_engine import SimilarityEngine
from app.services.matching_engine import MatchingEngine


def populate():
    # quick synthetic population
    users = []
    projects = []
    for i in range(1, 6):
        uid = UserRepository.create_user(f"User{i}", "creator")
        CreatorRepository.create_creator_profile(uid, "dev", "python", "full", "NY", "bio")
        pid = ProjectRepository.create_project(uid, f"Project {i}", "An example project", "idea")
        users.append(uid)
        projects.append(pid)

    # add some engagements
    for p in projects:
        for u in users[:3]:
            EngagementRepository.create_engagement(p, u, "like", weight=1.0)


def test_fairrank():
    FairRankEngine.run()


def test_similarity():
    SimilarityEngine.generate_dummy_embeddings(dim=16)
    SimilarityEngine.compute_all_similarities()


def test_matching():
    # create a request and run matching
    uid = UserRepository.create_user("ReqUser", "creator")
    CreatorRepository.create_creator_profile(uid, "pm", "management", "part", "SF", "bio")
    pid = ProjectRepository.create_project(uid, "ReqProject", "Need help", "idea")
    from app.repositories.collab import CollabRepository
    rid = CollabRepository.create_request(uid, pid, "dev", "python", "NY")
    MatchingEngine.run(rid)


if __name__ == "__main__":
    populate()
    test_fairrank()
    test_similarity()
    test_matching()
from datetime import datetime
import json
import random
from app.core.logger import get_logger

logger = get_logger(__name__)

from app.repositories.base import BaseRepository
from app.repositories.users import UserRepository
from app.repositories.creators import CreatorRepository
from app.repositories.projects import ProjectRepository
from app.repositories.engagements import EngagementRepository
from app.repositories.fairrank import FairRankRepository
from app.services.fairrank_engine import FairRankEngine

from app.services.similarity_engine import SimilarityEngine
from app.repositories.similarity import SimilarityRepository

from app.services.matching_engine import MatchingEngine
from app.repositories.collab import CollabRepository


# -------------------------
# TEST COLLAB MATCHING
# -------------------------
def test_matching():
    logger.info("--- TESTING MATCHING ---")

    users = UserRepository.get_all_users()
    projects = ProjectRepository.get_all_projects()

    if not users or not projects:
        logger.warning("No users or projects available for matching test.")
        return

    request_id = CollabRepository.create_request(
        requester_id=users[0]["user_id"],
        project_id=projects[0]["project_id"],
        role_needed="ML Engineer",
        skills_needed="Python, ML",
        location_pref="USA",
    )

    MatchingEngine.run(request_id)

    matches = BaseRepository.fetch_all(
        "SELECT * FROM collab_matches WHERE request_id = ? ORDER BY match_score DESC",
        (request_id,)
    )

    logger.info("Match Results:")
    for m in matches:
        logger.info(m)


# -------------------------
# TEST SIMILARITY ENGINE
# -------------------------
def test_similarity():
    logger.info("--- GENERATING EMBEDDINGS ---")
    SimilarityEngine.generate_dummy_embeddings()

    logger.info("--- COMPUTING SIMILARITIES ---")
    SimilarityEngine.compute_all_similarities()

    similar = SimilarityRepository.get_similar_projects(1)
    logger.info("Similar to Project 1:")
    for s in similar[:5]:
        logger.info(s)


# -------------------------
# POPULATE DUMMY DATA
# -------------------------
def populate():
    logger.info("--- POPULATING DUMMY DATA ---")

    # Clear tables to avoid duplicates (order matters due to FKs)
    for tbl in [
        "collab_matches",
        "collab_requests",
        "project_similarity",
        "project_embeddings",
        "engagements",
        "projects",
        "creator_profiles",
        "users",
        "fair_rank_scores",
    ]:
        try:
            BaseRepository.execute(f"DELETE FROM {tbl}")
            logger.debug("Cleared table %s", tbl)
        except Exception:
            logger.exception("Failed to clear table %s", tbl)

    # Users and Creators
    users = []
    for i in range(5):
        uid = UserRepository.create_user(f"User{i}", "creator")
        CreatorRepository.create_creator_profile(uid, "Dev", "Python, ML", "Full-time", "USA", "Bio")
        users.append(uid)

    # Projects
    projects = []
    for u in users:
        for i in range(2):  # 2 projects per user
            pid = ProjectRepository.create_project(u, f"Project_{u}_{i}", "Abstract", "Idea")
            projects.append(pid)

    # Uneven Engagements (increasing weight)
    for i, pid in enumerate(projects):
        for j in range(i):  # More engagement for later projects
            try:
                EngagementRepository.create_engagement(pid, users[j % len(users)], "like", weight=1.0)
            except Exception:
                logger.exception("Failed to create engagement for project %s", pid)

    logger.info("Dummy data created.")


# -------------------------
# TEST FAIRRANK
# -------------------------
def test_fairrank():
    print("\n--- RUNNING FAIR RANK ---")
    FairRankEngine.run()
    ranked = FairRankRepository.get_ranked_projects()

    print("\n--- FAIR RANK RESULTS ---")
    for r in ranked:
        print(r)


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    populate()
    try:
        test_fairrank()
    except Exception:
        logger.exception("fairrank test failed")

    try:
        test_similarity()
    except Exception:
        logger.exception("similarity test failed")

    try:
        test_matching()
    except Exception:
        logger.exception("matching test failed")
