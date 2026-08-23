# Lab: Simulate GPU Scheduling and Out-of-Memory Failures

Use a deterministic discrete-event simulator to reason about GPU memory admission, fragmentation, placement, queue fairness, and retry behavior without requiring a GPU.

## Prerequisites

- Python 3.10 or newer and Bash
- No CUDA runtime, cluster, or cloud account
- Familiarity with scheduling requests and resource capacity

## Safety

This is a model, not a GPU benchmark. It allocates no device memory, launches no jobs, and runs at most 100 simulated events. Do not transfer simulated thresholds directly to production hardware without measurement.

## Setup and baseline

Create `.work/jobs.json` with twelve deterministic jobs. Each has job ID, tenant, arrival step, duration, requested GPU count, reserved memory MiB, peak memory MiB, and priority. Define two simulated GPUs with 16,384 MiB each and 512 MiB reserved for the system.

Write down expected placements for first-fit and least-used scheduling.

## Tasks

1. Implement `.work/simulate.py` with `--policy first-fit|least-used`, `--steps 100`, and `--seed 7`.
2. Admit a job only when requested count and reserved memory fit. Track queued, running, succeeded, rejected, and OOM states.
3. At the midpoint of each run, compare peak memory with remaining capacity. On OOM, fail the job and release all of its reservation exactly once.
4. Report utilization by step, queue wait by tenant, placements, OOM count, retries, and makespan as JSON.
5. Add invariants: allocated memory never exceeds allocatable memory, every GPU assignment is unique, terminal jobs hold no reservation, and each transition is valid.
6. Compare policies. Explain bin packing, head-of-line blocking, starvation, and why GPU count alone is insufficient admission information.
7. Propose production signals that would validate or falsify the simulator: allocator metrics, device telemetry, scheduler events, and workload traces.

## Evidence to keep

Keep fixture and hash, simulator source, seed, policy outputs, invariant results, queue-wait percentiles, memory timeline, OOM timeline, and assumptions about reservation versus peak usage.

## Failure injection

Add one job reserving 8,000 MiB but peaking at 17,000 MiB. It should pass naive reservation admission and fail at peak. First run a deliberately unsafe retry mode that immediately requeues it, capped at three retries; observe repeated failure and wasted capacity. Then quarantine deterministic OOM failures unless the resource request or workload changes.

Add a fragmentation scenario with free memory split across two GPUs but a job requiring one contiguous 12,000 MiB allocation. The scheduler must not sum free memory across devices for a single-device job.

## Cleanup

```bash
rm -rf .work
```

## Rubric

- 2 points: models capacity, reservations, peak use, and valid transitions
- 3 points: enforces invariants and releases resources correctly
- 2 points: demonstrates deterministic OOM and bounded retry behavior
- 2 points: compares placement fairness and fragmentation tradeoffs
- 1 point: clearly separates simulation claims from hardware evidence

## Sources

- [Kubernetes device plugins](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)
- [NVIDIA GPU Operator documentation](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/)
- [CUDA memory management](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#device-memory)
