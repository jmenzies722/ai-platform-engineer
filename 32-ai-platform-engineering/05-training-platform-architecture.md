# Training platform architecture

A training platform converts declared experiment intent into reproducible, schedulable, observable, and recoverable runs.

## Why it matters

Notebook success does not establish artifact lineage, resource fairness, resumability, or production suitability. Distributed training also creates coordinated failure: one missing worker can idle an entire gang, a retry can multiply spend, and a checkpoint that exists but lacks optimizer or sampler state can resume into a different experiment. The platform must make these mechanics explicit without forcing every user to operate the scheduler.

## How it works

A versioned `TrainingRun` contract names code and image digests, resolved data manifests, transformation versions, hyperparameters, seed, hardware and topology constraints, worker count, distribution strategy, owner, budget, deadline, checkpoint policy, and declared outputs. Admission authenticates the caller, resolves mutable references, checks policy and quota, estimates feasibility, and records immutable desired state. Acceptance means eligible for scheduling, not that capacity is immediately available.

A queue applies a documented fairness policy such as weighted fair share with reservations and aging. The scheduler performs gang placement so all required workers start on compatible topology; otherwise partial allocation wastes accelerators. A run controller reconciles attempts, worker membership, rendezvous, health, progress, checkpoint, cancellation, and terminal state. The platform records requested and resolved node type, accelerator, driver, runtime, image, data, and policy because a logical request alone cannot reproduce execution.

Checkpoints are a protocol, not just files. Workers write to an attempt-specific temporary location, include model, optimizer, scheduler, scaler, random-number, sampler, and progress state as applicable, verify shard completeness and checksums, then atomically publish a manifest. Resume validates code, topology, format, and data compatibility. A `checkpoint_written` log line proves neither completeness nor resumability; only restore and bounded continuation tests support that claim.

Retries classify failure. Node loss, preemption, and transient storage errors may justify a fresh attempt with exponential backoff and a retry budget. Invalid examples, deterministic out-of-memory at the declared shape, and user-code exceptions should become actionable terminal conditions rather than consume the fleet repeatedly. Cancellation stops admission, coordinates workers, publishes only validated artifacts, and reconciles external effects. A model is registered only after the output manifest and lineage transaction commit; worker exit code zero is insufficient.

## See it yourself

Run identical code and seed twice with an unpinned base image, resolving it before each run. Different image digests establish environment drift. Pinning one digest removes that source of variation, but does not prove numeric identity because data, hardware, parallel reduction order, kernels, and nondeterministic operations remain. Report reproduction within a declared metric or parameter tolerance and list the unresolved factors rather than promising bitwise equality.

## Where it shows up

Self-service APIs generate launcher configuration, scoped workload identity, data mounts, telemetry, checkpoint locations, and artifact registration. Users see queue reason, resolved resources, per-attempt state, first failing worker, progress age, cost, and terminal evidence without learning every scheduler primitive. Operators see gang fragmentation, queue wait by tenant, useful accelerator time, checkpoint throughput, and retry waste.

## When it breaks

Controllers retry deterministic failures, stale heartbeats kill healthy slow workers, checkpoints omit sampler state, logs leak examples, quota covers GPUs but not checkpoint storage, and artifact publication races job termination. Debug in causal order: admission decision, queue reason, placement, worker launch, rendezvous, first failing event, peer cancellation, checkpoint commit, and publication. Preserve attempt-level lineage; later worker errors may only be consequences. Compare requested with resolved state and distinguish capacity waiting from scheduler deadlock. Never mark success until every declared artifact validates.

## Practice

**Observe:** compare requested and resolved manifests and account for queue, compute, checkpoint, and retry time. **Build:** specify state transitions from admission through atomic artifact publication, including idempotent cancellation. **Break:** inject node loss, a partial checkpoint, deterministic bad sample, rendezvous timeout, and publication crash. Completion requires bounded retries, successful restore proof, no orphan registration, and a reproducible failure report naming the first cause.

## Check yourself

1. Why record resolved environment identity?
2. Which failures merit a fresh node?
3. What makes an artifact publication atomic?

## Sources

### REQUIRED

- [Kubeflow Training Operator](https://www.kubeflow.org/docs/components/trainer/)
- [Kubernetes controllers](https://kubernetes.io/docs/concepts/architecture/controller/)

### RECOMMENDED

- [MLflow tracking concepts](https://mlflow.org/docs/latest/ml/tracking/)

### DEEP DIVE

- [PyTorch distributed checkpoint](https://docs.pytorch.org/docs/stable/distributed.checkpoint.html)
- [PyTorch reproducibility](https://docs.pytorch.org/docs/stable/notes/randomness.html)

## Next

Continue to [Serving platform architecture](06-serving-platform-architecture.md).
