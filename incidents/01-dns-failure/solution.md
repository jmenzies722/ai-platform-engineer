# Facilitator solution: DNS Resolution Failure

This is one evidence-supported path, not permission to skip investigation. A
credible solution demonstrates boundary isolation rather than guessing “DNS.”

## Diagnosis

The configured recursive resolver returns `SERVFAIL` because validation of the
authoritative DNSSEC chain fails after incorrect key material was published.
Existing application connections briefly hide impact because they do not need a
fresh lookup.

## Reasoning from evidence

1. Confirm the failure is hostname-specific and affects fresh resolution or connection attempts.
2. Preserve the application’s resolver error. `NXDOMAIN`, `SERVFAIL`, timeout, refusal, and local lookup failure imply different paths. Here both the application and configured resolver produce `SERVFAIL`.
3. Compare application behavior with `getent`, which uses the host’s name-service configuration. Use `dig` to query a named DNS server and separate resolver-library behavior from server behavior.
4. Inspect `/etc/nsswitch.conf`, `/etc/resolv.conf`, local caching services, search suffixes, and environment-specific resolver configuration.
5. Query the configured resolver, then authoritative servers where safe and permitted. Check record type, owner name, answer, authority, TTL, and DNSSEC-related errors. A validating query fails while an explicitly non-validating diagnostic query returns data; DNSSEC validation traces identify the broken key chain.
6. Test IP routing and the dependency port separately. Successful direct IP access can narrow the fault, but it does not prove every non-DNS layer healthy.
7. Correlate the first `SERVFAIL` with the DNSSEC publication job, then compare
   published DS, DNSKEY, and signatures with the approved change artifact.

The route and cached-IP success contradict a general network outage. Healthy
application CPU and successful reused connections contradict application
saturation. `SERVFAIL` does not by itself prove DNSSEC, so the validating versus
non-validating test and chain inspection are required.

## Discriminating investigation

| Test | Expected observation | What it establishes |
|---|---|---|
| Query the configured recursive resolver | Repeatable `SERVFAIL` | Reproduces the application path |
| Query an authoritative server directly | Authoritative data is reachable | Resolver transport is not the only issue |
| Compare validation-enabled and diagnostic non-validating queries | Validation fails; unsigned diagnostic answer is present | Narrows failure to validation |
| Trace DS, DNSKEY, and RRSIG records | Published keys do not form the approved chain | Identifies the broken handoff |
| Query from another validating resolver | Same validation failure | Rules out one local resolver cache |

## Example Causal Chains

- A record was removed while dependent caches held different TTL state.
- A resolver configuration changed to an unreachable nameserver.
- A search-domain change made a short hostname resolve differently.
- An authoritative delegation or DNSSEC chain became invalid.
- A local cache retained a negative answer.

Each chain requires different evidence and prevention.

## Decision analysis

Restore the last known-good DNSSEC material through the authoritative change
path, or complete the intended key publication if its matching material is
available and verified. Canary with authoritative and validating queries before
expanding. Resolver failover is useful only if the alternate path can validate
the chain; moving all traffic to another validating resolver does not repair
bad authoritative data.

Do not disable DNSSEC validation globally. Do not hard-code an address unless a
pre-approved, owned break-glass path exists with an expiry and removal check.

## Mitigation sequence

1. Freeze further key automation and capture the served chain, serials, TTLs,
   job revision, and approval artifact.
2. Restore matching approved DS and DNSKEY material at the authoritative layer.
3. Query authoritative servers directly and then one validating recursive
   resolver.
4. Expand only after every authoritative target serves the intended material.
5. Track negative and failure cache windows while fresh application requests
   recover.

## Unsafe “Fixes”

- Hard-coding an address in application code or `/etc/hosts` without ownership and expiry.
- Restarting every component before capturing evidence.
- Flushing caches globally without understanding load and consistency effects.
- Lowering all TTLs permanently; this increases resolver dependency and query load.

## Recovery Proof

- The configured resolution path returns the intended record repeatedly.
- Fresh application instances can resolve and connect.
- End-user requests recover within the defined threshold.
- Error and latency indicators remain healthy through relevant cache-expiry windows.
- Any temporary bypass has an owner, expiry, and removal verification.

## Debrief

- `SERVFAIL` identified a class of resolver failure, not its cause.
- Existing connections delayed visible impact and made one HTTP probe
  misleading.
- The decisive evidence crossed application, recursive-resolver, and
  authoritative boundaries.
- Prevention must validate what is actually served, not merely whether an
  automation job reports success.

## Prevention Questions

- Are DNS records and dependencies managed as reviewed code?
- Are resolver failures distinguished by reason in telemetry?
- Are critical records monitored from relevant network locations?
- Are cache, TTL, retry, and connection-reuse behaviors understood?
- Does the service have a safe degradation or dependency-isolation strategy?

## Authoritative References

- **REQUIRED** — [RFC 1034: Domain Names—Concepts and Facilities](https://www.rfc-editor.org/rfc/rfc1034) — IETF — resolver and domain-system model.
- **REQUIRED** — [RFC 1035: Domain Names—Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035) — IETF — DNS messages and implementation behavior.
- **REQUIRED** — [RFC 4035: Protocol Modifications for DNSSEC](https://www.rfc-editor.org/rfc/rfc4035) — IETF — resolver validation behavior.
- **RECOMMENDED** — [resolv.conf(5)](https://man7.org/linux/man-pages/man5/resolv.conf.5.html) — Linux man-pages project — resolver configuration semantics.
- **RECOMMENDED** — [getent(1)](https://man7.org/linux/man-pages/man1/getent.1.html) — Linux man-pages project — queries through configured name-service databases.
