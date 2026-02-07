Frontend integration section
---------------------------
High-level flows frontend will need to integrate:
- Sign-up / login (not implemented) — if auth will be added, frontend should request tokens and include them in `Authorization` header.
- Project page
  - Fetch project details: `GET /api/projects/{id}` (show title, description, fairrank score, creator info)
  - Show top similar projects: read from `project_similarity` or call an endpoint that returns similar projects.
  - Allow user to react to the project: `POST /api/engagements` (reaction = like|comment). The backend awards +1 for likes/comments.
- Creator profile / leaderboard
  - Fetch `GET /api/creators/{id}` and `GET /api/creators/{id}/rewards`.
  - Leaderboard: `GET /api/fairrank/top?n=20` to show top projects and link to creators.
- Collaboration flow
  - Create a collab request: `POST /api/collab/requests`.
  - Display matches: `GET /api/collab/requests/{id}/matches`.
  - Accepting a match: POST to accept endpoint (not yet implemented) — when implemented, it should award the collaborator bonus.

Data contracts & sample shapes for frontend
- Creator profile object (JSON):
  - {"creator_id": int, "role": str, "skills": str, "points": int, "level": int, "bio": str }
- Reward object:
  - {"reward_id": int, "creator_id": int, "reward_type": str, "value": float, "awarded_at": str }
- FairRank item:
  - {"project_id": int, "final_score": float, "engagement_score": float, "creator_id": int }

Developer checklist (step-by-step)
1. Create `app/api` directory and `app/api/main.py` as FastAPI app.
2. Add dependencies: `fastapi`, `uvicorn`, `python-dotenv` (optional). Update README or `requirements.txt`.
3. Implement health endpoint.
4. Implement admin init endpoint: call `app.scripts.init_db.init_database()`.
5. Implement endpoints to trigger engines:
   - `POST /api/engines/fairrank` -> `FairRankEngine.run()` (support background tasks)
   - `POST /api/engines/similarity` -> `SimilarityEngine.generate_dummy_embeddings()` + `SimilarityEngine.compute_all_similarities()`
6. Create engagement endpoint calling `EngagementRepository.create_engagement`.
7. Expose creators endpoints to fetch profile & rewards (read from `creator_profiles` and `creator_rewards`).
8. Implement project endpoints (project detail + similarity joins).
9. Implement collab endpoints and match listing/accept flow. Move reward-on-insert for collab to be awarded upon acceptance instead of match creation (recommended).
10. Add CORS, logging, error handlers, and OpenAPI docs.
11. Add tests using `fastapi.testclient` for all endpoints.

Notes & pitfalls
- SQLite is fine for small/dev usage. For production, migrate to PostgreSQL (schema will mostly apply, but adjust `ON CONFLICT` and concurrency). Avoid long-running DB locks during heavy pairwise similarity computations.
- Deduplicate reward issuance: FairRank currently awards top-10 every run by inserting `creator_rewards`. Add a dedup strategy (timestamp window or unique constraint with run_id) if you don't want repeated awards.