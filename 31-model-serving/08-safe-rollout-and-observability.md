# Safe rollout and model observability

A model rollout changes code, weights, prompts, runtime, and behavior; safe delivery identifies the complete variant and evaluates both system and semantic outcomes.

## Why it matters

Healthy latency can accompany harmful predictions, while a quality improvement can exhaust memory or violate availability. Rollback is impossible if telemetry cannot identify what served each result.

## How it works

A release identity binds model digest, tokenizer, runtime, quantization, configuration, prompt or adapter, and policy. Shadowing observes compatibility without side effects; canaries expose a small eligible population; progressive delivery advances only after minimum samples and guardrails. Sticky assignment supports comparison but must not trap traffic on unhealthy replicas.

Telemetry spans request status, stage latency, tokens, cache, saturation, cost, output schema, safety decisions, and version. Content logging is minimized and access controlled. Online proxies never replace delayed ground truth, so rollback rules distinguish immediate hard gates from monitored business outcomes.

## See it yourself

A canary receives 1% of 10,000 daily requests, only 100 samples. A true 1% failure may yield roughly one event and high uncertainty. Absence of failure is weak evidence. Increase exposure or duration based on required statistical power while retaining hard safety checks.

## Where it shows up

A deployment controller verifies artifacts, warms replicas, runs semantic probes, shifts traffic, checks windowed guards, and records a decision event. Rollback restores a known-good complete release and verifies cache and schema compatibility.

## When it breaks

Canary populations differ, low volume produces false confidence, metric windows lag, shadow calls trigger tools, and rollback leaves incompatible caches. Inspect assignment, denominators, version cardinality, side-effect suppression, and artifact manifests. Stop progression on missing telemetry.

## Practice

**Observe:** calculate canary sample needs for a rare failure. **Build:** define a release manifest and guarded state machine. **Break:** remove version labels and introduce delayed quality regression. Completion requires deterministic rollback and proof that every response maps to one release.

## Check yourself

1. Why is a model name insufficient release identity?
2. Which shadow outputs must never cause side effects?
3. When should missing telemetry halt rollout?

## Sources

### REQUIRED

- [Google SRE: reliable product launches](https://sre.google/sre-book/reliable-product-launches/)

### RECOMMENDED

- [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/)

### DEEP DIVE

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

## Next

Continue to [Serving reliability and capacity](09-serving-reliability-and-capacity.md).
