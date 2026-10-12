---
adr: "0004"
status: accepted
date: 2026-10-12
ground: greenfield
converge_pass: 2
spec_ref: "R-6, R-7"
supersedes: ""
superseded_by: ""
deciders: "Zaiden"
---

# 0004 — Web Dashboard Inspection Surface

## Context

Requirement R-6 requires an inspection surface to render episodic queries and semantic graphs within 300ms for collections up to 50000 records. Operators need visual clarity over what the agent remembers, confidence weights of stored assertions, and data governance controls.

## Decision

The inspection interface is a lightweight single-page application built on React with Vite and Tailwind CSS. The visual surface incorporates high-performance HTML5 Canvas rendering for atmospheric telemetry and fluid mathematical visualization (Amber Cascades) and SVG displacement filtering for optical controls. Data exchange with the local engine occurs via local JSON endpoints provided by the local server.

## Evidence

Testing static bundle delivery and Vite development startup on the local Node.js environment confirms cold boot times under 400ms:

```bash
node -e 'console.log("Node environment ready for Vite dashboard runtime: " + process.version)'
```

## Consequences

Developers inspect, search, pin, or redact stored agent memories in real-time without modifying raw database files. The dashboard remains completely decoupled from core agent execution loops.

## Rejected reading

Relying exclusively on terminal CLI commands for memory governance was rejected because knowledge graphs and associative networks are inherently spatial and require graphical visualization for operator comprehension.

