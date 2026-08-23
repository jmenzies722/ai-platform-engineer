# Lab: Add Timeouts, Retries, and Idempotency to a Backend Call

Use a deterministic local HTTP service to show why deadlines, bounded retries, backoff, and idempotency must be designed together.

## Prerequisites

- Python 3.10 or newer and Bash
- No third-party packages or network access
- Ports 58080 and 58081 unused

## Safety

Both servers bind only to loopback and are stopped by cleanup. Each client run has a five-second total budget and at most three attempts. Never remove retry bounds or test retry logic against a chargeable endpoint.

## Setup and baseline

```bash
mkdir -p .work
cat >.work/server.py <<'PY'
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json, sys, time
counts = {}
class H(BaseHTTPRequestHandler):
    def do_POST(self):
        key = self.headers.get("Idempotency-Key", "")
        counts[key] = counts.get(key, 0) + 1
        if self.path == "/slow": time.sleep(2)
        if self.path == "/flaky" and counts[key] < 3:
            self.send_response(503); self.end_headers(); return
        body = json.dumps({"key": key, "attempt": counts[key]}).encode()
        self.send_response(201); self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def log_message(self, fmt, *args): print(fmt % args, flush=True)
ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
PY
python3 .work/server.py 58080 >.work/server.log 2>&1 &
SERVER_PID=$!; printf '%s\n' "$SERVER_PID" >.work/pid
curl --max-time 1 -X POST -H 'Idempotency-Key: baseline' http://127.0.0.1:58080/ok
```

Predict which HTTP methods and failures are safe to retry, and state assumptions about whether the server processed a timed-out request.

## Tasks

1. Call `/slow` with `curl --max-time 1`; prove a client timeout does not establish that the server did no work.
2. Write `.work/client.py` using `urllib.request`. Give it a five-second monotonic deadline, maximum three attempts, per-attempt timeout no greater than remaining budget, fixed idempotency key, and backoff of 0.1 then 0.2 seconds.
3. Retry only timeout-like transport errors and HTTP 503. Do not retry arbitrary 4xx responses.
4. Call `/flaky`; record each attempt, elapsed time, status, and final result.
5. Explain where production idempotency state must be durably stored. The lab server merely counts; it does not implement a production idempotency contract.

## Evidence to keep

Keep client source, server log, attempt timeline, total duration, idempotency key, final response, and a retry decision table. Include one ambiguous-outcome scenario and one retry-storm risk.

## Failure injection

Use `/slow` to exceed the per-attempt deadline and `/flaky` to return exactly two 503 responses. Run one fault at a time. Then stop the server and show that connection refusal is distinguishable from an HTTP status.

## Cleanup

```bash
SERVER_PID=$(<.work/pid 2>/dev/null || true)
if [[ "$SERVER_PID" =~ ^[0-9]+$ ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
  kill "$SERVER_PID"; wait "$SERVER_PID" || true
fi
rm -rf .work
```

## Rubric

- 2 points: defines a total deadline and explicit retry budget
- 3 points: retries only classified transient failures within budget
- 2 points: reuses one idempotency key and explains server obligations
- 2 points: separates timeout, refusal, and HTTP failure evidence
- 1 point: stops the loopback server and removes artifacts

## Sources

- [HTTP semantics, idempotent methods](https://www.rfc-editor.org/rfc/rfc9110#section-9.2.2)
- [Python `urllib.request`](https://docs.python.org/3/library/urllib.request.html)
- [AWS Builders' Library: timeouts, retries, and backoff](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
