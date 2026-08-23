# Data and feature platform contracts

An AI data platform makes datasets and features discoverable, reproducible, policy-aware, and safe to consume through versioned contracts.

## Why it matters

Training from mutable paths or undocumented joins makes results irreproducible and can leak restricted data into artifacts that are hard to recall. A checksum alone identifies bytes; it does not establish schema meaning, legal purpose, temporal correctness, quality, or authorization. The platform contract must bind those claims so consumers and operators can locate, compare, quarantine, and delete derived artifacts.

## How it works

A dataset version binds a stable ID to schema, immutable snapshot or manifest, producer, source lineage, collection and license terms, allowed purpose, classification, retention, quality results, and policy version. A manifest lists checksummed shards and canonical ordering; publication is atomic only when every referenced object exists and the metadata pointer becomes visible in one committed transition. Bad versions are quarantined and superseded, never silently overwritten.

Compatibility is consumer-specific. Adding a nullable column may be structurally backward compatible while changing a category's meaning is not. Producers run schema, range, uniqueness, null, distribution, and referential checks before publication; consumers may impose stricter acceptance. The catalog separates control metadata from bulk bytes, resolves logical references to immutable versions at admission, issues purpose- and version-scoped workload credentials, and records actual consumption in lineage.

Feature contracts additionally define entity key, value type, transformation digest, event time, creation time, time-to-live, freshness SLO, null and default behavior, and offline-online consistency tolerance. Point-in-time joins must select only values whose event time was available at the prediction or label cutoff. This prevents a future event from leaking into training. Online stores report feature age and fallback use, since returning a syntactically valid stale value can be more dangerous than a visible miss.

Deletion and revocation are graph operations. Source records map to manifests, derived datasets, runs, checkpoints, evaluations, and deployments. Policy determines whether an affected model must be retrained, recalled, access-restricted, or documented; machine unlearning is not assumed. Keep tombstones and audit evidence while deleting prohibited payloads. The graph bounds affected artifacts, but incomplete lineage means the platform cannot prove complete remediation.

## See it yourself

Run a job twice against `data/latest`, append one synthetic record between resolutions, and compare the resolved manifests. Different digests prove the jobs consumed different declared byte sets. Pin one manifest and verify each shard checksum; equal digests then prove the referenced bytes are stable under the hash assumptions. They do not prove deterministic parsing, transforms, training, or storage durability. Next, create an entity feature at event time 12:00 and a prediction cutoff at 11:00; a point-in-time join returning that feature is a deterministic leakage failure.

## Where it shows up

A training request names logical datasets, but admission resolves approved versions, verifies policy and compatibility, and records manifests in the run specification before workers start. A feature platform uses the same transformation definition for batch materialization and online publication, then compares sampled values across both paths. Catalog search can expose descriptions broadly while data access remains separately authorized; discoverability must not imply permission.

## When it breaks

Backfills use processing time as event time, labels reveal future outcomes, schema changes silently coerce values, duplicate entities multiply rows, online caches outlive revocation, and quality logs contain sensitive fields. Preserve the run's resolved manifest, schema and quality decisions, transformation digest, event and ingestion timestamps, principal, policy version, and derived lineage. Find the first divergent version rather than comparing only final metrics. Stop new consumption, quarantine the version, enumerate affected descendants, and test revocation at caches and replicas before declaring containment.

## Practice

**Observe:** trace one synthetic field from source through transformation, checkpoint, and deployment. **Build:** define dataset and feature contracts, immutable manifest verification, point-in-time join, compatibility tests, and lineage edges. **Break:** mutate `latest`, introduce a future-derived label, publish a partial manifest, and revoke one source record. Completion requires deterministic detection, quarantine, and an evidence-backed list of affected artifacts and unknown lineage gaps.

## Check yourself

1. What does a manifest digest prove?
2. Why does feature freshness belong in the contract?
3. How can deletion propagate to trained artifacts?

## Sources

### REQUIRED

- [NIST AI RMF data guidance](https://airc.nist.gov/AI_RMF_Knowledge_Base/AI_RMF/)
- [Datasheets for Datasets](https://doi.org/10.1145/3458723)

### RECOMMENDED

- [Apache Iceberg specification](https://iceberg.apache.org/spec/)

### DEEP DIVE

- [Feast architecture](https://docs.feast.dev/getting-started/architecture-and-components)

## Next

Continue to [Training platform architecture](05-training-platform-architecture.md).
