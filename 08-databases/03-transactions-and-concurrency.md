# Transactions and Concurrency

Transactions group changes into an atomic unit while isolation defines which concurrent effects are visible.

## Why it matters

A payment client that times out after commit cannot safely infer that the transaction failed. Repeating the transfer may duplicate an effect even though each individual transaction is atomic. Transaction design must pair database guarantees with retry and idempotency behavior at the application boundary.

## How it works

A transaction begins, reads or writes, then commits or rolls back. Atomicity prevents partial committed units; durability concerns committed data surviving failure. Isolation levels permit or prevent phenomena such as dirty reads, nonrepeatable reads, and phantoms. Locking and multiversion concurrency control are implementation strategies.

A transaction groups operations between begin and commit or rollback. Atomicity means no partial transaction becomes committed; consistency depends on constraints and correct transaction logic; isolation controls interactions among concurrent transactions; durability describes survival of committed state under the database’s failure model. Locking can block conflicting access, while multiversion concurrency control lets readers observe selected snapshots and retains old versions as needed. Isolation levels permit different anomalies, and product implementations must be read precisely rather than inferred from names alone. Deadlock detection aborts a participant so progress can resume, making transaction retries an expected control path. External effects such as email or remote payment calls are not automatically rolled back with database rows.

## See it yourself

Predict that both balance updates appear after the context commits and the total remains 100. Add a raised exception between updates and expect the context manager to roll back both changes.

```bash
python3 - <<'PY2'
import sqlite3
db=sqlite3.connect(':memory:'); db.execute('CREATE TABLE account(id INTEGER PRIMARY KEY, balance INTEGER CHECK(balance>=0))'); db.executemany('INSERT INTO account VALUES (?,?)', [(1,100),(2,0)])
with db:
    db.execute('UPDATE account SET balance=balance-30 WHERE id=1')
    db.execute('UPDATE account SET balance=balance+30 WHERE id=2')
print(db.execute('SELECT * FROM account').fetchall())
PY2
```

Expected observation: Both updates commit together and the check constraint guards nonnegative balances.

Limits of the transactions and concurrency observation: The single-connection example does not exercise concurrent anomalies, crash recovery, or coordination with external systems. It illustrates atomic grouping and a row constraint in one SQLite process.

## Where it shows up

An order service often writes an order and an outbox event in one local transaction. A separate publisher delivers the event and marks it sent, accepting possible repeat delivery while consumers deduplicate by event identity. This avoids pretending a database transaction also controls a message broker. Isolation still matters when two requests reserve the same stock, and retries must re-evaluate transactional conditions.

Operators also need the age of unpublished outbox rows, because atomic storage is useful only if delivery eventually resumes and lag remains bounded.

## When it breaks

Deadlock errors identify aborted concurrency, lock waits produce growing latency, serialization failures indicate a conflicting schedule, and invariant violations after retries suggest logic outside the atomic boundary. First capture transaction boundaries, isolation level, query order, lock or wait information, and exact database error. Keep the reproduction small and use two controlled sessions; increasing timeouts only prolongs a deadlock or contention problem.

## Practice

**Build:** implement a transfer that preserves nonnegative balances and total funds, then inject failure between debit and credit. **Break:** use two connections to update rows in competing order under bounded timeouts and handle the database’s outcome. **Explain back:** separate atomicity, isolation, durability, idempotency, and external effects. Success requires invariant checks after normal execution, rollback, and retry, with no duplicate logical transfer.

## Check yourself

1. Does atomicity imply isolation?
2. Why must an application handle transaction aborts?

## Sources

### REQUIRED

- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)

### RECOMMENDED

- [SQLite transactions](https://www.sqlite.org/lang_transaction.html)

### DEEP DIVE

- [A Critique of ANSI SQL Isolation Levels](https://www.microsoft.com/en-us/research/publication/a-critique-of-ansi-sql-isolation-levels/)

## Next

Continue to [Backend Engineering](../09-backend-engineering/README.md).
