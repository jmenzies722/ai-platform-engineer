# Glossary

Every entry has four teaching fields:

- **Plain definition:** the idea before specialized vocabulary.
- **Precise definition:** the engineering contract.
- **First lesson:** the gentlest introduction, not the most advanced source.
- **Explain in one breath:** a short, accurate answer you can say aloud.

Use [CONCEPT-INDEX.md](CONCEPT-INDEX.md) when you need the deeper curriculum path.

## A

### Abstraction

- **Plain definition:** A simpler way to use something without thinking about all of its machinery at once.
- **Precise definition:** A contract that exposes selected behavior while hiding implementation details; hidden details can still leak through limits, performance, and failure.
- **First lesson:** [Why Software Exists](00-history/02-why-software-exists.md)
- **Explain in one breath:** “An abstraction gives me a stable promise so I can work at a higher level, but the hidden layer still matters when the promise reaches a limit.”

### Agent

- **Plain definition:** Software that repeatedly looks at a situation, chooses an allowed action, and checks what happened while pursuing a goal.
- **Precise definition:** A policy- and resource-bounded execution loop combining model decisions, tools, state, control flow, evaluation, and optional human approval.
- **First lesson:** [Agentic Engineering](00-history/20-agentic-engineering.md)
- **Explain in one breath:** “An agent is a bounded observe–decide–act loop, not just a model response, so tools, permissions, state, budgets, and recovery are part of the system.”

### Assembly language

- **Plain definition:** Human-readable names for the small instructions a processor understands.
- **Precise definition:** A symbolic representation of machine instructions and addresses translated by an assembler into machine code for an instruction-set architecture.
- **First lesson:** [Machine Code to Assembly](00-history/03-machine-code-assembly-high-level-languages.md)
- **Explain in one breath:** “Assembly names CPU instructions and operands; an assembler encodes those symbols as machine code.”

## B

### Bytecode

- **Plain definition:** Compact intermediate instructions meant for a language runtime rather than directly for the physical CPU.
- **Precise definition:** An instruction representation for a virtual machine or interpreter; CPython code objects contain Python bytecode that native CPython code evaluates.
- **First lesson:** [How Software Actually Executes](01-software-foundations/01-how-software-actually-executes.md)
- **Explain in one breath:** “CPython compiles source to Python bytecode, then native interpreter instructions implement that bytecode on the CPU.”

## C

### Compiler

- **Plain definition:** A translator that turns one form of program into another.
- **Precise definition:** A system that transforms a source representation into a target representation while preserving the source language’s defined semantics.
- **First lesson:** [Machine Code to Assembly](00-history/03-machine-code-assembly-high-level-languages.md)
- **Explain in one breath:** “A compiler translates program representations—perhaps source to bytecode or machine code—so compiled and interpreted are not exclusive language identities.”

### Container

- **Plain definition:** A standard application package run in a separated area of a shared machine.
- **Precise definition:** An isolated process or process group launched from an image; on Linux it uses namespaces, cgroups, mounts, capabilities, and runtime conventions while sharing the host kernel.
- **First lesson:** [Containers](00-history/12-containers.md)
- **Explain in one breath:** “A container is isolated processes plus a packaged filesystem and configuration, not a lightweight virtual machine with its own kernel.”

### Control plane

- **Plain definition:** The part of a system that accepts what you want, decides what should happen, and keeps checking the result.
- **Precise definition:** Components that expose intent APIs, persist desired state, make decisions, and reconcile or configure data-plane resources.
- **First lesson:** [Kubernetes](00-history/13-kubernetes.md)
- **Explain in one breath:** “The control plane turns declared intent into repeated decisions; the data plane performs the actual work.”

### CPU

- **Plain definition:** The physical processor that performs a computer’s general-purpose instruction steps.
- **Precise definition:** A processor that fetches, decodes, and executes instructions while operating on registers and interacting with caches, memory, and devices.
- **First lesson:** [Origins of Computing](00-history/01-origins-of-computing.md)
- **Explain in one breath:** “The CPU performs native instructions and state changes; runtimes and operating systems organize which instructions execute and when.”

## D

### Database

- **Plain definition:** A disciplined shared record keeper that helps people find and change information without losing agreed facts.
- **Precise definition:** A managed system for storing and retrieving data while providing selected guarantees for structure, concurrency, integrity, durability, and recovery.
- **First lesson:** [Databases](00-history/08-databases.md)
- **Explain in one breath:** “A database connects logical queries to physical storage while coordinating concurrent changes and recovery.”

### Distributed system

