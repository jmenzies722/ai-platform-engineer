# Module-Mapped Interview Question Bank

Use this bank after producing evidence in the corresponding module. The interviewer should change one constraint after the first answer. The candidate should reason from mechanisms and evidence rather than repeat a prepared architecture.

## How to run a session

1. Select one mechanism question and one practical prompt.
2. Give the candidate time to establish scope and assumptions.
3. Ask for observable evidence before accepting a diagnosis.
4. Change a load, failure, security, or cost constraint.
5. Score the model, not product-name recall.

A strong answer is explicit about boundaries, uncertain claims, failure behavior, and what measurement would change the decision.

## Foundations

### 00 History

**Question:** Choose containers, cloud APIs, or transformers. Which earlier constraints made it possible, and which older idea does it reuse?

**Strong evidence:** Separates historical cause from chronology and connects the account to a working mechanism.

**Follow-up:** Name a current limitation inherited from that history.

### 01 Software foundations

**Question:** A Python program is stored on disk but is not running. Explain what must exist before it can consume CPU and write a byte.

**Strong evidence:** Distinguishes source, runtime, process, address space, scheduler, system call, descriptor, and device without claiming that every implementation is identical.

**Practical prompt:** Given a PID, identify three observations that establish activity and three that do not establish progress.

### 02 Python

**Question:** Explain why two names may observe the same mutable object and how you would protect an API from accidental aliasing.

**Strong evidence:** Uses Python’s object and binding model, copy choices, immutable boundaries, typing, tests, and ownership documentation.

**Follow-up:** Adapt the design for an iterator that owns a file descriptor.

### 03 Computer systems

**Question:** Why can sequential access outperform random access even when both perform the same number of operations?

**Strong evidence:** Connects locality, cache lines, translation, prefetching, memory bandwidth, and measurement noise.

**Practical prompt:** Design a bounded benchmark that could disprove the candidate’s bottleneck claim.

### 04 Linux

**Question:** A service is present in the process table but users receive timeouts. How do you narrow the fault?

**Strong evidence:** Checks scheduling, blocked state, descriptors, sockets, memory pressure, logs, dependencies, and recent changes in a safe order.

**Follow-up:** The host is nearly out of disk and restarting may worsen recovery.

### 05 Git

**Question:** A teammate says a commit was lost after a rebase. Explain Git’s object model and a safe recovery.

**Strong evidence:** Uses refs, reachability, reflogs, object identity, a preservation branch, and review before history changes.

**Practical prompt:** Recover the commit in a disposable repository without rewriting a shared remote.

### 06 Data structures and algorithms

**Question:** Choose a data structure for bounded admission control with priority and expiry.

**Strong evidence:** Defines operations and workload first, compares complexity and memory, handles concurrency, and tests invariants.

**Follow-up:** Memory is capped and approximate eviction is acceptable.

## Services and data

### 07 Networking

**Question:** A hostname works from one subnet and fails from another. Trace the investigation.

**Strong evidence:** Separates resolver configuration, authoritative data, routing, ACLs, transport, TLS identity, proxies, and application response.

**Practical prompt:** Explain what packet capture can prove and what encrypted payloads leave uncertain.

### 08 Databases

**Question:** A query became slow after data volume increased. What evidence distinguishes a missing index from lock wait, stale statistics, or storage pressure?

**Strong evidence:** Uses plans, actual timing, row estimates, wait events, transaction scope, buffer evidence, and workload-aware index costs.

**Follow-up:** The proposed index would block or overload production.

### 09 Backend engineering

**Question:** Design an idempotent API that starts background work.

**Strong evidence:** Defines request identity, durable state transitions, transaction boundaries, duplicate handling, status retrieval, authorization, and retention.

**Practical prompt:** Diagnose a queue backlog without assuming consumers are slow.

### 10 Go

**Question:** A Go service leaks goroutines during downstream timeouts. Explain the likely ownership mistake.

**Strong evidence:** Discusses cancellation propagation, channel ownership, blocked sends, deadlines, cleanup, profiles, and race testing.

**Follow-up:** Some work must survive client cancellation.

### 11 Software architecture

**Question:** When should two capabilities share a deployment but retain separate internal boundaries?

