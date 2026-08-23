# Practical lab: design an AI platform control plane

Design and simulate a small control plane that admits training and serving intents, preserves lineage, enforces tenant policy, and records cost and operations.

## Why it matters

Platform diagrams often omit state transitions and failure semantics. A runnable model exposes ownership, retries, policy timing, and publication boundaries.

## How it works

Use Python standard-library dataclasses for `Dataset`, `TrainingRun`, `Model`, `Evaluation`, and `Deployment`. Store append-only JSON events and derive current state by replay. Commands carry trusted principal and idempotency key. Admission checks immutable identities, quota, required lineage, evaluation gates, and budget before recording intent.

Implement transitions for dataset publication, training start and checkpoint, model registration, evaluation, approval, canary, promotion, rollback, and retirement. Meter synthetic GPU-seconds, tokens, and storage to the principal-derived cost center.

## See it yourself

Replay one successful path and prove every deployed digest reaches an approved evaluation and source manifest. Crash after recording a deployment intent but before acknowledgement; retry with the same key and show one effect. Change the model digest after evaluation and verify promotion fails.

## Where it shows up

The simulator mirrors production controllers, policy engines, registries, and audit systems while remaining safe enough for design review and incident exercises.

## When it breaks

Do not trust tenant labels as identity, mutate past events, expose data in billing logs, or retry ambiguous effects blindly. Inject policy unavailability and choose fail-closed behavior for promotion while preserving read access and emergency rollback.

## Practice

**Build:** implement the state machine with twenty tests and deterministic replay. **Break:** attempt cross-tenant access, orphan registration, stale approval, quota exhaustion, duplicate commands, partial publication, and policy outage. **Explain back:** trace one model through data, training, evaluation, serving, rollback, cost, and ownership. Completion requires zero unauthorized transitions and exact replayed state.

## Check yourself

1. Why derive billing identity from trusted context?
2. Which operations may remain during policy outage?
3. What event makes rollback auditable?

## Sources

### REQUIRED

- [Open Policy Agent documentation](https://www.openpolicyagent.org/docs/latest/)

### RECOMMENDED

- [Kubernetes operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)

### DEEP DIVE

- [in-toto attestation framework](https://in-toto.io/)

## Next

Continue to [Agentic Infrastructure](../33-agentic-infrastructure/README.md).
