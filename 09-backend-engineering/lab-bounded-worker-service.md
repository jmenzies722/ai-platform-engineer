# Lab: Build and Overload a Bounded Worker Service

Build a small HTTP service that accepts logical jobs without pretending acceptance means completion.

## Contract

Use a language standard library. `POST /jobs` accepts JSON containing an idempotency key and work duration. It returns a stable job identifier, or a documented invalid-input, duplicate, or overloaded response. `GET /jobs/{id}` returns one of `queued`, `running`, `succeeded`, or `failed`. Do not treat an in-memory job map as durable in your write-up.

Set these explicit bounds:

- request body size;
- at most two workers;
- queue capacity four;
- work duration and request deadline;
- graceful shutdown interval.

Predict all responses before implementation. Keep credentials and personal data out of payloads and logs.

## Build

Separate transport parsing, domain validation, an explicit authorization policy seam, job repository, queue admission, and worker execution. Store the first result by idempotency key so a repeated request returns the same job rather than enqueueing another. Emit structured records with request ID, job ID, state transition, queue wait, service time, and safe error code.

Start on loopback using a nonprivileged port. Submit one valid job, repeat its key, submit malformed JSON, and poll the successful job. Prove that duplicate submission produces one logical execution.

## Break it deliberately

Submit enough slow jobs to fill both workers and the queue. The next request must reject promptly rather than wait in an unbounded handler. Record queue age and response latency. Then:

1. cancel a polling client and determine whether server work is intentionally independent;
2. inject a handler failure and preserve a stable public error;
3. begin graceful shutdown with queued and running jobs;
4. restart and state which information is lost in this in-memory design.

If you add retries, classify errors, cap attempts, add jitter, and prove idempotency before enabling them.

## Measure

Run at least three bounded load levels. Record offered rate, accepted rate, completed rate, overload responses, median and tail latency, in-flight work, queue depth, and oldest age. Use Little’s Law to estimate average concurrency from completed throughput and time in system, then explain any difference from your sample.

Profile one interval with the language’s supported profiler. Make one change only if the profile identifies a bottleneck; repeat the same workload and report uncertainty. Sleeping jobs are useful for queue behavior but not CPU optimization.

## Deliverable

Submit the API contract, state machine, concurrency diagram or prose timeline, tests, load table, one failure trace, and cleanup command. Explain:

- where authentication and object authorization would run;
- which state requires durable storage in production;
- where duplicate delivery can occur after adding a broker;
- how readiness, draining, and shutdown deadlines interact; and
- what each measurement does not prove.

Success means overload is visible and bounded, duplicates produce one logical job, all goroutines or threads terminate, and rerunning starts cleanly.
