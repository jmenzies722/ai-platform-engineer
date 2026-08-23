# The efficient inference service nobody could wait for

> **Synthetic/composite case:** Alder AI, its people, workloads, prices, measurements, and decisions are fictional. The case combines common model-serving tradeoffs for teaching and does not describe a real company.

## Context and constraints

Alder serves one 13-billion-parameter text model on eight identical GPU workers. Two products share it:

- **Assist** is interactive. Its objective is time to first token below 800 ms at p95, with at least 99.5 percent successful admission inside its purchased tier.
- **Enrich** processes documents asynchronously. Its objective is 95 percent completion within 20 minutes.

Finance reports an allocated GPU cost of $2.40 per worker-hour. The serving team reports cost per million generated tokens, but currently divides GPU cost by successful output tokens only. Product wants the monthly bill down 15 percent without lowering answer-quality gates. The next reserved-capacity change cannot take effect for a week.

The scheduler revision under review increased the batch wait from 20 ms to 180 ms and the token budget per batch from 8,192 to 24,576. It also put both products into one FIFO queue. Model weights and quantization did not change.

Constraints:

- Eight workers are the hard capacity ceiling during the decision window.
- Worker startup and model loading take four minutes.
- Assist requests have a 1.5-second first-token deadline; Enrich can wait.
- Requests vary from 200 to 12,000 prompt tokens and may generate up to 1,000 tokens.
- Tenant quotas exist, but there is no class reservation or maximum queue age.
- A rejected Assist request is visible to the caller; a timeout often triggers one client retry.
- The team may change scheduler and admission policy, but not model quality or product promises unilaterally.

This case uses the models in [Latency, throughput, and batching](../31-model-serving/01-latency-throughput-and-batching.md), [Memory, routing, and overload](../31-model-serving/02-memory-routing-and-overload.md), [KV cache and continuous batching](../31-model-serving/05-kv-cache-and-continuous-batching.md), and [Routing, autoscaling, and overload](../31-model-serving/07-routing-autoscaling-and-overload.md). The [overload lab](../labs/17-model-serving-overload/README.md), [inference latency drill](../incidents/10-inference-latency/README.md), [queue overload drill](../incidents/12-queue-overload/README.md), and [model-serving system project](../projects/12-model-serving-system/README.md) provide hands-on companions.

## Stage 1: the efficiency win

The new scheduler runs for three days under a replay workload. Finance and platform dashboards show:

| Fleet measure | Revision 18 | Revision 19 |
|---|---:|---:|
| GPU utilization | 58% | 76% |
| Mean decode batch width | 11.2 | 24.7 |
| Generated tokens/s per worker | 1,180 | 1,530 |
| Successful output tokens/hour | 31.7M | 40.2M |
| Allocated GPU cost/hour | $19.20 | $19.20 |
| Reported cost/million successful output tokens | $0.61 | $0.48 |

The platform lead proposes immediate rollout. The change appears to cut reported unit cost by 21 percent, beyond the finance target.

### First complication

The replay combines request volume but not original arrival times. It submits Enrich work at a smooth rate and excludes timed-out attempts. Assist product telemetry from a 10 percent canary says:

| Assist measure | Baseline | Revision 19 canary |
|---|---:|---:|
| Time to first token p50 | 310 ms | 465 ms |
| Time to first token p95 | 640 ms | 1,280 ms |
| Inter-token latency p95 | 36 ms | 37 ms |
| First-token deadline exceeded | 0.3% | 4.9% |
| Client attempts/original request | 1.01 | 1.04 |

The scheduler is more efficient at completed token production and worse at the interactive outcome. The current unit-cost denominator makes the failed and rejected demand disappear, even though it consumes gateway, queue, prefill, and support capacity.

## Competing hypotheses

1. The longer batch window directly adds queue delay at low and moderate arrival rates.
2. FIFO mixing lets large Enrich prefills block Assist decode and admission.
3. Revision 19 causes a GPU kernel regression.
4. A specific worker or route is hot, unrelated to scheduler policy.
5. Client retries amplify offered load after deadlines, making a manageable regression unstable.
6. The canary has too little traffic to form efficient batches and will improve at full rollout.

Record what would distinguish queue delay, execution regression, route skew, and workload-mix effects. In particular, decide whether full rollout is a safe experiment.

## Stage 2: decompose work, not just requests

Traces and per-class scheduler data arrive:

