# Facilitator solution: Stale Evaluation Promotion and Artifact Digest Drift

This is an evidence-supported resolution for the supplied scenario, not a
substitute for verifying artifact and policy identities.

## Diagnosis

Evaluation `eval-442` validly passed digest `sha256:3ab`. Build automation later
moved mutable tag `support-model:2026-08-23` to digest `sha256:9c4`. Deployment
resolved the tag after that mutation. The promotion policy detected the subject
digest mismatch but broad exception `exc-17` changed enforcement to advisory,
so the unevaluated digest was allowed into production.

The stale evaluation was not a stale test result for `3ab`; it was a valid
result attached through a mutable name to a different artifact. Digest `9c4`
also shows real safety and quality regressions in the new cohort.

## Evidence-led reasoning

1. The signed evaluation subject is `3ab`; production and release `rel-881`
   report `9c4`. Parent checkpoint equality does not make artifacts identical.
2. The registry audit places retagging between evaluation and policy
   evaluation.
3. The policy log explicitly records
   `evaluation.subject_digest_matches=false`. This rules out a UI-only display
   defect.
4. `enforcement=advisory` and a repository-wide exception explain why a failed
   mandatory invariant still produced `allow`.
5. Safety and regulated-language metrics regress on the new cohort while server
   errors stay healthy, favoring artifact behavior over infrastructure failure.

## Discriminating investigation

| Test | Expected result | What it establishes |
|---|---|---|
| Verify attestation signature and subject | Valid signature for `3ab` only | Report integrity, not applicability to `9c4` |
| Resolve release tag using registry audit time | `3ab` before 06:31 and `9c4` afterward | Mutable reference race |
| Replay policy without `exc-17` | Promotion denies on subject mismatch | Exception enabled fail-open |
| Route a small cohort to pinned `3ab` | Safety slices recover | `9c4` is causal |
| Compare artifact manifests | Tokenizer or packaging differs | Rebuild changed evaluated subject |

If pinned `3ab` also fails under the same traffic and configuration, investigate
data drift or online evaluation validity before declaring full recovery.

## Decision analysis

Continuing rollout while evaluating `9c4` exposes more users without an approved
artifact. Rerunning evaluation can determine whether `9c4` is promotable later,
but cannot retroactively make the original decision compliant. Rolling back to
the same mutable tag may redeploy `9c4`.

The bounded choice is to freeze expansion and tag writes, then route to the
last known-good digest `3ab` with safety and operational guardrails. Promotion
must fail closed whenever artifact identity cannot be proven.

## Mitigation sequence

1. Freeze rollout, registry tag mutation, and release-policy changes. Preserve
   registry audit records, manifests, attestations, policy input and output,
   exception state, deployment resolution, and serving digest telemetry.
2. Confirm that `3ab` is the prior approved and operationally healthy digest.
   Pin a small affected cohort directly to `3ab`.
3. Compare safety refusal, regulated slice, latency, and error metrics against
   both the `9c4` cohort and existing `3ab` control.
4. Expand rollback by immutable digest when causal and operational signals
   recover. Stop if service-health guardrails breach, but do not route traffic
   back to unevaluated `9c4`.
5. Revoke `exc-17` for model releases and make subject mismatch a non-bypassable
   deny until a narrowly scoped exception mechanism is reviewed.
6. Inventory online, batch, cache, and regional consumers that resolved the
   mutable tag. Verify each running digest.
7. Evaluate `9c4` later as a new release with a new attestation and normal
   approval flow. Keep its result separate from incident recovery evidence.

## Recovery proof

- Serving telemetry and independent manifest inspection agree on pinned `3ab`
  for every restored target.
- Safety refusal and regulated-language metrics remain above thresholds over
  `<representative evaluation window>`.
- Operational SLOs remain healthy and cohort comparisons are statistically and
  practically meaningful.
- A reconciliation query finds no deployed digest without matching approved
  attestations for artifact, suite, data, and policy identities.
- Subject mismatch produces a deny in policy replay and a controlled
  production-like promotion test.
- Mutable release-tag writes are blocked and rollback instructions require
  digests.

## Prevention plan

| Control | Acceptance evidence |
|---|---|
| Immutable release identity | Promotion and deployment APIs reject tag-only model references |
| Complete signed attestation | Verified subjects bind model, tokenizer, configuration, suite, data snapshot, and policy bundle digests |
| Non-bypassable identity invariant | Missing, invalid, or mismatched subject always denies |
| Exception governance | Exceptions require rule, repository, digest, owner, approval, and short expiry; broad wildcards reject |
| Registry immutability | Release tags cannot move; rebuilding produces a new version and digest |
| Runtime reconciliation | Alert fires when running digest lacks a matching active approval |
| Independent cohort gate | Safety and regulated slices halt expansion before the next rollout stage |

## Debrief guide

- A cryptographically valid attestation is irrelevant when its subject is not
  the deployed subject.
- “Packaging-only” is a claim requiring a policy and evidence; any changed
  digest is a new artifact identity.
- Derived green dashboards must expose the exact joined identities and failed
  policy rules.
- Policy errors and absent evidence must have explicit fail-closed semantics for
  high-impact promotion.
- Recovery, retrospective evaluation, and future eligibility are three
  separate decisions.

## Authoritative sources

- [SLSA specification, Provenance](https://slsa.dev/spec/v1.0/provenance)
- [in-toto Attestation Framework](https://github.com/in-toto/attestation/blob/main/spec/README.md)
- [NIST AI RMF Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
