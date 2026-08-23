# Interview Map

Use this map **after** building and debugging in a domain. It converts evidence into a concise explanation; it is not a shortcut around competence. Interview practice without implementation evidence produces answers that collapse under one changed constraint.

Before practicing a theme:

1. score the concept with [TEACH-BACK.md](TEACH-BACK.md);
2. link build or incident evidence in [PROGRESS.md](PROGRESS.md);
3. prepare one claim you revised because evidence contradicted your first model.

## Evaluation Pattern

For every theme, prepare to:

1. establish requirements and constraints;
2. state a mental model;
3. describe internals and critical paths;
4. identify failure modes and evidence;
5. quantify capacity, reliability, security, and cost tradeoffs;
6. evolve the design when assumptions change.

Begin in plain language, then earn the precise term. A strong answer can move between intuition, mechanism, and engineering tradeoffs without confusing them.

## Select evidence for the role

Use [role tracks](tracks/README.md) to choose relevant themes, then select the corresponding integration brief from [PROJECTS.md](PROJECTS.md). A gate outcome in [PROGRESS.md](PROGRESS.md) is stronger preparation than broad question coverage because it records separate Explain, Build, Debug, Operate, and Design evidence.

Use the synthetic [case studies](case-studies/README.md) for changed-constraint practice:

| Interview focus | Decision practice | Related project |
|---|---|---|
| Kubernetes rollout, mitigation, and recovery | [Failed Kubernetes rollout](case-studies/01-failed-kubernetes-rollout.md) | [Multi-Tenant Kubernetes Application Platform](projects/06-kubernetes-platform/README.md) |
| Inference latency, fairness, capacity, and cost | [Inference latency and cost](case-studies/02-inference-latency-and-cost.md) | [Multi-Tenant Model Serving System](projects/12-model-serving-system/README.md) |
| Platform adoption, governance, and economics | [Platform adoption](case-studies/03-platform-adoption.md) | [Secure Developer Platform Control Plane](projects/09-developer-platform-control-plane/README.md) |

| Domain | Common interview themes | Preparation modules | Evidence to bring |
|---|---|---|---|
| Software execution | Compilation vs interpretation, process/thread, virtual memory, syscalls, CPU vs I/O work | [Software Foundations](01-software-foundations/README.md), [Computer Systems](03-computer-systems/README.md), [Linux](04-linux/README.md) | Process inspection lab; execution trace explained without notes |
| Programming | Language semantics, testing, concurrency, API design, complexity | [Python](02-python/README.md), [Go](10-go/README.md), [DS&A](06-data-structures-algorithms/README.md) | Tested implementation plus profile and design rationale |
| Networking | DNS, TCP/TLS, HTTP, load balancing, timeouts, retries, connection failure | [Networking](07-networking/README.md) | Packet/request trace and a diagnosed DNS or connection incident |
| Databases | Indexes, query plans, transactions, isolation, replication, consistency, schema evolution | [Databases](08-databases/README.md), [Distributed Systems](17-distributed-systems/README.md) | Query-plan analysis, migration strategy, and consistency tradeoff |
| Backend systems | API contracts, auth, queues, caching, idempotency, backpressure | [Backend Engineering](09-backend-engineering/README.md), [Software Architecture](11-software-architecture/README.md) | Production-shaped service and failure test |
| Cloud and infrastructure | IAM, VPCs, compute/storage selection, IaC state, CI/CD, rollback | [AWS](12-aws/README.md), [DevOps](13-devops/README.md), [Terraform](14-terraform/README.md) | Reviewed infrastructure plan and deployment/rollback evidence |
| Containers | Isolation, images, namespaces, cgroups, registries, runtime and supply chain | [Containers](15-containers/README.md), [Linux](04-linux/README.md), [Security](20-security/README.md) | Image analysis and host-to-container debugging trace |
| Kubernetes | API intent, reconciliation, scheduling, probes, resources, networking, storage, operators | [Kubernetes](16-kubernetes/README.md), [Control Planes](23-control-planes/README.md) | Workload failure diagnosed layer by layer; small controller |
| Distributed systems | Partial failure, clocks, consensus, replication, partitions, idempotency, queues | [Distributed Systems](17-distributed-systems/README.md), [System Design](34-system-design/README.md) | Failure model, sequence diagram, and tested recovery behavior |
| Observability | Instrumentation, cardinality, context propagation, sampling, correlation, telemetry cost | [Observability](18-observability/README.md) | Investigation driven by metrics/logs/traces rather than a known answer |
| SRE | SLI/SLO, error budgets, toil, incident command, capacity, graceful degradation | [SRE](19-sre/README.md) | SLO document, incident review, and reliability investment decision |
| Security | Threat models, least privilege, secrets, identity, network and supply-chain controls | [Security](20-security/README.md) | Threat model with mitigations and residual risk |
| Platform engineering | Platform as product, paved roads, APIs, self-service, governance, adoption, cognitive load | [Platform Engineering](21-platform-engineering/README.md), [Developer Platforms](22-developer-platforms/README.md) | User discovery, platform contract, adoption and reliability metrics |
| ML systems | Training/evaluation, drift, lineage, reproducibility, deployment and rollback | [AI Foundations](24-ai-foundations/README.md), [ML/DL](25-ml-deep-learning/README.md), [MLOps](28-mlops/README.md) | Reproducible experiment and model promotion decision |
| LLM systems | Tokenization, attention, context, retrieval, evaluation, hallucination, safety, cost | [Transformers/LLMs](26-transformers-llms/README.md), [LLM Engineering](27-llm-engineering/README.md) | Evaluated LLM system with decomposed failure analysis |
| GPU systems | SIMT, memory hierarchy, kernels, utilization, interconnects, collectives | [GPU Systems](29-gpu-systems/README.md) | Profile interpreted into a bottleneck hypothesis and correction |
| AI infrastructure | Scheduling, data paths, GPU fleets, tenancy, quota, observability, failure domains | [AI Infrastructure](30-ai-infrastructure/README.md), [Model Serving](31-model-serving/README.md) | Capacity model and cross-layer incident diagnosis |
| Model serving | Batching, KV cache, parallelism, routing, autoscaling, rollout, throughput/latency/cost | [Model Serving](31-model-serving/README.md) | Load-test curves and deployment safety strategy |
| AI platforms | Model lifecycle, self-service inference, evaluation gates, policy, lineage, multi-tenancy | [AI Platform Engineering](32-ai-platform-engineering/README.md) | Control-plane design with contracts and operator model |
| Agentic infrastructure | Tool permissions, durable execution, state, approvals, sandboxing, audit, evaluation | [Agentic Infrastructure](33-agentic-infrastructure/README.md), [Security](20-security/README.md) | Threat model and recoverable agent workflow |
| Senior/staff leadership | Ambiguity, strategy, influence, tradeoffs, migrations, incidents, organizational leverage | [Senior/Staff](35-senior-staff-engineering/README.md), [System Design](34-system-design/README.md) | Decision records with outcomes, changed minds, and lessons |

## Practice Record

| Date | Theme | Level | Result | Weakest follow-up | Evidence to produce next |
|---|---|---|---|---|---|
| YYYY-MM-DD | Example: Kubernetes scheduling | Senior | Needs work | Preemption and disruption interaction | Reproduce in a local cluster |

After each attempt, repair the weakest follow-up by building or measuring something. Rehearsing the same wording is not remediation.
