# 11 — Distributed GPU Capacity Planner and Simulator

Build a discrete-event planner in an independent repository. It should make scheduling and economics decisions inspectable without requiring access to a real accelerator fleet.

## Problem and users

AI infrastructure teams must choose fleet shape, topology, placement, queue policy, checkpoint cadence, and capacity before hardware is available. Researchers care about job completion; finance cares about useful work per dollar; operators care about failures and fragmentation. Spreadsheet averages hide queueing and correlated failure behavior.

## Constraints and simulation contract

- Model heterogeneous GPU types, node/rack topology, network/storage limits, distributed jobs, reservations, preemption, checkpoints, and failures.
- Consume versioned workload traces or synthetic generators and produce deterministic event logs for a fixed seed.
- Validate reduced cases analytically and calibrate assumptions from published or measured evidence.
- Do not claim cycle-accurate hardware fidelity, build a real scheduler, or optimize to undocumented vendor behavior.

## Architecture expectations

Separate workload/fleet schemas, event engine, resource/topology model, placement policies, failure/recovery model, metrics, experiment runner, and report generation. Define ordering for simultaneous events and invariants preventing impossible allocation. Represent compute, communication, input, checkpoint, restart, and queue time distinctly. Quantify uncertainty rather than presenting one forecast.

## Milestone plan

1. Publish assumptions, schemas, invariants, analytical test cases, and baseline FIFO simulation.
2. Add topology-aware placement, gang scheduling, heterogeneity, fragmentation, and fair-share queues.
3. Add storage/network contention, checkpoints, preemption, node/rack failures, and recovery.
4. Calibrate, run sensitivity experiments, compare policies, and deliver a capacity recommendation.

## Required artifacts

- Simulator specification, event/state diagrams, schema/version docs, ADRs, and invariant catalog.
- Validation suite against hand calculations and at least one public workload or benchmark source.
- Reproducible experiment manifests, raw event logs, notebooks or reports, and uncertainty analysis.
- Executive capacity recommendation covering service levels, utilization, resilience, and cost.

## Tests and failure drills

Use unit, property, determinism, conservation, and metamorphic tests; check that more capacity cannot worsen a no-contention case. Drill GPU/node/rack loss, checkpoint-storage slowdown, network oversubscription, starvation, head-of-line blocking, workload estimation error, correlated arrivals, and policy misconfiguration. Test event storms and very long virtual time for numerical and memory stability.

## Observability, security, and cost

Expose queue wait, slowdown, makespan, useful GPU time, fragmentation, preemption waste, recovery time, network/storage saturation, fairness, and event-engine performance. Treat imported traces as sensitive: validate schemas, sandbox parsers, remove identifiers, and record provenance. Model purchase or rental, power proxy, idle time, storage/network, checkpoint overhead, and cost per successful job/useful GPU-hour.

## Explicit success rubric

| Quality | Pass condition |
|---|---|
| Correctness | Invariants and analytical cases pass; fixed inputs produce byte-stable normalized results. |
| Fidelity | Calibration gaps and model limits are quantified, not concealed. |
| Decision value | At least three policies are compared under baseline and adverse workloads with a defensible recommendation. |
| Resilience | Correlated failures and recovery alter completion/cost as predicted by documented mechanisms. |
| Communication | An infrastructure review can reproduce every chart from manifests and event logs. |

## Stretch work

Add trace-driven power modeling, carbon-aware scheduling, elastic distributed jobs, or optimization that proposes fleet mixes and verifies them through simulation.

## Authoritative sources

- [The Roofline Model](https://doi.org/10.1145/1498765.1498785)
- [MLPerf Training benchmark](https://mlcommons.org/benchmarks/training/)
- [Pollux: Co-adaptive Cluster Scheduling for Goodput-Optimized Deep Learning](https://www.usenix.org/conference/osdi21/presentation/qiao)
- [NVIDIA Collective Communications Library documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/)

## Mapped modules

[06 Data Structures and Algorithms](../../06-data-structures-algorithms/README.md), [17 Distributed Systems](../../17-distributed-systems/README.md), [29 GPU Systems](../../29-gpu-systems/README.md), [30 AI Infrastructure](../../30-ai-infrastructure/README.md), and [34 System Design](../../34-system-design/README.md).
