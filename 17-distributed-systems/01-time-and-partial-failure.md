# Time, causality, and partial failure

A distributed observation is local evidence, not omniscient truth. A timeout says that a result did not arrive before a deadline; it cannot say whether the peer never started, is slow, committed, crashed, or lost its reply.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Wall clocks approximate civil time and can jump. Monotonic clocks measure local intervals without stepping backward, but cannot compare events on different hosts. Lamport clocks preserve the rule that causal events receive increasing timestamps; vector clocks can also expose concurrency, at a metadata cost proportional to participants.

A failure detector converts missing evidence into suspicion. Its timeout trades detection speed against false suspicion. Production protocols therefore attach epochs or fencing tokens to authority: a paused former leader may resume, but storage rejects its stale epoch.

## See it yourself

Predict the four states possible after `charge` times out: request absent, request running, charge rejected, or charge committed with reply lost. The same client symptom fits every state. This is a small indistinguishability proof: if local observations are identical, no local algorithm can always choose the correct state without more communication or durable identity.

## Where it shows up

Lease renewal, cache expiry, credential validation, database conflict resolution, and incident timelines all encode clock assumptions. A job scheduler should use a monotonic deadline for elapsed time and a durable epoch for ownership, while retaining wall time only for human audit.

## When it breaks

Clock steps can expire valid credentials; stop-the-world pauses can outlive leases; last-write-wins can discard a causally later write; and a partition can make two healthy nodes suspect each other. Diagnose with monotonic durations, synchronization state, epoch values, and message histories rather than sorted wall-clock logs alone.

## Practice

Observe wall and monotonic time in a short program, then design a lease record containing owner, epoch, and expiry. Break it by pausing the owner beyond expiry. Completion means the resumed owner is fenced from writing and you can explain which observation caused each transition.

## Check yourself

1. What does a timeout prove, and what remains unknowable?
2. Why can a monotonic clock measure a deadline but not order two hosts?
3. How does a fencing token make a false suspicion safe?
4. Which evidence distinguishes clock skew from network delay?

## Sources

### REQUIRED

- [Time, Clocks, and the Ordering of Events](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)

### RECOMMENDED

- [AWS Builders' Library: Timeouts, retries, and backoff](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

### DEEP DIVE

- [Unreliable Failure Detectors for Reliable Distributed Systems](https://www.cs.cornell.edu/home/rvr/papers/UnreliableFD.pdf)

## Next

[Consistency models and client guarantees](02-consistency-models.md)
