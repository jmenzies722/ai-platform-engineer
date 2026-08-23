# Reliability, overload, and recovery

Reliable systems preserve the most important user outcomes and invariants when components are slow, unavailable, overloaded, or wrong.

## Why it matters

Redundancy without bounded retries, tested failover, and recovery evidence can multiply failure rather than contain it.

## How it works

Define service level indicators from user-visible outcomes, then set objectives and an error budget. Map dependencies and failure domains: process, host, zone, region, identity provider, control plane, and human operation. Redundancy helps only when copies do not share the same hidden dependency and failover capacity exists.

Every remote call needs a deadline derived from the caller’s remaining budget. Retry only transient failures, with backoff, jitter, and a bounded attempt budget. Limit concurrency, shed low-priority work, and use circuit breaking to stop spending resources on a failing dependency. Graceful degradation must preserve security and correctness; a stale recommendation may be acceptable while a stale authorization decision may not.

Recovery has two clocks. Recovery point objective bounds acceptable data loss; recovery time objective bounds restoration. Backups are claims until restore drills prove integrity, access, tooling, and elapsed time. Run game days that test detection, decision authority, failover, reconciliation, and return to normal, not only infrastructure automation.

## See it yourself

Three layers each retry three times, so one user request can produce up to twenty-seven calls at the deepest dependency. During overload, this retry multiplication steals capacity from fresh work. Move retries to one layer, impose a shared deadline and budget, add jitter, then compare downstream attempts and successful user outcomes.

## Where it shows up

An AI assistant may degrade from generated answers to cited search results when model capacity is unavailable. That path needs its own quality, security, and telemetry contract. Returning an uncited guess is not graceful degradation when provenance is a core requirement.

## When it breaks

Failures cascade through synchronized retries, failover overloads the healthy region, health checks remove all capacity, or a restore reveals missing keys. Diagnose resource saturation and dependency latency before restarting. Protect the control path, stop amplification, preserve evidence, and choose degradation according to declared priorities.

## Practice

**Build:** write a reliability model for an inference service with SLIs, objectives, dependency budgets, overload policy, degraded modes, RPO, RTO, and restoration procedure. **Break:** lose a zone while a provider throttles and a backup key is unavailable. **Explain back:** decide which traffic survives and prove that your response protects critical invariants.

## Check yourself

1. Why does redundancy fail when dependencies are correlated?
2. How can layered retries amplify an outage?
3. What evidence turns an RTO from hope into a claim?

## Sources

### REQUIRED

- [Google SRE Workbook: Implementing SLOs](https://sre.google/workbook/implementing-slos/)

### RECOMMENDED

- [Amazon Builders’ Library: Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

### DEEP DIVE

- [Google SRE Book: Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/)

## Next

Continue to [Security, privacy, and abuse resistance](09-security-privacy-and-abuse-resistance.md).
