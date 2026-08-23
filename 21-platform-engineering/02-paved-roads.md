# Paved roads and capability contracts

A paved road is a supported composition of versioned capabilities that makes a common safe path easier than assembling it independently. Its contracts make guarantees, limits, responsibilities, and escape routes testable.

## Why it matters

Rigid standards block legitimate workloads, while unlimited choice makes every team rediscover identity, delivery, telemetry, recovery, and policy. A contract lets the platform simplify implementation without concealing the obligations that cross its boundary.

## How it works

Define capabilities independently of interface: run a workload, issue identity, provision storage, publish telemetry, or restore data. For each, specify accepted intent, outputs, invariants, quotas, SLOs, security defaults, data handling, cost attribution, ownership, support, versions, and deletion semantics. State consumer responsibilities with equal precision.

A paved road composes contracts into a reference journey. A service path might combine repository controls, build provenance, workload identity, deployment, logs, metrics, rollback, and ownership metadata. API, CLI, portal, and Git interfaces may expose the same contract; interface parity prevents one channel from bypassing policy or returning weaker status.

Use defaults for choices most consumers should not make. Expose advanced controls when they remain inside the support envelope. An escape hatch is an explicit route outside the paved road with a named owner, residual obligations, evidence, support boundary, and re-entry path. Unsupported abandonment is not an escape hatch.

Version contracts according to compatibility rather than implementation releases. Publish how deprecation is announced, how long versions overlap, who performs migrations, and what happens to existing workloads. Contract tests should verify both successful behavior and stable failure semantics.

## Vocabulary

- **capability:** a useful outcome exposed independently of a particular interface
- **contract:** testable promises and responsibilities between provider and consumer
- **paved road:** supported composition of capabilities for a recurring journey
- **escape hatch:** governed path for needs outside the standard support envelope

## See it yourself

Given this promise, identify what is missing:

```text
Create a production PostgreSQL database in under 30 minutes.
Backups are enabled. Encryption is enabled. Contact #platform for help.
```

The statement lacks availability scope, restore objective and evidence, supported regions and versions, quota, tenant isolation, cost attribution, deletion behavior, consumer duties, and error semantics. Predicting “database ready” from this text is impossible. A useful contract turns each relevant claim into an observable API field, metric, test, or documented responsibility.

## Where it shows up

A managed runtime can promise workload identity and telemetry while requiring the application to expose a health endpoint and respect termination signals. If a deployment fails because the health endpoint returns 500, status should identify the violated consumer responsibility rather than report generic platform failure.

## When it breaks

Leaky paths expose provider knobs until users need provider expertise. Opaque paths report “provisioning failed” without the violated contract. Drift appears when portal, CLI, and Git invoke different policies. Measure repeated overrides, version skew, support tickets by contract clause, and escape-hatch age to locate these failures.

Overpromising is also dangerous. A platform that advertises “automatic rollback” but cannot define its trigger or data-safety limits causes false confidence. Narrow the guarantee and expose evidence rather than relying on reassuring labels.

## Practice

**Observe:** choose one existing shared capability and trace its promise across docs, API schema, runtime status, and support policy. Record contradictions. Completion means every claimed guarantee has evidence or is marked unverified.

**Design:** write a contract for deploying an HTTP service. Include inputs, outputs, provider and consumer duties, reliability, identity, telemetry, costs, quotas, versions, deletion, errors, and one escape hatch.

**Break:** submit three cases: missing ownership, quota exhaustion, and unsupported region. Design distinct machine-readable and human-readable failure responses, then show how each user recovers.

**Say it out loud:** explain why a template is not itself a capability contract.

## Check yourself

1. Why must capability meaning remain stable across portal and API interfaces?
2. What turns an escape hatch into a governed engineering choice?
3. Which contract promises require runtime evidence rather than documentation?
4. How can a platform evolve a paved road without regenerating application code?

## Sources

### REQUIRED

- [CNCF Platforms whitepaper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

### RECOMMENDED

- [CNCF Cloud Native Platform Engineering maturity model](https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/)

### DEEP DIVE

- [Google SRE: Service level objectives](https://sre.google/sre-book/service-level-objectives/)

## Next

Continue to [Adoption, governance, and measurement foundations](03-adoption-and-governance.md).
