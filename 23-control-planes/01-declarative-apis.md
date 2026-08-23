# Declarative APIs and desired state

A declarative API records durable intent and exposes observed state without requiring clients to orchestrate provider steps. Its resource contract is the boundary that allows independent clients and controllers to evolve safely.

## Why it matters

Imperative provisioning scripts lose progress and intent when interrupted. A durable resource supports retries, policy, drift correction, asynchronous status, and multiple clients without embedding workflow order in each caller.

## How it works

Define stable identity and metadata, user-owned desired `spec`, and controller-owned `status`. Desired fields express outcomes rather than provider procedure. Status reports observations, external identity, last successful observation, and conditions with type, state, reason, message, transition time, and observed generation.

Default before persistence so readers see effective intent. Validate syntax, cross-field invariants, authorization, quota, and supported transitions at the earliest reliable boundary. Admission cannot validate facts that may change asynchronously; those become conditions during reconciliation.

Specify field mutability, default ownership, merge behavior, optimistic concurrency, and delete semantics. Use resource versions or entity tags to prevent lost updates. Separate request acceptance from readiness: create may return a durable resource before an external database exists.

Conditions are observations, not an append-only event log. They should answer stable questions such as `Ready`, `Progressing`, and `Degraded`; reasons provide machine-groupable detail. An observed generation proves which desired revision the status describes.

## Vocabulary

- **desired state:** persisted outcome requested by an authorized user
- **observed state:** controller's latest evidence about actual reality
- **generation:** revision of desired state
- **condition:** structured current observation about an aspect of resource state

## See it yourself

Given `Database.spec.endpoint` and `Database.status.size`, predict the ownership conflict. Endpoint is provider-derived and belongs in observed state; requested capacity belongs in desired state. Move them, then update spec from 10 to 20 while status still observes generation 4 at size 10. A client must not report the new intent ready until status observes generation 5.

## Where it shows up

A database API accepts engine, class, region, backup policy, and owner. It returns stable resource identity immediately, then status exposes external ID, endpoint, actual version, and readiness. Provider-specific operation IDs remain status detail rather than desired user intent.

## When it breaks

Controllers overwrite desired fields, clients infer readiness from object existence, and stale status is presented for new intent. Defaults change meaning without persistence. Unknown provider state is reported as absent. Detect with schema ownership tests, generation assertions, concurrency tests, and condition-transition traces.

## Practice

**Observe:** take an imperative provisioning sequence and classify each input, derived value, operation state, and external fact as desired state, observed state, or event.

**Build:** design a database resource schema with defaults, validation, mutability, concurrency, status, conditions, and create, resize, and delete semantics.

**Break:** update size twice before the first operation completes and deliver stale status. Show how generation and resource version prevent a false-ready result and lost update.

**Say it out loud:** explain why accepted, progressing, and ready are distinct API states.

## Check yourself

1. Why should provider-derived endpoints usually live in status?
2. What does observed generation protect clients from?
3. Which validation belongs at admission and which belongs in reconciliation?
4. When should changing a field require replacement?

## Sources

### REQUIRED

- [Kubernetes API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)

### RECOMMENDED

- [Kubernetes API concepts](https://kubernetes.io/docs/reference/using-api/api-concepts/)

### DEEP DIVE

- [CNCF Operator whitepaper](https://github.com/cncf/tag-app-delivery/blob/main/operator-wg/whitepaper/Operator-WhitePaper_v1-0.md)

## Next

Continue to [Reconciliation, queues, and convergence](02-reconciliation.md).
