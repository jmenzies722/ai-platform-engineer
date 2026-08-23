# 01 — Software Foundations

Software is not magic hidden behind syntax. This module follows a program from source text into a process, then studies the resources, timing, boundaries, and operational evidence that determine whether it behaves correctly. Read in order and run the proofs: later lessons depend on the distinctions established earlier.

## What you will learn

By the end, you can trace execution across runtime and operating-system boundaries; distinguish processes, threads, memory, files, and protocols; state concurrency and interface invariants; and investigate failures with observations rather than folklore. This is orientation, not mastery of every runtime or operating system.

## Lessons

1. [How Software Actually Executes](./01-how-software-actually-executes.md)
2. [Processes, Memory, and Files](./02-processes-memory-and-files.md)
3. [Concurrency and Waiting](./03-concurrency-and-waiting.md)
4. [Interfaces, State, and Data Flow](./04-interfaces-state-and-data-flow.md)
5. [Reliability, Errors, and Observability](./05-reliability-errors-and-observability.md)
6. [Software Lifecycle and Engineering Tradeoffs](./06-software-lifecycle-and-tradeoffs.md)

## Practice

[Make a Python Process Visible](../labs/01-software-execution/README.md) after lesson 2, then complete [Trace a Failure Across Boundaries](./lab-trace-a-failure.md) after lesson 5. Each lab asks for predictions, preserved evidence, and cleanup, not merely a successful command.

Practice is part of the path, not an optional recap. Predict first, work only in disposable or explicitly scoped resources, compare expected and actual observations, and perform the documented cleanup.

## Ready to continue

Continue when you can narrate one request from input through computation and output; identify ownership at every boundary; distinguish race, deadlock, timeout, crash, and bad contract; produce a minimal evidence bundle; and explain why a locally successful run is not yet a production reliability claim.

## Next

Start with [How Software Actually Executes](./01-how-software-actually-executes.md).
