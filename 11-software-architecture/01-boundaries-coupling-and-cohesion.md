# Boundaries, Coupling, and Cohesion

Architecture begins with deciding which responsibilities change together and which dependencies must stay controlled.

## Why it matters

A new tax rule should change tax policy without forcing edits in HTTP routing, database serialization, and deployment code. When one requirement ripples everywhere, the architecture has coupled reasons to change. Boundaries earn their cost by localizing such change and protecting a coherent responsibility, not by multiplying folders or interfaces.

## How it works

A cohesive component owns related behavior and data. Coupling describes what one component must know about another. Dependencies can be directed through interfaces so policy does not depend on transport or storage details. A boundary is useful only when its contract is clearer than direct access.

Cohesion measures how strongly a component’s responsibilities belong together; coupling measures the assumptions one component makes about another. A useful module owns an invariant or capability and exposes a contract smaller than its implementation. Dependency direction matters: domain policy can depend on an abstract behavior supplied by an adapter, so transport and storage details point inward toward the need rather than policy pointing outward toward frameworks. Information hiding keeps likely-to-change design decisions behind the boundary. Runtime calls can travel either way through these abstractions; source dependency and control flow are not the same thing. Boundaries also have costs in translation, testing, latency when remote, and ownership. A pass-through layer that hides no volatile decision is ceremony, while a shared database write that bypasses policy is uncontrolled coupling.

## See it yourself

Predict `1200` because checkout knows only the policy method and the concrete tax object supplies a twenty-percent calculation. Replace it with a fake policy to show the boundary without changing checkout.

```bash
python3 - <<'PY2'
class TaxPolicy:
    def total(self, cents): return cents + cents // 5
def checkout(policy, cents): return policy.total(cents)
print(checkout(TaxPolicy(), 1000))
PY2
```

Expected observation: Checkout depends on a small behavior contract rather than a database, HTTP framework, or global configuration.

Limits of the boundaries, coupling, and cohesion observation: The example does not justify a service boundary, persistence abstraction, or a class hierarchy. One injected behavior demonstrates source dependency only.

## Where it shows up

A modular monolith can keep ordering, pricing, and fulfillment as separate ownership boundaries while deploying one process. Pricing owns calculation rules and publishes a stable result contract; HTTP and database adapters translate at its edges. If later scaling or team ownership warrants process separation, the existing contract helps, but network failure and data consistency must then become explicit new concerns.

## When it breaks

Changes touching unrelated modules suggest low cohesion or leaked knowledge; circular imports reveal bidirectional source coupling; duplicated policy across adapters indicates the boundary does not own its invariant; an interface with one implementation and no volatile detail may be needless. First take one recent change and map every file, data owner, and dependency it crossed. That evidence is more useful than counting layers or applying a named architecture style.

## Practice

**Build:** separate one backend feature into domain policy, transport adapter, and persistence adapter, with tests at each contract. **Break:** let transport details enter the domain and make a second adapter expose the resulting friction, then restore direction. **Explain back:** justify each boundary by a reason to change and name its translation cost. Success means a policy change affects one cohesive area while integration tests still prove the assembled behavior.

## Check yourself

1. How does cohesion differ from coupling?
2. When is adding an interface needless?

## Sources

### REQUIRED

- [Parnas on decomposing systems](https://dl.acm.org/doi/10.1145/361598.361623)

### RECOMMENDED

- [Clean Architecture article](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

### DEEP DIVE

- [Software Architecture in Practice](https://www.oreilly.com/library/view/software-architecture-in/9780136885979/)

## Next

Continue to [Quality Attributes and Decisions](./02-quality-attributes-and-decisions.md).
