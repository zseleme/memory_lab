---
id: T-20261012-core-working
title: "Implement working memory buffer and procedural reinforcement"
status: ready
format_version: 3
profile: standard
effort: S
budget_iterations: 15
agent: zaiden
parent: cvg/swimlanes/core/leg-03-working.md
depends_on:
  - T-20261012-core-storage
  - T-20261012-core-semantic
supersedes: (none)

touches_paths: []
creates_paths:
  - memory_lab/cognitive/working.py
  - tests/test_cognitive.py
source_note: "cvg/swimlanes/core/leg-03-working.md"
created: 2026-10-12T20:16:32Z
tags: [core, working, procedural, token-budget]
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
signed_off_at: 2026-10-12T20:25:24Z
accepted: false
accepted_by: (none)
accepted_at: (none)
evidence_refs: []
signed_off_sig: hmac-sha256-v3:3d32e54d:cc68b2366ea9a83c11fc983d9b246e63c5b69a014c4c3ba462283c93fb2cb14e
---

# "Implement working memory buffer and procedural reinforcement"

> **Why:** Bound working memory context size under a strict 4000-token ceiling and maintain procedural skill reinforcement with recency decay.

---

## Goal

Provide WorkingMemoryBuffer to pack salience-ranked context up to a strict 4000 token limit with eviction, and ProceduralStore to track and reinforce reusable operational skills under power-law practice dynamics.

---

## Context

Decomposed from `cvg/swimlanes/core/leg-03-working.md` and R-4 / R-5 in `cvg/docs/tech-spec/memory-lab.md`. Addresses objection OBJ-002 from Pass 4 consensus log.

---

## Behavior

- **B-1** — GIVEN working memory items with token counts WHEN pushed into WorkingMemoryBuffer exceeding 4000 tokens THEN oldest and lowest-salience items are evicted until total <= 4000 tokens.
- **B-2** — GIVEN a procedural skill WHEN reinforced with execution outcome THEN success count increments and base-level activation updates according to power law of practice.

---

## Success Criteria

Each criterion is a runnable bash function returning 0 (pass) or non-zero (fail).

```bash
# eval-1: verify working memory token budget ceiling and eviction
eval_1() {
  python3 -c "from memory_lab.cognitive.working import WorkingMemoryBuffer; b = WorkingMemoryBuffer(max_tokens=4000); b.add_item('ctx-1', 'x'*1000, tokens=1000, salience=0.5); b.add_item('ctx-2', 'y'*3500, tokens=3500, salience=0.9); assert b.current_tokens <= 4000; assert 'ctx-2' in [i.item_id for i in b.get_active_items()]"
}

# eval-2: verify procedural skill reinforcement
eval_2() {
  python3 -c "from memory_lab.cognitive.working import ProceduralStore; s = ProceduralStore(':memory:'); s.register_skill('compile_code', 'steps'); s.reinforce('compile_code', success=True); assert s.get_skill('compile_code')['success_count'] == 1"
}

# eval-3: run cognitive unit test suite
eval_3() {
  python3 -m unittest tests/test_cognitive.py
}
```

---

## Validation Card

```yaml
success_criteria:
  - id: eval_1
    description: verify working memory token budget ceiling and eviction
    runnable: bash
    check_type: deterministic
    verifies: [B-1]
    terminal: true
    expected_duration_sec: 2
  - id: eval_2
    description: verify procedural skill reinforcement
    runnable: bash
    check_type: deterministic
    verifies: [B-2]
    terminal: true
    expected_duration_sec: 2
  - id: eval_3
    description: run cognitive unit test suite
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

1. **Git revert** — `git checkout -- memory_lab/cognitive/working.py tests/test_cognitive.py`
2. **File restore** — discard any scratch files
3. **State reset** — update task status to `parked` and record `blocked_reason`

(none — this task is additive with no destructive external changes)

---

## Observability Hooks

What to watch during execution and after deployment:

- **Expected duration:** 15s
- **Key metric:** working memory token ceiling <= 4000 tokens
- **Alert condition:** token budget overrun or negative token count
- **Log tail:** stderr on eviction events

---

## Anti-Patterns

- **Don't exceed 4000 token limit under any circumstance** — Working memory must strictly bound prompt size to protect LLM context windows.
- **Don't evict high-salience items before low-salience items** — Eviction policy must prioritize keeping items with higher salience score.
- **Don't ignore decay** — Procedural skills without usage over time must exhibit decay in activation score.

---

## Do-Not-Touch

Files the executor MUST NOT modify:

- cvg/
- .cvg/

---

## Open Questions

Things the executor should resolve DURING build, not assume:

(none — this task is fully specified)
