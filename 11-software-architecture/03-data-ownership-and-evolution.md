# Data Ownership and Evolution

Systems evolve safely when one authority owns each invariant and contracts change compatibly across independent lifecycles.

## Why it matters

Renaming a required API field can break old consumers during a rolling deployment even when every new binary is correct in isolation. Safe evolution depends on who owns the invariant and how old and new representations overlap. A migration plan must preserve compatibility long enough to observe adoption and retain a rollback path.

## How it works

A component that owns data also owns rules for changing it. Other components use a contract rather than writing storage directly. Compatible evolution adds tolerable fields or behavior before removing old forms. Migrations often require expand, deploy, backfill, switch, and contract phases.

Data ownership means one authority defines allowed state transitions and enforces invariants, not merely that one team administers a database. Other components request changes through contracts or consume published facts rather than writing storage behind the owner. Compatibility has direction: a new reader may tolerate old records, an old reader may ignore an additive field, but changing meaning under the same field is dangerous. Expand-and-contract migration first adds a compatible representation, deploys code that can read both and writes the chosen transition form, backfills historical data idempotently, switches reads after evidence, and removes the old form only when no old participant remains. Events and caches complicate the window because old data can outlive deployment. Versioning is a coordination tool, not a substitute for semantic migration or consumer inventory.

## See it yourself

Predict that both old and expanded records produce a user with a timezone, with UTC serving as an explicit compatibility default. Ask whether that default is semantically valid before adopting the pattern.

```bash
python3 - <<'PY2'
def read_user(record):
    return {'name':record['name'], 'timezone':record.get('timezone','UTC')}
print(read_user({'name':'Ada'}))
print(read_user({'name':'Ada','timezone':'Europe/London'}))
PY2
```

Expected observation: The reader tolerates old and expanded records, allowing producers and consumers to move at different times.

Limits of the data ownership and evolution observation: The function does not migrate stored rows, coordinate writers, detect unknown fields, or prove that UTC is correct for every user. It demonstrates one backward-compatible reader only.

## Where it shows up

Splitting a customer module into a service exposes ownership decisions. If other services continue updating customer tables directly, the network API adds latency without creating an invariant boundary. Moving writes behind the owner, publishing change events, and measuring consumer lag creates a real contract, but reporting and rollback may require temporary replicated views. The extraction is complete when old write paths are absent and operational ownership is explicit.

## When it breaks

Unknown-field parsing errors during rollout suggest incompatible readers; old values reappearing suggest dual writers or stale events; mismatched counts after backfill suggest non-idempotent migration or changing source data; cross-service invariant failures suggest ambiguous ownership. First inventory producers, consumers, stored forms, versions, and direct write paths, then compare old/new counts and error rates by version. Stop destructive contraction until telemetry proves old readers and writers are gone.

## Practice

**Build:** design and implement a field rename with dual-read compatibility, idempotent backfill, version metrics, and final validation. **Break:** run an old reader during each migration phase and inject a backfill restart, preserving data. **Explain back:** name the owner of each invariant and every compatibility direction. Success requires old and new participants to coexist during expansion, rollback before contraction, zero unexplained mismatches, and documented removal evidence.

## Check yourself

1. Who should enforce an invariant spanning related fields?
2. Why is a database-per-service rule insufficient by itself?

## Sources

### REQUIRED

- [Evolutionary Database Design](https://martinfowler.com/articles/evodb.html)

### RECOMMENDED

- [Semantic Versioning](https://semver.org/)
- [Postel reconsidered RFC 9413](https://www.rfc-editor.org/rfc/rfc9413)

### DEEP DIVE

- [Building Evolutionary Architectures](https://www.oreilly.com/library/view/building-evolutionary-architectures/9781491986356/)

## Next

Continue to [Architecture Styles and Deployment Boundaries](./04-architecture-styles-and-deployment-boundaries.md).
