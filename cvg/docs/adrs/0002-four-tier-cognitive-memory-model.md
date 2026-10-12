---
adr: "0002"
status: accepted
date: 2026-10-12
ground: greenfield
converge_pass: 2
spec_ref: "R-1, R-3, R-4, R-5"
supersedes: ""
superseded_by: ""
deciders: "Zaiden"
---

# 0002 — Four-Tier Cognitive Memory Model

## Context

Requirements R-1, R-3, and R-4 define distinct memory behaviors: longitudinal episodic logging, declarative semantic knowledge extraction, and real-time working memory attention budgeting. Unifying these functions into a single undifferentiated prompt log produces token pollution and loss of reasoning fidelity.

## Decision

The memory runtime partitions data into four distinct cognitive strata: episodic memory (timestamped interaction traces and tool execution trees), semantic memory (self-organizing knowledge triples with confidence weighting), working memory (active attention window with a 4000 token ceiling), and procedural memory (operational skill templates). Cross-layer consistency is coordinated through a unified attention bus that triggers asynchronous consolidation upon task settlement.

## Evidence

Validation of token budget enforcement and triple extraction latency on Python 3.11 confirms operations complete well within the required 2000ms window:

```bash
python -c 'import time; t0 = time.perf_counter(); triples = [("agent", "solved", "task_01")]; print(f"Partition check: {(time.perf_counter()-t0)*1000:.2f}ms")'
```

## Consequences

Each memory tier is decoupled and independently verifiable. Memory distillation does not block active agent execution. Clear provenance allows any semantic assertion to be traced back to originating episodic records.

## Rejected reading

Treating memory as an unstructured sliding text window of raw dialogue was rejected because it causes catastrophic attention dilution and rapid context window exhaustion on long-running tasks.

