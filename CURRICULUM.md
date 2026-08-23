# Curriculum

The curriculum follows the dependencies of an AI platform. Hardware and software execution come first; distributed infrastructure and platform control follow; AI workloads sit on those foundations. Use [ROADMAP.md](ROADMAP.md) to decide how much evidence you need before moving on.

A module README is a map, not a lesson. Each chapter contains an ordered lesson sequence, practical evidence, failure work, and primary sources. A learner should leave with a mechanism they can explain and evidence they can inspect. If a chapter cannot support that claim, it remains a curriculum gap rather than completed learning material.

## Chapter contract

Every major technology is treated as an engineering system, not a vocabulary list. Its chapter should establish:

- why the system exists and which constraints shaped it;
- what contract users and neighboring systems rely on;
- how the mechanism, state, and critical paths work;
- which internals explain correctness, performance, security, or cost;
- how to build a reduced version or exercise the real interface;
- how it fails, which symptoms are ambiguous, and how to debug it;
- how to operate, secure, scale, recover, and evolve it;
- how to compare designs under stated requirements.

Lessons use **See it yourself** for bounded proofs. Module labs combine mechanisms. [Incident drills](incidents/README.md) withhold the diagnosis. [Projects](projects/README.md) require integration and sustained engineering judgment.

## Foundations

- 00 [History](00-history/README.md)
- 01 [Software Foundations](01-software-foundations/README.md)
- 02 [Python](02-python/README.md)
- 03 [Computer Systems](03-computer-systems/README.md)
- 04 [Linux](04-linux/README.md)
- 05 [Git](05-git/README.md)
- 06 [Data Structures and Algorithms](06-data-structures-algorithms/README.md)

## Data and services

- 07 [Networking](07-networking/README.md)
- 08 [Databases](08-databases/README.md)
- 09 [Backend Engineering](09-backend-engineering/README.md)
- 10 [Go](10-go/README.md)
- 11 [Software Architecture](11-software-architecture/README.md)

## Cloud infrastructure

- 12 [AWS](12-aws/README.md)
- 13 [DevOps](13-devops/README.md)
- 14 [Terraform](14-terraform/README.md)
- 15 [Containers](15-containers/README.md)
- 16 [Kubernetes](16-kubernetes/README.md)
- 17 [Distributed Systems](17-distributed-systems/README.md)
- 18 [Observability](18-observability/README.md)
- 19 [Site Reliability Engineering](19-sre/README.md)
- 20 [Security](20-security/README.md)

## Platforms

- 21 [Platform Engineering](21-platform-engineering/README.md)
- 22 [Developer Platforms](22-developer-platforms/README.md)
- 23 [Control Planes](23-control-planes/README.md)

## AI systems

- 24 [AI Foundations](24-ai-foundations/README.md)
- 25 [Machine Learning and Deep Learning](25-ml-deep-learning/README.md)
- 26 [Transformers and LLMs](26-transformers-llms/README.md)
- 27 [LLM Engineering](27-llm-engineering/README.md)
- 28 [MLOps](28-mlops/README.md)
- 29 [GPU Systems](29-gpu-systems/README.md)
- 30 [AI Infrastructure](30-ai-infrastructure/README.md)
- 31 [Model Serving](31-model-serving/README.md)
- 32 [AI Platform Engineering](32-ai-platform-engineering/README.md)
- 33 [Agentic Infrastructure](33-agentic-infrastructure/README.md)

## Design and leadership

- 34 [System Design](34-system-design/README.md)
- 35 [Senior and Staff Engineering](35-senior-staff-engineering/README.md)

## How to use it

Study dependencies in order when a subject is new. Skip ahead only when you can produce the prerequisite evidence: a correct explanation, a working build, and diagnosis of a relevant failure. Deepen the modules that support your work; return to earlier ones when an abstraction leaks.

The module numbers provide the dependable first pass. Real work is less linear. Once you can program and inspect a system, it is reasonable to study an application track alongside its infrastructure track. The [ROADMAP.md](ROADMAP.md) stage gates state the evidence needed before later platform claims are credible.

Use the full learning loop:

1. read the chapter orientation and record a prediction;
2. work the lessons in order, running the smallest useful proofs;
3. complete the module lab without copying unexplained commands;
4. attempt a related incident before opening its solution;
5. integrate the domain into a portfolio project;
6. use the interview bank to explain changed constraints;
7. record inspectable evidence in [PROGRESS.md](PROGRESS.md).
