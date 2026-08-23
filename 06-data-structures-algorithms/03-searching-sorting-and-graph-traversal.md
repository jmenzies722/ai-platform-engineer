# Searching, Sorting, and Graph Traversal

Many larger problems reduce to ordering values, finding boundaries, or exploring connected states.

## Why it matters

A dependency resolver that forgets visited nodes can loop forever on one cycle, and a binary search over unsorted data can return a plausible but wrong absence. These algorithms are short because strong invariants do the work. Engineering safely means stating the invariant and the graph or ordering model before trusting the implementation.

## How it works

Binary search repeatedly discards half of a sorted search interval. Comparison sorting generally needs O(n log n) comparisons in the worst case. Breadth-first search explores by distance in unweighted graphs; depth-first search follows a path before backtracking. Both require tracking visited states.

Binary search maintains a half-open interval in which the target boundary may still lie, compares at a midpoint, and discards a region that cannot contain that boundary under sorted order. Sorting establishes order at an O(n log n) comparison cost for general comparison models, with stability deciding whether equal keys retain input order. A graph represents vertices and edges; breadth-first search uses a queue to expand unweighted distance layers, while depth-first search uses a stack or recursion to follow one frontier deeply. A visited set prevents repeated exploration and gives termination on finite graphs. BFS yields shortest paths only when edges have equal cost; weighted shortest paths require algorithms whose frontier ordering respects weights. Parent links reconstruct paths without storing a full path in every queue entry.

## See it yourself

**Tiny Proof:** predict that `bisect_left` returns index one for target four and index three as the insertion point for five. Membership still requires checking that the index is in range and holds the target.

```bash
python3 - <<'PY2'
from bisect import bisect_left
xs=[2,4,4,9]
for target in (4,5):
    i=bisect_left(xs,target)
    print(target, i, i < len(xs) and xs[i] == target)
PY2
```

Expected observation: Insertion position and successful membership are separate facts, especially with duplicates.

Limits of the searching, sorting, and graph traversal observation: The sample does not verify sorted input, measure logarithmic growth, or define behavior under concurrent mutation. `bisect` trusts the caller’s ordering invariant.

## Where it shows up

Service dependency analysis turns configuration into a directed graph. During an incident, BFS can find a minimum-hop path from an entry service to a failed datastore, while DFS can detect cycles in startup dependencies. The result is only as valid as the graph snapshot: dynamic routing, optional edges, and weighted latency can make “fewest hops” the wrong operational path.

## When it breaks

Incorrect binary-search answers at boundaries suggest interval or duplicate handling; traversal that never terminates suggests missing visited state; a path that is not cheapest suggests using BFS on weighted edges. First save the smallest failing input and log the interval or frontier plus visited set at each step. Assert sortedness or graph invariants in tests rather than adding conditionals around wrong results.

## Practice

**Build:** implement BFS returning a shortest unweighted path and binary search returning the first equal index. **Break:** include a cycle, duplicate sorted keys, empty input, and an unreachable destination; separately violate sorted order and document that the contract is broken. **Explain back:** state each loop invariant and why it permits discarding work. Success is property-oriented tests that compare results with a simple reference on many small generated cases.

## Check yourself

1. What invariant makes binary search correct?
2. Why does BFS find shortest paths only under the right edge-cost model?

## Sources

### REQUIRED

- [Python bisect](https://docs.python.org/3/library/bisect.html)

### RECOMMENDED

- [CLRS graph algorithms](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)

### DEEP DIVE

- [The Design and Analysis of Computer Algorithms](https://www.pearson.com/en-us/subject-catalog/p/design-and-analysis-of-computer-algorithms-the/P200000003482)

## Next

Continue to [Recursion, Divide and Conquer, and Greedy Choice](./04-recursion-divide-and-conquer-and-greedy-choice.md).
