# Concept Index

Use this index when a term appears before its lesson. Start with the introductory lesson, then follow the deeper module when you need implementation or operational detail.

Search this file with your browser’s Find command.

| Concept | Question | Start here | Continue with |
|---|---|---|---|
| Abstraction | How can I use something without carrying every detail in my head? | [Why Software Exists](00-history/02-why-software-exists.md) | [Software Architecture](11-software-architecture/README.md), [Control Planes](23-control-planes/README.md) |
| Agent | How can software choose and perform several steps toward a goal? | [Agentic Engineering](00-history/20-agentic-engineering.md) | [Agentic Infrastructure](33-agentic-infrastructure/README.md) |
| Assembly language | How do symbolic instructions become exact processor instructions? | [Machine Code to Assembly](00-history/03-machine-code-assembly-high-level-languages.md) | [Computer Systems](03-computer-systems/README.md) |
| Attention | How can a model weigh which other tokens matter for each token? | [Transformers and LLMs](00-history/17-transformers-and-llms.md) | [Transformers and LLMs](26-transformers-llms/README.md) |
| Backpressure | What should a system do when work arrives faster than it can finish? | [Distributed Systems](00-history/09-distributed-systems.md) | [Distributed Systems](17-distributed-systems/README.md), [Model Serving](31-model-serving/README.md) |
| Bytecode | What intermediate instructions does CPython execute? | [How Software Executes](01-software-foundations/01-how-software-actually-executes.md) | [Python](02-python/README.md) |
| Cloud computing | How did compute become a programmable, metered service? | [Virtualization and Cloud](00-history/10-virtualization-and-cloud.md) | [AWS](12-aws/README.md) |
| Compiler | How does one program representation become another? | [Machine Code to Assembly](00-history/03-machine-code-assembly-high-level-languages.md) | [How Software Executes](01-software-foundations/01-how-software-actually-executes.md) |
| Container | How can an application carry its environment while sharing a host kernel? | [Containers](00-history/12-containers.md) | [Linux](04-linux/README.md), [Containers](15-containers/README.md) |
| Control plane | How does a system turn declared intent into ongoing action? | [Kubernetes](00-history/13-kubernetes.md) | [Control Planes](23-control-planes/README.md) |
| CPU | What physically performs a program’s instructions? | [Origins of Computing](00-history/01-origins-of-computing.md) | [Computer Systems](03-computer-systems/README.md) |
| Database | How can many users share durable, queryable records? | [Databases](00-history/08-databases.md) | [Databases](08-databases/README.md) |
| Debugging | How do I reduce uncertainty from evidence rather than guesses? | [How Software Executes](01-software-foundations/01-how-software-actually-executes.md) | [Observability](18-observability/README.md), [SRE](19-sre/README.md) |
| Distributed system | What changes when components communicate over an unreliable network? | [Distributed Systems](00-history/09-distributed-systems.md) | [Distributed Systems](17-distributed-systems/README.md) |
| File descriptor | How does a process refer to an open file, pipe, terminal, or socket? | [How Software Executes](01-software-foundations/01-how-software-actually-executes.md) | [Linux](04-linux/README.md) |
| GPU | Why are some processors better at many similar operations? | [Origins of Computing](00-history/01-origins-of-computing.md) | [GPU Systems](29-gpu-systems/README.md) |
| Interpreter | What executes another program’s representation? | [How Software Executes](01-software-foundations/01-how-software-actually-executes.md) | [Python](02-python/README.md) |
| Kernel | Which privileged software controls shared hardware and protection? | [Evolution of Operating Systems](00-history/05-evolution-of-operating-systems.md) | [Linux](04-linux/README.md) |
| Kubernetes | How can a cluster keep correcting itself toward declared workload state? | [Kubernetes](00-history/13-kubernetes.md) | [Kubernetes](16-kubernetes/README.md) |
| Large language model | How can next-token prediction produce useful language behavior? | [Transformers and LLMs](00-history/17-transformers-and-llms.md) | [Transformers and LLMs](26-transformers-llms/README.md), [LLM Engineering](27-llm-engineering/README.md) |
| Machine code | What instruction representation can a CPU execute directly? | [Machine Code to Assembly](00-history/03-machine-code-assembly-high-level-languages.md) | [Computer Systems](03-computer-systems/README.md) |
| Machine learning | How can behavior be fitted from examples rather than handwritten rules? | [Machine Learning](00-history/16-machine-learning.md) | [AI Foundations](24-ai-foundations/README.md), [ML and Deep Learning](25-ml-deep-learning/README.md) |
| Memory hierarchy | Why is nearby storage small and fast while distant storage is large and slow? | [Origins of Computing](00-history/01-origins-of-computing.md) | [Computer Systems](03-computer-systems/README.md), [GPU Systems](29-gpu-systems/README.md) |
| Network protocol | How can independently built computers agree on message meaning and delivery? | [Networking and the Internet](00-history/07-networking-and-the-internet.md) | [Networking](07-networking/README.md) |
| Observability | What evidence lets us ask new questions about a running system? | [SRE and Observability](00-history/14-sre-and-observability.md) | [Observability](18-observability/README.md) |
| Operating system | How can many programs safely share one machine? | [Evolution of Operating Systems](00-history/05-evolution-of-operating-systems.md) | [How Software Executes](01-software-foundations/01-how-software-actually-executes.md), [Linux](04-linux/README.md) |
| Platform engineering | How can repeated infrastructure work become safe self-service? | [Platform Engineering](00-history/15-platform-engineering.md) | [Platform Engineering](21-platform-engineering/README.md), [Developer Platforms](22-developer-platforms/README.md) |
| Process | What is the difference between stored code and one running instance? | [How Software Executes](01-software-foundations/01-how-software-actually-executes.md) | [Linux](04-linux/README.md) |
| Reconciliation | How can a controller repeatedly close the gap between desired and actual state? | [Kubernetes](00-history/13-kubernetes.md) | [Control Planes](23-control-planes/README.md) |
| Runtime | What machinery supports a language while a program runs? | [How Software Executes](01-software-foundations/01-how-software-actually-executes.md) | [Python](02-python/README.md), [Go](10-go/README.md) |
| Scheduler | Who decides which ready work gets a CPU or cluster resource next? | [Evolution of Operating Systems](00-history/05-evolution-of-operating-systems.md) | [Linux](04-linux/README.md), [Kubernetes](16-kubernetes/README.md), [AI Infrastructure](30-ai-infrastructure/README.md) |
| SLI / SLO | How do we measure user-visible reliability and set a target? | [SRE and Observability](00-history/14-sre-and-observability.md) | [SRE](19-sre/README.md) |
| System call | How does ordinary software safely request a protected kernel operation? | [How Software Executes](01-software-foundations/01-how-software-actually-executes.md) | [Linux](04-linux/README.md) |
| Transformer | What architecture uses attention to process token relationships in parallel? | [Transformers and LLMs](00-history/17-transformers-and-llms.md) | [Transformers and LLMs](26-transformers-llms/README.md) |
| Virtual memory | How does each process get its own address space without owning all physical RAM? | [How Software Executes](01-software-foundations/01-how-software-actually-executes.md) | [Computer Systems](03-computer-systems/README.md), [Linux](04-linux/README.md) |
| Virtualization | How can one physical machine present several isolated logical machines? | [Virtualization and Cloud](00-history/10-virtualization-and-cloud.md) | [AWS](12-aws/README.md), [Containers](15-containers/README.md) |

## Common distinctions

- **Program vs process:** stored instructions vs one OS-managed execution.
- **Compiler vs interpreter:** translation vs execution strategy; one runtime can use both.
- **Virtual machine vs container:** virtualized hardware/guest kernel vs isolated processes sharing a host kernel.
- **Observability vs monitoring:** ability to investigate internal behavior vs checking known conditions.
- **Platform vs portal:** a reliable set of capabilities and contracts vs one possible interface.
- **Model vs agent:** a parameterized prediction system vs a bounded execution loop that may use a model and tools.

For concise definitions, use [GLOSSARY.md](GLOSSARY.md).
