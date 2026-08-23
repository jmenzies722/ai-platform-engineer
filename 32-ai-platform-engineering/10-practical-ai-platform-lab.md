# Practical lab: verify an AI platform control plane

Run a deterministic control-plane slice that preserves tenant-scoped corpus lineage, blocks partial index promotion, binds evaluation to a model digest, deduplicates commands, and records rollback.

## Why it matters

Platform diagrams do not prove transition semantics. A small executable model makes admission timing, trusted identity, idempotency, lineage, publication boundaries, and rollback assertions reviewable. This lab deliberately excludes network, storage, scheduler, and model-runtime behavior; passing it proves only the implemented control-plane invariants.

## How it works

The standard-library simulator in [`lab/control_plane.py`](lab/control_plane.py) stores append-only dictionaries and derives decisions from prior events. The authenticated principal is passed as trusted context and becomes the tenant namespace; no request field can substitute another tenant. Each command is keyed by principal plus idempotency key, so a retry returns the original result instead of repeating an effect.

`publish_corpus` hashes a synthetic manifest. `publish_index` requires that exact corpus in the principal's namespace and matching expected and indexed document counts before emitting `index.promoted`. `register_model` binds model digest to corpus version. Evaluation binds suite result to the exact model digest, and deployment admits only that digest. A later deployment records the previous approved digest, enabling an auditable rollback event.

Run from this module:

```bash
cd lab
python3 -m unittest -v
```

The six tests must report `OK`. One test serializes events with sorted keys and compact separators, then checks a fixed SHA-256 digest. This gives byte-stable evidence for the fixture and Python string semantics used here. It does not prove a production event store is durable, concurrent, or tamper-resistant.

Inspect the evidence directly:

```bash
python3 - <<'PY'
from control_plane import ControlPlane
p = ControlPlane()
c = p.publish_corpus("tenant-a", "c1", "support", "doc-1\ndoc-2")["corpus_version"]
m = p.register_model("tenant-a", "m1", "model-v1", c)["model_digest"]
p.evaluate("tenant-a", "e1", m, True)
p.deploy("tenant-a", "d1", m, "staging")
print(p.normalized_events())
PY
```

The output has monotonically increasing sequences and immutable digest identities. Re-run it and compare bytes. Then change `tenant-a` to `tenant-b` only for model registration; the command must fail because tenant B cannot resolve tenant A's corpus.

## See it yourself

Read each test as a bounded claim. `test_tenant_namespace_is_enforced_before_indexing` proves the adapter method searches the principal's namespace before index publication. `test_partial_index_cannot_promote` proves a count mismatch emits no promotion event. `test_idempotent_command_has_one_effect` proves one in-memory process deduplicates a repeated key, even when the second payload differs. In production, that payload mismatch should also produce a conflict and the deduplication record must share a transaction with durable effects.

Break one invariant at a time. Remove the principal predicate in `_latest`; the cross-tenant test must fail. Change `indexed_docs != expected_docs` to `False`; the partial-index test must fail. Allow deployment to find any passing evaluation rather than the exact digest; the stale-evaluation test must fail. Restore the code after each mutation and preserve the failing and passing transcripts.

## Where it shows up

The simulator mirrors production API admission, policy, registry, index controller, promotion controller, audit ledger, and deployment reconciler boundaries. A real implementation would use authenticated workload identity, transactional storage, signed attestations, optimistic concurrency, asynchronous status, policy versions, cache invalidation, metrics, and retries. The event fields form a starting audit contract, not a complete schema.

## When it breaks

The implementation is intentionally single-process. Two replicas could race on the same idempotency key; process loss destroys events; dictionaries do not enforce schema; and SHA-256 identity does not validate artifact safety. Before production, require uniqueness and event append in one database transaction, compare request hashes on duplicate keys, authorize every transition, verify signatures, and test replay after crash.

Debug a failed test from the first unauthorized or missing event. Preserve principal, key, kind, digest, and sequence. Do not weaken a denial merely to make the happy path pass. If the deterministic hash changes after an intentional schema edit, review the normalized diff and update the expected digest only after every invariant test passes.

## Practice

**Build:** add policy version and usage events whose tenant derives from principal. Make usage replay idempotent. **Break:** inject a duplicate key with changed payload, policy outage, stale corpus ACL, partial event write, and rollback without a prior target. **Prove:** retain commands, failing transcript, fix, passing transcript, normalized event log, and hash. Then complete standalone [Lab 18: Verify AI Platform Tenant Isolation](../labs/18-ai-platform-tenancy/README.md) for SQLite-backed storage, cache-key, quota, and accounting evidence.

## Check yourself

1. Which passing claims are limited to one process?
2. Why must evaluation and deployment compare exact digests?
3. What transaction makes idempotency durable?

## Sources

### REQUIRED

- [Kubernetes operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
- [Open Policy Agent documentation](https://www.openpolicyagent.org/docs/latest/)

### RECOMMENDED

- [in-toto attestation framework](https://in-toto.io/)
- [SQLite transactions](https://www.sqlite.org/lang_transaction.html)

### DEEP DIVE

- [Kubernetes API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)
- [SLSA provenance](https://slsa.dev/spec/v1.0/provenance)

## Next

Continue to [Agentic Infrastructure](../33-agentic-infrastructure/README.md).
