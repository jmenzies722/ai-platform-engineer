# Queries and Indexes

A query states the result; the optimizer chooses an execution plan using available access paths and estimates.

## Why it matters

Adding an index to cure one slow query can double write work, consume cache, and still be ignored because the predicate does not match its leading keys. The decision should come from the observed plan, selectivity, workload frequency, and acceptable maintenance cost. SQL text states a result, not how the database will obtain it.

## How it works

A scan examines candidate rows. A B-tree index keeps keys ordered and points toward rows, making selective equality and range lookups cheaper while adding write and storage cost. Composite index usefulness depends on key order and predicates. `EXPLAIN` reveals the chosen plan.

A planner transforms a declarative query into candidate physical plans and estimates row counts and costs using statistics. A table scan reads qualifying rows from the table representation. A B-tree index stores ordered keys and row locators, supporting equality, prefix, and range access according to key order. Composite indexes are most useful when predicates and ordering align with leading columns; included data may enable an index-only plan if visibility rules permit. Joins can use nested-loop, hash, or merge strategies depending on cardinality and ordering. Every index consumes storage and must be updated transactionally on writes. `EXPLAIN` exposes the selected plan, while an execution form such as `EXPLAIN ANALYZE` actually runs the query and should be used with production caution.

## See it yourself

Predict that the first plan reports a scan and that creating `event_kind` permits an indexed search. Since half the rows share each value, also predict that this tiny data set may not run faster.

```bash
python3 - <<'PY2'
import sqlite3
db=sqlite3.connect(':memory:'); db.execute('CREATE TABLE event(id INTEGER, kind TEXT)')
db.executemany('INSERT INTO event VALUES (?,?)', ((i,'odd' if i%2 else 'even') for i in range(1000)))
print(db.execute('EXPLAIN QUERY PLAN SELECT * FROM event WHERE kind=?',('odd',)).fetchall())
db.execute('CREATE INDEX event_kind ON event(kind)')
print(db.execute('EXPLAIN QUERY PLAN SELECT * FROM event WHERE kind=?',('odd',)).fetchall())
PY2
```

Expected observation: The plan can change from a table scan to indexed search; this small data set does not prove lower elapsed time.

Limits of the queries and indexes observation: The plan output does not guarantee wall-clock improvement, represent a larger production distribution, or show write overhead. SQLite’s planner terminology is not a portable plan contract.

## Where it shows up

A multi-tenant audit API often filters by tenant and time and orders newest first. An index on `(tenant_id, occurred_at)` can restrict one tenant and walk the desired range, whereas separate single-column indexes may force extra work. Before adding it, engineers inspect real predicates, row distribution, plans, read frequency, ingest rate, and existing overlapping indexes. The result is a workload decision rather than an index checklist.

## When it breaks

A sequential scan on a selective query suggests a missing or unusable index, stale statistics, type mismatch, function-wrapped column, or cost estimate; a correct index with slow latency may be blocked, uncached, or returning too many rows. First capture the exact parameterized query, plan with estimated and actual rows in a safe environment, table/index definitions, and statistics freshness. Large estimate errors direct investigation differently from a sound plan waiting on I/O.

## Practice

**Build:** generate at least 10,000 skewed rows and compare plans for tenant-time queries before and after a composite index. **Break:** reverse key order and wrap an indexed column in an expression, observing plan changes. **Explain back:** connect predicate, selectivity, key order, estimated rows, and maintenance cost. Success includes equal result sets, recorded plans, repeated timings, and measured insert cost rather than a blanket “index fixed it.”

## Check yourself

1. Why can an index make writes slower?
2. Why is plan evidence stronger than guessing from SQL text?

## Sources

### REQUIRED

- [SQLite query planner](https://www.sqlite.org/queryplanner.html)

### RECOMMENDED

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)

### DEEP DIVE

- [Database System Concepts](https://www.db-book.com/)

## Next

Continue to [Transactions and Concurrency](./03-transactions-and-concurrency.md).
