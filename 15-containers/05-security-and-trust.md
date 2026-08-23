# Runtime hardening and image trust

Container security requires trustworthy image inputs and minimal runtime authority because isolation controls reduce risk but do not turn a shared kernel into a separate machine.

## Why it matters

An attacker exploiting an application inherits the container's credentials, mounts, network access, capabilities, and kernel attack surface. A signed image run as privileged with a host socket mount is still dangerous.

## How it works

Build from reviewed, digest-pinned bases and minimize packages. Record SBOM and provenance, scan known vulnerabilities, and verify trusted signatures or attestations at admission. These controls answer different questions: content identity, origin, known findings, and policy compliance.

At runtime use a non-root UID, preferably with user namespace mapping or rootless operation; drop capabilities and add back only demonstrated needs; set `no-new-privileges`; apply a default or tailored seccomp profile; use SELinux or AppArmor policy; make the root filesystem read-only; constrain mounts, devices, processes, memory, CPU, and network; and deliver short-lived secrets through a dedicated mechanism.

Avoid `--privileged`, host PID or network namespaces, broad device access, and mounting the container engine socket. The engine API commonly controls the host, so socket access is not ordinary application access.

## See it yourself

Inspect a disposable container with `docker inspect` and record user, capabilities, security options, readonly root, mounts, devices, and namespaces. Run `docker run --rm --cap-drop ALL alpine:latest id` and compare with a default run. Dropping capabilities narrows kernel privileges but does not establish image trust or eliminate kernel vulnerabilities.

## Where it shows up

A production web image runs by digest as a fixed non-root UID, has no added capabilities, uses a read-only root with tmpfs scratch, mounts one secret read-only, reaches only required dependencies, and has measured resource limits. Admission policy rejects mutable image identity and forbidden runtime settings.

## When it breaks

The image declares a user but entrypoint scripts regain root. A writable host mount bypasses root filesystem protection. A scanner finding is accepted without exploitability review or expiry. Secrets appear in environment dumps or layers. Rootless mode is assumed to solve all host-kernel risk. Policy is enforced only in one launch path.

Investigate effective settings from runtime state, not Dockerfile intent alone. Capture image digest, runtime spec, process credentials, mounts, namespace mode, seccomp and LSM labels, network peers, and credential source.

## Practice

**Observe:** create an authority inventory for one container and explain why each privilege, mount, network destination, and secret exists.

**Build:** harden a local HTTP workload until it runs non-root with all capabilities dropped, no privilege escalation, read-only root, bounded resources, and only required writable paths.

**Break safely:** require a low port or a root-owned write path, observe denial, and redesign instead of adding broad privilege. Completion means functionality returns with one narrowly justified exception or none.

## Check yourself

1. What does image signing not prove about runtime safety?
2. Why is the engine socket effectively host authority?
3. How can a mount defeat a read-only root filesystem?
4. Which evidence reveals effective rather than declared identity?

## Sources

### REQUIRED

- [OCI runtime specification](https://github.com/opencontainers/runtime-spec)

### RECOMMENDED

- [Docker Engine security](https://docs.docker.com/engine/security/)

### DEEP DIVE

- [NIST Application Container Security Guide](https://csrc.nist.gov/pubs/sp/800/190/final)

## Next

[Evidence-driven container debugging](06-debugging.md)
