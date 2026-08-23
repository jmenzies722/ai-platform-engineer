# Lab: test identity and application boundaries

Build a local authorization boundary, attack it with cross-tenant and injection-shaped input, and use structured evidence to diagnose and correct the defects.

## Goal

Produce a small policy-enforced document service whose tests prove tenant isolation, parameterized storage, secret-safe logging, and a bounded incident record.

## Before you start

Read lessons 1, 2, 4, 6, and 7. Use Python 3 and SQLite in a temporary directory; use only synthetic identities and secrets. No network, account, privilege, or cost is required. Stop if any real credential appears. Predict each allow and deny result.

## Establish a baseline

`python3 --version` must show Python 3. Create two tenants, one user each, and one document each. Assert each user reads only its own document and logs contain decision metadata without content.

## Make it work

Implement lookup with a parameterized SQLite query and derive tenant from authenticated test context, not request parameters. Emit JSON decisions with actor, action, resource, outcome, policy version, and correlation ID. Add negative tests for cross-tenant IDs and injection-shaped strings.

## Break it

Change lookup to trust a request-supplied tenant. The expected symptom is a cross-tenant read while authentication still appears successful. Capture only synthetic evidence.

## Diagnose it

Start from the isolation invariant, compare trusted actor tenant with requested resource owner, and inspect the authorization decision. Restore server-side ownership enforcement and rerun all negative tests. Prove denied attempts are visible and no document body or fake secret enters logs.

## Clean up

Delete the temporary database, program, and logs. Search the temporary directory before deletion for the synthetic secret and confirm only the intentionally controlled test fixture contained it.

## What to keep

Keep predictions, test output, failed boundary assumption, policy correction, and a redacted incident timeline. Explain how the same defect would be contained by cloud identity, database policy, and detection as independent layers.

## Sources

- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
