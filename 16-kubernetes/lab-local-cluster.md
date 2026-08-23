# Lab: diagnose a local Kubernetes workload

Use kind, minikube, or another disposable cluster. Confirm context first; never run this lab against production.

## Create the workload

```bash
kubectl config current-context
kubectl create namespace curriculum-k8s
kubectl -n curriculum-k8s create deployment web --image=nginx:alpine --replicas=2
kubectl -n curriculum-k8s expose deployment web --port=80 --target-port=8080
kubectl -n curriculum-k8s rollout status deployment/web --timeout=90s
```

The Service deliberately points to the wrong target port.

## Gather evidence

```bash
kubectl -n curriculum-k8s get deployment,replicaset,pod,service,endpointslice -o wide
kubectl -n curriculum-k8s describe service web
kubectl -n curriculum-k8s get events --sort-by=.lastTimestamp
kubectl -n curriculum-k8s run client --rm -it --restart=Never --image=curlimages/curl -- curl -v --max-time 3 http://web/
```

Before changing anything, answer:

- Which controller owns each Pod?
- Does the Service have endpoints?
- Which port does Nginx listen on?
- Is this discovery, selection, policy, or application reachability failure?

## Repair and observe reconciliation

```bash
kubectl -n curriculum-k8s patch service web --type merge -p '{"spec":{"ports":[{"port":80,"targetPort":80}]}}'
kubectl -n curriculum-k8s run client --rm -it --restart=Never --image=curlimages/curl -- curl --fail http://web/
kubectl -n curriculum-k8s delete pod -l app=web
kubectl -n curriculum-k8s get pods --watch
```

Stop the watch after replacements become Ready. Explain why the Deployment still has two replicas and why the Service identity survived.

## Cleanup

```bash
kubectl delete namespace curriculum-k8s
```

If you created a local cluster solely for this lab, delete it with that tool's documented command.
