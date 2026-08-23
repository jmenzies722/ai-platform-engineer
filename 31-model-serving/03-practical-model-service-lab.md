# Practical lab: build a tiny model service

This lab uses only Python's standard library. The “model” is a deterministic sentiment score with simulated compute, so you can study serving behavior without downloading weights.

## Why it matters

Queue limits, concurrency, latency, health, and versioning are observable even when model math is trivial. Those controls transfer to real inference servers.

## How it works

Create `/tmp/tiny_serve.py`:

```python
import json, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

slots = threading.BoundedSemaphore(2)
POSITIVE = {"good", "great", "fast", "clear", "love"}

class Handler(BaseHTTPRequestHandler):
    def reply(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self.reply(200, {"status": "ready", "model_version": "toy-v1"})

    def do_POST(self):
        if self.path != "/predict":
            return self.reply(404, {"error": "not found"})
        if not slots.acquire(blocking=False):
            return self.reply(503, {"error": "overloaded"})
        started = time.perf_counter()
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length))
            text = body["text"]
            if not isinstance(text, str) or len(text) > 1000:
                return self.reply(400, {"error": "text must be a string <= 1000 chars"})
            time.sleep(0.1)
            words = text.lower().split()
            score = sum(word.strip(".,!?") in POSITIVE for word in words)
            self.reply(200, {"label": "positive" if score else "neutral",
                             "score": score, "model_version": "toy-v1",
                             "latency_ms": round((time.perf_counter()-started)*1000, 1)})
        except (json.JSONDecodeError, KeyError):
            self.reply(400, {"error": "expected JSON with text"})
        finally:
            slots.release()

ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
```

`ThreadingHTTPServer` gives each connection a thread, while the semaphore limits the expensive section to two concurrent requests. Nonblocking acquisition is deliberate: once both slots are occupied, the service returns a bounded 503 instead of creating an invisible queue. The 100 ms sleep stands in for inference. The model version travels with every successful prediction so a result can be tied to an implementation.

This is admission control, not rate limiting. A client may send many requests per second, but only two execute concurrently. It is also not batching: each admitted request pays its own simulated compute. Those distinctions matter when interpreting the measurements.

Run `python /tmp/tiny_serve.py`. In another shell:

```bash
curl -s http://127.0.0.1:8000/
curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"text":"great clear service"}' http://127.0.0.1:8000/predict
seq 1 10 | xargs -P10 -I{} curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"text":"good"}' http://127.0.0.1:8000/predict
```

## See it yourself

Count 200 and 503 responses during the ten-request burst. With capacity two and near-simultaneous arrival, expect roughly two successes and eight fast overload responses; exact scheduling can vary. Time the burst. Change capacity to one and four and record status counts and latency.

Then replace `acquire(blocking=False)` with blocking acquisition. Most requests now return 200, but later requests wait in thread stacks and total completion arrives in waves of about 100 ms. This proves rejection and queueing expose overload differently. Add a 50 ms acquisition timeout to create a bounded queue and compare all three policies.

## Where it shows up

In a production inference service, the handler would deserialize tensors, reserve model and cache capacity, execute on an accelerator, and validate output. The semaphore corresponds to a coarse concurrency budget; real admission may reserve tokens or bytes. A router should send traffic only after the model is loaded and a readiness probe succeeds. The returned digest or version lets incident responders connect a bad prediction to rollout history.

## When it breaks

The service has no authentication, TLS, durable metrics, graceful shutdown, or multi-process coordination. Its health endpoint does not test dependency health. It is a lab, not a production server.

If requests hang, first compare client timestamps with server access logs and inspect whether blocking admission was enabled. If every request returns 503, verify semaphore release in `finally` and check for a handler still occupying a slot. If the process is healthy but predictions fail, replay one bounded JSON request and inspect status and body before adding concurrency. Never expose this lab beyond loopback.

## Practice

**Build:** add generated or accepted request IDs, monotonic latency timing, and thread-safe counters for success, invalid input, and overload. Add a `/metrics` JSON endpoint. Completion means counters reconcile exactly with a 20-request test.

**Break:** remove `finally`, trigger invalid JSON after acquiring a slot, and observe capacity leak; then restore it. Enable blocking admission and use a short client timeout to expose abandoned work. Keep the service bound to `127.0.0.1`.

**Explain back:** write a p95 latency and availability SLO, then present the status counts and timing that would falsify it. Distinguish concurrency limiting, queueing, batching, and rate limiting using this service's observed behavior.

Next, complete standalone [Lab 17: Control Model-Serving Overload](../labs/17-model-serving-overload/README.md). Preserve its bounded-load evidence for the [inference-latency drill](../incidents/10-inference-latency/README.md) and the [Multi-Tenant Model Serving System](../projects/12-model-serving-system/README.md).

## Check yourself

1. Why return 503 instead of accepting unlimited work?
2. Which latency does the current response omit?
3. How would retries change the burst?

## Sources

### REQUIRED

- [Python `http.server`](https://docs.python.org/3/library/http.server.html)

### RECOMMENDED

- [NVIDIA Triton model management](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_management.html)

### DEEP DIVE

- [Google SRE: addressing cascading failures](https://sre.google/sre-book/addressing-cascading-failures/)

## Next

Continue to [AI Platform Engineering](../32-ai-platform-engineering/README.md).
