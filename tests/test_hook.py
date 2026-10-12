"""Unit tests for Converge pre/post execution memory hooks."""

import unittest

from memory_lab.interfaces.hook import MemoryHook


class TestMemoryHook(unittest.TestCase):
    """Test suite for MemoryHook lifecycle integration."""

    def setUp(self):
        self.hook = MemoryHook(db_path=":memory:")

    def tearDown(self):
        self.hook.close()

    def test_pre_execution_context_empty(self):
        ctx = self.hook.pre_execution_context("test-session")
        self.assertIsInstance(ctx, str)
        self.assertIn("test-session", ctx)
        self.assertIn("Working Tokens", ctx)

    def test_pre_and_post_execution_flow(self):
        # Post execution record
        ep_id = self.hook.post_execution_record(
            session_id="build-42",
            actor="agent-executor",
            outcome_summary="Compiled rust crate with zero warnings",
            salience=0.9,
            tags="build,rust",
            skill_name="build_rust",
            success=True,
        )
        self.assertIsNotNone(ep_id)

        # Pre execution context for next run in the same session
        ctx = self.hook.pre_execution_context("build-42")
        self.assertIn("build-42", ctx)
        self.assertIn("Compiled rust crate", ctx)
        self.assertIn("build_rust", ctx)

    def test_semantic_query_hint(self):
        # Seed graph in server
        self.hook.server.semantic.add_concept("sqlite")
        self.hook.server.semantic.add_concept("wal")
        self.hook.server.semantic.link("sqlite", "wal", 0.95)

        ctx = self.hook.pre_execution_context("session-wal", query="sqlite")
        self.assertIn("wal", ctx)


if __name__ == "__main__":
    unittest.main()
