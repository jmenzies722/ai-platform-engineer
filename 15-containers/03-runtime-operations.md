# Runtime networking, storage, and security

Operating containers means debugging across application, container, runtime, and host boundaries.

## Why it matters

An image can be correct while the process is unreachable, read-only, starved, or running with dangerous authority. Runtime configuration is part of the workload's security and reliability contract.

## How it works

Bridge networking gives a container an isolated interface and address; published ports install host forwarding. Binding inside the container to `127.0.0.1` does not accept traffic arriving on its container interface. Volumes persist outside the writable layer; bind mounts expose chosen host paths.

Run with a non-root UID, drop capabilities, enable a read-only root filesystem where possible, and mount only required paths. Pass secrets at runtime through a dedicated mechanism, never bake them into images or ordinary environment dumps. Set CPU, memory, and process limits from measured behavior.

The effective runtime specification combines image defaults with command-line or orchestrator settings. Entrypoint and command determine PID 1 and signal delivery. Health checks should exercise readiness without causing load or mutating state. Restart policy handles process failure but can create evidence-destroying loops; it cannot repair bad configuration or unavailable dependencies.

Logs written to stdout and stderr are captured by a logging driver with its own buffering, rotation, backpressure, and disk behavior. Runtime events connect lifecycle transitions to timestamps. The host remains part of diagnosis: disk, memory, conntrack, kernel, daemon, and neighboring workloads can fail a healthy image.

## See it yourself

Inspect process, command, mounts, network, port bindings, limits, restart count, health, security settings, and logs with `docker inspect`, `docker top`, `docker stats`, and runtime events. Connect each observed value to image or run configuration. Predict evidence for process crash, health failure, OOM, and manual stop before inducing them locally.

## Where it shows up

Compose, CI runners, managed container services, and Kubernetes translate higher-level declarations into these runtime choices. Production records should connect image digest, runtime spec, secret and config versions, node, start and stop reason, health, resource use, and user SLI.

## When it breaks

Port publishing cannot fix the wrong listen address. UID or LSM label mismatches deny volume writes. Unbounded logs fill disks. Health checks that test only process existence route traffic to broken behavior, while aggressive checks cause restart storms. Shell entrypoints swallow signals. DNS, conntrack, and ephemeral-port pressure break new connections. An engine restart changes process state while volumes remain.

Preserve the failed container, immutable digest, inspect output, exit and OOM state, logs, events, mounts, listeners, cgroup counters, and host pressure before recreation. Change one boundary and verify the user path.

## Practice

**Observe:** create an evidence bundle for one runtime including artifact, process, limits, storage, network, security, health, logging, and host context.

**Build:** run HTTP as non-root with read-only root, tmpfs scratch, bounded resources, dropped capabilities, and localhost-only publication. Explain every exception.

**Break safely:** use wrong listen address, unwritable mount, failed health endpoint, and low memory. Completion means each layer is distinguished before restart and the repair preserves hardening.

## Check yourself

1. What survives removal: writable layer or named volume?
2. Why is a published host port not sufficient for reachability?

## Sources

### REQUIRED
- [Docker networking overview](https://docs.docker.com/engine/network/)

### RECOMMENDED
- [Docker storage overview](https://docs.docker.com/engine/storage/)

### DEEP DIVE
- [CNCF Cloud Native Security whitepaper](https://github.com/cncf/tag-security/blob/main/security-whitepaper/v2/cloud-native-security-whitepaper.md)

## Next

[Container networks and persistent storage](04-network-and-storage.md)
