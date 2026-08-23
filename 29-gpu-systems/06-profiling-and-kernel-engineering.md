# Profiling and kernel engineering

Kernel optimization is a controlled experiment that starts with an end-to-end trace, forms one bottleneck hypothesis, and tests it against counters and correctness.

## Why it matters

Microbenchmarks can improve a kernel that contributes little wall time, while fusion, precision changes, and launch tuning can silently alter results or move cost elsewhere.

## How it works

First establish workload, warmup, synchronization, clocks, and output tolerance. A system timeline separates CPU preparation, transfers, kernels, collectives, and idle gaps. Kernel profiling then measures duration, achieved bandwidth, instruction mix, active lanes, occupancy, cache behavior, and warp stalls. The roofline classifies a bound; source correlation locates it.

Optimization changes a resource ledger. Fusion removes launches and intermediate traffic but lengthens live ranges. Tiling creates reuse but consumes shared memory. Vectorization reduces instruction overhead but imposes alignment. Persistent kernels amortize launch and state setup but can monopolize resources. Always report end-to-end impact as well as kernel impact.

## See it yourself

Suppose a kernel falls from 20 ms to 10 ms but occupies 20 ms of a 200 ms request. Amdahl's law predicts request time falls to 190 ms, only 1.053 times faster. If fusion also adds a 15 ms synchronization elsewhere, the request regresses. This arithmetic proves local speedup cannot be interpreted without contribution and side effects.

## Where it shows up

A compiler-generated attention kernel may select different tiles by sequence length and data type. A representative shape distribution, not one favorable matrix, is the unit of evaluation. Performance tests record compiler, driver, clocks, kernel digest, shapes, outputs, and profiler evidence.

## When it breaks

Asynchronous launches produce false timings unless the measured boundary synchronizes. Cold initialization contaminates samples. Profiler overhead distorts tiny kernels. Counter collection may replay a nondeterministic kernel. Thermal or power limits change clocks. Check timeline semantics, repeatability, profiler passes, device state, output error, and the unprofiled baseline before accepting a conclusion.

## Practice

**Observe:** rank kernels by total contribution rather than single-call duration. **Build:** create a benchmark harness with warmup, quantiles, synchronization, correctness oracle, and environment manifest. **Break:** omit synchronization and choose one unrepresentative shape. Completion requires detecting both false conclusions and producing one optimization backed by a before-and-after resource ledger.

## Check yourself

1. Why can a lower kernel duration leave request latency unchanged?
2. Which experiment distinguishes launch overhead from memory latency?
3. What must accompany a claimed mixed-precision speedup?

## Sources

### REQUIRED

- [Nsight Systems User Guide](https://docs.nvidia.com/nsight-systems/UserGuide/)

### RECOMMENDED

- [Nsight Compute Profiling Guide](https://docs.nvidia.com/nsight-compute/ProfilingGuide/)

### DEEP DIVE

- [Triton language and compiler](https://triton-lang.org/main/index.html)

## Next

Continue to [Topology, collectives, and scaling](07-topology-collectives-and-scaling.md).
