# Ownership, policy, and control-plane operations

A production control plane must make ownership, deletion, policy, tenancy, and its own failure modes explicit.

## Why it matters

Creating resources is easy compared with safely upgrading, isolating tenants, recovering state, and deleting external dependencies after partial failure.

## How it works

Assign one controller authority over each field and external object. Owner references or equivalent metadata describe lifecycle. Finalizers block API deletion while a controller performs idempotent external cleanup; deletion timestamps make termination visible.

Enforce authentication, authorization, admission policy, quotas, and tenant isolation at boundaries. Separate control-plane availability from data-plane continuity. Back up durable state, test restoration, expose queue depth and reconcile latency, and canary controller upgrades. Record audit events without leaking secrets.

## See it yourself

During deletion, the API marks a resource terminating. The controller deletes the external database, confirms absence, then removes its finalizer. If provider access is permanently lost, an operator needs an audited break-glass decision.

## Where it shows up

Kubernetes operators, cloud management planes, internal provisioning services, GitOps controllers, and SaaS tenant automation.

## When it breaks

Dead finalizers block deletion, shared credentials erase tenant boundaries, incompatible controller versions corrupt status, or a queue backlog hides widespread staleness.

## Practice

Write a runbook for a stuck finalizer. Require external-state evidence, impact analysis, approval, audit record, and orphan follow-up before forced removal.

## Check yourself

1. Why is force-removing a finalizer risky?
2. Which signals reveal a control plane that is alive but not converging?

## Sources

### REQUIRED
- [Kubernetes finalizers](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/)

### RECOMMENDED
- [Kubernetes API access control](https://kubernetes.io/docs/reference/access-authn-authz/)

### DEEP DIVE
- [CNCF Operator whitepaper](https://github.com/cncf/tag-app-delivery/blob/main/operator-wg/whitepaper/Operator-WhitePaper_v1-0.md)

## Next

[AI Foundations](../24-ai-foundations/README.md)
