# Platform Engineering

Platform engineering turns repeated infrastructure work into a reliable product that developers can use safely without becoming infrastructure experts.

## Why it matters

**Prerequisite:** [SRE and Observability](./14-sre-and-observability.md).

When every team assembles infrastructure and delivery independently, the organization pays repeatedly for the same decisions and inconsistent controls. A maintained internal platform can offer those capabilities through stable self-service contracts.

The platform is valuable only when it reduces user effort without hiding essential choices. Paved roads can become restrictive or sprawl into another tool layer; AI platforms face the same product problem across data, models, accelerators, and evaluation.

## How it works

A platform is an internal product: users choose a supported path that composes underlying capabilities and exposes escape hatches and evidence.

Product discovery identifies repeated jobs; platform APIs and templates encode defaults; control planes orchestrate providers; policy checks constraints; telemetry measures user outcomes and platform health.

The best interface may be API, CLI, repository template, or workflow—not necessarily a portal. Successful platforms reduce time-to-value and operating risk while keeping ownership with teams. Forced adoption can hide poor product fit.

## Vocabulary

- **Platform:** A managed set of capabilities and contracts used to build or operate products.
- **IDP:** An internal developer platform offering self-service capabilities to engineering users.
- **Self-service:** A supported operation users can complete without manual provider intervention.
- **Paved road:** A supported, opinionated path that makes common work safer and easier.
- **Golden path:** A recommended end-to-end route for a well-understood use case.
- **Cognitive load:** The mental effort required to understand and perform work.
- **Contract:** A documented promise, constraint, and ownership boundary.
- **Capability:** A useful outcome a platform enables for its users.
- **Portal:** A user interface that may expose platform capabilities but is not itself the platform.
- **Product discovery:** Learning user problems and validating which outcomes are worth building.

## See it yourself

```yaml
apiVersion: platform.example/v1
kind: ModelService
spec:
  model: fraud-v17
  latencySLO: 200ms
  scale: { min: 2, max: 20 }
  dataClass: restricted
```

Predict which decisions the platform must make from this request and which remain unspecified. A mature implementation should either return validated status with chosen runtime and policy or reject the request with an actionable condition. This supports the value of a concise self-service contract. A manifest alone does not prove that the capability exists, is operable, or fits its users.

## Where it shows up

A `ModelService` API can accept model identity, latency target, traffic policy, and data classification, then choose a supported runtime and GPU profile. Defaults reduce repeated decisions; status conditions expose provider or policy failures; an escape hatch handles workloads outside the paved road. The model team still owns behavior and business outcomes, while the platform owns the reliability of the capability it promises.

## When it breaks

Teams may bypass a platform even while its dashboard shows rising resource counts. The paved road may solve the wrong job, hide failures, impose ownership without control, or cost more than direct use. First follow one user journey and inspect support demand, lead time, abandonment, and status quality; adoption must be explained, not mandated.

## Practice

### Observe

Interview a hypothetical model team, map its deployment journey, identify repeated decisions, and choose one high-leverage capability.

### Build

Specify a versioned self-service model endpoint API with defaults, validation, cost visibility, status conditions, and escape hatch.

### Break

Change a provider API, exceed GPU quota, violate policy, and submit an old schema. Ensure contract behavior remains understandable.

### Say it out loud

Explain what makes an internal platform a product.

**Success:** Name a user job, capability contract, ownership boundary, escape hatch, and outcome that would justify continued investment.

## Check yourself

1. Why treat a platform as a product?
2. What belongs in a golden path?
3. When should an escape hatch exist?

### Interview stretch

- Design an AI platform MVP.
- Drive adoption without mandates.
- Decide whether to abstract Kubernetes.

## Sources

### REQUIRED

- “Platform Engineering Maturity Model” — CNCF Platforms Working Group. [CNCF whitepaper](https://tag-app-delivery.cncf.io/whitepapers/platforms/). Defines platform capabilities and maturity.

### RECOMMENDED

- “What is Platform Engineering?” — Martin Fowler site, Evan Bottcher. [Article](https://martinfowler.com/articles/talk-about-platforms.html). Frames platforms as products and service layers.

### DEEP DIVE

- “Team Topologies” — Skelton and Pais. [Official site](https://teamtopologies.com/key-concepts). Connects platform teams to cognitive load and interaction modes.

## Next

Continue with [./16-machine-learning.md](./16-machine-learning.md).
