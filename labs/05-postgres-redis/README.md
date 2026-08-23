# Lab: Observe PostgreSQL Transactions and Redis Expiration

Compare durable relational transaction behavior with an in-memory key expiration mechanism using disposable local containers.

## Prerequisites

- Docker Engine with permission to run containers
- `docker compose` v2
- Ports 55432 and 56379 unused
- About 500 MiB free disk space

## Safety

Use the fixed lab names and non-default host ports. The databases contain generated data only. Do not point any command at an existing database, shared Docker context, or production credentials. Images are unpinned for readability; record exact image digests in evidence and pin them when repeating results.

## Setup and baseline

```bash
mkdir -p .work
cat >.work/compose.yaml <<'YAML'
services:
  postgres:
    image: postgres:17
    environment:
      POSTGRES_PASSWORD: lab-only
    ports: ["127.0.0.1:55432:5432"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 2s
      timeout: 2s
      retries: 15
  redis:
    image: redis:8
    ports: ["127.0.0.1:56379:6379"]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 2s
      timeout: 2s
      retries: 15
YAML
docker compose -f .work/compose.yaml up -d
docker compose -f .work/compose.yaml ps
```

Wait for both services to become healthy. Predict what another PostgreSQL session sees before commit and what Redis returns after a TTL expires.

## Tasks

1. Create a PostgreSQL table:

   ```bash
   docker compose -f .work/compose.yaml exec -T postgres psql -U postgres <<'SQL'
   CREATE TABLE accounts(id integer PRIMARY KEY, balance integer CHECK(balance >= 0));
   INSERT INTO accounts VALUES (1, 100), (2, 100);
   SQL
   ```

2. Open two `psql` sessions. In session A, begin a transaction and update account 1 without committing. In session B, read the row, inspect `pg_stat_activity`, then attempt the same update with `SET lock_timeout='2s'`. Capture visibility and lock-wait evidence.
3. Commit A and retry B. Prove the invariant `sum(balance)=200` after a transfer.
4. Exercise Redis expiration:

   ```bash
   docker compose -f .work/compose.yaml exec -T redis redis-cli SET session:lab active EX 5
   docker compose -f .work/compose.yaml exec -T redis redis-cli TTL session:lab
   sleep 6
   docker compose -f .work/compose.yaml exec -T redis redis-cli GET session:lab
   ```

5. Compare a database transaction guarantee with Redis key expiration. Do not infer durability merely because a key survived one process check.

## Evidence to keep

Keep image digests, health output, SQL transcript, transaction IDs from `txid_current()`, `pg_stat_activity` wait fields, timeout error, invariant query, Redis TTL samples, and an explanation of visibility versus durability.

## Failure injection

Hold a row lock in session A and force session B's two-second lock timeout. This is one bounded contention fault. Diagnose the blocking PID using `pg_blocking_pids(pid)` before rolling back A. Separately, expiration is an expected behavior experiment, not a service failure.

## Cleanup

```bash
docker compose -f .work/compose.yaml down --volumes --remove-orphans
docker ps -a --filter label=com.docker.compose.project --format '{{.Names}}'
rm -rf .work
```

Confirm no lab containers or volumes remain.

## Rubric

- 2 points: establishes healthy isolated services and records versions
- 3 points: proves transaction visibility, blocking, and recovery
- 2 points: measures Redis TTL behavior without claiming stronger guarantees
- 2 points: distinguishes consistency, isolation, and durability
- 1 point: removes containers, networks, volumes, and artifacts

## Sources

- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL lock monitoring](https://www.postgresql.org/docs/current/monitoring-locks.html)
- [Redis `EXPIRE`](https://redis.io/docs/latest/commands/expire/)