- **Plain definition:** A system made from computers that coordinate by sending messages and can fail separately.
- **Precise definition:** A system whose components communicate over a network under independent failure, variable delay, and incomplete knowledge.
- **First lesson:** [Distributed Systems](00-history/09-distributed-systems.md)
- **Explain in one breath:** “Distribution adds capacity and fault isolation, but messages, partial failure, and uncertain time remove the guarantees of one machine.”

## F

### File descriptor

- **Plain definition:** A small number a process uses as a handle for an open input or output route.
- **Precise definition:** A per-process integer referring to an open kernel-managed object such as a file, pipe, terminal, socket, or device.
- **First lesson:** [How Software Actually Executes](01-software-foundations/01-how-software-actually-executes.md)
- **Explain in one breath:** “A file descriptor is the process’s numbered handle; fd 1 can point to a terminal, file, pipe, or socket.”

## I

### Interpreter

- **Plain definition:** A program that carries out instructions written in another program representation.
- **Precise definition:** A system that directly implements the semantics of an input representation, often after parsing or compiling it into an intermediate form.
- **First lesson:** [How Software Actually Executes](01-software-foundations/01-how-software-actually-executes.md)
- **Explain in one breath:** “An interpreter executes a program representation; CPython first compiles source to bytecode and then interprets that bytecode.”

## K

### Kernel

- **Plain definition:** The protected manager that controls shared hardware and the boundaries between programs.
- **Precise definition:** The privileged core of an operating system that manages scheduling, memory, devices, filesystems, protection, and system-call interfaces.
- **First lesson:** [Evolution of Operating Systems](00-history/05-evolution-of-operating-systems.md)
- **Explain in one breath:** “The kernel owns protected resources and lets user processes request controlled operations through system calls.”

### Kubernetes

- **Plain definition:** A system that repeatedly corrects a cluster toward the application state you declared.
- **Precise definition:** An extensible API-driven distributed control plane that reconciles desired and observed workload and infrastructure state.
- **First lesson:** [Kubernetes](00-history/13-kubernetes.md)
- **Explain in one breath:** “Kubernetes stores desired state and uses asynchronous controllers, schedulers, and node agents to converge actual state toward it.”

## L

### Large language model (LLM)

- **Plain definition:** A model trained on text patterns to predict the next token and generate sequences.
- **Precise definition:** A high-capacity parameterized model trained to estimate token-sequence distributions, often adapted for instruction following and tool use.
- **First lesson:** [Transformers and LLMs](00-history/17-transformers-and-llms.md)
- **Explain in one breath:** “An LLM predicts token distributions from context; useful application behavior adds prompting, data, tools, evaluation, serving, and safety boundaries.”

## M

### Machine code

- **Plain definition:** The bit patterns a particular kind of processor can execute directly.
- **Precise definition:** Binary-encoded instructions and operands defined by a processor instruction-set architecture.
- **First lesson:** [Machine Code to Assembly](00-history/03-machine-code-assembly-high-level-languages.md)
- **Explain in one breath:** “Machine code is the CPU’s encoded instruction format; source and bytecode need lower-level machinery before the CPU can execute them.”

### Machine learning

- **Plain definition:** Fitting behavior from examples instead of writing every rule by hand.
- **Precise definition:** Optimizing a parameterized model against data and an objective so it generalizes measured behavior to new inputs.
- **First lesson:** [Machine Learning](00-history/16-machine-learning.md)
- **Explain in one breath:** “Machine learning derives parameters from data and objectives, so model quality depends on data, optimization, evaluation, and deployment conditions.”

## O

### Observability

- **Plain definition:** The ability to understand what a system is doing from useful evidence it exposes.
- **Precise definition:** A system property that enables investigation of internal behavior from telemetry, state, and debuggable interfaces, including questions not anticipated in advance.
- **First lesson:** [SRE and Observability](00-history/14-sre-and-observability.md)
- **Explain in one breath:** “Observability is the ability to ask and answer new questions from evidence, not the number of dashboards.”

### Operating system

- **Plain definition:** Software that safely shares a computer and gives programs common ways to use it.
- **Precise definition:** System software that multiplexes hardware resources, enforces protection, and exposes abstractions such as processes, files, virtual memory, and sockets.
- **First lesson:** [Evolution of Operating Systems](00-history/05-evolution-of-operating-systems.md)
- **Explain in one breath:** “The operating system turns hardware into protected shared abstractions, and those abstractions leak through scheduling, memory, I/O, and permissions.”

## P

### Process

