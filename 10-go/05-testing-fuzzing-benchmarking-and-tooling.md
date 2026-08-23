# Testing, Fuzzing, Benchmarking, and Tooling

Go’s toolchain makes evidence cheap when tests isolate contracts and benchmarks control the work they claim to measure.

## Why it matters

A test that sleeps until a goroutine “probably finished” is flaky synchronization. A benchmark that includes setup in one version but not another is a persuasive fiction. Fast feedback comes from deterministic units, explicit seams, adversarial fuzz inputs, race-enabled execution, and measurements whose environment and uncertainty are visible.

## How it works

Table-driven tests express input, expected output, and a descriptive case name. Keep cases independent; subtests may run in parallel only when captured variables and shared fixtures are safe. Test observable behavior rather than private implementation details. Small interfaces should usually be declared by the consuming package, allowing a hand-written fake without forcing every dependency behind an interface.

HTTP handlers can be tested with `httptest` without binding a real port. Integration tests cross real adapters such as a database and belong behind explicit setup, cleanup, and perhaps build tags. Avoid package-global mutable fixtures. `TestMain` is useful for process-wide setup but can make isolation harder.

Fuzz tests start from seed corpus entries, generate inputs, and preserve values that cause crashes or violated invariants. Good fuzz properties include round-trip preservation, parser nonpanic, canonicalization idempotence, and agreement between implementations. Fuzzing finds examples, not proof; resource limits and semantic assertions still matter.

Benchmarks run functions beginning with `Benchmark`, repeat work according to `b.N` or the current benchmark API, and should move setup outside measured regions when setup is not the subject. Report allocations where relevant. Compare multiple samples with statistical tooling, pin material environment factors, and inspect profiles before rewriting code. A lower nanoseconds-per-operation result can still lose under realistic contention or larger data.

Standard checks include `gofmt`, `go vet`, `go test`, `go test -race`, fuzzing, benchmarks, coverage as a navigation signal, and dependency or vulnerability checks appropriate to the project. Coverage says which statements executed, not whether assertions were meaningful.

## See it yourself

Create a temporary module and predict three passing subtests.

```bash
d=$(mktemp -d)
cd "$d" || exit 1
go mod init example.test/normalize >/dev/null
cat >normalize_test.go <<'EOF'
package normalize
import (
	"strings"
	"testing"
)
func normalize(s string) string { return strings.ToLower(strings.TrimSpace(s)) }
func TestNormalize(t *testing.T) {
	for _, tc := range []struct{name, in, want string}{
		{"spaces", " Go ", "go"}, {"case", "HTTP", "http"}, {"empty", "", ""},
	} {
		t.Run(tc.name, func(t *testing.T) {
			if got:=normalize(tc.in); got!=tc.want { t.Fatalf("got %q want %q", got, tc.want) }
		})
	}
}
EOF
go test ./...
cd / && rm -rf "$d"
```

Expected observation: named cases pass in an isolated module.

Limits of the observation: the pure function has no concurrency, integration, malformed encoding policy, or benchmark. Three examples do not establish correctness for all Unicode input.

## Where it shows up

A JSON endpoint can have pure validation tables, handler contract tests with `httptest`, repository integration tests against a disposable database, a fuzz property that decoding never panics, and a load test outside `go test`. Each layer answers a different question and yields a different failure radius.

## When it breaks

Intermittent failures often reveal shared state, leaked goroutines, dependence on map order, wall-clock assumptions, port collisions, or missing cleanup. Benchmark variance can come from CPU scaling, background load, garbage collection, setup leakage, or inlining differences. Preserve seed, test name, repetition count, race output, Go version, platform, benchmark samples, and profile. Do not “repair” a flaky test with a longer sleep.

## Practice

**Build:** test a parser with tables, fuzz round trips, benchmark two implementations, and add a race-enabled concurrent test. **Break:** introduce a shared loop variable, leaked goroutine, and benchmark setup cost one at a time. **Explain back:** state what each tool proves and misses. Success includes deterministic synchronization, automatic cleanup, reproducible fuzz seeds, allocation counts, and a statistically supported benchmark comparison.

## Check yourself

1. Why is coverage percentage not a measure of assertion quality?
2. What setup must be excluded from a benchmark comparison, and when should it remain included?

## Sources

### REQUIRED

- [Go Testing Package](https://pkg.go.dev/testing)
- [Go Fuzzing](https://go.dev/doc/security/fuzz/)

### RECOMMENDED

- [Go Blog: Subtests and Sub-benchmarks](https://go.dev/blog/subtests)
- [Go pprof Package](https://pkg.go.dev/runtime/pprof)

### DEEP DIVE

- [Go Wiki: Performance](https://go.dev/wiki/Performance)

## Next

Continue to [Production Go Services](./06-production-go-services.md).
