# Incidents and learning

Incident response restores user service first, preserves coordination under pressure, and turns evidence into safer systems afterward.

## Why it matters

Unstructured response duplicates work and makes risky changes. Blame suppresses evidence; accountability requires understanding why actions made sense with information available then.

## How it works

Declare an incident early. Assign an incident commander, operations lead, communications lead, and scribe as scale requires. Establish impact, timeline, hypotheses, and decision log. Prefer reversible mitigation that limits blast radius. Communicate known facts, unknowns, and the next update time.

After recovery, reconstruct contributing technical and organizational conditions. Corrective actions need an owner, priority, and verifiable completion condition. Track recurring patterns, not only the final trigger.

## See it yourself

Compare "database caused outage" with evidence: connection saturation began after retry volume rose, a new timeout reduced client patience, and alerts tracked CPU rather than successful checkout.

## Where it shows up

On-call rotations, runbooks, status updates, incident reviews, and game days form one learning system.

## When it breaks

Too many commanders conflict, responders change multiple variables, executives bypass coordination, or reviews produce dozens of unowned tasks.

## Practice

Run a tabletop for a regional checkout failure. Write roles, first three evidence queries, safe mitigations, and communication cadence.

## Check yourself

1. Why separate command from hands-on operations?
2. What makes a corrective action testable?

## Sources

### REQUIRED
- [Google SRE: Managing incidents](https://sre.google/sre-book/managing-incidents/)

### RECOMMENDED
- [Google SRE Workbook: Postmortem culture](https://sre.google/workbook/postmortem-culture/)

### DEEP DIVE
- [NIST incident response guidance](https://csrc.nist.gov/pubs/sp/800/61/r3/final)

## Next

[Toil, capacity, and sustainable operations](03-toil-and-capacity.md)
