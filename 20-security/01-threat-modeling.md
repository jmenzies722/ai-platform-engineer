# Threat modeling and trust boundaries

Threat modeling asks what must be protected, from whom, across which boundaries, and what design changes reduce credible harm.

## Why it matters

Generic checklists miss system-specific abuse. A simple model exposes assumptions early, when changing architecture is cheaper.

## How it works

Define scope, assets, actors, data flows, entry points, trust boundaries, and dependencies. Enumerate abuse cases using prompts such as STRIDE, then rank them by plausible impact and likelihood. Choose mitigations that prevent, detect, limit, or support recovery; record accepted risk and owner.

Model machine identities, CI, administrators, vendors, and control planes, not only internet users. Revisit the model when data, boundaries, or capabilities change.

## See it yourself

For file upload, trace bytes through edge, scanner, object store, worker, and download. Ask where content becomes trusted and what happens if scanning times out.

## Where it shows up

Architecture reviews, sensitive feature design, cloud boundaries, supply chains, and incident preparation.

## When it breaks

Teams list threats without decisions, assume internal networks are trusted, ignore compromised dependencies, or score risk with fake precision.

## Practice

Create a one-page model for password reset: assets, actors, flows, five abuse cases, controls, residual risk, and evidence.

## Check yourself

1. What makes a trust boundary meaningful?
2. Why include detection and recovery controls?

## Sources

### REQUIRED
- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)

### RECOMMENDED
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)

### DEEP DIVE
- [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon/)

## Next

[Identity, authorization, and secrets](02-identity-and-secrets.md)
