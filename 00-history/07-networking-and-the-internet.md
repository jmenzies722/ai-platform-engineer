# Networking and the Internet

Networks let independent computers exchange messages even when they differ internally or the path between them is unreliable.

## Why it matters

**Prerequisite:** [Unix, C, and Linux](./06-unix-c-linux.md).

Isolated computers shared data through physical media or private links. Connecting unlike networks required protocols that could survive different hardware, routes, and operators.

Packet switching and the Internet protocol suite created that common contract. DNS, HTTP, and TLS made the network useful and safer at global scale, while congestion, attack, and independent failure ensured that communication could never be treated like a local function call.

## How it works

Each layer wraps a payload with enough information to provide a narrower service; no layer guarantees more than its contract.

DNS resolves names; routing selects next hops; IP provides best-effort datagrams; TCP establishes ordered reliable byte streams using acknowledgments and congestion control; TLS authenticates and encrypts; HTTP defines application semantics.

TCP reliability is end-to-end, not instantaneous: retransmission raises tail latency. Throughput depends on bandwidth-delay product and congestion windows. Application retries can amplify load unless bounded and idempotent.

## Vocabulary

- **Packet:** A bounded unit of data sent through a packet network.
- **IP:** The Internet Protocol for addressed best-effort packet delivery.
- **Route:** A decision or path for forwarding traffic toward a destination.
- **TCP:** A reliable ordered byte-stream transport over IP.
- **UDP:** A message-oriented transport with minimal delivery guarantees.
- **DNS:** The distributed naming system that maps names to records.
- **HTTP:** An application protocol for requests, responses, and resource semantics.
- **TLS:** A protocol providing authenticated encrypted transport.
- **RTT:** Round-trip time for a message to reach a peer and a response to return.
- **MTU:** Maximum transmission unit carried in one link-layer frame without fragmentation.
- **Congestion window:** A sender-side limit on unacknowledged TCP data based on network conditions.
- **Bandwidth-delay product:** The data needed in flight to fill a path of given bandwidth and RTT.

## See it yourself

```bash
ip route
getent hosts example.com
curl -v --connect-timeout 3 https://example.com/
ss -tan
```

Before running the commands, assign each one to naming, routing, HTTP/TLS, or connection state. A healthy path should yield a route, one or more addresses, a completed TLS-backed response, and socket information. Together they support a layered account of communication. They do not prove that another client, route, address family, or later request will behave the same way.

## Where it shows up

Suppose a model request intermittently times out while the server reports healthy. One client may hold a stale DNS answer, a load balancer may queue new connections, or packet loss may trigger TCP retransmission. Each cause produces a different timing signature even though the application sees one deadline. Separating resolution, connect, TLS, first-byte, and transfer time turns “network error” into a testable location.

## When it breaks

Intermittent timeouts can come from stale DNS, exhausted connection pools or ports, packet loss, MTU trouble, TLS failure, or retry amplification. The first useful move is to split one request into resolution, route, connect, TLS, and application timing from both endpoints. Packet capture comes later when those boundary checks leave transport behavior uncertain.

## Practice

### Observe

Resolve a host, inspect route and TLS handshake, measure timing with `curl`, and explain each phase without using “the network” as one box.

### Build

Implement a length-prefixed TCP echo protocol with deadlines, request IDs, and bounded messages.

### Break

Inject latency, loss, truncated frames, and duplicate requests. Add timeouts and idempotency.

### Say it out loud

Explain a web request without using “the network” as a single box.

**Success:** Name the contracts for naming, routing, transport, TLS, and HTTP, then localize one timeout from evidence.

## Check yourself

1. Why is IP best effort?
2. What does TCP guarantee—and not guarantee?
3. Why can retries worsen failure?

### Interview stretch

- Debug intermittent cross-region timeouts.
- Explain DNS TTL trade-offs.
- Compare TCP and UDP for model traffic.

## Sources

### REQUIRED

- “A Protocol for Packet Network Intercommunication” — Vint Cerf and Bob Kahn. [IEEE DOI](https://doi.org/10.1109/TCOM.1974.1092259). Establishes internetworking principles.

### RECOMMENDED

- “Internet Protocol” — IETF, RFC 791. [RFC Editor](https://www.rfc-editor.org/rfc/rfc791). Canonical IP specification and best-effort model.

### DEEP DIVE

- “TCP Congestion Control” — IETF, RFC 5681. [RFC Editor](https://www.rfc-editor.org/rfc/rfc5681). Defines core congestion behavior behind production throughput.

## Next

Continue with [./08-databases.md](./08-databases.md).
