# Availability architecture and failure domains

Availability is an end-to-end property of dependencies, state, traffic policy, and recovery. Redundant instances improve it only when failures are sufficiently independent and failover itself is safe.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

For independent serial components, availability multiplies; redundant parallel paths reduce shared outage only when they do not share control planes, identities, quotas, or data risks. Map zones, regions, accounts, DNS, certificates, databases, and human access as failure domains.

Set recovery time and recovery point objectives from business impact. Backups address data loss only if restore procedures, keys, dependencies, and integrity checks work. Disaster recovery ranges from restore to warm standby to active-active, with increasing consistency and operational complexity.

## See it yourself

Two serial dependencies each at 99.9% yield approximately `0.999 × 0.999 = 99.8001%`, before other failures. This simple bound shows why a service cannot promise more than critical dependencies without masking or substituting them.

## Where it shows up

Use dependency budgets, timeout isolation, bulkheads, fallback, and tested traffic failover. Run game days that verify user outcome, not merely instance replacement.

## When it breaks

Nominally redundant paths can share IAM, a corrupt write can replicate everywhere, DNS caching can delay failover, and cold capacity can fail under backlog. Inspect common dependencies, restoration throughput, control-plane health, and data correctness.

## Practice

Draw a failure-domain map and calculate an availability bound. Restore a test backup and simulate loss of one zone. Completion means the user journey meets stated RTO and RPO and every shared dependency has an explicit mitigation or accepted risk.

## Check yourself

1. Why does replication not replace backup?
2. What assumption underlies parallel availability math?
3. How do RTO and RPO differ?
4. Which shared control plane defeats your redundancy?

## Sources

### REQUIRED

- [Google SRE: Distributed Systems for Fun and Profit](https://sre.google/sre-book/distributed-systems/)

### RECOMMENDED

- [AWS Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)

### DEEP DIVE

- [NIST SP 800-34 Rev. 1](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final)

## Next

[Release engineering and resilience](07-release-resilience.md)
