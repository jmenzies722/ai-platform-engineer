# Model serving operator sheet

Follow one request through routing, admission, queueing, prefill, decode, and
response delivery. Separate quality, latency, throughput, memory, and overload
before tuning the runtime.

## Frame the request class

Record tenant, model and immutable revision, endpoint, region, streaming mode,
prompt-token bucket, requested output limit, sampling configuration, arrival
rate, priority, start time, and recent rollout or traffic changes. Use request
IDs and token counts, never prompt or generated text, in ordinary diagnostics.

Partition latency into queue time, time to first token, inter-token latency, and
total completion time. A single end-to-end percentile cannot identify whether
admission, prefill, or decode is distressed.

## Is the intended model revision serving?

Compare the gateway route, model digest, tokenizer revision, runtime build,
quantization, tensor-parallel shape, replica readiness, and traffic weight.
Model names and mutable tags are insufficient evidence.

For a bounded synthetic request, preserve the returned request ID, serving
revision, token counts, status, and timings through the platform's approved
interface. A successful health endpoint proves neither correct routing nor
successful generation.

If errors began with a rollout, compare canary and baseline using equivalent
request classes. Do not infer model quality from transport success.

## Is admission or queueing rejecting work?

Distinguish policy denial, quota exhaustion, rate limiting, concurrency limits,
token-budget rejection, queue timeout, and unavailable capacity. Preserve the
machine-readable reason and retry guidance.

- Rising queue age with stable execution time implicates admission, scheduling,
  or insufficient capacity.
- Rising prompt tokens with worse time to first token implicates prefill work.
- Stable first-token time with worse inter-token latency implicates decode
  contention or memory pressure.
- More retries with no reduced arrival rate can amplify overload.

Do not bypass tenant quota or admission controls during overload. Apply the
documented shedding or priority policy and protect recovery capacity.

## Is KV-cache pressure limiting concurrency?

Estimate per-token KV-cache bytes from layers, KV heads, head dimension, element
size, and keys plus values. Multiply by active and reserved sequence tokens,
then add weights, runtime workspaces, allocator overhead, and safety margin.
Request count alone is not a memory forecast.

Inspect active sequences, admitted token budget, free cache blocks, allocation
failures, evictions, cancellations, leaked blocks, and per-replica sequence
length distribution. Interpret:

- Free blocks decline with admitted tokens and recover on completion: expected
  lifecycle pressure.
- Blocks do not recover after cancellation or completion: lifecycle leak.
- Allocation fails despite many total free bytes: fragmentation or block-shape
  constraints are plausible.
- One replica fills while peers remain free: routing affinity or stale load
  information is plausible.

Reducing output limits or concurrency can protect memory, but it changes the
service contract. Record which request classes are shed.

## Is continuous batching helping or hurting?

Continuous batching admits and removes sequences between decode iterations.
Inspect decode batch width, tokens generated per iteration, scheduler delay,
prefill chunking, preemption, and service by tenant and priority.

A high batch width can improve aggregate throughput while worsening tail
latency. A large prefill can block decode. Aggressive preemption can waste
recomputation. Compare throughput and latency for the same arrival and
prompt/output distribution; do not tune against an average request.

## Is prefix caching safe and effective?

Measure eligible prompt tokens, lookup rate, reused tokens, eviction rate, and
latency saved. A request-level hit rate can overstate benefit when hits reuse
few tokens.

Cache identity must include the exact token prefix and all serving state that
can change its interpretation, including model and tokenizer revision. Enforce
tenant and privacy boundaries. Do not log raw prefixes or allow reuse across an
unapproved trust boundary. Disable or invalidate reuse after uncertain model,
tokenizer, adapter, policy, or cache-key changes.

## Is the runtime executing efficiently?

Compare runtime counters with device evidence: GPU memory, compute activity,
kernel gaps, host-to-device copies, communication, and failed allocations.
Separate cold load and compilation from steady state.

- Low GPU activity with queue growth suggests host, scheduler, input, or launch
  starvation.
- High activity with low token throughput suggests expensive shapes, an
  inefficient kernel path, communication, or excessive recomputation.
- OOM at admission indicates reservation failure; OOM during decode indicates
  underestimated growth, fragmentation, or a leak.

Quantization, parallelism, speculative decoding, and kernel changes can alter
quality or numerical behavior. Require the applicable evaluation gate before
promotion.

## Controlled mitigation and rollback

Prefer bounded mitigations tied to evidence: shed an explicitly lower-priority
class, cap admitted tokens, drain a bad revision, restore known-good routing, or
reduce one concurrency limit. Define success using error rate, queue age,
first-token latency, inter-token latency, throughput, memory headroom, and
quality guardrails.

A rollback must restore a compatible model, tokenizer, runtime, cache identity,
and request contract. Draining preserves in-flight responses; abrupt
termination may create retries and duplicate client work.

Stop and escalate for cross-tenant cache risk, quality or safety regression,
unknown revision lineage, broad quota changes, persistent memory corruption,
data exposure, or overload without a documented shedding policy.

## Authoritative sources

- [NVIDIA Triton Inference Server user guide](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/)
- [KServe documentation](https://kserve.github.io/website/)
- [vLLM documentation](https://docs.vllm.ai/en/latest/)
- [Hugging Face text-generation-inference documentation](https://huggingface.co/docs/text-generation-inference/index)
- Repository lesson: [Model Serving](../31-model-serving/README.md)
