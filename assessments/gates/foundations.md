# Foundations Gate

This gate tests whether the learner can turn source code into an evidence-backed account of execution, resource use, correctness, and failure. It covers [history](../../00-history/README.md), [software foundations](../../01-software-foundations/README.md), [Python](../../02-python/README.md), and [computer systems](../../03-computer-systems/README.md).

## Prerequisites

- Complete the bounded proofs in the four modules and score at least 13/16 on a no-notes explanation using [TEACH-BACK.md](../../TEACH-BACK.md).
- Produce prior evidence from [Inspect One Python Process](../../labs/01-software-execution/README.md) and either [Build a Tested Streaming Package](../../02-python/lab-tested-streaming-package.md) or [Follow One Program Through the System](../../03-computer-systems/lab-follow-one-program.md).
- Be able to work on Linux without privileged access using Python 3, Bash, `/proc`, `ps`, and standard test tools.
- Show the prior work and current competency claims in [PROGRESS.md](../../PROGRESS.md). A completed checkbox is not prerequisite evidence by itself.

## Challenge

In a disposable directory, build a standard-library Python CLI that reads a bounded line-oriented input, validates and aggregates records, writes a deterministic report, and reports malformed input without losing accepted records. Cap input size and memory explicitly. Supply tests for empty input, malformed records, repeated keys, interrupted output, and one input large enough to expose accidental full materialization.

Before running it, draw the execution path from source and interpreter through process, virtual memory, file descriptors, system calls, buffering, and durable output. Predict process state, CPU-time behavior, memory growth, and output visibility for a small and a large fixture.

The evaluator then selects one fresh defect:

- a generator is accidentally materialized;
- output is buffered or flushed incorrectly;
- two names alias mutable state unexpectedly;
- a file descriptor is leaked on a failure path; or
- a result is correct for one encoding or byte-order assumption but not the declared contract.

The candidate must reproduce the symptom, preserve the baseline, locate the failed contract, correct it, and rerun the full bounded test and inspection sequence. The evaluator changes one requirement after recovery, such as lowering the memory budget or requiring atomic replacement of the report, and asks for a design adaptation.

All activity must remain local. Inspect only the recorded child PID. Do not increase the workload bounds, signal a process not started by the candidate, or retain sensitive environment or command-line content.

## Evidence packet

Include the [standard packet](../README.md#standard-evidence-packet) plus:

- CLI source, fixtures, tests, exact rerun command, Python version, and hashes of accepted inputs;
- a process identity record showing source argument, loaded executable, PID and parent, state samples, CPU time, memory fields, and file-descriptor destinations;
- small and large input measurements with a claim about algorithmic growth and a limit on that claim;
- the prediction, defect symptom, ranked hypotheses, discriminating observations, patch, and before/after test results;
- an explanation of `write`, language-level flush or close, and durable storage guarantees appropriate to the implementation;
- cleanup proof showing no child process or generated artifact remains outside the packet; and
- a one-page design note covering input contract, representation invariants, error ownership, resource limits, alternatives, and the changed requirement.

## Dimension requirements

- **Explain:** Distinguish source, interpreter, process, virtual address space, resident memory, descriptor, buffering, and durable output in one causal account. Explain why the relevant abstraction exists using a mechanism from [Why the Stack Exists](../../00-history/README.md).
- **Build:** Produce a deterministic, tested streaming CLI with explicit contracts, bounded resources, and correct cleanup on success and failure.
- **Debug:** Diagnose the hidden defect from process, test, memory, descriptor, or output evidence. Reject at least one plausible hypothesis and state what the evidence does not prove.
- **Operate:** Verify identity before inspection or signaling, monitor the bounded run, stop safely when assumptions fail, and prove process and file cleanup.
- **Design:** Defend the data representation and complexity, error and output semantics, and adaptation to the evaluator's changed requirement.

## Evaluator instructions

Prepare fresh synthetic fixtures and choose a defect the candidate has not already documented. Do not reveal the defect category until the symptom has been observed. Require a clean rerun and one live source or test change. Compare process observations with the candidate's predictions; variation is acceptable when explained from evidence.

Critical requirements:

- the program never reads an unbounded input wholly into memory unless the declared cap makes that choice explicit and measured;
- the candidate never targets a process by guessed PID or broad name match;
- malformed input cannot silently corrupt accepted output; and
- every mechanism claim is tied to an observation and bounded appropriately.

## Review prompts

1. What does the operating system execute, and what role does the `.py` file play?
2. Which state is owned by Python, the process, the kernel, and the filesystem?
3. Which observation distinguishes elapsed time from useful CPU work?
4. Why can virtual size, resident memory, and requested allocation all differ?
5. What would falsify the diagnosis of the hidden defect?
6. Which invariant makes the aggregation correct, and how do tests exercise it?
7. What guarantee does a successful function return provide about output visibility and durability?
8. How does the design change if the input is ten times larger but the memory budget is fixed?

## Pass and rework

Pass requires at least 2 in every dimension under [the rubric](../rubric.md), all critical requirements, a 13/16 or higher live teach-back with no zero in mechanism or precision, and reproducible clean-state execution.

Rework is assigned by claim:

- weak execution model: repeat the explanation against a new process trace;
- weak build evidence: add the missing contract or negative test and rerun from clean state;
- weak diagnosis: investigate a different defect without hints;
- weak operation: repeat identity, bounds, and cleanup on a fresh PID; or
- weak design: revise for a new resource or durability constraint and validate it.

## Remediation

Return only to the mechanism that failed: [software execution](../../01-software-foundations/01-how-software-actually-executes.md), [Python iteration and resources](../../02-python/06-iteration-resources-and-program-boundaries.md), [virtual memory](../../03-computer-systems/05-virtual-memory-and-address-translation.md), or [durable I/O](../../03-computer-systems/06-storage-filesystems-and-durable-io.md). Rerun the relevant bounded proof, record a corrected prediction, then attempt a fresh evaluator variant.
