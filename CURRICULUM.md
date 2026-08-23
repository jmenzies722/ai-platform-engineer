# Curriculum

The curriculum follows the dependencies of an AI platform. Hardware and software execution come first; distributed infrastructure and platform control follow; AI workloads sit on those foundations. Use [ROADMAP.md](ROADMAP.md) to decide how much evidence you need before moving on.

A module README is a map, not a lesson. Each chapter contains an ordered lesson sequence, practical evidence, failure work, and primary sources. A learner should leave with a mechanism they can explain and evidence they can inspect. If a chapter cannot support that claim, it remains a curriculum gap rather than completed learning material.

## Chapter contract

Every major technology is treated as an engineering system, not a vocabulary list. Its chapter should establish:

- why the system exists and which constraints shaped it;
- what contract users and neighboring systems rely on;
- how the mechanism, state, and critical paths work;
- which internals explain correctness, performance, security, or cost;
- how to build a reduced version or exercise the real interface;
- how it fails, which symptoms are ambiguous, and how to debug it;
- how to operate, secure, scale, recover, and evolve it;
- how to compare designs under stated requirements.

Lessons use **See it yourself** for bounded proofs. Module labs combine mechanisms. [Incident drills](incidents/README.md) withhold the diagnosis. [Projects](projects/README.md) require integration and sustained engineering judgment.

## Composition layer

The numbered modules below are the canonical curriculum. [Role tracks](tracks/README.md) compose those modules, labs, incidents, and projects for a target outcome; they do not fork lesson content or lower prerequisites. [Competency gates](assessments/README.md) assess the resulting evidence across Explain, Build, Debug, Operate, and Design. [Certification overlays](certs/README.md) map an external blueprint onto the same modules and evidence and are not separate courses.

Choose a track when role focus is useful, but enter it at the earliest unmet gate rather than restarting automatically. Use [case studies](case-studies/README.md) to practice decisions from incomplete evidence between guided work and independent projects.

## Evidence graph

The experiences form an evidence graph, not four independent inventories. Follow a module README's Practice sequence: establish a model in lessons, produce a bounded proof in a lab, diagnose a related incident without its solution, and integrate the corrected design in a project. Carry artifacts forward rather than repeating claims. A later artifact should name which earlier evidence it accepts, rejects, or supersedes.

Four cross-module paths are explicit:

- Platform product and control: [Platform Engineering](21-platform-engineering/README.md), the [adoption experiment](21-platform-engineering/lab-platform-adoption-experiment.md), [Developer Platforms](22-developer-platforms/README.md), [Control Planes](23-control-planes/README.md), the [control-plane lab](labs/14-platform-control-plane/README.md), the [retry storm](incidents/08-retry-storm/README.md) and [queue overload](incidents/12-queue-overload/README.md) incidents, then [project 09](projects/09-developer-platform-control-plane/README.md).
- Reproducible model release: [MLOps](28-mlops/README.md), the [ML reproducibility lab](labs/15-ml-reproducibility/README.md), the [release lab](28-mlops/lab-reproducible-release.md), the [bad rollout incident](incidents/06-bad-rollout/README.md), then [project 10](projects/10-reproducible-ml-pipeline/README.md).
- Accelerator systems and capacity: [GPU Systems](29-gpu-systems/README.md), its [performance investigation](29-gpu-systems/09-practical-gpu-systems-lab.md), the [GPU scheduling and OOM lab](labs/16-gpu-scheduling-oom/README.md), the [GPU OOM incident](incidents/11-gpu-oom/README.md), [AI Infrastructure](30-ai-infrastructure/README.md), its [cluster simulator](30-ai-infrastructure/09-practical-ai-infrastructure-lab.md), the [queue overload incident](incidents/12-queue-overload/README.md), then [project 11](projects/11-distributed-gpu-planner/README.md).
- AWS delivery and operations: [AWS](12-aws/README.md), [DevOps](13-devops/README.md), and [Terraform](14-terraform/README.md), their module labs, the [AWS product lab sequence](labs/README.md#aws-dop-c02-gap-labs), the [bad rollout incident](incidents/06-bad-rollout/README.md), then [projects 04 and 05](projects/README.md). The [DOP-C02 overlay](certs/aws-dop-c02.md) maps this evidence without replacing the modules.

## Foundations

- 00 [History](00-history/README.md)
- 01 [Software Foundations](01-software-foundations/README.md)
- 02 [Python](02-python/README.md)
- 03 [Computer Systems](03-computer-systems/README.md)
- 04 [Linux](04-linux/README.md)
- 05 [Git](05-git/README.md)
- 06 [Data Structures and Algorithms](06-data-structures-algorithms/README.md)

## Data and services

- 07 [Networking](07-networking/README.md)
- 08 [Databases](08-databases/README.md)
- 09 [Backend Engineering](09-backend-engineering/README.md)
- 10 [Go](10-go/README.md)
- 11 [Software Architecture](11-software-architecture/README.md)

## Cloud infrastructure

- 12 [AWS](12-aws/README.md)
- 13 [DevOps](13-devops/README.md)
- 14 [Terraform](14-terraform/README.md)
- 15 [Containers](15-containers/README.md)
- 16 [Kubernetes](16-kubernetes/README.md)
- 17 [Distributed Systems](17-distributed-systems/README.md)
- 18 [Observability](18-observability/README.md)
- 19 [Site Reliability Engineering](19-sre/README.md)
- 20 [Security](20-security/README.md)

## Platforms

- 21 [Platform Engineering](21-platform-engineering/README.md)
- 22 [Developer Platforms](22-developer-platforms/README.md)
- 23 [Control Planes](23-control-planes/README.md)

## AI systems

- 24 [AI Foundations](24-ai-foundations/README.md)
- 25 [Machine Learning and Deep Learning](25-ml-deep-learning/README.md)
- 26 [Transformers and LLMs](26-transformers-llms/README.md)
- 27 [LLM Engineering](27-llm-engineering/README.md)
- 28 [MLOps](28-mlops/README.md)
- 29 [GPU Systems](29-gpu-systems/README.md)
- 30 [AI Infrastructure](30-ai-infrastructure/README.md)
- 31 [Model Serving](31-model-serving/README.md)
- 32 [AI Platform Engineering](32-ai-platform-engineering/README.md)
- 33 [Agentic Infrastructure](33-agentic-infrastructure/README.md)

## Design and leadership

- 34 [System Design](34-system-design/README.md)
- 35 [Senior and Staff Engineering](35-senior-staff-engineering/README.md)

## How to use it

Study dependencies in order when a subject is new. Skip ahead only when you can produce the prerequisite evidence: a correct explanation, a working build, and diagnosis of a relevant failure. Deepen the modules that support your work; return to earlier ones when an abstraction leaks.

The module numbers provide the dependable first pass. Real work is less linear. Once you can program and inspect a system, it is reasonable to study an application track alongside its infrastructure track. The [ROADMAP.md](ROADMAP.md) stage gates state the evidence needed before later platform claims are credible.

Use the full learning loop:

1. read the chapter orientation and record a prediction;
2. work the lessons in order, running the smallest useful proofs;
3. complete the linked module and standalone labs, retaining the evidence named in their rubrics;
4. attempt the linked incident before opening its solution, then record which design assumption changed;
5. integrate the accepted evidence and incident corrections into the linked portfolio project;
6. use the interview bank to explain changed constraints;
7. record inspectable evidence in [PROGRESS.md](PROGRESS.md).
