# 31 — Model Serving

Model serving converts requests into predictions under explicit latency, throughput, availability, quality, and cost constraints.

## What you will learn

- Explain inference runtime execution, KV-cache allocation, and continuous batching.
- Choose quantization, routing, autoscaling, and overload controls from evidence.
- Roll out model revisions with quality, performance, and operational observability.

## Lessons

1. [Latency, throughput, and batching](01-latency-throughput-and-batching.md)
2. [Memory, routing, and overload](02-memory-routing-and-overload.md)
3. [Inference runtimes and execution](04-inference-runtimes-and-execution.md)
4. [KV cache and continuous batching](05-kv-cache-and-continuous-batching.md)
5. [Quantization and quality control](06-quantization-and-quality-control.md)
6. [Routing, autoscaling, and overload](07-routing-autoscaling-and-overload.md)
7. [Safe rollout and model observability](08-safe-rollout-and-observability.md)
8. [Serving reliability and capacity](09-serving-reliability-and-capacity.md)
9. [Practical lab: build a tiny model service](03-practical-model-service-lab.md)

## Practice

Complete the local service lab, measure queueing, trigger bounded overload, add rollout telemetry, and reconcile every request with the resulting latency distribution.

## Ready to continue

You can account for runtime and cache memory, define serving SLOs, choose batching and admission policies, diagnose tail latency, and perform a guarded, observable rollout.

## Next

Begin [AI Platform Engineering](../32-ai-platform-engineering/README.md).
