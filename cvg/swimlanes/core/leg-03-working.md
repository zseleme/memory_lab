---
leg: swimlane-core-leg-03
parent: swimlane-core
swimlane: core
status: proposed
spec_ref: R-2, R-4
depends_on:
  - swimlane-core-leg-01
  - swimlane-core-leg-02
---

# Leg 03 — Working

## Responsibility

Manage active context attention budgets during agent task execution by dynamically prioritizing relevant memories and enforcing a strict 4000 token upper ceiling.

## Proves

- Given an incoming task prompt and a retrieved set of past memories exceeding 4000 tokens
- When evaluated by the working memory attention budgeter
- Then low-salience items are pruned to keep total tokens under 4000 while pinning critical constraints

## Independence

Combines outputs from Leg 01 and Leg 02 into in-memory context data structures without changing underlying storage.

## Yields at Pass 5B

- Write token counting and attention budgeting calculator
- Add context pruning algorithm prioritizing recent turns and pinned constraints
- Provide context synthesis function assembling final prompt additions under 500ms

