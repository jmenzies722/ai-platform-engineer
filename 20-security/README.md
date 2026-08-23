# 20 — Security

Security engineering makes trust, authority, cryptographic assumptions, and response paths explicit so compromise is prevented where possible and contained when prevention fails.

## What you will learn

- Threat-model assets, actors, flows, and trust boundaries.
- Design identity, authorization, cryptography, TLS, and secret lifecycles.
- Harden software supply chains, containers, cloud, and applications.
- Prepare detection, containment, eradication, and recovery with usable evidence.

## Lessons

1. [Threat modeling and trust boundaries](01-threat-modeling.md)
2. [Identity, authentication, and authorization](02-identity-and-access.md)
3. [Cryptography, key management, and TLS](03-cryptography-and-tls.md)
4. [Secrets and credential lifecycles](04-secrets-management.md)
5. [Software supply chain and container security](05-supply-chain-and-containers.md)
6. [Cloud and application security](06-cloud-and-application-security.md)
7. [Security detection and incident response](07-security-incident-response.md)

## Practice

Complete [test identity and application boundaries](lab-security-boundaries.md). Keep the prediction, baseline, injected failure, diagnostic evidence, correction, and production decision as an operator's record.

## Ready to continue

You can explain the guarantees and limits in this module, calculate the small bounds that govern production behavior, design a controlled failure, diagnose it from evidence, and operate the mechanism with explicit ownership and recovery.

## Next

Continue to [Platform Engineering](../21-platform-engineering/README.md).
