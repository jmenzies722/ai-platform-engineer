# Routing, autoscaling, and overload

A serving control loop routes compatible work, admits only bounded demand, and adds capacity early enough to matter.

## Why it matters

Autoscaling cannot recover an unbounded queue when model loading takes minutes. Retries and affinity can turn local saturation into a fleet-wide outage.

## How it works

Routing filters by model digest, hardware, context limit, tenant policy, readiness, and available budget, then balances among candidates. Affinity improves prefix reuse but needs bounded skew. Admission reserves tokens, cache blocks, or weighted service units before enqueueing. Load shedding returns explicit retry semantics before deadlines become impossible.

Scale signals should represent demand work and saturation: oldest queue age, admitted tokens, decode slots, cache pressure, and arrival rate. Predictive or scheduled headroom covers load time. Scale-down drains requests and preserves minimum failure headroom. Clients use capped exponential backoff, jitter, deadlines, and retry budgets.

## See it yourself

Demand rises from 100 to 300 requests/s, each replica handles 50, and load time is 120 seconds. Starting from three replicas, the queue accumulates 150 requests/s while three new replicas load, or 18,000 requests. A reactive target can never preserve a short SLO without warm headroom or rejection.

## Where it shows up

Gateways expose route reason, candidate count, admission result, retry hint, queue age, and revision. Tenant and global limits prevent one customer from consuming recovery reserves.

## When it breaks

Stale readiness routes to unloaded models; immediate retries amplify arrivals; one affinity key hotspots a replica; scale-down kills long generations; a global queue hides model-specific saturation. Plot arrival, admission, rejection, completion, queue age, route skew, and replica lifecycle on one timeline.

## Practice

**Observe:** compute backlog during cold start. **Build:** simulate weighted token admission and version-aware routing. **Break:** enable immediate retries and a hot affinity key. Completion requires bounded queue age, explicit rejections, and recovery without manual queue deletion.

## Check yourself

1. Why does CPU-based scaling often fail LLM serving?
2. What capacity must admission reserve?
3. When should a rejected request be retryable?

## Sources

### REQUIRED

- [Google SRE: handling overload](https://sre.google/sre-book/handling-overload/)

### RECOMMENDED

- [Kubernetes horizontal autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

### DEEP DIVE

- [Envoy overload manager](https://www.envoyproxy.io/docs/envoy/latest/configuration/operations/overload_manager/overload_manager)

## Next

Continue to [Safe rollout and model observability](08-safe-rollout-and-observability.md).
