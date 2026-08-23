# Identity, policy, and workload security

Kubernetes security is a chain of authenticated identities, authorization, admission, workload isolation, secret handling, and network policy; no single control makes a cluster safe.

## Why it matters

A compromised Pod can call the API with its service account, read mounted credentials, reach neighboring services, or exploit excessive runtime authority. Cluster-admin access or privileged workloads can collapse most namespace boundaries.

## How it works

The API server authenticates a request, RBAC authorizes verb, resource, namespace, and sometimes name, and admission validates or mutates the object. ServiceAccounts identify workloads; disable automatic token mounting when API access is unnecessary and use short-lived projected tokens with intended audiences.

Pod Security Standards define privileged, baseline, and restricted profiles. Security contexts set UID, group, privilege escalation, capabilities, seccomp, and filesystem behavior. NetworkPolicy selects Pods and permits ingress or egress, but enforcement depends on the network plugin and policies are additive. Default-deny requires explicit DNS and dependency flows.

Secrets are base64-encoded API data, not inherently encrypted. Protect etcd at rest, RBAC, delivery paths, logs, backups, and rotation. Prefer external workload identity over distributing durable cloud credentials.

## See it yourself

In a disposable namespace, run `kubectl auth can-i --as=system:serviceaccount:NAME:default list secrets -n NAME` and inspect a Pod's service account, token automount, security context, and effective network policies. Predict the authorization result before running it. `can-i` evaluates authorization, not whether admission or network controls make an operation safe.

## Where it shows up

A web Deployment uses a dedicated ServiceAccount permitted to read one ConfigMap but no Secrets, runs as non-root under restricted policy, has all capabilities dropped, and can reach only DNS and one backend. Cloud API calls use federated workload identity with bounded audience and subject.

## When it breaks

RBAC wildcards grow through aggregation. A default ServiceAccount is shared across unrelated Pods. A privileged DaemonSet mounts the host filesystem. Network policy exists but the plugin does not enforce it. Secret data appears in manifests, audit logs, or shell history. Namespace administrators can create workloads that escalate through node access.

Preserve the denied request identity, verb, resource, namespace, RBAC bindings, admission decision, Pod spec, runtime settings, and network-policy selection. Do not resolve incidents by granting cluster-admin.

## Practice

**Observe:** build an identity and authority map for one workload from human deployer through controller, ServiceAccount, API verbs, runtime privileges, secrets, and network peers.

**Build:** deploy a restricted Pod with a dedicated ServiceAccount, no automatic token unless needed, read-only root, no capabilities, default-deny network policy, and minimal egress.

**Break safely:** attempt a forbidden Secret read, privileged Pod creation, and unapproved network connection. Completion means each fails at the intended layer with auditable evidence and required application traffic still works.

## Check yourself

1. What question does RBAC answer that admission does not?
2. Why is base64 not a Secret protection control?
3. When does a NetworkPolicy have no effect?
4. Which workload settings reduce damage after code execution?

## Sources

### REQUIRED

- [Kubernetes security checklist](https://kubernetes.io/docs/concepts/security/security-checklist/)

### RECOMMENDED

- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)

### DEEP DIVE

- [Kubernetes authorization overview](https://kubernetes.io/docs/reference/access-authn-authz/authorization/)

## Next

[Autoscaling, upgrades, and cluster operations](06-scaling-and-upgrades.md)
