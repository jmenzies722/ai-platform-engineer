# Plugin architecture and extensibility

Plugins extend an IDP without forcing the core team to own every domain integration. A safe plugin model defines compatibility, permissions, data ownership, failure isolation, provenance, and retirement before inviting contribution.

## Why it matters

Unbounded plugins can execute with portal authority, leak catalog data, break upgrades, and make the core experience unreliable. A closed core instead turns every domain need into a central backlog bottleneck.

## How it works

Define extension points by contract: catalog processor, entity card, search provider, workflow action, policy check, or event consumer. Specify inputs, outputs, side effects, latency, error handling, version compatibility, and ownership. Prefer narrow capabilities over arbitrary in-process code.

Choose isolation according to risk. Pure presentation extensions may run client-side with constrained APIs. Backend actions handling secrets or mutations need server-side identity, network limits, scoped permissions, timeouts, audit, and often process or service isolation. Never pass the portal's broad credential to plugin code.

Require provenance, review, signed or verified artifacts, dependency scanning, test evidence, maintainer, support tier, and data-use declaration. Maintain a compatibility matrix and test plugins against candidate core releases. Budget latency and availability so one extension cannot block entity pages or search.

Provide lifecycle states: proposed, experimental, supported, deprecated, and removed. Make failure visible but degrade locally. A plugin should not own canonical data merely because it renders a view; authority remains with the relevant service.

## Vocabulary

- **extension point:** stable interface where independently owned behavior connects
- **plugin:** separately lifecycle-managed implementation of an extension contract
- **permission boundary:** limit on data and actions available to an extension
- **compatibility matrix:** tested combinations of core and plugin versions

## See it yourself

Model a scorecard plugin that needs catalog metadata and CI results. Predict the blast radius if it receives the portal backend token and runs in-process. Replace that with scoped read APIs, timeout, cached last-known result, and local error rendering. These controls reduce but do not eliminate supply-chain risk.

## Where it shows up

A database team owns a plugin that displays resource status and starts a resize workflow through the platform API. The plugin never stores database credentials, cannot mutate resources outside the viewed tenant, and fails as an isolated card when its backend is unavailable.

## When it breaks

Plugin upgrades pin the entire portal, abandoned dependencies block security patches, and frontend bundles expose sensitive configuration. Search providers return unauthorized entities. Workflow actions run shell fragments with unvalidated input. Detect with permission tests, software bills of materials, compatibility CI, latency budgets, and maintainer health.

## Practice

**Observe:** inventory extensions in an existing portal design. For each, record owner, permission, data authority, runtime isolation, support tier, and compatibility evidence.

**Design:** specify a plugin contract for database status and resize. Include schemas, auth, timeout, audit, degraded UI, versions, and retirement.

**Break:** make the plugin backend slow and then compromise its token. Define containment that keeps the portal usable and proves tenant scope limited exposure.

**Say it out loud:** explain why organizational ownership does not substitute for technical isolation.

## Check yourself

1. Which extension points should forbid side effects?
2. How can a portal remain available when a plugin fails?
3. Why must plugins declare data authority separately from display ownership?
4. What evidence permits a core upgrade with third-party plugins installed?

## Sources

### REQUIRED

- [Backstage plugins](https://backstage.io/docs/plugins/)

### RECOMMENDED

- [Backstage permissions](https://backstage.io/docs/permissions/overview/)

### DEEP DIVE

- [SLSA specification](https://slsa.dev/spec/v1.0/)

## Next

Continue to [Scorecards and engineering governance](06-scorecards-and-governance.md).
