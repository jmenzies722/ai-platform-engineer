# Control Flow and Functions

Functions turn a sequence of statements into a named contract with explicit inputs, results, and failure behavior.

## Why it matters

An endpoint that accepts an invalid port must choose a defined failure path before it opens a socket or writes state. Returning `None`, raising `ValueError`, and logging then continuing are different contracts for the caller. Clear control flow makes invalid cases visible in review and keeps partial work outside the valid path.

## How it works

`if` selects a path, loops repeat work, and `return` ends a function with a value. Python evaluates arguments before entering the function. Exceptions unwind the current path until a matching handler is found. Small functions are easiest to reason about when they avoid hidden global state.

Conditionals evaluate truth and select one suite; loops repeatedly bind targets and execute a body until the iterable ends or control exits. A function call evaluates argument expressions, creates a frame, binds parameters, and runs until `return` or an exception transfers control. Exceptions carry type, value, and traceback while unwinding frames; a matching handler takes responsibility for recovery at the level that understands the failure. `finally` runs cleanup regardless of the selected exit path. Separating calculation from I/O makes branches easy to exercise without setting up external state. Preconditions should be checked before irreversible effects, and a narrow exception handler should catch only errors it can interpret. A function contract includes side effects and exceptions as surely as its return value.

## See it yourself

**Tiny Proof:** predict `4.0` for the populated list and a handled `ValueError` for the empty list; no division should be attempted in the second case. Remove the guard in a copy and compare the new exception type and traceback location.

```bash
python3 - <<'PY2'
def mean(values):
    if not values:
        raise ValueError("values must not be empty")
    return sum(values) / len(values)
for xs in ([2, 4, 6], []):
    try: print(mean(xs))
    except ValueError as error: print(type(error).__name__, error)
PY2
```

Expected observation: The valid input returns `4.0`; the empty input follows an explicit exception path.

Limits of the control flow and functions observation: This small run does not prove numerical stability, thread safety, or that every iterable supports `len`. It demonstrates one explicit contract for concrete sequences, so broader inputs require a broader specification and tests.

## Where it shows up

Input parsing in a command service is a useful production boundary. A pure parser can reject malformed ports before configuration is committed, while the outer handler maps `ValueError` to a user-facing message and exit status. If parsing, file writes, and process startup share one broad `try`, a programming defect can be mislabeled as bad user input and leave partial state.

## When it breaks

A traceback before any side effect often identifies validation or calculation; a half-written file indicates the effect began before failure; swallowed errors show up as a false success status with missing results. First capture the complete traceback and the smallest input that triggers it, then identify the last completed side effect. Catching `Exception` around the whole function removes exactly the evidence needed to decide whether recovery is safe.

## Practice

**Build:** write `parse_port(text)` with an integer result from 1 through 65535 and explicit `ValueError` cases. **Break:** pass whitespace, text, zero, and 65536, then deliberately broaden a handler and observe how it hides an injected `RuntimeError`. **Explain back:** describe normal return, exceptional transfer, and cleanup as distinct paths. Success is a table of boundary inputs whose expected result or exception exactly matches automated assertions.

## Check yourself

1. What is the difference between returning an error value and raising an exception?
2. What makes a function pure?

## Sources

### REQUIRED

- [Python compound statements](https://docs.python.org/3/reference/compound_stmts.html)

### RECOMMENDED

- [Python errors and exceptions](https://docs.python.org/3/tutorial/errors.html)

### DEEP DIVE

- [Structure and Interpretation of Computer Programs](https://mitpress.mit.edu/9780262510875/structure-and-interpretation-of-computer-programs/)

## Next

Continue to [Modules, Environments, and Tests](./03-modules-environments-and-tests.md).
