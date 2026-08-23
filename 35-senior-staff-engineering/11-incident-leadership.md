# Incident leadership

Incident leadership creates a calm decision system when evidence is incomplete, consequences are growing, and normal coordination is too slow.

## Why it matters

Deep technical skill does not compensate for unclear command, unsafe simultaneous action, lost evidence, or stakeholders learning different versions of reality.

## How it works

Establish incident commander, operations lead, communications lead, and scribe. State user impact, scope, current hypothesis, actions in flight, and next update. The commander protects priorities and decision flow rather than personally debugging every component.

Prefer reversible containment before elegant diagnosis when harm is active. Assign one owner per action, record timestamps and expected observations, and stop changes that cannot be interpreted. Preserve logs and audit evidence. Communicate confirmed facts, uncertainty, decisions, and user guidance without speculation.

Declare recovery only after user outcomes and critical invariants are verified. Reconcile data, remove temporary access, restore capacity, and monitor recurrence. A blameless review reconstructs conditions and mechanisms, assigns durable actions, and examines why defenses failed. Rotate incident authority through practice.

## See it yourself

During a cross-tenant retrieval incident, one engineer tunes ranking while another flushes caches and a third rotates credentials. No observation can isolate cause. Command pauses independent changes, disables affected retrieval, preserves evidence, and sequences tests. Slower hands produce faster understanding.

## Where it shows up

Staff engineers lead high-severity reliability, security, data integrity, vendor, and AI quality incidents and improve the response system afterward.

## When it breaks

Incidents break through command-by-loudest-person, status-channel debugging, premature recovery, executive interference, and postmortems that list human mistakes. Reassert roles, user impact, action ownership, and update cadence.

## Practice

**Build:** run a timed simulation of cross-tenant retrieval during provider throttling. Maintain command roles, action log, stakeholder updates, containment, recovery criteria, and follow-up. **Break:** add an executive request to restore service before isolation is proven. **Explain back:** protect authority and user safety respectfully.

## Check yourself

1. Why should the commander avoid owning every diagnostic action?
2. What evidence permits declaring recovery?
3. How does blamelessness differ from lack of accountability?

## Sources

### REQUIRED

- [Google SRE Workbook: Incident Response](https://sre.google/workbook/incident-response/)

### RECOMMENDED

- [NIST SP 800-61 Revision 2](https://csrc.nist.gov/pubs/sp/800/61/r2/final)

### DEEP DIVE

- [Google SRE Book: Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)

## Next

Continue to [Stewardship and durable impact](12-stewardship-and-durable-impact.md).
