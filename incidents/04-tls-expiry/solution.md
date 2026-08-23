# Facilitator solution: TLS Certificate Expiry

This is one evidence-supported resolution path, not permission to skip investigation. Read the learner’s timeline and hypotheses before revealing it.

## Diagnosis

Automation renewed the leaf certificate but failed to deploy it to the production edge target, which continued serving the expired certificate.

## Reasoning from evidence

1. The client explicitly reports expiry and the lifetime metric is negative, while TCP succeeds; this localizes failure above transport.
2. The HTTP probe bypasses TLS and therefore cannot contradict the certificate failure.
3. Renewal success does not prove deployment. The renewer warning and served serial test establish the broken handoff.
4. Different connection reuse explains staggered impact because existing TLS sessions do not require a new full handshake immediately.

No single symptom is enough. The diagnosis requires the observations above to agree and plausible alternatives to be tested.

## Discriminating investigation

| Test | Expected observation | What it establishes |
|---|---|---|
| Inspect served chain with correct SNI | Expired leaf serial on edge | Actual served artifact |
| Compare issuance inventory | New valid serial exists | Issuance succeeded |
| Query every edge shard | Old serial remains on production target | Deployment failed |

Stop if a result differs. Update the hypothesis rather than forcing this solution.

## Decision analysis

The first priority is user and data safety, followed by preserving enough evidence to distinguish recurrence from a new failure. Avoid broad restarts, unbounded capacity increases, disabled verification, or destructive cleanup: each can conceal the mechanism or enlarge the blast radius.

The preferred response is: Deploy the already-issued certificate and full intended chain through the controlled edge configuration, canary one shard, then roll out. If deployment is unsafe, route to an endpoint serving a valid chain.

## Mitigation sequence

1. Declare scope, owner, and a measurable rollback trigger.
2. Capture the smallest decisive evidence set, including timestamps and version or resource identity.
3. Stop new work that amplifies impact while preserving durable work.
4. Apply the reversible mitigation to a canary or narrow cohort.
5. Compare canary and control signals, then expand only if the expected causal signal changes.

## Recovery proof

- Fresh handshakes succeed with correct SNI from representative networks
- Served serial and `notAfter` match the approved certificate on every shard
- Handshake failures and user transactions return to baseline

Continue monitoring for a full relevant workload cycle. Remove temporary controls only with the same evidence standard.

## Prevention plan

- Alert on externally served certificate lifetime, not only issuance
- Exercise renewal deployment and rollback
- Inventory SNI names and edge targets
- Use synthetic checks that validate chain and hostname

“Be more careful” is not an action. Convert each item into a tested control with an owner and objective completion evidence.

## Debrief guide

- Strong investigations separate the immediate failure mechanism from the condition that triggered it.
- Strong mitigations reduce offered harm without converting a transient incident into hidden permanent risk.
- Strong recovery checks include a user-visible signal, a subsystem signal, and evidence that temporary changes were removed.
- Ask which observation would falsify this diagnosis. If the team cannot name one, it is telling a story rather than testing a hypothesis.

## Authoritative sources

- [RFC 5280: PKIX certificate profile](https://www.rfc-editor.org/rfc/rfc5280)
- [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446)
- [OWASP TLS cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)
