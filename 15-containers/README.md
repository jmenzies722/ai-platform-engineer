# 15 — Containers

A container is an ordinary host process isolated and constrained by Linux, started from a content-addressed filesystem image.

## What you will learn

- Separate images, containers, registries, runtimes, and host kernels.
- Build reproducible, small images and run them with explicit limits.
- Predict network and storage behavior across host and container boundaries.
- Harden runtime authority and debug process, resource, network, and filesystem failures from evidence.

## Lessons

1. [Isolation and resource control](01-isolation-and-resources.md)
2. [OCI images and reproducible builds](02-images-and-builds.md)
3. [Runtime networking, storage, and security](03-runtime-operations.md)
4. [Container networks and persistent storage](04-network-and-storage.md)
5. [Runtime hardening and image trust](05-security-and-trust.md)
6. [Evidence-driven container debugging](06-debugging.md)

## Practice

Complete the [container failure-analysis lab](lab-container-inspection.md) with Docker or a compatible OCI tool. You will preserve evidence across startup, reachability, resource, persistence, and hardening tests.

## Ready to continue

You can connect namespaces and cgroups to observed process behavior, identify an image by digest, predict network and volume behavior, harden runtime authority, and diagnose failures without replacing the evidence.

## Next

Continue to [Kubernetes](../16-kubernetes/README.md).