- **Plain definition:** One active, OS-managed run of a program.
- **Precise definition:** An operating-system execution context with an identity, virtual address space, resources, security credentials, state, and one or more threads.
- **First lesson:** [How Software Actually Executes](01-software-foundations/01-how-software-actually-executes.md)
- **Explain in one breath:** “A program is stored instructions; a process is one managed execution with a PID, memory, threads, descriptors, credentials, and state.”

## R

### Reconciliation

- **Plain definition:** Repeatedly compare what should exist with what does exist, then take a safe step to close the gap.
- **Precise definition:** A control loop that observes desired and actual state and performs idempotent actions toward convergence.
- **First lesson:** [Kubernetes](00-history/13-kubernetes.md)
- **Explain in one breath:** “Reconciliation replaces one-shot commands with a loop that keeps driving actual state toward declared intent.”

### Runtime

- **Plain definition:** The machinery that supports a program while it runs.
- **Precise definition:** Services and implementation machinery for execution, potentially including interpretation, compilation, allocation, garbage collection, libraries, and interfaces to the operating system.
- **First lesson:** [How Software Actually Executes](01-software-foundations/01-how-software-actually-executes.md)
- **Explain in one breath:** “A runtime implements language behavior and mediates between source-level operations and lower-level OS and machine mechanisms.”

## S

### Scheduler

- **Plain definition:** The decision maker that chooses which ready work gets a resource next.
- **Precise definition:** A subsystem that selects runnable work for constrained execution resources such as CPUs, cluster nodes, or accelerators according to policy and state.
- **First lesson:** [Evolution of Operating Systems](00-history/05-evolution-of-operating-systems.md)
- **Explain in one breath:** “A scheduler maps ready work onto limited resources, so alive and runnable do not mean executing right now.”

### Service-level indicator (SLI)

- **Plain definition:** A number that measures behavior users care about.
- **Precise definition:** A quantitative measure of service behavior, such as the proportion of valid requests completed successfully within a latency threshold.
- **First lesson:** [SRE and Observability](00-history/14-sre-and-observability.md)
- **Explain in one breath:** “An SLI measures user-relevant behavior; it is the data an SLO sets a target for.”

### Service-level objective (SLO)

- **Plain definition:** A reliability target for a user-relevant measurement over a stated period.
- **Precise definition:** A target range or threshold for an SLI over a defined window, used to govern reliability expectations and tradeoffs.
- **First lesson:** [SRE and Observability](00-history/14-sre-and-observability.md)
- **Explain in one breath:** “An SLO says how reliable a measured user experience should be and makes the cost of reliability explicit.”

### System call

- **Plain definition:** A controlled request from an ordinary program to the protected operating-system kernel.
- **Precise definition:** A defined transition through which a user-space thread requests a kernel service such as I/O, mapping memory, or process operations.
- **First lesson:** [How Software Actually Executes](01-software-foundations/01-how-software-actually-executes.md)
- **Explain in one breath:** “A syscall crosses the user/kernel boundary for protected work; most ordinary language operations do not need one.”

## T

### Thread

- **Plain definition:** One sequence of execution within a process.
- **Precise definition:** A schedulable execution stream with registers and a stack that usually shares its process’s address space and resources with other threads.
- **First lesson:** [How Software Actually Executes](01-software-foundations/01-how-software-actually-executes.md)
- **Explain in one breath:** “The scheduler runs threads; threads in one process usually share memory and file descriptors but keep separate execution state.”

### Transformer

- **Plain definition:** A neural-network architecture that learns which other tokens matter when processing each token.
- **Precise definition:** A sequence-model architecture centered on attention and position-wise transformations, enabling parallel training over token sequences.
- **First lesson:** [Transformers and LLMs](00-history/17-transformers-and-llms.md)
- **Explain in one breath:** “A transformer repeatedly combines token representations through attention and feed-forward layers; scale turns that mechanism into large language models.”

## V

### Virtualization

- **Plain definition:** Making physical resources look like isolated logical machines or environments.
- **Precise definition:** Mediating hardware or resource interfaces to create isolated logical computing environments decoupled from their physical implementation.
- **First lesson:** [Virtualization and Cloud](00-history/10-virtualization-and-cloud.md)
- **Explain in one breath:** “Virtualization inserts a control boundary that lets multiple logical environments share physical resources with isolation.”

### Virtual memory

- **Plain definition:** The private address map a process uses instead of naming physical RAM locations directly.
- **Precise definition:** A process-visible address space translated by hardware and the OS to physical pages, files, shared mappings, or no current backing.
- **First lesson:** [How Software Actually Executes](01-software-foundations/01-how-software-actually-executes.md)
- **Explain in one breath:** “Virtual memory gives each process an address space; mapped size and currently resident physical pages are different facts.”
