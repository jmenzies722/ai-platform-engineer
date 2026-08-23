# Lab: Build, Race, Profile, and Drain a Go Service

Build one small Go service whose correctness includes startup, overload, and termination.

## Scaffold and contract

Create a temporary module outside this curriculum directory. Implement:

- `POST /work` with a limited JSON body and duration validation;
- a semaphore allowing two active jobs and an immediate overload response;
- `GET /live` and `GET /ready` with distinct meanings;
- structured request logs without body or credentials;
- signal-driven shutdown with a five-second maximum.

Keep domain validation in a package that imports no `net/http` types. Inject a clock or work function where deterministic tests need it. Reuse one configured server and outbound transport.

## Test before serving

Write table tests for bounds and malformed data, then handler tests with `httptest`. Add a fuzz test asserting that arbitrary request bodies never panic and cannot bypass the size limit. Use channels rather than sleeps to coordinate the concurrency test.

Run:

```bash
gofmt -w .
go vet ./...
go test ./...
go test -race ./...
```

Introduce one deliberate unsynchronized request counter, preserve the race report, repair it with an ownership or synchronization decision, and rerun the detector. Explain why a passing non-race run was not contrary evidence.

## Overload and profile

Start the server only on loopback. Hold two requests in the work function using a test-controlled channel, then submit a third and prove it is rejected within a stated latency bound. Record active count, accepted rate, rejected rate, and handler latency.

Protect diagnostic endpoints on a separate loopback listener. Capture a goroutine profile while work is blocked and identify the stacks you expect. If you benchmark a hot function, collect multiple samples and allocation counts. Do not claim a service speedup from a microbenchmark alone.

## Drain

With work in flight:

1. deliver the termination signal;
2. observe readiness become false;
3. verify new admission stops;
4. release one request and let it finish;
5. keep another blocked until the shutdown deadline;
6. prove the process follows the documented forced path.

Repeat with all work finishing inside the budget. Join background goroutines, stop tickers, close listeners, and flush telemetry within its own bound. A goroutine dump after repeated tests should not show growth from service-owned workers.

## Deliverable

Provide the package dependency sketch, API contract, test output, deliberate race and repair, overload timeline, selected profile excerpt, and both shutdown timelines. For each artifact, state its limit. Include the exact cleanup command for temporary binaries, profiles, and test data.

Success means `go test -race ./...` passes, overload stays bounded, diagnostics are not public, every goroutine has an exit path, and both graceful and forced shutdown are repeatable.
