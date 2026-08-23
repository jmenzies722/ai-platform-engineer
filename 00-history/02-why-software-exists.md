# Why Software Exists

Software lets us change what a machine does by changing instructions instead of rebuilding the machine.

## Why it matters

**Prerequisite:** [Origins of Computing](./01-origins-of-computing.md).

A machine that must be rewired for every task is expensive to change. Encoding behavior as stored instructions moved change out of the hardware and into an artifact people could copy, test, and revise.

That artifact is software. It made general-purpose computing practical, then introduced a different problem: large bodies of changeable instructions are hard to understand and coordinate. Modules, APIs, services, and infrastructure as code all manage that complexity.

## How it works

Software is an executable specification plus state. It translates human intent through layers until hardware can perform deterministic transitions; every translation adds leverage and possible mismatch.

Humans write source against language and library contracts. Toolchains translate it into machine instructions; an OS creates a process and mediates resources. Inputs and persistent state shape execution, while logs and metrics expose only selected internal events.

Software is cheap to copy but expensive to understand and evolve. Brooks’s essential complexity comes from the problem domain; accidental complexity comes from tools and representations. Good abstractions compress repeated decisions without erasing constraints operators must still see.

## Vocabulary

- **Program:** Stored instructions and data describing a computation.
- **Process:** One OS-managed running instance of a program.
- **Algorithm:** A finite procedure for transforming input into a result.
- **State:** Information retained at a point in a computation.
- **Side effect:** An observable change outside a function's returned value.
- **Interface:** A defined boundary through which components interact.
- **Contract:** Promised behavior and constraints at an interface.
- **Abstraction:** A contract that exposes useful behavior while hiding selected details.
- **Idempotency:** The property that repeating an operation has the same intended effect as doing it once.
- **Essential complexity:** Difficulty inherent in the problem being solved.
- **Accidental complexity:** Difficulty introduced by tools, representations, or implementation choices.

## See it yourself

```text
intent: add two inputs safely
parse(input_a, input_b)
validate(type=integer, range=-2^31..2^31-1)
result = checked_add(input_a, input_b)
emit(result)
```

Choose `7` and `5` as inputs and predict the emitted result; then choose a value outside the stated range. The valid case should reach `emit(12)`, while the invalid case should stop at validation in a real implementation. The trace supports the claim that software turns intent into explicit contracts and operations. Pseudocode is not an executable proof of parser, overflow, or recovery behavior.

## Where it shows up

Terraform is software that translates a desired resource description into provider API calls. A plan makes part of that translation reviewable, state records known resource identity, and apply performs side effects against an asynchronous remote system. If the provider changes behavior or an operator edits the resource directly, configuration, recorded state, and reality diverge. The abstraction improves repeatability without removing the need to inspect the execution layer.

## When it breaks

A deployment may report success while the service still behaves incorrectly. The specification may be incomplete, generated artifacts may differ, a dependency may drift, or a hidden side effect may fail after the main return. First compare the intended contract, produced artifact, runtime state, and external effect, stopping at the earliest boundary where they disagree.

## Practice

### Observe

Write one task as manual shell steps, then as an idempotent script. Run each twice, interrupt midway, and compare recoverability and observability.

### Build

Design a small declarative job format and interpreter supporting input validation, steps, retries, and explicit outputs.

### Break

Introduce malformed input, stale state, a non-idempotent retry, and an unavailable dependency. Make failures bounded and diagnosable.

### Say it out loud

Explain why a correct specification can still produce a wrong running system.

**Success:** Your account should name a translation boundary, persistent state, one side effect, and the evidence that locates divergence.

## Check yourself

1. Why is software more than encoded instructions?
2. What distinguishes essential from accidental complexity?
3. When does reuse become harmful coupling?

### Interview stretch

- Why do declarative systems still need operators who understand imperative execution?
- What makes an interface durable?
- Explain idempotency using a deployment operation.

## Sources

### REQUIRED

- “No Silver Bullet” — Frederick P. Brooks Jr. [University of North Carolina](https://www.cs.unc.edu/techreports/86-020.pdf). Distinguishes essential and accidental software complexity.

### RECOMMENDED

- “Software Engineering” — NATO Science Committee. [NATO conference report](http://homepages.cs.ncl.ac.uk/brian.randell/NATO/nato1968.PDF). Documents why programming became an engineering coordination problem.

### DEEP DIVE

- “On the Criteria To Be Used in Decomposing Systems into Modules” — D. L. Parnas. [ACM DOI](https://doi.org/10.1145/361598.361623). Establishes information hiding as a basis for evolvable software.

## Next

Continue with [./03-machine-code-assembly-high-level-languages.md](./03-machine-code-assembly-high-level-languages.md).
