---
id: T-20261012-core-storage
title: "Implement SQLite episodic storage engine and database schema"
status: ready
format_version: 3
profile: standard
effort: S
budget_iterations: 15
agent: zaiden
parent: cvg/swimlanes/core/leg-01-storage.md
depends_on: []
supersedes: (none)

touches_paths: []
creates_paths:
  - memory_lab/storage/
  - tests/test_storage.py
source_note: "cvg/swimlanes/core/leg-01-storage.md"
created: 2026-10-12T20:15:08Z
tags: [core, storage, sqlite, episodic]
owner: zaiden
priority: P1
severity: feature
due_date: 2026-10-31
precondition: (none)
blocked_reason: (none)
security_class: (none)
source_action_item: (none)
tracker_ref: (none)
execution_backend: any
signed_off: true
signed_off_by: operator
signed_off_at: 2026-10-12T20:37:30Z
accepted: false
accepted_by: (none)
accepted_at: (none)
evidence_refs: []
signed_off_sig: hmac-sha256-v3:3d32e54d:bf663dc1cc2bb8f3343f961d88313c3a31858431a2cb4deeaf9a351177fe6694
---

# "Implement SQLite episodic storage engine and database schema"

> **Why:** Establish the local-first embedded SQLite persistence layer with WAL journaling, FTS5 full-text indexing, and structured schema for episodic memory storage.

---

## Goal

Provide a robust StorageEngine class backed by SQLite with WAL mode enabled that creates necessary tables (episodic_memories, semantic_nodes, semantic_edges, working_memory, procedural_skills, fts_episodes) and supports fast (<100ms) transactional ingestion and retrieval of task execution episodes.

---

## Context

For the architectural foundation, see `cvg/docs/adrs/0001-local-sqlite-storage-engine.md` and `cvg/swimlanes/core/leg-01-storage.md`. This task implements the foundational persistence layer without requiring external services or cloud APIs.

---

## Behavior

- **B-1** — GIVEN an episodic memory payload with actor, session_id, and content WHEN recorded via StorageEngine.record_episode THEN the episode is committed to SQLite with WAL enabled within 100ms and returns an assigned UUID.
- **B-2** — GIVEN stored episodic records with tags and sessions WHEN queried via StorageEngine.get_episodes_by_session THEN matching episodes are returned in descending chronological order with salience scores.

---

## Success Criteria

Each criterion is a runnable bash function returning 0 (pass) or non-zero (fail).

```bash
# eval-1: verify storage schema migration and tables
eval_1() {
  python3 -c "from memory_lab.storage.engine import StorageEngine; e = StorageEngine(':memory:'); e.init_db(); assert 'episodic_memories' in e.get_tables()"
}

# eval-2: verify episodic insertion and retrieval latency
eval_2() {
  python3 -c "from memory_lab.storage.engine import StorageEngine; import time; e = StorageEngine(':memory:'); e.init_db(); t0 = time.time(); ep_id = e.record_episode('session-1', 'user', 'hello', 0.9); assert ep_id is not None; assert (time.time() - t0) < 0.1; res = e.get_episodes_by_session('session-1'); assert len(res) == 1"
}

# eval-3: run storage unit test suite
eval_3() {
  python3 -m unittest tests/test_storage.py
}
```

---

## Validation Card

```yaml
success_criteria:
  - id: eval_1
    description: verify storage schema migration and tables
    runnable: bash
    check_type: deterministic
    verifies: [B-1]
    terminal: true
    expected_duration_sec: 2
  - id: eval_2
    description: verify episodic insertion and retrieval latency
    runnable: bash
    check_type: deterministic
    verifies: [B-1, B-2]
    terminal: true
    expected_duration_sec: 2
  - id: eval_3
    description: run storage unit test suite
    runnable: bash
    check_type: deterministic
    verifies: [B-2]
    terminal: true
    expected_duration_sec: 5

retry_policy:
  max_iterations: 15
  circuit_breaker_no_progress: 3
  on_terminal_failure: park_with_context

agent_contract:
  version: 2
  read: [intent, behavior, contract, guardrails, operations]
  produce:
    - code
    - docs
    - config
    - tests
  required_tools: [git, bash]
  timeout_minutes: 30
  sandbox_type: host
  output_artifacts: []
  mcp_dependencies: []
  emit:
    - pass
    - fail
    - retry_with_reason
    - parked_with_context
  backend_metadata: {}
```

---

## Exit Check

```bash
eval_1 && eval_2 && eval_3
```

---

## Rollback Plan

If execution fails mid-task, revert to the pre-task state:

1. **Git revert** — `git checkout -- memory_lab/storage/ tests/test_storage.py`
2. **File restore** — remove any uncommitted database or artifact files
3. **State reset** — update task status to `parked` and record `blocked_reason`

(none — this task is additive with no destructive external changes)

---

## Observability Hooks

What to watch during execution and after deployment:

- **Expected duration:** 15s
- **Key metric:** write latency < 100ms
- **Alert condition:** sqlite operational error or lock timeout
- **Log tail:** stderr on db init

---

## Anti-Patterns

- **Don't use external database servers** — SQLite local WAL is the architectural requirement (ADR-0001). Use embedded sqlite3 standard library.
- **Don't omit WAL mode pragma** — Standard rollback journal causes read/write lock contention. Always execute PRAGMA journal_mode=WAL on connection.
- **Don't leave database connections unclosed** — Open connection leaks cause file locks on Windows. Always use context managers or explicit close.

---

## Do-Not-Touch

Files the executor MUST NOT modify:

- cvg/
- .cvg/

---

## Open Questions

Things the executor should resolve DURING build, not assume:

(none — this task is fully specified)
