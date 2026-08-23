# The rollout that passed its first check

> **Synthetic/composite case:** Northstar Retail, its people, systems, numbers, and incident are fictional. The case combines recurring Kubernetes failure patterns for teaching and does not describe a real company.

## Context and constraints

Northstar's `quote-api` turns a cart and delivery destination into a price quote. Twelve replicas run across three zones behind a Kubernetes Service. The service-level objective is 99.95 percent successful quotes with p95 latency below 250 ms. A failed quote prevents checkout, but an old quote can also be wrong, so the gateway cannot serve arbitrary cached responses.

At 14:00 UTC, the team begins rolling out image digest `sha256:91c` with a new fraud-client timeout. The Deployment uses `maxUnavailable: 1` and `maxSurge: 3`. Its readiness probe checks `/ready`; its liveness probe checks `/live`. The release controller advances when new Pods are Ready for 60 seconds and aggregate HTTP 5xx stays below 1 percent.

Constraints narrow the response:

- A seasonal campaign starts in 40 minutes. Traffic is already rising.
- Database schema and public API are unchanged, so the previous image remains compatible.
- Release engineering can pause or undo a Deployment. Cluster-wide changes require the platform on-call.
- Fraud review may be bypassed only for a product-approved low-risk cart class.
- The incident team must preserve rollout, Pod, EndpointSlice, and request evidence.
- Deleting all Pods, disabling probes, or editing the live ReplicaSet is outside the safe operating contract.

This case builds on [Services, configuration, and failure diagnosis](../16-kubernetes/03-service-and-operations.md), [Autoscaling, upgrades, and cluster operations](../16-kubernetes/06-scaling-and-upgrades.md), the [Kubernetes operations lab](../labs/10-kubernetes-operations/README.md), the [bad rollout drill](../incidents/06-bad-rollout/README.md), and the [Kubernetes platform project](../projects/06-kubernetes-platform/README.md).

## Stage 1: a healthy rollout, according to one controller

At 14:07, the release dashboard reports 6 of 12 new replicas Ready. The deployment is progressing. Then the quote success SLI drops.

### Timeline

| Time (UTC) | Event |
|---|---|
| 14:00 | Deployment revision 184 created for digest `sha256:91c` |
| 14:03 | First three new Pods become Ready |
| 14:05 | Automated readiness gate passes |
| 14:07 | New revision reaches six Ready Pods |
| 14:08 | Quote 5xx reaches 4.8 percent; p95 reaches 610 ms |
| 14:09 | Incident declared; rollout still reports `Progressing=True` |

### Initial evidence

```text
deployment/quote-api
  replicas=15 updated=6 ready=12 available=12 unavailable=3
  progressing=True reason=ReplicaSetUpdated

service/quote-api
  selector=app=quote-api

endpointslice/quote-api-k9m2p
  endpoints=12 ready=12
```

```text
14:08:13 gateway ERROR upstream=quote-api status=503 request=q-702
14:08:13 quote INFO version=sha256:91c ready=true fraud_pool_active=24
14:08:14 quote ERROR version=sha256:91c fraud_request deadline_exceeded elapsed_ms=500
14:08:14 quote INFO version=sha256:77a ready=true fraud_pool_active=3
```

| Signal | Old digest `sha256:77a` | New digest `sha256:91c` |
|---|---:|---:|
| Requests/min | 18,400 | 9,100 |
| 5xx | 0.3% | 14.1% |
| p95 latency | 176 ms | 940 ms |
| Pod readiness | 6/6 | 6/6 |
| Restarts | 0 | 0 |

### Competing hypotheses

1. The new application revision exhausts its fraud-client connection pool under production concurrency.
2. The Service selects terminating or unready endpoints during replacement.
3. Rising campaign traffic saturates a shared fraud dependency, independent of version.
4. A zone or node fault happens to contain most new Pods.
5. Readiness is too shallow: it proves that the process can answer `/ready`, not that it can complete a quote.

