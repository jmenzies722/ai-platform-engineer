# Evaluation and operations

Agent evaluation must examine both task outcome and the trajectory used to reach it.

## Why it matters

An agent may complete a task through unsafe, wasteful, or irreproducible actions that an outcome-only score misses.

## How it works

Replay versioned scenarios with controlled tools and score completion, policy compliance, action count, latency, cost, reversibility, and recovery. Traces correlate decisions with observations while redacting secrets. Production controls include concurrency caps, kill switches, budget alarms, sampled review, and runbooks for stuck or harmful runs.

Scenario initial state and tool behavior must be reproducible so candidate trajectories are comparable. Outcome scores remain task-specific; policy violations are hard gates. Trajectory metrics reveal unnecessary exploration, repeated errors, and unsafe near misses. Live canaries use lower authority and bounded tasks because offline mocks cannot reproduce every permission or timing condition.

## See it yourself

Give two agents the same answer task. Agent A reads three relevant files in five actions for $0.03. Agent B scans 2,000 files, hits one denial, retries, and finishes in 40 actions for $0.40. Both get outcome score 1, but B fails least-privilege and efficiency thresholds. The comparison proves completion alone is an unsafe objective.

## Where it shows up

Before upgrading a coding agent, replay repository fixtures containing tool denial, ambiguous state, and crash recovery. A low-authority canary then measures real latency and denial rates. Production traces retain event IDs and policy decisions so an incident can be replayed without storing raw secrets.

## When it breaks

Mocks omit real permissions, replay changes external state, trace volume hides signals, and success criteria reward shortcuts. On regression, first compare scenario, model, prompt, tool, and policy versions, then align trajectory diffs at the first changed action. A changed initial state is not a model regression; repeated denials suggest policy or planning; missing events suggest instrumentation.

## Practice

**Build:** create five deterministic scenarios with outcome and trajectory rubrics. **Break:** make a mock over-permissive and remove one trace field; show the false pass and lost diagnosis. **Explain back:** review two successful runs and defend which is deployable, then state the first artifacts needed after a production incident.

## Check yourself

1. Why score trajectories?
2. What should a kill switch stop?
3. Which traces are sensitive?

## Sources

### REQUIRED

- [NIST AI 600-1](https://doi.org/10.6028/NIST.AI.600-1)

### RECOMMENDED

- [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/)

### DEEP DIVE

- [AgentBench](https://arxiv.org/abs/2308.03688)

## Next

Continue to [System Design](../34-system-design/README.md).
