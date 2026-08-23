# Virtualization and Cloud

Virtualization turns physical computers into isolated logical machines, and cloud platforms make those machines available through APIs.

## Why it matters

**Prerequisite:** [Distributed Systems](./09-distributed-systems.md).

Dedicated servers were slow to provision and often sat mostly idle. Hypervisors let operators divide one physical machine into isolated virtual machines, improving utilization without requiring applications to share one operating-system instance.

Cloud platforms exposed pooled compute, network, and storage through APIs. Provisioning became faster, but finite capacity, tenancy, cost, asynchronous control planes, and provider contracts became part of normal system design.

## How it works

Cloud is a distributed control plane that reconciles declared resource records with leased physical capacity; “elastic” means automation around finite pools.

A hypervisor mediates CPU, memory, and devices. Cloud control planes authenticate API calls, persist desired resources, schedule capacity, configure networking and storage, then report lifecycle state asynchronously.

Hardware-assisted virtualization reduces trap overhead, but noisy neighbors and device topology remain. Availability zones limit correlated failures; they do not eliminate them. Object storage trades filesystem semantics for scalable API-managed durability.

## Vocabulary

- **Hypervisor:** Software or firmware that runs and isolates virtual machines.
- **Virtual machine (VM):** A logical machine with virtual hardware and its own guest OS.
- **Image:** A reusable template for a machine or workload filesystem and configuration.
- **Tenancy:** The way resources and boundaries are shared among customers or workloads.
- **Region:** A cloud provider's geographic service area.
- **Availability zone:** An isolated infrastructure location within a region.
- **Elasticity:** Adjusting allocated capacity as demand changes.
- **Quota:** An enforced limit on resource consumption or creation.
- **Control plane:** APIs and decision systems that manage desired infrastructure state.
- **Data plane:** Resources that handle the workload's actual traffic or computation.
- **IAM:** Identity and access management for authenticating principals and authorizing actions.

## See it yourself

```text
POST /instances {image, cpu, memory, zone, idempotency_key}
202 Accepted {operation_id}
GET /operations/{id} returns pending | succeeded | failed
```

Predict the first response to a create request and the later states returned for its operation ID. The immediate result should be `202 Accepted`, with completion learned asynchronously. This supports the distinction between accepted intent and realized infrastructure. It does not prove that capacity exists, that retries are safe without the key, or that a successful control-plane record means the VM is usable.

## Where it shows up

A request for eight GPUs can fail despite unused regional quota. The chosen zone may lack eight compatible devices on one host or fabric, while capacity elsewhere cannot satisfy the placement constraint. Quota authorizes consumption; inventory and topology determine allocatability. Cloud APIs hide the physical pool during ordinary operation, but placement failures expose it.

## When it breaks

A resource can remain `pending` until a client times out. Quota may be exhausted, zonal inventory may be unavailable, identity policy may deny a dependent action, or an asynchronous network step may be stuck. First preserve the operation ID and inspect its events, requested zone, quota, capacity class, and authorization decision before issuing another create.

## Practice

### Observe

Model a VM lifecycle from requested to terminated and list compensating actions for failure at each transition.

### Build

Write a mock cloud allocator with zones, finite CPU/GPU pools, idempotent requests, and asynchronous status.

### Break

Exhaust quota, remove zonal capacity, repeat requests, and fail network setup. Prevent leaked allocations.

### Say it out loud

Explain why cloud capacity is not the same as quota.

**Success:** Include asynchronous control-plane state, physical placement, one correlated failure domain, and a useful operation record.

## Check yourself

1. What differs between virtualization and cloud?
2. Why are cloud creates asynchronous?
3. What does shared responsibility imply?

### Interview stretch

- Diagnose pending GPU instances.
- Compare block and object storage.
- Explain zonal resilience without claiming zero downtime.

## Sources

### REQUIRED

- “Amazon EC2” — Amazon Web Services. [Official EC2 documentation](https://docs.aws.amazon.com/ec2/). Canonical description of production VM resource abstractions.

### RECOMMENDED

- “The NIST Definition of Cloud Computing” — Mell and Grance, NIST. [NIST SP 800-145](https://doi.org/10.6028/NIST.SP.800-145). Defines cloud characteristics and service models precisely.

### DEEP DIVE

- “Formal Requirements for Virtualizable Third Generation Architectures” — Popek and Goldberg. [ACM DOI](https://doi.org/10.1145/361011.361073). Establishes foundations of machine virtualization.

## Next

Continue with [./11-devops.md](./11-devops.md).
