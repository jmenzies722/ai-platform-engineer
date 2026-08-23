# Lab: Inspect One Python Process

This lab makes execution visible without requiring privileged tools. You will start one bounded process, inspect only its PID, observe memory and output routes, and stop or wait for that exact process.

## Goal

Prove the difference among Python source, the Python executable, and a running process. Then explain why an alive process may use little CPU, why virtual size differs from resident memory, and where standard output goes.

## Requirements and safety

Use Linux with `/proc`, Bash, Python 3, and `ps`. Work from `labs/01-software-execution`. The supplied workload caps duration at ten minutes and allocation at 256 MiB. Never substitute a PID found by name, never signal a process you did not start, and do not raise those limits.

## 1. Check the files

```bash
cd labs/01-software-execution
python3 -m py_compile process_workload.py
bash -n inspect_process.sh
test -r /proc/self/status && echo ready
```

Expected observation: `ready` appears and the validation commands are silent. Python may create `__pycache__`, which cleanup removes.

Before continuing, predict which path `/proc/PID/exe` will show, whether the process will usually be running or sleeping, and whether VSZ or RSS will be larger.

## 2. Start the bounded workload

```bash
python3 process_workload.py --seconds 90 --memory-mib 32 \
  >workload.stdout.log 2>workload.stderr.log &
LAB_PID=$!
printf '%s\n' "$LAB_PID" > .lab-pid
printf 'started pid=%s\n' "$LAB_PID"
```

Expected observation: the shell prints one numeric PID and returns immediately. `$!` is the exact background child created by this shell.

## 3. Inspect that identity

In a second terminal, from the same directory:

```bash
LAB_PID=$(<.lab-pid)
bash inspect_process.sh "$LAB_PID" | tee inspection.txt
readlink "/proc/$LAB_PID/exe"
tr '\0' ' ' < "/proc/$LAB_PID/cmdline"; printf '\n'
```

Expected observations:

- `exe` resolves to a Python binary, while `cmdline` includes `process_workload.py`;
- the PID and parent PID agree across the report;
- fd 1 and fd 2 point to the two log files;
- `VmSize` normally exceeds `VmRSS`.

This proves what Linux loaded and what it currently reports. It does not prove that every byte of mapped memory is resident or that the process is making useful progress.

## 4. Observe waiting and CPU time

```bash
ps -o pid,ppid,stat,etime,time,%cpu,args -p "$LAB_PID"
sleep 5
ps -o pid,ppid,stat,etime,time,%cpu,args -p "$LAB_PID"
```

Expected observation: elapsed time grows while accumulated CPU time changes little during the workload’s sleep. `S` means interruptible sleep; `R` means running or runnable. A state is a sample, not a complete history.

## 5. Follow memory and output

```bash
sed -n '/^VmSize:/p;/^VmRSS:/p;/^RssAnon:/p;/^RssFile:/p' "/proc/$LAB_PID/status"
for fd in 0 1 2; do printf 'fd %s -> ' "$fd"; readlink "/proc/$LAB_PID/fd/$fd"; done
sed -n '1,8p' workload.stdout.log
sed -n '1,8p' workload.stderr.log
```

Expected observation: virtual and resident measurements differ, and stdout and stderr follow separate descriptors. The allocation will not equal one field exactly because Python, shared libraries, mappings, and accounting also contribute.

## 6. Explain the evidence

Create `evidence.md` with five rows: loaded executable, source argument, waiting state, memory measurements, and output destinations. For each row record the command, observation, supported claim, and one claim it does not prove. Include one prediction you revised.

## 7. Controlled failure

After the workload exits, run the inspector with the recorded PID. It should refuse because `/proc/PID` is gone. PIDs can later be reused, which is why a stored number alone is not durable identity.

You may also run `bash inspect_process.sh abc`; expected observation is a validation error without inspecting any process.

## Cleanup

In the terminal that started the workload:

```bash
if [[ -n "${LAB_PID:-}" ]] && kill -0 "$LAB_PID" 2>/dev/null; then
  kill -TERM "$LAB_PID"
  wait "$LAB_PID" || true
fi
rm -rf __pycache__
rm -f .lab-pid inspection.txt evidence.md workload.stdout.log workload.stderr.log
```

Expected observation: `kill -0 "$LAB_PID"` no longer succeeds and `git status --short` shows no generated lab artifacts.

## Completion check

You are done when you can explain why the `.py` file is not the loaded executable, why elapsed and CPU time differ, why VSZ is not “RAM owned,” and how fd 1 reaches a file.

## Next

Continue to [Concurrency and Waiting](../../01-software-foundations/03-concurrency-and-waiting.md).
