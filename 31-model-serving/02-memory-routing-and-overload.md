# Memory, routing, and overload

A serving fleet must place model state, route compatible requests, and reject work before resource exhaustion becomes an outage.

## Why it matters

Model weights and per-request cache compete for finite memory. A process can be alive yet unable to admit another safe request.

## How it works

Capacity includes weights, runtime workspace, activations, and, for autoregressive models, a KV cache that grows with active sequence length. Routers consider model revision, tenant, locality, and replica health. Admission control applies concurrency, token, or memory budgets before enqueueing. Load shedding returns a fast explicit failure. Autoscaling reacts to queue depth and saturation, but cold model loading limits response speed.

Admission must reserve against future work, not only current bytes. A generation request declares or receives a maximum token budget; otherwise one long sequence can evict or starve many short ones. Routing affinity improves cache reuse but can create hot replicas. Health therefore includes readiness for the requested model revision and available admission budget, not merely an open socket.

## See it yourself

Assume a simplified cache cost of 0.5 MiB per token. Eight requests with 1,000 cached tokens consume about 4 GiB; the same eight at 8,000 consume 32 GiB before weights and workspace. On a replica with 24 GiB free after loading weights, the second set is impossible. A token-memory reservation should reject before allocation rather than waiting for an out-of-memory crash.

## Where it shows up

An LLM gateway routes by revision and context capacity, then returns a retryable overload response only when another attempt has a bounded chance. Autoscaling watches queue age and admitted-token pressure, but maintains warm headroom because loading weights may take minutes. Canary routing pins request and telemetry to one digest.

## When it breaks

Retries amplify overload, stale health checks route to stuck replicas, and autoscaling arrives after queues are already unrecoverable. First inspect per-replica reserved versus actual memory, active tokens, queue age, admission outcomes, and route distribution. Skew indicates routing; growing reservations indicate capacity; synchronized retry traffic indicates amplification. Preserve an explicit rejected result rather than hiding it in client timeout.

## Practice

**Build:** simulate two replicas with weight and token-memory budgets and version-aware routing. **Break:** send long contexts to one affinity key and enable immediate retries; observe skew and amplification. **Explain back:** show why readiness, liveness, and admission capacity are separate and identify the first overload dashboard.

## Check yourself

1. Why is process health insufficient?
2. What should a retry budget prevent?
3. Which signals should scale a serving fleet?

## Sources

### REQUIRED

- [Kubernetes resource management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

### RECOMMENDED

- [Kubernetes horizontal pod autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

### DEEP DIVE

- [Orca: a distributed serving system for transformer models](https://www.usenix.org/conference/osdi22/presentation/yu)

## Next

Continue to [Practical lab: build a tiny model service](03-practical-model-service-lab.md).
