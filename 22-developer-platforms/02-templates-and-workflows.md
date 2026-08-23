# Templates and self-service workflows

Templates create an initial shape; self-service workflows execute durable lifecycle changes. Keeping these concerns separate prevents copied scaffolding from becoming an unmaintainable control plane.

## Why it matters

Generated code diverges after creation. A template that only opens repositories moves upgrades to every team. A workflow without durable state cannot explain partial success or retry safely after a timeout.

## How it works

Use templates for deliberately owned files: project structure, contract examples, tests, and references to versioned capabilities. Minimize generated content and mark ownership. Shared behavior should live in versioned libraries, build actions, modules, and APIs so upgrades do not require overwriting application code.

A workflow collects minimum intent, validates and authorizes it, resolves policy, shows a plan, and creates an operation record before side effects. Each step has a stable key, bounded timeout, retry classification, output, and redacted audit event. On restart, it observes actual state before deciding the next action.

Distinguish compensation from reconciliation. A compensating action attempts to undo a completed step but may itself fail or be irreversible. Reconciliation drives declared resources toward intent and often handles long-lived drift better. Tell users which outcome applies.

Run with delegated, least-privilege workload identity rather than portal credentials. Destructive workflows require current dependency checks, explicit target and consequence, retention policy, and often a delayed or separately authorized execution. Publish who owns abandoned operations.

## Vocabulary

- **scaffolder:** mechanism rendering initial files from user input
- **workflow:** durable, observable sequence coordinating side effects
- **compensation:** explicit action intended to offset an earlier side effect
- **operation record:** durable state and evidence for one workflow invocation

## See it yourself

Run a three-step paper workflow: reserve service ID, create repository, request database. Inject a timeout after each side effect but before success is recorded. Predict retry behavior. Stable idempotency keys and observation recover safely; blind create repeats can duplicate resources. This test does not prove provider APIs honor idempotency, which must be verified.

## Where it shows up

A create-service workflow writes catalog intent, creates a repository, requests runtime capabilities, and reports conditions. Later upgrade and retirement workflows reuse the same identity and operation model rather than asking users to regenerate the project.

## When it breaks

Untrusted template parameters reach shell commands, secrets appear in logs, retries duplicate resources, and success is reported before asynchronous dependencies converge. Workflow engines retain privileged credentials or operation history forever. Observe stuck-operation age, retries by error class, duplicate external IDs, redaction tests, and manual repair.

## Practice

**Observe:** inspect one generator and label every emitted file by long-term owner and upgrade mechanism. Completion means copied behavior without an upgrade path is identified.

**Build:** design a resumable create-service workflow with intent, authorization, operation schema, step keys, identities, outputs, retry classes, reconciliation, and cleanup.

**Break:** inject a timeout after repository creation and a permanent denial during database creation. Demonstrate distinct status, safe retry, and an operator repair path.

**Say it out loud:** explain why “the workflow failed” is not a sufficient user-facing condition.

## Check yourself

1. Which generated files should a platform be allowed to overwrite?
2. What state must survive a workflow worker restart?
3. When is compensation unsafe or impossible?
4. How does delegated identity constrain workflow blast radius?

## Sources

### REQUIRED

- [Backstage Software Templates](https://backstage.io/docs/features/software-templates/)

### RECOMMENDED

- [CNCF Platforms whitepaper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

### DEEP DIVE

- [Temporal durable execution](https://docs.temporal.io/temporal)

## Next

Continue to [Golden paths and developer experience](03-golden-paths-and-experience.md).
