"""Database schema definitions and migrations for Memory Lab SQLite engine."""

SCHEMA_SQL = """
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS episodic_memories (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    actor TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp REAL NOT NULL,
    salience REAL DEFAULT 0.5,
    tags TEXT DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_episodic_session ON episodic_memories(session_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_episodic_salience ON episodic_memories(salience DESC);

CREATE TABLE IF NOT EXISTS semantic_nodes (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    properties TEXT DEFAULT '{}',
    activation REAL DEFAULT 1.0,
    updated_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS semantic_edges (
    id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    weight REAL NOT NULL DEFAULT 0.5,
    updated_at REAL NOT NULL,
    UNIQUE(source_id, target_id),
    FOREIGN KEY(source_id) REFERENCES semantic_nodes(id) ON DELETE CASCADE,
    FOREIGN KEY(target_id) REFERENCES semantic_nodes(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_edges_source ON semantic_edges(source_id);
CREATE INDEX IF NOT EXISTS idx_edges_target ON semantic_edges(target_id);

CREATE TABLE IF NOT EXISTS working_memory (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    content TEXT NOT NULL,
    tokens INTEGER NOT NULL DEFAULT 0,
    salience REAL DEFAULT 0.5,
    updated_at REAL NOT NULL,
    UNIQUE(session_id, item_id)
);

CREATE INDEX IF NOT EXISTS idx_working_session ON working_memory(session_id, salience DESC);

CREATE TABLE IF NOT EXISTS procedural_skills (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    steps TEXT NOT NULL,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    last_used REAL NOT NULL,
    base_activation REAL DEFAULT 1.0
);

CREATE VIRTUAL TABLE IF NOT EXISTS fts_episodes USING fts5(
    content,
    actor,
    tags,
    tokenize = 'porter unicode61'
);

CREATE TRIGGER IF NOT EXISTS trg_episodic_ai AFTER INSERT ON episodic_memories BEGIN
    INSERT INTO fts_episodes(rowid, content, actor, tags)
    VALUES (new.rowid, new.content, new.actor, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS trg_episodic_ad AFTER DELETE ON episodic_memories BEGIN
    INSERT INTO fts_episodes(fts_episodes, rowid, content, actor, tags)
    VALUES('delete', old.rowid, old.content, old.actor, old.tags);
END;
"""
