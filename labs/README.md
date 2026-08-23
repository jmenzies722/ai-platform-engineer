# Labs

Labs turn a conceptual model into observable evidence. Predict first, establish a baseline, inspect the mechanism, make one change, introduce one fault, diagnose it, and prove recovery. Completion means you can account for behavior, not merely that commands exited successfully.

## Choose a lab

Start with the smallest environment you have. "Local" means no cloud account; some local labs optionally require Docker or a disposable Kubernetes cluster. Expected time is a bounded working-session range, not a guarantee.

| Lab | Engineering domain | Environment | Expected time | Primary evidence |
|---|---|---|---|---|
| [01. Inspect One Python Process](01-software-execution/README.md) | Software execution | Linux, Python | 30 to 45 minutes | Process identity, `/proc`, memory, descriptors |
| [02. Diagnose a Slow Linux Workload](02-linux-diagnosis/README.md) | Linux diagnosis | Linux, Python | 45 to 60 minutes | State, CPU time, context switches, files, host pressure |
| [03. Recover Git Work](03-git-recovery/README.md) | Git recovery | Git, local repository | 45 to 60 minutes | Reflog, object IDs, index/worktree distinctions |
| [04. Debug DNS, TCP, TLS, and HTTP](04-network-dns-tls/README.md) | Networking | Local tools, public endpoint | 45 to 60 minutes | Resolver, connection, certificate, HTTP-layer evidence |
| [05. Observe PostgreSQL and Redis](05-postgres-redis/README.md) | Data systems | Docker Compose | 60 to 90 minutes | Transactions, locks, invariants, key expiration |
| [06. Engineer Backend Reliability](06-backend-reliability/README.md) | Backend reliability | Python, loopback | 60 to 90 minutes | Deadline, retry timeline, idempotency assumptions |
| [07. Review AWS Architecture Read-Only](07-aws-architecture-review/README.md) | Cloud architecture | Approved AWS sandbox | 60 to 90 minutes | Redacted inventory, relationships, evidence-linked findings |
| [08. Protect Terraform Plan and State](08-terraform-safety/README.md) | Infrastructure as code | Terraform, local state | 60 to 75 minutes | Saved plans, state, hashes, stale-plan analysis |
| [09. Inspect Container Isolation](09-container-isolation/README.md) | Containers | Docker | 60 to 75 minutes | Namespaces, cgroups, mounts, ports, resource limits |
| [10. Operate Kubernetes Workloads](10-kubernetes-operations/README.md) | Kubernetes | Disposable local cluster | 60 to 90 minutes | Reconciliation, probes, events, endpoints |
| [11. Investigate OpenTelemetry Traces](11-opentelemetry-traces/README.md) | Observability | Docker Compose | 60 to 90 minutes | Span parentage, timing, critical path, error status |
| [12. Calculate an SLO and Run an Incident](12-sre-slo-incident/README.md) | SRE | Python, synthetic data | 60 to 90 minutes | SLI, error budget, burn rate, incident timeline |
| [13. Threat-Model a File Upload Service](13-security-threat-model/README.md) | Security | Markdown, Mermaid | 60 to 90 minutes | Trust boundaries, threat register, testable controls |
| [14. Design a Reconciliation Control Plane](14-platform-control-plane/README.md) | Platform engineering | Python, SQLite | 90 to 120 minutes | API contract, convergence, audit, tenant checks |
| [15. Reproduce an ML Experiment](15-ml-reproducibility/README.md) | Machine learning | Python, synthetic data | 60 to 90 minutes | Data/code hashes, split lineage, deterministic metrics |
| [16. Simulate GPU Scheduling and OOM](16-gpu-scheduling-oom/README.md) | GPU infrastructure | Python simulation | 60 to 90 minutes | Placements, memory timeline, invariants, retry waste |
| [17. Control Model-Serving Overload](17-model-serving-overload/README.md) | Model serving | Python, loopback | 60 to 90 minutes | Tail latency, admission, rejection, retry amplification |
| [18. Verify AI Platform Tenancy](18-ai-platform-tenancy/README.md) | AI platform | Python, SQLite | 75 to 105 minutes | Isolation tests, cache keys, usage idempotency |
| [19. Bound an Agent Runtime](19-agent-runtime-safety/README.md) | Agent safety | Python, mocked tools | 75 to 105 minutes | Policy denials, budgets, approvals, audit chain |
| [20. Operate an AWS-Native Delivery Path](20-aws-native-delivery/README.md) | AWS delivery | Authorized AWS sandbox | 75 to 105 minutes | Pipeline gates, ECR digest, deployment, rollback, audit |
| [21. Operate a CloudFormation Resource Lifecycle](21-cloudformation-lifecycle/README.md) | AWS infrastructure as code | Local review and authorized AWS sandbox | 60 to 120 minutes | Change set, replacement, rollback, drift, StackSets boundary |
| [22. Review AWS Organization Governance and Audit Controls](22-aws-org-governance-and-audit/README.md) | AWS governance and audit | Local fixture; optional organization sandbox | 45 to 90 minutes | SCP reasoning, delegated administration, centralized audit, tamper denial |
| [23. Operate a Small AWS Fleet and Bounded Event Remediation](23-aws-fleet-and-event-remediation/README.md) | AWS fleet operations | Local fixture; optional authorized AWS sandbox | 45 to 150 minutes | SSM inventory, Config drift, durable events, idempotent remediation |
| [24. Deploy One Immutable Workload to Lambda and ECS Fargate](24-aws-deployment-targets/README.md) | AWS deployment targets | Authorized AWS sandbox | 75 to 120 minutes | Shared image digest, target-specific failure, recovery |
| [25. Measure AWS Backup Recovery and Tabletop Multi-Region Failover](25-aws-recovery-and-backup/README.md) | AWS resilience | Authorized AWS sandbox and local tabletop | 45 to 90 minutes | Restore, measured RTO/RPO, DNS behavior, failback gates |
| [26. Build and Diagnose a Bounded AWS Telemetry Pipeline](26-aws-telemetry-pipeline/README.md) | AWS observability | Local fixture or authorized AWS sandbox | 60 to 90 minutes | Encrypted logs, metric filter, query, alarm, missing telemetry, cost |
| [27. Route and Triage Bounded AWS Security Findings](27-aws-security-findings/README.md) | AWS security operations | Authorized empty AWS sandbox | 60 to 90 minutes | Synthetic findings, constrained routing, triage, expiring suppression |

