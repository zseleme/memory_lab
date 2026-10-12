"""Unit tests for StorageEngine SQLite persistence."""

import time
import unittest
from memory_lab.storage.engine import StorageEngine


class TestStorageEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = StorageEngine(":memory:")
        self.engine.init_db()

    def tearDown(self) -> None:
        self.engine.close()

    def test_schema_initialization(self) -> None:
        tables = self.engine.get_tables()
        self.assertIn("episodic_memories", tables)
        self.assertIn("semantic_nodes", tables)
        self.assertIn("semantic_edges", tables)
        self.assertIn("working_memory", tables)
        self.assertIn("procedural_skills", tables)
        self.assertIn("fts_episodes", tables)

    def test_record_episode_latency_and_durability(self) -> None:
        t0 = time.time()
        ep_id = self.engine.record_episode(
            session_id="test-session-1",
            actor="user",
            content="Deploy database migrations",
            salience=0.85,
            tags="deploy,db",
        )
        elapsed = time.time() - t0
        self.assertLess(elapsed, 0.1, "Insertion took longer than 100ms")
        self.assertIsNotNone(ep_id)

        episodes = self.engine.get_episodes_by_session("test-session-1")
        self.assertEqual(len(episodes), 1)
        record = episodes[0]
        self.assertEqual(record["id"], ep_id)
        self.assertEqual(record["actor"], "user")
        self.assertEqual(record["content"], "Deploy database migrations")
        self.assertEqual(record["salience"], 0.85)

    def test_fts_search(self) -> None:
        self.engine.record_episode(
            session_id="sess-search",
            actor="engineer",
            content="Converge Pass 4 consensus reached with zero blockers",
            salience=0.9,
            tags="consensus,review",
        )
        results = self.engine.search_episodes_fts("consensus")
        self.assertGreaterEqual(len(results), 1)
        self.assertIn("consensus", results[0]["content"].lower())


if __name__ == "__main__":
    unittest.main()
