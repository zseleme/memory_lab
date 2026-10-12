"""Storage engine backed by SQLite with WAL mode and transaction safety."""

from __future__ import annotations

import sqlite3
import time
import uuid
from typing import Any

from .schema import SCHEMA_SQL


class StorageEngine:
    def __init__(self, db_path: str = "memory_lab.db") -> None:
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._configure_connection()

    def _configure_connection(self) -> None:
        cursor = self._conn.cursor()
        cursor.execute("PRAGMA journal_mode = WAL;")
        cursor.execute("PRAGMA synchronous = NORMAL;")
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.close()

    def init_db(self) -> None:
        cursor = self._conn.cursor()
        cursor.executescript(SCHEMA_SQL)
        self._conn.commit()
        cursor.close()

    def get_tables(self) -> list[str]:
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type IN ('table', 'view') AND name NOT LIKE 'sqlite_%';"
        )
        tables = [row["name"] for row in cursor.fetchall()]
        cursor.close()
        return tables

    def record_episode(
        self,
        session_id: str,
        actor: str,
        content: str,
        salience: float = 0.5,
        tags: str = "",
    ) -> str:
        episode_id = str(uuid.uuid4())
        now = time.time()
        cursor = self._conn.cursor()
        cursor.execute(
            """
            INSERT INTO episodic_memories (id, session_id, actor, content, timestamp, salience, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            (episode_id, session_id, actor, content, now, salience, tags),
        )
        self._conn.commit()
        cursor.close()
        return episode_id

    def get_episodes_by_session(
        self, session_id: str, limit: int = 50
    ) -> list[dict[str, Any]]:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT id, session_id, actor, content, timestamp, salience, tags
            FROM episodic_memories
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?;
            """,
            (session_id, limit),
        )
        rows = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        return rows

    def search_episodes_fts(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT rowid, content, actor, tags
            FROM fts_episodes
            WHERE fts_episodes MATCH ?
            ORDER BY rank
            LIMIT ?;
            """,
            (query, limit),
        )
        rows = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        return rows

    def close(self) -> None:
        if self._conn:
            self._conn.close()
