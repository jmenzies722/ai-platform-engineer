# Lab: Inspect a Python Process on Linux

Use a bounded Python workload, `ps`, and Linux `/proc` to connect Python execution to process identity, scheduling, virtual memory, file descriptors, and output. This lab supports [How Software Actually Executes](../../01-software-foundations/01-how-software-actually-executes.md).

The workload runs for at most 10 minutes, allocates at most 256 MiB, handles termination signals, and performs no network or privileged operations. The inspector refuses to examine a process owned by another user.

## Prerequisites

- Linux with `/proc` mounted
- Bash 4 or later
- Python 3.9 or later
- `ps`, `readlink`, `stat`, `sed`, and `tr` (normally supplied by procps and coreutils)
- Two terminal sessions in this lab directory
- Permission to inspect processes owned by your user

Docker Desktop users should run the lab inside the same Linux container in both terminals. macOS does not provide Linux `/proc`; use a Linux VM or container rather than substituting macOS commands.

## Objectives

By the end, you will be able to:

1. distinguish a Python source file, Python executable, and running process;
2. identify PID, parent PID, process state, elapsed time, and CPU time;
3. compare virtual memory size (VSZ/VmSize) with resident memory (RSS/VmRSS);
4. relate memory mappings to executables, libraries, anonymous memory, heap, and stack;
5. identify where standard input, output, and error point;
6. use wait-channel and context-switch evidence carefully;
7. stop and clean up only the process you started.

## Files

- [`process_workload.py`](./process_workload.py) — bounded memory, CPU, sleep, stdout, and stderr behavior
- [`inspect_process.sh`](./inspect_process.sh) — read-only summary of a same-user PID through `ps` and `/proc`

## Setup

From the repository root:

```bash
cd labs/01-software-execution
python3 --version
bash --version | sed -n '1p'
test -r /proc/self/status
python3 -m py_compile process_workload.py
bash -n inspect_process.sh
```

The compile check may create `__pycache__`; cleanup instructions remove it. The scripts accept only bounded arguments:

```bash
python3 process_workload.py --help
./inspect_process.sh 2>&1 || true
```

If the inspector is not executable in a copied checkout, run `chmod u+x inspect_process.sh` or invoke it as `bash inspect_process.sh`.

## Steps

### 1. Predict before running

Write down:

- whether the process will usually be running or sleeping when inspected;
- whether VSZ or RSS will be larger;
- what file descriptors `0`, `1`, and `2` will reference;
- whether the CPU executes `process_workload.py` text or native CPython instructions.

Keep these predictions for the evidence report.

### 2. Start the workload in terminal A

```bash
python3 process_workload.py --seconds 180 --memory-mib 32 \
  >workload.stdout.log 2>workload.stderr.log &
LAB_PID=$!
printf 'LAB_PID=%s\n' "$LAB_PID"
printf '%s\n' "$LAB_PID" > .lab-pid
```

`$!` is the PID of the last background process started by this shell. `.lab-pid` lets terminal B use the exact PID without searching all processes. Do not replace it with a PID from an unrelated process.

Confirm that the process is still yours and running:

```bash
kill -0 "$LAB_PID"
ps -o user,pid,ppid,stat,etime,time,vsz,rss,comm -p "$LAB_PID"
```

`kill -0` sends no signal; it asks the OS to validate process existence and permission.

### 3. Inspect it in terminal B

```bash
cd labs/01-software-execution
LAB_PID=$(<.lab-pid)
./inspect_process.sh "$LAB_PID" | tee inspection.txt
```

If the process has already exited, restart it in terminal A. PIDs can be reused after exit, so always confirm the command and owner in the inspector output.

### 4. Connect the executable to the source

Compare:

```bash
readlink "/proc/$LAB_PID/exe"
tr '\0' ' ' <"/proc/$LAB_PID/cmdline"; printf '\n'
```

The executable path should identify Python, while the command line should include `process_workload.py`. Explain why the kernel-loaded executable and source input are different files.

