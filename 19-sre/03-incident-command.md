# Incident response and command

Incident response is a control system for reducing harm under uncertainty. Clear roles, a stable communication cadence, and explicit decisions preserve attention for mitigation.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Declare based on impact and risk, then assign incident commander, operations lead, communications lead, and scribe as scale requires. Establish user impact, current state, objective, safe next action, owner, and check-in time. Prefer reversible mitigation before deep diagnosis.

Maintain one timeline in UTC, one decision log, and one source of operational truth. Handoffs state impact, mitigations, active hypotheses, disproved hypotheses, risks, and owners. Escalation is capacity management, not failure.

## See it yourself

If ten responders independently query the same dependency and each asks two more people, coordination work grows faster than diagnosis. Role assignment bounds parallel work and converges evidence through one command loop.

## Where it shows up

Runbooks provide safe first moves, access requirements, rollback steps, and verification. Status updates separate known facts from inference and avoid unsupported recovery times.

## When it breaks

Unowned actions conflict, risky restarts destroy evidence, communication goes stale, and tunnel vision overfits the first hypothesis. Watch action ownership, decision timestamps, repeated work, and responder fatigue.

## Practice

Tabletop a regional checkout failure. Rotate commander and scribe, issue two updates, and conduct a handoff. Inject a misleading deploy correlation. Completion means the team mitigates from impact evidence, preserves the alternative hypothesis, and records every risky action.

## Check yourself

1. Why separate command from hands-on operations?
2. What belongs in a handoff?
3. When should diagnosis yield to mitigation?
4. How does a decision log improve safety?

## Sources

### REQUIRED

- [Google SRE: Managing Incidents](https://sre.google/sre-book/managing-incidents/)

### RECOMMENDED

- [NIST SP 800-61 Rev. 2](https://csrc.nist.gov/pubs/sp/800/61/r2/final)

### DEEP DIVE

- [PagerDuty Incident Response Documentation](https://response.pagerduty.com/)

## Next

[Learning reviews and toil reduction](04-learning-and-toil.md)
