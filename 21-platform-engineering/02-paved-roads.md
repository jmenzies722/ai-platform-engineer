# Paved roads and capability contracts

A paved road is a supported composition of platform capabilities that makes a common safe path easier without denying legitimate alternatives.

## Why it matters

Rigid standards block unusual workloads; unlimited flexibility makes every team integrate identity, delivery, observability, and policy alone.

## How it works

Define capabilities independent of interface: deploy workload, provision database, issue identity, publish telemetry. Each contract states inputs, outputs, guarantees, limits, security defaults, ownership, support, lifecycle, and escape hatches.

Compose capabilities into versioned reference paths. Automate policy and evidence at boundaries. Make exceptions explicit, reviewed by risk, time-bounded where appropriate, and observable. A path should be removable and evolvable, not a permanent generated scaffold.

## See it yourself

A database capability might promise encrypted storage, backups, restore testing, metrics, and an owner tag. Whether invoked through API, CLI, portal, or Git is a separate design choice.

## Where it shows up

Infrastructure modules, deployment APIs, service templates, policy bundles, and managed runtime profiles.

## When it breaks

The path leaks every underlying option, hides critical limits, has no upgrade contract, or calls unsupported work an "escape hatch."

## Practice

Write a one-page contract for deploying an HTTP service. Include reliability, identity, telemetry, cost visibility, supported versions, and exception process.

## Check yourself

1. Why separate capability from interface?
2. What makes an escape hatch responsible?

## Sources

### REQUIRED
- [CNCF Platforms whitepaper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

### RECOMMENDED
- [CNCF Cloud Native Platform Engineering maturity model](https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/)

### DEEP DIVE
- [Google SRE: Service level objectives](https://sre.google/sre-book/service-level-objectives/)

## Next

[Adoption, governance, and measurement](03-adoption-and-governance.md)
