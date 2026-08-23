# 01 — Software Foundations

> **Status:** In progress · **Published lesson:** 1 · **Published lab:** 1

## 5-Minute Orientation

### What is this?

This module explains what actually happens between writing source code and seeing a result. Its current gold-standard lesson traces one memorable chain:

**Source → Runtime/Compiler → OS → Process → Memory → CPU → Output**

### Why does it matter?

“The code is broken” names no mechanism. This model lets you separate syntax, runtime, process, memory, scheduling, syscall, and output problems—and choose evidence for the correct boundary.

### Where does it fit?

History explained why software and operating systems exist. This module turns that story into an inspectable Linux process. Python, Linux, containers, Kubernetes, and AI runtimes all depend on this model.

### What do I need first?

- [Origins of Computing](../00-history/01-origins-of-computing.md) for the state-transition model
- [Why Software Exists](../00-history/02-why-software-exists.md) for the program/hardware distinction
- Linux for the lab; the lesson itself requires no prior programming experience

### What will I be able to explain afterward?

- the difference among source code, a runtime, an executable, and a process;
- why CPython both compiles and interprets;
- what the operating system, virtual memory, scheduler, and CPU each do;
- how output reaches a terminal or file and why it can appear late;
- how to find the last proven layer when execution fails.

## Competency Tiers

### Minimum Competency

Draw the seven-link chain from memory, run the Tiny Proof, complete the guided lab path, and explain the result to a non-engineer.

### Strong Engineer

Inspect process state, mappings, CPU/wait behavior, and file descriptors; break one boundary safely; diagnose it from evidence; explain unsupported conclusions.

### Deep Dive

Read CPython and Linux internals sources, compare language implementations, and connect execution costs to container limits and production performance.

## AI Learning Policy

### AI Tutor

Ask for one question at a time or request a different analogy. Do not ask AI to answer the Knowledge Check before your first attempt.

### AI Pair

Predict every command’s effect before running it. Use AI only after you can identify which execution layer the command inspects.

### AI Review

Give AI your evidence and explanation; ask it to find leaps in inference, not to replace your explanation.

### No-AI Challenge

Repeat the process inspection using only Python, `ps`, `/proc`, shell built-ins, and official documentation.

### Explain Back

Use `print("hello")` to narrate the full chain at friend, junior-engineer, and interview depth without notes.

## Published Path

1. Read [How Software Actually Executes](./01-how-software-actually-executes.md).
2. Complete [Inspect a Python Process on Linux](../labs/01-software-execution/README.md).
3. Record evidence in [PROGRESS.md](../PROGRESS.md).

## Planned Scope

Future lessons may cover processes and threads, memory, files and I/O, concurrency, runtimes, linking, and debugging. They are intentionally not represented by empty files. The published lesson and lab are the complete current learning surface.

## Next

Open [01-software-foundations/01-how-software-actually-executes.md](./01-how-software-actually-executes.md).
