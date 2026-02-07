Project overview
- Language: Python 3
- DB: SQLite (backend/fairrank.db by default). Schema is in `app/models/schema.sql`.
- Repo pattern: `app/repositories/*` for DB access, `app/services/*` for business logic.
- Engines implemented:
  - `FairRankEngine` — compute fair-rank scores and update `fair_rank_scores`.
  - `SimilarityEngine` — deterministic text-based embeddings and pairwise similarity persisted to `project_embeddings` and `project_similarity`.
  - `MatchingEngine` — scores creators against a collaboration request and writes `collab_matches`.
- Gamification and rewards:
  - `app/services/gamification.py` and `app/repositories/rewards.py` (records rewards in `creator_rewards`, updates `creator_profiles.points` and `level`).

How to run & test locally
- From project root:
```bash
cd "path to your dir"/SparkHack
PYTHONPATH=. python3 app/scripts/init_db.py      # initialize schema
PYTHONPATH=. python3 -m unittest discover -v tests
```
- Integration harness:
```bash
PYTHONPATH=. python3 app/scripts/test_fairrank.py
```
- CLI (alternative):
```bash
PYTHONPATH=. python3 main.py --init-db
PYTHONPATH=. python3 main.py --run-fairrank
PYTHONPATH=. python3 main.py --compute-similarity
PYTHONPATH=. python3 main.py --run-matching --request-id 1
```

Key files and services (where to look)
- Schema: `app/models/schema.sql`
- DB helpers: `app/core/database.py`
- Logger: `app/core/logger.py`
- Repositories: `app/repositories/*.py` (users, creators, projects, engagements, embeddings, similarity, fairrank, collab, rewards, platform_stats)
- Services: `app/services/*.py` (fairrank_engine.py, similarity_engine.py, matching_engine.py, gamification.py)
- Integration script: `app/scripts/test_fairrank.py`
- CLI entrypoint: `main.py`

FastAPI endpoints to implement
--------------------------------
Base path: `/api` (recommended)

1) Health / info
- GET `/api/health`
  - Response: {"status": "ok", "time": "..."}

2) Initialize DB (admin)
- POST `/api/admin/init`  (or `/api/init`)
  - Body: none
  - Action: runs `app.scripts.init_db.init_database()` (idempotent)
  - Response: {"ok": true, "message": "initialized"}

3) Run FairRank engine
- POST `/api/engines/fairrank`
  - Body (optional): {"background": true|false}
  - Action: call `app.services.fairrank_engine.FairRankEngine.run()` (in background if requested)
  - Response (sync): {"ok": true}
  - Response (async): {"job_id": "...", "status": "started"}

4) Run Similarity engine
- POST `/api/engines/similarity`
  - Body (optional): {"dim": 16, "background": true|false}
  - Action: `SimilarityEngine.generate_dummy_embeddings(dim)` then `SimilarityEngine.compute_all_similarities()`
  - Response similar to FairRank

5) Run Matching for a request
- POST `/api/matching/{request_id}`
  - Path param: `request_id` (int)
  - Body (optional): {"background": true|false}
  - Action: `MatchingEngine.run(request_id)`

6) Create engagement (client-produced)
- POST `/api/engagements`
  - Body: {"project_id": int, "user_id": int, "reaction": "like|comment|other", "weight": float}
  - Action: call `app.repositories.engagements.EngagementRepository.create_engagement(...)` — this already triggers reward logic for like/comment
  - Response: {"engagement_id": 123}

7) Create collab request
- POST `/api/collab/requests`
  - Body: {"requester_id": int, "project_id": int, "role_needed": str, "skills_needed": str, "location_pref": str}
  - Action: `CollabRepository.create_request(...)`
  - Response: {"request_id": 1}

8) Run matching/accept match
- GET `/api/collab/requests/{id}/matches` — list matches
- POST `/api/collab/requests/{id}/matches/accept` — accept a match (this should be implemented to actually confirm collaboration; currently the repo only inserts matches and auto-awards on insertion)

9) Creator profile & rewards
- GET `/api/creators/{creator_id}` — returns `creator_profiles` row (points, level, etc.)
- GET `/api/creators/{creator_id}/rewards` — returns `creator_rewards` rows

10) FairRank leaderboard / project detail
- GET `/api/fairrank/top?n=10` — returns top N projects (read from `fair_rank_scores` joined with `projects`)
- GET `/api/projects/{project_id}` — project details + fairrank score + top similar projects (join `project_similarity`)

Request / Response examples
- Creating an engagement:
```http
POST /api/engagements
Content-Type: application/json

{ "project_id": 12, "user_id": 34, "reaction": "like", "weight": 1.0 }

Response 200
{ "engagement_id": 77 }
```

Integration notes & background tasks
- Running heavy work (similarity pairwise computations, full fairrank over many projects) should be offloaded to a background worker.
  - Quick options: use `fastapi.BackgroundTasks` for simple cases.
  - Scalable options: integrate Celery / RQ + Redis and return a job id for the frontend to poll.
- Ensure idempotency for endpoints that mutate state. Example: re-running `/engines/fairrank` should not duplicate rewards — `RewardRepository.add_reward` appends records, but FairRank awards are inserted every run. Consider adding a dedup key or timestamp window.

Security / auth suggestions
- Add an API key or JWT-based auth for admin endpoints (`/admin/init`, engine triggers), and protect any endpoints that mutate data.
- CORS: enable for frontend host(s).

Testing
- Unit tests already exist in `tests/test_engines.py`.
- Add API tests using `pytest` + `httpx` or `fastapi.testclient` to exercise endpoints.

Deployment notes
- Run FastAPI with uvicorn:
```bash
PYTHONPATH=. uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
```
- Use an environment variable `FAIRRANK_DB` to point to the intended DB file in production.
