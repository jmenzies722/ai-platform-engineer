# Facilitator solution: Agent Runaway, Tool Budget Exhaustion, and Kill-Switch Latency

This solution explains the supplied evidence. A learner should reject it if a
discriminating test does not match.

## Diagnosis

Workflow `wf-209` loops on completion verification and recursively spawns child
runs. Each child receives a fresh per-run tool budget, so the nominal limit does
not constrain the root lineage. Missing idempotency keys turn ambiguous
tool-gateway timeouts into duplicate side effects.

The global stop updates the planner and supervisor, but effective containment
is delayed because workers check stop state only at dequeue and the gateway
accepts capability tokens issued under older control generations until their
ten-minute expiry. Runtime status therefore reports `stopped` almost five
minutes before the last newly authorized side effect.

## Evidence-led reasoning

1. A run at recursion depth six reaches its budget, immediately followed by a
   child with `inherited_budget=false`. This explains continuing calls after
   apparent budget exhaustion.
2. The planner's `verify_completion` reason and high child creation rate support
   a recursive control loop rather than a traffic-only increase.
3. `email.send` times out without an idempotency key and is retried under a new
   invocation ID. A timeout does not prove the first call had no effect.
4. The control plane reaches generation 44 at 11:05, while the gateway accepts
   token generation 43 at 11:08. The enforcement point is stale.
5. A worker leased before the stop checks only at dequeue, so already leased
   work can proceed without another authorization check.

## Discriminating investigation

| Test | Expected result | What it proves |
|---|---|---|
| Aggregate counters by root lineage | Descendant calls greatly exceed root limit | Budget scope bypass |
| Disable child creation for a canary lineage | Call growth stops | Recursive fan-out is causal |
| Present generation 43 token after stop | Gateway accepts it until expiry | Stale capability window |
| Pause consumers while leaving planners active | Side effects stop, queue grows | Queue execution boundary |
| Query external API by business operation ID | Some timed-out calls completed | Blind retry caused duplicates |

If calls continue with gateway denies enabled, inspect alternate credentials
and direct tool paths rather than assuming this mechanism is complete.

## Decision analysis

A planner rollback stops new intent but does not contain durable queued work.
Deleting the queue loses reconciliation evidence and may abandon valid
operations. Revoking broad employee or service credentials has excessive blast
radius.

The tool gateway is the last centrally enforceable boundary before external
effects. Denying stale generations and the affected workflow there contains
harm while queue consumers and planner creation are paused in a scoped,
reversible way.

## Mitigation sequence

1. Declare a side-effect cutoff timestamp and incident control generation.
   Preserve workflow digest, lineage graph, budget records, queue offsets,
   invocation IDs, token generations, and external operation IDs.
2. At the gateway, deny side-effecting tools for `wf-209` and reject capability
   generations below 44. Retain separately authorized read-only operations.
3. Confirm deny counters increase and newly accepted side effects reach zero.
   If any bypass remains, apply the global side-effect deny policy.
4. Stop new child runs and pause only `wf-209` consumers. Do not acknowledge or
   delete queued messages.
5. Reconcile external effects by stable business key. Classify every invocation
   as completed, not completed, ambiguous, or duplicate.
6. Roll back workflow `wf-209`. Resume a canary only with root-lineage budget
   enforcement and mandatory idempotency.
7. Remediate duplicates through business-owned reversal or notification
   procedures; do not automatically issue compensating effects when semantics
   are unclear.

The rollback trigger for the scoped gateway deny is unexpected denial of
unrelated workflow IDs. Correct policy scope without restoring stale-generation
access. If read-only diagnostics can mutate state indirectly, disable them too.

## Recovery proof

- Gateway audit shows no accepted side-effecting call for the affected scope
  after the cutoff.
- External-system audit independently confirms no new effect after the bounded
  in-flight window.
- The complete queue and invocation set has one reconciliation state and an
  owner.
- A root run and all descendants share atomic counters for calls, retries,
  tokens, duration, child count, and cost.
- A kill-switch exercise under queue backlog meets `<10 seconds>` at p99 from
  operator action to gateway deny and produces no post-cutoff effect.
- Canary workflow completes without recursive growth, duplicates, or budget
  reset.

## Prevention plan

| Control | Acceptance evidence |
|---|---|
| Root-lineage budget ledger | Concurrent descendants cannot exceed any root limit in race tests |
| External recursion and fan-out limits | Runtime denies depth and child-count violations independent of model output |
| Generation-bound gateway authorization | Old generations are denied on every queued and direct invocation |
| Risk-tiered capability TTL | Write capability lifetime is below the effective-stop objective |
| Idempotent side-effect contract | Gateway rejects writes lacking a stable key; retries return the original result |
| Ambiguous outcome reconciliation | Timeout tests query operation status before retry |
| Kill-switch SLO | Scheduled backlog tests measure p50, p95, p99, and maximum effective latency |

## Debrief guide

- Contrast control-plane acknowledgment latency with effective side-effect stop
  latency.
- Ask why a limit enforced per execution unit was presented as a business-risk
  budget.
- Identify which duplicates came from reasoning loops and which came from
  transport retries.
- Verify the team preserved durable work and reconciliation evidence.
- Require named ownership for the gateway, because a stop button without an
  enforcement contract is only advisory.

## Authoritative sources

- [NIST AI RMF Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [Google SRE, Handling Overload](https://sre.google/sre-book/handling-overload/)
- [AWS Builders' Library, Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)
- [NIST SP 800-207, Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
