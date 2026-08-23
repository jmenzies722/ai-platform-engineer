# Model packaging and deployment

Deployment promotes an evaluated artifact and its runtime contract into bounded traffic; it never rebuilds the candidate in production.

## Why it matters

[Pipeline testing and reproducibility](05-pipeline-testing-and-reproducibility.md) creates trustworthy artifacts. Packaging or serving skew can invalidate that evidence after training succeeds.

## How it works

A deployable bundle identifies model bytes, preprocessing, tokenizer or feature schema, runtime and dependencies, hardware assumptions, signature, evaluation, owner, and compatibility. Prefer constrained, inspectable formats when possible; many native serialization formats can execute code and require trusted provenance.

Batch inference optimizes throughput and completion windows. Online inference adds request validation, admission, batching, timeout, health, autoscaling, and fallback. A shadow receives copied traffic without affecting users. A canary serves a small bounded population. Blue-green switches between complete environments. Rollback restores the prior immutable bundle and compatible state.

Promotion is an audited registry transition referencing one digest. Deployment verifies signature and digest, checks contracts, warms the runtime, runs smoke fixtures, then ramps under automated and human gates.

## See it yourself

Evaluate artifact digest A, then rebuild “the same” source and deploy digest B. Even if metrics appear equal, evidence for A does not establish B's dependency bytes. Deploy A directly.

This proof is about identity, not quality: immutable promotion preserves what was tested but cannot make a poor test adequate.

## Where it shows up

A classifier canary receives one percent of eligible traffic, stratified to include critical slices. Gates compare errors, latency, feature validity, abstention, and delayed quality. One command references the prior digest for rollback.

## When it breaks

Unsafe deserialization executes code, preprocessing versions diverge, cold starts violate latency, canary routing excludes important slices, and rollback fails after an incompatible schema change.

Before rollout, run a golden input through offline and serving stacks and compare transformed tensors and outputs. During incident response, verify deployed digest and route first, then rollback without rebuilding.

## Practice

**Observe:** inventory a model bundle's runtime dependencies. **Build:** write a release manifest and canary gates. **Break:** change preprocessing in serving only and catch it with a golden fixture.

## Check yourself

1. Why must deployment use the evaluated digest?
2. What risk does model deserialization introduce?
3. How can canary sampling hide harm?
4. Which evidence proves rollback readiness?

## Sources

### REQUIRED

- [NIST Secure Software Development Framework](https://csrc.nist.gov/Projects/ssdf)

### RECOMMENDED

- [MLflow model deployment](https://mlflow.org/docs/latest/ml/deployment/)

### DEEP DIVE

- [SLSA specification](https://slsa.dev/spec/)

## Next

Continue to [Model monitoring and response](07-model-monitoring-and-response.md).
