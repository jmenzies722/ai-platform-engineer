# 10 — Go

Write Go that remains understandable under aliasing, errors, concurrency, load, and shutdown. Read the lessons in order: language rules lead into runtime behavior, tests, and a production service lifecycle.

## What you will learn

By the end, you can:

- reason about values, pointers, slices, maps, methods, interfaces, and package boundaries;
- wrap and classify errors without losing causal detail;
- control goroutine lifetime with channels, contexts, synchronization, and ownership;
- explain allocation, escape analysis, garbage collection, scheduling, and data races;
- write table, fuzz, race, benchmark, integration, and HTTP tests; and
- build a bounded service with observability, profiling, configuration, and graceful shutdown.

## Lessons

1. [Values, Slices, and Methods](./01-values-slices-and-methods.md)
2. [Interfaces, Errors, and Packages](./02-interfaces-errors-and-packages.md)
3. [Goroutines, Channels, and Cancellation](./03-goroutines-channels-and-cancellation.md)
4. [Runtime, Memory, Scheduling, and Races](./04-runtime-memory-scheduling-and-races.md)
5. [Testing, Fuzzing, Benchmarking, and Tooling](./05-testing-fuzzing-benchmarking-and-tooling.md)
6. [Production Go Services](./06-production-go-services.md)

## Practice

[Build, Race, Profile, and Drain a Go Service](./lab-go-service.md) develops one small service through unit tests, a deliberate race, bounded concurrency, profiling, and signal-driven shutdown.

Practice is part of the path, not an optional recap. Predict first, work only in disposable or explicitly scoped resources, compare expected and actual observations, and perform the documented cleanup.

## Ready to continue

Continue when you can predict slice aliasing, defend an interface at its consumer, trace every goroutine’s exit, interpret race and escape reports, reject a misleading benchmark, and demonstrate a service draining within its deadline.

## Next

Start with [Values, Slices, and Methods](./01-values-slices-and-methods.md).
