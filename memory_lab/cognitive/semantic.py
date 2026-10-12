"""Semantic memory association graph with spreading activation traversal."""

from __future__ import annotations

import json
import sqlite3
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple, Union

from memory_lab.storage.engine import StorageEngine


class SemanticGraph:
    """Associative knowledge graph backed by SQLite storage."""

    def __init__(self, db_path: Union[str, StorageEngine] = ":memory:"):
        if isinstance(db_path, StorageEngine):
            self.engine = db_path
        else:
            self.engine = StorageEngine(db_path)
            self.engine.init_db()

    @property
    def conn(self) -> sqlite3.Connection:
        """Return the underlying SQLite database connection."""
        return self.engine._conn

    def add_concept(self, name: str, properties: Optional[Dict[str, Any]] = None) -> str:
        """Add or update a concept node in the semantic graph."""
        props_str = json.dumps(properties or {})
        now = time.time()
        cursor = self.conn.cursor()

        cursor.execute("SELECT id FROM semantic_nodes WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            node_id = row[0]
            cursor.execute(
                "UPDATE semantic_nodes SET properties = ?, updated_at = ? WHERE id = ?",
                (props_str, now, node_id),
            )
        else:
            node_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO semantic_nodes (id, name, properties, activation, updated_at) VALUES (?, ?, ?, ?, ?)",
                (node_id, name, props_str, 1.0, now),
            )
        self.conn.commit()
        return node_id

    def get_concept(self, name: str) -> Optional[Dict[str, Any]]:
        """Retrieve concept details by name."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, name, properties, activation, updated_at FROM semantic_nodes WHERE name = ?",
            (name,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "name": row[1],
            "properties": json.loads(row[2]) if row[2] else {},
            "activation": row[3],
            "updated_at": row[4],
        }

    def link(
        self,
        source: str,
        target: str,
        weight: float = 0.5,
        bidirectional: bool = True,
    ) -> None:
        """Create or update an associative link between two concepts."""
        src_node = self.get_concept(source)
        if not src_node:
            src_id = self.add_concept(source)
        else:
            src_id = src_node["id"]

        tgt_node = self.get_concept(target)
        if not tgt_node:
            tgt_id = self.add_concept(target)
        else:
            tgt_id = tgt_node["id"]

        now = time.time()
        cursor = self.conn.cursor()

        # Insert or replace forward edge
        edge_id_1 = str(uuid.uuid4())
        cursor.execute(
            """INSERT INTO semantic_edges (id, source_id, target_id, weight, updated_at)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(source_id, target_id) DO UPDATE SET weight = excluded.weight, updated_at = excluded.updated_at""",
            (edge_id_1, src_id, tgt_id, weight, now),
        )

        if bidirectional and src_id != tgt_id:
            edge_id_2 = str(uuid.uuid4())
            cursor.execute(
                """INSERT INTO semantic_edges (id, source_id, target_id, weight, updated_at)
                   VALUES (?, ?, ?, ?, ?)
                   ON CONFLICT(source_id, target_id) DO UPDATE SET weight = excluded.weight, updated_at = excluded.updated_at""",
                (edge_id_2, tgt_id, src_id, weight, now),
            )

        self.conn.commit()

    def get_edge_weight(self, source: str, target: str) -> Optional[float]:
        """Get the associative link weight between source and target."""
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT e.weight FROM semantic_edges e
               JOIN semantic_nodes s ON e.source_id = s.id
               JOIN semantic_nodes t ON e.target_id = t.id
               WHERE s.name = ? AND t.name = ?""",
            (source, target),
        )
        row = cursor.fetchone()
        return float(row[0]) if row else None

    def get_neighbors(self, concept: str) -> List[Dict[str, Any]]:
        """Retrieve all neighbor concepts and their edge weights."""
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT t.name, e.weight, t.properties FROM semantic_edges e
               JOIN semantic_nodes s ON e.source_id = s.id
               JOIN semantic_nodes t ON e.target_id = t.id
               WHERE s.name = ?
               ORDER BY e.weight DESC""",
            (concept,),
        )
        results = []
        for row in cursor.fetchall():
            results.append({
                "name": row[0],
                "weight": float(row[1]),
                "properties": json.loads(row[2]) if row[2] else {},
            })
        return results

    def activate(
        self,
        seeds: Union[str, List[str]],
        decay: float = 0.85,
        max_hops: int = 2,
        threshold: float = 0.01,
    ) -> Dict[str, float]:
        """Execute spreading activation starting from seed concept(s).
        
        Returns a dictionary mapping activated concept names to energy levels,
        ranked in descending order of energy.
        """
        if isinstance(seeds, str):
            seeds = [seeds]

        current_frontier: Dict[str, float] = {s: 1.0 for s in seeds}
        accumulated_energy: Dict[str, float] = {s: 1.0 for s in seeds}

        for _ in range(max_hops):
            next_frontier: Dict[str, float] = {}
            for node, energy in current_frontier.items():
                if energy < threshold:
                    continue
                neighbors = self.get_neighbors(node)
                for nb in neighbors:
                    nb_name = nb["name"]
                    spread_energy = energy * nb["weight"] * decay
                    if spread_energy >= threshold:
                        next_frontier[nb_name] = max(
                            next_frontier.get(nb_name, 0.0), spread_energy
                        )
                        accumulated_energy[nb_name] = (
                            accumulated_energy.get(nb_name, 0.0) + spread_energy
                        )
            current_frontier = next_frontier
            if not current_frontier:
                break

        # Return ordered dict by activation energy
        sorted_items = sorted(
            accumulated_energy.items(), key=lambda kv: kv[1], reverse=True
        )
        return dict(sorted_items)

    def get_graph_snapshot(self) -> Dict[str, Any]:
        """Return the complete graph state formatted for visualization."""
        cursor = self.conn.cursor()

        cursor.execute("SELECT id, name, properties, activation FROM semantic_nodes")
        nodes = [
            {
                "id": r[0],
                "name": r[1],
                "properties": json.loads(r[2]) if r[2] else {},
                "activation": r[3],
            }
            for r in cursor.fetchall()
        ]

        cursor.execute(
            """SELECT e.id, s.name, t.name, e.weight
               FROM semantic_edges e
               JOIN semantic_nodes s ON e.source_id = s.id
               JOIN semantic_nodes t ON e.target_id = t.id"""
        )
        edges = [
            {"id": r[0], "source": r[1], "target": r[2], "weight": r[3]}
            for r in cursor.fetchall()
        ]

        return {"nodes": nodes, "edges": edges}

    def close(self) -> None:
        """Close backing storage engine."""
        self.engine.close()
