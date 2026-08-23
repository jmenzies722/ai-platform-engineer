# Sequences, Hash Tables, and Trees

The right data structure makes frequent operations cheap and makes required invariants visible.

## Why it matters

Choosing a dictionary because lookup is “O(1)” can fail when the application also needs sorted range scans, bounded memory, or stable duplicate handling. Data structures encode which operations are cheap and which invariants they maintain. The design decision should begin with operation frequency and ordering requirements, not the structure’s familiar name.

## How it works

Arrays and dynamic arrays give indexed access and contiguous storage. Linked structures trade locality for cheap relinking when a node is known. Hash tables map keys to buckets and resolve collisions. Balanced search trees preserve order while keeping height logarithmic.

A contiguous array maps an integer index to an offset and gives strong locality; a dynamic array reserves capacity and occasionally copies elements as it grows. Linked nodes make relinking cheap once a node is known but require pointer traversal for indexing. A hash table computes a hash, maps it to a bucket, and resolves collisions while resizing to control load; equality still decides whether candidate keys match. Expected constant lookup relies on hash distribution and bounded collision behavior. Search trees compare keys along paths, and balancing rules keep height logarithmic after updates. Heaps maintain only enough order to expose an extremal element efficiently. No structure dominates: layout, metadata, mutation, iteration, ordering, and concurrency requirements all move cost between operations.

## See it yourself

Predict that the second `sam` assignment replaces the first value, while sorting the items creates an ordered view without changing the mapping’s key-value contract.

```bash
python3 - <<'PY2'
records=[('sam',3),('lee',5),('sam',7)]
latest={}
for name, value in records: latest[name]=value
print(latest, sorted(latest.items()))
PY2
```

Expected observation: The dictionary keeps one latest value per key; sorting adds ordered traversal that the mapping contract does not require.

Limits of the sequences, hash tables, and trees observation: The output does not benchmark dictionary complexity, promise iteration behavior in other languages, or show collision handling. A three-key example only demonstrates replacement and an explicit sort.

## Where it shows up

A scheduler is a concrete production connection. Jobs arrive by ID, operators need direct cancellation, and workers need the earliest deadline. One dictionary can own ID lookup while a heap supplies deadline order, with stale heap entries handled deliberately. Forcing either structure to satisfy both operations alone creates linear scans or complicated mutation; combining them requires an invariant that both views represent the same live jobs.

That invariant should be checked in tests after every mutation, because two individually valid structures can still disagree about shared logical state.

## When it breaks

Slow lookups under selected keys can indicate collision or expensive equality; memory spikes during growth suggest resize and over-allocation; sorted traversal becoming linear suggests an unbalanced tree or wrong structure. First record operation counts, input distribution, size, and profile location. Check the representation invariant with a small diagnostic before replacing the structure, because stale duplicate entries often masquerade as algorithmic slowness.

## Practice

**Build:** implement a tiny scheduler using a dictionary plus heap and test insert, replace, cancel, and next-due behavior. **Break:** leave a canceled job in the heap and demonstrate how lazy deletion must detect it. **Explain back:** compare array, linked structure, hash table, balanced tree, and heap for one workload. Success means invariants hold after every operation and measured complexity matches the operation table you wrote first.

## Check yourself

1. Why is hash-table lookup expected O(1), not guaranteed O(1)?
2. What workload benefits from ordered keys?

## Sources

### REQUIRED

- [Python collections](https://docs.python.org/3/library/collections.html)

### RECOMMENDED

- [Open Data Structures](https://opendatastructures.org/)

### DEEP DIVE

- [Purely Functional Data Structures](https://www.cambridge.org/core/books/purely-functional-data-structures/0409255DA1B48FA731859AC72E34D494)

## Next

Continue to [Searching, Sorting, and Graph Traversal](./03-searching-sorting-and-graph-traversal.md).
