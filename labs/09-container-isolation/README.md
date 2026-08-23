# Lab: Inspect Container Isolation and Debug a Broken Service

Run one bounded container and inspect namespaces, cgroups, mounts, identity, capabilities, networking, and logs before diagnosing a deliberate health failure.

## Prerequisites

- Docker Engine and Bash
- Ability to run Docker commands
- Port 58090 unused

## Safety

Use only the named lab container and network. Do not use `--privileged`, host PID/network namespaces, host filesystem mounts, added capabilities, or the Docker socket. Bind the service to loopback and cap memory, CPU, PIDs, and runtime.

## Setup and baseline

```bash
mkdir -p .work
docker network create lab-isolation
docker run -d --name lab-isolation-web --network lab-isolation \
  --read-only --tmpfs /tmp:rw,noexec,nosuid,size=16m \
  --memory 128m --cpus .5 --pids-limit 64 \
  --security-opt no-new-privileges \
  -p 127.0.0.1:58090:8000 \
  python:3.13-alpine sh -c 'cd /tmp && printf healthy >index.html && python -m http.server 8000'
curl --max-time 3 http://127.0.0.1:58090
```

Record the image digest. Predict which kernel the container reports and whether its root filesystem accepts writes.

## Tasks

1. Inspect configuration:

   ```bash
   docker inspect lab-isolation-web >.work/inspect.json
   docker stats --no-stream lab-isolation-web | tee .work/stats.txt
   docker top lab-isolation-web | tee .work/top.txt
   ```

2. Compare host and container process IDs with `docker top` and `docker exec ... ps`.
3. Inside the container, inspect `/proc/1/status`, `/proc/self/mountinfo`, `/proc/self/cgroup`, `id`, and `/etc/resolv.conf`.
4. Attempt `touch /proof` and capture the expected read-only-filesystem failure. Prove `/tmp` remains writable and bounded.
5. Use `docker inspect` to explain port publication, network address, resource limits, dropped privilege assumptions, and health status.

## Evidence to keep

Keep image ID and digest, inspect excerpts, PID comparison, cgroup path, mount flags, identity, capability fields, resource sample, logs, and a statement of what container isolation does not guarantee.

## Failure injection

Replace the container with the same limits but start the HTTP server on port 8001 while publishing container port 8000:

```bash
docker rm -f lab-isolation-web
docker run -d --name lab-isolation-web --network lab-isolation \
  --read-only --tmpfs /tmp:size=16m --memory 128m --cpus .5 --pids-limit 64 \
  --security-opt no-new-privileges -p 127.0.0.1:58090:8000 \
  python:3.13-alpine sh -c 'cd /tmp; printf healthy >index.html; python -m http.server 8001'
```

Expected symptom: the process and container are running, but the published endpoint fails. Diagnose by comparing logs, listening port, and `docker inspect` port mapping.

## Cleanup

```bash
docker rm -f lab-isolation-web 2>/dev/null || true
docker network rm lab-isolation 2>/dev/null || true
rm -rf .work
```

Verify `docker ps -a --filter name=lab-isolation-web` is empty.

## Rubric

- 2 points: applies explicit process, CPU, memory, filesystem, and privilege limits
- 3 points: explains namespace, cgroup, mount, and port evidence
- 2 points: diagnoses process-up but endpoint-down behavior
- 2 points: distinguishes isolation from a security boundary guarantee
- 1 point: removes only named lab resources

## Sources

- [OCI runtime specification](https://github.com/opencontainers/runtime-spec)
- [Docker resource constraints](https://docs.docker.com/engine/containers/resource_constraints/)
- [Linux namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html)
