# Safety controls and fleet operations

Operating agents safely requires layered prevention, bounded blast radius, rapid containment, evidence-preserving response, and tested recovery.

## Why it matters

At fleet scale, rare planning, model, tool, and policy failures become routine events. Prompt improvements alone cannot contain authority.

## How it works

Prevention combines typed tools, least privilege, isolation, input provenance, output validation, approval, quotas, and deny-by-default egress. Detection uses policy denials, repeated actions, unusual targets, cost velocity, effect rate, and semantic monitors. Containment includes per-run cancel, capability revocation, tenant pause, tool disable, model rollback, and global admission stop.

Kill switches are independent of the model path, authenticated, audited, and tested under control-plane degradation. Draining prevents new effects while reconciling in-flight work. Recovery rotates credentials, validates external state, replays durable events, and resumes only known-safe runs. SLOs cover completion, stuck runs, policy availability, effect reconciliation, and cancellation latency.

## See it yourself

If 10,000 runs each have independent harmful-effect probability \(10^{-4}\), the probability of at least one is approximately \(1-(1-10^{-4})^{10000}\), about 63%. Scale converts a rare per-run event into likely fleet exposure.

## Where it shows up

Operations dashboards segment authority class and tenant. Runbooks begin with stopping new consequential actions, preserving events, querying committed effects, and notifying owners rather than deleting failed runs.

## When it breaks

Cancellation stops the planner but not remote tools, global switches depend on the failed policy service, alerts leak content, and retries resume quarantined runs. Exercise each control with in-flight effects and verify acknowledgement at every executor.

## Practice

**Observe:** map preventive, detective, and containment controls. **Build:** write SLOs and runbooks for runaway cost, tool compromise, and duplicate effects. **Break:** make policy unavailable and delay cancellation acknowledgement. Completion requires bounded new effects and a reconciled recovery inventory.

## Check yourself

1. Why must a kill switch bypass the agent path?
2. What remains after planner cancellation?
3. Which evidence is preserved before credential rotation?

## Sources

### REQUIRED

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)

### RECOMMENDED

- [Google SRE incident response](https://sre.google/sre-book/managing-incidents/)

### DEEP DIVE

- [OWASP Top 10 for LLM applications](https://genai.owasp.org/llm-top-10/)

## Next

Continue to [Practical lab: simulate a durable agent runtime](09-practical-agent-runtime-lab.md).
