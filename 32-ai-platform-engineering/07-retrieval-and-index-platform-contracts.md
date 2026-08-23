# Retrieval and index platform contracts

A retrieval platform turns governed source corpora into versioned, tenant-scoped indexes whose authorization, freshness, and rollback behavior are explicit.

## Why it matters

Retrieval adds mutable state between source data and generation. If a service searches a global index and filters afterward, unauthorized content may already influence ranking, caches, logs, or model context. If corpus and embedding versions are hidden, an answer cannot be reproduced and a bad reindex cannot be reversed. Indexing success is therefore a release claim, not merely a completed batch job.

## How it works

A `CorpusVersion` binds tenant namespace, source snapshot or manifests, parser and chunker digests, embedding model and dimensions, metadata schema, policy version, and deletion watermark. An `IndexVersion` binds that corpus to engine configuration, shard layout, build run, checksums, quality evidence, creation time, and lifecycle state. Queries resolve an immutable active index version at request start and record it in traces and citations.

Authorization happens before retrieval. The authenticated principal and purpose resolve allowed tenant namespaces and document ACL predicates before candidate generation. The engine searches only authorized partitions or applies a native pre-filter guaranteed by the adapter. Post-filtering is not equivalent: unauthorized candidates can displace allowed results, leak through scores, and contaminate caches. Caches include tenant, authorization-set fingerprint, policy, corpus, index, and model versions, plus normalized-input hash.

Indexing is a reconciliation workflow. A controller snapshots sources, parses and chunks deterministically, embeds idempotently, writes a shadow index, validates counts and checksums, and runs retrieval and ACL tests. Publication atomically changes an active-version pointer; pinned readers may finish on the previous version. In-place mutation creates partial states that rollback cannot identify.

Freshness measures source watermark lag, ingestion queue age, indexed-document lag, deletion propagation age, and active version. “Job completed recently” does not show every source was included. Define SLOs by corpus class: serve a named older version with a freshness signal, fail closed for revoked documents, or reject when policy requires current data.

Reindex when parser, chunking, embedding, schema, engine, or policy semantics change. Dual-read a bounded query set, compare relevance and ACL decisions, canary tenants, then promote. Retain the previous compatible index and source snapshot for rollback. Rollback moves the pointer and purges version-sensitive caches; it cannot restore deleted source data or make an old index acceptable if its ACL policy is now invalid.

## See it yourself

Create two synthetic tenants, each with document ID `shared-name`, and a query whose text matches both. A global top-one search followed by tenant filtering may return zero for tenant A because tenant B occupied the only candidate slot. Searching A's namespace returns A's document. This deterministically proves pre-filtering preserves both isolation and recall in this fixture; it does not prove the vector engine has no implementation side channel. Build index v2 with one intentionally omitted source, compare expected versus indexed manifest counts, and verify promotion fails while v1 remains active.

## Where it shows up

RAG gateways, search, semantic caches, and agent knowledge tools need this contract. A trace carries query ID, tenant, policy decision, corpus and index versions, retriever and reranker versions, document IDs, latency, and freshness without raw restricted chunks. Operators need build progress, source lag, denials, empty results, shard health, and rollback status.

## When it breaks

Common failures include global indexes with application post-filtering, stale ACL replicas, dimension mismatch, partial reindex, duplicate chunks, missed tombstones, cache keys without policy version, and promotion based only on aggregate recall. First preserve principal, authorization decision, resolved namespace, active pointer, source watermark, build manifest, adapter query, candidate counts, and cache decision. Stop promotion, fail closed for revocation uncertainty, compare the first divergent stage, and roll back only to a policy-compatible version. Reconcile deletions across active, shadow, replicas, and caches before closing an exposure.

## Practice

**Build:** define `CorpusVersion` and `IndexVersion`, pre-retrieval ACL enforcement, freshness indicators, shadow build, atomic promotion, cache keys, and rollback. **Break:** omit tenant scope, miss one source, change embedding dimensions, delay a tombstone, and promote a low-recall index. **Explain back:** show deterministic ACL and manifest tests, what they cannot prove, and the exact evidence required to reindex, promote, or roll back.

## Check yourself

1. Why is post-filtering not equivalent to authorization before retrieval?
2. Which identities make a retrieval result reproducible?
3. When is an older index unsafe as a rollback target?

## Sources

### REQUIRED

- [NIST SP 800-207, Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

### RECOMMENDED

- [Elasticsearch document-level security](https://www.elastic.co/guide/en/elasticsearch/reference/current/document-level-security.html)
- [OpenSearch index aliases](https://docs.opensearch.org/latest/im-plugin/index-alias/)

### DEEP DIVE

- [FAISS: similarity search and clustering of dense vectors](https://github.com/facebookresearch/faiss/wiki)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

## Next

Continue to [Evaluation, lineage, and release governance](08-evaluation-lineage-and-release-governance.md).
