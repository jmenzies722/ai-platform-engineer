# Containers

A container packages a program with its environment while isolating its processes on a shared operating-system kernel.

## Why it matters

**Prerequisite:** [DevOps](./11-devops.md).

Applications installed directly on mutable hosts accumulated hidden dependencies and environment drift. Linux isolation primitives already separated processes; layered images and standard runtimes packaged those primitives into a repeatable unit.

A container is still a host process, not a small virtual machine. Portability improved, while image supply chains, shared-kernel risk, persistent data, device access, and fleet scheduling became visible problems.

## How it works

A container is a Linux process with restricted views, resource controls, and a prepared root filesystem—not a miniature VM.

A runtime unpacks image layers, constructs mounts, creates namespaces and cgroups, applies credentials and capabilities, then starts the configured process. Registries distribute content-addressed manifests and blobs.

Namespaces isolate views; cgroups account and limit resources. Images are immutable content, but writable container layers are ephemeral. Shared kernels reduce overhead while making kernel and privilege boundaries security-critical.

## Vocabulary

- **Container:** An isolated process group launched with a packaged filesystem and configuration.
- **Image:** An immutable content-addressed template for a container filesystem and metadata.
- **Layer:** A reusable filesystem change set within an image.
- **Digest:** A cryptographic content identifier.
- **Registry:** A service for storing and distributing container images.
- **Namespace:** A Linux mechanism that gives processes isolated views of selected resources.
- **Cgroup:** A Linux mechanism for grouping, accounting for, and limiting resource use.
- **OCI:** Open Container Initiative specifications for images, runtimes, and distribution.
- **Runtime:** Software that creates and manages containers from runtime specifications.
- **Capability:** A separable unit of Linux privilege.
- **Rootfs:** The root filesystem presented to a container process.
- **SBOM:** A software bill of materials listing artifact components.

## See it yourself

On Linux, inspect the isolation and resource-control identities of the process running this command:

```bash
python3 - <<'PY'
from pathlib import Path

for name in ("pid", "mnt", "net", "uts", "user"):
    print(f"{name:>4} namespace: {Path(f'/proc/self/ns/{name}').readlink()}")

print("cgroup membership:")
print(Path("/proc/self/cgroup").read_text().strip())
PY
```

Predict whether every namespace entry will share one identifier, then run the command on Linux. The expected output shows that the process belongs to one instance of each namespace type and to a cgroup hierarchy. That supports the kernel-primitives account of containers. It does not prove strong isolation, active resource limits, or that the process was launched from an image.

## Where it shows up

A CUDA-enabled image can package user-space libraries but not its own host kernel or physical driver. At startup, the container runtime exposes devices and mounts compatible driver components from the host. An image that works on one node may fail on another whose driver cannot support its CUDA runtime. The digest identifies the package; node and device evidence complete the execution environment.

## When it breaks

Exit code 137 commonly appears when a container receives `SIGKILL`, often after a cgroup OOM, but it can also follow an external forced stop. First inspect the container termination reason, cgroup memory events, configured limit, and node pressure. The code alone does not distinguish a memory limit from an operator or runtime kill.

## Practice

### Observe

Build a minimal image, inspect layers and process identity, run read-only with resource limits, and observe termination behavior.

### Build

Create a non-root, multi-stage model API image with health checks, pinned dependencies, and an SBOM.

### Break

Use a mutable tag, write to rootfs, omit signal handling, and exceed memory. Make each failure explicit.

### Say it out loud

Explain why a container is not a small virtual machine.

**Success:** Include image contents, namespaces, cgroups, the shared kernel, and the first evidence for an OOM or signal failure.

## Check yourself

1. How do namespaces differ from cgroups?
2. Why are digests stronger than tags?
3. Why is container isolation unlike VM isolation?

### Interview stretch

- Debug a container killed with exit code 137.
- Secure a model-serving image.
- Explain host-driver/container-toolkit compatibility.

## Sources

### REQUIRED

- “OCI Runtime Specification” — Open Container Initiative. [Official specification](https://github.com/opencontainers/runtime-spec). Defines portable container execution.

### RECOMMENDED

- “Docker Engine Security” — Docker. [Official docs](https://docs.docker.com/engine/security/). Explains daemon, namespaces, capabilities, and attack boundaries.

### DEEP DIVE

- “Control Group v2” — Linux kernel community. [Kernel documentation](https://docs.kernel.org/admin-guide/cgroup-v2.html). Canonical resource-control semantics.

## Next

Continue with [./13-kubernetes.md](./13-kubernetes.md).