**Strong evidence:** Reasons from change coupling, data ownership, failure isolation, latency, team ownership, and migration cost rather than equating boundaries with services.

**Practical prompt:** Write the decision and a measurable revisit trigger.

## Cloud, delivery, and reliability

### 12 AWS

**Question:** Review a public API design across identity, network, compute, data, failure domains, and cost.

**Strong evidence:** Uses explicit trust boundaries, least privilege, regional assumptions, quotas, recovery objectives, telemetry, and cost drivers.

**Follow-up:** A region becomes unavailable while the database remains healthy in another region.

### 13 DevOps

**Question:** What makes a deployment pipeline evidence-producing rather than a sequence of scripts?

**Strong evidence:** Covers immutable artifacts, provenance, test layers, promotion, approvals, environment parity, observation, rollback, and learning.

**Practical prompt:** Stop a bad rollout while preserving evidence.

### 14 Terraform

**Question:** Why is Terraform state operationally sensitive, and how would you recover from partial application?

**Strong evidence:** Explains identity mapping, dependency graph, locking, remote state controls, refresh, import, plan review, and avoidance of blind state edits.

**Follow-up:** A resource was changed manually during an incident.

### 15 Containers

**Question:** What isolation does a Linux container provide, and what does it still share?

**Strong evidence:** Covers namespaces, cgroups, capabilities, seccomp, filesystem mounts, image trust, and the host kernel.

**Practical prompt:** Diagnose a container killed under a memory limit.

### 16 Kubernetes

**Question:** A Deployment has desired replicas but no Ready endpoints. Investigate from API intent to traffic.

**Strong evidence:** Reads conditions and events, scheduler decisions, image/runtime state, probes, resources, Services, endpoints, policy, and node health.

**Follow-up:** The rollout must continue without violating disruption limits.

### 17 Distributed systems

**Question:** Explain why a timeout does not establish failure and how an API should handle the ambiguity.

**Strong evidence:** Covers partial failure, retries, idempotency, durable identity, deduplication, reconciliation, and bounded uncertainty.

**Practical prompt:** Break a retry loop that amplifies an overloaded dependency.

### 18 Observability

**Question:** Design telemetry for a request that crosses an asynchronous queue.

**Strong evidence:** Preserves context intentionally, defines semantic attributes, controls cardinality and sampling, and links telemetry to a diagnostic question.

**Follow-up:** Telemetry volume must be cut in half without losing incident utility.

### 19 SRE

**Question:** Define an SLO for interactive inference and explain how it changes release decisions.

**Strong evidence:** States eligible events, success and latency thresholds, windows, exclusions, burn alerts, error-budget policy, and user consequences.

**Practical prompt:** Choose between rollback and graceful degradation during fast burn.

### 20 Security

**Question:** Threat-model a multi-tenant build or model-serving platform.

**Strong evidence:** Identifies assets, actors, entry points, trust boundaries, abuse paths, preventive and detective controls, and residual risk.

**Follow-up:** A privileged control-plane identity is compromised.

## Platforms and control planes

### 21 Platform engineering

**Question:** How do you know a paved road is a product rather than centrally imposed infrastructure?

**Strong evidence:** Uses user research, contracts, supported journeys, escape hatches, ownership, adoption, reliability, lead-time, and support-load evidence.

**Follow-up:** Adoption is high but teams report rising cognitive load.

### 22 Developer platforms

**Question:** Design a service-creation workflow that remains useful after the first commit.

**Strong evidence:** Connects catalog ownership, templates, policy, delivery, runtime evidence, scorecards, maintenance, and lifecycle removal.

**Practical prompt:** Evolve a template without silently breaking existing services.

### 23 Control planes

**Question:** Design a reconciler for a durable external resource.

**Strong evidence:** Defines desired and observed state, idempotency, ownership, finalization, status conditions, retries, queue discipline, API evolution, and recovery.

**Follow-up:** The process crashes after the external side effect but before status persistence.

## AI systems

### 24 AI foundations

**Question:** Why can an improving training objective fail to improve the product decision?

**Strong evidence:** Separates objective, data distribution, estimator, uncertainty, calibration, metric, threshold, and real-world cost.

**Practical prompt:** Construct a small counterexample with asymmetric error cost.

### 25 Machine learning and deep learning

**Question:** A neural model beats the baseline offline but regresses after release. Structure the investigation.

