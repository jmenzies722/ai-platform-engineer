# API evolution and compatibility

Control-plane API evolution preserves the meaning of stored intent while schemas, defaults, controllers, clients, and external providers change. Compatibility is behavioral, not merely successful decoding.

## Why it matters

Resources can live for years and outlast the binaries that created them. Changing a default, enum meaning, status condition, or delete behavior can silently mutate old intent and break automation even when the JSON still parses.

## How it works

Version the external contract and define a canonical storage representation. Convert requests at API boundaries without losing information. Conversion should be deterministic and side-effect free; provider calls belong in reconciliation. Round-trip tests prove fields survive conversion across supported versions.

Add optional fields with explicit defaulting and ownership. Persist effective defaults so later server changes do not reinterpret existing resources. Treat enum expansion carefully because old clients may reject unknown values. Never reuse removed fields or identifiers with new meaning.

Classify changes as compatible, conditionally compatible, or breaking across schema, semantics, authorization, status, timing, quotas, and failure behavior. Support overlapping controller and API versions during rollout. Gate writes when an old controller could corrupt a new representation.

For breaking changes, publish deprecation, inventory stored and active use, provide conversion or migration, verify outcomes, and retain rollback or forward-repair. External provider deprecation may force contract change; expose impact rather than silently translating to weaker guarantees.

## Vocabulary

- **storage version:** schema used for durable persistence
- **conversion:** transformation between API versions without external side effects
- **round-trip preservation:** retaining meaning through forward and reverse conversion
- **semantic compatibility:** preservation of observable contract behavior

## See it yourself

Version 1 defaults backups to false when omitted; version 2 defaults them to true. Predict what happens if omission remains unpersisted. Merely reading an old resource through version 2 changes effective intent. Persist v1's effective false or migrate explicitly. Decoding success does not preserve semantics.

## Where it shows up

A database API replaces `sizeGB` with a capacity tier. Conversion can preserve exact values only when tiers cover them. Out-of-range resources need a migration state and owner decision rather than lossy rounding hidden by the API server.

## When it breaks

Conversion drops unknown fields, rollback cannot read newly stored state, condition reasons change and break automation, and dual controllers write incompatible status. Migration jobs overload providers. Detect with storage-version inventory, round-trip property tests, old-client suites, shadow conversion, skew tests, and migration convergence metrics.

## Practice

**Observe:** classify five proposed API changes across wire, schema, semantic, operational, and client compatibility.

**Build:** design v1 and v2 of a database resource with defaulting, conversion, storage, status, migration, skew support, and rollback boundary.

**Break:** add an enum value, roll back the API server, and convert an unrepresentable capacity. Specify expected rejection or preserved unknown state without silent loss.

**Say it out loud:** explain why “additive JSON change” can still break a control-plane client.

## Check yourself

1. Why should conversion avoid provider calls?
2. When must defaults be persisted?
3. What makes an enum expansion unsafe?
4. Which evidence proves rollback is supported?

## Sources

### REQUIRED

- [Kubernetes API deprecation policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/)

### RECOMMENDED

- [Kubernetes CustomResourceDefinition versioning](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning/)

### DEEP DIVE

- [Kubernetes API changes](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api_changes.md)

## Next

Continue to [Multitenancy and security boundaries](07-multitenancy-and-security.md).
