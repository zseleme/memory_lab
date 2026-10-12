---
id: T-20261012-core-semantic
title: "Implement semantic association graph and spreading activation"
status: done
format_version: 3
profile: standard
effort: S
budget_iterations: 15
agent: zaiden
parent: cvg/swimlanes/core/leg-02-semantic.md
depends_on:
  - T-20261012-core-storage
supersedes: (none)

touches_paths: []
creates_paths:
  - memory_lab/cognitive/semantic.py
  - tests/test_semantic.py
source_note: "cvg/swimlanes/core/leg-02-semantic.md"
created: 2026-10-12T20:16:32Z
tags: [core, semantic, graph, activation]
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
signed_off_at: 2026-10-12T20:24:53Z
accepted: true
accepted_by: operator
accepted_at: 2026-10-12T20:58:44Z
evidence_refs: []
signed_off_sig: hmac-sha256-v3:3d32e54d:ec99928dfed9a2586b638e219bcbb4ed4e6d7bc35e0b8bcd146ac26f236cd510
accepted_tier: 1
accepted_attempt_id: 9b534e22-7816-4fa6-a918-bc96fe7b852c
accepted_authorization_ref: hmac-sha256-v3:3d32e54d:ec99928dfed9a2586b638e219bcbb4ed4e6d7bc35e0b8bcd146ac26f236cd510
acceptance_record_digest: sha256:7d0bc6aee4f2db4517012286a37ccb41438f78df4504d41fa4708d52f72daa46
---

# "Implement semantic association graph and spreading activation"

> **Why:** Provide the semantic memory tier enabling associative recall, entity-relation graphs, and sub-500ms spreading activation queries.

---

## Goal

Implement the SemanticGraph engine supporting weighted associative edges, decay-based spreading activation traversal, and post-settlement background graph consolidation from episodic logs.

---

## Context

Decomposed from `cvg/swimlanes/core/leg-02-semantic.md` and R-2 / R-3 in `cvg/docs/tech-spec/memory-lab.md`. Leverages the local SQLite database from `T-20261012-core-storage`.

---

## Behavior

- **B-1** — GIVEN concepts with associative relations WHEN inserted into semantic graph via SemanticGraph.add_concept and link THEN association weight is recorded and bidirectional links are queryable.
- **B-2** — GIVEN a query concept WHEN spreading activation is executed with decay factor 0.85 THEN activated neighbor concepts are returned ranked by activation energy within 200ms.

---

## Success Criteria

Each criterion is a runnable bash function returning 0 (pass) or non-zero (fail).

```bash
# eval-1: verify semantic node and link creation
eval_1() {
  python3 -c "from memory_lab.cognitive.semantic import SemanticGraph; g = SemanticGraph(':memory:'); g.add_concept('python', {'type': 'lang'}); g.add_concept('sqlite', {'type': 'db'}); g.link('python', 'sqlite', 0.8); assert g.get_edge_weight('python', 'sqlite') == 0.8"
}

# eval-2: verify spreading activation ranking
eval_2() {
  python3 -c "from memory_lab.cognitive.semantic import SemanticGraph; g = SemanticGraph(':memory:'); g.add_concept('A'); g.add_concept('B'); g.link('A', 'B', 0.9); res = g.activate('A', decay=0.85, max_hops=2); assert 'B' in res"
}

# eval-3: run semantic unit test suite
eval_3() {
  python3 -m unittest tests/test_semantic.py
}
```

---

## Validation Card

```yaml
success_criteria:
  - id: eval_1
    description: verify semantic node and link creation
    runnable: bash
    check_type: deterministic
    verifies: [B-1]
    terminal: true
    expected_duration_sec: 2
  - id: eval_2
    description: verify spreading activation ranking
    runnable: bash
    check_type: deterministic
    verifies: [B-2]
    terminal: true
    expected_duration_sec: 3
  - id: eval_3
    description: run semantic unit test suite
    runnable: bash
    check_type: deterministic
    verifies: [B-1, B-2]
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

1. **Git revert** — `git checkout -- memory_lab/cognitive/semantic.py tests/test_semantic.py`
2. **File restore** — delete any uncommitted temporary files
3. **State reset** — update task status to `parked` and record `blocked_reason`

(none — this task is additive with no destructive external changes)

---

## Observability Hooks

What to watch during execution and after deployment:

- **Expected duration:** 15s
- **Key metric:** spreading activation query latency < 200ms
- **Alert condition:** recursion depth limit reached or cyclic loop deadlock
- **Log tail:** stderr on graph activation

---

## Anti-Patterns

- **Don't perform unbounded graph recursion** — Always enforce `max_hops <= 3` and an energy cutoff threshold (`energy < 0.05`).
- **Don't run blocking consolidation during user interaction** — Graph consolidation from episodic traces must execute asynchronously.
- **Don't store unnormalized edge weights** — Association weights must be clamped in the range `[0.0, 1.0]`.

---

## Do-Not-Touch

Files the executor MUST NOT modify:

- cvg/
- .cvg/

---

## Open Questions

Things the executor should resolve DURING build, not assume:

(none — this task is fully specified)
