# Serving platform architecture

A serving platform offers a stable deployment contract while owning placement, rollout, routing, capacity controls, and operational evidence.

## Why it matters

Without a platform boundary, every model team rebuilds risky gateways, rollout, autoscaling, and accounting. With an overreaching boundary, the platform becomes responsible for prediction semantics it cannot judge. The serving contract must divide execution guarantees from model behavior while preserving enough evidence to admit, route, contain, and reverse a release.

## How it works

The `Deployment` contract names immutable model, tokenizer, preprocessing, and runtime digests; input/output schema; owner; traffic and data class; latency and availability objective; resource envelope; evaluation attestation; rollout policy; and compatible rollback target. Admission checks authorization, signatures, evidence freshness, policy, interface compatibility, and whether the requested envelope is physically plausible. It records desired state; a controller performs asynchronous loading and rollout.

The data path authenticates and bounds requests before expensive work. Admission uses model-aware estimates such as prompt tokens, output cap, memory class, deadline, and tenant quota. Routing chooses a compatible ready replica and propagates cancellation. Dynamic batching trades queue wait for throughput, so latency classes need separate maximum delay and batch policies. Autoscaling must observe queue age, concurrency, and service time as well as device utilization; utilization alone can look healthy while requests miss deadlines.

Readiness means the correct immutable artifacts loaded and a bounded functional probe passed. It does not establish quality or capacity. Release therefore combines an operational canary, comparing error, queue, latency, memory, and saturation by version, with domain-owned semantic checks. Traffic shifts are explicit and monotonic unless analysis fails. Rollback routes to a retained, compatible bundle including preprocessing and tokenizer, then verifies traffic and outcomes; changing only model weights can preserve the defect.

The platform owns execution reliability, isolation, metering, policy enforcement, and standard telemetry. Model teams own intended behavior, representative workloads, quality criteria, and known limitations. Both own the release decision under a documented incident authority. Per-request evidence includes request class, tenant, deployment and model digests, route, queue time, execution stages, token or item counts, status, and trace ID while excluding sensitive payloads by default.

## See it yourself

Submit `model: latest` with a 100 ms p95 objective but no tokenizer, output bound, hardware, or load distribution. The platform cannot reproduce the bundle or test capacity, so rejection is correct. Pin all artifacts and replay a fixed synthetic trace at 10 requests per second. If 95 of 100 complete within 100 ms under that stated setup, the experiment supports only that bounded workload claim. It does not prove future production SLO compliance or semantic correctness.

## Where it shows up

A paved road generates workload identity, admission budgets, queue classes, canary stages, dashboards, alerts, metering, and rollback from one declaration. A model gateway can host multiple backends while preserving tenant and policy context. Offline batch inference may share artifacts but use a throughput-optimized queue and different deadline contract rather than competing with interactive traffic.

## When it breaks

Abstractions hide critical tuning, unbounded requests trigger out-of-memory, retry layers amplify overload, batching raises time to first token, default quotas starve real workloads, and rollback targets are incompatible. Debug by version and request class, decomposing edge, queue, load, prefill or preprocessing, execution, and streaming time. Correlate the first regression with rollout and configuration, but use a canary rollback or controlled replay to discriminate causality. During overload, reject early with explicit retry guidance; blind retries and unlimited queues turn bounded saturation into an outage.

## Practice

**Observe:** create a responsibility matrix and stage-level latency trace. **Build:** specify the versioned API, admission rules, rollout state machine, capacity test, and compatible rollback bundle. **Break:** submit mutable identity, impossible SLO, oversized context, stale evaluation, and unsupported hardware; then regress batch wait in a canary. Completion requires actionable rejection, bounded overload, version-correlated evidence, rollback proof, and a governed exception where appropriate.

## Check yourself

1. Which serving properties belong to user intent?
2. Who owns semantic correctness?
3. What makes an escape hatch governable?

## Sources

### REQUIRED

- [KServe concepts](https://kserve.github.io/website/latest/modelserving/)
- [NVIDIA Triton dynamic batching](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html)

### RECOMMENDED

- [Kubernetes API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)

### DEEP DIVE

- [Google SRE: reliable product launches](https://sre.google/sre-book/reliable-product-launches/)
- [Google SRE: handling overload](https://sre.google/sre-book/handling-overload/)

## Next

Continue to [Retrieval and index platform contracts](07-retrieval-and-index-platform-contracts.md).
