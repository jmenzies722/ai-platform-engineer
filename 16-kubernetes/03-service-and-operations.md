# Services, configuration, and failure diagnosis

Kubernetes networking and configuration connect disposable Pods to stable consumers, but each abstraction adds evidence you must inspect.

## Why it matters

Most cluster incidents are not solved by restarting everything. Labels, endpoints, ports, DNS, policies, configuration, and application listeners must agree.

## How it works

Each Pod receives an address. A Service selects ready Pods and exposes a stable virtual IP and DNS name. The Service `port` is the client-facing port; `targetPort` reaches the Pod listener. EndpointSlices show actual selected backends.

ConfigMaps hold non-secret configuration; Secrets are API objects and require encryption, access control, and careful delivery. Neither automatically makes an application reload values. PersistentVolumeClaims request storage from a class; volume semantics still come from the storage system.

Debug from intent outward: inspect object spec and status, events, selected Pods, EndpointSlices, DNS, connectivity, logs, and node state.

The cluster network model gives each Pod a routable address through a CNI implementation. kube-proxy or an alternative data plane implements Service forwarding. CoreDNS answers service discovery. Ingress or Gateway API resources express traffic intent, while a controller realizes load balancers and routes. NetworkPolicy is additive and depends on plugin enforcement.

Configuration delivery has lifecycle semantics. Environment values are fixed at process start; mounted ConfigMap and Secret projections update eventually but applications must reload them. Rollouts should carry config identity. Secrets need least-privilege API access, encryption at rest, careful logs, rotation, and short-lived external identity where possible.

## See it yourself

Run `kubectl get service,endpointslice -l app=demo -o wide`. Change a selector so no Pod matches and observe that DNS and virtual IP remain while endpoints disappear. From a disposable client, test DNS, Service port, endpoint address, and application path separately. This isolates network layers but does not prove every client or policy path.

## Where it shows up

ClusterIP Services support internal discovery, headless Services expose endpoint records, and Ingress or Gateway implementations route external traffic. NetworkPolicies restrict permitted Pod flows where enforced. Production operations connect route identity, TLS certificate, Service, EndpointSlice, Pod readiness, config revision, logs, and user SLI.

## When it breaks

Selector labels drift, `targetPort` is wrong, Pods listen only on loopback, readiness removes every endpoint, CoreDNS is unavailable, or a default-deny policy omits DNS. Ingress references the wrong Service or TLS secret. Configuration changes do not reload. Secret values leak through manifests, logs, shell history, or broad RBAC. Node conntrack or plugin failure affects only some paths.

Start with exact name, namespace, source, destination, port, protocol, and time. Preserve object generations, EndpointSlices, DNS answer, connection error, policy selection, listener, application logs, and node scope. Restarting everything erases the distinction.

## Practice

**Observe:** trace a production-shaped request from DNS through route, Service, EndpointSlice, readiness, Pod listener, config, and dependency.

**Build:** deploy a Service with explicit ports, readiness, versioned configuration, TLS or gateway plan, and default-deny policy allowing only required flows.

**Break safely:** misalign selector, target port, readiness, DNS egress, and mounted configuration one at a time. Completion means evidence identifies the exact layer before repair and a user request verifies recovery.

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
