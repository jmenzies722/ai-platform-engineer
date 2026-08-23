# Collections, Comprehensions, and Data Modeling

Python’s built-in collections express order, uniqueness, association, and mutability. Choosing among them is a modeling decision before it is a performance decision.

## Why it matters

Representing unique account IDs in a list permits duplicates and invites repeated linear scans. Replacing every list with a set is no better when input order or duplicate evidence matters. A collection should make the domain invariant easy to state and hard to violate, while retaining only the data the operation actually needs.

## How it works

A `list` is a mutable ordered sequence with indexed access. A `tuple` is an immutable sequence and can be a dictionary key when all its elements are hashable. A `dict` maps unique hashable keys to values and preserves insertion order in current Python’s language contract. A `set` stores unique hashable members and supports mathematical set operations. Hashability requires a stable hash consistent with equality, which is why mutable lists cannot be keys.

Slicing creates a new sequence for built-in lists and strings; a slice’s stop is excluded. Comprehensions combine iteration, optional filtering, and construction in one expression. They are clearest when the expression is a direct transformation, not a nest of side effects. Unpacking destructures values by shape and starred targets collect a remainder. Data modeling often benefits from retaining both a sequence of observations and a mapping or set derived for lookup. Derived views need an update invariant if they persist; recomputing a small view can be safer than synchronizing two mutable stores.

## See it yourself

**Tiny Proof:** predict which information each structure discards. The list retains order and duplicates, the set retains unique values, and the dictionary retains one value per key.

```bash
python3 - <<'PY2'
events = [("a", 2), ("b", 1), ("a", 5)]
names = {name for name, _ in events}
latest = {name: value for name, value in events}
positive = [(name, value) for name, value in events if value > 1]
print(names, latest, positive)
PY2
```

Expected observation: `events` contains three observations, `names` has two members, and `latest["a"]` is five.

Limits of this proof: set display order is not a sorted contract, and a tiny example says nothing about memory or crossover performance. The dictionary comprehension deliberately overwrites duplicate keys.

## Where it shows up

An ingestion service may need an ordered audit trail, a set of IDs seen in the current batch, and a dictionary of the newest event per ID. Keeping all three can be correct if their roles and lifetimes differ. If they survive mutations together, code should centralize updates and assert that every lookup entry corresponds to an audit event. Otherwise one stale derived structure can produce decisions inconsistent with the source data.

## When it breaks

`KeyError` suggests absent-key behavior was unspecified; silently lost duplicates suggest a mapping or set erased meaningful events; `TypeError: unhashable type` suggests a mutable key; memory spikes suggest an unnecessary materialized copy. First reduce the problem to the required operations and inspect representative cardinality, duplicates, ordering, and key types. Do not use `dict.get` blindly when absence and a stored `None` have different meanings.

## Practice

**Build:** parse ordered `(user, role)` events into an audit list, a unique-user set, and a latest-role mapping, with a report that preserves first-seen order. **Break:** include duplicate users, empty roles, and a list as a key candidate. **Explain back:** name what each representation preserves and discards. Success means tests cover ordering, duplicate policy, missing keys, and invariants between every derived view.

## Check yourself

1. Why must a dictionary key’s hash remain stable?
2. When is a comprehension less clear than an ordinary loop?

## Sources

### REQUIRED

- [Python data structures](https://docs.python.org/3/tutorial/datastructures.html)

### RECOMMENDED

- [Python expressions: displays and comprehensions](https://docs.python.org/3/reference/expressions.html#displays-for-lists-sets-and-dictionaries)

### DEEP DIVE

- [Python data model: hashable objects](https://docs.python.org/3/reference/datamodel.html#object.__hash__)

## Next

Continue to [Classes, Protocols, and Type Hints](./05-classes-protocols-and-type-hints.md).
