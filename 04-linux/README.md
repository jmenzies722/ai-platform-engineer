# 04 — Linux

Operate Linux by following kernel-visible state rather than memorizing rescue commands. The sequence begins with files and processes, builds safe shell habits, then adds identity, software installation boundaries, networking, and evidence-led diagnosis.

## What you will learn

By the end, you can inspect path and permission decisions, control only processes you own, compose safe shell commands, reason about users and package provenance, trace a local network path, and build a bounded incident snapshot before changing the host. Distribution details vary; the underlying interfaces and evidence habits transfer.

## Lessons

1. [Filesystem and Permissions](./01-filesystem-and-permissions.md)
2. [Processes, Signals, and Services](./02-processes-signals-and-services.md)
3. [Shell Composition and Safe Automation](./03-shell-composition-and-safe-automation.md)
4. [Users, Privilege, and Software Installation](./04-users-privilege-and-software-installation.md)
5. [Linux Networking and Name Resolution](./05-linux-networking-and-name-resolution.md)
6. [Observability, Logs, and Resource Diagnosis](./06-observability-logs-and-resource-diagnosis.md)

## Practice

[Inspect and Control One Process](./lab-process-control.md) after lesson 2. After lesson 6, repeat it while producing the identity, state, resource, event, and cleanup evidence bundle defined there. Lesson practices add temporary filesystem, account-identity, and loopback-network experiments.

Practice is part of the path, not an optional recap. Predict first, work only in disposable or explicitly scoped resources, compare expected and actual observations, and perform the documented cleanup.

## Ready to continue

Continue when you can explain directory traversal, identify a process before signaling, quote arbitrary data safely, distinguish real and effective identity, identify which package manager owns a file, separate DNS from routing and listening, and collect a minimal host snapshot without exposing secrets or applying speculative fixes.

## Next

Start with [Filesystem and Permissions](./01-filesystem-and-permissions.md).
