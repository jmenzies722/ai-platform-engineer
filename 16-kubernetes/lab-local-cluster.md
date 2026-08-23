# Lab: operate and diagnose a local Kubernetes workload

Use kind, minikube, or another disposable cluster. Confirm context first; never run this lab against production. The exercise preserves API, scheduling, network, storage, security, rollout, and scaling evidence before repair.

## Safety and baseline

Create an evidence directory. Stop if the context or cluster is not explicitly disposable.

```bash
kubectl config current-context
kubectl cluster-info
rm -rf /tmp/curriculum-k8s-evidence
mkdir /tmp/curriculum-k8s-evidence
kubectl version -o yaml > /tmp/curriculum-k8s-evidence/version.yaml
kubectl create namespace curriculum-k8s
```

Apply a restricted workload:

```bash
kubectl -n curriculum-k8s create deployment web --image=nginx:alpine --replicas=2
kubectl -n curriculum-k8s set resources deployment/web \
  --requests=cpu=25m,memory=32Mi --limits=cpu=200m,memory=128Mi
kubectl -n curriculum-k8s patch deployment web --type merge -p \
  '{"spec":{"template":{"spec":{"securityContext":{"seccompProfile":{"type":"RuntimeDefault"}},"containers":[{"name":"nginx","securityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"],"add":["NET_BIND_SERVICE"]}},"readinessProbe":{"httpGet":{"path":"/","port":80},"initialDelaySeconds":2,"periodSeconds":2}}]}}}}'
kubectl -n curriculum-k8s expose deployment web --port=80 --target-port=8080
kubectl -n curriculum-k8s rollout status deployment/web --timeout=90s
```

The Service deliberately points to the wrong target port. The capability exception supports the low listener port; the lab later asks you to redesign or justify it.

## Trace API and controller ownership

```bash
kubectl -n curriculum-k8s get deployment web -o yaml > /tmp/curriculum-k8s-evidence/deployment.yaml
kubectl -n curriculum-k8s get pods -o json > /tmp/curriculum-k8s-evidence/pods.json
kubectl -n curriculum-k8s get deployment,replicaset,pod,service,endpointslice -o wide
kubectl -n curriculum-k8s describe deployment web
```

Identify spec, status, generation, observed generation, managed fields, owner references, ReplicaSet revision, Pod service account, node binding, requests, limits, probes, and effective security context. Delete one Pod and watch reconciliation replace it. Explain why desired replicas did not change.

## Diagnose the network failure before repair

```bash
kubectl -n curriculum-k8s describe service web
kubectl -n curriculum-k8s get events --sort-by=.lastTimestamp
kubectl -n curriculum-k8s run client --rm -it --restart=Never --image=curlimages/curl -- curl -v --max-time 3 http://web/
```

Before changing anything, answer:

- Which controller owns each Pod?
- Does the Service have endpoints?
- Which port does Nginx listen on?
- Is this discovery, selection, policy, or application reachability failure?

Save Service, EndpointSlice, Pod readiness, listener assumptions, client output, and events. DNS and endpoints can remain healthy while the target port is wrong.

## Repair and verify the user path

```bash
kubectl -n curriculum-k8s patch service web --type merge -p '{"spec":{"ports":[{"port":80,"targetPort":80}]}}'
kubectl -n curriculum-k8s run client --rm -it --restart=Never --image=curlimages/curl -- curl --fail http://web/
```

The successful client request, not only ready Pods, is recovery evidence.

## Exercise scheduling and disruption

Patch a disposable copy of the Deployment to request more CPU than any node provides. Record Pending status, scheduler events, node allocatable resources, selectors, taints, affinity, and quota. Repair the request rather than adding nodes blindly.

Create a PodDisruptionBudget allowing one unavailable replica. Cordon one worker and use a dry-run or approved local drain command appropriate for the cluster. Predict which Pods can move, whether local or zonal storage matters, and why a PDB does not guarantee application availability. Uncordon the worker before continuing.

## Exercise persistent storage

Check available StorageClasses:

```bash
kubectl get storageclass
```

If the local cluster has a default dynamic provisioner, create a 64 MiB claim, mount it in a disposable Pod, write a marker, delete the Pod, mount the same claim in a replacement, and verify the marker. Capture PVC, PV, StorageClass, node topology, events, and reclaim policy. Then create a claim naming a nonexistent class and diagnose why it remains Pending before deleting only that failed claim.

If no provisioner exists, perform the same prediction from object manifests and clearly mark the execution gap. Persistence across a Pod proves neither backup nor application-consistent restore.

## Exercise authorization and policy

```bash
kubectl auth can-i --as=system:serviceaccount:curriculum-k8s:default list secrets -n curriculum-k8s
kubectl -n curriculum-k8s get deployment web -o jsonpath='{.spec.template.spec.serviceAccountName}{"\n"}'
```

Record the result without reading Secret values. Create a dedicated ServiceAccount with no extra RBAC and update the Deployment. Attempt a forbidden API read from that identity. Review namespace Pod Security labels and whether the cluster's network plugin enforces NetworkPolicy. Apply default-deny only after writing explicit DNS and required web-flow policy, then prove allowed and denied paths from disposable clients.

## Exercise scaling and rollout

If Metrics Server is available, create an HPA with a small maximum, generate bounded local load, and trace metric timestamp, current replicas, desired replicas, scheduler events, readiness, EndpointSlices, and response success. If it is unavailable, preserve the missing-metrics HPA condition as the intended failure and do not install cluster-wide components solely for the lab.

Roll out a deliberately nonexistent image tag:

```bash
kubectl -n curriculum-k8s set image deployment/web nginx=nginx:this-tag-must-not-exist
kubectl -n curriculum-k8s rollout status deployment/web --timeout=30s
kubectl -n curriculum-k8s get pods,replicasets
kubectl -n curriculum-k8s get events --sort-by=.lastTimestamp
```

Verify whether the old ReplicaSet still serves traffic, then use `kubectl rollout undo deployment/web` and prove recovery with a client request. Explain why rollback may be unsafe for a schema change.

## Upgrade readiness review

Without changing cluster version, inventory node, control-plane, kubelet, CNI, CSI, ingress, metrics, CRD, webhook, and deprecated-API compatibility. Write a canary-node upgrade plan with version-skew checks, backup or recovery evidence, drain constraints, PDB review, storage topology, guardrail SLIs, pause criteria, and roll-forward path.

## Completion criteria

The lab passes when a reviewer can trace one Pod from API intent through controllers, scheduler, kubelet, readiness, EndpointSlice, and Service; diagnose network and scheduling failures from preserved evidence; verify claim persistence without overstating durability; demonstrate least authority and a denied path; explain HPA evidence; recover a failed rollout; and review a bounded upgrade plan.

## Cleanup

```bash
kubectl delete namespace curriculum-k8s
rm -rf /tmp/curriculum-k8s-evidence
```

If you created a local cluster solely for this lab, delete it with that tool's documented command.
