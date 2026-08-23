# Lab: test identity and application boundaries

Build a local authorization boundary, attack it with cross-tenant and injection-shaped input, and use structured evidence to diagnose and correct the defects.

## Goal

Produce a small policy-enforced document service whose tests prove tenant isolation, parameterized storage, secret-safe logging, and a bounded incident record.

## Before you start

Read lessons 1, 2, 4, 6, and 7. Use Python 3 and SQLite in a temporary directory; use only synthetic identities and secrets. No network, account, privilege, or cost is required. Stop if any real credential appears. Predict each allow and deny result.

## Establish a baseline

`python3 --version` must show Python 3. Create an isolated database and program path:

```bash
mkdir -p /tmp/security-boundary-lab
python3 - <<'PY'
import sqlite3
path = "/tmp/security-boundary-lab/documents.db"
db = sqlite3.connect(path)
db.execute("create table documents (id text primary key, tenant text not null, body text not null)")
db.executemany("insert into documents values (?, ?, ?)", [
    ("doc-a", "tenant-a", "synthetic-alpha"),
    ("doc-b", "tenant-b", "synthetic-bravo"),
])
db.commit()
assert db.execute("select count(*) from documents").fetchone()[0] == 2
print("baseline database ready")
PY
```

This establishes only the starting data. Write down four predictions: each owner read, one cross-tenant read, and one injection-shaped ID.

## Make it work

Save `/tmp/security-boundary-lab/service.py`:

```python
import json
import sqlite3

DB = "/tmp/security-boundary-lab/documents.db"
USERS = {"alice": "tenant-a", "bob": "tenant-b"}

def read_document(actor, document_id):
    tenant = USERS[actor]
    row = sqlite3.connect(DB).execute(
        "select body from documents where id = ? and tenant = ?",
        (document_id, tenant),
    ).fetchone()
    event = {
        "actor": actor, "action": "document.read", "resource": document_id,
        "outcome": "allow" if row else "deny", "policy_version": "1",
        "correlation_id": f"test-{actor}-{document_id[:8]}",
    }
    print(json.dumps(event, sort_keys=True))
    return row[0] if row else None

assert read_document("alice", "doc-a") == "synthetic-alpha"
assert read_document("alice", "doc-b") is None
assert read_document("bob", "doc-b") == "synthetic-bravo"
assert read_document("alice", "' or 1=1 --") is None
```

Run `python3 /tmp/security-boundary-lab/service.py | tee /tmp/security-boundary-lab/audit.jsonl`. Confirm all assertions pass and the audit stream contains decisions but no document bodies.

## Break it

Change the function signature to accept `requested_tenant`, use it in the query instead of `USERS[actor]`, and call `read_document("alice", "doc-b", "tenant-b")`. The expected symptom is a cross-tenant read while authentication still appears successful. This is the only injected fault. Capture only synthetic evidence.

## Diagnose it

Start from the isolation invariant, compare trusted actor tenant with requested resource owner, and inspect the authorization decision. The `allow` event for Alice and `doc-b` proves the policy decision is wrong; successful authentication is irrelevant to resource authorization. Restore server-side ownership enforcement, rerun all tests, then use `! rg 'synthetic-(alpha|bravo)' /tmp/security-boundary-lab/audit.jsonl` to prove bodies were not logged.

## Clean up

The document bodies are synthetic fixtures, not secrets. Confirm they occur only in the database and source assertions, then remove all artifacts:

```bash
rm -rf /tmp/security-boundary-lab
test ! -e /tmp/security-boundary-lab
```

## What to keep

Keep predictions, test output, failed boundary assumption, policy correction, and a redacted incident timeline. Explain how the same defect would be contained by cloud identity, database policy, and detection as independent layers.

## Sources

- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
