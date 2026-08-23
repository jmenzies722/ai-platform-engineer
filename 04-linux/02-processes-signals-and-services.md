# Processes, Signals, and Services

Linux gives running work identities, parent relationships, states, and controlled ways to request termination.

## Why it matters

A service that ignores a deployment’s graceful-stop window may be hung, may be finishing in-flight work, or may never have received the signal in its namespace. Sending `SIGKILL` immediately sacrifices logs and cleanup without explaining the symptom. Safe operation starts with exact identity, current state, signal semantics, and who is responsible for collecting the exit status.

## How it works

A process contains one or more schedulable threads. The shell exposes a background child PID as `$!`; `ps` samples its state. Signals deliver asynchronous notifications. `SIGTERM` requests graceful termination and can be handled; `SIGKILL` cannot be handled and should be a last resort. Service managers supervise long-lived processes.

A process has a PID, credentials, address space, descriptor table, and at least one thread; Linux schedules threads rather than abstract service names. Parent and child relationships let a parent receive termination information through `wait`, preventing an exited child from remaining a zombie. Signals are numbered notifications with default actions; a process may catch, ignore, or block many of them. `SIGTERM` conventionally requests termination and allows handlers, whereas `SIGKILL` cannot be caught or deferred. Delivery to a multithreaded process and handling by a particular thread follow defined rules. A service manager adds desired-state policy: start ordering, environment, restart conditions, resource limits, and stop timeouts. A restarted PID is a new process even if the service name is unchanged.

## See it yourself

Predict that the background `sleep` is usually sampled in interruptible sleep, that `$!` agrees with `ps`, and that `wait` returns a signal-related nonzero status after `SIGTERM`. Record the actual status rather than assuming one shell convention.

```bash
sleep 30 &
pid=$!
ps -o pid,ppid,stat,etime,comm -p "$pid"
kill -TERM "$pid"
wait "$pid"; printf 'status=%s\n' "$?"
```

Expected observation: The process is visible before the signal, then `wait` reports signal-related termination status.

Limits of the processes, signals, and services observation: This run does not prove how an application handler drains work, whether a service manager will restart it, or why another process is sleeping. One state sample describes a moment, not an execution history.

## Where it shows up

Rolling deployment of an HTTP worker connects all the ideas. The supervisor sends a graceful signal, stops routing new requests, waits for active requests within a deadline, and then starts or retains enough workers for availability. Process state, open connections, handler logs, and supervisor events show whether shutdown is progressing. A hard kill may be appropriate after the explicit deadline, but it should be the final bounded action rather than the diagnostic first move.

## When it breaks

A process absent from `ps` suggests wrong identity or prior exit; state `D` suggests uninterruptible kernel wait; a zombie has exited but awaits collection; repeated new PIDs indicate a restart loop. First validate PID, owner, command line, parent, start time, and supervisor status, then capture state and logs before signaling. For a stuck graceful shutdown, inspect stacks, wait channels, and in-flight work rather than repeatedly sending the same signal.

## Practice

**Build:** complete [Inspect and Control One Linux Process](./lab-process-control.md), then write a bounded Python child that logs and exits on `SIGTERM`. **Break:** delay its handler within a documented timeout and observe the parent waiting; do not use unrelated PIDs. **Explain back:** contrast signal delivery, handler behavior, process exit, collection, and supervisor restart. Success requires one tracked PID, expected state observations, recorded exit status, and proof that cleanup left no child running.

## Check yourself

1. Why is `kill -9` a poor default?
2. What does a parent gain by waiting for a child?

## Sources

### REQUIRED

- [signal(7)](https://man7.org/linux/man-pages/man7/signal.7.html)

### RECOMMENDED

- [proc(5)](https://man7.org/linux/man-pages/man5/proc.5.html)

### DEEP DIVE

- [systemd.service(5)](https://man7.org/linux/man-pages/man5/systemd.service.5.html)

## Next

Continue to [Shell Composition and Safe Automation](./03-shell-composition-and-safe-automation.md).
