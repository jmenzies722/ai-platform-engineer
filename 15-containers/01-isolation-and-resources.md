# Isolation and resource control

A container is a process whose view and resource access are shaped by the host kernel.

## Why it matters

Containers start quickly and package dependencies well, but they share a kernel. Misunderstanding that boundary leads to weak isolation, runaway memory, confusing process behavior, and unsafe privileges.

## How it works

Linux namespaces isolate views of process IDs, mounts, networks, hostnames, users, and other resources. Control groups account for and limit CPU, memory, and process usage. Capabilities split root powers into narrower privileges. Seccomp filters system calls; Linux security modules add policy.

The runtime creates namespaces and cgroups, mounts an image root filesystem, applies credentials and limits, then starts the declared process. PID 1 must reap children and handle termination signals. A container exits when its main process exits.

## See it yourself

Run a disposable shell and inspect `/proc/1/status`, mounts, and cgroup data. Compare its PID from inside with `docker inspect` on the host. The views differ; the process is still scheduled by the host kernel.

## Where it shows up

CI jobs, Kubernetes Pods, local development, and serverless container products all depend on these primitives with different surrounding controls.

## When it breaks

Running privileged removes important boundaries. Missing memory limits lets one workload pressure the host; hitting a limit can trigger an OOM kill. Writing durable data only to the writable layer loses it when the container is replaced.

## Practice

Run a process with one CPU and a small memory limit. Inspect its cgroup limits and observe its exit status when memory is exceeded.

## Check yourself

1. Which isolation boundary do containers normally share?
2. Why does PID 1 behavior matter?

## Sources

### REQUIRED
- [Docker container security](https://docs.docker.com/engine/security/)

### RECOMMENDED
- [Linux namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html)

### DEEP DIVE
- [OCI runtime specification](https://github.com/opencontainers/runtime-spec)

## Next

[OCI images and reproducible builds](02-images-and-builds.md)
