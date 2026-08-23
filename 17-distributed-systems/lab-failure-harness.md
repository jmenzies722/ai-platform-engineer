# Lab: expose duplicate work and overload

Build a local queue simulator that makes ambiguous completion, duplicate delivery, and finite capacity visible.

## Goal

Produce an idempotent worker with a bounded queue, then prove that response loss does not duplicate a side effect and overload does not consume unbounded memory.

## Before you start

Read lessons 6 and 7. Use Python 3 and a temporary directory; no network, credentials, privileges, or cost are required. Stop if you adapt the lab to any shared queue. Before running, predict side-effect count and rejected submissions.

## Establish a baseline

`python3 --version` must print Python 3. Run a one-item `queue.Queue(maxsize=1)` put/get smoke test; successful exit establishes the runtime and bounded primitive.

## Make it work

Write a small producer/consumer program with `Queue(maxsize=10)`, operation IDs, a locked result dictionary, attempt counts, and a 50 ms consumer delay. Submit 30 operations with nonblocking admission. For admitted operations, enqueue selected IDs twice to model redelivery. Print accepted, rejected, unique effects, duplicates, and oldest age.

## Break it

After recording the baseline, remove the result-dictionary check but change nothing else. The expected symptom is `unique effects` remaining plausible while the raw side-effect count exceeds unique admitted operation IDs.

## Diagnose it

Start with the user-visible invariant: one effect per admitted ID. Compare IDs in the side-effect log to the result dictionary and attempt counts. Restore the atomic check, rerun the same input, and prove every admitted ID has at most one effect while overload remains explicit as rejection.

## Clean up

Delete the temporary program and output. Confirm no Python process or temporary file from the lab remains.

## What to keep

Keep the prediction, counts, duplicated IDs, correction, and a production policy for key retention, retry ownership, admission, and queue-age alerting. Explain why the queue absorbs a burst but cannot repair a sustained rate mismatch.

## Sources

- [Python queue documentation](https://docs.python.org/3/library/queue.html)
