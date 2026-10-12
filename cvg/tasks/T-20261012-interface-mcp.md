---
id: T-20261012-interface-mcp
title: "Implement Model Context Protocol server exposing memory tools"
status: ready
format_version: 3
profile: standard
effort: S
budget_iterations: 15
agent: zaiden
parent: cvg/swimlanes/interface/leg-01-mcp-server.md
depends_on:
  - T-20261012-core-working
supersedes: (none)

touches_paths: []
creates_paths:
  - memory_lab/interfaces/mcp_server.py
  - tests/test_mcp.py
source_note: "cvg/swimlanes/interface/leg-01-mcp-server.md"
created: 2026-10-12T20:16:32Z
tags: [interface, mcp, jsonrpc, stdio]
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
signed_off_at: 2026-10-12T20:25:56Z
accepted: false
accepted_by: (none)
accepted_at: (none)
evidence_refs: []
signed_off_sig: hmac-sha256-v3:3d32e54d:e0878b1f606affb91d618e4cf57cd0e64dea3f3a38843053568a83c0834c5bed
---

# "Implement Model Context Protocol server exposing memory tools"

> **Why:** Provide the standard Model Context Protocol interface allowing agentic workflows (Claude, Cursor, Converge) to interact with the 4 memory tiers via JSON-RPC.

---

## Goal

Implement an MCP server exposing stdio and JSON-RPC dispatch for `remember_episodic`, `search_semantic`, `get_working_context`, and `reinforce_procedure` tools.

---

## Context

Decomposed from `cvg/swimlanes/interface/leg-01-mcp-server.md` and R-6 in `cvg/docs/tech-spec/memory-lab.md` and ADR-0003 (`cvg/docs/adrs/0003-mcp-protocol-interface.md`).

---

## Behavior

- **B-1** — GIVEN valid MCP tool call `remember_episodic` over stdio transport WHEN dispatched with payload THEN episode is recorded and success response is returned with episode id.
- **B-2** — GIVEN tool call `get_working_context` WHEN queried with active session THEN packed context fitting 4000 token ceiling is returned within 500ms.

---

## Success Criteria

Each criterion is a runnable bash function returning 0 (pass) or non-zero (fail).

```bash
# eval-1: verify MCP tool listing exposes cognitive tools
eval_1() {
  python3 -c "from memory_lab.interfaces.mcp_server import create_mcp_server; server = create_mcp_server(); tools = server.list_tools(); assert 'remember_episodic' in [t.name for t in tools]; assert 'get_working_context' in [t.name for t in tools]"
}

# eval-2: verify JSON-RPC tool dispatch execution
eval_2() {
  python3 -c "from memory_lab.interfaces.mcp_server import handle_jsonrpc_request; req = {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call', 'params': {'name': 'get_working_context', 'arguments': {'session_id': 'test'}}}; res = handle_jsonrpc_request(req); assert 'result' in res or 'error' in res"
}

# eval-3: run mcp interface unit test suite
eval_3() {
  python3 -m unittest tests/test_mcp.py
}
```

---

## Validation Card

```yaml
success_criteria:
  - id: eval_1
    description: verify MCP tool listing exposes cognitive tools
    runnable: bash
    check_type: deterministic
    verifies: [B-1]
    terminal: true
    expected_duration_sec: 2
  - id: eval_2
    description: verify JSON-RPC tool dispatch execution
    runnable: bash
    check_type: deterministic
    verifies: [B-2]
    terminal: true
    expected_duration_sec: 3
  - id: eval_3
    description: run mcp interface unit test suite
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

1. **Git revert** — `git checkout -- memory_lab/interfaces/mcp_server.py tests/test_mcp.py`
2. **File restore** — delete uncommitted socket or pipe files
3. **State reset** — update task status to `parked` and record `blocked_reason`

(none — this task is additive with no destructive external changes)

---

## Observability Hooks

What to watch during execution and after deployment:

- **Expected duration:** 15s
- **Key metric:** JSON-RPC tool dispatch roundtrip < 500ms
- **Alert condition:** JSON-RPC malformed parse error or protocol schema violation
- **Log tail:** stderr on stdio read loop

---

## Anti-Patterns

- **Don't pollute stdout** — MCP stdio communication reserves stdout for JSON-RPC messages; all debug output must go to stderr.
- **Don't return unbounded outputs** — Responses for context retrieval must adhere to the 4000-token ceiling.
- **Don't swallow exceptions** — Unhandled server errors must format into standard JSON-RPC error responses with error codes.

---

## Do-Not-Touch

Files the executor MUST NOT modify:

- cvg/
- .cvg/

---

## Open Questions

Things the executor should resolve DURING build, not assume:

(none — this task is fully specified)
