# RFCs, decisions, and dissent

Decision artifacts preserve context, evidence, accountability, and legitimate dissent so an organization can act without erasing uncertainty.

## Why it matters

Important choices become folklore when their alternatives, assumptions, and authority are absent; repeated debate then consumes trust and time.

## How it works

An RFC states context, problem, goals, non-goals, constraints, options, evidence, recommendation, consequences, risks, migration, operations, security, and unresolved questions. It names the decision owner and consultation model. Reviewers classify feedback as correctness, evidence, risk, or preference.

Use an architecture decision record for a concise accepted choice and its consequences. Link rather than duplicate evidence. Set a review window and decision date. Pre-read with groups that carry unusual burden, but keep material tradeoffs visible to all affected parties.

Consensus is not always required. Preserve principled dissent, identify the value or evidence behind it, and record why the accountable owner chose otherwise. Reopen a decision only when a stated trigger occurs, evidence changes materially, or a hidden affected party emerges. Status alone is not evidence.

## See it yourself

Two teams dispute one provider versus many. Cost measurements favor one; resilience and bargaining power favor portability. The RFC quantifies switching cost, names the business preference, and records an exit trigger. The final choice is legible even though no formula eliminates the value judgment.

## Where it shows up

RFCs are useful for public APIs, shared platforms, data authority, migrations, security controls, and standards. Lightweight records are better for reversible local choices.

## When it breaks

Artifacts fail as retrospective justification, endless comment threads, silent approval, or a vote among people with unequal consequences. When review stalls, list unresolved claims, evidence, values, and decision authority.

## Practice

**Build:** write an RFC choosing an AI-provider integration model with alternatives, cost, reliability, security, migration, decision owner, dissent, and revisit triggers. **Break:** reveal a contractual exit restriction after approval. **Explain back:** decide whether the trigger reopens the choice and preserve the prior reasoning.

## Check yourself

1. Which feedback is a blocker versus a preference?
2. Why preserve dissent after a decision?
3. What legitimately reopens an accepted decision?

## Sources

### REQUIRED

- [Architecture Decision Records](https://adr.github.io/)

### RECOMMENDED

- [Google Engineering Practices: Code review](https://google.github.io/eng-practices/review/)

### DEEP DIVE

- [IETF RFC 7282: On Consensus and Humming](https://www.rfc-editor.org/rfc/rfc7282)

## Next

Continue to [Influence without command](06-influence-without-command.md).
