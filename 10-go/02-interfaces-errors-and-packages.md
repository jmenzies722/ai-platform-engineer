# Interfaces, Errors, and Packages

Go programs stay understandable when package boundaries expose small behavior contracts and failures remain explicit.

## Why it matters

A storage package that exports a twenty-method interface forces every test fake and alternate implementation to depend on behavior its caller never uses. Likewise, matching error strings turns added context into a breaking change. Small consumer-owned interfaces and wrapped error identities let packages evolve without hiding failure meaning.

## How it works

An interface is satisfied implicitly by a type’s method set. Functions should usually accept the smallest behavior they need. Errors are ordinary values; callers inspect or wrap them with context. Packages define namespaces and visibility through capitalization, while import cycles are forbidden.

An interface value carries a dynamic type and value; a concrete type satisfies an interface implicitly through its method set. This enables decoupling at the use site, but an interface containing a typed nil pointer is itself non-nil because its dynamic type is present. Interfaces should usually be declared near consumers and contain only operations that consumer needs. Packages define import boundaries and exported names; Go rejects import cycles, encouraging dependencies to point in one direction. Errors implement a small interface and are handled as values. `fmt.Errorf` with `%w` preserves a cause in an unwrap chain, while `errors.Is` and `errors.As` inspect identity or type without parsing text. Context should state the failed operation and relevant non-secret identity; classification should tell callers which policy is safe.

## See it yourself

Predict the printed message to include `load profile` while `errors.Is` still reports true for `ErrMissing`. Replacing `%w` with `%v` should preserve text but lose the unwrap relationship.

```bash
cat >/tmp/go-errors.go <<'EOF'
package main
import ("errors"; "fmt")
var ErrMissing=errors.New("missing")
func load() error { return fmt.Errorf("load profile: %w", ErrMissing) }
func main(){ err:=load(); fmt.Println(err, errors.Is(err,ErrMissing)) }
EOF
go run /tmp/go-errors.go
rm -f /tmp/go-errors.go
```

Expected observation: Wrapping adds operation context while `errors.Is` preserves machine-checkable classification.

Limits of the interfaces, errors, and packages observation: The example does not define retry policy, structured error fields, package layout, or behavior of a typed nil interface. It demonstrates wrapping and identity inspection.

## Where it shows up

A user service may depend on a two-method repository interface while PostgreSQL and in-memory implementations live outside domain policy. The HTTP adapter can map a not-found sentinel to 404 and an unavailable typed error to 503 while retaining operation context in logs. Because the interface belongs to the service, adding a database administration method does not burden every caller or fake.

## When it breaks

`err != nil` with a seemingly nil pointer suggests a typed nil inside an interface; tests breaking after harmless wording changes suggest string matching; import cycles indicate responsibilities are coupled in both directions. First print `%T` for the unexpected dynamic type and use `errors.Is/As` against documented categories. For package cycles, draw actual import directions before extracting a generic dumping-ground package.

## Practice

**Build:** define a minimal repository interface at a consumer, implement a fake, and wrap not-found errors with operation context. **Break:** return a typed nil pointer as an interface and replace `%w` with `%v`, writing tests that reveal each trap. **Explain back:** describe dynamic type/value, method set, package direction, error context, and classification. Success is table-driven behavior tests that avoid error-string equality and compile with both implementations.

## Check yourself

1. Where should an interface normally be declared?
2. Why use `%w` when wrapping an error?

## Sources

### REQUIRED

- [Go errors package](https://pkg.go.dev/errors)

### RECOMMENDED

- [Go blog: errors are values](https://go.dev/blog/errors-are-values)

### DEEP DIVE

- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)

## Next

Continue to [Goroutines, Channels, and Cancellation](./03-goroutines-channels-and-cancellation.md).
