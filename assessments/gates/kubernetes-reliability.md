# Kubernetes Reliability Gate

This gate tests reconciliation, partial failure, observability, reliability policy, and security under operational pressure. It covers [Kubernetes](../../16-kubernetes/README.md), [distributed systems](../../17-distributed-systems/README.md), [observability](../../18-observability/README.md), [site reliability engineering](../../19-sre/README.md), and [security](../../20-security/README.md).

## Prerequisites

- Pass the [Cloud Delivery Gate](cloud-delivery.md).
- Complete [Operate and Diagnose a Kubernetes Workload](../../labs/10-kubernetes-operations/README.md), [Investigate an OpenTelemetry Trace](../../labs/11-opentelemetry-traces/README.md), [Calculate an SLO and Run an Incident](../../labs/12-sre-slo-incident/README.md), and [Threat-Model a File Upload Service](../../labs/13-security-threat-model/README.md).
- Provide a disposable-cluster baseline based on [Multi-Tenant Kubernetes Application Platform](../../projects/06-kubernetes-platform/README.md), with telemetry or reliability evidence from [Operable Telemetry Stack](../../projects/07-telemetry-stack/README.md) or [Reliability Review and Incident Exercise](../../projects/08-reliability-exercise/README.md).
- The evaluator and candidate must verify a local, disposable cluster context and one dedicated namespace. Shared or production clusters are prohibited.

## Challenge

Deploy a namespace-scoped service with a Deployment, Service, configuration, readiness and liveness behavior, requests and limits, restricted security context, default-deny network policy, quota, disruption control, and correlated request telemetry. Define a user-centered SLI, SLO, error-budget policy, multi-window burn decision, capacity bound, and rollback trigger.

Run a healthy baseline that ties API objects, owner references, scheduler decision, pod identity, endpoints, request result, trace, metric, and event timeline together. The evaluator then selects a blind incident or compound variant from:

- [Kubernetes CrashLoopBackOff](../../incidents/07-kubernetes-crashloopbackoff/README.md);
- [bad rollout](../../incidents/06-bad-rollout/README.md);
- [retry storm](../../incidents/08-retry-storm/README.md);
- [queue overload](../../incidents/12-queue-overload/README.md);
- a readiness or Service endpoint fault from [the operations lab](../../labs/10-kubernetes-operations/README.md); or
- telemetry loss combined with one of the preceding service faults.

The candidate acts as incident commander and primary investigator. They must establish impact, assign or name roles, maintain a timestamped fact and decision log, rank hypotheses, state rollback criteria before mitigation, reduce impact with the smallest reversible change, prove recovery for a relevant SLO window, and produce a learning review. The evaluator then changes one design assumption, such as zone failure, webhook outage, quota exhaustion, certificate expiry, or a new tenant, and requests a design revision.

## Evidence packet

Include the [standard packet](../README.md#standard-evidence-packet) plus:

- cluster context and versions, namespace manifest set, policy tests, image digest, workload identity, owner references, pod UIDs, endpoints, resource and quota state, and cleanup proof;
- SLI definition, objective, error-budget calculation, burn-rate series, alert timestamp, capacity calculation, and release decision;
- sanitized trace or correlation table, metric semantics, events and logs, telemetry completeness checks, and explicit handling of missing signals;
- incident impact, roles, timeline, hypotheses, test costs, contradictions, communications, mitigation, rollback trigger, and sustained user and subsystem recovery;
- threat and trust-boundary model, abuse cases, control verification, residual risk and owner; and
- learning review separating trigger, contributing conditions, and testable prevention actions.

## Dimension requirements

- **Explain:** Trace desired state through API admission, storage, controllers, scheduler, node runtime, Service endpoints, and request telemetry. Explain partial failure, retries, SLO math, and security boundaries without claiming that one signal proves health.
- **Build:** Deliver the namespace-scoped workload, telemetry, SLO analyzer or calculation, policy checks, and recovery controls as reproducible artifacts.
- **Debug:** Diagnose the blind or compound incident from incomplete and potentially misleading evidence, including at least one rejected hypothesis.
- **Operate:** Lead the incident, protect tenants and accepted work, use bounded mitigation and rollback, verify recovery over the declared window, and clean the namespace and local forwarding processes.
- **Design:** Revise workload, failure-domain, observability, capacity, security, and recovery choices under the evaluator's changed assumption, with costs and ownership explicit.

## Evaluator instructions

Choose a scenario whose solution the candidate has not read. Follow the academy method in [Incident Drill Academy](../../incidents/README.md): reveal evidence in timeline order, require a rollback trigger before mitigation, and challenge broad restarts, disabled policy, or capacity-only fixes. For a compound incident, ensure one plausible first hypothesis is wrong.

Observe the context check, baseline, incident, rollback or correction, and cleanup. Require one live manifest, query, alert, or policy change and a rerun. Do not equate pod `Running`, a successful rollout command, or one green request with recovery.

Critical requirements:

- all mutations remain within the verified namespace and no privileged workload is introduced;
- the SLI and burn calculation detect missing telemetry rather than treating it as success;
- retry, queue, and resource behavior remain bounded under overload;
- mitigation states blast radius, reversibility, owner, and rollback trigger; and
- recovery is proven at user, workload, dependency, and telemetry layers for a relevant cycle.

## Review prompts

1. Which controller owns each observed state transition, and what does `Running` fail to prove?
2. Why can a ready pod be absent from useful Service endpoints, or an endpoint still fail a request?
3. Which signal defines user impact, and how does missing telemetry affect the SLI?
4. How do retry and queue policies alter offered load and recovery time?
5. Which observation discriminated the causal fault from the misleading symptom?
6. What did the mitigation risk, and what exact evidence would have triggered rollback?
7. Which trust boundary or authority remains exposed after the correction?
8. How does the design change under the evaluator's new failure-domain or tenancy assumption?

## Pass and rework

Pass requires at least 2 in every dimension under [the rubric](../rubric.md), all critical requirements, and no score below 2 in the [incident academy completion rubric](../../incidents/README.md#completion-rubric). A candidate who restores service but cannot establish cause, safe mitigation, or sustained recovery receives Rework.

Rework for Debug or Operate uses a different incident. SLO gaps require recalculation on a fresh synthetic interval including missing data. Security gaps require a new abuse case and control test. Design gaps require a revised failure drill and acceptance criterion, not only an updated diagram.

## Remediation

Use [Kubernetes service and operations](../../16-kubernetes/03-service-and-operations.md), [idempotency and retries](../../17-distributed-systems/06-idempotency-and-retries.md), [instrumentation and diagnosis](../../18-observability/07-instrumentation-and-diagnosis.md), [incident command](../../19-sre/03-incident-command.md), or [security incident response](../../20-security/07-security-incident-response.md). Repeat the associated lab or incident with a new fixture before reassessment.
