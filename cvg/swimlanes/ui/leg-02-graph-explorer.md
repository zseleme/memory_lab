---
leg: swimlane-ui-leg-02
parent: swimlane-ui
swimlane: ui
status: proposed
spec_ref: R-6, R-7
depends_on:
  - swimlane-ui-leg-01
  - swimlane-interface-leg-01
---

# Leg 02 — Graph Explorer

## Responsibility

Render interactive node-link knowledge graph exploration, episode search timeline, and data retention governance controls within sub-300ms query response times.

## Proves

- Given a user searching historical memories or inspecting distilled knowledge
- When queries are submitted in the dashboard interface
- Then relevant graph nodes and episodic timeline cards render within 300ms with provenance badges

## Independence

Consumes the standard JSON output schemas from Interface Leg 01.

## Yields at Pass 5B

- Write episodic memory timeline viewer with search filters and salience tags
- Implement interactive knowledge graph visualization component for entity triples
- Add retention control panels for pinning redacting and exporting memory records

