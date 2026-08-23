# Evidence-driven container debugging

Container debugging works fastest when you locate the failing boundary first and preserve the stopped container, exit status, runtime configuration, and host evidence before replacement.

## Why it matters

Restarting or rebuilding may temporarily clear a symptom while deleting logs, filesystem changes, and process state. Application, image, runtime, kernel, network, and storage failures can present as the same "container exited" report.

## How it works

Begin with identity and timeline: image digest, command, creation and start times, exit code, signal, restart count, health status, and recent runtime events. Then inspect stdout and stderr, effective environment names without exposing secret values, mounts, port mappings, network membership, user, limits, and security options.

Exit code 137 often reflects SIGKILL and may indicate an OOM kill, but host and cgroup evidence must confirm it. Exit 126 indicates a command found but not executable; 127 usually indicates command not found. CPU throttling appears as latency with cgroup throttled-time counters rather than termination. DNS, routes, listener address, and connection tests isolate network layers. Read-only errors, ownership, mount source, inode use, and bytes available isolate storage layers.

Use an ephemeral diagnostic container sharing only the needed namespace when the production image lacks tools. Do not install tools into the failing container or expose secrets merely to debug.

## See it yourself

Run a container with a nonexistent command and inspect `docker ps -a`, `docker inspect`, and `docker logs`. Then run a bounded memory stressor in a disposable environment and compare exit code with `OOMKilled` state and host logs where authorized. Predict the evidence before each run; results vary by runtime and host policy.

## Where it shows up

An HTTP container is reported unavailable. The artifact digest is correct and process is running, but inspection shows the server listens on loopback. In another incident the process exits 137 and cgroup memory events increment, proving limit pressure rather than a bad health check.

## When it breaks

An automatic restart loop overwrites useful context. Mutable tags make reproduction use different bytes. Host disk exhaustion affects every container. Debug commands run with `--privileged` and change the security boundary. Clocks disagree across application and runtime logs.

Freeze destructive automation when safe, capture minimal evidence, reproduce with the exact digest and runtime settings, change one variable, and verify the user-visible path after repair.

## Practice

**Observe:** build a one-page evidence bundle for a running container including digest, command, PID, limits, mounts, network, security settings, health, and log timestamps.

**Build:** write a decision tree for crash, Pending-like startup, unreachable service, slow service, and failed write. Every branch must name a command, expected observation, and next hypothesis.

**Break safely:** create wrong command, loopback bind, read-only write, and memory-limit failures in disposable containers. Completion means each diagnosis cites distinguishing evidence before any restart and the repaired workload retains hardening controls.

## Check yourself

1. Why does exit code 137 require corroborating evidence?
2. Which observations distinguish forwarding failure from listener failure?
3. When is an ephemeral diagnostic container safer than modifying the image?
4. What evidence is usually lost by removing a failed container?

## Sources

### REQUIRED

- [Docker container logs](https://docs.docker.com/engine/logging/)

### RECOMMENDED

- [Docker inspect reference](https://docs.docker.com/reference/cli/docker/inspect/)

### DEEP DIVE

- [Linux control group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)

## Next

[Kubernetes](../16-kubernetes/README.md)
