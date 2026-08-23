# Tool contracts and secure execution

A tool call is an untrusted proposal crossing into ordinary software; typed parsing is only the first control.

## Why it matters

[RAG pipeline engineering](04-rag-pipeline-engineering.md) supplies information. Tools add side effects, money movement, private reads, and retry hazards that model confidence cannot authorize.

## How it works

A tool schema defines operation and typed arguments. The host parses output, rejects unknown fields, validates semantic constraints, authenticates the caller, authorizes the exact resource and action, applies rate and spend limits, and executes with least privilege. Tool results are bounded, provenance-labeled, and treated as untrusted input on return.

Read and write capabilities should be separate. Consequential writes use preview and approval tied to an immutable action digest. Idempotency keys make identical retries converge on one effect; they do not make two semantically different requests equivalent. Timeouts and cancellation must account for effects that may have completed after the caller stopped waiting.

Tool descriptions and retrieved text can contain hostile instructions. Policy comes from trusted application code, not context priority invented by a model. Secrets remain inside executors and never enter prompts or traces.

## See it yourself

A model proposes `transfer(account="A", amount=-100)`. JSON schema may accept a number, but semantic validation rejects a nonpositive amount. Then try the same valid request twice with one idempotency key; the ledger should contain one effect and two response records.

The example proves syntax, semantics, authorization, and retry control are distinct gates.

## Where it shows up

A support assistant may draft a refund, but a service checks order ownership, refundable balance, policy version, actor role, approval threshold, and idempotency record. Audit logs capture decision metadata and redact payment data.

## When it breaks

Over-broad credentials bypass tenant isolation, retries duplicate writes, partial failure creates ambiguity, and verbose tool output causes injection or context exhaustion. Approval can become stale if the underlying resource changes.

Trace proposal ID, caller, policy decision, validated digest, approval, execution ID, idempotency result, and final status. On timeout, query operation status before retrying. Reauthorize at execution time.

## Practice

**Observe:** classify schema, semantic, authorization, and business-rule checks. **Build:** create a mock ledger tool with preview and idempotency. **Break:** time out after commit and prove retry does not duplicate the effect.

## Check yourself

1. Why is valid JSON not authorization?
2. What must an approval bind to?
3. How should a timeout after a write be handled?
4. Why must tool output remain untrusted?

## Sources

### REQUIRED

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)

### RECOMMENDED

- [JSON Schema specification](https://json-schema.org/specification)

### DEEP DIVE

- [Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests)

## Next

Continue to [Agents and bounded workflows](06-agents-and-bounded-workflows.md).
