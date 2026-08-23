# Software supply chain and container security

A secure artifact is traceable to reviewed source, controlled inputs, an isolated build, and verifiable provenance. Scanning is useful evidence, but provenance and deployment policy control what is allowed to run.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Pin dependencies and base images by immutable identity, review lockfile changes, isolate builds, minimize credentials, generate an SBOM, sign attestations, and verify policy at admission. SLSA describes increasing provenance guarantees; reproducibility can independently check outputs.

Containers share the host kernel. Run as non-root, drop capabilities, use read-only filesystems, constrain syscalls, set resources, avoid host namespaces, and patch base images. Separate build stages so compilers and credentials do not enter runtime artifacts.

## See it yourself

A package checksum proves bytes match the selected package; it does not prove the package is benign or that selection was authorized. Provenance adds who built what from which inputs, while review and policy address whether those inputs should be trusted.

## Where it shows up

CI identities and artifact registries are production control planes. Protect branch rules, workflow changes, runners, signing authority, and promotion. Deploy the same digest tested rather than rebuilding per environment.

## When it breaks

Mutable tags drift, dependency confusion selects attacker packages, build logs leak tokens, privileged containers escape intended isolation, and scanners miss unknown flaws. Verify digest, provenance, signer identity, policy decision, runtime controls, and observed process behavior.

## Practice

Build a minimal container if a local engine exists, produce an SBOM, and inspect user, capabilities, and filesystem. Otherwise inspect a supplied manifest. Break it by using a mutable tag and root user. Completion means policy rejects both and accepts a pinned, non-root artifact.

## Check yourself

1. What does an SBOM prove and not prove?
2. Why is a digest stronger than a tag?
3. How does build provenance differ from vulnerability scanning?
4. Which kernel boundary do containers share?

## Sources

### REQUIRED

- [SLSA specification](https://slsa.dev/spec/)

### RECOMMENDED

- [NIST SP 800-190](https://csrc.nist.gov/pubs/sp/800/190/final)

### DEEP DIVE

- [OCI Image Specification](https://github.com/opencontainers/image-spec)

## Next

[Cloud and application security](06-cloud-and-application-security.md)
