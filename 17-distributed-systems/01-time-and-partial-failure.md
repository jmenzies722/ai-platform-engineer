# Time, ordering, and partial failure

A distributed caller cannot instantly distinguish a slow peer, a lost message, a partition, and a failed process.

## Why it matters

Timeouts and clocks are evidence with uncertainty, not truth. Designs that assume a single global order produce duplicate actions, stale writes, and split-brain decisions.

## How it works

Wall clocks can jump because of synchronization or administrator changes. Monotonic clocks measure elapsed time locally but cannot order events across machines. Causality gives a partial order: if event A can influence B, A happened before B; concurrent events may have no meaningful order.

A timeout bounds how long a caller waits. It does not prove the remote operation failed: the response may be lost after the side effect committed. Failure detectors are therefore suspicions tuned between fast detection and false positives.

## See it yourself

List outcomes when a client times out after sending `charge(card, $10)`: request lost, server still running, charge rejected, charge committed with reply lost. The same client observation fits all four.

## Where it shows up

Leader leases, cache expiry, request deadlines, database timestamps, and incident timelines all rely on explicit clock assumptions.

## When it breaks

Clock skew expires valid credentials, last-write-wins discards a causally later update, and synchronized retries turn a slow dependency into an outage.

## Practice

Rewrite one synchronous call contract to include deadline, uncertain outcome, retry ownership, and a query for final status.

## Check yourself

1. What does a timeout prove?
2. When is a monotonic clock preferable?

## Sources

### REQUIRED
- [Google SRE: Handling overload](https://sre.google/sre-book/handling-overload/)

### RECOMMENDED
- [AWS Builders' Library: Timeouts and retries](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

### DEEP DIVE
- [Time, Clocks, and Ordering of Events](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)

## Next

[Replication, consistency, and consensus](02-replication-and-consensus.md)
