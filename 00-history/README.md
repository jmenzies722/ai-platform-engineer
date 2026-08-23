# 00 — History: Why the Stack Exists

**Module status: Complete**

## 5-Minute Orientation

### What

This module is a systems history of the abstractions beneath an AI platform: computation, languages, operating systems, networks, data systems, distributed coordination, cloud infrastructure, delivery practices, containers, orchestration, reliability, machine learning, large language models, and agents. It is not a chronology quiz. Every lesson uses two linked lenses:

1. **Before → Problem → Innovation → New abstraction → New problems → Modern connection**
2. **Capability → Complexity → Abstraction → Adoption → New Complexity → Next Abstraction**

### Why

Staff engineers must recognize why an abstraction exists, which failure it hides, and when that hidden failure leaks through. History supplies that causal model. Without it, a platform engineer can operate tools but cannot confidently debug below them, evaluate replacements, or predict the next bottleneck.

### Where It Fits

This is the curriculum foundation. It precedes hands-on depth in Linux, networking, distributed systems, Kubernetes, reliability, ML systems, and agent platforms. Later modules turn each historical layer into implementation and operational competence.

### Prerequisites

- Comfort using a terminal and reading short code examples
- Basic familiarity with applications, APIs, and cloud services
- Curiosity about system boundaries; no formal CS degree is assumed

### Outcomes

After this module, you can:

- explain the causal chain from physical computation to agentic systems;
- identify the abstraction and leaked implementation detail at each layer;
- connect production incidents to historical design trade-offs;
- distinguish durable principles from transient products;
- build, break, debug, and explain a small model of every major layer.

## Lesson Index

1. [Origins of Computing](./01-origins-of-computing.md)
2. [Why Software Exists](./02-why-software-exists.md)
3. [Machine Code to Assembly to High-Level Languages](./03-machine-code-assembly-high-level-languages.md)
4. [Evolution of Programming Languages](./04-evolution-of-programming-languages.md)
5. [Evolution of Operating Systems](./05-evolution-of-operating-systems.md)
6. [Unix, C, and Linux](./06-unix-c-linux.md)
7. [Networking and the Internet](./07-networking-and-the-internet.md)
8. [Databases](./08-databases.md)
9. [Distributed Systems](./09-distributed-systems.md)
10. [Virtualization and Cloud](./10-virtualization-and-cloud.md)
11. [DevOps](./11-devops.md)
12. [Containers](./12-containers.md)
13. [Kubernetes](./13-kubernetes.md)
14. [SRE and Observability](./14-sre-and-observability.md)
15. [Platform Engineering](./15-platform-engineering.md)
16. [Machine Learning](./16-machine-learning.md)
17. [Transformers and LLMs](./17-transformers-and-llms.md)
18. [AI Infrastructure](./18-ai-infrastructure.md)
19. [AI Platform Engineering](./19-ai-platform-engineering.md)
20. [Agentic Engineering](./20-agentic-engineering.md)

## Competency Tiers

### Minimum Competency

Complete every Knowledge Check and No-AI Challenge. Be able to name the problem each abstraction solved, draw its visual model, run the basic commands, and identify one failure that crosses its boundary.

### Strong Engineer

Complete every lab, build exercise, and break-it exercise. Compare alternatives using workload, reliability, security, cost, and operability. Debug from evidence rather than product folklore.

### Deep Dive

Read the DEEP DIVE references, reproduce seminal mechanisms in miniature, and connect at least three layers in one design review—for example GPU scheduling, model serving, backpressure, and SLOs.

## AI Learning Policy

### AI Tutor

Use AI to ask Socratic questions, request a second explanation, or generate a counterexample. Require it to identify assumptions and cite primary sources. Verify claims against the references.

### AI Pair Programming

Use AI after writing your own design sketch. Keep changes small, inspect every command, and retain ownership of tests, security boundaries, and operational consequences.

### AI Review

Ask AI to challenge your model: “Which abstraction leaks?”, “What fails under partial outage?”, and “What evidence would disprove this diagnosis?” Treat its response as review input, not authority.

### No-AI Challenge

Complete each lesson’s No-AI Challenge without autocomplete, chat, or generated search summaries. The purpose is retrieval practice and independent systems reasoning.

### Explain Back

Close each lesson by explaining the full causal chain aloud or in writing to another person. If you cannot state the before-state, pressure, abstraction, new complexity, and modern connection, revisit the lesson.

## Completion Standard

The module is complete when the learner can traverse the stack in both directions: from transistors to agents and from an agent failure back through model serving, orchestration, distributed state, networking, operating systems, and hardware.
