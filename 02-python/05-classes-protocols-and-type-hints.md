# Classes, Protocols, and Type Hints

Python classes can protect invariants and provide behavior through ordinary protocols. They are valuable when they clarify a concept, not merely when they wrap a dictionary.

## Why it matters

A monetary value with an amount but no currency permits meaningless addition. A class can validate construction and define only legitimate operations, while type hints let tools identify inconsistent uses before execution. Neither mechanism substitutes for runtime validation at untrusted boundaries.

## How it works

A class statement creates a class object. Calling it normally allocates an instance and invokes initialization. Instance attribute lookup consults the instance and class hierarchy; methods are functions that bind the instance when accessed. Class attributes are shared through the class and should not accidentally hold per-instance mutable state. Composition gives one object collaborators; inheritance establishes a substitutable relationship and carries coupling to base behavior.

Python protocols are behavior conventions such as iteration, context management, comparison, and string representation. Implementing the relevant special methods lets an object participate without inheriting from a particular concrete class. `dataclasses` generate routine initialization and comparison code while leaving validation and semantics to the author. Type annotations are metadata consumed by readers and static checkers; Python generally does not enforce them at runtime. Structural `Protocol` types describe required operations, making dependency boundaries explicit without demanding shared ancestry.

## See it yourself

**Tiny Proof:** predict that two frozen values compare by fields and cannot have `amount` reassigned. Validation still runs at construction.

```bash
python3 - <<'PY2'
from dataclasses import dataclass
@dataclass(frozen=True)
class Money:
    amount: int
    currency: str
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("amount must be nonnegative")
print(Money(5, "USD") == Money(5, "USD"))
try:
    Money(-1, "USD")
except ValueError as error:
    print(type(error).__name__, error)
PY2
```

Expected observation: field equality is true and the invalid amount follows the explicit error path.

Limits of this proof: `frozen=True` does not recursively freeze mutable fields, validate currency codes, or make arithmetic semantics correct. Type annotations alone would accept bad runtime data.

## Where it shows up

A service that sends notifications can depend on a `Sender` protocol with a `send(message)` method. Production supplies an SMTP or queue adapter; tests supply a recording fake. The application owns the semantic contract while adapters own external details. This boundary is stronger than mocking arbitrary internal methods because it names the actual capability and failure behavior the use case requires.

## When it breaks

State shared between instances suggests a mutable class attribute; deep inheritance failures suggest violated substitutability; `AttributeError` at a boundary suggests an undocumented protocol; a clean type-check with bad input suggests missing runtime parsing. First inspect construction, instance dictionaries, method resolution, and the smallest public contract. Prefer composition when a subclass must disable or contradict inherited behavior.

## Practice

**Build:** define immutable `Measurement(value, unit)`, validate allowed units, and inject a formatter satisfying a small protocol. **Break:** place a mutable list in a class attribute and demonstrate cross-instance leakage, then correct it with an instance field. **Explain back:** distinguish runtime class, instance, protocol, annotation, and validation. Success means a static checker can understand the interface, tests use a fake collaborator, and untrusted values are rejected at runtime.

## Check yourself

1. What does method binding add to a function retrieved through an instance?
2. Why do type hints not remove the need for boundary validation?

## Sources

### REQUIRED

- [Python classes](https://docs.python.org/3/tutorial/classes.html)

### RECOMMENDED

- [dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [typing.Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol)

### DEEP DIVE

- [PEP 544: Protocols](https://peps.python.org/pep-0544/)

## Next

Continue to [Iteration, Resources, and Program Boundaries](./06-iteration-resources-and-program-boundaries.md).
