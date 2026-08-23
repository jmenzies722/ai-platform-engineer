# Roadmap

This roadmap groups the curriculum by engineering capability. Move forward when you can produce the stated evidence. Reading every linked page is neither necessary nor sufficient.

Stages 1 through 6 build the software, infrastructure, reliability, and platform foundations. Stage 7 can begin once your programming and systems knowledge is sound. Stage 8 depends on both infrastructure practice and AI foundations. Stages 9 and 10 add platform ownership and technical leadership.

Use [HOW-TO-LEARN.md](HOW-TO-LEARN.md) to structure practice and [PROGRESS.md](PROGRESS.md) to record evidence.

## Select a role track

The stages below remain the broad capability map and the numbered modules remain canonical. Select a role-shaped composition from [tracks/README.md](tracks/README.md) when you know the work you are targeting. A track identifies which stages and modules to emphasize; it does not duplicate or replace their content. Enter at the earliest prerequisite for which current evidence is missing.

## Assessment gates

Use the cumulative [assessment system](assessments/README.md) at these capability boundaries. Every gate requires independently reviewable Explain, Build, Debug, Operate, and Design evidence; passing is based on the required vector and critical conditions, not an average or reading completion.

| Sequence | Gate |
|---:|---|
| 1 | [Foundations](assessments/gates/foundations.md) |
| 2 | [Systems, Linux, and Networking](assessments/gates/systems-linux-networking.md) |
| 3 | [Cloud Delivery](assessments/gates/cloud-delivery.md) |
| 4 | [Kubernetes Reliability](assessments/gates/kubernetes-reliability.md) |
| 5 | [Platform](assessments/gates/platform.md) |
| 6 | [AI Platform](assessments/gates/ai-platform.md) |
| 7 | [Staff](assessments/gates/staff.md) |

Each gate file owns its exact prerequisites and scope, so this roadmap does not restate them. Record each outcome and dimension vector in [PROGRESS.md](PROGRESS.md). Certification plans in [certs/README.md](certs/README.md) are optional overlays and do not add or replace a gate.

## 1. Foundations

**Modules:** [History](00-history/README.md), [Software Foundations](01-software-foundations/README.md), [Python](02-python/README.md), [Git](05-git/README.md), [Data Structures and Algorithms](06-data-structures-algorithms/README.md)

**Purpose:** Build causal context, programming fluency, source-control discipline, and the ability to trace source code into runtime behavior.

**Prerequisites:** Curiosity, command-line access, and willingness to test assumptions.

**Exit evidence:**
- Explain how source code becomes observable machine behavior through a runtime, operating system, process, memory, and CPU.
- Implement and test a nontrivial command-line program.
- Use branches, commits, diffs, and pull requests deliberately.
- Analyze time/space tradeoffs for common data structures.

## 2. Systems Practitioner

**Modules:** [Computer Systems](03-computer-systems/README.md), [Linux](04-linux/README.md), [Networking](07-networking/README.md), [Databases](08-databases/README.md), [Go](10-go/README.md)

**Purpose:** Understand the machine, kernel, network, and storage boundaries on which production software depends.

**Prerequisite:** Stage 1 exit evidence.

**Exit evidence:**
- Diagnose CPU, memory, file-descriptor, DNS, connection, and disk symptoms from OS evidence.
- Trace an HTTP request across DNS, TCP/TLS, application, and database boundaries.
- Explain process isolation, virtual memory, scheduling, transactions, indexes, and durability.
- Build a concurrent service and characterize its bottleneck.

## 3. Backend and Cloud Engineer

**Modules:** [Backend Engineering](09-backend-engineering/README.md), [Software Architecture](11-software-architecture/README.md), [AWS](12-aws/README.md)

**Purpose:** Design and operate service boundaries, data contracts, cloud resources, and failure-aware application architectures.

**Prerequisite:** Stage 2 systems and networking competency.

**Exit evidence:**
- Build an authenticated API with persistence, migrations, tests, and telemetry.
- Defend consistency, caching, API, and deployment tradeoffs.
- Map cloud identity, networking, compute, storage, and observability into a threat and failure model.

## 4. Infrastructure Engineer

**Modules:** [DevOps](13-devops/README.md), [Terraform](14-terraform/README.md), [Containers](15-containers/README.md), [Kubernetes](16-kubernetes/README.md), [Security](20-security/README.md)

**Purpose:** Make software delivery reproducible, isolated, policy-aware, and operable across environments.

**Prerequisite:** A production-shaped service from Stage 3.

**Exit evidence:**
- Build a CI/CD path with explicit promotion and rollback.
- Provision infrastructure idempotently and review a plan for destructive change.
- Explain container isolation from kernel primitives.
- Debug a Kubernetes workload from API intent through scheduling, networking, storage, and runtime.
- Apply least privilege, secret boundaries, image provenance, and supply-chain controls.

