---
adr: "0000"
status: accepted
date: 2026-10-12
ground: greenfield
converge_pass: 2
spec_ref: "R-1, R-2, R-3, R-4, R-5, R-6, R-7, W-1"
supersedes: ""
superseded_by: ""
deciders: "Zaiden"
---

# 0000 — Context: the ground we stand on

## Terrain

Greenfield memory infrastructure repository initialized within Converge execution ecosystem. No legacy code exists in this repository; the ADRs record the constraints that the Pass 1 Tech-Spec imposes on the underlying runtime environment.

## Given surface

- Host operating system: Windows workstation with Python 3.11 runtime environment.
- Git version control initialized at repository root with Converge control plane in `cvg/`.
- Local execution harness with Git Bash (`/c/Program Files/Git/bin/bash.exe`) and Ollama local model engine on PATH.
- Node.js / NPM environment supporting modern web development.

## Build surface

- Python cognitive memory core package managing episodic storage, semantic graph consolidation, and working memory budgets.
- Model Context Protocol (MCP) server exposing memory tool definitions to agent harnesses.
- Web inspection dashboard providing visual graph exploration and retention controls.

## Spec

The canonical tech-spec is `cvg/docs/tech-spec/memory-lab.md` signed on 2026-10-12.
