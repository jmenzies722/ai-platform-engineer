# AWS Certified DevOps Engineer - Professional (DOP-C02) overlay

This is an assessment and study overlay on the existing curriculum, not a
parallel certification course. Follow linked lessons for the material itself;
use this page to select, sequence, and assess that work against the official
blueprint.

Passing a certification exam is not equivalent to operating competence. The
exam can validate knowledge and scenario judgment within its blueprint.
Competence requires independent implementation, diagnosis under uncertainty,
safe operation, and defensible design backed by inspectable evidence.

## Official scope

Exam claims on this page come only from the current [AWS certification
page](https://aws.amazon.com/certification/certified-devops-engineer-professional/)
and the [AWS DOP-C02 exam
guide](https://docs.aws.amazon.com/aws-certification/latest/devops-engineer-professional-02/devops-engineer-professional-02.html),
including its six linked domain pages. The blueprint and exam details were
verified against those pages on 2026-08-23; recheck them before scheduling or
when AWS publishes a new exam code.

AWS describes the exam as validating technical expertise in provisioning,
operating, and managing distributed systems and services on AWS. The
certification page currently lists a Professional-level, 180-minute exam with
75 multiple-choice or multiple-response questions. The exam guide says that 65
questions are scored, 10 are unscored, the scaled score range is 100 to 1,000,
and the minimum passing score is 750. AWS recommends two or more years of
experience provisioning, operating, and managing AWS environments, plus
software development lifecycle and programming or scripting experience.

| Official content domain | Weight |
|---|---:|
| [Domain 1: SDLC Automation](https://docs.aws.amazon.com/aws-certification/latest/devops-engineer-professional-02/devops-engineer-professional-02-domain1.html) | 22% |
| [Domain 2: Configuration Management and IaC](https://docs.aws.amazon.com/aws-certification/latest/devops-engineer-professional-02/devops-engineer-professional-02-domain2.html) | 17% |
| [Domain 3: Resilient Cloud Solutions](https://docs.aws.amazon.com/aws-certification/latest/devops-engineer-professional-02/devops-engineer-professional-02-domain3.html) | 15% |
| [Domain 4: Monitoring and Logging](https://docs.aws.amazon.com/aws-certification/latest/devops-engineer-professional-02/devops-engineer-professional-02-domain4.html) | 15% |
| [Domain 5: Incident and Event Response](https://docs.aws.amazon.com/aws-certification/latest/devops-engineer-professional-02/devops-engineer-professional-02-domain5.html) | 14% |
| [Domain 6: Security and Compliance](https://docs.aws.amazon.com/aws-certification/latest/devops-engineer-professional-02/devops-engineer-professional-02-domain6.html) | 17% |

Weights allocate review effort; they do not lower the competency standard for
any domain.

## Assessment gates used in the mapping

These gates apply the repository's [competency
matrix](../PROGRESS.md#competency-matrix), [evidence
rules](../PROGRESS.md#evidence-rules), [roadmap advancement
rule](../ROADMAP.md#advancement-rule), [lab completion
record](../labs/README.md#standard-completion-record), [incident completion
rubric](../incidents/README.md#completion-rubric), and [project graduation
criteria](../PROJECTS.md#graduation-criteria).

| Gate | Required evidence |
|---|---|
| G0, entry | Meet the relevant Stage 3, 4, and 5 exit evidence in [ROADMAP.md](../ROADMAP.md): AWS architecture, delivery and IaC, security, distributed systems, observability, SRE, and design. A knowledge-only gap is recorded, not hidden. |
| G1, guided mechanism | **Explain** the mechanism and tradeoff accurately; **Build** the linked module or guided lab; retain prediction, commands or configuration, output, limits, and cleanup proof. |
| G2, failure response | **Debug** a linked incident before reading its solution; **Operate** through bounded mitigation and recovery; pass every dimension of the Incident Drill Academy rubric. |
| G3, independent system | In a separate repository, complete the linked project milestones and explicit rubric. Evidence must cover **Explain, Build, Debug, Operate, Design**; the weakest relevant dimension limits the claim. |
| G4, blueprint readiness | Explain every task statement without notes, compare plausible AWS choices from stated constraints, and justify why alternatives fail. Close or explicitly accept every gap below, then use AWS's official practice questions and practice exam. G4 is exam readiness, not a `Competent` rating. |

G0 through G4 are overlay checkpoints, not a second set of curriculum gates. Use the repository's [common assessment rubric](../assessments/rubric.md) and record formal gate outcomes in [PROGRESS.md](../PROGRESS.md#assessment-gate-outcomes). The official domains align to the existing gates as follows:

| Official domains | Curriculum gates that supply evidence |
|---|---|
| Domains 1 and 2 | [Cloud Delivery](../assessments/gates/cloud-delivery.md) is the primary gate for pipelines, artifacts, IaC, account boundaries, configuration, recovery, and supply-chain controls. |
| Domain 3 | [Cloud Delivery](../assessments/gates/cloud-delivery.md) establishes cloud change and recovery evidence; [Kubernetes Reliability](../assessments/gates/kubernetes-reliability.md) tests scaling, availability, release, and recovery judgment under failure. |
| Domains 4 and 5 | [Kubernetes Reliability](../assessments/gates/kubernetes-reliability.md) tests telemetry-led operations and incident response; [Platform](../assessments/gates/platform.md) adds event-driven reconciliation and safe automated action. |
| Domain 6 | [Cloud Delivery](../assessments/gates/cloud-delivery.md) tests identity, artifact, state, and policy boundaries; [Kubernetes Reliability](../assessments/gates/kubernetes-reliability.md) tests workload security and response; [Platform](../assessments/gates/platform.md) adds tenant-safe governance at scale. |

Passing these gates does not by itself close the AWS-product gaps below. Conversely, an exam-ready explanation without gate evidence does not establish Build, Debug, Operate, or Design competence.

## Complete task-statement map

The lesson column names exact existing curriculum material. Practice links are
selected evidence opportunities, not substitutes for AWS product practice.
“No direct drill” is an intentional gap declaration.

### Domain 1: SDLC Automation, 22%

| Official task statement | Exact modules and lessons | Guided labs, incident drills, and projects | Gates |
|---|---|---|---|
| **1.1 Implement CI/CD pipelines.** | [DevOps](../13-devops/README.md): [Continuous integration and delivery](../13-devops/02-continuous-delivery.md), [Artifacts, registries, and promotion](../13-devops/04-artifacts-and-promotion.md), [Delivery governance and production learning](../13-devops/06-governance-and-learning.md); [AWS](../12-aws/README.md): [Operations, observability, and safe automation](../12-aws/05-operations-and-observability.md) | [Evidence-preserving delivery path](../13-devops/lab-delivery-evidence.md), [AWS-native delivery path](../labs/20-aws-native-delivery/README.md); [Bad rollout](../incidents/06-bad-rollout/README.md); [Verifiable Software Delivery Pipeline](../projects/05-secure-delivery-pipeline/README.md) | G1, G2, G3, G4 |
| **1.2 Integrate automated testing into CI/CD pipelines.** | [DevOps](../13-devops/README.md): [Continuous integration and delivery](../13-devops/02-continuous-delivery.md), [Safe changes and recovery](../13-devops/03-safe-change.md), [Software supply-chain security](../13-devops/05-supply-chain-security.md); [SRE](../19-sre/README.md): [Release engineering and resilience](../19-sre/07-release-resilience.md) | [Evidence-preserving delivery path](../13-devops/lab-delivery-evidence.md), [AWS-native delivery path](../labs/20-aws-native-delivery/README.md); [Bad rollout](../incidents/06-bad-rollout/README.md); [Verifiable Software Delivery Pipeline](../projects/05-secure-delivery-pipeline/README.md) | G1, G2, G3, G4 |
| **1.3 Build and manage artifacts.** | [DevOps](../13-devops/README.md): [Artifacts, registries, and promotion](../13-devops/04-artifacts-and-promotion.md), [Software supply-chain security](../13-devops/05-supply-chain-security.md); [Containers](../15-containers/README.md): [OCI images and reproducible builds](../15-containers/02-images-and-builds.md), [Runtime hardening and image trust](../15-containers/05-security-and-trust.md) | [Evidence-preserving delivery path](../13-devops/lab-delivery-evidence.md), [AWS-native delivery path](../labs/20-aws-native-delivery/README.md), [Inspect Container Isolation](../labs/09-container-isolation/README.md); [Bad rollout](../incidents/06-bad-rollout/README.md); [Verifiable Software Delivery Pipeline](../projects/05-secure-delivery-pipeline/README.md) | G1, G2, G3, G4 |
| **1.4 Implement deployment strategies for instance, container, and serverless environments.** | [AWS](../12-aws/README.md): [Compute, storage, and managed data](../12-aws/03-compute-storage-data.md); [DevOps](../13-devops/README.md): [Safe changes and recovery](../13-devops/03-safe-change.md); [Kubernetes](../16-kubernetes/README.md): [Services, configuration, and failure diagnosis](../16-kubernetes/03-service-and-operations.md), [Autoscaling, upgrades, and cluster operations](../16-kubernetes/06-scaling-and-upgrades.md) | [AWS-native delivery path](../labs/20-aws-native-delivery/README.md), [Lambda and ECS Fargate targets](../labs/24-aws-deployment-targets/README.md), [Operate Kubernetes Workloads](../labs/10-kubernetes-operations/README.md), [Evidence-preserving delivery path](../13-devops/lab-delivery-evidence.md); [Bad rollout](../incidents/06-bad-rollout/README.md), [Kubernetes CrashLoopBackOff](../incidents/07-kubernetes-crashloopbackoff/README.md); [Verifiable Software Delivery Pipeline](../projects/05-secure-delivery-pipeline/README.md) | G1, G2, G3, G4 |

### Domain 2: Configuration Management and IaC, 17%

| Official task statement | Exact modules and lessons | Guided labs, incident drills, and projects | Gates |
|---|---|---|---|
| **2.1 Define cloud infrastructure and reusable components to provision and manage systems throughout their lifecycle.** | [Terraform](../14-terraform/README.md): [Configuration, providers, and the graph](../14-terraform/01-configuration-and-graph.md), [Modules and safe lifecycle](../14-terraform/03-modules-and-lifecycle.md), [Testing and automated workflows](../14-terraform/04-testing-and-workflows.md), [Drift operations and state recovery](../14-terraform/06-drift-and-recovery.md); [AWS](../12-aws/README.md): [Operations, observability, and safe automation](../12-aws/05-operations-and-observability.md) | [CloudFormation resource lifecycle](../labs/21-cloudformation-lifecycle/README.md), [Protect Terraform Plan and State](../labs/08-terraform-safety/README.md), [Terraform change control](../14-terraform/lab-change-control.md); [Bad rollout](../incidents/06-bad-rollout/README.md); [Recoverable AWS Foundation with Terraform](../projects/04-aws-terraform-foundation/README.md) | G1, G2, G3, G4 |
| **2.2 Deploy automation to create, onboard, and secure AWS accounts in a multi-account or multi-Region environment.** | [AWS](../12-aws/README.md): [Accounts, IAM, and the AWS API](../12-aws/01-identity-and-api.md), [Cost models, allocation, and optimization](../12-aws/06-cost-and-governance.md); [Security](../20-security/README.md): [Identity, authentication, and authorization](../20-security/02-identity-and-access.md), [Cloud and application security](../20-security/06-cloud-and-application-security.md); [Terraform](../14-terraform/README.md): [Modules and safe lifecycle](../14-terraform/03-modules-and-lifecycle.md) | [Organization governance and audit controls](../labs/22-aws-org-governance-and-audit/README.md), [CloudFormation StackSets boundary](../labs/21-cloudformation-lifecycle/README.md), [Review AWS Architecture Read-Only](../labs/07-aws-architecture-review/README.md), [Test identity and application boundaries](../20-security/lab-security-boundaries.md); no direct multi-account incident drill; [Recoverable AWS Foundation with Terraform](../projects/04-aws-terraform-foundation/README.md) supplies a single-account baseline only | G1 and G4; G2 and G3 remain open until authorized multi-account onboarding, governance, and failure evidence exists |
| **2.3 Design and build automated solutions for complex tasks and large-scale environments.** | [AWS](../12-aws/README.md): [Operations, observability, and safe automation](../12-aws/05-operations-and-observability.md); [Distributed Systems](../17-distributed-systems/README.md): [Idempotency, retries, and uncertain outcomes](../17-distributed-systems/06-idempotency-and-retries.md), [Queues, flow control, and backpressure](../17-distributed-systems/07-queues-and-backpressure.md); [Control Planes](../23-control-planes/README.md): [Reconciliation, queues, and convergence](../23-control-planes/02-reconciliation.md), [Idempotency and external identity](../23-control-planes/04-idempotency-and-external-identity.md) | [CloudFormation resource lifecycle](../labs/21-cloudformation-lifecycle/README.md), [Fleet and event remediation](../labs/23-aws-fleet-and-event-remediation/README.md), [Design a Reconciliation Control Plane](../labs/14-platform-control-plane/README.md), [Expose duplicate work and overload](../17-distributed-systems/lab-failure-harness.md); [Retry storm](../incidents/08-retry-storm/README.md), [Queue overload](../incidents/12-queue-overload/README.md); [Secure Developer Platform Control Plane](../projects/09-developer-platform-control-plane/README.md) | G1, G2, G3, G4 |

### Domain 3: Resilient Cloud Solutions, 15%

| Official task statement | Exact modules and lessons | Guided labs, incident drills, and projects | Gates |
|---|---|---|---|
| **3.1 Implement highly available solutions to meet resilience and business requirements.** | [AWS](../12-aws/README.md): [Regions, VPCs, and network boundaries](../12-aws/02-regions-and-vpcs.md), [Availability, recovery, and resilient design](../12-aws/04-availability-and-recovery.md); [SRE](../19-sre/README.md): [Availability architecture and failure domains](../19-sre/06-availability-engineering.md); [Software Architecture](../11-software-architecture/README.md): [Quality Attributes and Decisions](../11-software-architecture/02-quality-attributes-and-decisions.md) | [Backup recovery and multi-Region tabletop](../labs/25-aws-recovery-and-backup/README.md), [Review AWS Architecture Read-Only](../labs/07-aws-architecture-review/README.md), [Calculate an SLO and Run an Incident](../labs/12-sre-slo-incident/README.md); [DNS resolution failure](../incidents/01-dns-failure/README.md), [TLS certificate expiry](../incidents/04-tls-expiry/README.md); [Recoverable AWS Foundation with Terraform](../projects/04-aws-terraform-foundation/README.md), [Reliability Review and Incident Exercise](../projects/08-reliability-exercise/README.md) | G1, G2, G3, G4 |
| **3.2 Implement solutions that are scalable to meet business requirements.** | [AWS](../12-aws/README.md): [Compute, storage, and managed data](../12-aws/03-compute-storage-data.md); [SRE](../19-sre/README.md): [Capacity planning and overload](../19-sre/05-capacity-and-overload.md); [Distributed Systems](../17-distributed-systems/README.md): [Queues, flow control, and backpressure](../17-distributed-systems/07-queues-and-backpressure.md); [Kubernetes](../16-kubernetes/README.md): [Autoscaling, upgrades, and cluster operations](../16-kubernetes/06-scaling-and-upgrades.md) | [Engineer Backend Reliability](../labs/06-backend-reliability/README.md), [Operate Kubernetes Workloads](../labs/10-kubernetes-operations/README.md); [Memory exhaustion and OOM kill](../incidents/02-oom/README.md), [Retry storm](../incidents/08-retry-storm/README.md), [Queue overload](../incidents/12-queue-overload/README.md); [Reliability Review and Incident Exercise](../projects/08-reliability-exercise/README.md) | G1, G2, G3, G4 |
| **3.3 Implement automated recovery processes to meet RTO and RPO requirements.** | [AWS](../12-aws/README.md): [Availability, recovery, and resilient design](../12-aws/04-availability-and-recovery.md); [Terraform](../14-terraform/README.md): [Drift operations and state recovery](../14-terraform/06-drift-and-recovery.md); [SRE](../19-sre/README.md): [Availability architecture and failure domains](../19-sre/06-availability-engineering.md), [Release engineering and resilience](../19-sre/07-release-resilience.md) | [Backup recovery and multi-Region tabletop](../labs/25-aws-recovery-and-backup/README.md) supplies guided restore evidence but not an automated recovery implementation; [Terraform change control](../14-terraform/lab-change-control.md), [Calculate an SLO and Run an Incident](../labs/12-sre-slo-incident/README.md); [Disk exhaustion](../incidents/03-disk-exhaustion/README.md), [Bad rollout](../incidents/06-bad-rollout/README.md); [Recoverable AWS Foundation with Terraform](../projects/04-aws-terraform-foundation/README.md), [Reliability Review and Incident Exercise](../projects/08-reliability-exercise/README.md) | G1, G2, G3, G4 |

### Domain 4: Monitoring and Logging, 15%

| Official task statement | Exact modules and lessons | Guided labs, incident drills, and projects | Gates |
|---|---|---|---|
| **4.1 Configure the collection, aggregation, and storage of logs and metrics.** | [AWS](../12-aws/README.md): [Operations, observability, and safe automation](../12-aws/05-operations-and-observability.md); [Observability](../18-observability/README.md): [Telemetry as an evidence model](../18-observability/01-telemetry-model.md), [Metrics, distributions, and alertable semantics](../18-observability/03-metrics.md), [Structured logs and event design](../18-observability/04-logs.md), [Cardinality, retention, and telemetry cost](../18-observability/06-cardinality-and-cost.md) | [AWS telemetry pipeline](../labs/26-aws-telemetry-pipeline/README.md), [Diagnose a telemetry pipeline](../18-observability/lab-telemetry.md), [Investigate OpenTelemetry Traces](../labs/11-opentelemetry-traces/README.md); [Disk exhaustion](../incidents/03-disk-exhaustion/README.md); [Operable Telemetry Stack](../projects/07-telemetry-stack/README.md) | G1, G2, G3, G4 |
| **4.2 Audit, monitor, and analyze logs and metrics to detect issues.** | [Observability](../18-observability/README.md): [Metrics, distributions, and alertable semantics](../18-observability/03-metrics.md), [Structured logs and event design](../18-observability/04-logs.md), [Traces, causality, and sampling](../18-observability/05-traces-and-sampling.md), [Instrumentation strategy and evidence-led diagnosis](../18-observability/07-instrumentation-and-diagnosis.md); [AWS](../12-aws/README.md): [Operations, observability, and safe automation](../12-aws/05-operations-and-observability.md) | [AWS telemetry pipeline](../labs/26-aws-telemetry-pipeline/README.md), [Organization governance and audit controls](../labs/22-aws-org-governance-and-audit/README.md), [Investigate OpenTelemetry Traces](../labs/11-opentelemetry-traces/README.md), [Calculate an SLO and Run an Incident](../labs/12-sre-slo-incident/README.md); [Database pool exhaustion](../incidents/05-database-pool-exhaustion/README.md), [Bad rollout](../incidents/06-bad-rollout/README.md); [Operable Telemetry Stack](../projects/07-telemetry-stack/README.md) | G1, G2, G3, G4 |
| **4.3 Automate monitoring and event management of complex environments.** | [AWS](../12-aws/README.md): [Operations, observability, and safe automation](../12-aws/05-operations-and-observability.md); [Observability](../18-observability/README.md): [Metrics, distributions, and alertable semantics](../18-observability/03-metrics.md); [Distributed Systems](../17-distributed-systems/README.md): [Queues, flow control, and backpressure](../17-distributed-systems/07-queues-and-backpressure.md); [Control Planes](../23-control-planes/README.md): [Reconciliation, queues, and convergence](../23-control-planes/02-reconciliation.md) | [Fleet and event remediation](../labs/23-aws-fleet-and-event-remediation/README.md), [Design a Reconciliation Control Plane](../labs/14-platform-control-plane/README.md), [Engineer Backend Reliability](../labs/06-backend-reliability/README.md); [Retry storm](../incidents/08-retry-storm/README.md), [Queue overload](../incidents/12-queue-overload/README.md); [Operable Telemetry Stack](../projects/07-telemetry-stack/README.md), [Secure Developer Platform Control Plane](../projects/09-developer-platform-control-plane/README.md) | G1, G2, G3, G4 |

### Domain 5: Incident and Event Response, 14%

| Official task statement | Exact modules and lessons | Guided labs, incident drills, and projects | Gates |
|---|---|---|---|
| **5.1 Manage event sources to process, notify, and take action in response to events.** | [Distributed Systems](../17-distributed-systems/README.md): [Queues, flow control, and backpressure](../17-distributed-systems/07-queues-and-backpressure.md), [Idempotency, retries, and uncertain outcomes](../17-distributed-systems/06-idempotency-and-retries.md); [Backend Engineering](../09-backend-engineering/README.md): [Queues, Delivery, and Workflow State](../09-backend-engineering/05-queues-delivery-and-workflow-state.md); [AWS](../12-aws/README.md): [Operations, observability, and safe automation](../12-aws/05-operations-and-observability.md) | [Fleet and event remediation](../labs/23-aws-fleet-and-event-remediation/README.md), [Engineer Backend Reliability](../labs/06-backend-reliability/README.md), [Expose duplicate work and overload](../17-distributed-systems/lab-failure-harness.md); [Retry storm](../incidents/08-retry-storm/README.md), [Queue overload](../incidents/12-queue-overload/README.md); [Reliability Review and Incident Exercise](../projects/08-reliability-exercise/README.md) | G1, G2, G3, G4 |
| **5.2 Implement configuration changes in response to events.** | [Control Planes](../23-control-planes/README.md): [Reconciliation, queues, and convergence](../23-control-planes/02-reconciliation.md), [Ownership, policy, and control-plane operations](../23-control-planes/03-ownership-and-operations.md); [Terraform](../14-terraform/README.md): [State, plans, and drift](../14-terraform/02-state-plans-drift.md), [Drift operations and state recovery](../14-terraform/06-drift-and-recovery.md); [AWS](../12-aws/README.md): [Operations, observability, and safe automation](../12-aws/05-operations-and-observability.md) | [Fleet and event remediation](../labs/23-aws-fleet-and-event-remediation/README.md), [Design a Reconciliation Control Plane](../labs/14-platform-control-plane/README.md), [Protect Terraform Plan and State](../labs/08-terraform-safety/README.md); [Kubernetes CrashLoopBackOff](../incidents/07-kubernetes-crashloopbackoff/README.md), [Bad rollout](../incidents/06-bad-rollout/README.md); [Recoverable AWS Foundation with Terraform](../projects/04-aws-terraform-foundation/README.md), [Secure Developer Platform Control Plane](../projects/09-developer-platform-control-plane/README.md) | G1, G2, G3, G4 |
| **5.3 Troubleshoot system and application failures.** | [Observability](../18-observability/README.md): [Instrumentation strategy and evidence-led diagnosis](../18-observability/07-instrumentation-and-diagnosis.md); [SRE](../19-sre/README.md): [Incident response and command](../19-sre/03-incident-command.md), [Learning reviews and toil reduction](../19-sre/04-learning-and-toil.md); [Containers](../15-containers/README.md): [Evidence-driven container debugging](../15-containers/06-debugging.md); [Kubernetes](../16-kubernetes/README.md): [Services, configuration, and failure diagnosis](../16-kubernetes/03-service-and-operations.md) | [Diagnose a telemetry pipeline](../18-observability/lab-telemetry.md), [Operate an SLO-driven incident](../19-sre/lab-slo-incident.md), [Operate Kubernetes Workloads](../labs/10-kubernetes-operations/README.md); complete at least three [Incident Drill Academy](../incidents/README.md) scenarios, including [Bad rollout](../incidents/06-bad-rollout/README.md); [Reliability Review and Incident Exercise](../projects/08-reliability-exercise/README.md) | G1, G2, G3, G4 |

### Domain 6: Security and Compliance, 17%

| Official task statement | Exact modules and lessons | Guided labs, incident drills, and projects | Gates |
|---|---|---|---|
| **6.1 Implement techniques for identity and access management at scale.** | [AWS](../12-aws/README.md): [Accounts, IAM, and the AWS API](../12-aws/01-identity-and-api.md); [Security](../20-security/README.md): [Identity, authentication, and authorization](../20-security/02-identity-and-access.md), [Secrets and credential lifecycles](../20-security/04-secrets-management.md); [Platform Engineering](../21-platform-engineering/README.md): [Self-service and tenancy](../21-platform-engineering/04-self-service-and-tenancy.md) | [Organization governance and audit controls](../labs/22-aws-org-governance-and-audit/README.md), [Review AWS Architecture Read-Only](../labs/07-aws-architecture-review/README.md), [Test identity and application boundaries](../20-security/lab-security-boundaries.md); no direct IAM-at-scale incident drill; [Recoverable AWS Foundation with Terraform](../projects/04-aws-terraform-foundation/README.md) | G1, G3, G4; G2 remains open until an authorized IAM failure drill exists |
| **6.2 Apply automation for security controls and data protection.** | [AWS](../12-aws/README.md): [Regions, VPCs, and network boundaries](../12-aws/02-regions-and-vpcs.md); [Security](../20-security/README.md): [Cryptography, key management, and TLS](../20-security/03-cryptography-and-tls.md), [Cloud and application security](../20-security/06-cloud-and-application-security.md); [Networking](../07-networking/README.md): [Addresses, Packets, and Routing](../07-networking/01-addresses-packets-and-routing.md), [HTTP, TLS, Proxies, and Load Balancing](../07-networking/05-http-tls-proxies-and-load-balancing.md) | [Threat-Model a File Upload Service](../labs/13-security-threat-model/README.md), [Review AWS Architecture Read-Only](../labs/07-aws-architecture-review/README.md); [DNS resolution failure](../incidents/01-dns-failure/README.md), [TLS certificate expiry](../incidents/04-tls-expiry/README.md); [Recoverable AWS Foundation with Terraform](../projects/04-aws-terraform-foundation/README.md) | G1, G2, G3, G4 |
| **6.3 Implement security monitoring and auditing solutions.** | [AWS](../12-aws/README.md): [Operations, observability, and safe automation](../12-aws/05-operations-and-observability.md); [Security](../20-security/README.md): [Cloud and application security](../20-security/06-cloud-and-application-security.md), [Security detection and incident response](../20-security/07-security-incident-response.md); [Observability](../18-observability/README.md): [Structured logs and event design](../18-observability/04-logs.md), [Instrumentation strategy and evidence-led diagnosis](../18-observability/07-instrumentation-and-diagnosis.md) | [AWS security findings](../labs/27-aws-security-findings/README.md), [Organization governance and audit controls](../labs/22-aws-org-governance-and-audit/README.md), [Review AWS Architecture Read-Only](../labs/07-aws-architecture-review/README.md), [Diagnose a telemetry pipeline](../18-observability/lab-telemetry.md), [Test identity and application boundaries](../20-security/lab-security-boundaries.md); [TLS certificate expiry](../incidents/04-tls-expiry/README.md); [Recoverable AWS Foundation with Terraform](../projects/04-aws-terraform-foundation/README.md), [Reliability Review and Incident Exercise](../projects/08-reliability-exercise/README.md) | G1, G2, G3, G4 |

## Overlay study order

Do not reorder unfamiliar dependencies merely to follow domain numbers.

1. **Baseline and scope:** pass G0; read the official exam guide and all six
   domain pages; create a 19-row evidence ledger matching the table above.
2. **AWS substrate:** complete [AWS](../12-aws/README.md) lessons 1 through 6
   and both [AWS architecture evidence
   lab](../12-aws/lab-read-only-inventory.md) and [guided read-only AWS
   review](../labs/07-aws-architecture-review/README.md).
3. **Delivery and IaC:** complete [DevOps](../13-devops/README.md) and
   [Terraform](../14-terraform/README.md), their module labs, then the guided
   Terraform lab. Apply Domain 1's higher weight when allocating recall and
   scenario practice.
4. **Runtime and failure mechanics:** revisit the mapped [Containers](../15-containers/README.md),
   [Kubernetes](../16-kubernetes/README.md), [Distributed
   Systems](../17-distributed-systems/README.md), and [Control
   Planes](../23-control-planes/README.md) lessons. Run the linked overload,
   rollout, and configuration drills.
5. **Evidence and response:** complete the mapped
   [Observability](../18-observability/README.md), [SRE](../19-sre/README.md),
   and [Security](../20-security/README.md) lessons and labs. Pass G2 on at
   least three incidents, with one deployment failure, one saturation or queue
   failure, and one security or certificate failure.
6. **Integration:** build [Project 04](../projects/04-aws-terraform-foundation/README.md)
   and [Project 05](../projects/05-secure-delivery-pipeline/README.md); use
   [Project 08](../projects/08-reliability-exercise/README.md) for the
   operational review. Reuse one suitable system across briefs when it can
   satisfy each contract; do not duplicate implementation for the exam.
7. **Close AWS-specific gaps:** complete [labs 20 through
   27](../labs/README.md#aws-dop-c02-gap-labs) in order. Use each local path
   before its account-backed extension when one exists. Keep costs, identity,
   Region, cleanup, and evidence limits explicit. Record the organization-only
   evidence below as remaining until an authorized organization sandbox exists.
8. **Exam review:** weight review by the official percentages, practice
   explaining all 19 task statements from constraints, pass G4, and only then
   use AWS's official practice set and practice exam.

## AWS-specific gap register

Transferable systems knowledge is valuable, but a generic mechanism or local
simulation is not evidence that its AWS implementation can be configured and
operated.

| Gap | Bounded practice now available | Status |
|---|---|---|
| AWS-native CI/CD and artifacts | [Operate an AWS-Native Delivery Path](../labs/20-aws-native-delivery/README.md) builds and tests with CodePipeline and CodeBuild, publishes an ECR digest, fails gates, recovers Lambda, checks secret access, and preserves CloudTrail evidence. CodeDeploy, CodeArtifact, and EC2 Image Builder remain explicit comparison choices rather than extra billable services. | **Guided gap closed.** |
| CloudFormation-family IaC | [Operate a CloudFormation Resource Lifecycle](../labs/21-cloudformation-lifecycle/README.md) reviews change sets and replacement, exercises rollback and drift, and includes a bounded StackSets review with a separately authorized organization extension. | **Guided gap closed.** |
| Account vending and governance | [Review AWS Organization Governance and Audit Controls](../labs/22-aws-org-governance-and-audit/README.md) provides a local policy fixture and exact read-only organization-sandbox evidence for SCPs, delegated administration, baselines, and centralized evidence. | **Organization evidence remains.** See the exact requirement below. |
| Fleet and configuration automation | [Operate a Small AWS Fleet and Bounded Event Remediation](../labs/23-aws-fleet-and-event-remediation/README.md) uses a local fixture or one SSM-managed instance, Config drift, EventBridge, durable failure routing, idempotent remediation, unsafe-action rejection, partial failure, and rollback. | **Guided gap closed.** Large-fleet competence is not implied. |
| AWS deployment targets | [Deploy One Immutable Workload to Lambda and ECS Fargate](../labs/24-aws-deployment-targets/README.md) runs one ECR digest on serverless and container targets, induces a failed release on each, and proves target-specific recovery. | **Guided gap closed.** EC2 instance deployment remains a comparison, not direct evidence. |
| Multi-Region resilience and AWS Backup | [Measure AWS Backup Recovery and Tabletop Multi-Region Failover](../labs/25-aws-recovery-and-backup/README.md) measures a bounded DynamoDB restore, stale-data bounds, RTO/RPO, DNS and client behavior, failback gates, and optional cross-Region copy. | **Guided gap closed.** This is operator-driven recovery evidence, not a production DR claim. |
| CloudWatch and AWS telemetry pipeline | [Build and Diagnose a Bounded AWS Telemetry Pipeline](../labs/26-aws-telemetry-pipeline/README.md) configures encrypted logs, retention, a metric filter, Logs Insights diagnosis, a user-impact alarm, missing-telemetry behavior, optional trace correlation, and a cost worksheet. | **Guided gap closed.** |
| Event-driven AWS operations | [Operate a Small AWS Fleet and Bounded Event Remediation](../labs/23-aws-fleet-and-event-remediation/README.md) exercises duplicate delivery, idempotency, durable failed work, a safe configuration repair, an unsafe-action denial, audit, and recovery. | **Guided gap closed.** |
| AWS security automation and findings | [Route and Triage Bounded AWS Security Findings](../labs/27-aws-security-findings/README.md) enables a minimal Security Hub and GuardDuty slice, generates only documented synthetic findings, routes and triages them, records expiring suppression, checks encryption and permissions, and accounts for residual risk and cost. | **Guided gap closed.** Organization aggregation is covered by the remaining requirement below. |
| Audit at organization scale | [Review AWS Organization Governance and Audit Controls](../labs/22-aws-org-governance-and-audit/README.md) provides a local audit fixture and a non-mutating extension for an existing organization trail, protected archive, Config aggregator, principal-to-resource query, and attributable denial tests. | **Organization evidence remains.** See the exact requirement below. |

### Remaining organization-sandbox evidence

Do not simulate these claims into completion. They require an existing,
purpose-built AWS Organizations sandbox and written authorization:

| Remaining claim | Exact evidence required |
|---|---|
| Task 2.2 account onboarding and governance; task 6.1 IAM at scale | One disposable member-account onboarding record; approved baseline and role path; Control Tower or equivalent lifecycle evidence; SCP allow and explicit-deny tests with decoded authorization; delegated-administrator registration; a bounded failed-onboarding or access-denial diagnosis; and owner-approved cleanup or reset proof. |
| Organization-scale audit | An organization trail covering the disposable member account; protected archive retention and encryption settings; cross-account Config aggregator query; event-to-principal-to-resource investigation; anomalous-event alert delivery; an attributable denied archive-tamper attempt; retention policy; break-glass review; and proof that the lab changed no production organization control. |

## Practice and evidence plan

Maintain one evidence index keyed by task statement. A single artifact may
support several tasks, but each claim must identify the exact observation it
supports and what it does not prove.

| Dimension | Practice | Minimum inspectable evidence | Competency gate |
|---|---|---|---|
| **Explain** | Teach back each task from a business constraint through AWS service choice, mechanism, permissions, state, failure modes, cost, and rejected alternatives. | Nineteen concise explanations; domain-weighted comparison questions; uncertainty and gap notes; no memorized service list without causal reasoning. | G1 for guided understanding; G4 for complete blueprint recall and scenario judgment. |
| **Build** | Complete mapped labs, then implement the smallest authorized AWS-native slice that closes each accepted gap. | Versioned configuration and tests, principal and Region proof, reviewed changes, immutable artifact identities, outputs, cost bounds, and cleanup proof. | G1 for guided work; G3 for independent integration. |
| **Debug** | Attempt incident drills closed-book and inject product-specific deployment, policy, telemetry, drift, scaling, and event failures. | Symptoms, ranked hypotheses, discriminating tests, contradictory evidence, root or contributing causes, and proof that the correction addresses the mechanism. | G2, plus the Debug column in [PROGRESS.md](../PROGRESS.md). |
| **Operate** | Run releases, rollback, failover or recovery, alert response, credential or policy change, retention, patching, and audit review within explicit stop conditions. | Runbooks used by another operator, timelines, approvals, rollback triggers, measured recovery, residual risk, cost, and complete teardown. | G2 for bounded incidents; G3 for sustained project operation. |
| **Design** | Compare multi-account, multi-AZ or multi-Region, deployment, IaC, event, observability, and security-control options against requirements. | Architecture and trust-boundary diagrams, RTO/RPO and capacity assumptions, ADRs, policy model, failure analysis, cost model, and revisit triggers. | G3 and the Design column in [PROGRESS.md](../PROGRESS.md). |

Only update competency ratings when the evidence meets the repository rules.
An exam pass may be linked as certification evidence, but it cannot by itself
advance Build, Debug, Operate, or Design.
