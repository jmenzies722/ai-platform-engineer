# 20 — Security

> **Status:** Scaffolded · Detailed lessons are intentionally not yet published.

## 5-Minute Orientation

### What is this?

Apply threat modeling, least privilege, identity, cryptography, secret management, isolation, secure delivery, and response practices across the stack. Make trust boundaries and abuse cases visible in design.

### Why does it matter?

This layer exists because the previous layer alone cannot make production systems understandable, dependable, and evolvable at scale. The module will teach the mechanism before the product vocabulary and connect every abstraction to observable behavior.

### Where does it fit?

This is Module 20 of 35. It follows [Site Reliability Engineering](../19-sre/README.md) and provides foundations used by later modules. See the [Curriculum](../CURRICULUM.md) for the complete dependency path.

### What do I need first?

Complete the Minimum Competency tier for [Site Reliability Engineering](../19-sre/README.md), or demonstrate the same capability with build and debugging evidence. Follow any additional prerequisites when this module’s lessons are published.

### What will I be able to explain afterward?

- the everyday problems this domain solves, before using specialized vocabulary;
- the relationships among threat modeling, least privilege, identity, cryptography, secret management, isolation, secure delivery, and response practices across the stack;
- where the abstraction appears in production and which lower-layer details can leak through it;
- one common failure, the evidence that distinguishes it, and a defensible design tradeoff.

## Competency Tiers

### Minimum Competency

Explain the module’s central mental model, complete guided proofs, and solve the designated No-AI challenge. This is enough for a first pass when the domain is not yet on your critical path.

### Strong Engineer

Build a representative system, break it safely, diagnose it from evidence, and operate it under realistic constraints. Explain the mechanism to both a new learner and a working engineer.

### Deep Dive

Inspect internals and primary sources, quantify reliability/security/cost tradeoffs, and make a design decision that accounts for adjacent layers.

Go deep when this domain blocks a current project, recurs in incidents, or underpins a decision you own. Otherwise earn Minimum Competency and continue.

## AI Learning Policy

### AI Tutor

Use AI for Socratic questions, prerequisite refreshers, and alternative analogies. Verify technical claims against canonical sources.

### AI Pair

Write your prediction and plan first. Read every generated command, state its expected effect, and keep ownership of tests and safety.

### AI Review

Ask AI to challenge assumptions, identify missing failure modes, and point out claims unsupported by evidence.

### No-AI Challenge

Complete the designated retrieval/build/debug task using your own model, local tools, and official documentation before consulting AI.

### Explain Back

Explain the concept without notes to a smart non-engineer, a junior engineer, and an interviewer. If one version collapses into jargon, revisit the intuition and mechanism.

## Planned Scope

No empty lesson files are created for this module. When authored, each lesson must satisfy [the lesson contract](../templates/LESSON.md), include a narratable Mermaid diagram, and end with an exact next path.

## Next

This scaffold is orientation, not completion. If you are following the active path, return to [START-HERE.md](../START-HERE.md). To preview the dependency that follows this module, open [Platform Engineering](../21-platform-engineering/README.md).
