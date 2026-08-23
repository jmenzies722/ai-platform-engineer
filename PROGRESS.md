# Progress

Update this file with links to work you can inspect again. Every domain begins unclaimed.

**Scale:** ⬜ Not Started · 🟨 Learning · 🟦 Practicing · 🟩 Competent · 🟪 Deep Understanding

**Dimensions:** Explain · Build · Debug · Operate · Design

## Evidence rules

- **Learning:** can follow the intuition and mechanism, run a guided proof, and identify current gaps.
- **Practicing:** can build and debug with limited guidance; evidence is repeatable.
- **Competent:** can independently build, debug, operate, and make sound routine design decisions.
- **Deep Understanding:** can reason from internals, handle novel failure, quantify tradeoffs, teach others, and improve the surrounding system.
- A rating should link to evidence in a lab, project, incident review, design document, talk, or production outcome.
- The weakest relevant dimension limits an overall domain claim. Strong explanation does not substitute for operational experience.
- Completion of a file changes no rating by itself.

## First evidence

After the Day 1 path in [START-HERE.md](START-HERE.md), add:

| Date | Concept | Prediction | Observation | Model corrected | Teach-back score | Evidence link |
|---|---|---|---|---|---:|---|
| YYYY-MM-DD | Software execution | What did you expect? | What happened? | What changed? | /16 | Lab note |

## Competency Matrix

| Domain | Explain | Build | Debug | Operate | Design | Evidence / next proof |
|---|---:|---:|---:|---:|---:|---|
| [History](00-history/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Explain why three major systems exist and support each account with a mechanism |
| [Software Foundations](01-software-foundations/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Complete [execution lab](labs/01-software-execution/README.md) and explain one failure chain |
| [Python](02-python/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Ship a tested CLI; profile it; explain object and exception behavior |
| [Computer Systems](03-computer-systems/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Measure cache and memory effects; explain the observed limit |
| [Linux](04-linux/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Diagnose a bounded process, memory, permission, or disk fault |
| [Git](05-git/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Recover a lost commit and resolve a conflict while preserving intent |
| [Data Structures and Algorithms](06-data-structures-algorithms/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Implement, test, and benchmark structures under two workloads |
| [Networking](07-networking/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Trace and diagnose a DNS, TCP, TLS, or HTTP request failure |
| [Databases](08-databases/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Explain a query plan and reproduce an isolation or locking anomaly |
| [Backend Engineering](09-backend-engineering/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Operate a tested API with persistence, auth, telemetry, and overload limits |
| [Go](10-go/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Build a cancellable concurrent service and investigate its profile |
| [Software Architecture](11-software-architecture/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Defend an ADR with quality attributes, alternatives, and revisit triggers |
| [AWS](12-aws/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Review identity, network, data, failure-domain, and cost boundaries |
| [DevOps](13-devops/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Demonstrate a delivery path with provenance, promotion, rollback, and feedback |
| [Terraform](14-terraform/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Review a plan, recover drift safely, and explain state ownership |
| [Containers](15-containers/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Build and inspect an image; diagnose isolation or resource behavior |
| [Kubernetes](16-kubernetes/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Diagnose a workload across API, scheduler, network, storage, and runtime |
| [Distributed Systems](17-distributed-systems/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Demonstrate partial failure, idempotency, and bounded retry behavior |
| [Observability](18-observability/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Instrument and investigate a request with correlated telemetry |
| [SRE](19-sre/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Write an SLO and use burn evidence to make a release decision |
| [Security](20-security/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Produce a threat model, verify controls, and state residual risk |
| [Platform Engineering](21-platform-engineering/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Validate a platform capability with users, contracts, and outcome metrics |
| [Developer Platforms](22-developer-platforms/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Build and test a self-service workflow with ownership and escape hatches |
| [Control Planes](23-control-planes/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Implement an idempotent reconciler and recover interrupted work |
| [AI Foundations](24-ai-foundations/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Derive and test an optimization or probability claim on small data |
| [ML and Deep Learning](25-ml-deep-learning/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Train, evaluate, and debug a model against a documented baseline |
| [Transformers and LLMs](26-transformers-llms/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Explain and inspect tokenization, attention, generation, and memory use |
| [LLM Engineering](27-llm-engineering/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Build an evaluated application with structured, retrieval, safety, and cost tests |
| [MLOps](28-mlops/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Reproduce a model artifact from versioned code, data identity, and configuration |
| [GPU Systems](29-gpu-systems/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Explain a profile and distinguish compute, memory, launch, and communication limits |
| [AI Infrastructure](30-ai-infrastructure/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Design a scheduled accelerator workload with topology, storage, and recovery evidence |
| [Model Serving](31-model-serving/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Produce load curves and demonstrate admission control, rollout, and recovery |
| [AI Platform Engineering](32-ai-platform-engineering/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Design a multi-tenant lifecycle with quotas, policy, lineage, and operator ownership |
| [Agentic Infrastructure](33-agentic-infrastructure/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Run a durable, permission-bounded workflow and recover a duplicate or interrupted action |
| [System Design](34-system-design/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Complete and review a quantified design under changed assumptions |
| [Senior and Staff Engineering](35-senior-staff-engineering/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Produce a strategy, decision record, risk plan, and outcome review |

## Review log

| Date | Domain | Previous level and new level | Evidence | Gap exposed |
|---|---|---|---|---|
| YYYY-MM-DD | Example | Learning; now Practicing in Build | Link to lab or project | Describe the next concrete proof |

Review this file after completing a lab, resolving an incident, shipping a project milestone, teaching a concept, or discovering that an earlier rating was too generous. Downgrading a rating when evidence changes is sound engineering.

Use [TEACH-BACK.md](TEACH-BACK.md) to score explanations. Use [ROADMAP.md](ROADMAP.md) to decide whether the next stage’s prerequisite evidence exists.
