# Reliable distributed jobs

Distributed AI jobs need coordinated startup, progress preservation, failure classification, and clean termination.

## Why it matters

One failed worker can waste the synchronized work of hundreds of healthy devices.

## How it works

A controller reconciles desired workers, rendezvous assigns membership, and heartbeats expose liveness. Checkpoints atomically capture model, optimizer, scheduler, and data position. Retry policy distinguishes transient infrastructure faults from deterministic code or data failures. Observability correlates job, worker, node, device, and collective events.

Reconciliation separates a durable desired state from replaceable processes. Elastic membership is useful only when the algorithm and checkpoint semantics support changed world size. Checkpoint interval balances write overhead against expected recomputation; a completion marker prevents readers from accepting partial state. Retry budgets include lost accelerator time, not just attempt count.

## See it yourself

If failures arrive uniformly within an interval, expected recomputation is roughly half that interval: 2.5, 15, or 60 minutes. Add a two-minute checkpoint cost incurred each interval. For a four-hour mean time between failures, compare overhead plus expected loss; neither “checkpoint constantly” nor “rarely” is free. The calculation makes policy workload-specific.

## Where it shows up

A controller launching 64 workers records rank and node, waits for rendezvous, and monitors progress steps as well as heartbeats. On a preemption notice it requests a checkpoint and restarts from its verified manifest. Deterministic data errors are quarantined and surfaced rather than retried across new nodes.

## When it breaks

Partial checkpoints appear valid, retries loop on deterministic errors, and a straggler looks alive while blocking collectives. First align the last progress timestamp and error signature across ranks. One repeatable failing sample indicates data or code; changing node-correlated faults indicate infrastructure; all ranks waiting on one arrival identifies a straggler. Verify checkpoint manifest before resume.

## Practice

**Build:** write a controller-state and failure matrix with checkpoint and retry policy. **Break:** inject a partial checkpoint, one deterministic bad sample, and one slow rank; record distinct evidence. **Explain back:** justify checkpoint interval quantitatively and distinguish liveness from forward progress.

## Check yourself

1. What must a resumable checkpoint include?
2. Why bound retries?
3. How is liveness different from progress?

## Sources

### REQUIRED

- [PyTorch distributed checkpoint](https://docs.pytorch.org/docs/stable/distributed.checkpoint.html)

### RECOMMENDED

- [Kubernetes Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/)

### DEEP DIVE

- [PyTorch Elastic](https://docs.pytorch.org/docs/stable/elastic/run.html)

## Next

Continue to [Cluster architecture and failure domains](04-cluster-architecture-and-failure-domains.md).
