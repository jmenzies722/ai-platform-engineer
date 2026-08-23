# 15 — Containers

A container is an ordinary host process isolated and constrained by Linux, started from a content-addressed filesystem image.

## What you will learn

- Separate images, containers, registries, runtimes, and host kernels.
- Build reproducible, small images and run them with explicit limits.
- Debug process, network, filesystem, and supply-chain failures.

## Lessons

1. [Isolation and resource control](01-isolation-and-resources.md)
2. [OCI images and reproducible builds](02-images-and-builds.md)
3. [Runtime networking, storage, and security](03-runtime-operations.md)

## Practice

Complete the [local container inspection lab](lab-container-inspection.md) with Docker or a compatible OCI tool.

## Ready to continue

You can explain why containers are not virtual machines, inspect image layers, predict port and volume behavior, and run a workload without root with resource limits.

## Next

Continue to [Kubernetes](../16-kubernetes/README.md).
