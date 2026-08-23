# Complexity and Measurement

Complexity describes how resource use grows with input size; measurement shows constants and machine effects for a real workload.

## Why it matters

A list scan may be perfectly adequate for twenty feature flags and disastrous for ten million authorization records. Choosing a representation requires both growth reasoning and measurements at relevant sizes. Big-O prevents a benchmark from hiding an eventual scaling problem, while measurement prevents asymptotics from hiding constants, allocation, and machine effects.

## How it works

Asymptotic notation bounds growth while ignoring constant factors. Worst-case, average-case, and amortized analyses answer different questions. Space matters alongside time. A benchmark must keep semantics and workload equivalent before comparing implementations.

An input-size function models a chosen resource such as comparisons, allocations, bytes, or elapsed time. Big-O supplies an upper growth bound after some point; theta describes a tight asymptotic bound, and omega a lower bound. Worst-case analysis protects guarantees, average-case requires a stated input distribution, and amortized analysis spreads occasional expensive operations across a sequence without assuming randomness. Space analysis includes auxiliary structures and sometimes output. Experimental timing observes an implementation on a machine, so setup, warm-up, timer resolution, background load, and data distribution must be controlled. Equivalent workloads must return the same result and perform the same logical task. Plotting or tabulating several powers of two often reveals growth more reliably than comparing one pair.

## See it yourself

Predict that absent membership examines every list element and that larger lists generally take longer. Expect noisy individual times, especially at small sizes, rather than exact doubling.

```bash
python3 - <<'PY2'
import time
for n in (10_000, 20_000, 40_000):
    xs=list(range(n)); start=time.perf_counter(); target=-1 in xs
    print(n, round(time.perf_counter()-start, 6), target)
PY2
```

Expected observation: Absent membership scans the whole list, so doubling input tends to increase work roughly linearly, though individual timings are noisy.

Limits of the complexity and measurement observation: The experiment does not establish a universal constant, isolate CPU effects, or prove asymptotic complexity from three samples. Python interpreter and machine conditions are part of the observation.

## Where it shows up

An API performing linear duplicate detection per inserted item can become quadratic over a batch. Production latency may look acceptable until a customer crosses a size threshold, then exceed a request deadline sharply. Counting operations against batch size, reproducing with realistic distributions, and switching to a set can fix the growth rate, but set construction, memory, and hash behavior remain part of the decision.

Capacity planning should use the largest credible batch, not only today’s median request, because growth costs appear at the edges first.

## When it breaks

Latency growing with record count suggests complexity or I/O volume; a sudden cliff suggests capacity, caching, or algorithm thresholds; high variance may be scheduler or data-dependent paths. First graph input size against the most direct operation count you can instrument, then measure elapsed time under a controlled fixture. Profiling before rewriting confirms whether the suspected operation dominates end-to-end cost and whether allocation or I/O changes the scaling story.

## Practice

**Build:** compare list and set membership across increasing sizes while separating construction and lookup. **Break:** feed duplicate-heavy and adversarially ordered data to expose distribution assumptions without attempting a denial of service. **Explain back:** distinguish worst-case, expected, and amortized claims for the measured operations. Success includes equivalent outputs, repeated samples, stated environment, and a crossover point rather than “sets are faster.”

## Check yourself

1. What does O(n) omit?
2. How does amortized cost differ from an average over random inputs?

## Sources

### REQUIRED

- [Introduction to Algorithms](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)

### RECOMMENDED

- [Python timeit](https://docs.python.org/3/library/timeit.html)

### DEEP DIVE

- [Algorithm Design Manual](https://www.algorist.com/)

## Next

Continue to [Sequences, Hash Tables, and Trees](./02-sequences-hash-tables-and-trees.md).
