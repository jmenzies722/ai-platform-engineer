# Facilitator Notes: DNS Resolution Failure

This is not a single-answer incident. The scaffold intentionally omits final logs so the investigator must create or receive evidence. A credible solution demonstrates boundary isolation rather than guessing “DNS.”

## Expected Reasoning

1. Confirm the failure is hostname-specific and affects fresh resolution or connection attempts.
2. Preserve the application’s resolver error. `NXDOMAIN`, `SERVFAIL`, timeout, refusal, and local lookup failure imply different paths.
3. Compare application behavior with `getent`, which uses the host’s name-service configuration. Use `dig` to query a named DNS server and separate resolver-library behavior from server behavior.
4. Inspect `/etc/nsswitch.conf`, `/etc/resolv.conf`, local caching services, search suffixes, and environment-specific resolver configuration.
5. Query the configured resolver, then authoritative servers where safe and permitted. Check record type, owner name, answer, authority, TTL, and DNSSEC-related errors.
6. Test IP routing and the dependency port separately. Successful direct IP access can narrow the fault, but it does not prove every non-DNS layer healthy.

## Example Causal Chains

- A record was removed while dependent caches held different TTL state.
- A resolver configuration changed to an unreachable nameserver.
- A search-domain change made a short hostname resolve differently.
- An authoritative delegation or DNSSEC chain became invalid.
- A local cache retained a negative answer.

Each chain requires different evidence and prevention.

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

## Prevention Questions

- Are DNS records and dependencies managed as reviewed code?
- Are resolver failures distinguished by reason in telemetry?
- Are critical records monitored from relevant network locations?
- Are cache, TTL, retry, and connection-reuse behaviors understood?
- Does the service have a safe degradation or dependency-isolation strategy?

## Authoritative References

- **REQUIRED** — [RFC 1034: Domain Names—Concepts and Facilities](https://www.rfc-editor.org/rfc/rfc1034) — IETF — resolver and domain-system model.
- **REQUIRED** — [RFC 1035: Domain Names—Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035) — IETF — DNS messages and implementation behavior.
- **RECOMMENDED** — [resolv.conf(5)](https://man7.org/linux/man-pages/man5/resolv.conf.5.html) — Linux man-pages project — resolver configuration semantics.
- **RECOMMENDED** — [getent(1)](https://man7.org/linux/man-pages/man1/getent.1.html) — Linux man-pages project — queries through configured name-service databases.
