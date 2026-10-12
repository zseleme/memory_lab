---
id: T-20261012-ui-canvas-graph
title: "Implement Amber Cascades canvas simulation and semantic graph explorer"
status: ready
format_version: 3
profile: standard
effort: S
budget_iterations: 15
agent: zaiden
parent: cvg/swimlanes/ui/leg-02-graph-explorer.md
depends_on:
  - T-20261012-ui-dashboard
supersedes: (none)

touches_paths: []
creates_paths:
  - frontend/src/components/AmberCascades.tsx
  - frontend/src/components/GraphExplorer.tsx
source_note: "cvg/swimlanes/ui/leg-02-graph-explorer.md"
created: 2026-10-12T20:16:32Z
tags: [ui, canvas, particle, graph-explorer, amber-cascades]
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
signed_off_at: 2026-10-12T20:26:13Z
accepted: false
accepted_by: (none)
accepted_at: (none)
evidence_refs: []
signed_off_sig: hmac-sha256-v3:3d32e54d:1bb255ee16ed64c93af247977ac9ce6bfeb9538f841eda636fc53c5108d34da3
---

# "Implement Amber Cascades canvas simulation and semantic graph explorer"

> **Why:** Provide the mesmerizing visual centerpieces of Memory Lab: the Amber Cascades canvas particle simulation background and the interactive semantic association graph explorer.

---

## Goal

Implement the AmberCascades canvas component animating fluid amber particle trails at 60 FPS, and GraphExplorer displaying associative memory networks with spreading activation energy glow effects.

---

## Context

Decomposed from `cvg/swimlanes/ui/leg-02-graph-explorer.md` and R-8 in `cvg/docs/tech-spec/memory-lab.md` and ADR-0004 (`cvg/docs/adrs/0004-web-dashboard-inspection-surface.md`).

---

## Behavior

- **B-1** — GIVEN the Amber Cascades canvas component WHEN mounted in dashboard THEN 60 FPS requestAnimationFrame particle simulation renders cascading golden-amber particles with depth and velocity.
- **B-2** — GIVEN semantic nodes and associative edges WHEN viewed in GraphExplorer THEN interactive visualizer renders nodes with spreading activation energy glowing animations.

---

## Success Criteria

Each criterion is a runnable bash function returning 0 (pass) or non-zero (fail).

```bash
# eval-1: verify AmberCascades and GraphExplorer source components exist
eval_1() {
  test -f frontend/src/components/AmberCascades.tsx && test -f frontend/src/components/GraphExplorer.tsx
}

# eval-2: verify AmberCascades canvas animation loop implementation
eval_2() {
  python3 -c "content = open('frontend/src/components/AmberCascades.tsx', encoding='utf-8').read(); assert 'requestAnimationFrame' in content or 'canvas' in content"
}

# eval-3: verify GraphExplorer node visualization and activation energy
eval_3() {
  python3 -c "content = open('frontend/src/components/GraphExplorer.tsx', encoding='utf-8').read(); assert 'activation' in content.lower() or 'node' in content.lower()"
}
```

---

## Validation Card

```yaml
success_criteria:
  - id: eval_1
    description: verify AmberCascades and GraphExplorer source components exist
    runnable: bash
    check_type: deterministic
    verifies: [B-1]
    terminal: true
    expected_duration_sec: 2
  - id: eval_2
    description: verify AmberCascades canvas animation loop implementation
    runnable: bash
    check_type: deterministic
    verifies: [B-1]
    terminal: true
    expected_duration_sec: 2
  - id: eval_3
    description: verify GraphExplorer node visualization and activation energy
    runnable: bash
    check_type: deterministic
    verifies: [B-2]
    terminal: true
    expected_duration_sec: 2

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

1. **Git revert** — `git checkout -- frontend/src/components/`
2. **File restore** — discard any temporary assets
3. **State reset** — update task status to `parked` and record `blocked_reason`

(none — this task is additive with no destructive external changes)

---

## Observability Hooks

What to watch during execution and after deployment:

- **Expected duration:** 15s
- **Key metric:** smooth 60 FPS animation without dropped frame spikes
- **Alert condition:** WebGL/2D canvas context loss or CPU burn
- **Log tail:** browser console warnings

---

## Anti-Patterns

- **Don't block the React main thread with unthrottled canvas math** — Use efficient particle pool arrays and requestAnimationFrame.
- **Don't drop the luxury palette** — Particles must use refined amber/gold gradients (`#f59e0b`, `#d97706`, `#78350f`) against deep blacks.
- **Don't hardcode static graph nodes** — Accept reactive node/link datasets from the memory store.

---

## Do-Not-Touch

Files the executor MUST NOT modify:

- cvg/
- .cvg/

---

## Open Questions

Things the executor should resolve DURING build, not assume:

(none — this task is fully specified)
