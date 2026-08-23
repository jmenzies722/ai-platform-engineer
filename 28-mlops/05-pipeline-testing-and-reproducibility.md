# Pipeline testing and reproducibility

An ML pipeline is reliable when each transformation has explicit inputs, outputs, invariants, and replay behavior.

## Why it matters

[Data versioning and contracts](04-data-versioning-and-contracts.md) identifies inputs. Orchestration alone does not prevent stale caches, partial outputs, nondeterminism, or a valid-looking bad model.

## How it works

Model a pipeline as a DAG of idempotent stages. A stage reads immutable inputs into an isolated work area, validates them, writes a new immutable output, then atomically publishes metadata. Its cache key covers upstream digests, code, parameters, environment, and relevant randomness.

Unit tests check pure transforms; contract tests check schemas and semantics; integration tests run a tiny end-to-end fixture; metamorphic tests assert behavior under valid transformations; replay tests compare known artifacts within documented numerical tolerances. Data and model validation gates prevent publication, not merely warn afterward.

Random seeds control pseudorandom streams but exact replay may also require library, compiler, hardware, kernel, thread, and reduction-order identity. Define the required reproducibility level: exact bytes, numerically equivalent metrics, or statistically equivalent outcomes.

## See it yourself

A feature stage key includes data and parameters but omits code. Change `x` to `log1p(x)`; the orchestrator reuses stale output. Add the source digest and descendants invalidate.

This counterexample proves cache correctness depends on complete dependency identity, not successful prior execution.

## Where it shows up

A scheduled trainer first runs a 100-row fixture, validates production snapshot contracts, builds features, trains, evaluates slices, and registers only after gates pass. Retries reuse committed stages and discard partial work.

## When it breaks

Concurrent runs publish to one mutable path, caches omit environment, tests accept empty data, and retries duplicate side effects. Nondeterministic reductions cause false byte-diff alarms.

Inspect the full cache-key explanation and artifact publication log. On replay drift, compare data, code, environment, random state, and hardware before widening tolerances.

## Practice

**Observe:** enumerate inputs to a transform cache key. **Build:** implement a three-stage file DAG with atomic publication and a tiny fixture. **Break:** omit code identity and demonstrate stale reuse.

## Check yourself

1. What makes a stage safe to retry?
2. Why is a seed insufficient for exact replay?
3. Which tests catch semantic schema changes?
4. When is statistical equivalence the right contract?

## Sources

### REQUIRED

- [TFX pipeline components](https://www.tensorflow.org/tfx/guide)

### RECOMMENDED

- [scikit-learn model persistence](https://scikit-learn.org/stable/model_persistence.html)

### DEEP DIVE

- [ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/)

## Next

Continue to [Model packaging and deployment](06-model-packaging-and-deployment.md).
