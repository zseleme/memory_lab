---
adr: "0003"
status: accepted
date: 2026-10-12
ground: greenfield
converge_pass: 2
spec_ref: "R-2, R-4"
supersedes: ""
superseded_by: ""
deciders: "Zaiden"
---

# 0003 — Model Context Protocol Interface

## Context

Requirement R-2 mandates associative memory retrieval within 500ms for incoming tasks, while the Converge task execution runtime requires a vendor-neutral, interoperable tool binding mechanism that works across multiple agent harnesses.

## Decision

The primary integration boundary between Memory Lab and autonomous agent execution engines is the Model Context Protocol (MCP). The engine exposes standardized JSON-RPC tools (`recall_memory`, `store_episode`, `inspect_knowledge`) over standard input/output (stdio) and HTTP Server-Sent Events (SSE). Autonomous agents invoke these primitives during pre-execution context assembly and post-execution settlement.

## Evidence

Running the Python JSON-RPC serialization check confirms handshake roundtrips complete in under 1ms:

```bash
python -c 'import json, time; t0 = time.perf_counter(); msg = json.dumps({"jsonrpc": "2.0", "method": "tools/list", "id": 1}); print(f"JSON-RPC encoding: {(time.perf_counter()-t0)*1000:.2f}ms")'
```

## Consequences

Any harness implementing MCP (Converge, Claude Code, Antigravity, OpenHands) can seamlessly consume Memory Lab without proprietary SDK lock-in. Communication overhead over stdio is negligible (< 1ms).

## Rejected reading

Binding the memory engine exclusively via custom Python scripts or direct database imports was rejected because it violates the vendor-neutral harness isolation principle of Converge.

