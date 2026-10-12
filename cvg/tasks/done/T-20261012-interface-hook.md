---
id: T-20261012-interface-hook
title: "Implement Converge pre-and-post execution memory hooks"
status: done
format_version: 3
profile: standard
effort: S
budget_iterations: 15
agent: zaiden
parent: cvg/swimlanes/interface/leg-02-converge-hook.md
depends_on:
  - T-20261012-interface-mcp
supersedes: (none)

touches_paths: []
creates_paths:
  - memory_lab/interfaces/hook.py
  - tests/test_hook.py
source_note: "cvg/swimlanes/interface/leg-02-converge-hook.md"
created: 2026-10-12T20:16:32Z
tags: [interface, hook, converge, lifecycle]
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
signed_off_at: 2026-10-12T20:25:40Z
accepted: true
accepted_by: operator
accepted_at: 2026-10-12T21:11:11Z
evidence_refs: []
signed_off_sig: hmac-sha256-v3:3d32e54d:cc5dde3d245d1f1ddc989ee19dfac974434320d69806d7bc2ecfab170080e1f8
accepted_tier: 1
accepted_attempt_id: 197e617f-2d8e-4835-b776-09cacab62bff
accepted_authorization_ref: hmac-sha256-v3:3d32e54d:cc5dde3d245d1f1ddc989ee19dfac974434320d69806d7bc2ecfab170080e1f8
acceptance_record_digest: sha256:7c876853af74e54cf5b915e1e339e37637845113865b026659065b49651fa69a
---

# "Implement Converge pre-and-post execution memory hooks"

> **Why:** Seamlessly connect Memory Lab to Converge and agent loops by injecting cognitive working context before agent dispatch and recording episodic traces upon completion.

---

## Goal

Provide MemoryHook class and CLI command hooks to perform pre-execution memory retrieval (injecting into agent context) and post-execution episodic recording into the SQLite storage engine.

---

## Context

Decomposed from `cvg/swimlanes/interface/leg-02-converge-hook.md` and R-7 in `cvg/docs/tech-spec/memory-lab.md`. Integrates with Converge descent passes and autonomous agent execution loops.

---

## Behavior

- **B-1** — GIVEN an agent invocation trigger WHEN pre-execution hook is invoked THEN working memory context is retrieved and emitted as markdown context.
- **B-2** — GIVEN an agent completion trigger with command outcome WHEN post-execution hook is invoked THEN execution trace is committed as an episodic record with calculated salience.

---

## Success Criteria

Each criterion is a runnable bash function returning 0 (pass) or non-zero (fail).

```bash
# eval-1: verify pre-execution context generation
eval_1() {
  python3 -c "from memory_lab.interfaces.hook import MemoryHook; h = MemoryHook(); ctx = h.pre_execution_context('session-test'); assert isinstance(ctx, str)"
}

# eval-2: verify post-execution trace commitment
eval_2() {
  python3 -c "from memory_lab.interfaces.hook import MemoryHook; h = MemoryHook(); res = h.post_execution_record('session-test', 'actor-1', 'task done', 0.85); assert res is not None"
}

# eval-3: run hook unit test suite
eval_3() {
  python3 -m unittest tests/test_hook.py
}
```

---

## Validation Card

```yaml
success_criteria:
  - id: eval_1
    description: verify pre-execution context generation
    runnable: bash
    check_type: deterministic
    verifies: [B-1]
    terminal: true
    expected_duration_sec: 2
  - id: eval_2
    description: verify post-execution trace commitment
    runnable: bash
    check_type: deterministic
    verifies: [B-2]
    terminal: true
    expected_duration_sec: 2
  - id: eval_3
    description: run hook unit test suite
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

1. **Git revert** — `git checkout -- memory_lab/interfaces/hook.py tests/test_hook.py`
2. **File restore** — delete uncommitted log or temp files
3. **State reset** — update task status to `parked` and record `blocked_reason`

(none — this task is additive with no destructive external changes)

---

## Observability Hooks

What to watch during execution and after deployment:

- **Expected duration:** 15s
- **Key metric:** hook dispatch overhead < 100ms
- **Alert condition:** storage lock contention or failed context injection
- **Log tail:** stderr on hook run

---

## Anti-Patterns

- **Don't crash agent execution on memory failure** — Hooks must fail open with a clean fallback so agent runs are not aborted if memory indexing fails.
- **Don't inject unformatted raw blobs** — Pre-execution context should be rendered into readable markdown blocks with memory tier citations.
- **Don't block the caller on long consolidation** — Heavy graph updates must be queued asynchronously.

---

## Do-Not-Touch

Files the executor MUST NOT modify:

- cvg/
- .cvg/

---

## Open Questions

Things the executor should resolve DURING build, not assume:

(none — this task is fully specified)
