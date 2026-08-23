# Lab: inspect and constrain a container

Use Docker or a compatible CLI and the official `nginx:alpine` image. Pulling an image uses network bandwidth; the lab creates no cloud resources.

## Run safely

```bash
docker run --name curriculum-web --detach \
  --publish 127.0.0.1:8080:8080 \
  --read-only --tmpfs /var/cache/nginx --tmpfs /var/run \
  --memory 128m --cpus 0.5 --pids-limit 100 \
  nginx:alpine sh -c \
  "sed -i 's/listen       80;/listen       8080;/' /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'"
```

This demonstration edits configuration at startup, so the root filesystem cannot actually be read-only. Predict the failure, inspect it, then fix the design by mounting a prepared configuration file read-only rather than making the whole root writable. That tension is the point of the lab.

## Inspect

```bash
docker ps --all --filter name=curriculum-web
docker logs curriculum-web
docker inspect curriculum-web
docker stats --no-stream curriculum-web
docker image inspect nginx:alpine
docker history nginx:alpine
```

Find the process command, effective user, port binding, mount list, memory limit, CPU quota, and exit code. Explain why binding the host side to `127.0.0.1` differs from binding the server inside the container.

## Repair

Create a local Nginx configuration that listens on 8080 and mounts it at `/etc/nginx/conf.d/default.conf:ro`. Keep the root read-only and tmpfs mounts. Re-run, then verify with:

```bash
curl --fail http://127.0.0.1:8080/
```

For an additional hardening pass, investigate the UID used by the image and remove capabilities one by one. Do not blindly use `--privileged`.

## Cleanup

```bash
docker rm --force curriculum-web
```

Optionally remove the downloaded image with `docker image rm nginx:alpine`.
