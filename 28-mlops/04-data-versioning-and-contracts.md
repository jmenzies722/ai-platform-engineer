# Data versioning and contracts

Reproducible ML needs immutable data identity plus executable contracts for meaning, timing, ownership, and permitted use.

## Why it matters

[Release and monitoring](03-release-and-monitoring.md) operates a model, but no model can be reproduced or governed if “the training data” means a mutable table queried later.

## How it works

A dataset version references immutable object digests, schema, extraction query and time, source snapshots, partition manifest, label policy, exclusions, and access policy. Content addressing proves byte identity; a manifest preserves logical ordering and metadata. Version code and configuration separately because identical data under changed feature logic is a different training input.

Contracts validate field names, types, units, ranges, null behavior, keys, event time, freshness, and semantic expectations. Statistical checks compare distributions but should alert rather than silently redefine the contract. Point-in-time joins and label maturation are first-class metadata.

Lineage is a directed graph from source through snapshot, features, training run, evaluation, model, and deployment. Each edge records the transformation identity. Deletion and consent changes require derived-artifact impact analysis, not just removing one source row.

## See it yourself

Hash three files into a sorted manifest, then hash the manifest. Change one byte in one file: its digest and dataset digest change. Rename without changing the logical manifest policy and decide whether identity should change; document that rule.

This proves content identity detects mutation. It does not prove the data is lawful, representative, or correctly labeled.

## Where it shows up

A risk model release can answer which source snapshot, customers, label window, transform, and policy produced each artifact. Access to raw records is narrower than access to aggregate metrics, and retention jobs traverse lineage.

## When it breaks

Mutable partitions are overwritten, late events alter old snapshots, schema-compatible fields change units, and credentials or private rows enter manifests. Floating “latest” references make rollback non-reproducible.

On mismatch, compare manifests, object digests, row counts, event-time ranges, and contract reports. Treat semantic unit changes as breaking even when physical types match.

## Practice

**Observe:** distinguish content, schema, and semantic identity. **Build:** create a manifest and contract for five files. **Break:** change a unit from dollars to cents without changing type and write a semantic test.

## Check yourself

1. Why is a query string insufficient dataset identity?
2. What does a content digest prove?
3. How should late data affect snapshots?
4. Why must deletion traverse lineage?

## Sources

### REQUIRED

- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010)

### RECOMMENDED

- [DVC data versioning](https://dvc.org/doc/user-guide/data-management/data-versioning)

### DEEP DIVE

- [W3C PROV overview](https://www.w3.org/TR/prov-overview/)

## Next

Continue to [Pipeline testing and reproducibility](05-pipeline-testing-and-reproducibility.md).
