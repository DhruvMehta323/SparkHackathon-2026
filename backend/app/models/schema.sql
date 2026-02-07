-- Minimal schema for FairStage platform
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    user_type TEXT,
    verified INTEGER DEFAULT 0,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS creator_profiles (
    creator_id INTEGER PRIMARY KEY,
    role TEXT,
    skills TEXT,
    availability TEXT,
    location TEXT,
    bio TEXT,
    points REAL DEFAULT 0,
    level INTEGER DEFAULT 1,
    FOREIGN KEY (creator_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    creator_id INTEGER,
    title TEXT,
    abstract TEXT,
    description TEXT,
    stage TEXT,
    created_at TEXT,
    impressions INTEGER DEFAULT 0,
    FOREIGN KEY (creator_id) REFERENCES creator_profiles(creator_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS engagements (
    engagement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    user_id INTEGER,
    reaction TEXT,
    weight REAL,
    created_at TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS project_embeddings (
    project_id INTEGER PRIMARY KEY,
    embedding TEXT
);

CREATE TABLE IF NOT EXISTS project_similarity (
    project_a INTEGER,
    project_b INTEGER,
    similarity REAL,
    posted_first INTEGER,
    PRIMARY KEY (project_a, project_b)
);

CREATE TABLE IF NOT EXISTS fair_rank_scores (
    project_id INTEGER PRIMARY KEY,
    engagement_score REAL,
    freshness_boost REAL,
    diversity_boost REAL,
    underexposed_boost REAL,
    final_score REAL,
    computed_at TEXT
);

CREATE TABLE IF NOT EXISTS collab_requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    requester_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    role_needed TEXT,
    skills_needed TEXT,
    location_pref TEXT,
    availability TEXT,
    budget TEXT,
    status TEXT DEFAULT 'open',
    created_at TEXT NOT NULL,
    FOREIGN KEY (requester_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS collab_matches (
    request_id INTEGER NOT NULL,
    creator_id INTEGER NOT NULL,
    match_score REAL,
    explanation TEXT,
    PRIMARY KEY (request_id, creator_id),
    FOREIGN KEY (request_id) REFERENCES collab_requests(request_id) ON DELETE CASCADE,
    FOREIGN KEY (creator_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS creator_rewards (
    reward_id INTEGER PRIMARY KEY AUTOINCREMENT,
    creator_id INTEGER,
    reward_type TEXT,
    value REAL,
    awarded_at TEXT,
    FOREIGN KEY (creator_id) REFERENCES creator_profiles(creator_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS platform_stats (
    id INTEGER PRIMARY KEY DEFAULT 1,
    total_creators INTEGER DEFAULT 0,
    total_projects INTEGER DEFAULT 0,
    underexposed_count INTEGER DEFAULT 0,
    avg_fairrank REAL DEFAULT 0.0,
    exposure_gini REAL DEFAULT 0.0,
    updated_at TEXT
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_projects_creator ON projects(creator_id);
CREATE INDEX IF NOT EXISTS idx_engagements_project ON engagements(project_id);
CREATE INDEX IF NOT EXISTS idx_rewards_creator ON creator_rewards(creator_id);
CREATE INDEX IF NOT EXISTS idx_collab_matches_request ON collab_matches(request_id);
CREATE INDEX IF NOT EXISTS idx_collab_requests_project ON collab_requests(project_id);
CREATE INDEX IF NOT EXISTS idx_fairrank_score ON fair_rank_scores(final_score DESC);