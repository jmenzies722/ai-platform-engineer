# Production Go Services

A production Go service is a lifecycle: construct dependencies, serve bounded work, expose evidence, drain, and release every owned resource.

## Why it matters

The handler can be correct while deployment still drops requests because readiness changes too late, timeouts are missing, or background goroutines outlive shutdown. Go makes starting concurrency easy. Service quality comes from making ownership, budgets, configuration, and termination equally easy to inspect.

## How it works

Construct configuration and dependencies explicitly in `main`, then pass narrow values into packages. Validate configuration before listening and keep secrets out of errors and diagnostics. Package-level globals hide tests and lifecycle. Return cleanup functions or give owned components `Close` methods with idempotent behavior.

An `http.Server` needs read-header, request-handling, idle, and response policies appropriate to its exposure; a blanket timeout can be wrong for streaming. Limit body size before decoding, reject malformed input, and propagate `r.Context()` into dependencies. Context carries cancellation and request-scoped metadata across an operation; do not store it in structs or use it as an optional-parameter bag. The caller usually owns cancellation.

Bound outbound transports and reuse clients. Creating a new `http.Client` or transport per request defeats connection pooling. Set end-to-end deadlines, classify errors, and close response bodies. Bound database pools and worker concurrency based on downstream capacity. Every goroutine needs a clear owner, stop signal, and join path.

For shutdown, receive a termination signal into a root context, fail readiness so new traffic stops, allow propagation, call server shutdown with a bounded context, stop producers, drain or persist accepted work according to contract, close dependencies, and wait for goroutines. A second signal or expired deadline can force exit. Liveness should prove the process can make local progress; readiness should represent whether it should receive new work without turning every shared dependency wobble into total removal.

Observability uses structured logs, stable metric names with bounded labels, trace context, and profiles protected from public access. Build metadata and configuration shape aid incident comparison. Profiles are powerful and may contain sensitive names or operational detail.

## See it yourself

Predict that cancellation stops the worker before its timer and that `Wait` proves it exited.

```bash
cat >/tmp/lifecycle.go <<'EOF'
package main
import (
	"context"
	"fmt"
	"sync"
	"time"
)
func main() {
	ctx, cancel := context.WithCancel(context.Background())
	var wg sync.WaitGroup
	wg.Add(1)
	go func(){ defer wg.Done(); select {
	case <-ctx.Done(): fmt.Println("stopped:", ctx.Err())
	case <-time.After(time.Second): fmt.Println("finished")
	} }()
	cancel()
	wg.Wait()
}
EOF
go run /tmp/lifecycle.go
rm -f /tmp/lifecycle.go
```

Expected observation: cancellation becomes observable and the process waits for worker completion.

Limits of the observation: there is no HTTP listener, signal race, buffered job, forced deadline, or dependency cleanup. Printing a cancellation does not prove production draining.

## Where it shows up

A service owns an HTTP server, database pool, telemetry exporter, and outbox publisher. Startup validates schema compatibility before readiness. Shutdown first removes readiness, then stops HTTP admission, lets handlers finish, stops outbox polling, flushes telemetry within a bound, closes the pool, and verifies the goroutine group is empty.

## When it breaks

Goroutine count climbing suggests leaked sends, blocked reads, missing body closes, or forgotten tickers. File-descriptor growth points to connections or files not closed. Shutdown resets suggest the load balancer still assigned traffic or deadlines were misaligned. Capture goroutine dump, open descriptor count, pool statistics, server error logs, signal timestamp, readiness transition, in-flight requests, and shutdown phase durations. Do not expose `pprof` unauthenticated on a public listener.

## Practice

**Build:** complete the module lab with explicit construction, `/live`, `/ready`, bounded work, request IDs, runtime metrics, and a protected profile listener. **Break:** leak a response body in a disposable client, block a worker, send malformed and oversized bodies, and terminate during load. **Explain back:** account for every resource from creation to release. Success includes clean race tests, no goroutine growth after repeated requests, graceful drain evidence, and a forced-shutdown test.

## Check yourself

1. Why should readiness usually change before HTTP shutdown begins?
2. What is wrong with creating a new HTTP transport for every request?

## Sources

### REQUIRED

- [Go net/http Package](https://pkg.go.dev/net/http)
- [Go context Package](https://pkg.go.dev/context)

### RECOMMENDED

- [Go Diagnostics](https://go.dev/doc/diagnostics)
- [Go Execution Tracer](https://go.dev/blog/execution-traces-2024)

### DEEP DIVE

- [Go Blog: Pipelines and Cancellation](https://go.dev/blog/pipelines)

## Next

Continue to [Software Architecture](../11-software-architecture/README.md).
