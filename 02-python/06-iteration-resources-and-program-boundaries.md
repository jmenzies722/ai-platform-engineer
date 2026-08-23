# Iteration, Resources, and Program Boundaries

Iteration lets Python process values over time; context managers give acquired resources a visible lifetime. Together they support programs that remain correct when data is large or failures interrupt work.

## Why it matters

Reading an entire multi-gigabyte log into a list can exhaust memory even when each record is tiny. Streaming line by line bounds memory, but an iterator may be single-use and a file must close on every exit path. The design must specify consumption, error, and cleanup semantics rather than assuming a loop is harmless.

## How it works

An iterable can produce an iterator. Calling `iter` obtains it; each `next` yields a value or raises `StopIteration`. Iterator state advances, so many iterators cannot restart. A generator function containing `yield` returns a generator whose body runs lazily as values are requested. Generator expressions are lazy, unlike list comprehensions. Laziness bounds intermediate storage but postpones computation and errors until consumption.

A context manager’s enter operation acquires or exposes a resource and its exit operation performs cleanup while receiving exception information. The `with` statement guarantees exit is attempted for normal return and exceptions, though no in-process mechanism survives every forced termination. Files decode bytes using an explicit encoding, and newline and error policies matter at boundaries. Command-line programs should keep parsing, domain calculation, and I/O adapters separate; `main` maps outcomes to user-visible output and exit status. Atomic replacement commonly writes and flushes a temporary file in the destination filesystem before renaming it, with durability requirements documented separately.

## See it yourself

**Tiny Proof:** predict that generator messages interleave with consumption and that a second loop over the same generator yields nothing.

```bash
python3 - <<'PY2'
def values():
    for n in range(3):
        print("produce", n)
        yield n * n
stream = values()
print("created")
print("first", next(stream))
print("rest", list(stream))
print("again", list(stream))
PY2
```

Expected observation: creation runs no generator body, production happens on demand, and the exhausted generator does not restart.

Limits of this proof: a finite generator does not demonstrate file cleanup, backpressure, or bounded memory under a real parser. Laziness can still retain large referenced objects.

## Where it shows up

An import command can open an input file with UTF-8, yield validated records, transform them, and write to a temporary output under a context manager. The domain function can consume any iterable, while the command layer owns paths, diagnostics, and statuses. If record 50 fails, the contract decides whether to reject the entire file, report a line-specific error, or emit partial output. That policy must be settled before writing begins.

## When it breaks

An empty second pass suggests iterator exhaustion; errors appearing far from construction suggest deferred generator work; “too many open files” suggests resources outliving their scope; corrupted partial output suggests direct writes before validation completed. First identify who creates and consumes the iterator, inspect one-pass assumptions, and count open resources. Do not convert everything to a list as a default fix because that trades lifetime ambiguity for unbounded memory.

## Practice

**Build:** complete [Build a Tested Streaming Package](./lab-tested-streaming-package.md). **Break:** include malformed lines, consume one generator twice, and raise during output while confirming the input closes. **Explain back:** distinguish iterable, iterator, generator, context manager, parser, and command boundary. Success means memory does not grow with retained input records, line errors preserve context, all resources close, and `main` returns documented statuses.

## Check yourself

1. Why can an iterable be restartable while its iterator is not?
2. What cleanup guarantee does `with` provide, and what cannot it guarantee?

## Sources

### REQUIRED

- [Python iterator types](https://docs.python.org/3/library/stdtypes.html#iterator-types)

### RECOMMENDED

- [Python context managers](https://docs.python.org/3/reference/datamodel.html#context-managers)
- [Python input and output](https://docs.python.org/3/tutorial/inputoutput.html)

### DEEP DIVE

- [PEP 342: Coroutines via enhanced generators](https://peps.python.org/pep-0342/)

## Next

Continue to [Computer Systems](../03-computer-systems/README.md).
