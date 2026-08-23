# Software Foundations

**Status:** In progress  
**Orientation time:** 5 minutes

## What

This module builds a working model of the machinery beneath application code. It starts with the path from a Python file to observable output, then moves through operating systems, networking, storage, concurrency, and debugging. The emphasis is not memorizing trivia: it is learning which layer owns a behavior and what evidence that layer exposes.

## Why

Engineers lose time when they treat every failure as an application-code failure. A slow request may be waiting for CPU time, blocked on a syscall, faulting memory pages, resolving DNS, or buffering output. Understanding the execution stack makes logs, process tools, traces, and resource metrics explainable instead of mysterious.

## Where It Fits

This is the first technical module in the curriculum. It supplies the vocabulary and causal models used later in backend engineering, distributed systems, containers, cloud platforms, observability, performance work, and AI infrastructure. Later modules assume you can move between source-level behavior and operating-system evidence.

## Prerequisites

- Basic command-line navigation (`cd`, `ls`, and running a command)
- Ability to read and edit a small Python program
- Access to Linux for the hands-on lab; a Linux VM, container, or WSL 2 is sufficient
- No prior operating-systems or compiler coursework

## Outcomes

After this module, you should be able to:

- Trace software behavior across language runtime, OS, memory, scheduler, CPU, and I/O layers.
- Distinguish a process from a program and virtual memory from physical memory.
- Use process and filesystem evidence to test an execution hypothesis.
- Explain common failures at the layer that causes them.
- Communicate a compact execution model without hiding behind “the runtime handles it.”

## Completed Lesson

1. [How Software Actually Executes](./01-how-software-actually-executes.md) — follow Python source through CPython and Linux to CPU execution and output.

## Roadmap

Remaining lessons:

- Operating Systems, Processes, and Threads
- Memory, Storage, and Filesystems
- Networking from Socket to Service
- Concurrency, Parallelism, and Coordination
- Debugging with Evidence

## Competency Tiers

### Minimum Competency

You can identify the major execution layers, explain the difference between Python bytecode and CPU instructions, inspect a Linux process with `ps` and `/proc`, and locate failures in the right layer.

### Strong Engineer

You can connect process state, memory mappings, scheduling, syscalls, buffering, and exit status to production symptoms. You form testable hypotheses and choose evidence before changing code.

### Deep Dive

You can reason from CPython implementation details and Linux kernel interfaces, qualify version-dependent behavior, and use low-level tools such as `strace`, debuggers, and profilers without confusing observations at one layer for causes at another.

## Learning Policy

### AI Tutor

Use AI to ask for alternate explanations, diagrams, or targeted questions after making your own first pass. Require it to distinguish facts from simplifications and verify low-level claims against canonical documentation.

### AI Pair Programming

Use AI to suggest experiments or small code changes, but predict the result before running them. Read every command, understand its scope, and keep ownership of the hypothesis being tested.

### AI Review

Ask AI to challenge your explanation for missing layers, incorrect terminology, and unsupported conclusions. Treat the response as review input, not proof; resolve disagreements with runtime evidence and primary sources.

### No-AI Challenge

Complete each lesson’s no-AI exercise without an assistant. Documentation, manual pages, and the program’s own output are allowed. The goal is to make the model retrievable when an assistant is unavailable.

### Explain Back

After using AI, close it and explain the concept from memory using a concrete example. If you cannot predict what the OS or runtime will do next, revisit the evidence and try again.
