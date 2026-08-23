# Values, Names, and Types

Python variables are names bound to objects, not boxes with fixed types. That distinction explains mutation, aliasing, and many surprising bugs.

## Why it matters

A function that “only sorts a list” can silently reorder data owned by its caller because two names reach the same mutable object. That bug changes API design: should the function mutate in place, return a copy, or document ownership transfer? Understanding binding and identity prevents defensive copying everywhere while making mutation explicit where it matters.

## How it works

Assignment binds a name to an object. Immutable objects such as integers and strings cannot change in place; operations create another object. Lists and dictionaries are mutable, so two names can observe the same object changing. Type belongs to the object and determines supported operations.

Python evaluates an object and binds a name to the resulting reference. Rebinding one name does not alter other names, but mutating the shared object is visible through every alias. Immutable objects expose no operation that changes their value; an expression such as `n + 1` creates or retrieves another integer and rebinds a name if assigned. A list copy creates a new outer list, yet its elements may still be references to the same nested objects, which is why shallow and deep copying answer different ownership needs. Function arguments are bindings in a new local namespace, not pass-by-value copies of arbitrary objects. Equality delegates to value behavior, whereas identity asks whether two references designate the same object. `None`, sentinels, and singleton objects are identity questions; ordinary strings and numbers are usually value questions.

## See it yourself

Predict that appending through `b` changes the list displayed by `a`, while `c == a` is true and `c is a` is false. Add a nested list and predict which inner mutation a shallow copy will share.

```bash
python3 - <<'PY2'
a = [1, 2]
b = a
b.append(3)
print(a, a is b)
c = a.copy()
print(c == a, c is a)
PY2
```

Expected observation: `a` changes through alias `b`. The shallow copy compares equal but has a different identity.

Limits of the values, names, and types observation: The output does not reveal object addresses, prove that every immutable value is interned, or make identity comparisons safe for equal numbers and strings. Interning is an implementation choice, not an application contract.

## Where it shows up

Configuration handling makes aliasing operationally important. A server may cache a default dictionary, pass it into each request setup, and then add request-specific keys. If the code reuses the same nested dictionary, one tenant’s settings can leak into another request. An explicit copy policy, immutable configuration representation, or constructor that owns its input gives reviewers a boundary they can test.

## When it breaks

Unexpected changes in a caller’s list suggest aliasing; state retained between calls often points to a mutable default; `is` comparisons that vary across runs suggest mistaken reliance on interning. First print or test identity at the suspected ownership boundary and reduce the case to two names plus one mutation. Inspect nested identities separately before reaching for `deepcopy`, because indiscriminate deep copying can be expensive or semantically wrong.

## Practice

**Build:** implement `sorted_copy(values)` and a function that safely adds a key to a nested configuration without changing its input. **Break:** replace the copy with direct mutation and write a test that exposes the caller-visible change. **Explain back:** use the words binding, alias, identity, equality, mutable, and shallow copy against the test objects. Success requires assertions for both values and identities before and after each call.

## Check yourself

1. What is bound by `x = y`?
2. When should you use `is` instead of `==`?

## Sources

### REQUIRED

- [Python data model](https://docs.python.org/3/reference/datamodel.html)

### RECOMMENDED

- [Python tutorial: data structures](https://docs.python.org/3/tutorial/datastructures.html)

### DEEP DIVE

- [Fluent Python](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/)

## Next

Continue to [Control Flow and Functions](./02-control-flow-and-functions.md).
