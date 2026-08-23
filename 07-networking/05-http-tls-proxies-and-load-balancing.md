# HTTP, TLS, Proxies, and Load Balancing

Production HTTP is usually a chain of independently timed connections, not one transparent pipe from browser to handler.

## Why it matters

A load balancer can return a valid HTTPS 503 while every application instance is healthy, or return 502 because it cannot complete TLS to an origin. The status proves that some HTTP participant answered; it does not identify the participant or root cause. Safe retries and useful telemetry require a precise model of connection boundaries, request identity, and health policy.

## How it works

An HTTP/1.1 connection carries messages over a TCP byte stream, using syntax such as `Content-Length` or chunked coding to frame bodies. HTTP/2 multiplexes streams over one connection and compresses headers; HTTP/3 maps HTTP semantics onto QUIC. Methods describe requested semantics. Safe methods are intended not to request state changes, while idempotent methods can be repeated with the same intended effect, though logging and billing side effects still need care.

TLS begins before encrypted HTTP on an HTTPS connection. The client offers protocol versions, cipher capabilities, and usually a server name through SNI. The server presents a certificate chain and proves possession of the private key; the client validates trust, validity, hostname, and policy. ALPN can select HTTP/2 or HTTP/1.1. A reverse proxy may terminate this TLS connection and create a separate upstream connection with its own DNS, transport, TLS, timeout, and identity rules.

A load balancer selects an eligible backend using an algorithm such as round robin, least connections, or a consistent hash. Active health checks test a configured endpoint; passive checks infer health from real traffic. A shallow `/health` can keep an instance eligible even when its critical dependency is exhausted, while an overly deep check can remove every instance during a shared dependency failure. Connection draining stops new assignment and allows bounded in-flight work to finish. Forwarded headers are trustworthy only when sanitized and set by a known proxy boundary.

## See it yourself

Predict that the response contains status and headers selected by an intermediary or origin, and that the TLS certificate names `example.com`. Exact headers and server addresses may vary.

```bash
curl --silent --show-error --output /dev/null \
  --write-out 'code=%{http_code} remote=%{remote_ip} tls=%{ssl_verify_result}\n' \
  https://example.com/
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null |
  openssl x509 -noout -subject -issuer -dates
```

Expected observation: an HTTPS request succeeds only after transport and TLS setup, and the certificate exposes identity and validity metadata.

Limits of the observation: one success does not prove all backends healthy, reveal every proxy hop, or establish retry safety. Certificate metadata alone does not prove the application response came from a particular origin process.

## Where it shows up

During deployment, an ingress stops assigning new requests to an old instance, but existing HTTP/2 streams and keep-alive connections may continue. The process needs a readiness transition, a drain interval aligned with request deadlines, and a hard shutdown bound. Otherwise clients see resets precisely when the orchestrator reports a successful rollout.

## When it breaks

A certificate hostname error belongs to client-to-terminator TLS. A 421 can indicate authority sent over the wrong connection; 502 often means proxy-to-upstream failure; 503 often means no eligible capacity or deliberate unavailability; 504 indicates an intermediary’s upstream deadline. These conventions are not universal, so inspect the responding hop’s logs. Preserve request ID, `Host` or `:authority`, SNI, selected address, protocol version, status, timing phases, backend choice, and retry count. Never disable certificate verification as a production fix.

## Practice

**Build:** place a simple local reverse proxy in front of two identifiable handlers, then record which backend serves each request. **Break:** stop one backend, make a health endpoint fail, and delay a response beyond the proxy deadline one variable at a time. **Explain back:** name each connection and timeout budget. Success includes graceful removal, no trusted client-supplied forwarding identity, and evidence distinguishing proxy-generated from application-generated errors.

## Check yourself

1. Why can a valid HTTPS error response rule out some failures but not identify the failing backend?
2. What makes a health check deep enough without making a shared outage remove all capacity?

## Sources

### REQUIRED

- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
- [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446)

### RECOMMENDED

- [RFC 9112: HTTP/1.1](https://www.rfc-editor.org/rfc/rfc9112)
- [NGINX HTTP Load Balancing](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/)

### DEEP DIVE

- [RFC 9114: HTTP/3](https://www.rfc-editor.org/rfc/rfc9114)

## Next

Continue to [Network Debugging from Symptom to Packet](./06-network-debugging-from-symptom-to-packet.md).
