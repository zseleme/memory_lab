"""Unit tests for working memory buffer and procedural reinforcement store."""

import unittest

from memory_lab.cognitive.working import (
    ProceduralStore,
    WorkingMemoryBuffer,
    WorkingMemoryItem,
)


class TestWorkingMemoryBuffer(unittest.TestCase):
    """Test suite for WorkingMemoryBuffer token bounds and eviction."""

    def test_within_budget(self):
        buf = WorkingMemoryBuffer(max_tokens=4000)
        buf.add_item("item-1", "some content", tokens=500, salience=0.6)
        buf.add_item("item-2", "more content", tokens=1200, salience=0.8)

        self.assertEqual(buf.current_tokens, 1700)
        self.assertEqual(len(buf.get_active_items()), 2)
        # Should be sorted by salience descending
        items = buf.get_active_items()
        self.assertEqual(items[0].item_id, "item-2")
        self.assertEqual(items[1].item_id, "item-1")

    def test_eviction_on_ceiling_breach(self):
        buf = WorkingMemoryBuffer(max_tokens=4000)
        buf.add_item("low-salience", "x" * 1000, tokens=1000, salience=0.3)
        buf.add_item("mid-salience", "y" * 1500, tokens=1500, salience=0.6)
        # Adding large high-salience item
        buf.add_item("high-salience", "z" * 2500, tokens=2500, salience=0.9)

        self.assertLessEqual(buf.current_tokens, 4000)
        active_ids = [i.item_id for i in buf.get_active_items()]
        # "high-salience" and "mid-salience" should be kept, "low-salience" evicted
        self.assertIn("high-salience", active_ids)
        self.assertNotIn("low-salience", active_ids)

    def test_pack_context_and_clear(self):
        buf = WorkingMemoryBuffer(max_tokens=4000)
        buf.add_item("c1", "System prompt", tokens=10, salience=1.0)
        buf.add_item("c2", "User query", tokens=5, salience=0.8)

        packed = buf.pack_context()
        self.assertIn("System prompt", packed)
        self.assertIn("User query", packed)

        buf.clear()
        self.assertEqual(buf.current_tokens, 0)
        self.assertEqual(len(buf.get_active_items()), 0)


class TestProceduralStore(unittest.TestCase):
    """Test suite for ProceduralStore skill tracking and power-law dynamics."""

    def setUp(self):
        self.store = ProceduralStore(":memory:")

    def tearDown(self):
        self.store.close()

    def test_register_and_get_skill(self):
        skill_id = self.store.register_skill("deploy_app", ["step1", "step2"])
        self.assertIsNotNone(skill_id)

        skill = self.store.get_skill("deploy_app")
        self.assertIsNotNone(skill)
        self.assertEqual(skill["name"], "deploy_app")
        self.assertEqual(skill["success_count"], 0)
        self.assertEqual(skill["failure_count"], 0)

    def test_reinforce_success_increases_activation(self):
        self.store.register_skill("test_skill", "steps", base_activation=1.0)
        initial_act = self.store.get_skill("test_skill")["base_activation"]

        self.store.reinforce("test_skill", success=True)
        updated = self.store.get_skill("test_skill")

        self.assertEqual(updated["success_count"], 1)
        self.assertGreater(updated["base_activation"], initial_act)

    def test_reinforce_failure_decreases_activation(self):
        self.store.register_skill("flaky_skill", "steps", base_activation=1.0)
        initial_act = self.store.get_skill("flaky_skill")["base_activation"]

        self.store.reinforce("flaky_skill", success=False)
        updated = self.store.get_skill("flaky_skill")

        self.assertEqual(updated["failure_count"], 1)
        self.assertLess(updated["base_activation"], initial_act)

    def test_list_skills_ranking(self):
        self.store.register_skill("low_skill", "steps", base_activation=0.5)
        self.store.register_skill("high_skill", "steps", base_activation=2.0)

        skills = self.store.list_skills()
        self.assertEqual(len(skills), 2)
        self.assertEqual(skills[0]["name"], "high_skill")
        self.assertEqual(skills[1]["name"], "low_skill")


if __name__ == "__main__":
    unittest.main()
