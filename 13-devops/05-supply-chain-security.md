# Software supply-chain security

Supply-chain security protects the path from developer intent through dependencies, build systems, registries, deployment credentials, and the artifact running in production.

## Why it matters

A reviewed application can still ship compromised dependencies or be replaced by an attacker controlling CI. Pipeline code executes untrusted repository input near credentials, making the delivery system itself a production attack surface.

## How it works

Threat-model source control, dependency resolution, builders, artifact storage, and deployment separately. Protect branches and reviews, pin dependencies with integrity metadata, isolate ephemeral builders, minimize network access, generate an SBOM, emit provenance, sign attestations with protected workload identity, and verify policy before deployment.

Least privilege is contextual. Pull-request jobs from untrusted forks should not receive secrets or production write access. Deployment jobs should use short-lived federated identity bound to repository, workflow, branch or environment, and intended audience. Separate artifact publication from deployment authority so compromise of one step does not silently control every environment.

Vulnerability scans find known issues but do not establish provenance, exploitability, absence of malware, or safe configuration. Exceptions need owner, rationale, scope, expiration, compensating controls, and evidence of removal.

## See it yourself

Inspect a dependency lock file and one CI workflow. Predict which external code executes, which action versions can move, what credentials are available, and which outputs become trusted. Pin a harmless action or package to an immutable revision in a sandbox and record its integrity value. This narrows input identity; it does not prove the input is benign.

## Where it shows up

A protected workflow builds in an ephemeral runner, obtains an identity token, publishes an image, and signs provenance. A separate deployment controller verifies trusted builder identity, source repository, commit, and required tests before admitting the digest. Production credentials never enter a pull-request job.

## When it breaks

Actions are referenced by floating tags. Cache poisoning crosses trust boundaries. Build logs expose secrets. Self-hosted runners retain workspace or credentials. A compromised maintainer releases a validly signed malicious package. Teams suppress scanner findings indefinitely.

Preserve workflow revision, runner identity, token claims, dependency resolution, registry events, and deployed digest during investigation. Rotate affected credentials and revoke trust roots deliberately; deleting only the visible artifact leaves the path compromised.

## Practice

**Observe:** map trust boundaries for one pipeline, including repository events, third-party code, caches, credentials, artifacts, and environment approvals.

**Build:** write a policy requiring immutable dependencies, ephemeral isolation, minimal federated claims, provenance, SBOM, and admission verification.

**Break safely:** model an untrusted pull request that changes pipeline code and attempts to print a fake secret. Completion means the job has no sensitive credential, cannot publish a trusted artifact, and leaves auditable denial evidence.

## Check yourself

1. Why does a clean vulnerability scan not prove supply-chain integrity?
2. Which claims should bind a short-lived deployment credential?
3. How does separating publication from deployment reduce blast radius?
4. What makes an exception governable instead of permanent?

## Sources

### REQUIRED

- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)

### RECOMMENDED

- [SLSA specification](https://slsa.dev/spec/v1.0/)

### DEEP DIVE

- [CNCF Software Supply Chain Security paper](https://github.com/cncf/tag-security/blob/main/supply-chain-security/supply-chain-security-paper/CNCF_SSCP_v1.pdf)

## Next

[Delivery governance and production learning](06-governance-and-learning.md)
