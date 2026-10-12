"""Converge pre- and post-execution lifecycle memory hooks."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Union

from memory_lab.interfaces.mcp_server import MCPServer, create_mcp_server
from memory_lab.storage.engine import StorageEngine


class MemoryHook:
    """Lifecycle hook for Converge agent workflows to inject and persist cognitive memory."""

    def __init__(
        self,
        server: Optional[MCPServer] = None,
        db_path: Union[str, StorageEngine] = ":memory:",
    ) -> None:
        if server is not None:
            self.server = server
        else:
            self.server = create_mcp_server(db_path)

    def pre_execution_context(
        self,
        session_id: str,
        query: Optional[str] = None,
    ) -> str:
        """Generate markdown memory context before agent dispatch."""
        buf = self.server.get_working_buffer(session_id)
        active_items = buf.get_active_items()

        # If semantic query provided, perform spreading activation lookup
        semantic_hints = []
        if query:
            try:
                activations = self.server.semantic.activate(
                    seeds=query, decay=0.85, max_hops=2
                )
                for concept, energy in list(activations.items())[:5]:
                    if concept != query:
                        semantic_hints.append(f"- **{concept}** (association energy: {energy:.2f})")
            except Exception:
                pass

        lines = [
            "### [Memory Lab Context]",
            f"- **Session:** `{session_id}`",
            f"- **Working Tokens:** {buf.current_tokens} / {buf.max_tokens}",
        ]

        if active_items:
            lines.append("\n#### Active Working Memory")
            for item in active_items:
                lines.append(f"> **[{item.item_id}]** (salience: {item.salience:.2f})\n> {item.content}")

        if semantic_hints:
            lines.append("\n#### Associative Concepts")
            lines.extend(semantic_hints)

        # Include top procedural skills
        skills = self.server.procedural.list_skills()[:3]
        if skills:
            lines.append("\n#### Available Reusable Skills")
            for sk in skills:
                lines.append(
                    f"- `{sk['name']}`: base activation {sk['base_activation']:.2f} (successes: {sk['success_count']})"
                )

        return "\n".join(lines)

    def post_execution_record(
        self,
        session_id: str,
        actor: str,
        outcome_summary: str,
        salience: float = 0.5,
        tags: str = "",
        success: bool = True,
        skill_name: Optional[str] = None,
    ) -> str:
        """Persist execution outcome as an episodic memory trace and reinforce skills."""
        res = self.server.call_tool(
            "remember_episodic",
            {
                "session_id": session_id,
                "actor": actor,
                "content": outcome_summary,
                "salience": salience,
                "tags": tags,
            },
        )
        episode_id = res["episode_id"]

        if skill_name:
            try:
                self.server.call_tool(
                    "reinforce_procedure",
                    {"name": skill_name, "success": success},
                )
            except Exception:
                pass

        return episode_id

    def close(self) -> None:
        """Close backing server resources."""
        self.server.close()
