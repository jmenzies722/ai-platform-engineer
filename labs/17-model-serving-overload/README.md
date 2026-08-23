# Lab: Diagnose and Control Model-Serving Overload

Exercise a synthetic loopback inference service to observe queueing, tail latency, rejection, concurrency limits, and retry amplification under bounded load.

## Prerequisites

- Python 3.10 or newer and Bash
- No model weights, GPU, packages, or network access
- Ports 58170 and 58171 unused

## Safety

Bind only to `127.0.0.1`. Cap the server at four workers, client at 200 requests, payload at 1 KiB, and each run at 30 seconds. Stop if host load is already elevated. This benchmark models service time; it does not measure real model quality or GPU throughput.

## Setup and baseline

Create `.work/server.py` using `ThreadingHTTPServer`. For `POST /infer`, validate payload size, acquire a `BoundedSemaphore(4)` without waiting, sleep exactly 100 ms to simulate inference, and return JSON. Return 429 with `Retry-After: 1` when no slot is available. Log request ID, queue/admission outcome, start, finish, and status.

```bash
mkdir -p .work
python3 .work/server.py --host 127.0.0.1 --port 58170 --workers 4 \
  >.work/server.log 2>&1 &
SERVER_PID=$!; printf '%s\n' "$SERVER_PID" >.work/pid
curl --max-time 2 -X POST --data '{"input":"baseline"}' \
  http://127.0.0.1:58170/infer
```

Predict maximum steady throughput from worker count and service time, ignoring overhead.

## Tasks

1. Write `.work/load.py` with explicit `--requests`, `--concurrency`, `--timeout`, and `--retries`. Use standard-library HTTP and unique request IDs.
2. Run 40 requests at concurrency 1, then 4, then 20. Record status counts, throughput, and p50, p95, p99 latency using a documented percentile method.
3. Separate offered load, admitted load, completed throughput, and concurrency. Explain why average latency hides overload.
4. Plot or tabulate request start, admission, completion, and rejection over time.
5. Add one retry for 429 using `Retry-After`, a fixed total deadline, and jitter from a seeded generator. Compare total attempts with no-retry runs.
6. Design an overload contract covering queue bound, 429 versus 503, deadlines, cancellation, max payload, batching, fairness, and autoscaling signals.

## Evidence to keep

Keep server/client source, exact commands, environment, baseline, raw result JSON, percentile method, offered/admitted/completed rates, status counts, attempt amplification, and conclusions bounded to this synthetic service.

## Failure injection

Concurrency 20 against four zero-queue workers is the overload fault. Expected evidence is immediate 429 responses rather than unbounded latency. Then modify a copy to wait on the semaphore for up to two seconds; compare tail latency and explain the tradeoff. Never remove both queue and client bounds.

## Cleanup

```bash
SERVER_PID=$(<.work/pid 2>/dev/null || true)
if [[ "$SERVER_PID" =~ ^[0-9]+$ ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
  kill "$SERVER_PID"; wait "$SERVER_PID" || true
fi
rm -rf .work
```

## Rubric

- 2 points: implements bounded admission and deterministic service time
- 3 points: measures offered, admitted, completed, and tail latency correctly
- 2 points: demonstrates overload and bounded retry amplification
- 2 points: proposes a coherent overload and fairness contract
- 1 point: stops loopback processes and avoids production claims

## Sources

- [HTTP 429 status](https://www.rfc-editor.org/rfc/rfc6585#section-4)
- [Google SRE Book: handling overload](https://sre.google/sre-book/handling-overload/)
- [Little's Law](https://doi.org/10.1287/opre.9.3.383)