Before reading on, rank the hypotheses. For each, name one observation that supports it, one that resists it, and one test that discriminates it from the others.

## Decision boundary 1: stop changing the system

The incident commander pauses the rollout at revision 184. This does not repair affected requests, but it prevents the new digest from replacing more known-good capacity while the team gathers evidence.

The team explicitly rejects three tempting actions:

- Scaling all replicas immediately could raise pressure on the same dependency and entangle HPA, scheduler, and rollout effects.
- Disabling readiness would add endpoints without proving they can serve.
- Restarting every new Pod would erase useful process state while recreating the same revision and configuration.

Pausing is highly reversible, has a narrow blast radius, and should make the version mix stable. Its stop condition is evidence that the release is not causal or that holding both revisions is itself unsafe.

## Stage 2: readiness is true, service is not

The team segments traces by digest, zone, and request class. It also compares the Pod template and configuration identity between revisions.

```text
trace request=q-711 version=sha256:91c
  gateway                 11 ms
  quote.compute           23 ms
  fraud.acquire_pool     401 ms
  fraud.request           not started
  total                  517 ms

trace request=q-712 version=sha256:77a
  gateway                  9 ms
  quote.compute           26 ms
  fraud.acquire_pool       4 ms
  fraud.request           38 ms
  total                  112 ms
```

```diff
- FRAUD_POOL_SIZE=8
- FRAUD_TIMEOUT_MS=1200
+ FRAUD_POOL_SIZE=24
+ FRAUD_TIMEOUT_MS=500
```

The new client creates 24 connections per Pod during startup. The fraud service allows 180 connections from this caller. Six old Pods use about 18 connections in total. Six new Pods can claim up to 144. During surge, three additional starting Pods compete for another 72. The fraud service remains healthy overall but rejects and delays this caller after its limit.

| Segment | 5xx | Pool-acquire p95 | Fraud-service p95 |
|---|---:|---:|---:|
| Old digest, all zones | 0.3% | 7 ms | 46 ms |
| New digest, all zones | 14.1% | 438 ms | 49 ms |
| New digest, zone A | 13.8% | 431 ms | 48 ms |
| New digest, zone B | 14.4% | 442 ms | 51 ms |
| New digest, zone C | 14.0% | 440 ms | 47 ms |

EndpointSlices contain only Ready Pods. There is no zone concentration. Fraud execution latency is stable; waiting to acquire a client slot dominates. Hypotheses 2, 3, and 4 now rank below a revision-specific pool and admission interaction. Hypothesis 5 remains true as a detection gap: shallow readiness allowed a harmful revision to receive traffic.

## Options and tradeoffs

| Option | Benefit | Cost or risk | Reversibility |
|---|---|---|---|
| Resume and rely on autoscaling | More quote Pods | More dependency connections; likely amplification | Easy to stop, harmful while active |
| Patch pool size on the new revision | Keeps new code and tests the suspected mechanism | Creates a third state during an incident; config-only forward fix still needs a guarded rollout | Reversible, but adds ambiguity |
| Roll back to revision 183 | Removes the strongly correlated digest and pool settings through the normal controller | Gives up the release; replacement still causes temporary churn | High because schema and API are compatible |
| Route low-risk carts around fraud | Preserves some checkout capacity | Product and risk policy change; does not repair high-risk carts | Reversible but outside engineering authority alone |
| Scale the fraud service | May increase connection capacity | Cold response, unknown downstream limit, and cluster-wide ownership | Reversible slowly; broad blast radius |

## Decision and reversible mitigation

The incident commander chooses a controlled rollback to revision 183 while keeping the rollout paused until release engineering confirms the target revision and digest. Product does not authorize a fraud bypass because healthy old capacity can recover inside the error-budget window.

The rollback uses the Deployment's normal revision mechanism, retains `maxUnavailable: 1`, and is gated after the first two replacement Pods. The team records:

