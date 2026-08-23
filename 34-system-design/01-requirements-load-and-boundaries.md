# Requirements and system boundaries

System design begins by replacing an attractive solution story with a precise account of users, outcomes, invariants, constraints, and exclusions.

## Why it matters

A technically elegant system can be a complete failure when it solves the wrong journey, protects the wrong invariant, or assumes a responsibility that belongs elsewhere.

## How it works

Begin with actors and their critical journeys. Write functional requirements as observable outcomes. Write quality attributes as measured behavior under named conditions: latency at peak traffic, durability after a zone loss, recovery time, privacy constraints, and a cost envelope. State non-goals and deferred journeys as carefully as goals.

Name invariants separately. “An accepted payment is never charged twice” is an invariant; “use Kafka” is not. Identify the system of record, trust boundaries, administrative surfaces, dependencies, and the team responsible for each decision. A context diagram should show external actors and owned systems before an internal component diagram appears.

Resolve uncertainty by classifying it. A fact can be measured, a forecast can be bounded, a preference can be negotiated, and a policy constraint needs an accountable interpretation. Keep an assumption ledger with owner, evidence, confidence, consequence if wrong, and validation date. This makes the design revisable without making it vague.

## See it yourself

Take “build a document assistant” and ask what must remain true. Tenant A must never retrieve tenant B’s text. A cited answer must preserve the source identity. Deletion must become effective within a stated period. These statements immediately expose identity, authorization, provenance, and lifecycle boundaries that “chat over documents” conceals.

## Where it shows up

For a model inference API, an interactive request and a batch evaluation may use the same model but have different latency, fairness, and interruption requirements. Separate journeys prevent one undifferentiated availability target from producing a costly and misleading design.

## When it breaks

Requirements fail when nouns are undefined, averages replace distributions, every journey is called critical, or non-goals remain political secrets. Boundaries fail when two systems can both declare the same fact authoritative. When review stalls, return to one disputed journey and ask who observes what, under which conditions, and what harm follows from failure.

## Practice

**Build:** write a requirements brief for a tenant-aware document assistant: actors, three critical journeys, five quality attributes with conditions, four invariants, non-goals, trust boundaries, owners, and an assumption ledger. **Break:** add legal deletion and one untrusted ingestion source; revise boundaries without silently weakening an invariant. **Explain back:** justify each boundary from ownership, trust, or failure isolation.

## Check yourself

1. How does an invariant differ from a quality attribute?
2. Why must a performance target name its operating condition?
3. Which uncertainty belongs in an experiment rather than a meeting?

## Sources

### REQUIRED

- [Google SRE Workbook: Implementing SLOs](https://sre.google/workbook/implementing-slos/)

### RECOMMENDED

- [NIST SP 800-160 Volume 1: Systems Security Engineering](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final)

### DEEP DIVE

- [RFC 2119: Key words for use in RFCs](https://www.rfc-editor.org/rfc/rfc2119)

## Next

Continue to [Estimation and capacity](02-estimation-and-capacity.md).
