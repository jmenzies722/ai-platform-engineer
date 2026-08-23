# Recursion, Divide and Conquer, and Greedy Choice

Recursive definitions reduce a problem to smaller instances. Divide-and-conquer and greedy algorithms use that reduction in different ways, and each needs a proof that local work composes into a global answer.

## Why it matters

A recursive function can look mathematically elegant while repeating the same work exponentially or overflowing the call stack. A greedy rule can pass dozens of examples and still fail because an early local choice blocks the optimum. The implementation is the easy part; the reduction, progress measure, and proof obligation decide whether it is an algorithm.

## How it works

Recursion needs base cases and a progress measure that moves every call toward them. The call stack stores suspended state, so recursion depth consumes space even when the total operation count is small. An iterative form can represent pending work explicitly when depth is unbounded.

Divide-and-conquer splits a problem into mostly independent subproblems, solves them, and combines results. Its cost is often expressed by a recurrence such as `T(n) = 2T(n/2) + O(n)` for merge sort. Balanced division and linear combination yield `O(n log n)`; unbalanced partitions can change the bound. A greedy algorithm makes one irrevocable locally preferred choice. Correctness requires structure such as a greedy-choice property and optimal substructure, often proved by exchange: transform an optimal solution to include the greedy choice without making it worse. Activity selection by earliest finish has such an argument; coin change with arbitrary denominations does not.

## See it yourself

**Tiny Proof:** predict that earliest-finish scheduling selects four compatible intervals from this input. Trace the invariant that selected intervals never overlap.

```bash
python3 - <<'PY2'
activities = [(0, 6), (1, 2), (3, 4), (5, 7), (8, 9)]
chosen = []
finish = float("-inf")
for start, end in sorted(activities, key=lambda item: item[1]):
    if start >= finish:
        chosen.append((start, end))
        finish = end
print(chosen)
PY2
```

Expected observation: the result is `[(1, 2), (3, 4), (5, 7), (8, 9)]`; the selected intervals do not overlap.

Limits of this proof: one example does not prove optimality, weighted activities need a different algorithm, and sorting cost is part of total complexity. The exchange argument, not the output, justifies the greedy rule.

## Where it shows up

External merge sort divides data into memory-sized sorted runs and merges them, turning a memory limit into an explicit I/O strategy. Scheduling systems use greedy policies for particular objectives, but shortest-job-first, earliest-deadline, and fairness optimize different criteria. Applying a known greedy name without matching assumptions can starve work or miss service objectives.

## When it breaks

Maximum recursion depth suggests the progress measure or input depth exceeds the call-stack model; duplicated subcalls suggest overlapping subproblems; poor quicksort behavior suggests pathological partitions; a greedy result below a small exhaustive optimum disproves the rule. First save the smallest counterexample and trace subproblem sizes and choices. Replace recursion with iteration only after preserving the invariant, not as a syntax translation.

## Practice

**Build:** implement merge sort with one reusable merge buffer and interval scheduling by earliest finish. **Break:** use latest start or shortest duration as alternative greedy rules and find minimal counterexamples by exhaustive search over small intervals. **Explain back:** state base case, progress measure, recurrence, combine rule, and exchange argument. Success means outputs match Python’s sorted reference and greedy choices match exhaustive optimum for all generated small unweighted cases.

## Check yourself

1. What proves a recursive function terminates?
2. Why is optimal substructure alone insufficient to justify a greedy choice?

## Sources

### REQUIRED

- [Introduction to Algorithms](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)

### RECOMMENDED

- [Open Data Structures: sorting](https://opendatastructures.org/ods-python/11_Sorting_Algorithms.html)

### DEEP DIVE

- [Algorithm Design](https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003259)

## Next

Continue to [Dynamic Programming and Optimization](./05-dynamic-programming-and-optimization.md).
