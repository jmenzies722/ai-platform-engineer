# Platforms as products

An internal platform is a product and a long-lived service. It earns investment when it solves repeated problems for defined users better than local solutions, while preserving clear boundaries and support obligations.

## Why it matters

A tool mandate can consolidate interfaces while leaving waits, failures, and cognitive load intact. Product thinking forces a team to identify whose problem matters, what evidence demonstrates it, and which outcome justifies operating another critical system.

## How it works

Segment users by work and constraints: application teams, regulated workloads, data teams, operators, and security reviewers may need different promises. Interview them about a recent event rather than asking for features. Reconstruct elapsed time, hands-on time, handoffs, failures, workarounds, and consequences across creation, change, operation, and retirement.

Turn evidence into a problem statement with frequency, affected population, baseline, and falsifiable outcome. Prioritize repeated, undifferentiated work where central expertise or economies of scale matter. A platform should not absorb product-specific decisions merely because it can automate them.

Write a product charter: target users, jobs to be done, capabilities, non-goals, service levels, ownership, funding, support, and retirement conditions. Maintain a roadmap of outcomes and risks, not a shopping list of integrations. Start with a thin end-to-end capability and instrument it before expanding.

Product management does not remove operational accountability. The platform team owns reliability, incident response, documentation, migrations, and user research for its service. Stream-aligned teams remain accountable for their applications and for decisions outside the published contract.

## Vocabulary

- **internal platform:** shared capabilities consumed by engineering teams through supported contracts
- **platform product:** the capabilities, interfaces, service model, and lifecycle managed for internal users
- **cognitive load:** mental effort required to understand and safely complete work
- **job to be done:** a user outcome described independently of a requested implementation

## See it yourself

Compare two discovery notes:

```text
Request: Give every team Kubernetes access.
Observed journey: 12 teams opened 31 environment tickets last month.
Median elapsed time was 3.8 days; median hands-on platform work was 24 minutes.
Nine tickets were reopened because identity or telemetry was missing.
```

Predict which note permits a testable investment decision. The second establishes volume, delay, rework, and likely common capability. It still does not prove Kubernetes or a portal is the right solution; a prototype and outcome measurement must do that.

## Where it shows up

A cloud foundation team found that account creation was slow, but interviews showed the largest cost occurred after creation: teams could not identify owners or budgets. Its first product increment therefore coupled account vending with ownership and cost contracts. The design addressed the complete user journey instead of optimizing one provisioning step.

## When it breaks

Technology-first programs often report shipped components while developer lead time stays flat. Watch for low repeat use, shadow tooling, rising exception queues, unresolved support tickets, and users who cannot explain the platform promise. These distinguish weak product fit from an interface usability problem.

A platform also fails by accepting every request. Unbounded scope produces fragile integrations and no coherent contract. Review demand by segment and frequency; explicitly decline work that is rare, differentiating, or better owned by another team.

## Practice

**Observe:** interview three users about the same recent delivery task. Build a journey table with timestamps, handoffs, errors, and evidence links. Completion means another reviewer can distinguish reported opinion from observed event data.

**Design:** write a one-page product charter for one repeated problem. Include target and excluded users, baseline, outcome, capabilities, non-goals, SLO, support, and retirement trigger.

**Break:** challenge the charter with one regulated workload and one unusual high-scale workload. Do not add features automatically. Record whether each need changes the core contract, needs a separate tier, or belongs outside the platform.

**Say it out loud:** explain why high request volume is not by itself evidence that a feature belongs in the platform.

## Check yourself

1. What evidence distinguishes a recurring user problem from enthusiasm for a tool?
2. When should a platform team reject a commonly requested capability?
3. Why can mandatory adoption hide weak product fit?
4. Which service obligations continue after a capability first ships?

## Sources

### REQUIRED

- [CNCF Platform Engineering Technical Community Group](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

### RECOMMENDED

- [Team Topologies: Platform as a product](https://teamtopologies.com/key-concepts-content/platform-as-a-product)

### DEEP DIVE

- [DORA platform engineering research](https://dora.dev/research/2024/dora-report/)

## Next

Continue to [Paved roads and capability contracts](02-paved-roads.md).
