#!/usr/bin/env python3
import argparse
import os
from app.core.logger import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init-db", action="store_true")
    parser.add_argument("--run-fairrank", action="store_true")
    parser.add_argument("--compute-similarity", action="store_true")
    parser.add_argument("--run-matching", action="store_true")
    parser.add_argument("--request-id", type=int)
    parser.add_argument("--run-tests", action="store_true")
    args = parser.parse_args()

    if args.init_db:
        from app.scripts.init_db import init_database
        init_database()

    if args.run_fairrank:
        from app.services.fairrank_engine import FairRankEngine
        FairRankEngine.run()

    if args.compute_similarity:
        from app.services.similarity_engine import SimilarityEngine
        SimilarityEngine.generate_dummy_embeddings()
        SimilarityEngine.compute_all_similarities()

    if args.run_matching:
        from app.services.matching_engine import MatchingEngine
        if not args.request_id:
            logger.error("--request-id is required for --run-matching")
        else:
            MatchingEngine.run(args.request_id)

    if args.run_tests:
        os.environ.setdefault("PYTHONPATH", os.getcwd())
        from app.scripts.test_fairrank import populate, test_fairrank, test_similarity, test_matching
        populate()
        test_fairrank()
        test_similarity()
        test_matching()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""CLI entrypoint to run DB init and engines manually.

Usage examples:
  python3 main.py --init-db
  python3 main.py --run-fairrank
  python3 main.py --compute-similarity
  python3 main.py --run-matching --request-id 1
  python3 main.py --run-tests
"""
import argparse
import os
from app.core.logger import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="FairRank backend CLI")
    parser.add_argument("--init-db", action="store_true", help="Initialize the database schema")
    parser.add_argument("--run-fairrank", action="store_true", help="Run the FairRank engine")
    parser.add_argument("--compute-similarity", action="store_true", help="Run the similarity engine")
    parser.add_argument("--run-matching", action="store_true", help="Run matching for a request id")
    parser.add_argument("--request-id", type=int, help="Request id for matching")
    parser.add_argument("--run-tests", action="store_true", help="Run the test_fairrank script")

    args = parser.parse_args()

    if args.init_db:
        from app.scripts.init_db import init_database

        init_database()

    if args.run_fairrank:
        from app.services.fairrank_engine import FairRankEngine

        FairRankEngine.run()

    if args.compute_similarity:
        from app.services.similarity_engine import SimilarityEngine

        SimilarityEngine.generate_dummy_embeddings()
        SimilarityEngine.compute_all_similarities()

    if args.run_matching:
        from app.services.matching_engine import MatchingEngine

        if not args.request_id:
            logger.error("--request-id is required for --run-matching")
        else:
            MatchingEngine.run(args.request_id)

    if args.run_tests:
        # run test_fairrank script (same as running the module)
        os.environ.setdefault("PYTHONPATH", os.getcwd())
        from app.scripts.test_fairrank import populate, test_fairrank, test_similarity, test_matching

        populate()
        test_fairrank()
        test_similarity()
        test_matching()


if __name__ == "__main__":
    main()
