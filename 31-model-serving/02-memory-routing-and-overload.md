# Admission, routing, and overload

A serving fleet must route only compatible work, reserve its worst permitted resource demand, and reject excess load before queue growth or memory exhaustion becomes an outage.

## Why it matters

A live process is not necessarily ready for a model revision or able to accept another sequence. Cold loading, variable token counts, retries, and affinity make request rate alone a misleading capacity signal.

## How it works

Routing first removes ineligible replicas by model digest, tokenizer and adapter compatibility, hardware class, context limit, tenant policy, locality, draining state, and semantic readiness. It then balances among candidates using capacity and bounded affinity. Prefix affinity can improve cache reuse, but the router must cap per-key skew and spill to another eligible replica before one hot key monopolizes service.

Admission happens before enqueueing. A request supplies or receives limits for prompt tokens, generated tokens, deadline, and service class. The scheduler estimates prefill work, reserves KV-cache blocks for the permitted lifetime, and charges tenant and global budgets. It admits only when all relevant constraints hold. A short bounded queue can absorb ordinary variance; load shedding rejects work whose deadline or reservation cannot be honored. Rejection carries a stable reason and is retryable only when policy can name a later condition that may succeed.

Autoscaling is a slower control loop, not admission control. Useful signals include arrival token work, oldest queue age, admitted and rejected work, prefill saturation, decode slots, cache pressure, and warm capacity by revision. Scheduled or predictive headroom covers model load time. Scale-down drains, stops new admissions, waits for or cancels bounded generations, and retains failure headroom. Clients enforce one end-to-end deadline, capped backoff with jitter, and a retry budget shared across layers.

## See it yourself

Suppose three warm replicas each safely complete 50 requests/s. Demand rises from 100 to 300 requests/s and another three replicas need 120 seconds to load. Without shedding, backlog grows at \(300-150=150\) requests/s and reaches 18,000 requests before new capacity is ready. Even if six replicas then exactly match demand, drain rate is zero, so the backlog never recovers. This proves reactive scaling alone cannot restore a finite latency objective.

Now reserve memory. A replica has 24 GiB free after weights and workspace, and this simplified model uses 0.5 MiB per cached token. Eight requests capped at 8,000 cached tokens require about 31.25 GiB. Current allocation can look safe while future permitted growth is impossible. Reserving the declared maximum rejects at admission; observing only current bytes delays the decision until allocation failure.

## Where it shows up

An inference gateway emits candidate count, exclusion reason, chosen replica, affinity spill, reservation, queue deadline, admission result, retry hint, and release digest. Per-tenant limits protect shared recovery reserve. Canary routing keeps assignment and telemetry tied to one complete release while health removes a failed candidate.

Use [Lab 17: Control Model-Serving Overload](../labs/17-model-serving-overload/README.md) to measure offered, admitted, and completed work. The [GPU out-of-memory drill](../incidents/11-gpu-oom/README.md) tests token-memory admission, while the [retry-storm drill](../incidents/08-retry-storm/README.md) tests amplification during recovery.

## When it breaks

Stale readiness routes to unloaded models, optimistic token estimates overcommit cache, affinity hotspots one replica, and per-layer retries multiply demand. CPU-based scaling may remain quiet while decode slots and memory are exhausted. First align arrival, admission, rejection, completion, oldest age, reservations, actual blocks, route skew, retry attempts, and replica lifecycle on one timeline. A rising oldest age with completion below admitted work proves instability; skew isolated to one key implicates routing; synchronized attempts beyond original requests implicate retries.

Never hide shedding behind client timeout. Preserve a terminal overload record, do not retry non-idempotent work without a stable key, and do not call recovery complete until queue age declines under continued normal demand.

## Practice

**Build:** complete [Lab 17](../labs/17-model-serving-overload/README.md), then extend its simulator to two model versions, token reservations, tenant shares, bounded affinity, and a 120-second cold-start clock. **Break:** add a hot prefix and immediate retries. **Prove:** assert queue length never exceeds its configured bound, every admitted reservation is released exactly once, no incompatible revision is selected, and total attempts remain within the retry budget.

Carry the evidence into the [Multi-Tenant Model Serving System](../projects/12-model-serving-system/README.md): admission contract, workload distribution, route-reason telemetry, overload runbook, and recovery trace are required project artifacts rather than optional polish.

## Check yourself

1. Why must admission reserve future permitted work?
2. What evidence distinguishes routing skew from fleet-wide saturation?
3. Why can autoscaling not replace rejection during cold start?

## Sources

### REQUIRED

- [Google SRE: handling overload](https://sre.google/sre-book/handling-overload/)

### RECOMMENDED

- [Kubernetes horizontal pod autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

### DEEP DIVE

- [Orca: a distributed serving system for transformer models](https://www.usenix.org/conference/osdi22/presentation/yu)

## Next

Continue to [Inference runtimes and execution](04-inference-runtimes-and-execution.md).
