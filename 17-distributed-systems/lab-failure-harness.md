# Lab: expose duplicate work and overload

Build a local queue simulator that makes ambiguous completion, duplicate delivery, and finite capacity visible.

## Goal

Produce an idempotent worker with a bounded queue, then prove that response loss does not duplicate a side effect and overload does not consume unbounded memory.

## Before you start

Read lessons 6 and 7. Use Python 3 and a temporary directory; no network, credentials, privileges, or cost are required. Stop if you adapt the lab to any shared queue. Before running, predict side-effect count and rejected submissions.

## Establish a baseline

`python3 --version` must print Python 3. Create an isolated directory and prove the queue rejects excess work:

```bash
mkdir -p /tmp/ds-failure-lab
python3 - <<'PY'
from queue import Full, Queue
q = Queue(maxsize=1)
q.put_nowait("first")
try:
    q.put_nowait("second")
    raise AssertionError("queue exceeded its bound")
except Full:
    print("bounded queue rejects excess work")
PY
```

The printed line establishes the runtime and bounded primitive; it says nothing yet about duplicate-safe processing.

## Make it work

Save this deterministic worker as `/tmp/ds-failure-lab/worker.py`:

```python
from collections import Counter
from queue import Full, Queue
from threading import Lock, Thread
from time import sleep

queue = Queue(maxsize=10)
lock = Lock()
results, effects, rejected = {}, [], []

def worker():
    while True:
        operation = queue.get()
        if operation is None:
            queue.task_done()
            return
        sleep(0.01)
        with lock:
            if operation not in results:
                effects.append(operation)
                results[operation] = f"result-{operation}"
        queue.task_done()

thread = Thread(target=worker)
thread.start()
for operation in [f"op-{n}" for n in range(30)] + ["op-1", "op-2"]:
    try:
        queue.put_nowait(operation)
    except Full:
        rejected.append(operation)
queue.join()
queue.put(None)
thread.join()
counts = Counter(effects)
assert max(counts.values(), default=0) <= 1
assert queue.maxsize == 10 and rejected
print({"effects": len(effects), "rejected": len(rejected), "duplicates": []})
```

Run it twice:

```bash
python3 /tmp/ds-failure-lab/worker.py | tee /tmp/ds-failure-lab/baseline.txt
python3 /tmp/ds-failure-lab/worker.py
```

Both runs must satisfy the assertions. Queue admission can vary with scheduling, so reason from the invariants rather than expecting one rejection count.

## Break it

After recording the baseline, change `if operation not in results:` to `if True:` but change nothing else. Slow the producer by adding `sleep(0.002)` after each successful `put_nowait` if duplicate IDs were rejected before admission. The expected symptom is an assertion failure or repeated IDs in `Counter(effects)`. This is one fault: loss of the atomic idempotency decision.

## Diagnose it

Start with the user-visible invariant: one effect per admitted ID. Temporarily print `Counter(effects)` and compare it with `results`; this separates duplicate execution from duplicate submission and queue rejection. Restore the atomic check, rerun the same input, and prove every admitted ID has at most one effect while overload remains explicit as rejection. In production, the lock and dictionary must become one durable conditional insert or transaction.

## Clean up

```bash
rm -rf /tmp/ds-failure-lab
test ! -e /tmp/ds-failure-lab
```

## What to keep

Keep the prediction, counts, duplicated IDs, correction, and a production policy for key retention, retry ownership, admission, and queue-age alerting. Explain why the queue absorbs a burst but cannot repair a sustained rate mismatch.

## Sources

- [Python queue documentation](https://docs.python.org/3/library/queue.html)
