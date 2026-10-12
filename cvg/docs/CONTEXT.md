# CONTEXT — Memory Lab Domain Glossary

This glossary anchors the technical and cognitive vocabulary across Memory Lab passes. Terms here reflect immutable domain definitions.

## Cognitive Memory Terms

- **Episodic Memory**: High-fidelity longitudinal record of complete agent execution traces, interactions, prompts, and tool results, organized by temporal sessions and salience scores.
- **Semantic Memory**: Knowledge graph of distilled facts, entities, and relationships extracted across multiple interactions, structured as queryable triples with confidence weights.
- **Working Memory**: Real-time context budget manager that maintains active execution state, filters conversational noise, and coordinates hand-offs to persistent storage.
- **Procedural Memory**: Extracted heuristics, successful tool invocation sequences, and operational scripts compiled from repetitive execution patterns.
- **Salience Score**: Normalized scalar value between 0.0 and 1.0 indicating the cognitive priority, novelty, and lasting relevance of an episodic trace.
- **Attention Budget**: Strict upper ceiling on active prompt tokens (default: 4000 tokens) allocated to working context, preventing model attention dilution.
- **Knowledge Triple**: Atomic unit of semantic memory composed of Subject, Predicate, and Object, tied to originating episodic IDs for verifiable provenance.
- **Memory Hand-off**: Deterministic transition phase where working memory commits significant segments to episodic storage and updates the semantic graph.
- **Memory Redaction**: Explicit lifecycle action removing or masking sensitive data from episodic and semantic stores while maintaining graph integrity.

