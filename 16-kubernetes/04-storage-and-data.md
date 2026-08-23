# Persistent storage and data workloads

Kubernetes can attach and mount storage for replaceable Pods, but durability, consistency, topology, backup, and application recovery still belong to the storage system and workload design.

## Why it matters

A PersistentVolumeClaim surviving a Pod does not guarantee it survives zone loss, concurrent writers, corruption, or cluster deletion. StatefulSet identity does not make a database replicated or consistent.

## How it works

A PersistentVolumeClaim requests capacity, access mode, volume mode, and optionally a StorageClass. Dynamic provisioning creates a PersistentVolume through a CSI driver. Binding connects claim to volume; the scheduler considers volume topology; attach and mount operations make storage available on the selected node. Reclaim policy determines whether storage is retained or deleted after release.

Access modes describe requested mount capabilities, not application-level concurrency safety. `ReadWriteOnce` is not necessarily single-Pod access; driver and topology semantics matter. StatefulSets give Pods stable ordinals and claim templates, while the application must implement replication, quorum, backup, restore, and schema compatibility.

Snapshots are point-in-time storage operations where supported. Application-consistent backup may require quiescing writes or database-native coordination. Test restores into an isolated namespace and verify logical data.

## See it yourself

In a disposable cluster, inspect `kubectl get pvc,pv,storageclass -o wide` and describe a bound claim. Predict selected zone, reclaim behavior, and what happens when its Pod is deleted. Deleting the Pod should preserve a retained claim, but this does not prove backup or zone-failure recovery.

## Where it shows up

A StatefulSet runs three database members with one claim each and topology spread. The database replicates records; CSI only supplies volumes. A scheduled backup records database checkpoint, snapshot identity, encryption key dependency, and restore test result.

## When it breaks

A claim remains Pending because no class matches or immediate binding selects an incompatible zone. Attach is blocked by stale node state or access constraints. A deleted claim triggers destructive reclaim. Node drain cannot move a zonal volume. Snapshot succeeds while buffered writes make restored data inconsistent. Finalizers delay deletion for safety.

Gather claim and volume events, StorageClass binding mode, CSI controller and node evidence, node topology, attachment objects, mount errors, capacity, and application replication status before force-detaching or deleting anything.

## Practice

**Observe:** trace one claim from StatefulSet template through PVC, PV, StorageClass, CSI driver, node, mount, reclaim policy, and backup owner.

**Build:** deploy a disposable stateful writer, prove data survives Pod replacement, snapshot or back it up using cluster-supported tooling, and restore to a new claim.

**Break safely:** request an unavailable class or incompatible topology. Completion means you diagnose Pending from events, repair without deleting good data, and validate restored logical content rather than claim status alone.

## Check yourself

1. Which component provides application replication?
2. Why can a bound claim still prevent rescheduling?
3. What does reclaim policy control?
4. Which evidence establishes an application-consistent restore?

## Sources

### REQUIRED

- [Kubernetes persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)

### RECOMMENDED

- [Kubernetes StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)

### DEEP DIVE

- [Container Storage Interface specification](https://github.com/container-storage-interface/spec)

## Next

[Identity, policy, and workload security](05-security-and-policy.md)
