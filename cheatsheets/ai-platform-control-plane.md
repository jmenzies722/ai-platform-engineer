# AI platform control-plane operator sheet

Trace declared intent through identity, admission, orchestration, artifact
publication, evaluation, deployment, and reconciliation. Treat status as a
claim backed by immutable identities and evidence, not as proof by itself.

## Frame the resource and decision

Record tenant, authenticated principal, resource kind and stable ID, generation,
immutable data, code, environment and model digests, region, owner, policy
version, start time, and recent platform changes. Decide whether the failure is
rejection, queueing, execution, publication, promotion, deployment, drift, or
deletion.

Use the platform API and audit trail as the primary contract. Dashboards and
portals can lag, collapse states, or omit machine-readable reasons.

## Did the API accept valid intent?

Inspect the stored specification, generation, admission decision, field
ownership, conditions, and audit event through approved read-only interfaces.
Preserve exact reason codes for authentication, authorization, schema, policy,
quota, budget, and dependency failures.

Authentication establishes a principal; authorization decides an action.
Quota bounds admitted consumption; a budget creates a spending decision.
Available physical capacity does not override either policy.

Do not bypass admission or edit durable state directly. If policy is
unavailable, use the documented fail-open or fail-closed contract; inventing an
incident exception creates unaudited state.

## Has the latest generation been reconciled?

Compare desired generation with observed generation, condition transition
times, queue age, retry count, controller version, and external resource ID.
Events are hints and may be duplicated, delayed, or absent.

- Desired generation exceeds observed generation: the controller has not
  completed observation of the latest intent.
- Oldest queue age rises across resources: controller capacity or a dependency
  is broadly constrained.
- One key retries while peers converge: terminal intent, poison data, or one
  external object is plausible.
- External state exists but status lacks identity: a crash window or status
  conflict is plausible; observe before creating again.

A reconciler must derive the next step from current desired and external state.
Restarting a controller or replaying an event is not a repair if side effects
are not idempotent.

## Is quota, scheduling, or execution blocking progress?

Follow the same trusted tenant identity through quota decision, scheduler
allocation, workload identity, runtime, storage, and metering. Compare requested
and resolved resource shape, gang placement, queue reason, retry class,
checkpoint, and terminal result.

Quota usage can include GPUs, CPU, memory, storage, online concurrency, tokens,
or provider calls. Increasing one limit can move the failure to another
resource or harm other tenants. Confirm headroom and fairness before any
approved quota change.

For failed execution, preserve the first failing attempt and classify transient
infrastructure separately from deterministic code, data, policy, or contract
failure. Blind retries consume quota and can overwrite useful evidence.

## Are data, features, and artifacts reproducible?

Resolve dataset manifests, schema, checksums, event-time policy, producer,
purpose, access decision, and upstream lineage. For features, compare entity
key, event time, freshness, null behavior, transformation version, and
offline-online consistency.

A feature-store lookup succeeding does not prove freshness or point-in-time
correctness. A mutable path is not a dataset identity. Quarantine bad versions;
do not overwrite artifacts that existing lineage references.

Artifact publication should be atomic and bind output digest to run, attempt,
resolved inputs, code, environment, and validation result. Job completion
without a verified artifact is not platform success.

## Is the evaluation gate complete and applicable?

Compare the candidate digest with the exact digest evaluated. Preserve suite,
scenario set, slices, metric definitions, judge and prompt versions, seeds,
threshold policy, safety and compliance results, approval identity, and expiry.

- Missing lineage or evidence is not a pass.
- A changed judge, dataset, or threshold is a changed gate, not a comparable
  score.
- Aggregate improvement can conceal a failing protected or critical slice.
- Manual approval does not replace hard safety or compliance requirements.

Promotion should accept only an immutable digest whose required gates are
current. Quarantine an unverifiable candidate instead of reconstructing
lineage from filenames or mutable tags.

## Did deployment converge on the promoted artifact?

Join promotion record, deployment intent, model and tokenizer digests, runtime
revision, traffic policy, replica observations, and serving telemetry. Separate
control-plane convergence from data-plane health and model quality.

A ready replica may serve the wrong digest. A successful rollout can still
violate latency, cost, or quality objectives. Roll back to a known-compatible
artifact set, not merely a previous model name.

## Are external effects reconciled?

For provider jobs, notifications, tickets, data writes, or agent tool calls,
bind each intended effect to a stable operation identity. After timeout or
worker crash, query external state by that identity before retrying.

Classify each effect as not started, in progress, succeeded, failed terminally,
or unknown. Unknown is not equivalent to failed. Reconciliation closes the gap
between durable intent and observed effect while preventing duplicate
consequences. Escalate when the provider cannot support lookup, idempotency, or
a safe compensating action.

## Controlled change and rollback

Before mutation, define affected tenants and resources, expected convergence,
quality and cost guardrails, migration or compensation, rollback compatibility,
and the evidence that will close the incident. Canary policy, controller, and
contract changes on representative resources; watch queue age, reconcile
errors, convergence lag, denied requests, external calls, and tenant fairness.

Stop and escalate for cross-tenant access, missing audit history, uncertain
lineage, data corruption, bypassed evaluation, unknown external effects,
controller hot loops, destructive finalization, or rollback across an
incompatible schema or artifact contract.

## Authoritative sources

- [Kubernetes controllers](https://kubernetes.io/docs/concepts/architecture/controller/)
- [ML Metadata documentation](https://www.tensorflow.org/tfx/guide/mlmd)
- [Feast feature store documentation](https://docs.feast.dev/)
- [OpenLineage documentation](https://openlineage.io/docs/)
- Repository lesson: [AI Platform Engineering](../32-ai-platform-engineering/README.md)
