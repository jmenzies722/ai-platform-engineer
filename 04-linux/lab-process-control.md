# Lab: Inspect and Control One Linux Process

Use a process you create yourself to practice identity, state, signals, exit status, and cleanup. Everything is local and bounded.

## Prepare

```bash
lab=$(mktemp -d)
printf 'lab=%s\n' "$lab"
```

Keep this shell open. Do not replace the tracked PID with output from `pgrep` or `ps`.

## Start and inspect

```bash
sleep 120 &
pid=$!
printf '%s\n' "$pid" > "$lab/pid"
ps -o user,pid,ppid,stat,etime,time,comm,args -p "$pid"
readlink "/proc/$pid/exe"
```

Expected observation: `sleep` has the PID in `$!`, is usually in state `S`, and has almost no CPU time. The `/proc` link identifies the loaded executable.

Sample twice:

```bash
ps -o pid,stat,etime,time -p "$pid"
sleep 2
ps -o pid,stat,etime,time -p "$pid"
```

Elapsed time grows; CPU time should barely move. Existence is not the same as active CPU execution.

## Request graceful termination

```bash
kill -TERM "$pid"
wait "$pid"
status=$?
printf 'status=%s\n' "$status"
```

Expected observation: the process ends, `wait` returns a nonzero signal-related status, and `/proc/$pid` disappears. `SIGTERM` is a request a program may handle; this `sleep` exits.

## Controlled failure

Run `kill -TERM "$pid"` again. Expected observation: the shell reports that no such process exists. This is safer than experimenting on an unrelated process. Do not use `kill -9`; it adds no useful lesson here and denies applications a cleanup path.

## Explain what happened

Write four sentences: how you obtained identity, what `S` established, what the two time samples established, and why the second signal failed. State why none of these observations proves how another service handles `SIGTERM`.

## Cleanup

```bash
if kill -0 "$pid" 2>/dev/null; then kill -TERM "$pid"; wait "$pid" || true; fi
rm -rf "$lab"
```

Expected observation: no tracked process or temporary directory remains.

## Next

Continue to [Shell Composition and Safe Automation](./03-shell-composition-and-safe-automation.md).
