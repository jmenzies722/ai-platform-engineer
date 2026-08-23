# Continuous integration and delivery

Continuous integration keeps the main line healthy; continuous delivery keeps every accepted change in a releasable state.

## Why it matters

Large, long-lived branches accumulate merge uncertainty. Manual builds produce artifacts that cannot be reproduced or trusted. Infrequent releases combine many independent risks into one event.

## How it works

Integrate small changes frequently. A pipeline checks formatting, tests behavior, scans dependencies, builds one immutable artifact, records provenance, and promotes that same artifact through environments. Fast deterministic checks run first; slower integration and end-to-end checks follow.

Deployment installs a version. Release exposes it to users, perhaps through a feature flag or traffic policy. Keeping these decisions separate enables gradual exposure without rebuilding. Environment-specific configuration belongs outside the artifact, but configuration must still be versioned, validated, and observable.

## See it yourself

Given commit `a1b2c3`, identify one artifact digest and the test evidence attached to it. If production rebuilds from source, it is not deploying the tested artifact.

## Where it shows up

Trunk-based development, pull-request checks, artifact registries, deployment automation, feature flags, and progressive delivery all serve the same short feedback loop.

## When it breaks

Flaky tests teach people to ignore red builds. Mutable tags hide what ran. Environment-specific builds drift. A pipeline with one shared administrator credential makes every repository a production trust boundary.

## Practice

Design stages for a small HTTP service. For each stage state its input, output, failure evidence, credentials, and maximum useful duration.

## Check yourself

1. Why promote an artifact instead of rebuilding it?
2. How can a change be deployed but not released?

## Sources

### REQUIRED
- [DORA: Continuous delivery](https://dora.dev/capabilities/continuous-delivery/)

### RECOMMENDED
- [SLSA build track](https://slsa.dev/spec/v1.0/levels)

### DEEP DIVE
- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)

## Next

[Safe changes and recovery](03-safe-change.md)
