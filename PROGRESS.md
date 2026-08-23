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

## Assessment gate outcomes

Use the [common assessment rubric](assessments/rubric.md) to record the evaluator's outcome and five-score vector. Gate scores use 0–3 and do not replace the domain ratings below. Record Pass, Rework, or Stop exactly; never average a weak dimension into a passing result.

| Gate | Date | Outcome | Explain | Build | Debug | Operate | Design | Evidence packet, evaluator, and next proof |
|---|---|---|---:|---:|---:|---:|---:|---|
| [Foundations](assessments/gates/foundations.md) |  |  |  |  |  |  |  |  |
| [Systems, Linux, and Networking](assessments/gates/systems-linux-networking.md) |  |  |  |  |  |  |  |  |
| [Cloud Delivery](assessments/gates/cloud-delivery.md) |  |  |  |  |  |  |  |  |
| [Kubernetes Reliability](assessments/gates/kubernetes-reliability.md) |  |  |  |  |  |  |  |  |
| [Platform](assessments/gates/platform.md) |  |  |  |  |  |  |  |  |
| [AI Platform](assessments/gates/ai-platform.md) |  |  |  |  |  |  |  |  |
| [Staff](assessments/gates/staff.md) |  |  |  |  |  |  |  |  |

For Rework, retain passed claims and name the smallest fresh proof required. For Stop, record containment and cleanup without reusing the compromised challenge. Add a dated row or linked assessment record for each later attempt rather than overwriting history. The gate's no-notes explanation is reviewed with [TEACH-BACK.md](TEACH-BACK.md).

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
| [AWS](12-aws/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Review identity, network, data, failure-domain, and cost boundaries; use the [AWS product labs](labs/README.md#aws-dop-c02-gap-labs) for bounded delivery and operations evidence |
| [DevOps](13-devops/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Demonstrate a delivery path with provenance, promotion, rollback, and feedback |
| [Terraform](14-terraform/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Review a plan, recover drift safely, and explain state ownership |
| [Containers](15-containers/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Build and inspect an image; diagnose isolation or resource behavior |
| [Kubernetes](16-kubernetes/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Diagnose a workload across API, scheduler, network, storage, and runtime |
| [Distributed Systems](17-distributed-systems/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Demonstrate partial failure, idempotency, and bounded retry behavior |
| [Observability](18-observability/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Instrument and investigate a request with correlated telemetry |
| [SRE](19-sre/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Write an SLO and use burn evidence to make a release decision |
| [Security](20-security/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Produce a threat model, verify controls, and state residual risk |
| [Platform Engineering](21-platform-engineering/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Run the [adoption experiment](21-platform-engineering/lab-platform-adoption-experiment.md); link reproducible baseline, segment, retention, old-path, support, and stop-decision evidence |
| [Developer Platforms](22-developer-platforms/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Prove one self-service workflow in the [control-plane lab](labs/14-platform-control-plane/README.md), then revise retry and support boundaries from the [retry storm](incidents/08-retry-storm/README.md) |
| [Control Planes](23-control-planes/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Link idempotency, convergence, tenant, and dead-letter proofs from the [control-plane lab](labs/14-platform-control-plane/README.md), plus recovery decisions from [queue overload](incidents/12-queue-overload/README.md) |
| [AI Foundations](24-ai-foundations/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Derive and test an optimization or probability claim on small data |
| [ML and Deep Learning](25-ml-deep-learning/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Train, evaluate, and debug a model against a documented baseline |
| [Transformers and LLMs](26-transformers-llms/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Explain and inspect tokenization, attention, generation, and memory use |
| [LLM Engineering](27-llm-engineering/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Build an evaluated application with structured, retrieval, safety, and cost tests |
| [MLOps](28-mlops/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Link a reproducible run from the [standalone lab](labs/15-ml-reproducibility/README.md), governed rollback from the [release lab](28-mlops/lab-reproducible-release.md), and a corrected canary decision from [bad rollout](incidents/06-bad-rollout/README.md) |
| [GPU Systems](29-gpu-systems/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Link roofline, profile, numerical, memory, and topology evidence from the [performance lab](29-gpu-systems/09-practical-gpu-systems-lab.md), then distinguish OOM causes in the [incident](incidents/11-gpu-oom/README.md) |
| [AI Infrastructure](30-ai-infrastructure/README.md) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Link deterministic cluster events, invariants, queue distributions, checkpoint recovery, and costs from the [cluster lab](30-ai-infrastructure/09-practical-ai-infrastructure-lab.md), then revise capacity from [queue overload](incidents/12-queue-overload/README.md) |
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

Use [TEACH-BACK.md](TEACH-BACK.md) to score explanations and prepare for gate review. Use [ROADMAP.md](ROADMAP.md) to decide whether the next stage’s prerequisite evidence exists, then use the corresponding [assessment gate](assessments/README.md) for a formal claim.
