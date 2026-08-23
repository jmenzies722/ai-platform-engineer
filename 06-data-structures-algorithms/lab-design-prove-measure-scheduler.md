# Lab: Design, Prove, and Measure a Scheduler

Build a scheduler twice: first as a simple reference, then with a heap and dictionary. The optimized version is complete only when it preserves the reference contract.

## Define the contract

Jobs have unique string IDs, integer priorities where smaller means earlier, and payloads. `put` inserts or replaces by ID. `cancel` reports whether a live job existed. `pop` returns the smallest `(priority, insertion_sequence)` live job and raises `IndexError` when empty. Replacing a job gives it a new sequence.

Write edge cases before implementation: duplicate ID, equal priority, canceled minimum, replacement to a later priority, and empty pop.

## Build the reference

Store live jobs in a dictionary containing priority, sequence, and payload. On `pop`, use `min` over live values, then delete the chosen ID. This costs linear time but keeps the contract visible. Assert after every operation that keys equal embedded job IDs and sequences are unique.

## Build the optimized version

Maintain the same live dictionary plus a heap of `(priority, sequence, job_id)`. `put` adds a new heap record and replaces the live dictionary entry. `cancel` deletes only the live entry. `pop` discards heap records until the tuple agrees with the current live entry, then removes and returns it.

State the invariant precisely: every live dictionary entry has at least one matching heap tuple, and a heap tuple is current only when its priority and sequence match the live entry. The heap may contain stale tuples.

## Differential proof

Generate a fixed-seed sequence of at least 5,000 bounded `put`, `cancel`, and `pop` operations over twenty IDs and five priorities. Apply each operation to both implementations. Compare return values, exceptions, and normalized live state after every operation. Print the seed and first mismatching prefix.

Expected observation: correct implementations remain equivalent. Remove the stale-entry check and the generated sequence should expose an incorrect pop.

## Measure honestly

For several live sizes, time equivalent batches that begin from equivalent state and produce the same checksum. Separate construction from operations. Count reference comparisons and optimized heap pushes and pops in addition to elapsed time. Report medians and environment, and explain why one benchmark cannot prove asymptotic bounds.

## Failure review

Classify every discovered mismatch as contract ambiguity, representation-invariant failure, implementation defect, or unequal benchmark. Minimize one failing operation sequence manually or with a reducer.

## Cleanup

The lab needs only Python’s standard library. Work in a temporary directory, preserve your report elsewhere, and remove generated files and caches when finished.

## Next

Continue to [Correctness, Testing, and Algorithm Selection](./06-correctness-testing-and-algorithm-selection.md).
