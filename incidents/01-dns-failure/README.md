# Drill: DNS Resolution Failure

> **Difficulty:** Starter  
> **Focus:** Resolver path, caching, boundary isolation  
> **Rule:** Investigate before opening [solution.md](solution.md).

## Context

At 14:07 UTC, requests from one application environment begin failing for `api.internal.example`. Existing connections continue briefly, but new connections fail. The application itself is healthy and no deployment was reported.

All names, addresses, logs, and values in this exercise are synthetic.

## Learner role

You are the application on-call. The network and DNS teams can run scoped
checks, but production DNS changes require an approved change owner.

## User impact

Requests requiring the dependency fail or time out. Quantify scope and duration from the evidence you create during the exercise.

## Symptoms

- Application error rate rises for new dependency calls.
- Direct IP connectivity may still work.
- Behavior may differ between hosts because cache and resolver state differ.

## Available evidence

Replace placeholders with outputs from your own safe local simulation or instructor-provided environment.

### Application log

```text
14:07:03 ERROR dependency request failed host=api.internal.example error="server misbehaving"
14:07:04 INFO  dependency request reused_connection=true status=200
14:07:10 ERROR dependency request failed host=api.internal.example error="server misbehaving"
```

### Resolver configuration

```text
$ cat /etc/resolv.conf
search app-prod.svc.example
nameserver 10.96.0.10
options ndots:5 timeout:1 attempts:2
```

### Query evidence

```text
$ getent hosts api.internal.example
<no result; exit 2>

$ dig @10.96.0.10 api.internal.example
;; ->>HEADER<<- opcode: QUERY, status: SERVFAIL, id: 4182
```

### Network evidence

```text
$ ip route
10.96.0.0/12 via 10.20.0.1 dev eth0
```

### Metrics

| Signal | Incident | Baseline |
|---|---:|---:|
| `dependency_errors{reason="dns"}` | 1,240/5m | 0/5m |
| `dns_responses{rcode="SERVFAIL"}` | 36% | less than 0.1% |
| Dependency TCP success by cached IP | 99.9% | 99.9% |
| Application CPU | 42% | 40% |

## Constraints

- Do not modify shared DNS infrastructure.
- Simulate with a disposable namespace, container, VM, or test hostname you control.
- Do not use public domains for destructive experiments.
- Preserve the exact resolver error; “DNS is down” is not a diagnosis.

## Investigation tasks

1. State impact and identify what is known versus inferred.
2. Draw the resolution path from the application through its resolver library or cache, the configured resolver, and the authoritative nameservers.
3. Write at least three plausible hypotheses.
4. For each hypothesis, choose a discriminating test and expected result.
5. Identify the earliest failing boundary.
6. Propose the lowest-risk mitigation.
7. Define user-visible recovery checks and monitoring improvements.

## Investigation Record

| Hypothesis | Supporting evidence | Contradicting evidence | Test | Result |
|---|---|---|---|---|
|  |  |  |  |  |

## Timeline

| Time (UTC) | Observation / action | Result |
|---|---|---|
| 13:55 | DNSSEC key publication job completes | Reported successful |
| 14:07 | Fresh dependency calls fail | Existing connections still succeed |
| 14:09 | Configured resolver returns `SERVFAIL` | Failure reproduced |
| 14:12 | Error-rate alert pages application on-call | Investigation begins |

## Decision points

- Do you fail over to another approved resolver, restore authoritative data, or
  wait for cache expiry? What evidence permits that choice?
- Is a temporary address override safe for this dependency?
- Which caches may preserve either the failure or the fix?

State the blast radius, reversibility, owner, expected signal, and rollback
trigger for every action.

## Mitigation and recovery

Mitigate at the earliest confirmed failing boundary. Prefer restoring the
approved resolution path or using an already-approved redundant path. Do not
turn an emergency address override into unmanaged configuration.

Recovery requires:

- Repeated successful queries through the configured resolver.
- A valid answer and response code from relevant authoritative servers.
- Fresh application instances resolving, connecting, and completing requests.
- User-visible errors remaining healthy through relevant positive and negative
  cache-expiry windows.

## Prevention

- Manage DNS records, delegation, and DNSSEC material as reviewed changes.
- Monitor externally observed answers, response codes, and certificate-like
  expiry windows for DNSSEC keys.
- Inventory resolver, application, and negative-cache behavior.
- Exercise resolver failover and authoritative rollback.

Each action needs an owner and measurable acceptance criterion.

## Debrief

1. Which test first separated resolution from routing or application failure?
2. Which error detail prevented a wrong diagnosis?
3. What evidence would falsify your leading causal chain?
4. Did mitigation preserve a supported, auditable resolution path?
5. Which signal proves recovery from a fresh client's perspective?

## Completion Criteria

- [ ] Resolution path and cache boundaries are explicit.
- [ ] Tests distinguish name resolution from routing, TCP, TLS, and application failure.
- [ ] Mitigation does not create an unmanaged permanent bypass.
- [ ] Recovery is verified at both DNS and user-request layers.
- [ ] Prevention addresses the causal mechanism, not only the symptom.

After completing the record, compare your work with [solution.md](solution.md).

## Authoritative sources

- [RFC 1034: Domain Names, Concepts and Facilities](https://www.rfc-editor.org/rfc/rfc1034)
- [RFC 1035: Domain Names, Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035)
- [RFC 2308: Negative Caching of DNS Queries](https://www.rfc-editor.org/rfc/rfc2308)
- [RFC 4035: DNSSEC Protocol Modifications](https://www.rfc-editor.org/rfc/rfc4035)
