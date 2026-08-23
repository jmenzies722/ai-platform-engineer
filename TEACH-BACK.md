# Teach Back

An explanation tests whether you can reconstruct a mechanism. Repeating the lesson’s phrasing tests memory of prose instead.

Use this rubric after every lesson. Explain once without notes, inspect the gap, then try again.

## Make the point first

Begin with the claim that matters. Define the problem, name the mechanism, and explain the practical consequence. Remove any term that does not help the listener predict behavior.

Adjust detail to the listener, but do not maintain three separate scripts. A new learner may need common language; an engineer may need boundary conditions and evidence. The underlying account must remain the same.

## Explain the mechanism

State:

- the relevant state and who owns it;
- the operation or decision that changes that state;
- the contract at each important boundary;
- one production location;
- one failure symptom and the first evidence you would inspect;
- a limit of the explanation.

An analogy is useful only when it clarifies a relation. State where it stops matching the real system.

## Score it

Score each row from 0–2.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Leads with the point | Opens with jargon or a product | Point is delayed | Claim and consequence are immediate |
| Language fits audience | Unexplained terms | Mostly appropriate | Every term earns its place |
| Mechanism | Labels only | Partial sequence | Causal, ordered, and bounded |
| Boundaries | Important boundary is absent | Boundary is named | Contract and limits are clear |
| Production connection | None | Generic use case | Concrete system and consequence |
| Failure/debugging | “Check logs” | Names a failure | Connects symptom, hypothesis, and evidence |
| Precision | False simplification | Correct but fuzzy | Correct, concise, states limits |
| Teachability | Memorized monologue | Understandable | Listener can transfer the model |

- **13–16:** usable explanation
- **9–12:** promising, but repair the lowest row
- **0–8:** return to the mechanism and demonstration

Do not average away a zero in mechanism or precision.

## Example

Consider a process:

> A program is stored code and data. A process is one operating-system-managed execution of that program, with an identity, virtual address space, threads, credentials, file descriptors, and scheduler state. Starting the same program twice creates two processes. In production, an existing PID proves that the process record exists, not that useful work is progressing. I would inspect process state, CPU-time change, wait state, open descriptors, and syscall or profile evidence before deciding why it is stuck.

The explanation leads with the distinction, supplies only the components needed for diagnosis, and limits the claim made by an existing PID.

## Review questions

- Can the listener state the main claim after one hearing?
- Can they predict one new case from the mechanism?
- Which sentence is unsupported or too broad?
- Which term can be removed?
- What observation would disprove your diagnosis?
- Does the explanation remain correct when the scale or failure assumption changes?

## Review record

| Date | Concept | Listener or setting | Lowest rubric row | Correction | Evidence |
|---|---|---|---|---|---|
| YYYY-MM-DD | Process | Study partner | Failure/debugging | Added state and wait evidence | Lab note |
