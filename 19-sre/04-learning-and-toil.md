# Learning reviews and toil reduction

SRE improves systems after incidents by explaining contributing conditions and changing defenses. It improves teams by identifying repetitive operational work whose growth is coupled to service growth.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

A learning review reconstructs timeline, impact, detection, response, causal conditions, and why defenses were absent or ineffective. Actions should name owner, due condition, verification, and the risk they reduce. Avoid monocausal stories and counterfactual certainty.

Toil is manual, repetitive, automatable, tactical, low enduring value, and service-growth-linked. Measure categories and interruptions. Eliminate causes first, then simplify, automate, or safely delegate. Automation needs tests, rollback, observability, and ownership.

## See it yourself

Automating a five-minute task run 1,000 times saves about 83 operator hours, but only if the automation does not create greater review and failure cost. Frequency times duration is a prioritization bound, not a complete business case.

## Where it shows up

Repeated certificate renewal, quota adjustment, and deployment recovery are common toil. A mature review can choose documentation, product change, capacity control, or automation based on risk.

## When it breaks

Reviews can become blame narratives, action lists can grow without closure, and automation can amplify privilege or mistakes. Audit completion by verified risk reduction, not ticket count; retain manual escape paths for dangerous workflows.

## Practice

Classify two weeks of operational tasks using the toil criteria. Select one and build a guarded automation design. Inject partial failure. Completion means it is idempotent, observable, bounded, reversible, and demonstrably reduces human steps.

## Check yourself

1. What makes repetitive work toil rather than operations?
2. Why is a root-cause label often misleading?
3. How should an action item prove completion?
4. When should a task be eliminated instead of automated?

## Sources

### REQUIRED

- [Google SRE: Eliminating Toil](https://sre.google/sre-book/eliminating-toil/)

### RECOMMENDED

- [Google SRE Workbook: Postmortem Culture](https://sre.google/workbook/postmortem-culture/)

### DEEP DIVE

- [Learning From Incidents](https://www.learningfromincidents.io/)

## Next

[Capacity planning and overload](05-capacity-and-overload.md)
