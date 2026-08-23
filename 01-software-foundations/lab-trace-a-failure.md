# Lab: Trace a Failure Across Boundaries

Create one disposable pipeline, predict its states, inject a controlled failure, and produce an evidence bundle that separates input, computation, process, and output.

## Prepare

```bash
lab=$(mktemp -d)
trap 'rm -rf "$lab"' EXIT
printf '4\n0\n2\n' > "$lab/input"
```

Record the temporary path and predict which input will fail.

## Build the pipeline

```bash
cat > "$lab/worker.py" <<'PY2'
import json, os, sys, time
for raw in sys.stdin:
    started = time.monotonic()
    value = int(raw)
    event = {"pid": os.getpid(), "input": value}
    try:
        event.update(outcome="ok", result=12 // value)
    except Exception as error:
        event.update(outcome="failed", error=type(error).__name__)
    finally:
        event["elapsed_ms"] = round((time.monotonic() - started) * 1000, 3)
        print(json.dumps(event), flush=True)
PY2
python3 "$lab/worker.py" < "$lab/input" > "$lab/events"
```

Expected observation: the process exits successfully because it converts the per-record exception into a structured failed outcome. There are three events and exactly one has `outcome` equal to `failed`.

## Inspect, do not guess

```bash
wc -l "$lab/input" "$lab/events"
python3 -m json.tool --json-lines "$lab/events"
```

Write down what each observation proves. The line counts establish cardinality, the records establish application outcomes, and neither proves durable remote delivery.

## Change the contract

In a disposable copy, replace the exception body with `raise`. Run it while capturing stdout, stderr, and status separately. Predict which output records survive and why buffering is not the explanation.

```bash
cp "$lab/worker.py" "$lab/failing.py"
sed -i '/event.update(outcome="failed"/c\        raise' "$lab/failing.py"
set +e
python3 "$lab/failing.py" < "$lab/input" > "$lab/partial" 2> "$lab/error"
status=$?
set -e
printf 'status=%s records=%s\n' "$status" "$(wc -l < "$lab/partial")"
sed -n '1,8p' "$lab/error"
```

Expected observation: the first result was flushed, the second record raises, the process exits nonzero, and the third input is never processed.

## Evidence report

Preserve the command, status, input checksum, complete stderr, structured events, and a five-sentence timeline. Name the earliest boundary known to fail and one plausible claim the evidence cannot establish. Do not describe a caught record error as a process crash.

## Cleanup

```bash
rm -rf "$lab"
trap - EXIT
```

Expected observation: only your written evidence report remains.

## Next

Continue to [Software Lifecycle and Engineering Tradeoffs](./06-software-lifecycle-and-tradeoffs.md).
