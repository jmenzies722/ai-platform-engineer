# TCP, UDP, and Ports

Transport protocols distinguish conversations between applications and choose different reliability guarantees.

## Why it matters

A client timeout after sending a request does not reveal whether TCP connected, bytes reached the peer, or the application completed an operation whose response was lost. Retry safety depends on that uncertainty. Engineers need endpoint identity, transport state, and application framing before deciding to reconnect or repeat work.

## How it works

UDP sends independent datagrams with ports but no built-in delivery or ordering. TCP creates a byte stream identified by endpoint addresses and ports, establishes state, numbers bytes, acknowledges data, retransmits loss, and controls flow and congestion. A listening socket accepts new TCP connections.

A socket binds protocol state to local addressing. UDP preserves datagram boundaries and adds ports plus a checksum, but applications must choose reliability, ordering, duplicate handling, and congestion behavior appropriate to their use. TCP establishes synchronized sequence state, presents each side with an ordered byte stream, acknowledges byte ranges, retransmits inferred loss, and uses flow and congestion control. A listening socket represents a local endpoint; `accept` creates a connected socket for one peer while leaving the listener available. The connection is identified by protocol and both address-port pairs, allowing many clients to use one server port. Client ephemeral ports separate simultaneous conversations. TCP has no record boundary: two writes can arrive in one read or one write across several reads, so the application protocol must frame messages.

## See it yourself

Predict that the client chooses an ephemeral local port and sees peer port 8765 on loopback. The server process should retain its listening socket after this one connected socket closes.

```bash
python3 -m http.server 8765 --bind 127.0.0.1 >/tmp/net-demo.log 2>&1 &
pid=$!
python3 - <<'PY2'
import socket
s=socket.create_connection(('127.0.0.1',8765)); print(s.getsockname(), s.getpeername()); s.close()
PY2
kill "$pid"; wait "$pid" 2>/dev/null || true; rm -f /tmp/net-demo.log
```

Expected observation: The client gets an ephemeral local port and connects to the server’s known listening port on loopback.

Limits of the tcp, udp, and ports observation: The connection test does not prove packet traversal beyond the host, delivery of application data, encryption, or durable processing. A completed handshake establishes transport state only.

## Where it shows up

A database connection pool makes these mechanics operational. Each pooled TCP stream occupies descriptors and server session state; an idle connection can become invalid behind a load balancer while still looking present to the client. Health validation, bounded pool size, connect and query deadlines, and protocol-aware retry rules prevent a dead socket from becoming duplicate transaction work. Increasing pool size can simply overload the database.

## When it breaks

Immediate refusal suggests a reachable host with no accepting listener or an active reject; connect timeout suggests dropping, routing, or return-path trouble; reset means a peer or intermediary aborted established state; truncated messages suggest framing errors above TCP. First inspect local listener and connection state with `ss`, then capture the exact endpoint pair and error timing. Only after transport is proven should application logs and message framing become the next boundary.

## Practice

**Build:** run the local HTTP server, inspect its listener, and write a client that prefixes a message with its byte length. **Break:** send a partial frame and enforce a server read deadline; contrast it with connecting to a closed local port. **Explain back:** separate UDP datagram, TCP stream, port, listener, connected socket, and application message. Success includes bounded cleanup and evidence for both endpoint pairs and each distinct failure.

## Check yourself

1. What does TCP guarantee that UDP does not?
2. Why must an application frame messages on a TCP stream?

## Sources

### REQUIRED

- [RFC 9293: TCP](https://www.rfc-editor.org/rfc/rfc9293)
- [RFC 768: UDP](https://www.rfc-editor.org/rfc/rfc768)

### RECOMMENDED

- [socket(7)](https://man7.org/linux/man-pages/man7/socket.7.html)

### DEEP DIVE

- [TCP Congestion Avoidance](https://www.rfc-editor.org/rfc/rfc5681)

## Next

Continue to [DNS, HTTP, and TLS](./03-dns-http-and-tls.md).
