# 05 — Verifiable Software Delivery Pipeline

Build a pipeline in a separate repository that can answer who built an artifact, from which inputs, under which policy, and how it reached an environment.

## Problem and users

Developers need fast releases, operators need predictable promotion and rollback, and security reviewers need tamper-evident provenance. A green CI check alone does not prove that the tested bytes are the deployed bytes. The project must make artifact identity and authorization continuous from source to runtime.

## Constraints and policy

- Use one small reference service and promote the same immutable OCI artifact through test and staging.
- Run builds with ephemeral credentials and isolated, least-privilege workers.
- Require review for protected source and explicit approval only where risk justifies it.
- Exclude production deployment, a custom CI engine, and security claims based only on scanner output.

## Architecture expectations

Model source, build worker, artifact registry, policy evaluator, environments, and evidence store as separate trust domains. Produce an SBOM and signed provenance tied to digest; verify before promotion and admission. Define branch, dependency, vulnerability, secret, license, and rollback policies with exception expiry. Prevent untrusted pull-request code from accessing release credentials.

## Milestone plan

1. Threat-model source-to-runtime paths and define artifact/evidence schemas.
2. Build, test, scan, generate SBOM/provenance, sign, and publish by digest.
3. Add policy gates, environment promotion, deployment verification, and rollback.
4. Run compromise drills, measure lead time and false positives, and document ownership.

## Required artifacts

- Trust-boundary diagram, pipeline contract, policy repository, and ADRs.
- SBOM, provenance statement, signature-verification transcript, and release manifest.
- Deployment/rollback runbooks, exception register, and key-rotation procedure.
- Delivery metrics report covering queue time, build duration, failure rate, and recovery.

## Tests and failure drills

Test pipeline definitions, policy rules, action pinning, artifact immutability, and environment authorization. Attempt dependency confusion, modified artifacts, forged provenance, leaked test token, poisoned cache, untrusted fork release, expired signing identity, admission of an unsigned image, and rollback after a bad migration simulation. Capture what blocked each path and any residual exposure.

## Observability, security, and cost

Track build identity, digest, policy decisions, approvals, deployment status, verification failures, queue saturation, and credential use in an append-only audit trail. Minimize token scope and lifetime, pin external actions, isolate caches, and document signer trust/rotation. Report runner minutes, storage, scanning, registry egress, and cost per successful release; set retention tiers for bulky evidence.

## Explicit success rubric

| Claim | Proof required |
|---|---|
| Artifact continuity | Deployed digest matches tested, scanned, signed, and approved digest. |
| Compromise resistance | All defined adversarial drills are blocked or explicitly accepted with bounded residual risk. |
| Recoverability | A failed promotion is detected and rolled back through the documented path. |
| Developer usability | Median pipeline time meets the declared budget and failures explain an actionable remedy. |
| Auditability | A reviewer reconstructs a release without privileged CI access. |

## Stretch work

Reach a documented SLSA build level, add reproducible-build comparison, or distribute verification metadata through a transparency log.

## Authoritative sources

- [SLSA specification](https://slsa.dev/spec/)
- [in-toto specification](https://in-toto.io/)
- [Sigstore documentation](https://docs.sigstore.dev/)
- [SPDX specification](https://spdx.dev/specifications/)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/Projects/ssdf)

## Mapped modules

[05 Git](../../05-git/README.md), [13 DevOps](../../13-devops/README.md), [15 Containers](../../15-containers/README.md), [16 Kubernetes](../../16-kubernetes/README.md), and [20 Security](../../20-security/README.md).
