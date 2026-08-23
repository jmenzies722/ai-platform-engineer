# 03 — Network Failure Laboratory

Create a reproducible laboratory, not a collection of command snippets, in its own repository.

## Problem and users

Developers and incident responders routinely misclassify DNS, TCP, TLS, proxy, and application failures because symptoms overlap. The lab must teach an engineer to form and eliminate hypotheses using packet captures, resolver output, connection state, and service telemetry. A facilitator must be able to run blind scenarios repeatedly.

## Constraints and experiment design

- Run locally with disposable network namespaces or equivalent isolated hosts; never target public systems.
- Pin images, certificates, DNS records, latency, loss, and clock assumptions so results are repeatable.
- Each scenario has a hidden fault, expected observations at every layer, safeguards, and a reset procedure.
- Exclude a polished training portal and any denial-of-service technique that escapes the lab boundary.

## Architecture expectations

Provide a small client, authoritative DNS server, recursive resolver or cache, TLS endpoint, reverse proxy, and packet-observation point. Treat topology, routes, names, trust stores, timeouts, and fault injection as versioned inputs. Distinguish control traffic from test traffic and host clocks from capture timestamps. Explain where encryption prevents inspection and which endpoint evidence replaces it.

## Milestone plan

1. Establish deterministic healthy DNS, TCP, TLS, HTTP/1.1, and HTTP/2 journeys.
2. Add DNS faults: stale cache, delegation error, NXDOMAIN, timeout, and split-horizon mismatch.
3. Add transport/security faults: loss, MTU issue, reset, expired certificate, SNI mismatch, and clock skew.
4. Add proxy/application faults, blind drill harness, scoring, cleanup checks, and evidence bundles.

## Required artifacts

- Topology and trust-boundary diagrams, scenario catalog, facilitator key, and learner runbook.
- Annotated packet captures and endpoint logs for one healthy and six failed journeys.
- Timeout/retry budget worksheet and a symptom-to-layer decision record.
- Automated environment reset and proof that no fault rules or secrets remain.

## Tests and failure drills

Test healthy probes before and after each scenario; validate DNS answers, certificate chains, route tables, and packet counters. Blind drills must include SERVFAIL, partial packet loss, PMTU black hole, TLS name failure, proxy 502, retry amplification, and a deliberately misleading application timeout. Score hypothesis quality and evidence, not command memorization.

## Observability, security, and cost

Correlate query ID, connection tuple, TLS handshake, request ID, and proxy attempt without logging credentials or full sensitive payloads. Restrict capabilities, bind services to the isolated network, use synthetic certificates, and document capture-data retention. The default lab should run on a developer machine with no paid services; publish CPU, memory, disk, and packet-capture growth.

## Explicit success rubric

| Outcome | Required evidence |
|---|---|
| Repeatability | Fresh setup produces the declared healthy traces and every scenario resets cleanly. |
| Layer reasoning | A reviewer identifies at least five of seven blind faults and cites discriminating evidence. |
| Safety | Isolation tests prove traffic, fault rules, and credentials cannot escape or persist. |
| Teaching quality | Scenario explanations connect symptoms to protocol state and acknowledge ambiguous evidence. |

## Stretch work

Add QUIC/HTTP/3 comparison, dual-stack IPv4/IPv6 faults, or a certificate-transparency investigation.

## Authoritative sources

- [DNS Concepts and Facilities, RFC 1034](https://www.rfc-editor.org/rfc/rfc1034)
- [TCP, RFC 9293](https://www.rfc-editor.org/rfc/rfc9293)
- [TLS 1.3, RFC 8446](https://www.rfc-editor.org/rfc/rfc8446)
- [HTTP/2, RFC 9113](https://www.rfc-editor.org/rfc/rfc9113)

## Mapped modules

[04 Linux](../../04-linux/README.md), [07 Networking](../../07-networking/README.md), [09 Backend Engineering](../../09-backend-engineering/README.md), [18 Observability](../../18-observability/README.md), and [19 Site Reliability Engineering](../../19-sre/README.md).
