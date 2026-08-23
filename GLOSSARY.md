# Glossary

Definitions are short enough to use while reading and precise enough to support later lessons. Use [CONCEPT-INDEX.md](CONCEPT-INDEX.md) for the deeper curriculum path.

## A

### Abstraction

A simpler way to use something without thinking about all of its machinery at once. A contract that exposes selected behavior while hiding implementation details; hidden details can still leak through limits, performance, and failure.

**Start with:** [Why Software Exists](00-history/02-why-software-exists.md)

### Agent

Software that repeatedly looks at a situation, chooses an allowed action, and checks what happened while pursuing a goal. A policy- and resource-bounded execution loop combining model decisions, tools, state, control flow, evaluation, and optional human approval.

**Start with:** [Agentic Engineering](00-history/20-agentic-engineering.md)

### API

A contract through which one system asks another to perform work or expose state. An API defines valid operations, representations, errors, compatibility expectations, and often authentication and rate limits; the transport is only one part of the contract.

**Start with:** [Backend Engineering](09-backend-engineering/README.md)

### Assembly language

Human-readable names for the small instructions a processor understands. A symbolic representation of machine instructions and addresses translated by an assembler into machine code for an instruction-set architecture.

**Start with:** [Machine Code to Assembly](00-history/03-machine-code-assembly-high-level-languages.md)

## B

### Backpressure

A system’s way of preventing incoming work from outrunning its ability to complete work. Backpressure may delay, reject, shed, or reduce work, but it must remain bounded and visible to callers.

**Start with:** [Distributed Systems](17-distributed-systems/README.md)

### Bytecode

Compact intermediate instructions meant for a language runtime rather than directly for the physical CPU. An instruction representation for a virtual machine or interpreter; CPython code objects contain Python bytecode that native CPython code evaluates.

**Start with:** [How Software Actually Executes](01-software-foundations/01-how-software-actually-executes.md)

## C

### Cache

A faster copy or computed result kept closer to expected use. A cache trades freshness, memory, invalidation complexity, and miss cost for lower latency or reduced load; it is not the source of truth unless explicitly designed as one.

**Start with:** [Computer Systems](03-computer-systems/README.md)

### Compiler

A translator that turns one form of program into another. A system that transforms a source representation into a target representation while preserving the source language’s defined semantics.

**Start with:** [Machine Code to Assembly](00-history/03-machine-code-assembly-high-level-languages.md)

### Container

A standard application package run in a separated area of a shared machine. An isolated process or process group launched from an image; on Linux it uses namespaces, cgroups, mounts, capabilities, and runtime conventions while sharing the host kernel.

**Start with:** [Containers](00-history/12-containers.md)

### Consistency

The rules governing which values an operation may observe when data has multiple copies or concurrent updates. Consistency is a family of contracts, not a single strength setting, and must be stated per operation and failure model.

**Start with:** [Distributed Systems](17-distributed-systems/README.md)

### Continuous batching

An inference scheduling method that adds ready sequences and removes completed ones between model iterations instead of waiting for one fixed request batch to finish. It improves accelerator occupancy under variable sequence lengths, but admission, prefill work, fairness, and KV-cache capacity still bound latency and throughput.

**Start with:** [KV Cache and Continuous Batching](31-model-serving/05-kv-cache-and-continuous-batching.md)

### Control plane

The part of a system that accepts what you want, decides what should happen, and keeps checking the result. Components that expose intent APIs, persist desired state, make decisions, and reconcile or configure data-plane resources.

**Start with:** [Kubernetes](00-history/13-kubernetes.md)

### CPU

The physical processor that performs a computer’s general-purpose instruction steps. A processor that fetches, decodes, and executes instructions while operating on registers and interacting with caches, memory, and devices.

**Start with:** [Origins of Computing](00-history/01-origins-of-computing.md)

## D

### Database

A disciplined shared record keeper that helps people find and change information without losing agreed facts. A managed system for storing and retrieving data while providing selected guarantees for structure, concurrency, integrity, durability, and recovery.

**Start with:** [Databases](00-history/08-databases.md)

### Distributed system

A system made from computers that coordinate by sending messages and can fail separately. A system whose components communicate over a network under independent failure, variable delay, and incomplete knowledge.

**Start with:** [Distributed Systems](00-history/09-distributed-systems.md)

## E

### Effect reconciliation

The process of comparing durable intent with the observed state of an external side effect, then safely completing, retrying, compensating, or recording that effect. It uses stable operation identity and re-observation to resolve timeouts and crash windows without assuming that an unknown outcome failed.

