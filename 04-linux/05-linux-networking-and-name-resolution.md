# Linux Networking and Name Resolution

Linux networking connects process sockets to addresses, routes, interfaces, and name-resolution policy. Each layer can succeed while the next one fails.

## Why it matters

“The network is down” can mean a name did not resolve, no route exists, a firewall rejected traffic, nothing listens on the destination port, or an application protocol failed after connection. Restarting random services destroys state without locating the boundary. Diagnosis should move from the requested name and socket to the narrowest failed layer.

## How it works

A process creates a socket with an address family, type, and protocol. A server binds a local address and port, listens, and accepts connections; a client connects to a destination. Binding to loopback permits only local paths, while a wildcard address accepts traffic directed to eligible local interfaces subject to policy. TCP provides an ordered byte stream and connection state; UDP sends datagrams without TCP’s delivery and ordering guarantees.

Name resolution converts names to addresses using configured sources such as `/etc/hosts` and DNS through the system resolver. Routing chooses a next hop and interface for a destination. Neighbor discovery maps local-network addresses to link-layer destinations. Firewalls filter at defined hooks and directions. Network namespaces can provide separate interfaces, routes, and firewall state, so observations from the host may not describe a container. `ss` inspects sockets; `ip address` and `ip route` inspect interface and route state; resolver tools expose name answers.

## See it yourself

**Tiny Proof:** start a server bound only to loopback, prove a listening socket exists, and make one local HTTP request. Use only the PID you create.

```bash
d=$(mktemp -d)
printf 'ok\n' > "$d/index.html"
python3 -m http.server 8765 --bind 127.0.0.1 --directory "$d" >/dev/null 2>&1 &
pid=$!
sleep 0.5
ss -ltn 'sport = :8765' 2>/dev/null || true
python3 -c 'import urllib.request; print(urllib.request.urlopen("http://127.0.0.1:8765", timeout=2).read())'
kill -TERM "$pid"; wait "$pid" || true
rm -rf "$d"
```

Expected observation: a loopback listener serves `ok`; no DNS lookup is required because the URL uses a numeric address.

Limits of this proof: it does not test external routing, firewall policy, TLS, proxies, IPv6, or another namespace. A successful loopback request proves only the local path tested.

## Where it shows up

A containerized service may listen on `127.0.0.1` inside its own namespace while a platform forwards traffic to the container’s non-loopback address. The process is healthy locally yet unreachable through the platform. Inspecting listener address in the correct namespace, route, translation or proxy configuration, and one connection attempt separates bind scope from DNS and application behavior.

## When it breaks

“Name or service not known” points to resolution; “network unreachable” points to routing; immediate “connection refused” usually indicates a reachable host with no accepting listener or an explicit reject; timeout can arise from filtering, loss, queueing, or a silent application. First record name, resolved addresses, destination port, namespace, route, listeners, and exact timestamp. Packet capture can expose payloads and requires authorization; begin with metadata and narrow filters.

## Practice

**Build:** repeat the loopback experiment with a random high port, inspect listener and established socket states, and resolve `localhost`. **Break:** request an unused local port and a nonexistent name, preserving the distinct exceptions. **Explain back:** separate resolution, route, listener, transport connection, and HTTP response. Success means bounded timeouts, one tracked PID, no external traffic requirement, and cleanup after every failure.

## Check yourself

1. Why does a listening process not prove remote reachability?
2. What diagnostic distinction does a numeric destination make?

## Sources

### REQUIRED

- [ip(7)](https://man7.org/linux/man-pages/man7/ip.7.html)

### RECOMMENDED

- [ss(8)](https://man7.org/linux/man-pages/man8/ss.8.html)
- [systemd-resolved](https://www.freedesktop.org/software/systemd/man/latest/systemd-resolved.service.html)

### DEEP DIVE

- [Linux network namespaces](https://man7.org/linux/man-pages/man7/network_namespaces.7.html)

## Next

Continue to [Observability, Logs, and Resource Diagnosis](./06-observability-logs-and-resource-diagnosis.md).
