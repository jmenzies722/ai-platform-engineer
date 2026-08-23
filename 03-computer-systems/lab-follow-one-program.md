# Lab: Follow One Program Through the System

Inspect one process from executable and memory mappings through descriptors and kernel I/O. The lab is read-only except for one temporary directory.

## Start a bounded workload

```bash
lab=$(mktemp -d)
python3 - "$lab/output" <<'PY2' &
import os, sys, time
path = sys.argv[1]
with open(path, "w", encoding="utf-8") as output:
    print(os.getpid(), flush=True)
    output.write("buffered\n")
    time.sleep(20)
    output.flush()
    os.fsync(output.fileno())
PY2
pid=$!
```

Predict the executable target, at least three mapping categories, and descriptors 0 through 2 before inspection.

## Inspect identity and mappings

```bash
ps -o pid,ppid,stat,vsz,rss,args -p "$pid"
readlink "/proc/$pid/exe"
sed -n '1,15p' "/proc/$pid/maps"
ls -l "/proc/$pid/fd"
```

Record which observations describe identity, virtual mappings, resident estimates, and open kernel references. Do not infer physical addresses from virtual ranges.

## Observe write visibility

Before the sleep completes, inspect the output size. After `wait "$pid"`, inspect it again:

```bash
stat -c '%s bytes' "$lab/output"
wait "$pid"
status=$?
stat -c '%s bytes' "$lab/output"
printf 'status=%s content=' "$status"
cat "$lab/output"
```

Expected observation: user-space buffering may leave the file empty before flush; after completion it contains the record. Normal completion does not simulate power loss.

## Optional focused tracing

If `strace` exists, repeat with a five-second sleep under `strace -e trace=openat,write,fsync,close`. Identify the descriptor returned by `openat`, the write, and synchronization request. State how tracing changes timing and why it cannot prove media durability.

## Report and cleanup

Produce a table with claim, observation, source, and limitation for executable identity, virtual memory, descriptor target, write visibility, and exit status. Then:

```bash
if kill -0 "$pid" 2>/dev/null; then kill -TERM "$pid"; wait "$pid" || true; fi
rm -rf "$lab"
```

## Next

Continue to [Storage, Filesystems, and Durable I/O](./06-storage-filesystems-and-durable-io.md).
