# Catalogs, ownership, and lifecycle

A service catalog is a trustworthy model of software entities, relationships, ownership, and lifecycle, not a manually curated list of links.

## Why it matters

During changes and incidents, teams need to know what a service does, who owns it, what it depends on, and where operational evidence lives.

## How it works

Model entities such as components, APIs, resources, systems, and groups with stable identifiers. Record owner, lifecycle, domain, dependencies, source, documentation, dashboards, runbooks, and health. Prefer authoritative ingestion from repositories and infrastructure, with validation and freshness indicators.

Ownership is a responsibility contract, not just a team name. Lifecycle includes creation, operation, transfer, deprecation, and deletion. Keep the schema small enough that fields remain accurate.

## See it yourself

Given a failing database, query relationships to find consuming services and owners. If relations are free-text names, renames and duplicates make impact analysis unreliable.

## Where it shows up

Incident routing, API discovery, compliance evidence, dependency reviews, scorecards, and cost allocation.

## When it breaks

Metadata is copied by hand, ownership points to dissolved teams, inferred relationships are presented as facts, or catalog health is confused with service health.

## Practice

Write one YAML entity for a service and one for its API. Include durable references, ownership, lifecycle, dependencies, and operational links.

## Check yourself

1. Which source should be authoritative for ownership?
2. Why must deletion be part of lifecycle?

## Sources

### REQUIRED
- [Backstage system model](https://backstage.io/docs/features/software-catalog/system-model/)

### RECOMMENDED
- [Backstage descriptor format](https://backstage.io/docs/features/software-catalog/descriptor-format/)

### DEEP DIVE
- [CNCF Platforms whitepaper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

## Next

[Templates and self-service workflows](02-templates-and-workflows.md)
