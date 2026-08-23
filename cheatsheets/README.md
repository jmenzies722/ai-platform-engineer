# Operator sheets

Compact decision aids for diagnosis and controlled change. They are not command
catalogs, runbooks, or substitutes for understanding the system.

| Sheet | Use it to decide |
|---|---|
| [Linux](linux.md) | Whether pressure, storage, a process, or a service is the first broken layer |
| [Git](git.md) | What state differs, whether work is recoverable, and which integration action is safe |
| [Networking](networking.md) | Whether failure begins at naming, routing, transport, TLS, HTTP, or the application |
| [Kubernetes](kubernetes.md) | Whether desired state, scheduling, startup, service routing, or capacity is failing |
| [AWS](aws.md) | Which identity, region, resource, dependency, or audit event explains a symptom |
| [OpenTelemetry](opentelemetry.md) | Whether telemetry was created, propagated, exported, accepted, and made queryable |

## Operating model

1. State the user-visible symptom, start time, scope, and recent changes.
2. Confirm identity, target, environment, and time window before every query.
3. Prefer bounded, read-only observations. Record command, timestamp, and output.
4. Form one falsifiable hypothesis and choose the cheapest discriminating check.
5. Before mutation, define success evidence, blast radius, rollback, and owner.
6. Change one variable. Re-run the same observation and watch for collateral harm.
7. Escalate when authority, evidence, or rollback confidence is insufficient.

## Safety labels

- **Read-only**: intended not to change remote or durable state. It can still be
  expensive, disclose sensitive data, or load a production API.
- **Local mutation**: changes only the current workstation or repository.
- **Remote mutation**: changes shared or production state. Use only through the
  applicable runbook and approval path.
- **Privilege**: requires elevated OS or cloud permissions. Do not bypass denied
  access; preserve the denial as evidence.

Examples use placeholders such as `<namespace>` and `<resource-id>`. Never paste
credentials, tokens, customer data, or unredacted telemetry into tickets.

## Stop conditions

Stop and escalate when the target is ambiguous, evidence conflicts, the incident
crosses a security or data-loss boundary, an action lacks a tested rollback, or
continued probing may amplify load. During an incident, the incident commander
and service runbook override these generic sheets.

All examples assume currently supported tool versions. Check each sheet's
authoritative sources when flags or platform semantics may differ.
