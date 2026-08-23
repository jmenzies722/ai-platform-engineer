# Memory systems and data movement

GPU performance is often the problem of moving the right bytes once, through the narrowest necessary scope, while preserving enough parallel work.

## Why it matters

High arithmetic throughput cannot compensate for redundant global reads, scattered transactions, page migration, or host synchronization. Memory also determines whether a model fits at all.

## How it works

Registers are private to a thread; shared memory is explicitly managed within a block; caches are hardware managed; global memory is device-wide; host memory lies beyond the interconnect. A load is efficient when active lanes request addresses served by few aligned transactions. Tiling stages reusable values in shared memory, but capacity and bank conflicts constrain the tile. Pinned host buffers permit asynchronous DMA; pageable buffers may require staging. Unified memory can simplify ownership while page faults make placement costs implicit.

For a kernel moving \(B\) bytes and performing \(F\) operations, arithmetic intensity is \(I=F/B\). The roofline bound is \(\min(P, I\beta)\), where \(P\) is peak compute and \(\beta\) sustained bandwidth. Count bytes at the level being diagnosed: cache hits reduce DRAM bytes but not load instructions.

## See it yourself

An FP32 operation `y = a*x + y` performs two floating-point operations and, without reuse, reads eight bytes and writes four. Its intensity is about \(2/12=0.167\) operations per byte. At 1.5 TB/s, the bandwidth roof is about 250 GFLOP/s, far below modern compute peaks. The calculation proves bandwidth is the idealized ceiling for this traffic model, not that an implementation reaches it.

## Where it shows up

Transformer inference reuses weights across a batch but streams KV-cache blocks per sequence. Training input pipelines cross storage, host, interconnect, and device boundaries. A useful timeline names bytes, owner, source, destination, lifetime, and overlap at each boundary.

## When it breaks

Misalignment and strides waste transactions; bank conflicts serialize shared-memory accesses; spills add hidden local-memory traffic; excessive prefetch evicts useful data; implicit page migration creates long tails. Validate with requested versus transferred sectors, cache hit rates, DRAM throughput, page-fault events, copy-engine overlap, and a memory ledger. A high bandwidth percentage with low useful bytes points to layout, not insufficient hardware.

## Practice

**Observe:** calculate useful and physical bytes for contiguous and strided access. **Build:** tile a matrix transpose or simulate its address transactions. **Break:** introduce a shared-memory bank conflict and pageable host transfer. Completion requires explaining each slowdown from counters and byte counts rather than elapsed time alone.

## Check yourself

1. Why must a roofline state which memory level supplies \(B\)?
2. When can a cache hit rate rise while runtime worsens?
3. What evidence distinguishes allocation pressure from transfer pressure?

## Sources

### REQUIRED

- [CUDA Best Practices Guide: memory optimizations](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/)

### RECOMMENDED

- [Nsight Compute memory workload analysis](https://docs.nvidia.com/nsight-compute/ProfilingGuide/)

### DEEP DIVE

- [Roofline model](https://doi.org/10.1145/1498765.1498785)

## Next

Continue to [Profiling and kernel engineering](06-profiling-and-kernel-engineering.md).
