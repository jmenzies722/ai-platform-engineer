# Values, Slices, and Methods

Go’s compact value model becomes predictable when you distinguish copied values from descriptors that share underlying storage.

## Why it matters

A Go helper can accept a slice “by value” and still overwrite the caller’s elements because the copied descriptor points at the same backing array. Whether an API may retain, mutate, or append to a slice is therefore an ownership decision, not a slogan about value semantics. Tests need to cover both contents and alias behavior across capacity boundaries.

## How it works

Assignment copies a value. A slice contains a pointer, length, and capacity describing an array; copying the slice can still share elements. Maps and channels are reference-like runtime values. Methods attach behavior to named types, and pointer receivers can mutate the addressed value.

Go assignment copies the complete value being assigned. For an array that means all elements; for a slice it means a descriptor containing pointer, length, and capacity, so copied slices can share storage. Index assignment mutates the shared array. `append` reuses capacity when possible and otherwise allocates another array, which can cause two slices that once aliased to diverge. Maps and channels are descriptors to runtime-managed state and should not be copied mentally as independent collections. Struct assignment copies fields, including descriptor fields and synchronization values that may forbid copying after use. Methods belong to named types; the method set differs for value and pointer receivers. Value receivers receive a copy, while pointer receivers can mutate the addressed value and avoid copying large structs, but callers still need a clear concurrency contract.

## See it yourself

Predict that both `a` and `b` print a first element of nine because they share the backing array. Add an append with spare capacity and another beyond capacity, then predict aliasing separately.

```bash
cat >/tmp/go-values.go <<'EOF'
package main
import "fmt"
func main(){ a:=[]int{1,2}; b:=a; b[0]=9; fmt.Println(a,b) }
EOF
go run /tmp/go-values.go
rm -f /tmp/go-values.go
```

Expected observation: Both slices observe the changed first element because their descriptors refer to the same backing array.

Limits of the values, slices, and methods observation: The output does not reveal capacity changes, prove all slice operations share forever, or establish race safety. One goroutine performs one in-bounds mutation.

## Where it shows up

A decoder returning a slice into a reusable network buffer creates a production ownership hazard. The next read can overwrite bytes retained by a request handler, producing corruption far from the read. Copying at the boundary or transferring ownership explicitly costs memory bandwidth but gives the data a stable lifetime. Profiling can decide whether a pool is warranted only after correctness is established.

## When it breaks

Caller data changing after a helper suggests shared backing storage; only some appended values appearing suggests reallocation at a capacity threshold; races in maps or slices indicate unsynchronized shared mutation. First log or test length, capacity, and selected addresses in a minimal case, then run `go test -race` over the ownership boundary. Do not “fix” a race by adding sleeps or assuming append always allocates.

## Practice

**Build:** implement `Clone` for a slice and a type with value and pointer receiver methods whose effects are explicit. **Break:** retain a subslice of a reused buffer and write a test that exposes later corruption, then repair it with a copy. **Explain back:** distinguish copied descriptor, shared array, length, capacity, and receiver. Success includes alias assertions, boundary-capacity cases, and a clean race-detector run.

## Check yourself

1. What is copied when a slice is assigned?
2. When should a method use a pointer receiver?

## Sources

### REQUIRED

- [Go language specification](https://go.dev/ref/spec)

### RECOMMENDED

- [Effective Go](https://go.dev/doc/effective_go)

### DEEP DIVE

- [The Go Programming Language](https://www.gopl.io/)

## Next

Continue to [Interfaces, Errors, and Packages](./02-interfaces-errors-and-packages.md).
