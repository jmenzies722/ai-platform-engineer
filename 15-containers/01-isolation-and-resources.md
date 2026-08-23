# Isolation and resource control

A container is a process whose view and resource access are shaped by the host kernel.

## Why it matters

Containers start quickly and package dependencies well, but they share a kernel. Misunderstanding that boundary leads to weak isolation, runaway memory, confusing process behavior, and unsafe privileges.

## How it works

Linux namespaces isolate views of process IDs, mounts, networks, hostnames, users, and other resources. Control groups account for and limit CPU, memory, and process usage. Capabilities split root powers into narrower privileges. Seccomp filters system calls; Linux security modules add policy.

The runtime creates namespaces and cgroups, mounts an image root filesystem, applies credentials and limits, then starts the declared process. PID 1 must reap children and handle termination signals. A container exits when its main process exits.

Namespace membership is per process and can be inspected through `/proc`. User namespaces map container IDs to different host IDs; they reduce host authority but do not remove kernel sharing. Cgroup v2 organizes processes hierarchically and exposes CPU weight and quota, memory current and maximum, OOM events, and process limits. CPU limits throttle; memory limits can kill; requests are a scheduler concept supplied by higher-level systems, not a Linux isolation primitive.

Capabilities, seccomp, and security modules constrain different surfaces. Dropping capabilities narrows privileged operations, seccomp filters system calls, and SELinux or AppArmor constrains object access. None compensates for a privileged container sharing host namespaces and devices.

## See it yourself

Run a disposable shell and inspect `/proc/1/status`, namespace links, mounts, and cgroup files. Compare its PID from inside with `docker inspect` and host process evidence. Apply a CPU and memory limit and predict changed cgroup values. The views differ; the process remains scheduled by the host kernel. A different PID view proves namespace isolation, not a separate kernel.

## Where it shows up

CI jobs, Kubernetes Pods, local development, and serverless container products depend on these primitives with different surrounding controls. A Pod may share one network namespace across containers while keeping separate mount views and cgroups. Rootless engines add user-namespace and daemon isolation but still require secure host configuration.

## When it breaks

Running privileged, mounting host devices, or sharing host PID defeats important boundaries. Missing memory limits lets one workload pressure the host; a low limit triggers OOM, while a low CPU quota produces throttling and latency. Process trees leak zombies when PID 1 does not reap. Signals never reach the application through a shell-form entrypoint. Writing durable data to the writable layer loses it on replacement.

Distinguish failures with runtime exit state, cgroup events, throttling counters, host pressure, process trees, signal handling, namespace membership, and mount source. Exit code alone is not enough.

## Practice

**Observe:** map PID, network, mount, user, and cgroup namespaces for a disposable process and identify the shared kernel.

**Build:** run a signal-aware process with CPU, memory, and PID limits, non-root identity, dropped capabilities, and default seccomp. Record effective settings.

**Break safely:** exceed memory, saturate CPU, and terminate PID 1 through both shell-form and exec-form commands. Completion means OOM, throttling, and signal-forwarding failures are distinguished from evidence.

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
