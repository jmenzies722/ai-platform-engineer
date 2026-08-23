# DNS Resolution and Operations

DNS is a distributed, cached database whose answers are scoped by name, type, authority, and time.

## Why it matters

A record changed in the authoritative zone can coexist with an older positive answer, a cached negative answer, and a different answer from split-horizon DNS. “DNS has propagated” hides all of those mechanisms. During a migration, an operator must know which resolver was asked, which record type it returned, whether the answer was authoritative, and how long that observer may reuse it.

## How it works

A stub resolver normally asks a recursive resolver for a specific owner name and record type. The recursive resolver may answer from cache or walk delegations from a root server to a top-level domain and then to an authoritative server. Each referral supplies name-server records and sometimes glue addresses needed to reach those servers. The authoritative server returns an answer, a referral, or a negative response backed by the zone’s start-of-authority data.

The cache key includes more than a human-readable hostname. `A`, `AAAA`, `MX`, `TXT`, and `CNAME` records have distinct meanings. A CNAME aliases one owner name and causes additional resolution; it is not an HTTP redirect. TTL limits how long a resolver may reuse an answer, but lowering a TTL after caches already hold the old, longer value cannot recall those entries. Negative responses are cached too. Search suffixes and `ndots` rules may turn one application name into several wire queries, while `/etc/hosts`, NSS configuration, or an application cache may bypass the recursive path an engineer is inspecting.

Operational changes therefore use staged timing: lower TTL before a planned cutover, wait out the previous TTL, publish the new data, verify it directly at authority and through representative recursive resolvers, then restore a sensible TTL. DNSSEC authenticates DNS data through a chain of signed delegations; it does not encrypt queries or prove that an addressed application is healthy.

## See it yourself

Predict that the system resolver returns one or more addresses for `example.com`, but do not predict their exact values or order. Then compare the configured resolver path with a direct tool if available.

```bash
python3 - <<'PY'
import socket
for item in socket.getaddrinfo("example.com", 443, type=socket.SOCK_STREAM):
    print(item[0].name, item[4][0])
PY
command -v dig >/dev/null && dig example.com A +noall +answer || true
```

Expected observation: the application-facing resolver can return IPv4 and IPv6 candidates, while `dig` displays DNS records and TTLs. Results vary by resolver, network, and time.

Limits of the observation: `getaddrinfo` may use sources other than DNS, and a recursive answer does not prove what every resolver sees. Neither command proves that port 443 is reachable or that HTTP is healthy.

## Where it shows up

A database failover name often maps clients to a new primary. Long-lived connection pools do not re-resolve merely because a TTL expires, so DNS can be correct while established sessions still use the former address. The rollout needs both DNS evidence and a connection-lifetime policy. Service discovery systems face the same distinction between publishing membership and making clients refresh it.

## When it breaks

`NXDOMAIN` means the queried name does not exist according to the answering chain; `NOERROR` with no requested records is different. `SERVFAIL` often points to validation, delegation, or upstream availability. Intermittent lookup delay can come from unreachable name servers, IPv6 path trouble, or repeated search-suffix attempts. Capture the exact query name and type, resolver address, flags, answer, authority section, TTL, and timing. Compare authority with recursion before flushing caches. A global cache flush destroys useful state and can create a thundering herd.

## Practice

**Build:** query one name through the system resolver and, if available, trace its delegation with `dig +trace`; record every claim with its observer and timestamp. **Break:** query a deliberately nonexistent subdomain and distinguish negative answer from transport failure. **Explain back:** describe why changing an authoritative record does not replace cached answers or existing TCP connections. Success is a table covering name, type, resolver, response code, authority, TTL, and what remains unproved.

## Check yourself

1. Why must a planned TTL reduction happen before a cutover?
2. How can an authoritative answer be correct while an application still reaches an old address?

## Sources

### REQUIRED

- [RFC 1034: Domain Names, Concepts and Facilities](https://www.rfc-editor.org/rfc/rfc1034)
- [RFC 1035: Domain Names, Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035)

### RECOMMENDED

- [RFC 2308: Negative Caching of DNS Queries](https://www.rfc-editor.org/rfc/rfc2308)
- [BIND 9 Administrator Reference Manual](https://bind9.readthedocs.io/)

### DEEP DIVE

- [DNSSEC Protocol Modifications](https://www.rfc-editor.org/rfc/rfc4035)

## Next

Continue to [HTTP, TLS, Proxies, and Load Balancing](./05-http-tls-proxies-and-load-balancing.md).
