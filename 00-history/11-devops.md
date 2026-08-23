# DevOps

DevOps shortens the path from code change to production learning by joining delivery and operational responsibility.

## Why it matters

**Prerequisite:** [Virtualization and Cloud](./10-virtualization-and-cloud.md).

Separate development and operations queues made releases large, slow, and difficult to diagnose. The incentives were also misaligned: one group was rewarded for change while another absorbed its risk.

Shared ownership, continuous integration, automated delivery, and infrastructure as code shortened the feedback loop. The resulting toolchains can themselves become a burden, which is why platform teams now package safe delivery paths as maintained products.

## How it works

Delivery is a sociotechnical feedback loop: code, evidence, deployment, production learning, and improved design.

Versioned changes trigger repeatable build and test stages; immutable artifacts move through policy gates; progressive deployment limits exposure; telemetry informs rollback and future work.

Deployment frequency and stability are not inherent opposites: small batches reduce change risk and diagnosis scope. Automation without operability merely accelerates bad states; organizational boundaries shape architecture and queues.

## Vocabulary

- **CI:** Continuous integration of small changes with automated verification.
- **Continuous delivery:** Keeping software releasable through an automated, controlled delivery path.
- **Deployment:** Installing and activating a software version in an environment.
- **Lead time:** Time from a change beginning to producing value in production.
- **Change failure rate:** Proportion of changes that cause degraded service or remediation.
- **MTTR:** Mean time to restore service after failure.
- **IaC:** Infrastructure as code: versioned, reviewable definitions of infrastructure state.
- **Canary:** A limited rollout used to evaluate a change before broad exposure.
- **Immutable artifact:** A built output promoted unchanged across environments.
- **Feedback loop:** A cycle in which observed outcomes inform the next action.

## See it yourself

```yaml
pipeline:
  - build: reproducible-artifact
  - test: unit-integration-security
  - deploy: canary-5-percent
  - verify: slo-and-business-signals
  - promote_or_rollback: automatic
```

For each stage, predict the durable artifact or decision it must produce. A coherent run should promote one immutable bundle only after its tests and canary signals pass; a failed signal should select rollback. This supports delivery as a feedback-controlled release process. YAML alone does not prove reproducibility, trustworthy tests, or a working rollback.

## Where it shows up

A model release joins code, weights, tokenizer, runtime, configuration, and evaluation evidence into one promotable identity. Building that bundle once and moving it unchanged through environments limits drift. A small canary then supplies production evidence before broad exposure, and rollback names the previous complete bundle rather than reconstructing files by hand. Fast delivery comes from reducing uncertainty and batch size, not omitting controls.

## When it breaks

A green pipeline can still release a broken service. Tests may be flaky or incomplete, artifacts mutable, environments drifted, secrets mishandled, or rollback untested. First verify the deployed digest and trace its evidence, rollout events, and user-facing signals; job success is not the same as a successful change.

## Practice

### Observe

Map one change from commit to production and identify every handoff, wait, mutation, and missing feedback signal.

### Build

Design a pipeline that signs an immutable model-serving bundle, evaluates it, canaries it, and automatically rolls back on an SLO breach.

### Break

Introduce a flaky test, mutable tag, leaked secret, and broken rollback. Add controls that expose each failure.

### Say it out loud

Explain how faster delivery can also be safer.

**Success:** Connect small batches, immutable artifacts, progressive exposure, user signals, and tested rollback in one coherent release account.

## Check yourself

1. Why can speed improve stability?
2. What makes an artifact promotable?
3. Why is DevOps sociotechnical?

### Interview stretch

- Improve a slow, unreliable release process.
- Which delivery metrics can be gamed?
- Design rollback for model and schema changes.

## Sources

### REQUIRED

- “Accelerate” research program — DORA/Google Cloud. [Official DORA research](https://dora.dev/research/). Provides evidence linking delivery capabilities and outcomes.

### RECOMMENDED

- “Continuous Delivery” — Jez Humble and David Farley. [Official book site](https://continuousdelivery.com/). Defines deployment-pipeline principles.

### DEEP DIVE

- “DevOps: A Software Architect’s Perspective” — Bass, Weber, and Zhu. [SEI page](https://www.sei.cmu.edu/library/devops-a-software-architects-perspective/). Connects architecture and operational collaboration.

## Next

Continue with [./12-containers.md](./12-containers.md).
