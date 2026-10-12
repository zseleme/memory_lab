---
leg: swimlane-interface-leg-02
parent: swimlane-interface
swimlane: interface
status: proposed
spec_ref: R-1, R-2
depends_on:
  - swimlane-interface-leg-01
---

# Leg 02 — Converge Hook

## Responsibility

Provide an integration hook script and adapter that automatically queries relevant memories before a Converge task-loop run and writes interaction outcomes upon task settlement.

## Proves

- Given a signed Converge Task-Spec ready for dispatch
- When processed by the pre-flight memory hook
- Then relevant past episodes and constraints are injected into the agent context budget under 500ms

## Independence

Acts as a standalone shell/Python bridge interfacing with Converge CLI receipt structures.

## Yields at Pass 5B

- Write pre-flight context extraction script reading task intent
- Add post-settlement hook parsing task execution receipts into new episodes
- Provide configuration helper registering the hook with project control plane

