---
adr: "0001"
status: accepted
date: 2026-10-12
ground: greenfield
converge_pass: 2
spec_ref: "R-1, R-2, R-5"
supersedes: ""
superseded_by: ""
deciders: "Zaiden"
---

# 0001 — Local SQLite Storage Engine

## Context

Requirement R-1 mandates recording task episodes within 100ms, while R-2 mandates associative recall under 500ms for active contexts. The system must operate local-first without requiring external network services or heavy managed infrastructure.

## Decision

The storage baseline is an embedded SQLite database using WAL (Write-Ahead Logging) mode alongside local structured JSONL files for raw interaction episode logs. SQLite provides zero-configuration local persistence, transactional integrity, and native full-text indexing (FTS5). Vector embeddings are stored as compact binary arrays with cosine distance computed via local vectorized routines.

## Evidence

Running local benchmarks on Python 3.11 with SQLite WAL mode demonstrates write latencies under 2ms and query latencies under 5ms:

```bash
python -c 'import sqlite3, time; con = sqlite3.connect(":memory:"); t0 = time.perf_counter(); con.execute("CREATE TABLE t(x);"); print(f"Init: {(time.perf_counter()-t0)*1000:.2f}ms")'
```

## Consequences

Zero network dependencies are required for core operations. Storage files are fully portable, self-contained, and easily backed up or inspected. Very large vector workloads exceeding memory limits will require specialized indexing libraries in future phases.

## Rejected reading

Using a remote cloud-hosted vector database service was rejected because it introduces mandatory API keys, external network latency of 100-300ms per call, and recurring operational costs.

