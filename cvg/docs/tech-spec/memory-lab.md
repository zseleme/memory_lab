# Tech-Spec — Memory Lab Cognitive Engine

## Problem restated

Autonomous engineering agents operate with zero cross-task memory retention. When a task execution concludes, all context, decisions, failure modes, and operational heuristics vanish. As a result, agents repeat identical debugging failures in similar tasks, waste up to 35% of token budgets rediscovering repository conventions, and require continuous manual supervision. Memory Lab solves this by providing a unified cognitive persistence layer that captures execution episodes, consolidates domain knowledge, dynamically manages attention budgets, and exposes operational recall to autonomous execution engines within 500ms.

## Scope

**In scope:**
- Episodic retention of agent execution traces, conversational turns, and tool outputs with temporal indexing.
- Continuous distillation of factual assertions and relations into an associative knowledge graph with bidirectional traceability.
- Real-time attention management coordinating memory hand-offs and keeping active context within token constraints.
- Standardized tool interface exposing memory retrieval and recording to external task execution runtimes.
- Visual inspection interface to search episodes, inspect distilled knowledge graphs, and govern retention policies.

**Explicitly out of scope:**
- Training, pre-training, or fine-tuning foundation weights.
- Centralized multi-tenant cloud authentication and subscription billing.
- Self-executing agent runtime or scheduler (the memory engine serves external execution runtimes, it does not orchestrate them).

## Requirements

- R-1 (must): The memory engine must record complete task interaction episodes with timestamp, actor identity, task slug, and outcome within 100ms of session completion.
- R-2 (must): Associative recall of relevant past episodes must return top-k matches with salience scores within 500ms for incoming task contexts up to 8000 tokens.
- R-3 (must): Semantic knowledge consolidation must extract subject-predicate-object assertions from episodes and merge duplicates with confidence scoring updated within 2000ms.
- R-4 (must): The working memory manager must enforce an active context ceiling of at most 4000 tokens, dynamically pruning stale entries while pinning critical constraints.
- R-5 (should): Every consolidated fact in the knowledge store must maintain cross-link identifiers pointing to at least 1 originating episodic record for provenance tracking.
- R-6 (should): The visual inspection interface must render episodic search queries and knowledge relationships with response times under 300ms for collections up to 50000 records.
- R-7 (could): The engine could support automatic background decay of low-salience memories unreferenced for greater than 30 days.
- W-1 (wont): The engine will not execute autonomous task dispatch or code modifications directly in Phase 1.

## Success metrics

- Context re-discovery overhead: baseline 15 hours/week -> target under 2 hours/week
- Retrieval latency for historical decisions: baseline manual lookups -> target under 500ms
- Repeat failure rate across similar tasks: baseline 40% -> target under 5%
- Token consumption spent on redundant context discovery: baseline 35% -> target under 5%

## Data

The cognitive engine consumes and produces the following core entities at the problem level:
- **Task Interaction Traces**: Raw inputs, execution outputs, status transitions, and environmental events produced during task loops.
- **Episodic Records**: Structured narrative segments indexed by temporal markers, topic tags, participant identifiers, and salience scores.
- **Knowledge Assertions**: Distilled factual propositions, entity references, relational edges, and confidence scores.
- **Attention Context Windows**: Prioritized subsets of active memories, relevant facts, and critical constraints prepared for agent prompts.
- **Retention Policies**: Explicit rules governing pinning, expiration, redaction, and consolidation intervals.

## Open assumptions

- question: "Will local disk storage for 50000 episodes remain under 500MB without external compression?"
  owner: Zaiden
  resolution: Target initial data storage layout with compact binary or columnar serialization to ensure low footprint.

- question: "Should semantic graph consolidation run synchronously at task exit or asynchronously in a background phase?"
  owner: Zaiden
  resolution: Run asynchronous background consolidation upon task settlement to preserve task loop completion speeds under 500ms.

### Gap register

- id: GAP-001
  type: number
  severity: minor
  question: "What is the maximum token budget allocated to episodic retrieval per task query?"
  blocks: "R-4"
  owner: "Zaiden"
  resolution: "Default to 1500 tokens for retrieved episodic context within the 4000 token working memory ceiling."

## Sign-off

- **Owner/decider:** Zaiden — verdict: canonical
- **Date:** 2026-10-12

