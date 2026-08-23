# Secure delivery and response

Secure delivery preserves source, build, artifact, and deployment integrity while retaining evidence needed when controls fail.

## Why it matters

A trusted application built by a compromised pipeline is still compromised. Prevention alone is insufficient; responders need prepared authority, logs, and recovery paths.

## How it works

Protect branches and reviews, isolate build jobs, minimize pipeline credentials, pin dependencies, scan useful risk signals, generate SBOMs, record provenance, sign artifacts, and verify policy near deployment. Patch by exploitability and exposure, not raw vulnerability count.

Prepare incident contacts, evidence sources, containment options, clean build paths, key rotation, and communication obligations. Preserve volatile evidence before destructive remediation when safe. Revoke compromised trust, rebuild from known inputs, and verify eradication.

## See it yourself

Trace one artifact from commit to running digest. Identify who could alter source, workflow, dependency resolution, registry object, deployment policy, or runtime.

## Where it shows up

Repository rules, CI OIDC, isolated runners, registries, admission control, dependency updates, audit logs, and response playbooks.

## When it breaks

Scanners block on noisy findings, build jobs run privileged, signatures are accepted without identity policy, or containment destroys evidence and recovery credentials.

## Practice

Write a response plan for a leaked package-registry token. Include scope, revocation, artifact review, consumer notification, and proof of clean recovery.

## Check yourself

1. What does an SBOM provide, and what does it not prove?
2. Why verify signer identity and build context, not only a signature?

## Sources

### REQUIRED
- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)

### RECOMMENDED
- [OWASP Software Supply Chain Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html)

### DEEP DIVE
- [SLSA specification](https://slsa.dev/spec/v1.0/)

## Next

[Platform Engineering](../21-platform-engineering/README.md)
