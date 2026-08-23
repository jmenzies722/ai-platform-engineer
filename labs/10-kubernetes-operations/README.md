# Lab: Operate and Diagnose a Kubernetes Workload

Deploy a namespace-scoped service to a disposable local cluster, inspect desired and observed state, break readiness, and prove recovery through Kubernetes evidence.

## Prerequisites

- A disposable `kind` or `minikube` cluster
- `kubectl` compatible with the cluster
- Permission to create and delete namespace `lab-operations`

## Safety

Confirm the context is local and disposable. Stop if `kubectl config current-context` names a shared or production cluster. Use only namespace `lab-operations`; never use `--all-namespaces`, cluster-scoped mutations, force deletion, or privileged pods.

## Setup and baseline

```bash
mkdir -p .work
kubectl config current-context | tee .work/context.txt
kubectl cluster-info | tee .work/cluster-info.txt
kubectl create namespace lab-operations
kubectl auth can-i create deployments -n lab-operations
kubectl auth can-i delete namespaces
```

Write down the expected relationships among Deployment, ReplicaSet, Pod, Service, endpoint, readiness, and liveness.

## Tasks

1. Create `.work/app.yaml` containing a two-replica `nginx:1.27-alpine` Deployment with CPU/memory requests and limits, non-root-compatible security settings where supported, readiness probe on `/`, and a ClusterIP Service on port 80.
2. Apply it with `kubectl apply -f .work/app.yaml`; wait with:

   ```bash
   kubectl rollout status deployment/lab-web -n lab-operations --timeout=90s
   kubectl wait --for=condition=Ready pod -l app=lab-web -n lab-operations --timeout=90s
   ```

3. Capture `get deployment,rs,pod,service,endpoints -o wide`, `describe deployment`, one pod description, and namespace events sorted by creation timestamp.
4. Port-forward the Service to `127.0.0.1:58000`, request it with a three-second timeout, then stop the exact port-forward process.
5. Delete one pod and observe controller replacement. Explain why pod identity changes while desired replica count remains.

## Evidence to keep

Keep context, client/server versions, manifest, rollout conditions, owner references, pod UIDs, endpoint addresses, events, resource constraints, request result, and a desired-versus-observed state narrative.

## Failure injection

Patch the readiness path to `/not-ready`:

```bash
kubectl patch deployment lab-web -n lab-operations --type=strategic \
  -p '{"spec":{"template":{"spec":{"containers":[{"name":"nginx","readinessProbe":{"httpGet":{"path":"/not-ready","port":80}}}]}}}}'
kubectl rollout status deployment/lab-web -n lab-operations --timeout=45s || true
kubectl get pods,endpoints -n lab-operations -o wide
```

Expected symptom: containers can remain running while pods are not Ready and Service endpoints disappear. Diagnose probes and events, then reapply the known-good manifest and prove endpoints return.

## Cleanup

```bash
kubectl delete namespace lab-operations --wait=true --timeout=90s
kubectl get namespace lab-operations 2>&1 | tee .work/cleanup.txt || true
rm -rf .work
```

## Rubric

- 2 points: verifies local context and uses namespace-scoped resources
- 3 points: relates controllers, pods, readiness, Service, and endpoints
- 2 points: diagnoses and reverses readiness failure from evidence
- 2 points: observes reconciliation after pod deletion
- 1 point: confirms namespace deletion and stops port-forwarding

## Sources

- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Configure probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [Services](https://kubernetes.io/docs/concepts/services-networking/service/)
