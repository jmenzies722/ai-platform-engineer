# 01 — Systems Inspector and Capacity Probe

Build an evidence-first Linux CLI in an independent repository. This brief defines the work; no implementation belongs here.

## Problem and users

On-call engineers often see “the host is slow” before they know whether pressure comes from CPU scheduling, memory reclaim, storage, sockets, or process limits. Create a read-only inspector that turns kernel interfaces into a coherent diagnosis for application engineers and SREs. Success means a user can explain the mechanism behind every reported value and narrow an injected host fault within ten minutes.

## Constraints and scope

- Support one documented Linux distribution, cgroup v2, and unprivileged inspection first.
- Read `/proc`, `/sys`, cgroup files, and standard kernel interfaces directly; command wrappers may validate but not supply core data.
- Never mutate the inspected host. Redact command lines and environment-derived secrets by default.
- Exclude remote fleet management, automatic remediation, and a general monitoring agent.

## Architecture expectations

Separate collectors, normalized domain models, correlation rules, and text/JSON renderers. Preserve source timestamps and “unknown” states; do not turn missing permission or a raced process into zero. Model process identity safely across PID reuse. Document collection overhead, consistency limitations, trust boundaries, and the evidence chain from kernel source to conclusion.

## Milestone plan

1. Inventory processes, descriptors, mounts, sockets, and cgroups with fixture-backed parsers.
2. Add CPU, memory, I/O, and pressure-stall snapshots plus before/after comparison.
3. Correlate symptoms into bounded hypotheses, with raw evidence links and confidence limits.
4. Package reproducibly and run controlled pressure scenarios in an isolated VM.

## Required artifacts

- Architecture and data-model document; ADRs for sampling, process identity, and privileges.
- JSON schema with versioning policy; operator guide with worked diagnoses.
- Benchmark report for latency, memory, and perturbation at 100, 1,000, and 10,000 processes.
- Demo recording or transcript showing baseline, fault, diagnosis, and recovery.

## Tests and failure drills

Unit-test parsers using captured malformed and disappearing entries; property-test size/time conversions; integration-test in cgroup v2 namespaces. Drill CPU starvation, memory pressure, descriptor exhaustion, deleted-open files, a stuck filesystem, and a short-lived process storm. Prove partial results remain honest under permission denial and process races.

## Operations, security, and cost

Emit collection duration, skipped sources, parser errors, and snapshot age without phoning home. Threat-model hostile procfs strings, symlink races, terminal escape injection, and accidental sensitive output. Set a target below 1% CPU while sampling a 1,000-process host and publish measured overhead; ongoing infrastructure cost should be zero.

## Success rubric

| Evidence | Pass condition |
|---|---|
| Correctness | Golden snapshots match independent kernel-tool checks and represent unavailable data explicitly. |
| Diagnosis | A reviewer resolves at least four of six blind fault drills from the report alone. |
| Safety | Default execution is unprivileged, read-only, bounded, and secret-redacting. |
| Engineering | Reproducible release, tests, benchmark evidence, ADRs, and limitations are independently reviewable. |

## Stretch work

Add eBPF-assisted evidence behind an explicit privilege boundary, snapshot diff visualization, or FreeBSD interface comparison.

## Authoritative sources

- [proc(5), Linux man-pages](https://man7.org/linux/man-pages/man5/proc.5.html)
- [Control Group v2, Linux kernel documentation](https://docs.kernel.org/admin-guide/cgroup-v2.html)
- [PSI, Linux kernel documentation](https://docs.kernel.org/accounting/psi.html)
- [The Linux Programming Interface project](https://man7.org/tlpi/)

## Mapped modules

[01 Software Foundations](../../01-software-foundations/README.md), [03 Computer Systems](../../03-computer-systems/README.md), [04 Linux](../../04-linux/README.md), [06 Data Structures and Algorithms](../../06-data-structures-algorithms/README.md), and [20 Security](../../20-security/README.md).
