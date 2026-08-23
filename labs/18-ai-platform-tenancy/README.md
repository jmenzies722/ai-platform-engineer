# Lab: Verify AI Platform Tenant Isolation

Design and test tenant boundaries across prompts, retrieval, model routing, quotas, caches, telemetry, and usage accounting with a local SQLite policy harness.

## Prerequisites

- Python 3.10 or newer with SQLite and Bash
- No model API, embeddings, credentials, or network access
- Familiarity with authentication, authorization, and data classification

## Safety

Use only fictional tenants and synthetic text. Never put real prompts, documents, tokens, API keys, or model outputs into fixtures. The harness performs at most 100 policy decisions and makes no external calls.

## Setup and baseline

```bash
mkdir -p .work
python3 - <<'PY'
import sqlite3
db=sqlite3.connect(".work/tenancy.db")
db.executescript("""
create table documents(tenant text not null, document_id text not null, body text,
 primary key(tenant, document_id));
create table usage(tenant text not null, request_id text not null, input_tokens int,
 output_tokens int, primary key(tenant, request_id));
insert into documents values
 ('acme','shared-name','acme synthetic policy'),
 ('beta','shared-name','beta synthetic policy');
""")
db.commit()
PY
```

Define the reference monitor invariant: authenticated tenant identity is server-derived, immutable through the request, and included in every storage, cache, queue, and accounting key.

## Tasks

1. Write `.work/policy.md` covering control-plane roles, data-plane identity, service identity, model entitlements, regional constraints, retention, encryption context, and break-glass audit.
2. Implement `.work/harness.py`. It accepts a server-supplied principal and performs parameterized queries requiring both tenant and resource ID. The request body may not override tenant.
3. Add at least twenty allow/deny tests for document retrieval, prompt-template access, vector namespace, response cache, model route, quota bucket, usage row, trace access, evaluation dataset, and deletion.
4. Use identical resource names in two tenants to prove tenant identity is part of the key.
5. Specify cache keys that include tenant, model/version, policy version, retrieval corpus version, and normalized input hash. Never persist raw sensitive prompts in keys.
6. Test quota and accounting idempotency by replaying one request ID. Usage must be counted once for the authenticated tenant.
7. Document telemetry redaction and how support access is approved, time-bounded, attributed, and reviewed.

## Evidence to keep

Keep policy, schema, synthetic fixtures, test source and results, deny-by-default cases, cache-key design, accounting replay result, audit fields, and residual risks. Evidence should contain no raw production prompts or cross-tenant identifiers.

## Failure injection

Create an intentionally vulnerable query in a test-only function: select by `document_id` without tenant. The duplicate ID should return two rows and the test must fail closed. Correct it with a tenant predicate and verify exactly one authorized row.

Also omit tenant from a cache-key fixture. Two synthetic tenants using the same prompt hash must trigger a collision assertion before any value is returned.

## Cleanup

```bash
rm -rf .work
```

## Rubric

- 2 points: defines immutable server-derived tenant identity
- 3 points: tests isolation across storage, retrieval, cache, routing, and telemetry
- 2 points: proves accounting idempotency and tenant-scoped quotas
- 2 points: catches missing predicates and cache-key collisions fail closed
- 1 point: uses only synthetic data and removes the database

## Sources

- [NIST SP 800-207, Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
