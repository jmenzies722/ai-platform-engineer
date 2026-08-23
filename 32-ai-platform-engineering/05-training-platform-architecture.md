# Training platform architecture

A training platform converts declared experiment intent into reproducible, schedulable, observable, and recoverable runs.

## Why it matters

Notebook success does not establish artifact lineage, resource fairness, resumability, or production suitability.

## How it works

A versioned run contract names code digest, environment, data manifests, hyperparameters, seed, resource shape, distribution strategy, owner, budget, checkpoint policy, and expected outputs. Admission applies policy and quota; a scheduler places the gang; a controller reconciles workers, progress, checkpoint, and termination.

The platform records resolved rather than merely requested state. Artifacts publish atomically with lineage and evaluation status. Retries distinguish transient infrastructure from deterministic code or data failure. Escape hatches transfer named support and compliance responsibilities.

## See it yourself

Two runs share a Git commit but use an unpinned base image. A library update changes kernels and outputs. Binding an image digest removes that variation. Exact reproduction still depends on data, hardware, seeds, and nondeterministic operations, so the contract records all of them.

## Where it shows up

Self-service APIs produce launcher configuration, workload identity, telemetry, and artifact registration. Users see run state and failure evidence without learning every scheduler primitive.

## When it breaks

Controllers retry deterministic failures, checkpoints omit sampler state, logs leak examples, quotas ignore storage, and artifact publication races job termination. Preserve attempt-level lineage and classify the first failing event. Never mark success until declared artifacts validate.

## Practice

**Observe:** compare requested and resolved run manifests. **Build:** design state transitions from admission through artifact publication. **Break:** inject a partial checkpoint and deterministic bad sample. Completion requires bounded retries and a reproducible failure report.

## Check yourself

1. Why record resolved environment identity?
2. Which failures merit a fresh node?
3. What makes an artifact publication atomic?

## Sources

### REQUIRED

- [Kubeflow Training Operator](https://www.kubeflow.org/docs/components/trainer/)

### RECOMMENDED

- [MLflow tracking concepts](https://mlflow.org/docs/latest/ml/tracking/)

### DEEP DIVE

- [PyTorch distributed checkpoint](https://docs.pytorch.org/docs/stable/distributed.checkpoint.html)

## Next

Continue to [Serving platform architecture](06-serving-platform-architecture.md).
