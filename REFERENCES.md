# Authoritative References

Use the label as a reading priority, not a quality ranking:

- **REQUIRED** — foundational reference for the curriculum.
- **RECOMMENDED** — practical depth for working engineers.
- **DEEP DIVE** — specification, paper, or internals reference for advanced study.

Links favor maintainers, standards bodies, official documentation, and primary papers. Product documentation evolves; record the version used in lab evidence.

## Computing History and Software Foundations

- **REQUIRED** — [Computer History Museum collections](https://computerhistory.org/collections/) — primary artifacts and curated historical records.
- **REQUIRED** — [Python 3 documentation](https://docs.python.org/3/) — language, library, C API, and interpreter reference.
- **RECOMMENDED** — [Linux man-pages project](https://man7.org/linux/man-pages/) — user-space interfaces to the Linux kernel and C library.
- **DEEP DIVE** — [Linux kernel documentation](https://docs.kernel.org/) — subsystem and kernel-internal documentation.
- **DEEP DIVE** — [Intel 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) — instruction-set and system programming reference.
- **DEEP DIVE** — [LLVM documentation](https://llvm.org/docs/) — compiler infrastructure, IR, optimization, and code-generation internals.

## Git and Software Delivery

- **REQUIRED** — [Git reference documentation](https://git-scm.com/docs) — canonical command and model reference.
- **RECOMMENDED** — [Pro Git](https://git-scm.com/book/en/v2) — maintained conceptual and practical guide.
- **REQUIRED** — [GitHub Actions documentation](https://docs.github.com/en/actions) — official workflow, security, and runner reference.
- **RECOMMENDED** — [DORA research program](https://dora.dev/research/) — evidence on software delivery and organizational performance.

## Linux, Containers, and Kubernetes

- **REQUIRED** — [Linux kernel documentation](https://docs.kernel.org/) — kernel subsystem reference.
- **RECOMMENDED** — [systemd documentation](https://systemd.io/) — service and host lifecycle management.
- **REQUIRED** — [Open Container Initiative specifications](https://opencontainers.org/) — image, runtime, and distribution standards.
- **RECOMMENDED** — [Docker documentation](https://docs.docker.com/) — practical image, engine, build, and container guidance.
- **REQUIRED** — [Kubernetes documentation](https://kubernetes.io/docs/) — concepts, tasks, API behavior, and operations.
- **DEEP DIVE** — [Kubernetes Enhancement Proposals](https://github.com/kubernetes/enhancements/tree/master/keps) — design history and feature contracts.

## Networking and Internet Protocols

- **REQUIRED** — [RFC 8200: Internet Protocol, Version 6](https://www.rfc-editor.org/rfc/rfc8200) — IPv6 specification.
- **REQUIRED** — [RFC 9293: Transmission Control Protocol](https://www.rfc-editor.org/rfc/rfc9293) — current TCP specification.
- **REQUIRED** — [RFC 1034: Domain Names—Concepts and Facilities](https://www.rfc-editor.org/rfc/rfc1034) and [RFC 1035: Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035) — DNS foundations.
- **REQUIRED** — [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — HTTP meaning independent of wire version.
- **RECOMMENDED** — [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446) — modern transport security protocol.
- **DEEP DIVE** — [IETF Datatracker](https://datatracker.ietf.org/) — standards work, drafts, and document history.

## Databases and Distributed Systems

- **REQUIRED** — [PostgreSQL documentation](https://www.postgresql.org/docs/) — relational database behavior and operations.
- **DEEP DIVE** — [Architecture of a Database System — Hellerstein, Stonebraker, Hamilton](https://dsf.berkeley.edu/papers/fntdb07-architecture.pdf) — database subsystem architecture.
- **REQUIRED** — [Time, Clocks, and the Ordering of Events in a Distributed System — Lamport](https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/) — causality and logical clocks.
- **REQUIRED** — [In Search of an Understandable Consensus Algorithm (Raft)](https://raft.github.io/raft.pdf) — approachable consensus algorithm and rationale.
- **DEEP DIVE** — [Paxos Made Simple — Lamport](https://www.microsoft.com/en-us/research/publication/paxos-made-simple/) — primary consensus reference.

## Cloud, Infrastructure as Code, and Architecture

- **REQUIRED** — [AWS documentation](https://docs.aws.amazon.com/) — service behavior, API contracts, quotas, and operational guidance.
- **RECOMMENDED** — [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) — quality-attribute review model.
- **REQUIRED** — [Terraform documentation](https://developer.hashicorp.com/terraform/docs) — language, state, lifecycle, providers, and workflows.
- **RECOMMENDED** — [Architecture Decision Records](https://adr.github.io/) — lightweight record of consequential decisions and context.
- **DEEP DIVE** — [The Twelve-Factor App](https://12factor.net/) — historically influential cloud-application principles; evaluate critically rather than treating as law.

## Observability and SRE

- **REQUIRED** — [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) — Google’s foundational SRE text.
- **REQUIRED** — [The Site Reliability Workbook](https://sre.google/workbook/table-of-contents/) — implementation-oriented reliability practices.
- **REQUIRED** — [OpenTelemetry documentation](https://opentelemetry.io/docs/) — vendor-neutral telemetry APIs, SDKs, and data model.
- **RECOMMENDED** — [Prometheus documentation](https://prometheus.io/docs/) — metric model, PromQL, instrumentation, and operations.
- **DEEP DIVE** — [W3C Trace Context](https://www.w3.org/TR/trace-context/) — interoperable distributed trace propagation.

## Security

- **REQUIRED** — [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) — risk-based security outcomes.
- **REQUIRED** — [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) — testable application security requirements.
- **RECOMMENDED** — [OWASP Top 10](https://owasp.org/www-project-top-ten/) — common web application risk categories.
- **RECOMMENDED** — [SLSA specification](https://slsa.dev/spec/) — software artifact integrity and supply-chain assurance.
- **DEEP DIVE** — [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final) — identity- and policy-centered security architecture.

## Platform Engineering and Control Planes

- **REQUIRED** — [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/) — definitions, capabilities, and platform-as-product framing.
- **RECOMMENDED** — [Backstage documentation](https://backstage.io/docs/) — developer portal and software catalog implementation reference.
- **RECOMMENDED** — [Crossplane documentation](https://docs.crossplane.io/) — declarative infrastructure control planes built on Kubernetes.
- **DEEP DIVE** — [Kubernetes API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md) — API and reconciliation conventions.

## Machine Learning and Deep Learning

- **REQUIRED** — [Machine Learning glossary — Google](https://developers.google.com/machine-learning/glossary) — concise terminology reference.
- **RECOMMENDED** — [scikit-learn user guide](https://scikit-learn.org/stable/user_guide.html) — classical ML workflows and evaluation.
- **REQUIRED** — [PyTorch documentation](https://pytorch.org/docs/stable/index.html) — tensors, autograd, distributed training, and runtime APIs.
- **DEEP DIVE** — [Deep Learning — Goodfellow, Bengio, Courville](https://www.deeplearningbook.org/) — freely available foundational text.

## Transformers, LLMs, and LLM Engineering

- **REQUIRED** — [Attention Is All You Need — Vaswani et al.](https://arxiv.org/abs/1706.03762) — transformer architecture.
- **REQUIRED** — [Language Models are Few-Shot Learners — Brown et al.](https://arxiv.org/abs/2005.14165) — scaling and in-context learning evidence.
- **RECOMMENDED** — [Hugging Face Transformers documentation](https://huggingface.co/docs/transformers/) — model APIs and implementation ecosystem.
- **RECOMMENDED** — [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — AI risk governance and measurement.
- **DEEP DIVE** — [HELM](https://crfm.stanford.edu/helm/latest/) — transparent, multi-metric language-model evaluation.

## GPU Systems, AI Infrastructure, and Model Serving

- **REQUIRED** — [CUDA C++ Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/) — GPU execution and programming model.
- **RECOMMENDED** — [NVIDIA Collective Communication Library documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/) — multi-GPU collectives and topology.
- **RECOMMENDED** — [NVIDIA Kubernetes device plugin](https://github.com/NVIDIA/k8s-device-plugin) — exposing GPU resources to Kubernetes.
- **REQUIRED** — [vLLM documentation](https://docs.vllm.ai/en/latest/) — high-throughput LLM inference and serving.
- **DEEP DIVE** — [Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180) — vLLM’s memory-management design.
- **RECOMMENDED** — [KServe documentation](https://kserve.github.io/website/) — Kubernetes-native model serving APIs and operations.
- **DEEP DIVE** — [MLSys proceedings](https://proceedings.mlsys.org/) — primary systems research for machine learning.

## Senior and Staff Engineering

- **RECOMMENDED** — [ACM Code of Ethics](https://www.acm.org/code-of-ethics) — professional responsibility and decision framing.
- **RECOMMENDED** — [Google Engineering Practices](https://google.github.io/eng-practices/) — review and change-quality practices.
- **DEEP DIVE** — [Software Engineering at Google](https://abseil.io/resources/swe-book) — software engineering under time and organizational scale.
