# Incident: DNS Resolution Failure

> **Scenario status:** Starter scaffold. Investigate before opening [solution.md](solution.md).

## Situation

At 14:07 UTC, requests from one application environment begin failing for `api.internal.example`. Existing connections continue briefly, but new connections fail. The application itself is healthy and no deployment was reported.

## User Impact

Requests requiring the dependency fail or time out. Quantify scope and duration from the evidence you create during the exercise.

## Symptoms

- Application error rate rises for new dependency calls.
- Direct IP connectivity may still work.
- Behavior may differ between hosts because cache and resolver state differ.

## Available Evidence

Replace placeholders with outputs from your own safe local simulation or instructor-provided environment.

### Application log

```text
<timestamp> ERROR dependency request failed host=api.internal.example error=<resolver error>
```

### Resolver configuration

```text
$ cat /etc/resolv.conf
<capture output>
```

### Query evidence

```text
$ getent hosts api.internal.example
<capture output>

$ dig api.internal.example
<capture output>
```

### Network evidence

```text
$ ip route
<capture relevant output>
```

## Constraints

- Do not modify shared DNS infrastructure.
- Simulate with a disposable namespace, container, VM, or test hostname you control.
- Do not use public domains for destructive experiments.
- Preserve the exact resolver error; “DNS is down” is not a diagnosis.

## Your Tasks

1. State impact and identify what is known versus inferred.
2. Draw the resolution path: application → resolver library/cache → configured resolver → authoritative chain.
3. Write at least three plausible hypotheses.
4. For each hypothesis, choose a discriminating test and expected result.
5. Identify the earliest failing boundary.
6. Propose the lowest-risk mitigation.
7. Define user-visible recovery checks and monitoring improvements.

## Investigation Record

| Hypothesis | Supporting evidence | Contradicting evidence | Test | Result |
|---|---|---|---|---|
|  |  |  |  |  |

## Timeline

| Time (UTC) | Observation / action | Result |
|---|---|---|
| 14:07 | Alert or report received |  |

## Completion Criteria

- [ ] Resolution path and cache boundaries are explicit.
- [ ] Tests distinguish name resolution from routing, TCP, TLS, and application failure.
- [ ] Mitigation does not create an unmanaged permanent bypass.
- [ ] Recovery is verified at both DNS and user-request layers.
- [ ] Prevention addresses the causal mechanism, not only the symptom.

After completing the record, compare your work with [solution.md](solution.md).
