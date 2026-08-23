# Cloud and application security

Cloud and application security meet at identity and untrusted input: every request, object reference, metadata endpoint, storage policy, and managed-service call must preserve tenant and trust boundaries.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Cloud design separates accounts or projects, networks, identities, keys, logs, and guardrails by environment and blast radius. Block public access by policy, restrict egress, protect metadata credentials, centralize immutable audit evidence, and evaluate configuration continuously.

Applications validate syntax and semantics, encode output for its context, parameterize queries, enforce authorization on every object, protect state-changing browser requests, and bound uploads, parsing, and outbound fetches. SSRF defenses validate destinations after resolution, restrict schemes and egress, and resist redirects and DNS rebinding.

## See it yourself

Parameterization separates query structure from values, so a value cannot become SQL syntax through quoting tricks. It does not enforce authorization or make a logically unsafe query safe; each control addresses a distinct invariant.

## Where it shows up

A file service should authenticate, authorize tenant ownership, validate size and type, store outside executable paths, scan asynchronously with fail-closed policy, and serve through a separate origin with safe headers.

## When it breaks

Public storage, wildcard IAM, injection, cross-tenant IDOR, SSRF, unsafe deserialization, and parser bombs often compose. Test negative paths and inspect cloud audit logs, application decisions, network egress, and object ownership together.

## Practice

Build threat-driven tests for a document API: cross-tenant read, parameter injection, oversized upload, and outbound request to a link-local address. Completion means each fails at the intended boundary and emits a bounded security event.

## Check yourself

1. Why does input validation not replace output encoding?
2. How does SSRF become cloud credential theft?
3. What control prevents cross-tenant object access?
4. Which guardrail limits accidental public storage?

## Sources

### REQUIRED

- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)

### RECOMMENDED

- [CIS Critical Security Controls](https://www.cisecurity.org/controls)

### DEEP DIVE

- [OWASP Server Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)

## Next

[Security detection and incident response](07-security-incident-response.md)
