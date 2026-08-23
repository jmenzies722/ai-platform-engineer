# Technical vision and architecture direction

A technical vision describes a desirable, credible future and the principles and stepping stones that make progress toward it possible.

## Why it matters

Without shared direction, teams make locally sound choices that compound integration cost; with a rigid target state, they optimize for a future that evidence may invalidate.

## How it works

Describe today’s constraints before tomorrow’s architecture. State future capabilities in user and operator terms, then define principles that guide local decisions: authority boundaries, interoperability, security defaults, ownership, and build-versus-buy posture. Show a small number of architecture shapes without pretending the target is fully specified.

Connect vision to reality through transition states, paved paths, compatibility contracts, adoption incentives, and deprecation. Label commitments, options, and hypotheses. Each principle needs examples of behavior it encourages and rejects. Give teams controlled extension points so alignment does not erase legitimate domain needs.

Vision ownership is stewardship, not authorship. Seek critique from affected teams, publish dissent, and review against incidents, delivery evidence, changing strategy, and external constraints. A vision should become easier to execute without the author in the room.

## See it yourself

“All teams use one model” is brittle standardization. “Applications integrate through versioned evaluation, identity, audit, and quota contracts; approved models remain replaceable behind those contracts” establishes durable boundaries while preserving experimentation.

## Where it shows up

Technical vision guides platform APIs, data ownership, identity, observability, AI serving, and modernization. It gives RFC authors constraints without predetermining every implementation.

## When it breaks

Vision fails through target-state theater, hidden mandates, principles too vague to resolve choices, and no migration economics. Ask two teams to apply a principle to a real disagreement; inconsistent answers expose missing precision.

## Practice

**Build:** produce a three-year technical vision with current constraints, future capabilities, six principles, transition architecture, extension points, adoption path, and review triggers. **Break:** add an acquisition with a different cloud and identity system. **Explain back:** distinguish enduring contract from provisional implementation.

## Check yourself

1. How does vision differ from strategy?
2. Why label hypotheses separately from commitments?
3. What proves that a principle guides action?

## Sources

### REQUIRED

- [CNCF Technical Oversight Committee principles](https://github.com/cncf/toc)

### RECOMMENDED

- [AWS Prescriptive Guidance: Strangler fig pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html)

### DEEP DIVE

- [IETF RFC 2026: The Internet Standards Process](https://www.rfc-editor.org/rfc/rfc2026)

## Next

Continue to [RFCs, decisions, and dissent](05-rfcs-decisions-and-dissent.md).
