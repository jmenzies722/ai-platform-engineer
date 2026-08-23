# Runtime networking, storage, and security

Operating containers means debugging across application, container, runtime, and host boundaries.

## Why it matters

An image can be correct while the process is unreachable, read-only, starved, or running with dangerous authority. Runtime configuration is part of the workload's security and reliability contract.

## How it works

Bridge networking gives a container an isolated interface and address; published ports install host forwarding. Binding inside the container to `127.0.0.1` does not accept traffic arriving on its container interface. Volumes persist outside the writable layer; bind mounts expose chosen host paths.

Run with a non-root UID, drop capabilities, enable a read-only root filesystem where possible, and mount only required paths. Pass secrets at runtime through a dedicated mechanism, never bake them into images or ordinary environment dumps. Set CPU, memory, and process limits from measured behavior.

## See it yourself

Inspect a running container's process, mounts, network, port bindings, limits, health, and logs with `docker inspect`, `docker top`, and `docker stats`. Connect each observed value to its run option.

## Where it shows up

Compose, CI runners, managed container services, and Kubernetes translate higher-level declarations into these runtime choices.

## When it breaks

Port publishing cannot fix the wrong listen address. UID mismatches deny volume writes. Unbounded logs fill disks. Health checks that test only process existence route traffic to a broken dependency path.

## Practice

Run a simple HTTP image as non-root with a read-only root filesystem, temporary writable directory, memory limit, and localhost-only published port. Explain every exception you add.

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

[Kubernetes](../16-kubernetes/README.md)
