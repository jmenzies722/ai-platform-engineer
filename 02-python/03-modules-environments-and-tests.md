# Modules, Environments, and Tests

A Python program becomes maintainable when imports, dependencies, and behavior are explicit and repeatable.

## Why it matters

A module that sends a network request during import can make a test suite fail before it discovers a single test. The practical decision is where initialization belongs and which dependencies must be declared for a fresh environment. A repeatable import and test command is a stronger delivery artifact than “works in my shell.”

## How it works

A module is normally one `.py` file with its own namespace. Import executes module initialization once per interpreter and binds names. Virtual environments isolate installed distributions. Tests call public behavior with controlled inputs and compare actual results with expected results.

Import searches configured locations for a module specification, creates a module object, places it in `sys.modules`, and executes top-level code to initialize its namespace. The early cache entry helps with repeated imports and participates in circular-import behavior; it does not make arbitrary initialization safe. A package groups modules and controls its public surface through names and documentation. Virtual environments select an interpreter context and installation location, but they do not freeze dependency versions by themselves. Tests arrange controlled state, invoke public behavior, and assert outcomes; setup and teardown must not leak state across cases. Importing the module rather than copying implementation logic makes tests exercise the same boundary callers use. Running tests with `python -m` also makes interpreter selection explicit.

## See it yourself

Predict that the temporary directory is searched through `PYTHONPATH`, `double(3)` returns six, and the assertion prints `test passed`. Change the assertion to seven and predict the nonzero status before running it.

```bash
tmp=$(mktemp -d)
printf 'def double(n):\n    return n * 2\n' > "$tmp/math_demo.py"
PYTHONPATH="$tmp" python3 - <<'PY2'
from math_demo import double
assert double(3) == 6
print("test passed")
PY2
rm -rf "$tmp"
```

Expected observation: The temporary directory becomes an import location; the assertion passes and cleanup removes it.

Limits of the modules, environments, and tests observation: The demonstration does not create an installable distribution, isolate transitive dependencies, or prove that tests cover meaningful behavior. `PYTHONPATH` is a focused import experiment, not a packaging strategy.

## Where it shows up

A deployment image often fails because the build installed a distribution into one interpreter while the entrypoint invokes another. Recording `sys.executable`, installing from a locked dependency description, and running tests through that interpreter makes the mismatch observable during build. Keeping database connections and environment validation in an explicit `main` or application factory also lets tooling import modules without opening production resources.

## When it breaks

`ModuleNotFoundError` suggests search path, environment, package layout, or missing installation; an attribute missing during a circular import suggests partially initialized modules; order-dependent tests suggest leaked globals or fixtures. First print the active executable, module `__file__`, and a concise `sys.path`, then reproduce in a fresh process. Do not immediately add directories to `PYTHONPATH`; that can mask an incorrect package or deployment layout.

## Practice

**Build:** place one parser in a module and three `unittest` cases in a separate file, then run them with `python3 -m unittest`. **Break:** add an import-time read of a nonexistent file and observe when discovery fails; move that read behind an explicit function. **Explain back:** distinguish module, package, distribution, environment, and test process. Success is a clean run from a newly created virtual environment using only declared setup steps.

## Check yourself

1. Why should reusable modules avoid doing real work at import time?
2. What does a virtual environment isolate?

## Sources

### REQUIRED

- [Python modules](https://docs.python.org/3/tutorial/modules.html)

### RECOMMENDED

- [venv](https://docs.python.org/3/library/venv.html)
- [unittest](https://docs.python.org/3/library/unittest.html)

### DEEP DIVE

- [Python Packaging User Guide](https://packaging.python.org/en/latest/)

## Next

Continue to [Computer Systems](../03-computer-systems/README.md).
