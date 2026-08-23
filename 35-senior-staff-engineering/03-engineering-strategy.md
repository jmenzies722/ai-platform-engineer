# Engineering strategy

Engineering strategy is a coherent set of choices about where technical effort will create advantage, reduce constraint, and deliberately not be spent.

## Why it matters

A roadmap can contain many reasonable projects while lacking any explanation of why they jointly change the organization’s position.

## How it works

Begin with diagnosis: business direction, user need, technical constraints, organizational capability, external change, and evidence from incidents and delivery. State the few challenges that matter now. Then define guiding policies that constrain choices, such as “centralize safety enforcement while keeping model selection replaceable.”

Translate policy into coordinated actions, sequencing, ownership, and measures. A strategy names tradeoffs and exclusions. It distinguishes an outcome horizon from committed near-term work and preserves options where uncertainty is high. Test whether each initiative addresses the diagnosis through a named mechanism.

Use leading measures for adoption or constraint removal and lagging measures for outcomes. Include kill criteria and review triggers. Invite product, security, finance, and operating teams into diagnosis without turning the document into consensus prose. The accountable leader chooses when legitimate interests conflict.

## See it yourself

“Build an internal model gateway, evaluation service, and prompt registry” is a project list. “Reduce unsafe provider coupling by centralizing identity, audit, and spend controls while standardizing evaluation contracts and preserving provider portability” is a strategy because it explains choices and the relationship among actions.

## Where it shows up

Strategies guide reliability, cloud migration, developer platforms, data governance, build systems, and AI adoption. They are especially useful when local team incentives would otherwise produce incompatible optimizations.

## When it breaks

Strategy fails as aspiration, architecture inventory, executive vocabulary, or a backlog without exclusions. If teams cannot use it to choose between two plausible actions, the guiding policy is too weak.

## Practice

**Build:** write a two-page AI platform strategy with diagnosis, three guiding policies, coordinated actions, non-goals, measures, and review triggers. **Break:** cut the budget by 35 percent and add a portability requirement. **Explain back:** show which choices remain coherent and which initiative stops.

## Check yourself

1. How does strategy differ from a roadmap?
2. What makes a guiding policy useful?
3. Which evidence should cause a strategy review?

## Sources

### REQUIRED

- [DORA research](https://dora.dev/research/)

### RECOMMENDED

- [Thoughtworks Technology Radar](https://www.thoughtworks.com/radar)

### DEEP DIVE

- [Wardley Maps: Introduction](https://learnwardleymapping.com/book/)

## Next

Continue to [Technical vision and architecture direction](04-technical-vision-and-architecture-direction.md).