### 5. Inspect process identity and state

```bash
ps -o pid,ppid,stat,etime,time,%cpu,comm,args -p "$LAB_PID"
sed -n '/^Name:/p;/^State:/p;/^Pid:/p;/^PPid:/p;/^Threads:/p' \
  "/proc/$LAB_PID/status"
```

Run the command twice, several seconds apart. `etime` should grow. CPU `time` may barely grow during the sleep phase. `S` normally means interruptible sleep, while `R` means running or runnable; the inspector itself can affect the exact instant observed.

### 6. Compare virtual and resident memory

```bash
ps -o pid,vsz,rss -p "$LAB_PID"
sed -n '/^VmSize:/p;/^VmRSS:/p;/^RssAnon:/p;/^RssFile:/p' \
  "/proc/$LAB_PID/status"
```

Values are normally in KiB. The 32 MiB allocation should contribute to resident anonymous memory after the script touches its pages, but allocator behavior, shared pages, page size, and accounting mean the numbers will not match the argument exactly. VSZ measures mapped address space, not physical ownership.

Optional controlled comparison:

```bash
python3 process_workload.py --seconds 60 --memory-mib 64 >/dev/null 2>&1 &
SECOND_PID=$!
ps -o pid,vsz,rss,comm -p "$LAB_PID,$SECOND_PID"
wait "$SECOND_PID"
```

This second workload is also bounded. Do not increase memory merely to pressure the host.

### 7. Read memory mappings

```bash
sed -n '1,30p' "/proc/$LAB_PID/maps"
```

Find examples, if present, of:

- the Python executable or runtime;
- a shared library ending in `.so`;
- `[heap]`;
- `[stack]`;
- an anonymous mapping with no pathname.

Columns show virtual address range, permissions, file offset, device, inode, and optional pathname. `r-xp` typically indicates a private readable/executable mapping; it does not mean the whole mapping is resident.

### 8. Trace output destinations

```bash
for fd in 0 1 2; do
  printf 'fd %s -> ' "$fd"
  readlink "/proc/$LAB_PID/fd/$fd"
done
```

Because startup redirected output, descriptors `1` and `2` should point to the two log files. Read current output:

```bash
sed -n '1,20p' workload.stdout.log
sed -n '1,20p' workload.stderr.log
```

The workload explicitly flushes each message, so heartbeats should become visible without waiting for process exit.

### 9. Observe waiting and scheduling evidence

```bash
printf 'wait channel: '
tr -d '\n' <"/proc/$LAB_PID/wchan"
printf '\n'
sed -n '/^voluntary_ctxt_switches:/p;/^nonvoluntary_ctxt_switches:/p' \
  "/proc/$LAB_PID/status"
sleep 6
sed -n '/^voluntary_ctxt_switches:/p;/^nonvoluntary_ctxt_switches:/p' \
  "/proc/$LAB_PID/status"
```

During `time.sleep`, the wait channel often refers to a timer-related kernel path, but names vary by kernel and may be hidden. Voluntary context switches should generally increase as the process sleeps and wakes. These are observations, not proof of every scheduler decision.

### 10. Wait for normal exit

In terminal A:

```bash
wait "$LAB_PID"
LAB_STATUS=$?
printf 'exit_status=%s\n' "$LAB_STATUS"
```

A normal run should return `0`. If it was terminated during the lab, record the action and status rather than presenting it as normal completion.

## Observations to Record

Create `evidence.md` locally with:

| Claim | Command or file | Observation | Interpretation |
|---|---|---|---|
| Python is the loaded executable | `/proc/PID/exe` | your output | distinguish runtime from source |
| The shell is the parent | `PPid` and shell PID | your output | process relationship |
| The process is mostly sleeping | `stat`, CPU time, `wchan` | your output | scheduling state |
| Mapped memory exceeds resident memory | VSZ and RSS | your output | virtual versus physical |
| stdout and stderr are files | `/proc/PID/fd/1`, `/fd/2` | your output | output routing |
| Memory contains distinct regions | `/proc/PID/maps` | your output | code/data mapping |