- revision and image digest before and after the command;
- rollout conditions and ReplicaSet ownership;
- ready endpoints by digest;
- request success, latency, and fraud connection count;
- a rollback trigger: halt replacement if available replicas fall below 11 or old-digest error exceeds 1 percent.

This is mitigation, not proof of root cause. It is preferred because it removes the suspected change with known compatibility and bounded disruption. A forward patch may be appropriate later, under canary controls.

## Consequence and recovery review

At 14:16, two restored Pods are serving at baseline. By 14:23, all 12 serving endpoints report `sha256:77a`; new-digest traffic is zero. Quote 5xx falls to 0.4 percent, p95 returns to 181 ms, and caller connection count settles at 37. Campaign traffic proceeds without a bypass.

The rollback briefly reduces available replicas to 11, within the declared bound. No completed quote was calculated incorrectly; 1,842 quote attempts failed and clients retried 1,507 of them. Those retries enlarged peak load by 6 percent but remained bounded.

The review finds two causes and three enabling conditions:

- **Change mechanism:** per-Pod pool capacity tripled while timeout decreased.
- **System interaction:** surge replicas made potential connection demand exceed the caller limit.
- **Detection gap:** readiness checked only process-local state.
- **Analysis gap:** the release gate watched aggregate 5xx, diluted by old replicas, rather than version-specific errors.
- **Contract gap:** the workload contract specified CPU and memory but not dependency connection budgets.

The team does not replace readiness with a live fraud call; that would let a dependency incident remove every endpoint. Instead, readiness proves local initialization, while rollout analysis checks synthetic quote completion and version-specific pool saturation. Deployment policy also caps surge from the dependency budget.

## Reusable engineering lessons

1. `Progressing=True` means a controller is advancing desired state. It is not a user-success verdict.
2. Readiness, liveness, rollout health, and end-to-end service health answer different questions.
3. Preserve version identity in logs, traces, metrics, Pods, and endpoints so mixed-revision evidence can establish correlation.
4. During uncertainty, first stop the mechanism that expands blast radius. A pause is useful even when it is not a fix.
5. Prefer a known-compatible rollback when it removes one causal variable through a rehearsed control path.
6. Capacity budgets cross resource boundaries. Replica surge multiplied by per-replica dependency pools is demand on another system.
7. Verify recovery from controller state, endpoint identity, dependency pressure, and user SLIs. One green dashboard is insufficient.
8. Keep business exceptions, such as fraud bypass, under explicit product and risk authority.

## Evidence exercise

Produce an incident worksheet with these deliverables:

1. A hypothesis table after Stage 1 and a revised table after Stage 2. Do not mark correlation as causation without a discriminating observation.
2. A calculation of maximum potential fraud connections for each revision at steady state and at maximum surge.
3. A mitigation record naming blast radius, reversibility, owner, expected signal, stop condition, and preserved evidence.
4. A recovery checklist that distinguishes desired replicas, available replicas, Ready endpoints, serving digest, request SLI, and dependency state.
5. One release-gate proposal with a numerator, denominator, cohort, window, threshold, and behavior when telemetry is missing.
6. One conformance test suitable for the [multi-tenant Kubernetes platform project](../projects/06-kubernetes-platform/README.md).

Then run the readiness failure in the [Kubernetes operations lab](../labs/10-kubernetes-operations/README.md). Explain which lab evidence is analogous to this case and which production claim the local lab cannot support.

## Teach-back prompts

1. Why was pausing rational before the root cause was known?
2. What did Pod readiness prove here, and what did it fail to prove?
3. Why could adding replicas worsen the incident?
4. Under what new evidence would a forward configuration patch become safer than rollback?
5. How would you explain the difference between mitigation, recovery proof, and root cause to a product leader?
6. Which single change most improves the next rollout: a deeper readiness probe, a version-specific canary gate, or a dependency budget? Defend your priority and name what it leaves unresolved.
