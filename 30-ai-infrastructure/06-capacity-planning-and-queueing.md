# Capacity planning and queueing

Capacity planning converts demand distributions and service objectives into topology-qualified supply, reservations, and admission policy.

## Why it matters

Average utilization can be low while large gangs wait for hours. Bursts, fragmentation, maintenance, failures, and heterogeneous shapes determine whether capacity is useful.

## How it works

Describe demand by accelerator type, gang shape, duration, deadline, topology, and preemptibility. Describe supply after health, maintenance, reservations, and failure headroom. Queueing delay rises nonlinearly near saturation, while gang scheduling adds a shape constraint. Backfill uses otherwise idle gaps without delaying a reservation; fair-share corrects historical consumption; priority handles explicit business consequence.

Little's Law, \(L=\lambda W\), checks stable averages. It cannot predict tails or rescue an unstable queue. Scenario planning should replay traces under node loss, demand growth, and changed job mixes. Capacity is accepted when target wait and completion quantiles hold, not when a monthly average looks comfortable.

## See it yourself

A pool completes 20 eight-GPU jobs per day and receives 22. The backlog grows by two jobs daily regardless of short-term utilization charts. If arrivals average 18 but cluster maintenance removes 20% of supply weekly, the relevant service rate may still be below demand. Stability requires long-run arrival work below effective service capacity.

## Where it shows up

Teams reserve latency-sensitive inference and backfill preemptible research into remaining shapes. Capacity reviews separate allocated, active, useful, stranded, unhealthy, and reserved GPU-hours and segment wait by job class.

## When it breaks

Over-requesting hides supply; one rare shape dominates tail wait; reservations go unused; preemption loses more work than it recovers. Inspect queue age, reasons, free shapes, runtime estimates, checkpoint age, and useful utilization. Never infer a purchase solely from pending count.

## Practice

**Observe:** replay one week of synthetic arrivals. **Build:** compare FIFO, backfill, and fair-share. **Break:** fragment nodes and underestimate runtime. Completion requires p50 and p95 wait, preempted work, stranded capacity, and one policy tradeoff.

## Check yourself

1. Why can 30% free capacity fail an eight-GPU request?
2. What assumption makes Little's Law applicable?
3. When does backfill violate its promise?

## Sources

### REQUIRED

- [Kubernetes scheduling framework](https://kubernetes.io/docs/concepts/scheduling-eviction/scheduling-framework/)

### RECOMMENDED

- [Google SRE: handling overload](https://sre.google/sre-book/handling-overload/)

### DEEP DIVE

- [Omega cluster scheduler](https://research.google/pubs/omega-flexible-scalable-schedulers-for-large-compute-clusters/)

## Next

Continue to [Infrastructure economics and efficiency](07-infrastructure-economics-and-efficiency.md).
