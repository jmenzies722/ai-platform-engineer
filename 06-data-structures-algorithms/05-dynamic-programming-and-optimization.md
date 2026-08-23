# Dynamic Programming and Optimization

Dynamic programming solves overlapping subproblems once and combines their answers according to a state definition and recurrence.

## Why it matters

A naive recursive solution to a modest sequence problem can issue millions of repeated calls, while an incorrectly compressed table can return fast but wrong results. Dynamic programming is not “use a cache.” It requires a state containing exactly the information future choices need, correct transitions, base cases, and an evaluation order that satisfies dependencies.

## How it works

Optimal substructure means an optimal solution can be built from optimal subproblem solutions. Overlapping subproblems mean the same states recur. Top-down memoization preserves a recursive formulation and caches states reached; bottom-up tabulation orders states so dependencies are already available. Both trade storage for avoided recomputation.

Design begins by defining a state in words, such as “best value achievable using the first `i` items with capacity `c`.” The recurrence enumerates valid final choices, the base cases anchor empty inputs, and the answer maps back to a state. A table may retain parent choices to reconstruct a solution, not only its score. Space compression is safe only when overwritten states are no longer needed. Loop direction matters: updating one-dimensional 0/1 knapsack capacity upward accidentally permits reusing the same item, changing the problem into unbounded knapsack.

## See it yourself

**Tiny Proof:** predict the number of ways to climb five steps using moves of one or two. Each state depends only on the preceding two states.

```bash
python3 - <<'PY2'
ways = [0] * 6
ways[0] = 1
for step in range(1, len(ways)):
    ways[step] = ways[step - 1]
    if step >= 2:
        ways[step] += ways[step - 2]
print(ways)
PY2
```

Expected observation: state five is eight, and the table exposes every dependency used to obtain it.

Limits of this proof: this count has no optimization objective, integer values remain small, and a closed-form or constant-space recurrence exists. It demonstrates tabulation, not that every recurrence should use a table.

## Where it shows up

Diff tools use sequence-alignment ideas related to longest common subsequence; resource allocation can resemble knapsack; parsers and routing algorithms use structured state spaces. Production feasibility depends on state dimensions. A mathematically polynomial `O(nc)` capacity table is impractical when `c` is a huge numeric value, making it pseudo-polynomial rather than polynomial in the input’s bit length.

## When it breaks

Exponential call counts indicate uncached overlapping states; a table too large suggests an over-specified state or unsuitable formulation; correct score but wrong reconstruction suggests missing parent information; results changing with loop direction suggest accidental item reuse. First write the state meaning and recurrence independently of code, then enumerate tiny cases by brute force. Inspect only states needed for the first mismatch.

## Practice

**Build:** solve 0/1 knapsack with a two-dimensional table and reconstruct selected items. Add a brute-force oracle for up to twelve items. **Break:** compress to one dimension with forward capacity iteration and find a case where one item is reused. **Explain back:** define state, transition, base, order, answer, and complexity. Success means optimized and brute-force values agree across generated tiny inputs and reconstructed items satisfy capacity and value exactly.

## Check yourself

1. How do memoization and tabulation differ while using the same recurrence?
2. Why can loop direction change the problem represented by a compressed table?

## Sources

### REQUIRED

- [Introduction to Algorithms](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)

### RECOMMENDED

- [MIT OpenCourseWare: dynamic programming](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/lecture-19-dynamic-programming-i-fibonacci-shortest-paths/)

### DEEP DIVE

- [Dynamic Programming and Optimal Control](https://web.mit.edu/dimitrib/www/dpchapter.html)

## Next

Continue to [Correctness, Testing, and Algorithm Selection](./06-correctness-testing-and-algorithm-selection.md).
