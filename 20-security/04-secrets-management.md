# Secrets and credential lifecycles

A secret is a bootstrap liability, not a configuration convenience. Reduce secret count, scope, and lifetime; deliver remaining secrets through authenticated channels and make rotation routine.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Inventory owner, consumer, issuer, scope, storage, delivery, rotation, expiry, and revocation. Prefer workload identity and short-lived credentials over static keys. A secret manager encrypts storage and controls retrieval, but applications still expose values through environment dumps, process arguments, logs, crash reports, or child processes.

Use separate identities to fetch only required values, cache briefly with explicit expiry, and support overlap during rotation. Secret zero is resolved through platform identity, hardware root, or operator ceremony, not by embedding another long-lived token.

## See it yourself

A one-year credential exposed on day one offers roughly a year of reuse; a fifteen-minute credential bounds direct reuse to minutes if revocation is unavailable. Short lifetime does not erase permissions already used, but it sharply reduces replay opportunity.

## Where it shows up

Database passwords, signing keys, API credentials, and recovery codes require different handling and blast-radius analysis. Monitor unusual retrieval and use without logging values.

## When it breaks

Repository history preserves deleted keys, copied environment variables outlive rotation, and simultaneous cutover can cause outage. On exposure, revoke or rotate first, investigate use, and purge copies as defense in depth.

## Practice

Create a fake-secret inventory and a two-version rotation procedure. Inject one leaked old value and one failed consumer reload. Completion means overlap preserves availability, old use is rejected after cutover, and logs contain identifiers but never values.

## Check yourself

1. Why is a secret manager not sufficient by itself?
2. What is secret zero?
3. How does overlap make rotation safer?
4. What action comes first after confirmed exposure?

## Sources

### REQUIRED

- [NIST SP 800-57 Part 1 Rev. 5](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)

### RECOMMENDED

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

### DEEP DIVE

- [RFC 9700: OAuth 2.0 Security Best Current Practice](https://www.rfc-editor.org/rfc/rfc9700)

## Next

[Software supply chain and container security](05-supply-chain-and-containers.md)
