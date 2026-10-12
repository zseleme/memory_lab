"""Unit tests for semantic association graph and spreading activation."""

import time
import unittest

from memory_lab.cognitive.semantic import SemanticGraph


class TestSemanticGraph(unittest.TestCase):
    """Test suite for SemanticGraph associative memory."""

    def setUp(self):
        self.graph = SemanticGraph(":memory:")

    def tearDown(self):
        self.graph.close()

    def test_add_and_retrieve_concept(self):
        node_id = self.graph.add_concept("python", {"category": "language"})
        self.assertIsNotNone(node_id)
        concept = self.graph.get_concept("python")
        self.assertIsNotNone(concept)
        self.assertEqual(concept["name"], "python")
        self.assertEqual(concept["properties"]["category"], "language")

    def test_linking_and_bidirectional_weights(self):
        self.graph.add_concept("python")
        self.graph.add_concept("sqlite")
        self.graph.link("python", "sqlite", weight=0.85, bidirectional=True)

        w1 = self.graph.get_edge_weight("python", "sqlite")
        w2 = self.graph.get_edge_weight("sqlite", "python")
        self.assertEqual(w1, 0.85)
        self.assertEqual(w2, 0.85)

    def test_spreading_activation_two_hops(self):
        # Build A -> B -> C network
        self.graph.add_concept("A")
        self.graph.add_concept("B")
        self.graph.add_concept("C")
        self.graph.link("A", "B", weight=0.9, bidirectional=True)
        self.graph.link("B", "C", weight=0.8, bidirectional=True)

        t0 = time.time()
        res = self.graph.activate("A", decay=0.85, max_hops=2)
        duration = time.time() - t0

        self.assertLess(duration, 0.2, "Spreading activation must finish in sub-200ms")
        self.assertIn("A", res)
        self.assertIn("B", res)
        self.assertIn("C", res)
        # A should have highest activation, then B, then C
        self.assertGreater(res["A"], res["B"])
        self.assertGreater(res["B"], res["C"])

    def test_graph_snapshot(self):
        self.graph.add_concept("Node1")
        self.graph.add_concept("Node2")
        self.graph.link("Node1", "Node2", 0.7)

        snapshot = self.graph.get_graph_snapshot()
        self.assertEqual(len(snapshot["nodes"]), 2)
        # Bidirectional creates 2 directed edges
        self.assertGreaterEqual(len(snapshot["edges"]), 2)


if __name__ == "__main__":
    unittest.main()
