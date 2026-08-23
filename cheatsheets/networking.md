# Networking operator sheet

Diagnose from name resolution through application response. Test from the same
network namespace, host, and identity as the failing client; a laptop success
does not disprove a server-side path failure.

## Frame the question

Record client, destination, protocol, port, IP family, start time, frequency,
scope, and recent DNS, certificate, firewall, proxy, or deployment changes.
Classify the symptom: resolution failure, refusal, timeout, TLS failure, or
application response.

## 1. What name and address is the client using?

```bash
# Read-only
getent ahosts <host>
dig <host> A
dig <host> AAAA
dig <host> CNAME
```

`getent` uses the host's configured name-service path; `dig` directly queries
DNS and can disagree because `/etc/hosts`, NSS, split DNS, or caching intervenes.
`NOERROR` with no answers differs from `NXDOMAIN`. Multiple addresses imply
that one backend or IP family can fail intermittently.

```bash
# Read-only; query a named resolver to isolate resolver differences
dig @<resolver-ip> <host> A +noall +answer +authority
```

TTL is remaining cache lifetime, not propagation time. Do not flush shared
caches merely to make a test pass; compare authoritative and recursive answers
first.

## 2. Is local addressing and routing plausible?

```bash
# Read-only
ip -brief address
ip route get <destination-ip>
ip rule show
```

`ip route get` reports the kernel's selected route, source address, and
interface. It does not send a packet or prove return-path symmetry. `unreachable`
or a surprising source/interface points to local routing or policy rules.

**Caution:** Ping tests ICMP, not the required service. Filtering or success of
ICMP does not establish TCP, UDP, TLS, or application health.

## 3. Can transport establish?

```bash
# Read-only network probe; bounded timeout
nc -vz -w 3 <host> <port>
curl --connect-timeout 3 --max-time 10 -sS -o /dev/null \
  -w 'remote=%{remote_ip} code=%{http_code} connect=%{time_connect} tls=%{time_appconnect} total=%{time_total}\n' \
  https://<host>/health
```

Immediate `Connection refused` usually means the destination actively rejected
the connection or no listener exists. A timeout is less specific: packet loss,
filtering, routing, overloaded state tables, or an unresponsive peer. Connect
success proves a listener accepted transport, not that the application is ready.

The curl timings separate connection, TLS, and total latency. HTTP `000` means
no HTTP response was parsed; inspect stderr.

## 4. Is TLS identity and negotiation correct?

```bash
# Read-only network probe
openssl s_client -connect <host>:443 -servername <host> \
  -verify_hostname <host> -verify_return_error </dev/null
```

Check `Verification: OK`, subject alternative names, issuer, validity, and the
served chain. `-servername` sends SNI; omitting it can test the wrong virtual
host. A successful handshake with `-k` only proves encryption happened, not
server identity, so do not use `-k` as a fix.

```bash
# Read-only; show certificate dates and names without request data
openssl s_client -connect <host>:443 -servername <host> </dev/null 2>/dev/null |
  openssl x509 -noout -subject -issuer -dates -ext subjectAltName
```

## 5. What did HTTP say?

```bash
# Read-only network probe; headers may contain sensitive data
curl --connect-timeout 3 --max-time 10 -sS -D - -o /dev/null https://<host>/<path>
```

- `2xx`: request was handled, but validate the body or health contract.
- `3xx`: inspect `Location`; loops often indicate proxy or scheme confusion.
- `401`: authentication absent or invalid.
- `403`: identity understood but policy denied, though some systems obscure it.
- `404`: route or resource absent; it can also be an intentional security mask.
- `429`: rate or concurrency limit; respect `Retry-After`.
- `502`: proxy received an invalid upstream response.
- `503`: unavailable or deliberately drained.
- `504`: proxy timed out waiting for upstream.

Status alone does not identify which hop generated it. Correlate `Server`, trace
IDs, proxy logs, and application logs without exposing credentials.

## 6. Where might packets stop?

```bash
# Read-only network probes; behavior depends on filtering
tracepath <host>
ss -tn state syn-sent
```

Traceroute-style gaps do not prove the data path fails; intermediate devices may
drop probe responses. Repeated `SYN-SENT` supports failure before TCP handshake.
Packet capture requires privilege and can collect secrets:

```bash
# Privileged read; tightly scoped and approved
sudo tcpdump -ni <interface> host <ip> and port <port> -c 100
```

Store captures as sensitive evidence. Set packet and time bounds. Escalate before
capturing customer payloads or decrypted traffic.

## Change, rollback, and escalation

Do not simultaneously change DNS, firewall, load balancer, and application.
For one approved change, capture current config, define a health probe and error
budget guardrail, canary when possible, and keep the prior rule or record ready.
DNS rollback is constrained by caches and TTLs; firewall rollback must preserve
operator access.

Escalate for suspected DDoS, route leaks, widespread packet loss, certificate
private-key exposure, asymmetric paths outside your authority, or a required
change without independent access and rollback.

## Authoritative sources

- [iproute2 documentation](https://www.kernel.org/doc/man-pages/)
- [curl documentation](https://curl.se/docs/)
- [OpenSSL documentation](https://docs.openssl.org/)
- [DNS terminology, RFC 8499](https://www.rfc-editor.org/rfc/rfc8499)
- [HTTP semantics, RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- Repository lesson: [Networking](../07-networking/README.md)
