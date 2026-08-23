# Catalogs, ownership, and lifecycle

A service catalog is a queryable model of software entities, relationships, ownership, and lifecycle backed by authoritative sources and freshness evidence. A portal may display it, but the model and ingestion contracts are the product.

## Why it matters

During changes and incidents, teams need to know what a service does, who can decide, what depends on it, and where operational evidence lives. A stale inventory creates confident but wrong impact analysis and routing.

## How it works

Model a small ontology of components, APIs, resources, systems, domains, groups, and users. Give entities stable identifiers independent of display names. Represent relations as typed references such as component belongs-to system, API provided-by component, and resource consumed-by component.

Assign each field an authoritative source. Repository descriptors may own declared component metadata; identity systems own groups; runtime discovery owns deployed instances; observability systems own current health. Ingestion validates schema, records provenance and timestamp, and distinguishes declared, inferred, and observed facts. Define conflict resolution rather than silently accepting last write.

Ownership is a responsibility contract with a resolvable group, escalation path, and scope. Lifecycle covers creation, operation, transfer, deprecation, and deletion. Validate that owners exist and require explicit transfer acceptance. Orphan detection is a catalog health signal.

Expose catalog freshness, ingestion failures, relation integrity, and coverage separately from service health. Search and APIs must enforce authorization because ownership, dependency, and operational metadata can reveal sensitive architecture.

## Vocabulary

- **entity:** identified object represented in the catalog
- **ontology:** entity kinds and allowed relationships
- **provenance:** source and process from which a fact was derived
- **authoritative source:** system designated to decide a field's value

## See it yourself

Create two services that both use display name `payments`, then rename one owner team. Predict impact analysis with free-text links. Stable identifiers preserve relations; display-name joins produce ambiguity. This demonstrates identifier value, not truth of a relation whose source may still be stale.

## Where it shows up

Before a database maintenance event, operators query observed consumers, declared owners, and criticality. The UI shows that one dependency was last observed 40 days ago, preventing stale data from appearing equivalent to current runtime evidence.

## When it breaks

Manual metadata drifts, ingestion overwrites better sources, and deleted entities leave dangling relations. Broad search leaks internal topology. A catalog reports 98% entity coverage while only 55% have valid owners. Diagnose with source lag, schema rejection, orphan, duplicate-ID, relation-integrity, and field-provenance metrics.

## Practice

**Observe:** select five catalog fields and trace each to its authority, update event, validation, freshness objective, and conflict policy.

**Build:** define YAML for a component, API, resource, system, and group with stable references. Write validation cases for missing owner, dangling relation, and duplicate identity.

**Break:** dissolve an owner group and delay one ingestion source. Show how the catalog marks orphaned ownership and stale facts without deleting historical evidence.

**Say it out loud:** explain why catalog completeness and catalog trustworthiness are different measures.

## Check yourself

1. How should two sources disagreeing about ownership be resolved?
2. Why must inferred and declared dependencies remain distinguishable?
3. Which catalog fields require authorization to discover?
4. Why must deletion and transfer be modeled explicitly?

## Sources

### REQUIRED

- [Backstage system model](https://backstage.io/docs/features/software-catalog/system-model/)

### RECOMMENDED

- [Backstage descriptor format](https://backstage.io/docs/features/software-catalog/descriptor-format/)

### DEEP DIVE

- [CNCF Platforms whitepaper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

## Next

Continue to [Templates and self-service workflows](02-templates-and-workflows.md).
