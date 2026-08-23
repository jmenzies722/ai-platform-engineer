# Lab: Organizational pressure simulation

This simulation tests judgment when evidence, authority, incentives, and time pull in different directions. Assign a technical lead, product executive, security owner, application lead, platform operator, developing engineer, and observer.

## Initial decision

The technical lead has twenty minutes to present the operating packet. Each participant writes the decision they believe is required, their responsibility, expected burden, and strongest objection. Compare answers. Material differences indicate failed shared understanding and must be resolved in the written record.

## Pressure cards

Introduce one card every twelve minutes:

1. The executive moves launch forward by six weeks but offers no additional migration capacity.
2. Security reports that one team’s credential can invoke tools across tenants.
3. The largest product team rejects the platform after a previous mandate increased latency.
4. A provider offers a 45 percent discount tied to a two-year exclusivity clause.
5. Aggregate evaluation improves, but one language slice regresses enough to increase human escalations.
6. The developing engineer leading the RFC recommends an alternative the technical lead did not expect.
7. During canary, an incident exposes retrieved text across two tenants; an executive asks to restore service before isolation is proven.
8. A reorganization moves identity ownership and removes the original sponsor.

After each card, the lead must update facts, assumptions, scope, decision owner, commitments, risks, and communication. They may stop or narrow the program. They may not silently weaken tenant isolation, conceal evidence, reclaim delegated authority for stylistic reasons, or call a values conflict a technical fact.

## Observer rubric

Record concrete evidence for whether the lead:

- separated fact uncertainty from value and policy conflict;
- made consequence, options, and decision authority legible;
- preserved dissent and credit;
- changed scope by explicit tradeoff;
- protected affected users during incident pressure;
- adapted organizational interfaces after authority moved;
- used escalation without drama or surprise;
- transferred rather than accumulated responsibility;
- distinguished a durable platform contract from a fashionable implementation;
- named ethical limits and residual risk ownership.

## Incident segment

For card seven, establish incident command, operations, communications, and scribe. Require timed updates, one owner per action, evidence preservation, containment, recovery criteria, reconciliation, and a stakeholder message. The technical lead fails the exercise if they personally seize every role or declare recovery without proving the isolation invariant.

## Debrief

Each participant answers:

1. Which piece of evidence changed your recommendation?
2. Which conflict required authority rather than more analysis?
3. Where did the lead’s informal power help or suppress understanding?
4. Which mechanism will function when the lead is absent?
5. What should be stopped, not improved?

Revise the packet with decisions, dissent, owners, and review triggers. Repeat one pressure card with another person as technical lead.

## Completion

Return to the [curriculum](../CURRICULUM.md) only when the second lead can preserve user safety, decision clarity, and execution ownership without coaching from the original author.