```text
assist request=a-104
  queue_ms=711 prefill_ms=106 first_decode_ms=24
  prompt_tokens=884 generated_tokens=146
  batch_wait_limit_ms=180 blocked_by_prefill_tokens=11720

enrich request=e-882
  queue_ms=179 prefill_ms=936 first_decode_ms=26
  prompt_tokens=11720 generated_tokens=384

assist request=a-105 retry_of=a-105-original
  queue_ms=804 cancelled_after_ms=1500 generated_tokens=0
```

| Revision 19 cohort | Queue p95 | Prefill p95 | Decode/token p95 | Deadline failures |
|---|---:|---:|---:|---:|
| Assist alone | 274 ms | 132 ms | 37 ms | 0.8% |
| Assist mixed with Enrich | 892 ms | 138 ms | 37 ms | 5.2% |
| Enrich | 1.9 s | 1.1 s | 41 ms | not applicable |

Route distribution varies by less than 3 percent and no worker has abnormal execution or memory pressure. At peak, original demand is 92 Assist requests/s and 21 Enrich requests/s. Retries add 6 Assist attempts/s. Completion is 107 requests/s while offered attempts are 119/s, so oldest queue age rises.

The evidence lowers the kernel and hot-worker hypotheses. A longer wait contributes, but mixed FIFO scheduling and retry amplification explain the tail. Full rollout would expose all Assist traffic before admission and fairness are bounded; it is not a safe discriminating test.

## Stage 3: the cost denominator fights back

Finance asks for a decision using useful outputs rather than device activity. For the peak hour:

| Item | Revision 18 | Revision 19 projected |
|---|---:|---:|
| GPU cost | $19.20 | $19.20 |
| Successful Assist requests | 306,000 | 289,000 |
| Successful Enrich documents | 67,000 | 74,000 |
| Generated tokens from successful work | 31.7M | 40.2M |
| Generated tokens discarded after cancellation | 0.4M | 2.9M |
| Deadline failures | 1,100 | 18,400 |
| Retry attempts | 3,200 | 21,600 |

The $0.48 token figure is arithmetically correct for its narrow denominator, but it is not a complete economic result. Revision 19 generates more Enrich tokens, serves fewer successful Assist requests, and spends more work on cancelled attempts. A single blended token unit also treats an interactive success and an offline token as interchangeable when their product commitments differ.

The group adopts three paired measures:

1. accelerator cost per million **accepted and delivered** tokens, with cancelled compute shown separately;
2. accelerator cost per successful Assist request meeting its first-token objective;
3. accelerator cost per Enrich document completed inside 20 minutes.

All are segmented by class, prompt band, tenant, and scheduler revision. None may be presented without deadline-failure, quality, and rejection guardrails.

## Options and tradeoffs

| Option | Latency effect | Throughput and cost effect | Fairness and overload effect |
|---|---|---|---|
| Keep one FIFO queue and reduce wait to 20 ms | Improves queue floor; large prefills can still block | Gives back some batch efficiency | Does not establish class protection |
| Separate class queues with weighted scheduling | Bounds cross-class blocking | May leave some slots unfilled; preserves offline batching | Makes product priority explicit and testable |
| Reserve six workers for Assist and two for Enrich | Strong isolation | Stranded capacity when one class is quiet | Simple but coarse; capacity split needs governance |
| Admit every request and add a larger queue | Fewer immediate rejections | Converts overload into missed deadlines and wasted work | Old work can starve new feasible work |
| Bound queue age and token reservations | Rejects requests that cannot meet contract | Avoids doomed prefill/decode; improves useful-unit cost | Requires explicit retry and tenant policy |
| Disable retries | Removes amplification | May reduce eventual success during brief faults | Needs coordinated client contract |
| Add workers | Adds headroom after load time | Raises cost and misses the immediate event | Does not fix unfair scheduling |

## Decision

The team rolls revision 19 back for Assist and keeps it for an isolated Enrich pool. It then canaries revision 20 with:

- separate Assist and Enrich queues;
- weighted service with a minimum Assist share and an Enrich starvation bound;
- a 25 ms Assist batch-wait cap and a 180 ms Enrich cap;
- token-based batch and KV-cache reservations rather than request counts;
- admission that rejects work when predicted queue age cannot fit the remaining deadline;
- a maximum prompt and generation budget by product tier;
- no automatic retry after a deadline; overload responses include a bounded retry hint only when capacity is expected;
- cancellation propagated to queued work and runtime slots;
- per-class queue age, admitted tokens, completed tokens, discarded compute, and unit cost.

