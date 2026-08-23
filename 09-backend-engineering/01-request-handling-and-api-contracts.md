# Request Handling and API Contracts

A backend translates an external request into validated domain work and an explicit response contract.

## Why it matters

An API can return 200 while failing to perform the requested work, or expose an internal traceback for malformed input. Both are contract failures even if the handler process stays healthy. Engineers deciding where to validate and how to classify errors need a boundary that separates transport concerns from domain rules and dependency failures.

## How it works

An HTTP handler parses method, path, headers, and body; authenticates identity; validates input; invokes domain logic; and maps results or failures to status, headers, and a body. Keeping transport concerns at the edge makes core behavior testable without a server.

A server accepts a connection, parses protocol bytes into an HTTP request, selects a route, and invokes handler code with method, target, headers, identity context, and body. The transport boundary must reject malformed syntax and unsupported media types before domain work. Authentication establishes an identity claim; authorization decides whether that identity may perform this operation. Domain validation then checks business invariants independent of HTTP. The handler coordinates dependencies and maps outcomes into a status, headers, and representation. A 4xx response attributes a correctable problem to the request under the API contract, while 5xx indicates the server did not fulfill a valid request; exact choices require documented semantics. Keeping domain functions free of framework request objects allows direct tests and reuse from jobs or other protocols.

## See it yourself

Predict one normalized success result with status-like 201 and one explicit invalid-input result with 400. No database or network setup should be needed because the function models the inner contract.

```bash
python3 - <<'PY2'
def create_user(payload):
    email=payload.get('email','').strip().lower()
    if '@' not in email: return 400, {'error':'invalid email'}
    return 201, {'email':email}
print(create_user({'email':' A@EXAMPLE.COM '}))
print(create_user({}))
PY2
```

Expected observation: Normalization and validation happen before persistence, and each outcome has an explicit status-like result.

Limits of the request handling and api contracts observation: The example does not implement HTTP parsing, authentication, persistence, uniqueness, or concurrent requests. It proves only two pure branches of a proposed handler policy.

## Where it shows up

A user-creation endpoint demonstrates the layered boundary. The edge limits body size and parses JSON, authentication identifies the caller, domain code normalizes email and checks policy, and a repository attempts an atomic insert under a unique constraint. A duplicate maps to a stable conflict response; a database outage maps differently and retains internal diagnostics. Clients can then react to the contract without learning schema or stack details.

## When it breaks

A 400 with no handler log suggests rejection at proxy or parser; 401/403 points toward identity policy; 409 suggests a state conflict; 500 with a traceback points toward uncaught application or dependency failure. First capture method, sanitized target, request ID, response status, and the boundary log that last accepted the request. Reproduce with the smallest non-sensitive payload and do not log credentials or full personal data merely to gain context.

## Practice

**Build:** implement a pure create-user function and a thin adapter that maps malformed input, conflict, success, and dependency failure to documented outcomes. **Break:** send missing, oversized, duplicate, and unexpected-dependency cases, preserving request IDs. **Explain back:** identify parsing, authentication, authorization, domain, persistence, and response mapping in one request. Success means contract tests assert status and schema while domain tests run without an HTTP server.

## Check yourself

1. Which validation belongs at the transport boundary?
2. Why should domain logic avoid HTTP-specific types?

## Sources

### REQUIRED

- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)

### RECOMMENDED

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)

### DEEP DIVE

- [Patterns of Enterprise Application Architecture](https://martinfowler.com/books/eaa.html)

## Next

Continue to [State, Idempotency, and Background Work](./02-state-idempotency-and-background-work.md).
