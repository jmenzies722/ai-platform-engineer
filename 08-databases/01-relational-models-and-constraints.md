# Relational Models and Constraints

A relational database protects shared facts by giving data a schema and enforcing invariants near the data.

## Why it matters

If two application instances both check that an email is unused and then insert it, only a database uniqueness rule closes the race at the shared state boundary. Choosing which invariants belong in schema constraints determines whether every writer preserves the same facts. Application validation remains useful for messages, but it cannot substitute for authoritative enforcement.

## How it works

Tables represent relations over named attributes. Primary keys identify rows; foreign keys express references; unique and check constraints reject invalid states. Normalization separates facts to reduce contradictory updates, while deliberate denormalization trades consistency work for read shape.

A relation is a set of tuples over named attributes, while SQL tables implement this model with type and nullability details. A primary key supplies stable row identity; unique constraints reject duplicate candidate values under database-specific null rules. Foreign keys require referenced identities and define update or deletion behavior. Check constraints reject rows that violate predicates visible to that row. Normalization separates facts according to dependencies so one fact has one update location, reducing insertion, update, and deletion anomalies. Joins reconstruct related views by keys. Transactions determine when groups of constraint-checked changes become visible. Constraints should encode durable truths, not temporary workflow preferences that require external context.

## See it yourself

Predict one row with generated ID and normalized stored email. Add a second insert with the same email and expect the database, not a preceding query, to reject it.

```bash
python3 - <<'PY2'
import sqlite3
db=sqlite3.connect(':memory:'); db.execute('PRAGMA foreign_keys=ON')
db.execute('CREATE TABLE user(id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL)')
db.execute('INSERT INTO user(email) VALUES (?)', ('a@example.com',))
print(db.execute('SELECT id,email FROM user').fetchall())
PY2
```

Expected observation: The schema, not only application code, guarantees a unique non-null email in this database.

Limits of the relational models and constraints observation: The in-memory SQLite run does not prove behavior for every SQL product, persistence after process failure, or concurrent race handling. Constraint syntax and null semantics must be checked against the chosen database.

## Where it shows up

Order processing benefits from placing product identity, order identity, and line-item relationships in constraints. A foreign key stops orphaned lines even when a repair script bypasses the API, while a check can reject negative quantity. Inventory availability, however, spans changing rows and concurrency, so it usually needs transactional logic rather than a static row check. Clear ownership of each invariant keeps the schema from becoming either empty or an accidental rule engine.

## When it breaks

Duplicate rows indicate missing or incorrectly scoped uniqueness; orphaned references suggest disabled or absent foreign keys; contradictory duplicated attributes point toward a normalization or ownership problem. First query the smallest violating rows and inspect the actual constraint definitions and migration state. Do not add a constraint until existing violations are understood and cleanup is planned, because deployment can otherwise lock or fail on production data.

## Practice

**Build:** model authors and books with keys, required attributes, and a defensible deletion policy. **Break:** attempt duplicate identity, null required data, orphan references, and a violated check, recording the exact database errors. **Explain back:** state which facts each table owns and why each invariant sits in schema or transaction logic. Success means invalid rows are rejected from every insertion path and valid joins return the expected cardinality.

## Check yourself

1. Which invariants belong in database constraints?
2. What anomaly can duplicated facts create?

## Sources

### REQUIRED

- [SQLite foreign keys](https://www.sqlite.org/foreignkeys.html)

### RECOMMENDED

- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)

### DEEP DIVE

- [An Introduction to Database Systems](https://www.oreilly.com/library/view/an-introduction-to/9780321197849/)

## Next

Continue to [Queries and Indexes](./02-queries-and-indexes.md).
