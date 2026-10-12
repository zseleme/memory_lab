---
leg: swimlane-core-leg-01
parent: swimlane-core
swimlane: core
status: proposed
spec_ref: R-1
depends_on: []
---

# Leg 01 — Storage

## Responsibility

Persist structured task interaction episodes and execution traces into embedded SQLite storage with sub-100ms response latency and support for transactional rollback.

## Proves

- Given a new task interaction trace with actor identity and status
- When recorded by the episodic persistence engine
- Then the episode is durable in SQLite WAL storage with an assigned episode identifier within 100ms

## Independence

This leg operates independently on local disk files with zero network or external runtime requirements.

## Yields at Pass 5B

- Initialize SQLite database with episodic table schema and migration tooling
- Write episodic ingestion module storing interaction turns with timestamp and salience
- Add retrieval query functions fetching historical episodes by session and tag

