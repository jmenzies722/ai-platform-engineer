# Practical lab: simulate an accelerator cluster

Build a deterministic event-driven simulator that makes cluster placement, queueing, failure, checkpoint, and cost tradeoffs inspectable.

## Why it matters

Production experiments are expensive and confounded. A small model forces assumptions into code and creates repeatable counterexamples before policy reaches a real fleet.

## How it works

Represent nodes with rack, GPU type, count, health, and network island. Represent jobs with arrival, gang shape, duration, priority, topology, checkpoint interval, and preemptibility. Advance a logical clock across arrivals, completions, checkpoints, failures, and repairs. Implement FIFO plus conservative backfill; emit an append-only JSON event log.

Track queue age, completion time, GPU-hours allocated, useful GPU-hours, lost work, checkpoint bytes, and cost per completion. Seed randomness and record configuration digest so runs replay exactly.

## See it yourself

Submit four scattered one-GPU jobs before one eight-GPU gang on two eight-GPU nodes. Compare spread and pack placement. Then fail one rack halfway through a job with 30-minute checkpoint intervals. Predict expected lost work near 15 minutes for uniformly timed failures, while this deterministic run has an exact value.

## Where it shows up

Trace replay supports capacity reviews, scheduler-policy tests, maintenance planning, and incident exercises. Real arrival and duration distributions can replace fixtures after removing sensitive tenant data.

## When it breaks

Perfect runtime knowledge unfairly favors backfill; independent failures understate correlated loss; fixed bandwidth ignores contention; cost without quality rewards rejected work. State every simplification and perform sensitivity runs. Never present simulator output as a forecast without calibration.

## Practice

**Build:** implement placement, gang admission, quotas, backfill, preemption, checkpoints, rack failure, and cost accounting with at least fifteen tests. **Break:** inject fragmentation, a storage slowdown, a bad checkpoint, a slow rank, and correlated rack loss. **Explain back:** compare two policies using wait quantiles, useful utilization, lost work, and cost per completion. Completion requires deterministic replay and a report identifying which conclusion changes under one sensitivity test.

## Check yourself

1. Which unrealistic oracle can make backfill look too good?
2. How do useful and allocated GPU-hours differ?
3. What event proves a resumed job used a complete checkpoint?

## Sources

### REQUIRED

- [Volcano scheduling concepts](https://volcano.sh/en/docs/)

### RECOMMENDED

- [SimPy documentation](https://simpy.readthedocs.io/en/latest/)

### DEEP DIVE

- [Borg trace data](https://github.com/google/cluster-data)

## Next

Continue to [Model Serving](../31-model-serving/README.md).