**Start with:** [Durable Execution and Effect Reconciliation](33-agentic-infrastructure/06-durable-execution-and-reconciliation.md)

### Evaluation gate

A versioned release rule that requires specified evidence for an exact artifact before promotion. The gate binds evaluation suites, metrics, slices, thresholds, safety or compliance checks, and approvals to the candidate digest; missing or stale evidence is not a pass.

**Start with:** [AI Platform Engineering](00-history/19-ai-platform-engineering.md)

## F

### Feature store

A system that manages governed feature definitions and serves feature values for training and inference under contracts for entity identity, event time, freshness, transformation version, and access. It does not by itself guarantee point-in-time correctness or offline-online consistency; those properties require validated data and retrieval semantics.

**Start with:** [Data and Feature Platform Contracts](32-ai-platform-engineering/04-data-and-feature-platform-contracts.md)

### File descriptor

A small number a process uses as a handle for an open input or output route. A per-process integer referring to an open kernel-managed object such as a file, pipe, terminal, socket, or device.

**Start with:** [How Software Actually Executes](01-software-foundations/01-how-software-actually-executes.md)

## I

### Idempotency

The property that repeating an operation with the same identity has no additional intended effect after the first successful application. Implementations usually require durable deduplication state, not merely an HTTP method label.

**Start with:** [Backend Engineering](09-backend-engineering/README.md)

### Interpreter

A program that carries out instructions written in another program representation. A system that directly implements the semantics of an input representation, often after parsing or compiling it into an intermediate form.

**Start with:** [How Software Actually Executes](01-software-foundations/01-how-software-actually-executes.md)

## K

### KV cache

The per-sequence attention state that stores previously computed key and value tensors so an autoregressive model can decode a new token without recomputing the full prefix. Its memory grows with cached tokens, layers, KV heads, head dimension, and element size, so it often governs serving concurrency.

**Start with:** [KV Cache and Continuous Batching](31-model-serving/05-kv-cache-and-continuous-batching.md)

### Kernel

The protected manager that controls shared hardware and the boundaries between programs. The privileged core of an operating system that manages scheduling, memory, devices, filesystems, protection, and system-call interfaces.

**Start with:** [Evolution of Operating Systems](00-history/05-evolution-of-operating-systems.md)

### Kubernetes

A system that repeatedly corrects a cluster toward the application state you declared. An extensible API-driven distributed control plane that reconciles desired and observed workload and infrastructure state.

**Start with:** [Kubernetes](00-history/13-kubernetes.md)

## L

### Large language model (LLM)

A model trained on text patterns to predict the next token and generate sequences. A high-capacity parameterized model trained to estimate token-sequence distributions, often adapted for instruction following and tool use.

**Start with:** [Transformers and LLMs](00-history/17-transformers-and-llms.md)

### Latency

Elapsed time for one unit of work, measured between stated boundaries. Useful latency claims include a workload, percentile, window, and treatment of failures; an average alone hides tail behavior.

**Start with:** [Observability](18-observability/README.md)

### Lineage

The recorded provenance connecting an artifact or result to its resolved inputs, transformations, code, environment, execution attempts, evaluations, approvals, and derived outputs. Useful lineage uses immutable identities and supports reproducibility, comparison, policy enforcement, incident analysis, and recall.

**Start with:** [AI Platform Engineering](00-history/19-ai-platform-engineering.md)

## M

### Machine code

The bit patterns a particular kind of processor can execute directly. Binary-encoded instructions and operands defined by a processor instruction-set architecture.

**Start with:** [Machine Code to Assembly](00-history/03-machine-code-assembly-high-level-languages.md)

### Machine learning

Fitting behavior from examples instead of writing every rule by hand. Optimizing a parameterized model against data and an objective so it generalizes measured behavior to new inputs.

**Start with:** [Machine Learning](00-history/16-machine-learning.md)

### Model serving

The runtime system that accepts prediction requests, prepares inputs, schedules model execution, and returns outputs under latency, throughput, quality, reliability, and cost constraints.

**Start with:** [Model Serving](31-model-serving/README.md)

## O

### Observability

The ability to understand what a system is doing from useful evidence it exposes. A system property that enables investigation of internal behavior from telemetry, state, and debuggable interfaces, including questions not anticipated in advance.

**Start with:** [SRE and Observability](00-history/14-sre-and-observability.md)

### Operating system

Software that safely shares a computer and gives programs common ways to use it. System software that multiplexes hardware resources, enforces protection, and exposes abstractions such as processes, files, virtual memory, and sockets.

