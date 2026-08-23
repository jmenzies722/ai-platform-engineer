# Advanced serving topologies

Advanced LLM serving changes where work executes and which state is shared. Speculative decoding, tenant-scoped prefix caches, disaggregated prefill and decode, and mixture-of-experts models can improve throughput only when their communication, correctness, and isolation costs are explicit.

## Why it matters

A topology benchmark can report faster tokens while hiding rejected draft tokens, cache leakage, network saturation, expert hotspots, or worse tail latency. These designs add distributed state and therefore add failure modes that a single-replica throughput number cannot establish.

## How it works

Speculative decoding uses a cheaper draft model to propose \(k\) tokens. The target model verifies them in one pass and accepts only the longest valid prefix under the target distribution, then supplies a correction token when required. Correct sampling preserves the target distribution; accepting draft output by confidence threshold does not. Speedup depends on acceptance length, verification cost, draft cost, and memory bandwidth. Track proposed, accepted, corrected, and target-evaluated tokens separately.

A prefix cache reuses KV blocks for an exact tokenized prefix under a complete cache key: model and tokenizer digest, adapter, positional and attention settings, tenant or sharing policy, and content digest. Entries need ownership, quota, eviction, and invalidation. Cross-tenant reuse is disabled unless data classification and an explicit sharing contract permit it; timing and hit metadata can otherwise expose another tenant's activity.

Disaggregated serving places compute-heavy prompt prefill and bandwidth-heavy iterative decode on different worker pools. A handoff transfers KV state plus immutable request metadata and must be authenticated, checksummed, cancellable, and idempotent. Independent scaling can improve utilization, but network bytes, serialization, transfer latency, placement, and failure reconciliation become part of time to first token. A request is not admitted unless both stages and the transfer path have bounded capacity.

Mixture-of-experts inference activates only selected experts per token. Sparse arithmetic does not imply sparse communication: token dispatch and combine operations cross devices, and a popular expert can limit the whole step. Routers need expert placement and capacity information, while schedulers monitor per-expert token counts, dropped or rerouted tokens, all-to-all bytes, and stragglers. Tenant fairness at the request level is insufficient when one workload disproportionately selects a scarce expert.

## See it yourself

Use this bounded calculation before building a simulator. A draft proposes four tokens, each token is independently accepted with probability \(p=0.75\), draft cost is 0.25 target steps, and one verification pass costs one target step. The expected accepted draft prefix is
\[
E[A]=\sum_{i=1}^{4}P(A\ge i)=\sum_{i=1}^{4}p^i
=0.75+0.5625+0.421875+0.31640625=2.05078125.
\]
Counting the correction or next target token, expected progress is \(3.05078125\) tokens for cost \(1.25\), or about 2.44 tokens per target-step equivalent. If \(p=0.25\), expected progress is about 1.332 tokens and efficiency is about 1.07. Drafting is then barely useful before communication and memory costs.

The independence assumption is intentionally weak. Prove a candidate with a seeded simulation of at most 10,000 rounds, \(k\) between one and eight, and no external service. Compare simulated accepted-prefix mean with the finite sum above within a declared tolerance. Then add fixed draft and verification costs and assert that the policy disables speculation whenever measured efficiency is no better than ordinary decoding. This is a bounded proof of the model, not a production speed claim.

For disaggregation, suppose each request transfers 2 GiB of KV state over an effective 20 GiB/s link. Transfer alone adds at least 100 ms and ten handoffs/s consume the full effective bandwidth. Any plan claiming 50 ms additional first-token latency or 20 handoffs/s contradicts its own assumptions before queueing and protocol overhead.

## Where it shows up

Topology telemetry joins request and tenant IDs to draft acceptance by position, prefix hit ownership, blocks reused, KV transfer bytes and latency, prefill and decode worker identities, expert selection, all-to-all time, and fallback reason. Release manifests pin all participants; mixed draft, target, tokenizer, or adapter revisions invalidate correctness and cache compatibility.

The [inference-latency drill](../incidents/10-inference-latency/README.md) provides the stage-level incident method, and the [GPU out-of-memory drill](../incidents/11-gpu-oom/README.md) tests whether cache and handoff policies remain bounded. Implement one topology as stretch evidence in the [Multi-Tenant Model Serving System](../projects/12-model-serving-system/README.md).

## When it breaks

Low draft acceptance adds work, a stale cache key returns incompatible state, one tenant evicts another's prefixes, KV transfer saturates the fabric, a failed handoff leaves two decode owners, or hot experts create synchronized stragglers. Diagnose by comparing the advanced path with a non-speculative, cache-miss, colocated, or dense baseline under the same workload.

Fallback must preserve semantics and ownership. On draft mismatch, use target-only decode. On cache uncertainty, recompute the prefix. On handoff ambiguity, fence the old owner and reconcile one request ID before decode. On expert overload, apply model-supported capacity behavior rather than silently dropping tokens. Missing topology telemetry is a release failure because it prevents proving which path served the result.

## Practice

**Build:** write the seeded speculative-decoding simulation and one disaggregated-capacity calculator, each capped at 10,000 iterations and 64 MiB. **Break:** lower acceptance, corrupt one cache-key field, saturate transfer bandwidth, and skew 60% of tokens to one expert. **Prove:** target-only output remains the semantic reference, no cross-tenant cache hit occurs, every handoff has one fenced decode owner, and the simulator disables an unprofitable optimization.

After completing [Lab 17](../labs/17-model-serving-overload/README.md), reuse its offered/admitted/completed accounting for each topology. Do not compare only successful requests; include fallback, rejection, transfer failure, and correction work in the denominator.

## Check yourself

1. What must speculative verification preserve?
2. Why must prefix-cache keys include tenancy and complete model identity?
3. Which measurements can disprove a disaggregated or MoE speedup claim?

## Sources

### REQUIRED

- [Fast Inference from Transformers via Speculative Decoding](https://proceedings.mlr.press/v202/leviathan23a.html)

### RECOMMENDED

- [DistServe: disaggregating prefill and decoding](https://www.usenix.org/conference/osdi24/presentation/zhong-yinmin)

### DEEP DIVE

- [Switch Transformers](https://jmlr.org/papers/v23/21-0998.html)

## Next

Continue to [Safe rollout and model observability](08-safe-rollout-and-observability.md).
