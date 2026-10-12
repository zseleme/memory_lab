---
leg: swimlane-core-leg-02
parent: swimlane-core
swimlane: core
status: proposed
spec_ref: R-3, R-5
depends_on:
  - swimlane-core-leg-01
---

# Leg 02 — Semantic

## Responsibility

Extract subject-predicate-object knowledge assertions from episodic text and maintain a queryable, self-organizing graph that updates confidence scores and cross-links to episode origins.

## Proves

- Given a completed episodic trace with factual engineering assertions
- When processed by the semantic consolidation extractor
- Then distilled knowledge triples are stored with originating episode IDs and confidence weights within 2000ms

## Independence

Relies only on the local episodic storage interface established in Leg 01.

## Yields at Pass 5B

- Write knowledge assertion extraction logic for subject predicate object triples
- Add semantic graph storage tables linking assertions to originating episode IDs
- Provide associative graph search functions returning related entities with confidence scores