Six workers remain in the shared revision 20 pool and two run Enrich revision 19 during the canary. The split is a temporary safety boundary, not the final architecture. Advancement requires Assist p95 below 800 ms, deadline failures below 0.5 percent, Enrich completion within objective, no tenant starvation, and cost per successful class outcome no worse than revision 18.

The decision gives up a portion of maximum token throughput to restore a product latency contract and make overload finite. It does not promise that every offered request succeeds. It promises that accepted work has a credible path to its deadline and rejected work fails explicitly before consuming scarce execution.

## Consequence and review

Under a production-shaped replay preserving arrivals and cancellations, revision 20 produces:

| Measure | Revision 18 | Revision 19 mixed | Revision 20 |
|---|---:|---:|---:|
| Assist first-token p95 | 640 ms | 1,280 ms | 690 ms |
| Assist deadline failures | 0.3% | 4.9% | 0.4% |
| Enrich completed within 20 min | 96.1% | 98.7% | 97.9% |
| Generated tokens/s per worker | 1,180 | 1,530 | 1,410 |
| Discarded GPU work | 1.2% | 7.2% | 1.8% |
| Cost/million delivered tokens | $0.61 | $0.48 | $0.53 |

Revision 20 is less impressive on raw token cost than revision 19, but it restores the Assist latency objective and remains within the Enrich objective. During a burst, 0.7 percent of Assist requests receive explicit overload responses. Product accepts this bounded rejection because the alternative was 4.9 percent opaque deadline failure plus retries.

The review also finds that Enrich's 20-minute objective allows scheduled smoothing. Moving part of that workload away from the Assist peak reduces required warm capacity more cheaply than adding a worker. The replay does not establish Finance's 15 percent savings goal because the summary lacks a defensible allocation of shared GPU time, idle residency, and platform cost to each product class. That claim remains open until raw class-level events and an agreed allocation rule are reviewed.

## Reusable engineering lessons

1. Inference latency is a staged budget: admission, queue, prefill, first decode, and subsequent decode should be visible separately.
2. High utilization and high token throughput are not product success when the wrong class waits or work is discarded.
3. Batch policy must reflect arrival shape and token size. A request count hides large prefills and KV-cache commitments.
4. Near saturation, a larger queue stores lateness. Admission should reject work whose deadline is no longer feasible.
5. Queue discipline is product policy. Priority, reservations, and starvation bounds encode which promises hold under contention.
6. Retries are new offered load. They need deadlines, jitter, attempt caps, and a reason to believe another attempt can succeed.
7. Autoscaling cannot cover a four-minute model load for a sub-second objective without warm or scheduled headroom.
8. Unit cost needs a useful, quality-constrained denominator. Segment classes whose outcomes are not interchangeable.
9. Demand shaping can be an economic control. Flexible offline work should not silently consume interactive latency headroom.

## Evidence exercise

1. For each stage, update a hypothesis table with support, contradiction, discriminating test, and confidence.
2. Calculate backlog growth at peak from original demand, retries, and completion. State why Little's Law is not a stability promise during this interval.
3. Draft an Assist latency budget across gateway, admission, queue, prefill, and first decode. Include a cancellation reserve.
4. Define admission pseudocode using remaining deadline, estimated token cost, queue age, and tenant budget. State what happens when the estimate is missing.
5. Specify the raw events and allocation rule needed to compute class-aware cost per successful Assist request and per Enrich document. Explain why the summary table cannot support those figures, then list labor, idle residency, and shared-service costs a GPU-only calculation would still omit.
6. Design a load matrix spanning arrival burstiness, prompt bands, generation limits, class mix, retries, and cancellations.
7. Reproduce bounded overload in the [model-serving overload lab](../labs/17-model-serving-overload/README.md), then explain why its fixed 100 ms service time cannot validate GPU batching economics.

## Teach-back prompts

1. When does batching reduce unit cost, and when is batch wait pure delay?
2. Why did stable inter-token latency matter to the hypothesis ranking?
3. Is an explicit rejection a reliability failure? Answer separately for offered, admitted, and promised service.
4. What policy would prevent Enrich starvation without restoring FIFO head-of-line blocking?
5. Why is cost per generated token an incomplete measure even when computed correctly?
6. If finance demanded another 10 percent reduction, which evidence would help you choose demand shaping, quantization, lower warm headroom, or a changed product objective?
