# Services, configuration, and failure diagnosis

Kubernetes networking and configuration connect disposable Pods to stable consumers, but each abstraction adds evidence you must inspect.

## Why it matters

Most cluster incidents are not solved by restarting everything. Labels, endpoints, ports, DNS, policies, configuration, and application listeners must agree.

## How it works

Each Pod receives an address. A Service selects ready Pods and exposes a stable virtual IP and DNS name. The Service `port` is the client-facing port; `targetPort` reaches the Pod listener. EndpointSlices show actual selected backends.

ConfigMaps hold non-secret configuration; Secrets are API objects and require encryption, access control, and careful delivery. Neither automatically makes an application reload values. PersistentVolumeClaims request storage from a class; volume semantics still come from the storage system.

Debug from intent outward: inspect object spec and status, events, selected Pods, EndpointSlices, DNS, connectivity, logs, and node state.

## See it yourself

Run `kubectl get service,endpointslice -l app=demo -o wide`. Change a Service selector so no Pod matches and observe that DNS remains while endpoints disappear.

## Where it shows up

ClusterIP Services support internal discovery, Ingress or Gateway implementations route external HTTP traffic, and NetworkPolicies restrict permitted Pod flows where the network plugin enforces them.

## When it breaks

Selector labels drift, `targetPort` is wrong, Pods listen only on loopback, readiness removes every endpoint, or a default-deny policy omits DNS. Secret values leak through logs or shell history.

## Practice

Diagnose a Service with no response using only `get`, `describe`, `logs`, and a disposable client Pod. Record evidence before changing anything.

## Check yourself

1. Where can you see the real Service backends?
2. Why does creating a Secret not make a plaintext value safe?

## Sources

### REQUIRED
- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)

### RECOMMENDED
- [Debug Services](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/)

### DEEP DIVE
- [Kubernetes security checklist](https://kubernetes.io/docs/concepts/security/security-checklist/)

## Next

[Persistent storage and data workloads](04-storage-and-data.md)
