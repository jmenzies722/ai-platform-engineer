# Concurrency and Waiting

Concurrency means multiple tasks make progress during overlapping periods; parallelism means work executes at the same instant.

## Why it matters

When a request is slow, “the thread is alive” does not reveal whether it is computing, queued for CPU, waiting for a socket, or blocked on a lock. Choosing more workers can improve overlap for waiting workloads but worsen contention or memory pressure. The engineering decision begins with the kind of waiting and the state that tasks share.

## How it works

The operating system schedules threads, pausing and resuming them. A thread waiting for a timer, file, lock, or network response consumes little CPU. Shared state needs coordination because operations can interleave. Processes isolate memory by default; threads share their process address space.

The scheduler chooses runnable threads and stops them when they block or are preempted. A timer sleep removes a thread from runnable work until the timer expires; an I/O wait resumes when the relevant event occurs. Threads in one process share objects and address space, so an interleaving can expose intermediate state unless synchronization establishes ordering. A mutex gives one holder exclusive access to a protected region, while condition variables and channels let tasks wait for state transitions. Processes normally isolate address spaces and communicate through kernel-managed mechanisms. CPython’s default global interpreter lock limits simultaneous Python bytecode execution in one interpreter, but threads can still overlap waits and native code may release the lock. Concurrency is therefore a lifetime and coordination property, not a promise of CPU parallelism.

## See it yourself

**Tiny Proof:** predict that the three tasks finish near one sleep interval rather than three intervals, while their printed order remains unspecified. Run it several times and note that a stable order on one machine is still not a contract.

```bash
python3 - <<'PY2'
import threading, time
def work(n):
    time.sleep(0.2)
    print(n)
ts=[threading.Thread(target=work,args=(n,)) for n in range(3)]
for t in ts: t.start()
for t in ts: t.join()
PY2
```

Expected observation: All three tasks overlap while sleeping. Output order is not a reliable contract unless you impose one.

Limits of the concurrency and waiting observation: The example does not demonstrate parallel execution, data-race safety, or useful throughput under load. Sleeping deliberately releases waiting time; a CPU-bound workload and a shared downstream dependency can behave very differently.

## Where it shows up

A backend that starts one thread per outbound call may initially hide network latency. During a dependency outage those threads remain waiting, consume stacks and descriptors, and eventually crowd out healthy requests. A bounded pool, propagated deadline, and cancellation path control lifetime, while wait-state and queue measurements show whether the bound is helping. Merely increasing the pool shifts overload rather than removing it.

## When it breaks

Lost updates appear as a final counter smaller than expected; deadlock appears as tasks that stop making progress while remaining alive; starvation lets some work progress while one participant waits indefinitely. First collect thread states, stacks or wait points, queue depth, and whether CPU time is changing. For a suspected race, create a small repeatable workload and run the language’s race detector where available; adding arbitrary sleeps is weak evidence and can hide the schedule that triggers the fault.

## Practice

**Build:** coordinate several workers to update a shared counter under a lock and verify the exact final value. **Break:** remove the lock in a disposable copy or acquire two locks in opposite order with timeouts, never leaving an unbounded hang. **Explain back:** separate concurrency, parallelism, waiting, and synchronization using the observed run. Success includes bounded termination, an invariant checked by code, and evidence that identifies where blocked work waits.

## Check yourself

1. Can concurrent work be non-parallel?
2. Why does adding threads not necessarily speed CPU-bound Python code?

## Sources

### REQUIRED

- [Python threading](https://docs.python.org/3/library/threading.html)

### RECOMMENDED

- [POSIX Threads](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/pthread.h.html)

### DEEP DIVE

- [The Art of Multiprocessor Programming](https://www.elsevier.com/books/the-art-of-multiprocessor-programming/herlihy/978-0-12-415950-1)

## Next

Continue to [Interfaces, State, and Data Flow](./04-interfaces-state-and-data-flow.md).
