# Teach Back

If you can explain a system clearly, you probably have a usable model. If you can only repeat its vocabulary, you do not.

Use this rubric after every lesson. Explain once without notes, inspect the gap, then try again.

## The Three Audiences

### A curious friend

**Goal:** Make the problem and central idea feel obvious.

Include:

- the situation before the concept existed;
- one concrete analogy;
- what changed and why it helps;
- one honest limit of the analogy.

Avoid:

- acronyms;
- product names as explanations;
- invisible prerequisites;
- “basically” followed by unexplained jargon.

**Pass:** The listener can restate the idea and give a new example.

### A junior engineer

**Goal:** Supply vocabulary and a mechanism they can use while building or debugging.

Include:

- the precise engineering term and definition;
- components, boundaries, and state changes;
- one production location;
- one failure symptom and first evidence to inspect;
- what the abstraction hides.

**Pass:** The listener can draw the model and predict one behavior.

### An interviewer

**Goal:** Show a compact mental model, engineering judgment, and depth under follow-up.

In 60–90 seconds:

1. define the concept in one precise sentence;
2. state the problem it solves;
3. narrate the critical mechanism;
4. connect one production tradeoff or failure;
5. name useful evidence and one limit of the model.

**Pass:** Your answer remains coherent when a constraint changes.

## Scoring Rubric

Score each row from 0–2.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Starts with the problem | Opens with jargon/product | Problem is vague | Before-state and pressure are concrete |
| Language fits audience | Unexplained terms | Mostly appropriate | Every term earns its place |
| Mechanism | Labels only | Partial sequence | Causal, ordered, and bounded |
| Mental model | No drawable model | Model misses a boundary | Listener can redraw and narrate it |
| Production connection | None | Generic use case | Concrete system and consequence |
| Failure/debugging | “Check logs” | Names a failure | Symptom → hypothesis → evidence |
| Precision | False simplification | Correct but fuzzy | Correct, concise, states limits |
| Teachability | Memorized monologue | Understandable | Listener can transfer the model |

- **13–16:** usable explanation
- **9–12:** promising, but repair the lowest row
- **0–8:** return to Picture This, Mental Model, and Tiny Proof

Do not average away a zero in mechanism or precision.

## Example: Process

### To a curious friend

“A recipe sitting on a shelf is not dinner being cooked. In the same way, a program file is stored instructions, while a process is one active run with its own workspace and access to shared equipment. The operating system keeps track of that run so several programs can safely share the computer.”

### To a junior engineer

“A process is an OS-managed execution context: a PID, virtual address space, one or more threads, file descriptors, credentials, and execution state. Starting the same program twice creates two processes. If one is alive but not progressing, I first inspect its state, CPU-time change, wait channel, and open descriptors rather than rereading source blindly.”

### In an interview

“A program is stored code and data; a process is an OS-managed instance executing that program. On Linux, the process has a PID, virtual address space, threads, credentials, file descriptors, and scheduler state. The shell commonly creates a child and `execve` replaces its image with the target executable. This distinction matters operationally: a valid file does not prove startup, and an existing PID does not prove progress. I would use process state, CPU time, `/proc`, profiles, or syscall evidence to separate runnable, blocked, and failing behavior.”

## Example: Kubernetes Reconciliation

### To a curious friend

“A thermostat does not turn the heater on once and leave. It keeps comparing the room with your chosen temperature and corrects the difference. Kubernetes does that for applications: you describe the result you want, and it keeps checking and correcting the cluster.”

### To a junior engineer

“Kubernetes stores desired state as API objects. Controllers watch those objects and observed state, then perform idempotent actions to reduce the difference. Scheduling and node agents handle later boundaries. Convergence is asynchronous, so I inspect object generation, conditions, events, controller ownership, and node reality rather than assuming one API write immediately changed the workload.”

### In an interview

“Kubernetes is an API-driven distributed control plane built around reconciliation. Users declare desired state; controllers observe desired and actual state and repeatedly issue idempotent changes toward convergence. This separates intent from imperative orchestration and supports extensibility, but creates eventual consistency and asynchronous failure boundaries. In an incident I trace the object from admission and persisted intent through controller status, scheduling, node runtime, and network/storage dependencies. A present object proves accepted intent, not a healthy running workload.”

## A Reusable 90-Second Frame

> Before **[concept]**, people had **[concrete problem]**.
>
> **[Concept]** is **[precise definition]**.
>
> It works by **[ordered mechanism]**.
>
> In production, it appears in **[specific place]**.
>
> A common failure is **[symptom]**, so I inspect **[evidence]** first.
>
> The key tradeoff or limit is **[boundary]**.

Use the frame to organize thought, not as a script to memorize.

## Review Record

| Date | Concept | Audience | Lowest rubric row | Correction made | Evidence |
|---|---|---|---|---|---|
| YYYY-MM-DD | Process | Junior engineer | Failure/debugging | Added state and wait evidence | Lab note |
