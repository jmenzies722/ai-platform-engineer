# Lab: Measure a Database, Then Break It Safely

Build a disposable database experiment whose notebook separates schema guarantees, plan choices, transaction outcomes, contention, and cache freshness.

## Safety and setup

Use Python 3 and its standard-library SQLite driver. The lab writes only `/tmp/database-lab.db`; remove any previous file before starting and delete it at the end. SQLite is not PostgreSQL, so label every engine-specific observation.

```bash
rm -f /tmp/database-lab.db
python3 - <<'PY'
import sqlite3
db = sqlite3.connect("/tmp/database-lab.db")
db.executescript("""
PRAGMA journal_mode=WAL;
CREATE TABLE customer(id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE);
CREATE TABLE orders(
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customer(id),
  state TEXT NOT NULL CHECK(state IN ('open','paid')),
  total_cents INTEGER NOT NULL CHECK(total_cents >= 0)
);
CREATE INDEX orders_customer_state ON orders(customer_id, state);
INSERT INTO customer VALUES (1, 'reader@example.com');
INSERT INTO orders VALUES (1, 1, 'open', 2500);
""")
db.commit()
print(db.execute(
  "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id=? AND state=?",
  (1, "open")).fetchall())
db.close()
PY
```

Before running it, predict which constraints reject bad rows and whether the composite index can satisfy both predicates. Save the actual plan. A plan naming the index is evidence for this query and dataset, not proof that every production distribution should use it.

## Transaction and contention experiment

Write a script with two connections and bounded timeouts. Connection A begins a write transaction and updates order 1 without committing. Connection B attempts to update the same row. Record the exact exception and elapsed time, then roll back A and prove B can proceed. Repeat with A committed. Never leave the transaction open after the script exits.

Then test atomicity: inside one transaction, change the order to `paid` and insert a deliberately invalid negative total. Catch the exception, roll back, and query the original state. Explain why the check constraint and transaction establish different guarantees.

## Cache experiment

Add a small in-process cache keyed by order ID with an expiry timestamp. Count source loads. Exercise:

1. two reads before expiry;
2. a database update without invalidation;
3. a read before expiry and a read after expiry;
4. invalidation followed by a refill.

For each, predict value, freshness, and source-load count. This cache has no distributed invalidation, eviction, persistence, or concurrent stampede; say so in the notebook.

## Optional PostgreSQL extension

Only on a disposable instance you own, repeat the plan with `EXPLAIN (ANALYZE, BUFFERS)`, inspect `pg_stat_activity` during a lock wait, and create enough updates to observe dead tuples before and after vacuum. Do not run exploratory `ANALYZE` on writes or force `VACUUM FULL`.

## Deliverable

Produce one concise report with:

- schema invariants and the layer enforcing each one;
- query, plan, parameters, data size, and the plan’s limits;
- transaction timeline and lock outcome;
- cache freshness table and failure policy;
- one PostgreSQL behavior that SQLite cannot demonstrate; and
- commands and evidence showing cleanup.

## Cleanup

Close every connection and remove the file:

```bash
rm -f /tmp/database-lab.db /tmp/database-lab.db-shm /tmp/database-lab.db-wal
```

Success means the report can distinguish measured behavior from inference, and rerunning the lab starts from a clean state.
