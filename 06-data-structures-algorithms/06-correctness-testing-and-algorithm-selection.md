# Correctness, Testing, and Algorithm Selection

An algorithm is useful when its contract is explicit, its correctness argument matches its implementation, and its resource costs fit the real input distribution.

## Why it matters

A faster deduplication routine that changes which duplicate survives is not an optimization; it is a behavior change. Benchmarks can reward wrong work, and example tests can miss an entire boundary class. Selection must begin with semantics and constraints, then combine proof, differential tests, and measurement.

## How it works

A correctness argument states preconditions, postconditions, and invariants. A loop invariant holds before and after every iteration; initialization, maintenance, and termination connect it to the result. Representation invariants constrain valid data-structure states. Termination requires a well-founded progress measure. Proof applies to a model, so implementation details such as integer overflow, mutation, recursion depth, and concurrent access remain obligations.

Testing supplies complementary evidence. Example tests document named cases. Boundary tests target empty, singleton, duplicate, extreme, and invalid inputs. Property-oriented tests assert relationships such as sorted output being ordered and a permutation of input. Differential testing compares an optimized implementation with a simple trusted oracle across many small generated cases. Metamorphic tests derive new inputs whose outputs have known relationships. Complexity claims can be checked with operation counters and measured at several sizes, but timing alone does not prove a bound. Algorithm selection also accounts for memory, stability, determinism, online versus batch input, approximation tolerance, and operational complexity.

## See it yourself

**Tiny Proof:** predict that sorting preserves both length and element counts for every case, including duplicates and empty input.

```bash
python3 - <<'PY2'
from collections import Counter
cases = [[], [1], [3, 1, 3, 2]]
for values in cases:
    result = sorted(values)
    assert all(a <= b for a, b in zip(result, result[1:]))
    assert Counter(result) == Counter(values)
    print(values, result)
PY2
```

Expected observation: every result is ordered and is a permutation of its input; those two properties describe sorting more strongly than one expected list.

Limits of this proof: three cases do not verify an implementation universally, `sorted` is itself trusted here, and the properties do not check stability for distinct records with equal keys.

## Where it shows up

Replacing a list scan with a hash index in authorization code can improve expected lookup growth while increasing memory and introducing hash/equality assumptions. A safe change retains the old implementation as a test oracle, compares decisions over generated and production-shaped sanitized fixtures, verifies duplicate policy, profiles end-to-end cost, and rolls out with mismatch metrics. The old path is removed only after the comparison window and fallback plan expire.

## When it breaks

Rare wrong answers suggest an unstated edge condition or invariant violation; speedups with changed counts suggest unequal work; flaky output suggests nondeterministic iteration or shared mutation; stack or memory failures suggest resource analysis omitted implementation constraints. First minimize the failing input and compare every intermediate invariant with the oracle. Do not weaken assertions to accept the optimized output.

## Practice

**Build:** complete [Design, Prove, and Measure a Scheduler](./lab-design-prove-measure-scheduler.md). **Break:** inject stale heap entries, duplicate IDs, equal priorities, and empty removal. **Explain back:** give contract, invariant, termination argument, complexity by operation, and evidence limitations. Success means differential tests cover thousands of bounded generated operations with a fixed seed and benchmarks compare semantically identical results at several sizes.

## Check yourself

1. What three obligations connect a loop invariant to correctness?
2. Why can differential testing find bugs without proving absence of bugs?

## Sources

### REQUIRED

- [ACM curriculum: algorithmic foundations](https://csed.acm.org/knowledge-areas-algorithmic-foundations/)

### RECOMMENDED

- [Hypothesis property-based testing](https://hypothesis.readthedocs.io/en/latest/)

### DEEP DIVE

- [The Science of Programming](https://www.springer.com/gp/book/9780387964805)

## Next

Continue to [Networking](../07-networking/README.md).
