# Runtime, Memory, Scheduling, and Races

Go hides much runtime machinery, but production behavior still depends on where values live, when goroutines run, and who synchronizes shared memory.

## Why it matters

A tiny subslice can retain a huge byte array, a loop can allocate on every request because a value escapes, and code that “worked for months” can corrupt state because two goroutines race. Garbage collection prevents many lifetime errors; it does not choose ownership, bound retention, or make compound operations atomic.

## How it works

The compiler may place a value on a goroutine stack when its lifetime is proven local, or on the heap when it escapes. This is an implementation decision, not a language guarantee. Stacks grow and move. Heap objects remain reachable through roots until garbage collection determines otherwise. A slice or string view can keep its full backing storage reachable; copy a small retained portion when ownership and memory lifetime justify it.

Go’s concurrent garbage collector traces reachable objects and uses brief stop-the-world phases. Allocation rate, live heap size, pointer density, and memory limit influence CPU and pause behavior. `GOGC` adjusts the heap-growth target relative to live data; `GOMEMLIMIT` gives the runtime a soft memory limit. Aggressive collection can spend substantial CPU without repairing an actual leak.

The scheduler maps goroutines onto operating-system threads through logical processors controlled by `GOMAXPROCS`. A goroutine can be descheduled at many safe points, and blocking syscalls or synchronization affect execution. Scheduler fairness and map iteration order are not contracts. Never use timing assumptions as synchronization.

The memory model defines when one goroutine’s writes are guaranteed visible to another. Channel operations, mutexes, atomics, and other synchronization create happens-before relationships. A data race is concurrent access to the same memory where at least one access writes and no synchronization orders them. Race-free programs gain sequentially consistent behavior under the memory model; “it is only a boolean” is not synchronization.

## See it yourself

Predict a race report and a final count that is not a valid correctness argument. Run only on disposable code.

```bash
cat >/tmp/race.go <<'EOF'
package main
import ("fmt"; "sync")
func main() {
	var n int
	var wg sync.WaitGroup
	for i := 0; i < 2; i++ {
		wg.Add(1)
		go func(){ defer wg.Done(); for j:=0; j<1000; j++ { n++ } }()
	}
	wg.Wait()
	fmt.Println(n)
}
EOF
go run -race /tmp/race.go || true
rm -f /tmp/race.go
```

Expected observation: the race detector identifies conflicting accesses with stack traces. The printed value may vary and may even be 2000.

Limits of the observation: the detector reports races exercised in this run, not all possible races. It does not detect deadlocks, higher-level atomicity errors, or unsafely shared state in unexecuted paths.

## Where it shows up

A metrics collector that appends labels into a caller-owned slice may race with request code and retain request buffers. The repair can transfer ownership through a channel, copy at the boundary, or protect shared state with a mutex. Profiles decide whether copying matters; the memory model decides whether it is correct.

## When it breaks

Growing resident memory with a stable live heap may point to stacks, fragmentation, runtime metadata, or unreleased native memory; a growing live heap needs a heap profile and retention path. High GC CPU suggests allocation churn or an inappropriately tight memory limit. Sporadic corruption demands a race-enabled reproduction. Capture runtime metrics, heap and allocation profiles, goroutine dump, `GODEBUG` traces when scoped, and exact binary version. Do not tune `GOGC` before identifying retained objects and allocation rate.

## Practice

**Build:** implement a concurrent counter with mutex, atomic, and single-owner channel variants, documenting each contract. **Break:** retain a tiny subslice of a large allocation and create a deliberate race in a test. **Explain back:** connect escape, reachability, scheduling, synchronization, and detector evidence. Success includes a clean `go test -race`, before-and-after memory profiles, and no performance claim from a single run.

## Check yourself

1. Why can a small slice retain a much larger allocation?
2. Why does a correct final value in one run not disprove a data race?

## Sources

### REQUIRED

- [The Go Memory Model](https://go.dev/ref/mem)
- [Go Runtime Package](https://pkg.go.dev/runtime)

### RECOMMENDED

- [Data Race Detector](https://go.dev/doc/articles/race_detector)
- [Go Diagnostics](https://go.dev/doc/diagnostics)

### DEEP DIVE

- [A Guide to the Go Garbage Collector](https://go.dev/doc/gc-guide)

## Next

Continue to [Testing, Fuzzing, Benchmarking, and Tooling](./05-testing-fuzzing-benchmarking-and-tooling.md).
