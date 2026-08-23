# Artifacts, registries, and promotion

A delivery system should build once, identify the result immutably, and promote that same artifact with its evidence through every environment.

## Why it matters

Rebuilding for production permits source, dependencies, build images, timestamps, or network inputs to change after tests passed. Mutable names such as `latest` answer what a registry points to now, not what was reviewed or deployed.

## How it works

An artifact is a deployable output such as a package, container image, archive, or machine image. A cryptographic digest identifies bytes; a tag or version is a human-facing reference that may be mutable. The build records source revision, resolved dependencies, builder identity, commands, test results, SBOM, and provenance. A registry stores artifacts, controls read and write access, enforces retention, and records immutable identity.

Promotion changes an artifact's approved status or environment reference without changing its bytes. Deployment records artifact digest plus configuration identity because configuration can alter behavior. Release then exposes a deployed version to a cohort. Attestations are signed claims about an artifact; policy decides which issuers and predicates are trusted.

Retention must preserve deployed and recoverable versions. Garbage collection needs references from environments and rollback policy, not just artifact age.

## See it yourself

Create two files with identical content and verify `sha256sum` matches; change one byte and verify the digest changes. Record a manifest containing source commit, artifact digest, test command, and configuration revision. This demonstrates content identity, not build reproducibility or signer trust.

## Where it shows up

A pull-request pipeline produces image digest `sha256:...`, test evidence, SBOM, and provenance. Staging and production deploy the digest, not a floating branch tag. The release controller changes traffic while telemetry remains associated with that digest and configuration revision.

## When it breaks

A tag moves between approval and deployment. A registry allows overwrites or anonymous pushes. Promotion copies by rebuilding. Retention deletes the last known-good artifact. An artifact is signed, but policy trusts any signer. A deployment record omits environment configuration.

Diagnose by resolving references to digests at each step, comparing bytes, inspecting registry audit events, and verifying provenance issuer and subject. Treat a digest mismatch as a new artifact requiring new evidence.

## Practice

**Observe:** choose one deployed service and trace runtime digest to registry entry, build run, source revision, test evidence, and configuration.

**Build:** define an artifact manifest and promotion policy with immutable identity, required evidence, separation of write and deploy permissions, retention, and rollback eligibility.

**Break safely:** move a test tag or alter one artifact byte in a local registry model. Completion means policy rejects promotion and the known-good artifact remains deployable.

## Check yourself

1. Why is a semantic version not sufficient artifact identity?
2. Which configuration must accompany the digest in a deployment record?
3. What does a signature prove only after trust policy is evaluated?
4. Why can age-only garbage collection break recovery?

## Sources

### REQUIRED

- [SLSA provenance](https://slsa.dev/spec/v1.0/provenance)

### RECOMMENDED

- [OCI distribution specification](https://github.com/opencontainers/distribution-spec)

### DEEP DIVE

- [in-toto specification](https://in-toto.io/)

## Next

[Software supply-chain security](05-supply-chain-security.md)
