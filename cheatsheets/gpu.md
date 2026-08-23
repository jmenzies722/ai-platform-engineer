# GPU diagnosis operator sheet

Diagnose from workload progress outward. Separate admission and placement,
process ownership, device health, memory allocation, data movement, kernel
execution, and multi-GPU communication before changing the workload.

## Frame the symptom

Record the job, host, container, device UUID, start time, workload phase, input
shape, precision, last known-good run, and recent code, image, driver, topology,
or scheduler changes. Decide whether the symptom is no placement, no progress,
out of memory, low throughput, high latency, numerical failure, or device loss.

Throughput without a workload unit is not actionable. Use examples per second,
tokens per second, or completed steps alongside batch, sequence length, and
phase. GPU utilization is engine activity, not proof of useful progress.

## Is the workload on the intended device?

```bash
# Read-only
nvidia-smi --query-gpu=index,uuid,name,pci.bus_id,memory.total,memory.used,utilization.gpu,temperature.gpu,power.draw --format=csv
nvidia-smi pmon -s um -c 1
nvidia-smi topo -m
```

Confirm scheduler allocation against device UUIDs, not only mutable indices.
Join GPU processes to the container, pod, job, user, and command through the
platform's trusted inventory. A visible device can still be the wrong model,
partition, topology, or tenant.

`nvidia-smi` samples device-level counters. A short sample can miss bursts, and
a process list can race with process exit. Preserve the timestamp and host.
Do not kill an unknown process merely because it owns memory.

## Is the device or driver unhealthy?

```bash
# Read-only; privilege may be required for kernel logs
nvidia-smi -q -d ECC,ERROR,PERFORMANCE,POWER,TEMPERATURE
journalctl -k --since "<incident-start>" --no-pager
```

Correlate Xid events, ECC changes, PCIe errors, device disappearance, resets,
thermal limits, and power limits with the exact device and incident window.
Corrected ECC is evidence, not automatically the root cause. A device reset can
terminate every colocated context and destroy debugging evidence.

Quarantine or reset only through the platform runbook after identifying
affected tenants and checkpoint state. Escalate repeated hardware errors,
uncontained faults, or a device missing from inventory.

## Is memory the first failing constraint?

Build a phase-specific ledger for weights, optimizer state, gradients,
activations, KV cache, communication buffers, runtime workspaces, graphs,
allocator reservations, peer contexts, and other processes.

```bash
# Read-only
nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name,used_memory --format=csv
```

Capture the failed allocation size, free bytes, live allocated bytes, reserved
bytes, peak bytes, shape, and phase from the framework's approved diagnostics.
Interpret the evidence:

- Peak demand exceeds total usable memory: capacity or admission failure.
- Reserved memory grows while live allocations remain flat: fragmentation or
  allocator retention is plausible.
- Live allocations grow across equivalent iterations: retained references or a
  leak is plausible.
- An unexpected process owns memory: placement or lifecycle failure.
- Failure occurs only for rare shapes: admission ignored peak shape.

Free bytes alone cannot distinguish these cases. Do not begin with cache
clearing, process termination, or automatic retry; each can erase evidence or
synchronize the fleet into repeated OOM.

## Is useful compute starved?

Compare a representative steady-state window, not startup, compilation, data
loading, or checkpointing. Inspect CPU time, storage and network throughput,
host-to-device copy time, kernel time, launch gaps, achieved occupancy, and
memory bandwidth with the profiler approved for the environment.

- Long gaps before kernels implicate input, CPU, synchronization, or launch
  overhead.
- Small repeated kernels implicate launch overhead or insufficient fusion.
- High memory throughput with low arithmetic work suggests a bandwidth-bound
  kernel.
- High arithmetic utilization does not prove correct results or end-to-end
  throughput.
- Frequent device synchronization can serialize otherwise independent work.

Profiling changes timing and can expose tensor shapes or data. Reproduce on a
bounded, non-sensitive workload first; capture a production profile only with
the applicable approval.

## Is multi-GPU communication blocking progress?

Confirm rank-to-device mapping, world size, collective order, topology, link
health, and whether every rank reached the same operation. One failed or slow
rank can make all peers appear hung.

Use per-rank logs with monotonic step identifiers and bounded collective
timeouts. Compare single-device behavior with the same per-device workload.
If one device is healthy but scaling regresses, separate communication volume,
load imbalance, input skew, topology, and synchronization.

Do not enable broad debug logging indefinitely; it can disclose topology and
environment data and can materially change timing.

## Controlled changes

Before mutation, define the baseline workload, expected gain, correctness
tolerance, memory guardrail, rollback, and one variable to change.

Lowering batch or sequence length tests peak-memory pressure but changes the
workload. Changing precision can alter quality and numerical stability.
Recompilation can move warm-up cost and workspace demand. Moving ranks can
change both topology and contention. Validate output quality as well as speed.

Stop and escalate for suspected hardware failure, cross-tenant ownership,
driver or firmware changes, device resets, persistent numerical corruption,
unrecoverable checkpoints, or any action whose blast radius is unknown.

## Authoritative sources

- [NVIDIA System Management Interface](https://docs.nvidia.com/deploy/nvidia-smi/)
- [NVIDIA GPU Debug Guidelines](https://docs.nvidia.com/deploy/gpu-debug-guidelines/)
- [CUDA C++ Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/)
- [PyTorch CUDA semantics](https://docs.pytorch.org/docs/stable/notes/cuda.html)
- Repository lesson: [GPU Systems](../29-gpu-systems/README.md)
