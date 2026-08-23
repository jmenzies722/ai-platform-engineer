# 07 — Networking

Trace one request from a name on a screen to packets on a link, through transport and cryptography, across an HTTP exchange, and into a balanced service. Read the lessons in order: each one adds a layer without pretending the layers below disappeared.

## What you will learn

By the end, you can:

- explain addressing, longest-prefix routing, MTU, TCP streams, UDP datagrams, and socket identity;
- follow recursive DNS resolution and distinguish resolver, cache, delegation, and authoritative data;
- locate a failure in TCP, TLS, HTTP, proxying, or application processing from concrete evidence;
- reason about timeouts, retries, connection reuse, load-balancer health, and graceful draining; and
- run a safe packet-to-HTTP investigation without erasing the evidence you need.

## Lessons

1. [Addresses, Packets, and Routing](./01-addresses-packets-and-routing.md)
2. [TCP, UDP, and Ports](./02-tcp-udp-and-ports.md)
3. [DNS, HTTP, and TLS](./03-dns-http-and-tls.md)
4. [DNS Resolution and Operations](./04-dns-resolution-and-operations.md)
5. [HTTP, TLS, Proxies, and Load Balancing](./05-http-tls-proxies-and-load-balancing.md)
6. [Network Debugging from Symptom to Packet](./06-network-debugging-from-symptom-to-packet.md)

## Practice

[Trace a Local HTTP Connection](./lab-local-http.md) turns one loopback request into a protocol timeline. You will predict resolution and connection behavior, inspect sockets, capture only your own traffic when tools permit it, induce a refusal and a timeout-shaped application failure, and clean up every process and artifact.

Practice is part of the path, not an optional recap. Predict first, work only in disposable or explicitly scoped resources, compare expected and actual observations, and perform the documented cleanup.

## Ready to continue

Continue when you can narrate a request without collapsing DNS, routing, transport, TLS, and HTTP into “the network”; distinguish refusal, reset, timeout, TLS alert, and HTTP error; explain why retries can duplicate work; and produce a timeline whose claims are no stronger than its evidence.

## Next

Start with [Addresses, Packets, and Routing](./01-addresses-packets-and-routing.md).
