# Tenancy, governance, and cost

Shared AI platforms must isolate tenants, enforce policy, and make scarce-resource consumption attributable.

## Why it matters

One workload can exhaust accelerators, expose another tenant's data, or create spend no owner can explain.

## How it works

Identity flows into authorization, namespaces, quotas, network boundaries, secret scope, and audit logs. Policy engines validate requests before execution. Metering attributes accelerator time, storage, network, tokens, and reserved capacity to owners. Quotas bound harm; budgets create feedback; neither replaces capacity planning.

Isolation is layered because each mechanism has a different boundary. Scheduler quotas control allocation, network policy controls reachability, workload identity controls API calls, and encryption protects stored data. Cost attribution follows the same trusted identity through requests and derived resources. Labels supplied by tenants are useful dimensions but cannot be the authority for billing or access.

## See it yourself

Trace tenant A requesting two GPUs: authenticated identity authorizes a namespace, policy caps the shape, scheduler records allocation, workload identity accesses one dataset, and meter attributes GPU-seconds to A. Replace identity after admission with a shared service account. The resulting audit and bill become ambiguous, proving identity continuity is part of both security and economics.

## Where it shows up

In a shared model gateway, tenant identity selects quotas, allowed models, log-retention policy, and cost center. Prompt bodies stay out of ordinary billing logs; token counts and model IDs remain. Per-tenant concurrency prevents one burst from exhausting the global fleet, while a global reserve protects system recovery.

## When it breaks

Shared credentials erase attribution, labels are trusted as identity, quotas ignore secondary resources, and logs contain sensitive prompts. For suspected cross-tenant behavior, first preserve authenticated principal, authorization decision, resource namespace, network flow, and audit event. For cost anomalies, reconcile metered usage with scheduler allocation and gateway calls before changing prices or quotas.

## Practice

**Build:** define identity, isolation, quota, metering, and redaction for two teams sharing GPUs. **Break:** use a shared credential and exhaust storage while staying within GPU quota; show missing attribution and secondary-resource failure. **Explain back:** distinguish quota, budget, and capacity using auditable events.

## Check yourself

1. Why are namespaces insufficient isolation?
2. What should audit logs omit?
3. How do quota and budget differ?

## Sources

### REQUIRED

- [Kubernetes multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/)

### RECOMMENDED

- [Open Policy Agent documentation](https://www.openpolicyagent.org/docs/latest/)

### DEEP DIVE

- [NIST Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)

## Next

Continue to [Operating the platform as a product](03-operating-the-platform-as-a-product.md).
