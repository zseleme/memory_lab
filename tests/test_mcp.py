"""Unit tests for Model Context Protocol (MCP) server and JSON-RPC dispatch."""

import json
import unittest

from memory_lab.interfaces.mcp_server import (
    create_mcp_server,
    handle_jsonrpc_request,
)


class TestMCPServer(unittest.TestCase):
    """Test suite for MCP server interface and tool dispatch."""

    def setUp(self):
        self.server = create_mcp_server(":memory:")

    def tearDown(self):
        self.server.close()

    def test_list_tools(self):
        tools = self.server.list_tools()
        names = [t.name for t in tools]
        self.assertIn("remember_episodic", names)
        self.assertIn("search_semantic", names)
        self.assertIn("get_working_context", names)
        self.assertIn("reinforce_procedure", names)

    def test_jsonrpc_initialize(self):
        req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        res = self.server.handle_request(req)
        self.assertEqual(res["id"], 1)
        self.assertEqual(res["result"]["serverInfo"]["name"], "memory-lab")

    def test_remember_episodic_tool(self):
        req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "remember_episodic",
                "arguments": {
                    "session_id": "sess-alpha",
                    "actor": "user",
                    "content": "Fixed regression in WAL connection pooling",
                    "salience": 0.8,
                },
            },
        }
        res = self.server.handle_request(req)
        self.assertIn("result", res)
        struct = res["result"]["structured"]
        self.assertEqual(struct["status"], "recorded")
        self.assertIsNotNone(struct["episode_id"])

    def test_search_semantic_tool(self):
        # Seed graph
        self.server.semantic.add_concept("compiler")
        self.server.semantic.add_concept("parser")
        self.server.semantic.link("compiler", "parser", 0.9)

        req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "search_semantic",
                "arguments": {"concept": "compiler", "decay": 0.85, "max_hops": 2},
            },
        }
        res = self.server.handle_request(req)
        self.assertIn("result", res)
        struct = res["result"]["structured"]
        self.assertIn("parser", struct["activations"])

    def test_get_working_context_tool(self):
        req = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "get_working_context",
                "arguments": {
                    "session_id": "sess-beta",
                    "item_id": "ctx-1",
                    "add_content": "Current architectural contract",
                    "tokens": 4,
                    "salience": 0.9,
                },
            },
        }
        res = self.server.handle_request(req)
        self.assertIn("result", res)
        struct = res["result"]["structured"]
        self.assertEqual(struct["session_id"], "sess-beta")
        self.assertEqual(struct["current_tokens"], 4)
        self.assertIn("Current architectural contract", struct["packed_context"])

    def test_reinforce_procedure_tool(self):
        req = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "reinforce_procedure",
                "arguments": {"name": "run_migrations", "success": True},
            },
        }
        res = self.server.handle_request(req)
        self.assertIn("result", res)
        struct = res["result"]["structured"]
        self.assertEqual(struct["status"], "reinforced")
        self.assertEqual(struct["skill"]["success_count"], 1)

    def test_unknown_method_error(self):
        req = {"jsonrpc": "2.0", "id": 99, "method": "unknown/method", "params": {}}
        res = self.server.handle_request(req)
        self.assertIn("error", res)
        self.assertEqual(res["error"]["code"], -32601)


if __name__ == "__main__":
    unittest.main()
