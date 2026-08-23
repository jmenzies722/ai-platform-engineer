# Redis, Caching, and Database Operations

A cache is a deliberately stale copy with a failure policy; Redis is a data system whose speed does not remove durability or capacity decisions.

## Why it matters

A cache miss storm can overload the database, a stale authorization entry can retain access, and an unbounded Redis keyspace can evict the very data expected to protect latency. The design must define source of truth, key ownership, freshness, invalidation, miss behavior, memory bounds, and what happens when the cache is unavailable.

## How it works

Cache-aside code reads the cache, loads from the source on miss, and writes a value with a TTL. On mutation it updates the source and invalidates or replaces affected keys. That gap permits races: an old miss can repopulate stale data after invalidation. Versioned keys, ordered events, compare-and-set logic, or accepting a bounded stale interval may be appropriate depending on the invariant.

Read-through and write-through move policies behind a cache interface; write-behind acknowledges before durable storage and therefore changes the data-loss contract. A TTL bounds reuse after insertion but does not guarantee freshness until expiry. Randomized expiry spreads load. Request coalescing lets one loader fill a hot missing key; stale-while-revalidate can serve an older value while one refresh runs. Negative caching protects repeated misses but can hide newly created data.

Redis executes ordinary commands serially in its main command-processing path, while persistence and I/O details vary by configuration and version. Pipelines reduce round trips without making a group atomic. Transactions queue commands and execute them without interleaving, but rollback semantics differ from relational databases. Lua scripts and functions can make bounded server-side operations atomic, yet long work blocks other commands. RDB snapshots and AOF persistence trade recovery time, write cost, and potential loss. Replication and Sentinel or Cluster improve availability but do not turn asynchronous failover into zero-loss durability.

Database operations connect these choices to capacity. Bound connection pools, watch saturation and queueing, test schema migrations on realistic distributions, keep expand-and-contract compatibility during rolling deploys, and restore backups regularly. A backup file is evidence of an attempted backup; a validated restore is evidence of recoverability.

## See it yourself

Predict one loader call, two equal values before expiry, and a second loader call after expiry.

```bash
python3 - <<'PY'
import time
cache = {}
loads = 0
def get(key):
    global loads
    value = cache.get(key)
    if value and value[1] > time.monotonic():
        return value[0]
    loads += 1
    cache[key] = (f"value-{loads}", time.monotonic() + 0.05)
    return cache[key][0]
print(get("hot"), get("hot"), "loads", loads)
time.sleep(0.06)
print(get("hot"), "loads", loads)
PY
```

Expected observation: TTL permits reuse until local monotonic expiry, then causes another load.

Limits of the observation: this single-process dictionary has no concurrent stampede, eviction, network, invalidation race, persistence, or clock disagreement. It demonstrates expiry mechanics only.

## Where it shows up

A product catalog can tolerate a minute of stale descriptions but not stale price during checkout. Browsing may use a versioned cache with stale-while-revalidate; checkout reads authoritative price inside its transaction. This is not inconsistent engineering. It assigns different freshness contracts to different decisions.

## When it breaks

A falling hit ratio with rising database load suggests churn, eviction, or bad keys; synchronized expirations produce periodic latency spikes; Redis `used_memory` near a cap plus evictions reveals pressure; blocked clients and high command latency point to expensive commands or server stalls. First capture hit and miss rates by use case, key cardinality, TTL distribution, eviction policy, hot keys, command latency, persistence health, pool queueing, and source load. Do not run `KEYS *` on a large production instance or flush a cache during overload.

## Practice

**Build:** add cache-aside behavior with bounded TTL, randomized expiry, metrics, and request coalescing to a read model. **Break:** expire a hot key under concurrent load, make the cache unavailable, and mutate source data during a refill. **Explain back:** identify stale windows and source protection in every case. Success includes bounded source concurrency, a bypass or fail-closed decision per datum, and a restore drill for the authoritative store.

## Check yourself

1. Why does TTL not solve cache invalidation races?
2. When should a cache outage fail closed instead of falling back to the database?

## Sources

### REQUIRED

- [Redis Client-Side Caching](https://redis.io/docs/latest/develop/reference/client-side-caching/)
- [Redis Persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/)

### RECOMMENDED

- [Redis Eviction Policies](https://redis.io/docs/latest/develop/reference/eviction/)
- [PostgreSQL Backup and Restore](https://www.postgresql.org/docs/current/backup.html)

### DEEP DIVE

- [Caching at Netflix](https://netflixtechblog.com/caching-for-a-global-netflix-7bcc457012f1)

## Next

Continue to [Backend Engineering](../09-backend-engineering/README.md).
