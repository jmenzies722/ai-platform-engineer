# Goroutines, Channels, and Cancellation

Go makes concurrency cheap to start, not free to manage; every goroutine needs ownership and a termination path.

## Why it matters

Starting a goroutine for every request is easy; proving each goroutine stops when the request is canceled is the real engineering work. Leaked workers retain stacks, references, timers, and sometimes sockets, so latency incidents become memory incidents. Ownership must answer who starts work, who may cancel it, who closes channels, and who waits for termination.

## How it works

A goroutine executes concurrently. Channels communicate values and can coordinate ownership; closing a channel signals that no more values will be sent. `context.Context` carries cancellation and deadlines across call boundaries. `sync.WaitGroup` lets an owner wait for a known group to finish.

The `go` statement schedules a function independently and returns immediately. Channel send and receive synchronize according to buffering: an unbuffered operation pairs participants, while a buffered channel permits limited decoupling until capacity is reached. Closing records that no more values will be sent; receivers can drain remaining values and detect completion, but a send after close panics. The sender or coordinating owner that knows production is complete normally closes, never an arbitrary receiver. `WaitGroup` counts known goroutine lifetimes and must be incremented before the corresponding goroutine can finish. `context.Context` carries cancellation, deadline, and request-scoped values across API calls; blocking operations need a `select` or context-aware API to observe cancellation. The memory model defines which synchronization events make writes visible; merely starting goroutines does not make shared access safe.

## See it yourself

Predict two squared values in either order, then clean termination when the owner closes `out` after both senders finish. The loop must not wait forever for a third value.

```bash
cat >/tmp/go-concurrency.go <<'EOF'
package main
import ("fmt"; "sync")
func main(){ var wg sync.WaitGroup; out:=make(chan int,2); for _,n:=range []int{2,3}{ wg.Add(1); go func(n int){ defer wg.Done(); out<-n*n }(n) }; wg.Wait(); close(out); for n:=range out{ fmt.Println(n) } }
EOF
go run /tmp/go-concurrency.go
rm -f /tmp/go-concurrency.go
```

Expected observation: The owner waits for both senders, closes the channel once, and the range ends cleanly. Output order is unspecified.

Limits of the goroutines, channels, and cancellation observation: The sample does not propagate cancellation, limit a large job stream, prove output order, or permit concurrent map access. Its buffer is sized exactly for two sends.

## Where it shows up

A service fan-out to several dependencies should derive one context from the incoming deadline, start a bounded set of calls, and cancel remaining work once a decisive result or error is known. A result channel must not leave slower senders blocked after the receiver returns. Traces and goroutine profiles can show calls surviving past request completion, while a concurrency gauge reveals missing bounds.

## When it breaks

A steadily rising goroutine count suggests blocked sends, receives, timers, or dependency calls; `send on closed channel` identifies confused close ownership; race reports identify unsynchronized memory; requests outliving deadlines indicate cancellation is not observed. First capture a goroutine profile and stack groups plus the request’s cancellation timeline. Reproduce with a short deadline and bounded test; adding a larger channel only postpones a lifetime bug.

## Practice

**Build:** create a three-worker pool with fixed queue capacity, result collection, context cancellation, and one owner that closes each channel. **Break:** cancel while workers are blocked and write a test that would expose a leak or send-after-close; keep all waits bounded. **Explain back:** account for every goroutine from start to termination and every happens-before edge. Success means deterministic test completion, stable goroutine count after repeated runs, and `go test -race` passes.

## Check yourself

1. Who should close a channel?
2. Why should `context.Context` not be stored casually in a struct?

## Sources

### REQUIRED

- [Go memory model](https://go.dev/ref/mem)

### RECOMMENDED

- [Go blog: pipelines and cancellation](https://go.dev/blog/pipelines)

### DEEP DIVE

- [The Go Blog: context](https://go.dev/blog/context)

## Next

Continue to [Runtime, Memory, Scheduling, and Races](./04-runtime-memory-scheduling-and-races.md).
