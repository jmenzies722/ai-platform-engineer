# Lab: Diagnose a Slow Linux Workload

Use process, file-descriptor, CPU, memory, and I/O evidence to separate a busy process from a waiting one. All activity is limited to processes started by your shell.

## Prerequisites

- Linux with `/proc`, Bash, Python 3, `ps`, `top`, `vmstat`, `lsof`, and `timeout`
- Two terminals in `labs/02-linux-diagnosis`
- No root privileges

## Safety

The workload lasts at most 120 seconds, writes at most 32 MiB, and allocates at most 64 MiB. Record `$!` and inspect only that PID. Stop if the host is already memory constrained or if the PID no longer belongs to your command.

## Setup and baseline

```bash
mkdir -p .work
dd if=/dev/zero of=.work/input.bin bs=1M count=8 status=none
python3 -c 'import os; print(os.getpid()); print("baseline")'
vmstat 1 2 | tee .work/vmstat-baseline.txt
```

Write down whether a sleeping, CPU-bound, or I/O-bound process should accumulate CPU time fastest.

## Tasks

1. Start a bounded mixed workload:

   ```bash
   python3 -c '
   import hashlib, pathlib, time
   p=pathlib.Path(".work/input.bin")
   for i in range(240):
       hashlib.sha256(p.read_bytes()).digest()
       time.sleep(.25)
   ' >.work/stdout.log 2>.work/stderr.log &
   LAB_PID=$!; printf '%s\n' "$LAB_PID" >.work/pid
   ```

2. In the second terminal, prove identity and inspect state:

   ```bash
   LAB_PID=$(<.work/pid)
   ps -o pid,ppid,stat,etime,time,%cpu,%mem,args -p "$LAB_PID"
   sed -n '/^State:/p;/^VmRSS:/p;/^Threads:/p;/^voluntary_ctxt_switches:/p' "/proc/$LAB_PID/status"
   lsof -p "$LAB_PID" | tee .work/lsof.txt
   ```

3. Sample twice, five seconds apart. Explain elapsed time, CPU time, state, context switches, open files, and why one sample cannot establish a trend.
4. Use `vmstat 1 5` and `top -b -n 2 -p "$LAB_PID"` to distinguish host pressure from process behavior.

## Evidence to keep

Create `.work/evidence.md` containing the prediction, both process samples, descriptor evidence, host baseline, one rejected hypothesis, and a concise diagnosis. For every claim, name the field that supports it and a plausible fact it does not prove.

## Failure injection

Pause only the recorded process:

```bash
LAB_PID=$(<.work/pid)
kill -STOP "$LAB_PID"
ps -o pid,stat,time,args -p "$LAB_PID" | tee .work/stopped.txt
kill -CONT "$LAB_PID"
```

Expected symptom: `STAT` contains `T`, output stops changing, and CPU time does not materially increase. Diagnose from process state before correcting it. Never use `pkill`.

## Cleanup

```bash
LAB_PID=$(<.work/pid 2>/dev/null || true)
if [[ "$LAB_PID" =~ ^[0-9]+$ ]] && kill -0 "$LAB_PID" 2>/dev/null; then
  kill -TERM "$LAB_PID"; wait "$LAB_PID" || true
fi
rm -rf .work
```

## Rubric

- 2 points: captures a baseline and predicts state behavior
- 3 points: ties CPU, wait state, descriptors, and host metrics to evidence
- 2 points: identifies and safely recovers the stopped process
- 2 points: rejects at least one unsupported explanation
- 1 point: cleanup leaves no workload or generated files

## Sources

- [Linux proc filesystem](https://docs.kernel.org/filesystems/proc.html)
- [`proc_pid_status(5)`](https://man7.org/linux/man-pages/man5/proc_pid_status.5.html)
- [`ps(1)`](https://man7.org/linux/man-pages/man1/ps.1.html)
