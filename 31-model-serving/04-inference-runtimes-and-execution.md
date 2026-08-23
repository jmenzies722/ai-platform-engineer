# Inference runtimes and execution

An inference runtime turns a versioned model into executable kernels while managing shapes, memory, streams, synchronization, and request lifecycles.

## Why it matters

Framework eager latency is not production serving latency. Graph compilation, model loading, shape specialization, tokenization, copies, and runtime workspaces can dominate or invalidate a benchmark.

## How it works

The runtime loads immutable weights, validates compatibility, constructs or selects an execution graph, allocates persistent and temporary memory, and warms representative shapes before readiness. Compilers fuse operators and choose kernels by data type and dimensions. Static graphs improve planning; dynamic shapes require profiles, recompilation, padding, or fallback.

Autoregressive serving has a compute-heavy prefill over prompt tokens and repeated decode steps that usually become bandwidth and cache limited. Streams permit overlap only when dependencies and resources allow it. Readiness means the requested revision has completed required warmup and passed a semantic probe, not merely that the process accepts TCP.

## See it yourself

A 12-second compile followed by 20 ms execution makes the first request 12.02 seconds and later requests 20 ms. Reporting only warm latency hides cold-start risk; reporting only the first hides steady state. At 60 requests per minute, amortized compile cost is small only if replicas live long enough.

## Where it shows up

Production runtimes maintain engines by model digest, precision, and shape profile. Telemetry separates gateway, tokenize, queue, host-to-device, prefill, decode-per-token, and serialization time, plus compilation and load events.

## When it breaks

Unsupported shapes trigger slow fallback; graph capture reuses invalid addresses; warmup omits long contexts; driver or runtime incompatibility prevents loading; hidden synchronization destroys overlap. Compare engine selection, shape, revision, stage timing, memory workspace, and correctness against a reference runtime.

## Practice

**Observe:** draw the complete request timeline. **Build:** make a mock runtime with cold compile and shape profiles. **Break:** send an unsupported shape and recycle a replica during load. Completion requires separate cold and warm SLOs and a readiness rule that prevents premature routing.

## Check yourself

1. Why are prefill and decode different capacity dimensions?
2. What does semantic readiness prove beyond liveness?
3. When can graph specialization harm tail latency?

## Sources

### REQUIRED

- [NVIDIA Triton architecture](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/architecture.html)

### RECOMMENDED

- [ONNX Runtime execution providers](https://onnxruntime.ai/docs/execution-providers/)

### DEEP DIVE

- [TensorRT Developer Guide](https://docs.nvidia.com/deeplearning/tensorrt/latest/)

## Next

Continue to [KV cache and continuous batching](05-kv-cache-and-continuous-batching.md).
