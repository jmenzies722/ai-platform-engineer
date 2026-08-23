# Lab: diagnose and harden a container

Use Docker or a compatible CLI and the official `nginx:alpine` image. Pulling an image uses network bandwidth. The lab preserves evidence across deliberate startup, reachability, storage, and resource failures before producing a hardened workload.

## Safety and evidence directory

Run only on a disposable local engine. Do not use `--privileged`, mount the engine socket, expose a port beyond loopback, or inspect secret values. Create `/tmp/curriculum-container-evidence` and save command output there with timestamps.

```bash
rm -rf /tmp/curriculum-container-evidence
mkdir /tmp/curriculum-container-evidence
docker version > /tmp/curriculum-container-evidence/engine.txt
docker pull nginx:alpine
docker image inspect nginx:alpine > /tmp/curriculum-container-evidence/image.json
docker image inspect --format '{{json .RepoDigests}}' nginx:alpine
```

Record the immutable digest, architecture, declared user, entrypoint, and command. A digest establishes content identity, not safety or provenance.

## Trigger and diagnose startup failure

```bash
docker run --name curriculum-web --detach \
  --publish 127.0.0.1:8080:8080 \
  --read-only --tmpfs /var/cache/nginx --tmpfs /var/run \
  --memory 128m --cpus 0.5 --pids-limit 100 \
  nginx:alpine sh -c \
  "sed -i 's/listen       80;/listen       8080;/' /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'"
```

This tries to edit a read-only image filesystem. Predict the exit status and failing path before inspecting it.

```bash
docker ps --all --filter name=curriculum-web | tee /tmp/curriculum-container-evidence/ps-startup.txt
docker logs curriculum-web 2>&1 | tee /tmp/curriculum-container-evidence/logs-startup.txt
docker inspect curriculum-web > /tmp/curriculum-container-evidence/inspect-startup.json
docker inspect --format 'exit={{.State.ExitCode}} error={{.State.Error}} oom={{.State.OOMKilled}}' curriculum-web
```

Explain why making the root writable or privileged would hide the design conflict rather than solve it.

## Repair configuration without widening authority

```bash
docker rm curriculum-web
mkdir -p /tmp/curriculum-container-config
printf 'server { listen 8080; location / { return 200 "healthy\n"; } }\n' \
  > /tmp/curriculum-container-config/default.conf
docker run --name curriculum-web --detach \
  --publish 127.0.0.1:8080:8080 \
  --read-only --tmpfs /var/cache/nginx --tmpfs /var/run \
  --mount type=bind,src=/tmp/curriculum-container-config/default.conf,dst=/etc/nginx/conf.d/default.conf,readonly \
  --memory 128m --cpus 0.5 --pids-limit 100 \
  --security-opt no-new-privileges --cap-drop ALL --cap-add NET_BIND_SERVICE \
  nginx:alpine
curl --fail http://127.0.0.1:8080/
```

The capability exception may not be required for port 8080. Remove it, recreate, and retain it only if observed failure proves a need.

## Inspect namespaces, cgroups, network, and mounts

```bash
docker top curriculum-web
docker inspect curriculum-web > /tmp/curriculum-container-evidence/inspect-running.json
docker stats --no-stream curriculum-web | tee /tmp/curriculum-container-evidence/stats.txt
docker exec curriculum-web sh -c 'printf "pid=%s\n" "$$"; cat /proc/1/status; cat /proc/1/cgroup; ip route; mount'
docker port curriculum-web
```

Find PID 1, effective UID, namespace-visible interfaces, cgroup membership, root filesystem mode, tmpfs and bind mounts, memory limit, CPU quota, process limit, capabilities, security options, and localhost-only host binding. Relate each observation to a run option.

## Trigger a reachability failure

Change the configuration to `listen 127.0.0.1:8080`, recreate with the same runtime settings, and run the host `curl`. Preserve socket listeners, port mapping, container address, route, and logs before repair. Completion requires explaining why host forwarding cannot reach the loopback-only listener.

## Prove storage lifecycle

Create a named volume and marker:

```bash
docker volume create curriculum-data
docker run --rm --mount source=curriculum-data,target=/data alpine:latest \
  sh -c 'printf persistent >/data/marker'
docker run --rm --mount source=curriculum-data,target=/data,readonly alpine:latest \
  sh -c 'test "$(cat /data/marker)" = persistent'
```

Contrast the named volume with the failed container's writable layer and the configuration bind mount. State what survives container deletion, what is host-coupled, and why this is not a backup test.

## Trigger resource and security failures

Use a disposable image and a strict memory limit to produce allocation pressure. The exact command depends on available tools, so record the image and command. Confirm OOM from runtime state or cgroup memory evidence rather than exit code alone.

Then run the repaired Nginx container with all capabilities dropped, non-root UID supported by the image, read-only root, and no privilege escalation. If it fails, preserve evidence and change one constraint at a time. Never jump to privileged mode.

## Production review

Create a table with image digest, provenance status, process identity, namespaces, capabilities, seccomp or LSM policy, mounts, secrets path, network peers, resource requests and limits, health semantics, log retention, update policy, and owner. Mark what the local engine cannot prove.

## Completion criteria

The lab passes when another engineer can use the evidence directory to distinguish startup, reachability, permission, and OOM failures; verify named-volume persistence across replacement; reproduce the hardened runtime settings; and identify every remaining authority exception. Do not remove failed containers until review is complete.

## Cleanup

```bash
docker rm --force curriculum-web
docker volume rm curriculum-data
rm -rf /tmp/curriculum-container-config /tmp/curriculum-container-evidence
```

Optionally remove the downloaded image with `docker image rm nginx:alpine`.
