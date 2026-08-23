# Caches, Locality, and Measurement

Fast programs often reuse nearby data and avoid waiting on slow resources; measurement determines whether that intuition applies.

## Why it matters

A cache can cut median latency and simultaneously make stale data or tail latency worse. Engineers deciding to cache must name the reuse pattern, consistency requirement, eviction bound, and metric they expect to improve. A quick benchmark with unequal workloads cannot justify that operational trade.

## How it works

Caches exploit temporal locality, reuse soon, and spatial locality, nearby addresses soon. Hardware caches operate in lines; operating systems cache file pages; applications add their own caches. Benchmarks need a stable workload, repeated samples, and a stated metric.

Hardware caches move fixed-size lines and exploit reuse over time and neighboring addresses; a miss consults lower cache levels and eventually memory. Page caches retain file-backed pages, while application caches retain values chosen by program policy. Each layer has a key, capacity, replacement policy, and coherence or invalidation rule. Temporal locality makes recently used data likely to return; spatial locality makes nearby data likely to be consumed. Warm-up changes the available state, so cold and warm measurements answer different questions. Sound comparison holds result semantics and amount of useful work constant, chooses a relevant distribution rather than only an average, repeats enough to expose variation, and records environment. Counters can support a cache explanation, but elapsed time alone cannot identify which layer helped.

## See it yourself

Predict that the dense and sparse slices report different totals and touch different numbers of elements. Because those workloads are unequal, predict that even a consistent timing difference will be insufficient evidence for a locality conclusion.

```bash
python3 - <<'PY2'
import time
values=list(range(1_000_000))
for label, stride in [('dense',1),('sparse',97)]:
    start=time.perf_counter(); total=sum(values[::stride]); elapsed=time.perf_counter()-start
    print(label, round(elapsed,6), total)
PY2
```

Expected observation: The workloads do different amounts of work, so raw times do not prove a cache claim. That limitation is part of sound measurement.

Limits of the caches, locality, and measurement observation: This command does not isolate CPU cache effects, control allocation cost, or compare equivalent algorithms. The interpreter, slice construction, scheduler, and machine state all contribute to the measured interval.

## Where it shows up

A service-side user cache illustrates the full trade. Keeping profiles in memory can remove database reads for repeated requests, but eviction during a traffic spike creates a miss storm and stale entries can outlive permission changes. Hit rate, load latency, eviction count, entry age, and downstream load must be read together. A bounded cache with explicit invalidation and request coalescing is an architectural component, not a dictionary added for speed.

## When it breaks

A sudden latency jump after deployment may come from colder code and data, changed access order, or cache capacity pressure; rising memory with no eviction suggests an unbounded application cache; correct but old responses indicate invalidation failure. First split hit and miss outcomes and inspect cache size, age, eviction, and downstream request rate. For hardware claims, begin with a stable benchmark and profiler before selecting narrowly scoped counters.

## Practice

**Build:** write an LRU-like cache with a small fixed capacity and observable hit, miss, and eviction counts. **Break:** omit invalidation for a changed record and exceed capacity with a burst, recording stale and churn behavior. **Explain back:** distinguish hardware, page, and application caches without treating them as one store. Success includes correctness tests, a capacity invariant, and a benchmark where both alternatives return identical results.

## Check yourself

1. What are temporal and spatial locality?
2. Why is a faster one-off run weak evidence?

## Sources

### REQUIRED

- [Linux perf documentation](https://perf.wiki.kernel.org/index.php/Main_Page)

### RECOMMENDED

- [Systems Performance](https://www.brendangregg.com/systems-performance-2nd-edition-book.html)

### DEEP DIVE

- [A Methodology for Creating and Using Performance Benchmarks](https://dl.acm.org/doi/10.1145/285930.285972)

## Next

Continue to [Linux](../04-linux/README.md).
