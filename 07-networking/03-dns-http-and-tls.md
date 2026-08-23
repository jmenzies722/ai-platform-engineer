# DNS, HTTP, and TLS

Applications combine naming, request semantics, and authenticated encryption to communicate safely at human-scale names.

## Why it matters

A browser’s “site unavailable” can originate in name resolution, TCP connection, TLS authentication, HTTP routing, or application processing. Changing DNS during an HTTP 500 incident is both ineffective and risky. The useful engineering decision is which protocol produced the last valid evidence and which contract failed next.

## How it works

DNS resolves names through cached, delegated records. HTTP defines methods, targets, headers, status codes, and message bodies. TLS authenticates the server using certificates and negotiates encrypted transport. Each layer has separate evidence and failure modes.

DNS resolvers follow cached answers and delegations from the root toward authoritative servers, respecting record type and TTL while local search rules may transform a name. An address answer supplies input to connection attempts; it does not guarantee reachability. TCP establishes transport, then TLS negotiates protocol parameters, validates a certificate chain and hostname under a trust policy, and derives keys for integrity and confidentiality. HTTP carries method, target, headers, status, and body over the secured stream. Intermediaries may terminate TLS, route by hostname, cache responses, or retry selected requests, so the server process observing HTTP may not hold the public certificate. Each layer reports different errors and has different caching and timeout state.

## See it yourself

Predict a connection exception because IP literal `127.0.0.1` bypasses DNS and port 9 normally has no listener. The exception should occur before any HTTP response object exists.

```bash
python3 - <<'PY2'
from http.client import HTTPConnection
c=HTTPConnection('127.0.0.1', 9, timeout=1)
try: c.request('GET','/')
except OSError as e: print(type(e).__name__, e)
PY2
```

Expected observation: Using an IP literal bypasses DNS, yet transport can still fail because no service listens on the selected port.

Limits of the dns, http, and tls observation: The refusal does not prove port 9 is closed on every system, show TLS behavior, or say anything about DNS health. It isolates one local transport attempt under the current host configuration.

## Where it shows up

An API behind a CDN demonstrates the sequence. DNS can direct clients to an edge, TLS authenticates the public hostname there, and HTTP routing forwards a request to an origin using another connection. A 502 from the edge proves the client completed enough DNS, transport, TLS, and HTTP exchange to receive that response; investigation should move to edge-origin evidence rather than the client certificate store.

## When it breaks

`NXDOMAIN` indicates a negative DNS answer for the queried name; connect timeout or refusal occurs before HTTP; certificate hostname or expiry errors occur during TLS; 404 and 500 are HTTP outcomes after a request reached an HTTP participant. First capture the exact URL, resolver answer, selected address, connect result, certificate identity, and status without suppressing errors. Avoid clearing every cache at once, because it destroys evidence and changes several layers together.

## Practice

**Build:** extend the local networking lab with `/ok` and missing paths, recording status and body. **Break:** use an IP/port with no listener and, in a controlled TLS test environment, a hostname mismatch; never weaken global certificate verification. **Explain back:** identify the last proven layer for each symptom. Success is a timeline containing DNS, TCP, TLS, and HTTP observations where applicable, with unsupported layers explicitly marked.

## Check yourself

1. Which layer assigns an HTTP 404?
2. What does a valid TLS certificate establish, and what does it not?

## Sources

### REQUIRED

- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)

### RECOMMENDED

- [RFC 1034: DNS concepts](https://www.rfc-editor.org/rfc/rfc1034)
- [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446)

### DEEP DIVE

- [HTTP: The Definitive Guide](https://www.oreilly.com/library/view/http-the-definitive/1565925092/)

## Next

Continue to [DNS Resolution and Operations](./04-dns-resolution-and-operations.md).
