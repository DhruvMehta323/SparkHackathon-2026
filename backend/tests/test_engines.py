import os
import unittest
import tempfile

from app.scripts import init_db
from app.repositories.users import UserRepository
from app.repositories.creators import CreatorRepository
from app.repositories.projects import ProjectRepository
from app.repositories.engagements import EngagementRepository
from app.repositories.embeddings import EmbeddingRepository
from app.repositories.fairrank import FairRankRepository
from app.services.similarity_engine import SimilarityEngine
from app.services.fairrank_engine import FairRankEngine
from app.services.gamification import GamificationService


class EnginesTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_fd, cls.db_path = tempfile.mkstemp(prefix="fairrank_test_", suffix=".db")
        os.environ["FAIRRANK_DB"] = cls.db_path
        init_db.init_database()

    @classmethod
    def tearDownClass(cls):
        try:
            os.close(cls.db_fd)
        except Exception:
            pass
        try:
            os.remove(cls.db_path)
        except Exception:
            pass

    def test_similarity_embeddings_and_cosine(self):
        u1 = UserRepository.create_user("Alice", "creator")
        CreatorRepository.create_creator_profile(u1, "dev", "python", "full", "NY", "bio")
        p1 = ProjectRepository.create_project(u1, "Build AI", "An AI project about models", "idea")

        u2 = UserRepository.create_user("Bob", "creator")
        CreatorRepository.create_creator_profile(u2, "designer", "ui ux", "part", "SF", "bio2")
        p2 = ProjectRepository.create_project(u2, "Design App", "A simple app focused on UX", "prototype")

        SimilarityEngine.generate_dummy_embeddings(dim=16)
        emb = EmbeddingRepository.get_all_embeddings()
        self.assertTrue(len(emb) >= 2)

        parsed = {e["project_id"]: e["embedding"] for e in emb}
        v1 = parsed.get(p1)
        v2 = parsed.get(p2)
        self.assertIsNotNone(v1)
        self.assertIsNotNone(v2)

        sim = SimilarityEngine.cosine_similarity(v1, v2)
        self.assertGreaterEqual(sim, -1.0)
        self.assertLessEqual(sim, 1.0)

    def test_gamification_award_and_level(self):
        u = UserRepository.create_user("Carol", "creator")
        CreatorRepository.create_creator_profile(u, "dev", "go", "full", "Remote", "bio3")

        res = GamificationService.award_points(u, 120, "unit-test")
        self.assertIsNotNone(res)

        profile = CreatorRepository.get_creator(u)
        self.assertIsNotNone(profile)
        self.assertGreaterEqual(profile.get("points") or 0, 120)
        self.assertGreaterEqual(profile.get("level") or 1, 2)

    def test_fairrank_run_creates_scores(self):
        u = UserRepository.create_user("D", "creator")
        CreatorRepository.create_creator_profile(u, "dev", "rust", "full", "LA", "bio4")
        p = ProjectRepository.create_project(u, "CoolLib", "Library project", "beta")
        EngagementRepository.create_engagement(p, u, "like", weight=1.0)

        ok = FairRankEngine.run()
        self.assertTrue(ok)

        scores = FairRankRepository.get_ranked_projects()
        self.assertIsInstance(scores, list)


if __name__ == "__main__":
    unittest.main()
