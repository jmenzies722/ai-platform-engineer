# Lab: Run an adversarial design review

This lab tests whether a design can survive disciplined disagreement. The goal is not unanimous approval. The goal is a decision whose evidence, risks, owners, and revisit conditions are legible.

## Roles

Assign at least four reviewers. One owns reliability, one security and privacy, one product outcomes, and one cost and operations. A fifth person acts as decision owner. The author may answer questions but may not change a requirement verbally; changes must enter the packet.

## Round one: silent inspection

Each reviewer writes:

- one requirement that is not measurable;
- one invariant without a clear enforcement point;
- one estimate whose source or unit is missing;
- one correlated failure or overload path;
- one unsafe security, privacy, or deletion assumption;
- one operational question the telemetry cannot answer;
- one cost or quality sensitivity that could reverse the decision;
- one migration state with no tested recovery.

Reviewers classify each observation as a correctness blocker, evidence request, risk acceptance, or preference. Preferences cannot masquerade as blockers.

## Round two: fault hearing

The facilitator introduces three cards in order:

1. A timeout occurs after a side effect commits, and the caller retries.
2. The provider and failover region degrade during a hot-tenant burst.
3. A model migration passes aggregate quality but regresses one regulated-language slice.

For each card, the author traces identity, authority, state, telemetry, user consequence, and safe response. Reviewers may ask what observation would disprove the explanation. The recorder captures unknowns rather than allowing invented certainty.

## Round three: decision

The decision owner chooses approve, approve with bounded conditions, request revision, or reject. Record:

- decision and accountable owner;
- alternatives considered;
- blocking conditions and the evidence that closes each;
- accepted residual risks and the person authorized to accept them;
- dissent and why it did not control the decision;
- rollout and rollback authority;
- production measures and review date;
- triggers that reopen the decision;
- cleanup owner and date.

## Quality bar

Repeat the review if a component cannot be traced to a requirement, a risk has no owner, a reviewer invokes “best practice” without mechanism, or rollback ignores durable state. A successful review may reject the design. It may not produce ambiguous approval.

## Debrief

Individually write which fact changed your view, which value conflict required ownership rather than more data, and which question exposed the largest hidden consequence. Then compare the review record with the packet and make every accepted change explicit.

## Completion

Continue to [Senior and Staff Engineering](../35-senior-staff-engineering/README.md) after a reviewer unfamiliar with the design can accurately explain its invariants, overload behavior, and migration risk.
