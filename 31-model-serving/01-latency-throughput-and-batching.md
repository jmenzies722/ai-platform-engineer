# Latency, throughput, and batching

Serving performance is a queueing problem around a finite execution resource, not merely a fast model call.

## Why it matters

Average latency can look healthy while a small share of users wait through queues and timeouts.

## How it works

End-to-end latency includes admission, queueing, preprocessing, batching, execution, and serialization. Throughput is completed work per time. Dynamic batching raises device efficiency by waiting briefly to combine requests, trading queue delay for throughput. As utilization approaches capacity, queueing grows sharply; SLOs therefore require headroom and percentile measurements.

Little's Law relates average concurrency \(L\), arrival rate \(\lambda\), and time in system \(W\): \(L=\lambda W\) for a stable system. It is a consistency check, not a promise under overload. Service-time variance and bursts enlarge tails even at the same average rate. Batching policy may cap wait, item count, or total tokens; token-based limits better represent variable-length generation.

## See it yourself

One-at-a-time execution yields at most 125 requests/s at 8 ms each. Full batches of eight yield 400 requests/s, but a request may wait up to the 10 ms batch window before 20 ms execution, making no-contention latency as high as 30 ms. At low traffic, batches rarely fill and the window is pure delay. The example proves throughput gain and latency cost depend on arrival pattern.

## Where it shows up

An embedding API groups similarly sized requests up to a token budget. Metrics expose arrival rate, queue age, batch fill, execution, and end-to-end percentiles. If p95 rises while execution is flat and queue age grows, capacity or admission is implicated; optimizing the model kernel would treat the wrong stage.

## When it breaks

Unbounded queues convert overload into timeouts, mixed request sizes cause head-of-line blocking, and synchronized clients create bursts. First decompose latency by stage and request size while plotting arrival, completion, queue depth, and oldest age on one timeline. Rising age identifies unstable demand; one large-size slice identifies blocking; flat server time with client retries points upstream.

## Practice

**Build:** create a queue/batch simulation and reconcile throughput, concurrency, and latency with Little's Law. **Break:** add bursts and one oversized request; capture tail and head-of-line effects. **Explain back:** defend a 300 ms p95 budget stage by stage and name the first evidence collected when it fails.

## Check yourself

1. Why does queueing rise near saturation?
2. When does batching hurt?
3. Why report percentiles?

## Sources

### REQUIRED

- [NVIDIA Triton dynamic batching](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html)

### RECOMMENDED

- [Google SRE: handling overload](https://sre.google/sre-book/handling-overload/)

### DEEP DIVE

- [vLLM: PagedAttention](https://arxiv.org/abs/2309.06180)

## Next

Continue to [Admission, routing, and overload](02-memory-routing-and-overload.md).
