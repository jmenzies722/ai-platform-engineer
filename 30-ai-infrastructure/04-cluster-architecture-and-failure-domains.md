# Cluster architecture and failure domains

An accelerator cluster is a hierarchy of compute, links, storage paths, control services, and failure domains designed around workload communication.

## Why it matters

Buying enough accelerators does not produce a usable cluster. A failed switch, oversubscribed rack, incompatible driver, or saturated control plane can idle an entire training gang.

## How it works

Nodes combine accelerators, CPUs, memory, local storage, and network interfaces. Fast intra-node fabric carries chatty model-parallel traffic; the scale-out network carries collectives and data; a separate management path limits correlated disruption. Racks, power feeds, switches, zones, and software pools are explicit failure domains.

Provisioning establishes firmware, driver, runtime, fabric, health tests, labels, and attestation before inventory becomes schedulable. Controllers reconcile desired capacity while admission checks compatibility and topology. A capacity unit is therefore a schedulable shape, such as eight healthy connected GPUs, not a scalar GPU count.

## See it yourself

Four racks each contain 32 GPUs. Losing one rack leaves 96 GPUs, apparently enough for a 64-GPU job. If policy requires the job within two adjacent 32-GPU fabric islands and the remaining islands lack a direct non-oversubscribed path, it is not schedulable. This proves aggregate inventory is weaker than topology-qualified capacity.

## Where it shows up

Cluster blueprints map training parallel groups, checkpoint traffic, and serving replicas onto physical domains. Health gates run device diagnostics and link tests; repair drains the smallest safe domain. Canary pools validate firmware before broad rollout.

## When it breaks

Correlated firmware rollout can remove every pool. Partial network failure creates stragglers rather than clean faults. Control-plane dependency on the workload fabric blocks recovery. Compare desired and admitted inventory, domain-aware placement, link telemetry, node diagnostics, and controller reconciliation. Test domain loss rather than only process loss.

## Practice

**Observe:** map every shared component for a 64-GPU job. **Build:** define health states and admission gates. **Break:** remove one rack, one top-of-rack switch, and the provisioning service separately. Completion requires predicted blast radius, surviving control path, and a placement decision for each event.

## Check yourself

1. Why is a GPU count not a capacity promise?
2. Which services must survive workload-fabric failure?
3. How can degraded links mimic healthy nodes?

## Sources

### REQUIRED

- [NVIDIA DGX SuperPOD reference architecture](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/)

### RECOMMENDED

- [Kubernetes node status](https://kubernetes.io/docs/reference/node/node-status/)

### DEEP DIVE

- [Google cluster management at Borg scale](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/)

## Next

Continue to [Distributed training systems](05-distributed-training-systems.md).
