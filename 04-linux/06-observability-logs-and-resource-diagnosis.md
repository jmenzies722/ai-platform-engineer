# Observability, Logs, and Resource Diagnosis

Linux exposes snapshots and counters for processes, memory, storage, networking, and kernel events. Diagnosis is the work of connecting a symptom to the smallest responsible boundary without erasing evidence.

## Why it matters

High load average is not identical to high CPU use, free memory near zero is not automatically exhaustion, and a large log file is not automatically the cause of slow requests. Dashboard labels compress several mechanisms. An operator must identify scope, time window, workload, and resource before changing limits or restarting a service.

## How it works

Observations have kinds. Gauges describe current levels, counters accumulate events, samples capture states, and logs record selected events. CPU time measures execution, while elapsed time also includes waiting. Linux load average counts runnable tasks and tasks in uninterruptible wait, so storage stalls can raise load with idle CPU. Memory reports distinguish available capacity, cache, anonymous use, and swap; `/proc/PID` gives process-specific views. Storage capacity, inode capacity, throughput, latency, and queueing are separate dimensions.

Service managers collect lifecycle state and often journal output. Kernel messages report device, memory, and security events but require careful timestamp correlation. Logs are incomplete by design and may rotate, rate-limit, or contain secrets. A minimal incident snapshot records time, host or namespace identity, workload symptom, deployment version, process identity and state, resource saturation, recent relevant events, and exact commands. Baselines and repeated samples reveal change; one sample cannot establish a trend.

## See it yourself

**Tiny Proof:** predict that a sleeping process gains elapsed time while CPU time remains nearly unchanged. Two samples establish change between those moments, not long-term health.

```bash
sleep 5 &
pid=$!
ps -o pid,stat,etime,time,rss,comm -p "$pid"
sleep 1
ps -o pid,stat,etime,time,rss,comm -p "$pid"
wait "$pid"
```

Expected observation: elapsed time advances, state is usually sleeping, and accumulated CPU time stays close to zero.

Limits of this proof: scheduler timing varies, RSS accounting is approximate, and `ps` is a sample. It does not locate why an arbitrary production process waits.

## Where it shows up

During a slow-request incident, start with user-visible latency and error rate, then identify the serving version and process set. CPU saturation with runnable queues calls for profiles; low CPU with many blocked threads calls for wait points and dependencies; rising I/O latency with uninterruptible tasks points toward storage. Correlating service logs, supervisor events, and kernel messages around the first symptom can separate cause from restart aftermath.

## When it breaks

Missing logs may mean wrong unit, namespace, time range, rotation, permissions, or failure before initialization. Contradictory memory totals often reflect different scopes or accounting. A process that disappears while inspected may have exited or been restarted. First timestamp every command, verify scope and identity, save raw output, and note collection failures. Avoid `dmesg`, environment dumps, or command tracing in shared reports without filtering secrets and access tokens.

## Practice

**Build:** create a bounded process that alternates CPU work and sleep, then collect two-second samples of state, CPU time, elapsed time, RSS, and system load. **Break:** terminate it gracefully and identify which observations become unavailable after exit. **Explain back:** distinguish symptom, resource demand, saturation, error, event, and causal claim. Success is a concise incident bundle with timestamps, limitations, no secrets, no unrelated PIDs, and a cleanup check.

## Check yourself

1. Why can load average rise while CPUs are not saturated?
2. What turns a collection of command outputs into useful diagnostic evidence?

## Sources

### REQUIRED

- [proc(5)](https://man7.org/linux/man-pages/man5/proc.5.html)

### RECOMMENDED

- [systemd journal](https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html)

### DEEP DIVE

- [Linux Performance Analysis in 60,000 Milliseconds](https://www.brendangregg.com/blog/2015-12-03/linux-performance.html)

## Next

Continue to [Git and Version Control](../05-git/README.md).