## Suggested paths

- Foundations and diagnosis: 01, 02, 04, 06, 11, 12
- Delivery and infrastructure: 03, 08, 09, 10, 14, then 20 through 27 for AWS product practice
- Data and cloud: 05, 07, 13
- ML and AI systems: 15, 16, 17, 18, 19

The numbering provides a stable inventory, not a strict prerequisite chain. Each lab lists its own requirements and stop conditions.

## AWS DOP-C02 gap labs

Labs 20 through 27 are bounded product exercises for the [DOP-C02 overlay](../certs/aws-dop-c02.md). They extend the canonical AWS, DevOps, Terraform, observability, and security material; they do not form a separate certification course. Start with each lab's local or static path when available. Run account-backed steps only in the identity and sandbox boundary that the lab specifies.

Organization-level evidence in lab 22 requires an existing, explicitly authorized organization sandbox. An ordinary AWS account cannot supply that evidence, and the lab does not instruct you to create or dismantle an organization.

## Working rules

- Run unfamiliar commands in a disposable environment first.
- Read every command before execution; never paste secrets into evidence.
- Confirm the current directory, account, cluster context, and target identity before mutations.
- Predict output and failure signatures before observing them.
- Introduce one failure at a time and keep resource, request, and time bounds.
- Preserve only useful output, environment/version context, hashes, and timestamps.
- Treat missing telemetry and denied access as unknown, not healthy.
- Stop when safety, cost, authorization, or blast-radius assumptions are invalid.
- Complete cleanup and prove that local processes or billable resources are gone.
- Use [the lab template](../templates/LAB.md) for future labs.

## Standard completion record

For each lab, keep:

1. prerequisites and exact environment versions;
2. safety checks and stop conditions;
3. initial prediction and healthy baseline;
4. commands, configuration, and relevant output;
5. failure symptom, hypotheses, diagnosis, and correction;
6. evidence supporting each claim and what it does not prove;
7. cleanup proof, rubric score, and primary sources.
