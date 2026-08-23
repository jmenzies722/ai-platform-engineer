# Templates and self-service workflows

Templates should start a service safely; workflows should continue managing it throughout its life.

## Why it matters

Generated code diverges immediately. A template that only creates repositories moves maintenance burden to every team and cannot safely handle retries.

## How it works

Collect the minimum user intent, validate early, show a plan, execute idempotent steps, record outputs, and support resume after failure. Separate template content from provisioned capabilities. Generated projects should consume versioned libraries, actions, modules, and policy that can evolve centrally.

Workflows need scoped identity, audit records, timeouts, compensation or reconciliation, and clear ownership. Destructive actions require stronger confirmation and dependency checks. Treat workflow definitions and migrations as production software.

## See it yourself

If repository creation succeeds but database provisioning times out, retry must discover the existing repository rather than fail or create a duplicate.

## Where it shows up

Service creation, environment provisioning, access requests, migrations, certificate rotation, and retirement.

## When it breaks

Credentials belong to the portal, operations are not idempotent, users cannot see partial state, or template upgrades require regenerating and overwriting application code.

## Practice

Design a resumable create-service workflow. Specify intent, validations, identities, step state, outputs, retry rules, and cleanup.

## Check yourself

1. Why prefer centrally versioned dependencies over copied boilerplate?
2. What must a workflow retain after partial failure?

## Sources

### REQUIRED
- [Backstage Software Templates](https://backstage.io/docs/features/software-templates/)

### RECOMMENDED
- [CNCF Platforms whitepaper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

### DEEP DIVE
- [Temporal durable execution](https://docs.temporal.io/temporal)

## Next

[Golden paths and developer experience](03-golden-paths-and-experience.md)