## 5. Distributed Systems and SRE

**Modules:** [Distributed Systems](17-distributed-systems/README.md), [Observability](18-observability/README.md), [SRE](19-sre/README.md), [System Design](34-system-design/README.md)

**Purpose:** Reason about partial failure, time, coordination, uncertainty, and reliability at scale.

**Prerequisite:** Stage 4 operational fluency.

**Exit evidence:**
- Explain replication, consensus, partitions, idempotency, backpressure, and failure detectors.
- Define meaningful SLIs/SLOs and use an error budget to make a release decision.
- Investigate an incident using correlated metrics, logs, traces, and change history.
- Produce a capacity model and failure-domain-aware system design.

## 6. Platform Engineer

**Modules:** [Platform Engineering](21-platform-engineering/README.md), [Developer Platforms](22-developer-platforms/README.md), [Control Planes](23-control-planes/README.md)

**Purpose:** Turn repeated infrastructure work into a secure, reliable product for internal developers.

**Prerequisite:** Stage 5 reliability and design competency.

**Exit evidence:**
- Discover developer needs rather than beginning with a portal.
- Design a paved road with contracts, escape hatches, ownership, and measurable adoption.
- Implement a reconciliation-based control plane.
- Measure platform outcomes through lead time, reliability, cognitive load, and support demand.

## 7. AI Systems Foundations

**Modules:** [AI Foundations](24-ai-foundations/README.md), [ML and Deep Learning](25-ml-deep-learning/README.md), [Transformers and LLMs](26-transformers-llms/README.md), [LLM Engineering](27-llm-engineering/README.md)

**Purpose:** Understand what models compute, how they are trained and evaluated, and how probabilistic behavior changes software engineering.

**Prerequisite:** Stage 2 programming, systems, data, and quantitative fluency. This stage may run in parallel with Stages 3–6.

**Exit evidence:**
- Explain optimization, generalization, embeddings, attention, tokenization, and autoregressive inference.
- Build an evaluated LLM application with explicit data, latency, cost, safety, and failure boundaries.
- Distinguish model error from retrieval, orchestration, serving, and product errors.

## 8. AI Infrastructure Engineer

**Modules:** [MLOps](28-mlops/README.md), [GPU Systems](29-gpu-systems/README.md), [AI Infrastructure](30-ai-infrastructure/README.md), [Model Serving](31-model-serving/README.md)

**Purpose:** Operate the lifecycle and compute substrate for training and inference.

**Prerequisites:** Stages 4–5 plus Stage 7.

**Exit evidence:**
- Build a lineage-aware model lifecycle with reproducible artifacts and evaluation gates.
- Explain GPU execution, memory hierarchy, communication, batching, and utilization.
- Characterize model-server throughput, latency, memory, and quality tradeoffs under load.
- Debug failures across scheduler, node, driver, runtime, model, and request layers.

## 9. AI Platform Engineer

**Modules:** [AI Platform Engineering](32-ai-platform-engineering/README.md), [Agentic Infrastructure](33-agentic-infrastructure/README.md)

**Purpose:** Productize AI infrastructure as governed, observable self-service capabilities for model and application teams.

**Prerequisites:** Stage 6 platform product thinking and Stage 8 AI infrastructure competency.

**Exit evidence:**
- Design multi-tenant model lifecycle and inference control planes.
- Define policy, quotas, identity, lineage, evaluation, deployment, and rollback contracts.
- Operate agent execution with durable state, bounded tools, approvals, auditability, and cost controls.
- Demonstrate a platform capability with adoption and reliability evidence.

## 10. Platform Engineering Leadership

**Module:** [Senior and Staff Engineering](35-senior-staff-engineering/README.md)

**Purpose:** Lead ambiguous, multi-team technical systems through influence, strategy, and durable organizational mechanisms.

**Prerequisite:** Repeated evidence across design, implementation, operations, and platform adoption.

**Exit evidence:**
- Write a strategy that links user problems, technical architecture, sequencing, and measurable outcomes.
- Lead a cross-team design through disagreement and explicit decisions.
- Improve the system that produces engineering work: standards, reviews, incident learning, mentoring, and investment choices.
- Show judgment about what not to build.

## Advancement rule

Update [PROGRESS.md](PROGRESS.md) only from evidence. At formal boundaries, use the linked assessment gate and retain its outcome and dimension vector:

- “I read it” supports **Learning**.
- A repeatable demonstration plus an accurate explanation supports **Minimum Competency**.
- An independent build and diagnosed controlled failure support **Practicing**.
- Independent operation and defensible routine design support **Competent**.
- Novel failure reasoning, quantified tradeoffs, and successful teaching support **Deep Understanding**.

The weakest dimension relevant to the next stage is the gate. Strong explanations do not replace operational practice; years of tool use do not replace a correct mechanism.
