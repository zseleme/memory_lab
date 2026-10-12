"""Working memory buffer with strict token ceiling and procedural skill store."""

from __future__ import annotations

import json
import math
import sqlite3
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from memory_lab.storage.engine import StorageEngine


@dataclass
class WorkingMemoryItem:
    """An atomic item stored in the active working memory buffer."""

    item_id: str
    content: str
    tokens: int
    salience: float = 0.5
    timestamp: float = 0.0


class WorkingMemoryBuffer:
    """Bounded working memory maintaining context under a strict token ceiling."""

    def __init__(self, max_tokens: int = 4000) -> None:
        self.max_tokens = max_tokens
        self._items: Dict[str, WorkingMemoryItem] = {}

    @property
    def current_tokens(self) -> int:
        """Total token footprint of all active items in the buffer."""
        return sum(item.tokens for item in self._items.values())

    def add_item(
        self,
        item_id: str,
        content: str,
        tokens: int,
        salience: float = 0.5,
    ) -> None:
        """Add or update an item, evicting lowest-salience items if ceiling is exceeded."""
        now = time.time()
        # Remove existing item with same id if present to recalculate tokens
        if item_id in self._items:
            del self._items[item_id]

        new_item = WorkingMemoryItem(
            item_id=item_id,
            content=content,
            tokens=tokens,
            salience=salience,
            timestamp=now,
        )

        # Evict until new item fits within max_tokens
        while self.current_tokens + tokens > self.max_tokens and self._items:
            # Pick lowest salience, break tie with oldest timestamp
            evict_id = min(
                self._items.keys(),
                key=lambda k: (self._items[k].salience, self._items[k].timestamp),
            )
            # If the item to evict has higher salience than the incoming item and buffer is full,
            # we should not evict high-salience items for lower-salience item if incoming cannot fit.
            if self._items[evict_id].salience > salience and self.current_tokens + tokens > self.max_tokens:
                if len(self._items) == 1 and self._items[evict_id].tokens >= tokens:
                    # Let incoming displace if salience is sufficient
                    pass
            del self._items[evict_id]

        if self.current_tokens + tokens <= self.max_tokens:
            self._items[item_id] = new_item

    def get_active_items(self) -> List[WorkingMemoryItem]:
        """Return all active items sorted by salience descending."""
        return sorted(self._items.values(), key=lambda i: i.salience, reverse=True)

    def pack_context(self) -> str:
        """Pack active items into a contiguous context string."""
        active = self.get_active_items()
        return "\n\n".join(item.content for item in active)

    def clear(self) -> None:
        """Empty the working memory buffer."""
        self._items.clear()


class ProceduralStore:
    """Procedural memory storing operational skills reinforced by practice."""

    def __init__(self, db_path: Union[str, StorageEngine] = ":memory:") -> None:
        if isinstance(db_path, StorageEngine):
            self.engine = db_path
        else:
            self.engine = StorageEngine(db_path)
            self.engine.init_db()

    @property
    def conn(self) -> sqlite3.Connection:
        """Return the underlying SQLite connection."""
        return self.engine._conn

    def register_skill(
        self,
        name: str,
        steps: Union[str, List[Any], Dict[str, Any]],
        base_activation: float = 1.0,
    ) -> str:
        """Register a reusable operational skill."""
        steps_str = json.dumps(steps) if not isinstance(steps, str) else steps
        skill_id = str(uuid.uuid4())
        now = time.time()
        cursor = self.conn.cursor()

        cursor.execute(
            """INSERT INTO procedural_skills (id, name, steps, success_count, failure_count, last_used, base_activation)
               VALUES (?, ?, ?, 0, 0, ?, ?)
               ON CONFLICT(name) DO UPDATE SET steps = excluded.steps, last_used = excluded.last_used""",
            (skill_id, name, steps_str, now, base_activation),
        )
        self.conn.commit()
        return skill_id

    def reinforce(self, name: str, success: bool = True) -> None:
        """Reinforce skill with execution outcome according to power law of practice."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, success_count, failure_count, base_activation FROM procedural_skills WHERE name = ?",
            (name,),
        )
        row = cursor.fetchone()
        if not row:
            raise KeyError(f"Skill '{name}' not found")

        skill_id, sc, fc, act = row[0], row[1], row[2], row[3]
        now = time.time()

        if success:
            sc += 1
            # ACT-R power law reinforcement: activation increases logarithmically with practice
            new_act = act + math.log1p(sc) * 0.2
        else:
            fc += 1
            new_act = max(0.1, act * 0.85)

        cursor.execute(
            """UPDATE procedural_skills
               SET success_count = ?, failure_count = ?, last_used = ?, base_activation = ?
               WHERE id = ?""",
            (sc, fc, now, new_act, skill_id),
        )
        self.conn.commit()

    def get_skill(self, name: str) -> Optional[Dict[str, Any]]:
        """Retrieve skill definition and activation metrics."""
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT id, name, steps, success_count, failure_count, last_used, base_activation
               FROM procedural_skills WHERE name = ?""",
            (name,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "name": row[1],
            "steps": row[2],
            "success_count": row[3],
            "failure_count": row[4],
            "last_used": row[5],
            "base_activation": row[6],
        }

    def list_skills(self) -> List[Dict[str, Any]]:
        """List all registered skills ranked by base activation."""
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT id, name, steps, success_count, failure_count, last_used, base_activation
               FROM procedural_skills ORDER BY base_activation DESC"""
        )
        return [
            {
                "id": r[0],
                "name": r[1],
                "steps": r[2],
                "success_count": r[3],
                "failure_count": r[4],
                "last_used": r[5],
                "base_activation": r[6],
            }
            for r in cursor.fetchall()
        ]

    def close(self) -> None:
        """Close backing storage engine."""
        self.engine.close()
