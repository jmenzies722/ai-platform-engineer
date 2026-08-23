# Linux operator sheet

Use this sheet to locate the first constrained or failed layer before changing
processes, packages, files, or services. Commands assume systemd and procfs where
noted.

## Frame the question

Ask: Is the symptom host-wide or process-specific? Did demand grow, capacity
shrink, or a dependency fail? Confirm host, boot, clock, workload, and incident
window first.

```bash
# Read-only
hostnamectl
uptime
date --iso-8601=seconds
who -b
```

`uptime` shows load averages for roughly 1, 5, and 15 minutes. Load includes
runnable tasks and tasks waiting in uninterruptible sleep; it is not CPU percent.
A recent boot changes the investigation window. A wrong clock makes log
correlation unreliable.

## Is CPU or scheduling the constraint?

```bash
# Read-only; bounded samples
vmstat 1 5
ps -eo pid,ppid,user,stat,%cpu,%mem,etimes,comm --sort=-%cpu | sed -n '1,16p'
```

In `vmstat`, sustained `r` above available CPUs suggests runnable contention;
high `us` means user work, high `sy` kernel work, and high `wa` reported idle
time while I/O is outstanding. A single sample is weak evidence. In `ps`, `R`
is runnable, `D` is usually uninterruptible I/O wait, and `Z` is a zombie whose
parent has not reaped it.

**Caution:** High load with low CPU can be blocked I/O, not CPU scarcity. Do not
kill a process only because it tops one sample.

## Is memory pressure causing latency or termination?

```bash
# Read-only
free -h
vmstat 1 5
journalctl -k --since "-30 min" --grep='oom|Out of memory|Killed process'
```

Judge `available`, not `free`: Linux uses idle memory for cache. Sustained
nonzero `si` and `so` indicate swap traffic. Kernel OOM messages identify
victims but not necessarily the workload that caused pressure.

**Escalate:** Repeated OOM kills, kernel allocation failures, or pressure across
multiple tenants requires the host or platform owner. Preserve cgroup limits,
workload demand, and the OOM log before restarting.

## Is storage full, exhausted, or slow?

```bash
# Read-only
df -hT
df -i
findmnt
du -x -h --max-depth=1 /var 2>/dev/null | sort -h
```

`df` reports filesystem allocation; `du` reports reachable file sizes. A gap can
mean deleted but still-open files, snapshots, reserved blocks, or mount
confusion. `df -i` at 100 percent means inode exhaustion even if bytes remain.
`-x` keeps `du` on one filesystem.

```bash
# Read-only; requires access to process descriptors
lsof +L1
```

Entries with link count zero are deleted files still held open. Restarting the
owning process may release space, but only through its service runbook.

**Caution:** Never recursively delete logs or caches during diagnosis. Confirm
retention, ownership, mount boundaries, and recovery requirements.

## Did a service fail, or did its dependency fail?

```bash
# Read-only
systemctl status <unit> --no-pager
systemctl show <unit> -p ActiveState -p SubState -p Result -p ExecMainStatus
journalctl -u <unit> --since "-30 min" --no-pager
systemctl list-dependencies <unit>
```

`ActiveState=failed` and `Result` describe systemd's view; `ExecMainStatus`
contains the process exit status. `active` proves process supervision state, not
application health. Read logs for the first error and dependency evidence.

```bash
# Remote mutation and privilege; only after rollback is defined
sudo systemctl restart <unit>
```

Before restart, capture status and logs, verify restart safety and redundancy,
and define a health check. Roll back a configuration or package change rather
than repeatedly restarting. Stop after one unsuccessful restart.

## Is the process listening and using expected files?

```bash
# Read-only
ss -lntup
ls -l /proc/<pid>/fd
tr '\0' ' ' < /proc/<pid>/cmdline
```

A listening socket proves a local bind, not reachability or readiness. `0.0.0.0`
and `::` are wildcard binds; loopback binds are local-only. `/proc` access may
be restricted and command lines can expose secrets, so redact output.

## Controlled change and rollback

For a config change: validate with the program's check mode, preserve the prior
file and metadata, apply through configuration management, reload only if the
program documents reload semantics, and verify both health and logs. A reload
is not universally safer than a restart.

Escalate immediately for filesystem corruption, repeated kernel faults,
suspected compromise, data loss, unknown host ownership, or any action requiring
an untested reboot.

## Authoritative sources

- [Linux kernel documentation](https://docs.kernel.org/)
- [proc filesystem](https://docs.kernel.org/filesystems/proc.html)
- [systemd manual](https://www.freedesktop.org/software/systemd/man/latest/)
- [procps-ng manuals](https://gitlab.com/procps-ng/procps/-/tree/master/man)
- [iproute2 manuals](https://www.kernel.org/doc/man-pages/)
- Repository lessons: [Linux](../04-linux/README.md) and
  [computer systems](../03-computer-systems/README.md)
