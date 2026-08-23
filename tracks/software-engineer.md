# Software Engineer Track

## Outcome role

An engineer who can turn requirements into tested, maintainable software; reason from source code to runtime behavior; use data structures and storage deliberately; and operate a service with honest reliability boundaries. This is a broad software path, not a reduced backend or infrastructure path.

## Prerequisites

- Command-line access and willingness to work in disposable environments.
- Basic comfort editing text and running programs. Prior professional experience is not required.
- Evidence-based study practices from [How to Learn](../HOW-TO-LEARN.md).

## Ordered module path

| Order | Module | Why it is here |
|---:|---|---|
| 1 | [00 History](../00-history/README.md) | Establishes why current abstractions and operating practices exist; use selectively for context. |
| 2 | [01 Software Foundations](../01-software-foundations/README.md) | Connects source, process, resources, interfaces, failure, and evidence. |
| 3 | [02 Python](../02-python/README.md) | Builds one language deeply enough to express, test, and package real programs. |
| 4 | [05 Git](../05-git/README.md) | Makes change history, collaboration, recovery, and review deliberate. |
| 5 | [06 Data Structures and Algorithms](../06-data-structures-algorithms/README.md) | Supplies complexity and representation tools for defensible implementation choices. |
| 6 | [03 Computer Systems](../03-computer-systems/README.md) | Explains CPU, memory, privilege, filesystems, and I/O beneath a runtime. |
| 7 | [04 Linux](../04-linux/README.md) | Turns systems models into process and host diagnosis. |
| 8 | [07 Networking](../07-networking/README.md) | Makes request behavior explainable across DNS, transport, TLS, and HTTP. |
| 9 | [08 Databases](../08-databases/README.md) | Adds constraints, indexes, concurrency, durability, recovery, and caching. |
| 10 | [09 Backend Engineering](../09-backend-engineering/README.md) | Integrates untrusted requests, authorization, durable work, deadlines, queues, and overload. |
| 11 | [11 Software Architecture](../11-software-architecture/README.md) | Develops boundaries, coupling, evolution, and explicit tradeoff records. |
| 12 | [18 Observability](../18-observability/README.md) | Makes production claims testable with useful telemetry. |
| 13 | [34 System Design](../34-system-design/README.md) | Integrates requirements, data ownership, scale, reliability, and recovery into reviewable designs. |

[10 Go](../10-go/README.md) is a recommended second-language module after Computer Systems when concurrency, services, or systems tooling matters. It is not required merely to collect another syntax.

## Required practice

### Labs

- [Inspect One Python Process](../labs/01-software-execution/README.md)
- [Diagnose a Slow Linux Workload](../labs/02-linux-diagnosis/README.md)
- [Recover Git Work](../labs/03-git-recovery/README.md)
- [Debug DNS, TCP, TLS, and HTTP](../labs/04-network-dns-tls/README.md)
- [Observe PostgreSQL and Redis](../labs/05-postgres-redis/README.md)
- [Engineer Backend Reliability](../labs/06-backend-reliability/README.md)
- [Investigate OpenTelemetry Traces](../labs/11-opentelemetry-traces/README.md)

### Incident drills

- [DNS resolution failure](../incidents/01-dns-failure/README.md)
- [Memory exhaustion and OOM kill](../incidents/02-oom/README.md)
- [Database pool exhaustion](../incidents/05-database-pool-exhaustion/README.md)
- [Database deadlock](../incidents/09-deadlock/README.md)

### Projects

Complete [Systems Inspector and Capacity Probe](../projects/01-systems-inspector/README.md), then [Production Change-Request API](../projects/02-production-api/README.md). Add [Network Failure Laboratory](../projects/03-network-failure-lab/README.md) when networking diagnosis is central to the intended role.

## Competency gates

**[Foundations gate](../assessments/gates/foundations.md):** independently implement and test a bounded program, trace its execution through runtime and machine state, repair an evidence defect, and explain what the observations do not prove.

**[Systems, Linux, and networking gate](../assessments/gates/systems-linux-networking.md):** recover Git state, defend representation and complexity choices, and diagnose a controlled CPU, memory, descriptor, disk, DNS, or connection fault from OS and protocol evidence.

**Service engineering outcome evidence:** build and operate an authenticated, persistent API with migrations, object-level authorization, bounded concurrency, idempotency assumptions, telemetry, load evidence, and a rehearsed recovery. A design review must defend data ownership, failure domains, and capacity assumptions.

## Certification overlays

No certification is required. [AWS Certified DevOps Engineer - Professional (DOP-C02)](../certs/aws-dop-c02.md) is usually not aligned with this general software outcome. If the target role owns substantial AWS delivery and operations, use it with the [AWS module](../12-aws/README.md); it remains optional and does not replace service evidence.
