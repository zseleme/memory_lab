"""Model Context Protocol (MCP) server providing cognitive memory tools over stdio/JSON-RPC."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Union

from memory_lab.cognitive.semantic import SemanticGraph
from memory_lab.cognitive.working import ProceduralStore, WorkingMemoryBuffer
from memory_lab.storage.engine import StorageEngine


@dataclass
class MCPTool:
    """Definition of an MCP tool capability."""

    name: str
    description: str
    input_schema: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema,
        }


class MCPServer:
    """MCP server instance orchestrating the 4 memory tiers."""

    def __init__(self, db_path: Union[str, StorageEngine] = ":memory:") -> None:
        if isinstance(db_path, StorageEngine):
            self.storage = db_path
        else:
            self.storage = StorageEngine(db_path)
            self.storage.init_db()

        self.semantic = SemanticGraph(self.storage)
        self.procedural = ProceduralStore(self.storage)
        self.working_buffers: Dict[str, WorkingMemoryBuffer] = {}

    def get_working_buffer(self, session_id: str) -> WorkingMemoryBuffer:
        if session_id not in self.working_buffers:
            self.working_buffers[session_id] = WorkingMemoryBuffer(max_tokens=4000)
        return self.working_buffers[session_id]

    def list_tools(self) -> List[MCPTool]:
        """Return available MCP tool definitions."""
        return [
            MCPTool(
                name="remember_episodic",
                description="Record an episodic execution trace or observation into durable memory.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string"},
                        "actor": {"type": "string"},
                        "content": {"type": "string"},
                        "salience": {"type": "number", "default": 0.5},
                        "tags": {"type": "string", "default": ""},
                    },
                    "required": ["session_id", "actor", "content"],
                },
            ),
            MCPTool(
                name="search_semantic",
                description="Query the associative knowledge graph using spreading activation.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "concept": {"type": "string"},
                        "decay": {"type": "number", "default": 0.85},
                        "max_hops": {"type": "integer", "default": 2},
                    },
                    "required": ["concept"],
                },
            ),
            MCPTool(
                name="get_working_context",
                description="Retrieve salience-ranked context packed within the 4000-token ceiling.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string"},
                        "item_id": {"type": "string"},
                        "add_content": {"type": "string"},
                        "tokens": {"type": "integer"},
                        "salience": {"type": "number", "default": 0.5},
                    },
                    "required": ["session_id"],
                },
            ),
            MCPTool(
                name="reinforce_procedure",
                description="Update procedural skill base activation according to power law of practice.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "success": {"type": "boolean", "default": True},
                    },
                    "required": ["name"],
                },
            ),
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute the named tool with provided arguments."""
        if name == "remember_episodic":
            session_id = arguments["session_id"]
            actor = arguments.get("actor", "agent")
            content = arguments["content"]
            salience = float(arguments.get("salience", 0.5))
            tags = arguments.get("tags", "")
            ep_id = self.storage.record_episode(
                session_id=session_id,
                actor=actor,
                content=content,
                salience=salience,
                tags=tags,
            )
            # Automatically mirror to working memory
            buf = self.get_working_buffer(session_id)
            buf.add_item(
                item_id=ep_id,
                content=f"[{actor}] {content}",
                tokens=len(content.split()),
                salience=salience,
            )
            return {"status": "recorded", "episode_id": ep_id}

        elif name == "search_semantic":
            concept = arguments["concept"]
            decay = float(arguments.get("decay", 0.85))
            max_hops = int(arguments.get("max_hops", 2))
            activations = self.semantic.activate(
                seeds=concept, decay=decay, max_hops=max_hops
            )
            return {"concept": concept, "activations": activations}

        elif name == "get_working_context":
            session_id = arguments["session_id"]
            buf = self.get_working_buffer(session_id)

            if "add_content" in arguments and "item_id" in arguments:
                item_id = arguments["item_id"]
                content = arguments["add_content"]
                tokens = int(arguments.get("tokens", len(content.split())))
                salience = float(arguments.get("salience", 0.5))
                buf.add_item(item_id, content, tokens=tokens, salience=salience)

            items = [
                {
                    "item_id": i.item_id,
                    "tokens": i.tokens,
                    "salience": i.salience,
                    "content": i.content,
                }
                for i in buf.get_active_items()
            ]
            return {
                "session_id": session_id,
                "current_tokens": buf.current_tokens,
                "max_tokens": buf.max_tokens,
                "packed_context": buf.pack_context(),
                "items": items,
            }

        elif name == "reinforce_procedure":
            skill_name = arguments["name"]
            success = bool(arguments.get("success", True))
            # Auto-register if not yet present
            if not self.procedural.get_skill(skill_name):
                self.procedural.register_skill(skill_name, "default_steps")
            self.procedural.reinforce(skill_name, success=success)
            skill = self.procedural.get_skill(skill_name)
            return {"status": "reinforced", "skill": skill}

        raise ValueError(f"Unknown tool: {name}")

    def handle_request(self, req: Dict[str, Any]) -> Dict[str, Any]:
        """Process a standard JSON-RPC 2.0 request."""
        req_id = req.get("id")
        method = req.get("method", "")

        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "memory-lab", "version": "0.1.0"},
                        "capabilities": {"tools": {}},
                    },
                }
            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": [t.to_dict() for t in self.list_tools()]},
                }
            elif method == "tools/call":
                params = req.get("params", {})
                name = params.get("name", "")
                args = params.get("arguments", {})
                tool_result = self.call_tool(name, args)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {"type": "text", "text": json.dumps(tool_result)}
                        ],
                        "structured": tool_result,
                    },
                }
            elif method == "ping":
                return {"jsonrpc": "2.0", "id": req_id, "result": {}}
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method '{method}' not found",
                    },
                }
        except Exception as exc:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32000, "message": str(exc)},
            }

    def close(self) -> None:
        """Close backing storage resources."""
        self.storage.close()


_GLOBAL_SERVER: Optional[MCPServer] = None


def create_mcp_server(db_path: str = ":memory:") -> MCPServer:
    """Factory creating an MCPServer instance."""
    return MCPServer(db_path)


def handle_jsonrpc_request(
    request: Dict[str, Any], server: Optional[MCPServer] = None
) -> Dict[str, Any]:
    """Top-level JSON-RPC request dispatcher."""
    global _GLOBAL_SERVER
    if server is None:
        if _GLOBAL_SERVER is None:
            _GLOBAL_SERVER = create_mcp_server()
        server = _GLOBAL_SERVER
    return server.handle_request(request)


def run_stdio_server(db_path: str = "memory_lab.db") -> None:
    """Run interactive JSON-RPC server listening on standard input."""
    server = create_mcp_server(db_path)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = server.handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as err:
            err_res = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {err}"},
            }
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    run_stdio_server()