Replace `PID` with the actual numeric PID in captured commands. Also record one prediction that was wrong or too simplistic and explain the correction.

## Build Task

Copy the workload to `my_workload.py` and add one safe, bounded feature:

- open a local file and hold it open during the sleep phase;
- create one additional thread that sleeps;
- allocate memory in four timed increments, never exceeding 128 MiB; or
- print the system page size from `os.sysconf`.

Before running it, predict which `ps` or `/proc` field will change. Then demonstrate the change with before-and-after evidence. Do not add network calls, privilege changes, unbounded allocation, unbounded process creation, or infinite loops.

## Break Task

Choose one controlled failure:

1. Run `./inspect_process.sh abc` and explain its validation error.
2. Inspect the workload after it exits and explain why `/proc/<pid>` disappeared.
3. Remove `flush=True` in a temporary copy, redirect stdout, and compare visibility before exit.
4. Request `--memory-mib 999` and explain how argument validation prevents unsafe allocation.

Do not edit the supplied scripts for this task; use a copy when code changes are required.

## Debug Task

Scenario: `.lab-pid` exists, but the inspector says the process is not running.

Use this sequence:

```bash
LAB_PID=$(<.lab-pid)
printf 'recorded pid=%s\n' "$LAB_PID"
ps -o user,pid,ppid,stat,etime,comm,args -p "$LAB_PID"
sed -n '1,20p' workload.stderr.log
```

Decide among these hypotheses:

- the bounded workload completed;
- argument validation prevented startup;
- the process received a signal;
- the PID was mistyped or the file is stale.

Restart the workload only after identifying what the evidence supports. Never scan for and terminate processes by name; track the PID started by your shell.

## Cleanup

In terminal A, stop only the tracked workload if it is still running:

```bash
if [[ -n "${LAB_PID:-}" ]] && kill -0 "$LAB_PID" 2>/dev/null; then
  kill "$LAB_PID"
  wait "$LAB_PID" || true
fi
```

In terminal B, stop the optional second workload only if you started it and it remains active:

```bash
if [[ -n "${SECOND_PID:-}" ]] && kill -0 "$SECOND_PID" 2>/dev/null; then
  kill "$SECOND_PID"
  wait "$SECOND_PID" || true
fi
```

Remove generated artifacts, not the supplied scripts:

```bash
rm -rf __pycache__
rm -f .lab-pid inspection.txt evidence.md my_workload.py
rm -f workload.stdout.log workload.stderr.log
```

## Evidence

Retain these items until your work is reviewed:

- initial predictions;
- `inspection.txt`;
- the completed observation table;
- stdout and stderr samples;
- before-and-after evidence from the build task;
- break-task command, error, and explanation;
- normal or explained nonzero exit status;
- a diagram connecting source, CPython, process, memory, scheduler/CPU, syscall, fd, and output.

Do not include secrets, complete environment dumps, or evidence from processes you did not start.

## Completion Criteria

The lab is complete when you can demonstrate all of the following:

- [ ] The supplied syntax checks pass.
- [ ] The workload starts, reports its PID, and exits normally or has a documented termination.
- [ ] The recorded PID, command line, executable, parent, and owner agree.
- [ ] Your evidence distinguishes VSZ/VmSize from RSS/VmRSS.
- [ ] You identify at least four kinds of memory mapping without claiming all are resident.
- [ ] You identify fd `1` and fd `2` destinations and explain explicit flushing.
- [ ] You interpret process state and wait-channel evidence with appropriate uncertainty.
- [ ] The build task changes one predicted observable safely.
- [ ] The break task produces and explains one controlled failure.
- [ ] Cleanup leaves no workload process running.
- [ ] You can explain why the CPU executes native CPython instructions rather than Python source or bytecode directly.