**Start with:** [Evolution of Operating Systems](00-history/05-evolution-of-operating-systems.md)

## P

### Prefix cache

A serving cache that reuses model state computed for an exact token prefix across eligible requests. Correct reuse keys include the model, tokenizer, and other interpretation-changing state, while tenant and privacy boundaries constrain sharing; a hit is valuable in proportion to tokens and computation reused.

**Start with:** [KV Cache and Continuous Batching](31-model-serving/05-kv-cache-and-continuous-batching.md)

### Process

One active, OS-managed run of a program. An operating-system execution context with an identity, virtual address space, resources, security credentials, state, and one or more threads.

**Start with:** [How Software Actually Executes](01-software-foundations/01-how-software-actually-executes.md)

## Q

### Quota

An enforced upper bound on a tenant's admitted or concurrent use of named resources over a stated scope and window. Quota limits blast radius and supports fairness, but it is distinct from a budget, which triggers spending decisions, and from capacity, which describes resources that physically exist.

**Start with:** [Tenancy, Governance, and Cost](32-ai-platform-engineering/02-tenancy-governance-and-cost.md)

## R

### Reconciliation

Repeatedly compare what should exist with what does exist, then take a safe step to close the gap. A control loop that observes desired and actual state and performs idempotent actions toward convergence.

**Start with:** [Kubernetes](00-history/13-kubernetes.md)

### Runtime

The machinery that supports a program while it runs. Services and implementation machinery for execution, potentially including interpretation, compilation, allocation, garbage collection, libraries, and interfaces to the operating system.

**Start with:** [How Software Actually Executes](01-software-foundations/01-how-software-actually-executes.md)

## S

### Scheduler

The decision maker that chooses which ready work gets a resource next. A subsystem that selects runnable work for constrained execution resources such as CPUs, cluster nodes, or accelerators according to policy and state.

**Start with:** [Evolution of Operating Systems](00-history/05-evolution-of-operating-systems.md)

### Service-level indicator (SLI)

A number that measures behavior users care about. A quantitative measure of service behavior, such as the proportion of valid requests completed successfully within a latency threshold.

**Start with:** [SRE and Observability](00-history/14-sre-and-observability.md)

### Service-level objective (SLO)

A reliability target for a user-relevant measurement over a stated period. A target range or threshold for an SLI over a defined window, used to govern reliability expectations and tradeoffs.

**Start with:** [SRE and Observability](00-history/14-sre-and-observability.md)

### System call

A controlled request from an ordinary program to the protected operating-system kernel. A defined transition through which a user-space thread requests a kernel service such as I/O, mapping memory, or process operations.

**Start with:** [How Software Actually Executes](01-software-foundations/01-how-software-actually-executes.md)

## T

### Tensor

A multidimensional array together with a shape, element type, layout, and device placement. Machine learning runtimes apply vectorized operations to tensors and track the storage and dependency information needed for execution and differentiation.

**Start with:** [AI Foundations](24-ai-foundations/README.md)

### Thread

One sequence of execution within a process. A schedulable execution stream with registers and a stack that usually shares its process’s address space and resources with other threads.

**Start with:** [How Software Actually Executes](01-software-foundations/01-how-software-actually-executes.md)

### Token

A discrete symbol identifier produced by a tokenizer from text or another modality. A token is not necessarily a word; tokenization affects sequence length, cost, representational boundaries, and model-visible input.

**Start with:** [Transformers and LLMs](26-transformers-llms/README.md)

### Trace

A record of causally related work across process and service boundaries, represented as spans with timing, attributes, status, and parent relationships. Trace context propagates the identity needed to connect those spans.

**Start with:** [Observability](18-observability/README.md)

### Transformer

A neural-network architecture that learns which other tokens matter when processing each token. A sequence-model architecture centered on attention and position-wise transformations, enabling parallel training over token sequences.

**Start with:** [Transformers and LLMs](00-history/17-transformers-and-llms.md)

## V

### Virtualization

Making physical resources look like isolated logical machines or environments. Mediating hardware or resource interfaces to create isolated logical computing environments decoupled from their physical implementation.

**Start with:** [Virtualization and Cloud](00-history/10-virtualization-and-cloud.md)

### Virtual memory

The private address map a process uses instead of naming physical RAM locations directly. A process-visible address space translated by hardware and the OS to physical pages, files, shared mappings, or no current backing.

**Start with:** [How Software Actually Executes](01-software-foundations/01-how-software-actually-executes.md)
