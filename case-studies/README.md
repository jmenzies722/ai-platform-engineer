# Case Studies

These cases turn the curriculum's operating concepts into decisions made with incomplete evidence. Every organization, person, service, metric, and event in this directory is synthetic and composite. The cases are teaching material, not accounts of real companies.

## Cases

1. [The rollout that passed its first check](01-failed-kubernetes-rollout.md) asks you to contain a Kubernetes deployment failure without destroying evidence or making an irreversible production change.
2. [The efficient inference service nobody could wait for](02-inference-latency-and-cost.md) asks you to balance queueing, batching, admission, latency, fairness, and unit cost.
3. [The platform that shipped but did not land](03-platform-adoption.md) asks you to treat adoption as a product and governance problem, not a portal launch.

## How to use them

Read only through each evidence stage before recording:

- your current incident or product model;
- the strongest competing hypotheses;
- what the evidence proves and does not prove;
- the next discriminating test;
- the decision, owner, reversible step, and stop condition.

Then continue to the consequence and review. The point is not to guess the ending. It is to make a defensible decision at each boundary and explain how new evidence changes it.

## Curriculum map

- Kubernetes operations: [Kubernetes](../16-kubernetes/README.md), [local operations lab](../labs/10-kubernetes-operations/README.md), [bad rollout drill](../incidents/06-bad-rollout/README.md), and [Kubernetes platform project](../projects/06-kubernetes-platform/README.md)
- Model-serving economics: [Model Serving](../31-model-serving/README.md), [model-serving overload lab](../labs/17-model-serving-overload/README.md), [inference latency drill](../incidents/10-inference-latency/README.md), and [model-serving system project](../projects/12-model-serving-system/README.md)
- Platform product practice: [Platform Engineering](../21-platform-engineering/README.md), [Developer Platforms](../22-developer-platforms/README.md), [control-plane lab](../labs/14-platform-control-plane/README.md), and [developer platform project](../projects/09-developer-platform-control-plane/README.md)
