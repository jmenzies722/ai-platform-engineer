# Continuous integration and delivery

Continuous integration keeps the main line healthy; continuous delivery keeps every accepted change in a releasable state.

## Why it matters

Large, long-lived branches accumulate merge uncertainty. Manual builds produce artifacts that cannot be reproduced or trusted. Infrequent releases combine many independent risks into one event.

## How it works

Integrate small changes frequently. A pipeline checks formatting, tests behavior, scans dependencies, builds one immutable artifact, records provenance, and promotes that same artifact through environments. Fast deterministic checks run first; slower integration and end-to-end checks follow.

Deployment installs a version. Release exposes it to users, perhaps through a feature flag or traffic policy. Keeping these decisions separate enables gradual exposure without rebuilding. Environment-specific configuration belongs outside the artifact, but configuration must still be versioned, validated, and observable.

CI requires developers to integrate to a shared main line frequently and repair failures immediately. A merge queue can retest the exact combined revision when main changes quickly. Test selection should reflect risk: deterministic unit and contract tests provide fast isolation; integration tests prove important boundaries; end-to-end tests cover a few critical user paths. Flaky tests need ownership, quarantine with expiry, and repair rather than habitual reruns.

Pipeline jobs form trust boundaries. Untrusted pull-request code receives no production secret or publish authority. Build and deployment identities are short-lived and scoped to repository, workflow, environment, and action. Cache keys, build images, actions, dependencies, and runner persistence are inputs requiring integrity controls.

## See it yourself

Given commit `a1b2c3`, identify one artifact digest, dependency resolution, builder, tests, SBOM, and provenance attached to it. Follow the digest through staging to production and include configuration revision. If production rebuilds from source, it is not deploying the tested artifact. Predict which checks should fail after changing only pipeline policy.

## Where it shows up

Trunk-based development, merge queues, pull-request checks, artifact registries, deployment automation, feature flags, and progressive delivery serve the same short feedback loop. A production record connects change intent, reviewed source, immutable artifact, environment configuration, release cohort, user telemetry, and recovery action.

## When it breaks

Flaky tests teach people to ignore red builds. Slow gates increase batch size. Mutable tags hide what ran. Environment-specific builds drift. A pipeline with one shared administrator credential makes every repository a production trust boundary. Concurrent deployments race, canceled jobs leave locks, and a green pipeline can still verify the wrong behavior.

Preserve stage inputs, outputs, runner identity, timings, logs, artifact digest, and deployment state. Retry only after classifying infrastructure flake versus deterministic product failure; otherwise reruns erase the failure rate.

## Practice

**Observe:** trace one deployed version back through digest, build, tests, source, dependency lock, and reviewed change. Mark every mutable reference.

**Build:** design CI and CD stages for an HTTP service. For each state input, immutable output, failure evidence, credentials, timeout, concurrency, and owner; include post-deployment user verification.

**Break safely:** introduce a deterministic failing test, moved tag, and concurrent deployment in a sandbox model. Completion means failures stop before unsafe mutation, the tested artifact is promoted unchanged, and the last known-good version remains recoverable.

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