**Strong evidence:** Checks data contracts, leakage, skew, segment metrics, calibration, serving parity, drift, feedback, and baseline reproducibility.

**Follow-up:** Labels arrive thirty days late.

### 26 Transformers and LLMs

**Question:** Explain the work and memory growth during autoregressive generation.

**Strong evidence:** Covers tokenization, attention, prefill, decode, KV cache, sequence length, batching, and model architecture without treating all runtimes alike.

**Practical prompt:** Explain which observation distinguishes compute saturation from memory pressure.

### 27 LLM engineering

**Question:** Design an evaluated retrieval-backed assistant for a high-consequence domain.

**Strong evidence:** Decomposes retrieval, context construction, generation, structured validation, citations, permissions, refusal, evaluation, latency, and cost.

**Follow-up:** Retrieved documents contain malicious instructions.

### 28 MLOps

**Question:** What information is required to reproduce and promote a model artifact?

**Strong evidence:** Names code, data identity, features, environment, configuration, seeds, training evidence, evaluation, lineage, approval, and rollback.

**Practical prompt:** Investigate why a rerun differs despite the same source commit.

### 29 GPU systems

**Question:** A GPU shows high utilization but poor useful throughput. What might the metric hide?

**Strong evidence:** Distinguishes occupancy, memory stalls, kernel mix, launch overhead, synchronization, communication, padding, and useful application work.

**Follow-up:** Failures appear only when two tenants share the node.

### 30 AI infrastructure

**Question:** Design scheduling for distributed training across a heterogeneous GPU fleet.

**Strong evidence:** Includes gang placement, topology, data path, quotas, fairness, fragmentation, checkpointing, failure domains, and capacity economics.

**Practical prompt:** Recover a job after one worker and its local cache are lost.

### 31 Model serving

**Question:** Explain the latency and throughput effects of continuous batching.

**Strong evidence:** Discusses admission, queueing, prefill/decode interaction, KV memory, fairness, tail latency, overload, and workload shape.

**Follow-up:** A long-context tenant starves short interactive requests.

### 32 AI platform engineering

**Question:** Define the contracts of a multi-tenant training and serving platform.

**Strong evidence:** Covers identity, data and artifact lineage, quotas, scheduling, evaluation gates, release, policy, observability, cost allocation, and operator ownership.

**Practical prompt:** Decide which capability belongs in a control plane and which remains team-owned.

### 33 Agentic infrastructure

**Question:** Design durable execution for an agent that may cause external side effects.

**Strong evidence:** Uses bounded tools, capability identity, approvals, durable step state, idempotency, replay rules, audit, budget, cancellation, and evaluation.

**Follow-up:** The runtime loses acknowledgement after a payment tool succeeds.

## Design and leadership

### 34 System design

**Question:** Design a regional model-serving platform under explicit latency, availability, privacy, and budget constraints.

**Strong evidence:** Quantifies demand, defines boundaries and data, models failure, overload and recovery, addresses security and telemetry, compares alternatives, and plans evolution.

**Follow-up:** Traffic grows tenfold while GPU supply remains fixed.

### 35 Senior and Staff engineering

**Question:** Several teams need an AI platform, disagree on the interface, and each has a partial solution. What do you do in the first six weeks?

**Strong evidence:** Frames users and outcomes, maps stakeholders and existing systems, creates decision evidence, sequences reversible work, names risks and non-goals, and builds an operating mechanism rather than claiming authority.

**Follow-up:** An executive mandates a launch date that the evidence does not support.

## Scoring record

| Dimension | Weak | Working | Strong |
|---|---|---|---|
| Requirements | Assumes the problem | Asks basic scope questions | Quantifies users, workload, constraints, and non-goals |
| Mechanism | Names products | Explains the common path | Explains state, boundaries, internals, and uncertainty |
| Failure | Lists generic risks | Handles one expected fault | Reasons across correlated faults, overload, and recovery |
| Evidence | Relies on intuition | Names useful telemetry | Designs a bounded observation that can disprove the claim |
| Tradeoffs | Declares a preference | Compares two choices | States decision, cost, rejected options, and revisit trigger |
| Communication | Produces a monologue | Gives a structured answer | Adapts depth, checks alignment, and makes uncertainty legible |
