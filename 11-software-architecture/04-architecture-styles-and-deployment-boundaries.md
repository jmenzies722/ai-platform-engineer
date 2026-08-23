# Architecture Styles and Deployment Boundaries

An architecture style is a set of constraints that makes some changes and failures easier while charging for others.

## Why it matters

Calling a system “microservices” does not reveal whether services own data, can deploy independently, or merely perform remote calls in a cycle. Style labels become dangerous when they replace analysis. Choose boundaries from quality scenarios, reasons to change, team ownership, and operational capability, then verify that the implementation honors them.

## How it works

A layered style groups responsibilities such as presentation, application, domain, and infrastructure, constraining dependency direction. It is approachable but can degrade into pass-through layers or a domain coupled to a database model. Ports and adapters place application policy behind inbound and outbound contracts, making adapters replaceable and tests direct; indiscriminate interfaces add translation without hiding change.

A modular monolith gives modules explicit contracts and data ownership while deploying one process. It avoids network partial failure and distributed operations while preserving many source boundaries. Its risks are bypass through shared memory or tables and whole-process deployment coupling. Enforce module APIs with build rules and tests rather than folder names.

Services add independent process and deployment boundaries. They can isolate scaling and ownership, but every call introduces latency, authentication, versioning, observability, and partial failure. A distributed monolith gets those costs while requiring synchronized releases. Service boundaries are strongest around business capabilities and owned data, not technical layers such as “validation service.”

Event-driven styles publish facts or intents for asynchronous consumers, improving temporal decoupling and fan-out while adding duplicate delivery, lag, ordering, schema evolution, and difficult end-to-end reasoning. Pipes and filters fit transformations with clear stages and data contracts. A system can combine styles: a modular monolith may use ports internally and publish events to an analytics pipeline.

Deployment boundaries should follow the need for independent release, scaling, isolation, or ownership. They need not mirror every code module. The reverse is also true: putting several components in one repository does not erase runtime boundaries.

## See it yourself

Predict that the dependency check reports one forbidden import from domain policy to an HTTP adapter.

```bash
python3 - <<'PY'
deps = {
    "domain": {"http_adapter"},
    "application": {"domain"},
    "http_adapter": {"application"},
}
allowed = {
    "domain": set(),
    "application": {"domain"},
    "http_adapter": {"application", "domain"},
}
for source, targets in deps.items():
    for target in targets:
        if target not in allowed[source]:
            print("forbidden", source, "depends on", target)
PY
```

Expected observation: an executable rule catches dependency direction that a diagram alone cannot enforce.

Limits of the observation: import edges do not reveal runtime calls, shared database coupling, team coordination, generated code, or whether the proposed boundary is valuable.

## Where it shows up

A checkout product may begin as ordering, pricing, payment, and fulfillment modules in one deployment. Payment needs stricter access, independent scaling, and a provider-facing failure boundary, so it later becomes a service. Pricing remains local because every checkout needs it and its scaling matches the host. This mixed design follows scenarios rather than fashion.

## When it breaks

Circular package dependencies, cross-module table writes, coordinated release trains, chatty remote calls, and ownership tickets bouncing between teams reveal ineffective boundaries. A service with synchronous dependencies on five peers may have less failure isolation than a monolith. First map source dependencies, runtime calls, data writes, deployment units, owners, and one recent change path. Measure call counts, failure propagation, and lead time before redrawing boxes.

## Practice

**Build:** express one feature as layered, modular-monolith, and service designs, including code, runtime, data, deployment, and team boundaries. **Break:** simulate one dependency timeout and one incompatible deployment in each design. **Explain back:** score the options against named quality scenarios and operating capability. Success is a decision that names costs, rejects at least one style for evidence, and includes an incremental path rather than a rewrite.

## Check yourself

1. What distinguishes a code module from a deployment boundary?
2. How does a distributed monolith acquire service costs without service benefits?

## Sources

### REQUIRED

- [SEI: Software Architecture in Practice](https://www.sei.cmu.edu/library/software-architecture-in-practice/)
- [Parnas on decomposing systems](https://dl.acm.org/doi/10.1145/361598.361623)

### RECOMMENDED

- [Martin Fowler: Microservice Prerequisites](https://martinfowler.com/bliki/MicroservicePrerequisites.html)
- [Microsoft Architecture Styles](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/)

### DEEP DIVE

- [Patterns of Enterprise Application Architecture](https://martinfowler.com/books/eaa.html)

## Next

Continue to [Integration, Consistency, and Data Flow](./05-integration-consistency-and-data-flow.md).
