# Container networks and persistent storage

Container networking and storage translate isolated process views into host and external resources, so reachability and durability depend on both application behavior and runtime wiring.

## Why it matters

A published port cannot repair a server listening on loopback, and a running container does not imply its data will survive replacement. Incorrect host mounts can expose secrets or allow a container to alter the host.

## How it works

On a typical Linux bridge network, the runtime gives the container a network namespace, virtual interface, route, and DNS configuration. Port publishing installs host forwarding to a container address and port. The application must listen on the container interface, usually `0.0.0.0` or an explicit non-loopback address. User-defined networks provide scoped discovery; container addresses remain replaceable identities.

The image filesystem is layered and read-only. A writable copy-on-write layer captures runtime changes and disappears with container removal. Named volumes have lifecycle outside a container and are managed by the runtime. Bind mounts map a specific host path, inherit host ownership and labeling concerns, and can expose host authority. tmpfs provides nonpersistent memory-backed storage.

Durability also requires application consistency, backup, restore, and correct write ordering. A volume surviving removal does not prove its contents are valid or portable across hosts.

## See it yourself

Run `docker run --rm -d --name web -p 127.0.0.1:8080:80 nginx:alpine`, then inspect its network namespace values with `docker inspect web`. Write a marker to a named volume, remove the container, and mount the volume in a new container. Predict which data survives. This demonstrates local runtime lifecycle, not distributed storage durability.

## Where it shows up

A local service uses a user-defined network and DNS service name instead of fixed addresses. Its database stores files on a named volume while application containers remain replaceable. Production schedulers add network plugins and storage drivers, but listen addresses, mount permissions, and persistence contracts remain.

## When it breaks

The application binds to `127.0.0.1`. Host and container ports are confused. DNS points to a replaced container. A bind-mounted file has the wrong UID or security label. The writable layer fills the host disk. Two writers use storage that lacks safe multi-writer semantics. Backup copies crash-inconsistent data.

Gather socket listeners, routes, DNS results, published bindings, mount type, source, destination, permissions, capacity, and application logs before recreating the container.

## Practice

**Observe:** trace one request from host socket through published mapping to the process listener, and classify every mount by lifecycle and authority.

**Build:** run a service on a user-defined network with localhost-only host publication, a read-only configuration bind mount, a named data volume, and tmpfs scratch space.

**Break safely:** bind the service to loopback, then make a volume unwritable. Completion means evidence distinguishes forwarding from listen failure and permissions from capacity, while data survives container replacement.

## Check yourself

1. Why does publishing a port not guarantee reachability?
2. Which storage survives container removal by design?
3. What authority can a writable bind mount grant?
4. Why is volume persistence not the same as recoverability?

## Sources

### REQUIRED

- [Docker networking overview](https://docs.docker.com/engine/network/)

### RECOMMENDED

- [Docker storage overview](https://docs.docker.com/engine/storage/)

### DEEP DIVE

- [Container Network Interface specification](https://www.cni.dev/docs/spec/)

## Next

[Runtime hardening and image trust](05-security-and-trust.md)
