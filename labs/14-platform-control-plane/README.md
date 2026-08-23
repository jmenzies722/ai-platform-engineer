# Lab: Design and Test a Reconciliation Control Plane

Specify a small platform API and implement a local reconciliation simulator that turns desired state into idempotent actions while preserving tenancy and auditability.

## Prerequisites

- Python 3.10 or newer, SQLite support, and a Mermaid renderer
- Familiarity with APIs, queues, state machines, and eventual consistency
- No cloud account or external service

## Safety

The simulator may write only beneath `.work` and may not invoke shell commands or network APIs. Use fictional tenant IDs. Cap the queue at 100 requests and each reconciliation run at 20 actions.

## Setup and baseline

```bash
mkdir -p .work
python3 - <<'PY'
import sqlite3
db=sqlite3.connect(".work/control.db")
db.executescript("""
create table desired(tenant text, resource text, generation int, spec text,
 primary key(tenant,resource));
create table observed(tenant text, resource text, generation int, status text,
 primary key(tenant,resource));
create table audit(seq integer primary key, tenant text, resource text, action text);
""")
db.commit()
PY
```

Define the invariant: a tenant can read or mutate only resources carrying the same immutable tenant identity.

## Tasks

1. Create `.work/design.md` describing API, authentication, authorization, validation, idempotency key, desired/observed state, generation, status conditions, retry policy, quotas, audit record, and deletion finalizer.
2. Add a valid Mermaid sequence diagram for request admission, persistence, queueing, reconciliation, data-plane adapter, and status update.
3. Implement `.work/reconcile.py`. It reads SQLite desired and observed rows, emits at most one create/update/delete action per resource, records an audit row, and converges observed generation. It accepts `--max-actions 20`.
4. Run it twice against one desired row. The first run should act; the second should emit no action.
5. Update desired generation twice before reconciliation. Prove the reconciler converges to the newest generation rather than replaying stale work.
6. Add status conditions with type, status, reason, observed generation, and transition time. Explain why a successful API write does not imply a ready resource.
7. Document backpressure, poison work, adapter timeouts, regional failure, and control-plane dependency failure.

## Evidence to keep

Keep API contract, diagrams, schema, simulator source, deterministic input, action logs, audit rows, idempotency proof, convergence proof, tenant-isolation tests, and explicit consistency guarantees.

## Failure injection

Insert an observed row whose adapter status is `transient-error`. Make the simulator retry with a capped attempt count and deterministic backoff schedule, then move exhausted work to a local dead-letter table. Inject a desired row for tenant B while authenticating as tenant A; admission must reject it before persistence.

## Cleanup

```bash
rm -rf .work
```

## Rubric

- 2 points: separates API admission, desired state, reconciliation, and data plane
- 3 points: proves idempotency, newest-generation convergence, and bounded retries
- 2 points: enforces tenant identity at admission and storage queries
- 2 points: specifies status, audit, quotas, deletion, and failure handling
- 1 point: simulator is bounded, deterministic, and removed

## Sources

- [Kubernetes API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)
- [Kubernetes controllers](https://kubernetes.io/docs/concepts/architecture/controller/)
- [Google API design guide](https://cloud.google.com/apis/design)
