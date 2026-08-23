# Start Here

Begin with one working model of computation and one observed program. You need Python 3 for the first lesson and Linux for the first lab. Prior systems experience is not required.

## Read these first

Open these exact files in order:

1. [README.md](README.md)
2. [HOW-TO-LEARN.md](HOW-TO-LEARN.md)
3. [00-history/01-origins-of-computing.md](00-history/01-origins-of-computing.md)
4. [01-software-foundations/01-how-software-actually-executes.md](01-software-foundations/01-how-software-actually-executes.md)
5. [labs/01-software-execution/README.md](labs/01-software-execution/README.md)
6. [TEACH-BACK.md](TEACH-BACK.md)
7. [PROGRESS.md](PROGRESS.md)

Do not survey the whole repository first. These files establish the vocabulary and evidence habits used later.

## First session

In [00-history/01-origins-of-computing.md](00-history/01-origins-of-computing.md), predict the demonstration’s output before running it. Identify the stored state, the instruction being applied, and the resulting state.

Then read [01-software-foundations/01-how-software-actually-executes.md](01-software-foundations/01-how-software-actually-executes.md). In the lab, start a Python process and inspect its PID, memory mappings, resident memory, file descriptors, and output destination.

Write down one prediction that was correct and one that changed.

## Finish line

You are ready to continue when you can do the following without a script:

- explain why stored programs make hardware reusable;
- distinguish source code, an executable runtime, and a process;
- explain why a CPU does not execute Python source directly;
- inspect a process by PID and identify where its standard output goes;
- distinguish an address-space mapping from resident physical memory;
- state what your observation supports and what it leaves uncertain.

Record the evidence in [PROGRESS.md](PROGRESS.md), then continue with [00-history/README.md](00-history/README.md).

## If you are blocked

Use [CONCEPT-INDEX.md](CONCEPT-INDEX.md) for unfamiliar terms. Preserve exact command errors and observations. If Linux is unavailable, complete the reading now and return to the lab in a Linux VM or other environment that exposes `/proc`.
