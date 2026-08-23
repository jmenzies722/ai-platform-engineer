# Caching and derived state

A cache is a deliberately stale, lossy copy with a safety policy; it is not a transparent speed button.

## Why it matters

Caching moves latency and cost, but it also creates invalidation, stampede, privacy, and correctness paths that can be more dangerous than the original read.

## How it works

First decide whether the value is safe to reuse, for whom, and for how long. A cache key must include every input that can change meaning: tenant, principal or authorization class, locale, model version, prompt version, and relevant source version. A time-to-live bounds residence, not necessarily staleness, because a stale value can be refreshed just before underlying data changes.

Cache-aside lets the application read and populate; read-through delegates loading; write-through updates cache with the store; write-behind trades durability and ordering for latency. Versioned keys avoid ambiguous invalidation when immutable outputs can be addressed by source version. Event invalidation reduces stale windows but introduces delivery and repair requirements.

Protect cold and hot paths. Request coalescing allows one loader per key. Jittered expiry prevents synchronized refresh. Negative caching can shield missing-key storms but must not preserve a temporary authorization or creation outcome too long. Admission, size limits, and eviction policy protect memory from scan pollution and oversized objects.

## See it yourself

One million entries expire exactly at noon and each miss triggers a database read. The cache transformed one maintenance event into a database outage. Add expiry jitter and single-flight loading, then measure origin concurrency. The desired observation is distributed refresh work and one origin request per hot key, not merely a recovered hit rate.

## Where it shows up

Semantic caches for model outputs are especially risky. “Similar” prompts may differ in tenant, policy, source freshness, or required citations. Safe reuse requires a narrow equivalence rule, provenance, isolation, expiry, and evaluation of false matches. Exact caching of immutable embedding inputs is often easier to defend.

## When it breaks

Common failures are incomplete keys, cache penetration, stampedes, stale authorization, unbounded values, and a cache becoming an undeclared authority. Diagnose with hit rate by result class, origin load, key cardinality, object size, age at serve, evictions, and coalescing effectiveness. Flush only when the origin can survive the cold start.

## Practice

**Build:** design caches for document metadata, authorization decisions, embeddings, and generated answers. For each, define key, value, ownership, TTL, invalidation, cold-start behavior, and unsafe staleness. **Break:** revoke access, rotate a model, and expire hot keys together. **Explain back:** justify which data you refused to cache.

## Check yourself

1. Why is TTL not a complete freshness guarantee?
2. Which dimensions belong in an authorization-sensitive key?
3. How does request coalescing change origin pressure?

## Sources

### REQUIRED

- [AWS Well-Architected: Caching best practices](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/selection-architecture.html)

### RECOMMENDED

- [Cloudflare: Cache concepts](https://developers.cloudflare.com/cache/concepts/)

### DEEP DIVE

- [Redis documentation: Key eviction](https://redis.io/docs/latest/develop/reference/eviction/)

## Next

Continue to [Queues, streams, and asynchronous work](07-queues-streams-and-asynchronous-work.md).
