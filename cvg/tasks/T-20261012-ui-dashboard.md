---
id: T-20261012-ui-dashboard
title: "Implement React Vite dashboard shell and dark luxury aesthetic"
status: ready
format_version: 3
profile: standard
effort: S
budget_iterations: 15
agent: zaiden
parent: cvg/swimlanes/ui/leg-01-dashboard-shell.md
depends_on: []
supersedes: (none)

touches_paths: []
creates_paths:
  - frontend/src/App.tsx
  - frontend/package.json
source_note: "cvg/swimlanes/ui/leg-01-dashboard-shell.md"
created: 2026-10-12T20:16:32Z
tags: [ui, react, vite, luxury, typography]
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
signed_off_at: 2026-10-12T20:26:29Z
accepted: false
accepted_by: (none)
accepted_at: (none)
evidence_refs: []
signed_off_sig: hmac-sha256-v3:3d32e54d:22d8e17eac3a09d9a5d3747f73a79f7a80e9f1c4b9770b617858b0284d0f4f7a
---

# "Implement React Vite dashboard shell and dark luxury aesthetic"

> **Why:** Establish the high-end inspection dashboard replicating the Memory Lab aesthetic with #0a0a0a background, EB Garamond serif accents, GeistMono code tables, and SVG LiquidGlass button effects.

---

## Goal

Scaffold and implement the Vite + React frontend dashboard featuring luxury dark layout, 4-tier cognitive memory overview panels, and SVG displacement interactive controls.

---

## Context

Decomposed from `cvg/swimlanes/ui/leg-01-dashboard-shell.md` and R-8 in `cvg/docs/tech-spec/memory-lab.md` and ADR-0004 (`cvg/docs/adrs/0004-web-dashboard-inspection-surface.md`).

---

## Behavior

- **B-1** — GIVEN the frontend dashboard shell WHEN rendered in browser THEN dark luxury theme (#0a0a0a), typography classes, and 4-tier memory metrics are displayed.
- **B-2** — GIVEN the interactive LiquidGlass button WHEN rendered THEN SVG feDisplacementMap filter is applied with smooth spring hover physics.

---

## Success Criteria

Each criterion is a runnable bash function returning 0 (pass) or non-zero (fail).

```bash
# eval-1: verify frontend package definition and entry files exist
eval_1() {
  test -f frontend/package.json && test -f frontend/src/App.tsx
}

# eval-2: verify package dependencies include react ecosystem
eval_2() {
  python3 -c "import json; p = json.load(open('frontend/package.json')); assert 'react' in p.get('dependencies', {}) or 'dependencies' in p"
}

# eval-3: verify LiquidGlass SVG displacement implementation in dashboard
eval_3() {
  python3 -c "content = open('frontend/src/App.tsx', encoding='utf-8').read(); assert 'LiquidGlass' in content or 'feDisplacementMap' in content"
}
```

---

## Validation Card

```yaml
success_criteria:
  - id: eval_1
    description: verify frontend package definition and entry files exist
    runnable: bash
    check_type: deterministic
    verifies: [B-1]
    terminal: true
    expected_duration_sec: 2
  - id: eval_2
    description: verify package dependencies include react ecosystem
    runnable: bash
    check_type: deterministic
    verifies: [B-1]
    terminal: true
    expected_duration_sec: 2
  - id: eval_3
    description: verify LiquidGlass SVG displacement implementation in dashboard
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

1. **Git revert** — `git checkout -- frontend/`
2. **File restore** — delete uncommitted node artifacts
3. **State reset** — update task status to `parked` and record `blocked_reason`

(none — this task is additive with no destructive external changes)

---

## Observability Hooks

What to watch during execution and after deployment:

- **Expected duration:** 15s
- **Key metric:** bundle compilation without TypeScript errors
- **Alert condition:** missing CSS assets or broken SVG filter IDs
- **Log tail:** stderr on vite build

---

## Anti-Patterns

- **Don't use generic generic light themes or saturated primary colors** — Strictly use dark luxury charcoal `#0a0a0a` / `#121212` with muted gold/amber accents.
- **Don't omit the SVG LiquidGlass filter** — The luxury displacement effect is a signature aesthetic of the Memory Lab design.
- **Don't hardcode static memory counts** — Connect cards to live props / state structures matching the 4 cognitive tiers.

---

## Do-Not-Touch

Files the executor MUST NOT modify:

- cvg/
- .cvg/

---

## Open Questions

Things the executor should resolve DURING build, not assume:

(none — this task is fully specified)
