# Evaluation and trajectory observability

Agent evaluation scores the outcome, the path, and the exercised authority under reproducible scenario conditions.

## Why it matters

An agent can complete a task while wasting cost, violating policy, relying on leaked answers, or taking irreversible shortcuts.

## How it works

A scenario versions initial state, permitted tools, tool behavior, hidden checks, budgets, and rubric. Outcome metrics remain task specific. Trajectory metrics include action count, denials, retries, cost, latency, unnecessary access, reversibility, recovery, and policy compliance. Hard violations are gates, not values averaged into a score.

Production traces connect run, state, model, prompt, tool, policy, principal, effect, latency, and token usage. Sensitive content is minimized, redacted, access controlled, and retained by policy. Sampling preserves all consequential and anomalous runs while sampling routine spans.

## See it yourself

Two agents both fix a fixture. One reads four files and edits one; another scans secrets, receives denials, and edits the same file after 40 calls. Outcome-only scoring ties them. Trajectory scoring identifies authority and efficiency failure without claiming the shorter path is always semantically better.

## Where it shows up

Regression suites replay tool errors, hostile observations, approval denial, crashes, and ambiguous effects. Low-authority canaries then test real timing and permissions.

## When it breaks

Mocks are more permissive than production, judges drift, test cases leak, trace gaps hide actions, and replay causes real effects. Pin every component, use effect-free fixtures, compare at the first changed event, and treat missing telemetry as evaluation failure.

## Practice

**Observe:** diff two successful trajectories. **Build:** define ten scenarios and outcome plus trajectory rubrics. **Break:** remove a trace field and make a mock over-permissive. Completion requires detecting the false pass and localizing one regression.

## Check yourself

1. Which metrics are hard gates?
2. Why can fewer actions be a misleading objective?
3. What telemetry must never be sampled away?

## Sources

### REQUIRED

- [NIST AI 600-1](https://doi.org/10.6028/NIST.AI.600-1)

### RECOMMENDED

- [OpenTelemetry trace specification](https://opentelemetry.io/docs/specs/otel/trace/)

### DEEP DIVE

- [AgentBench](https://arxiv.org/abs/2308.03688)

## Next

Continue to [Safety controls and fleet operations](08-safety-controls-and-fleet-operations.md).
