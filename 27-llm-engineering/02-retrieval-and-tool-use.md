# Retrieval and tool use

Retrieval supplies evidence; tools let a model request computation or side effects. Neither makes the model itself authoritative.

## Why it matters

Most useful assistants need current private data or actions, which creates security and correctness boundaries beyond prompting.

## How it works

A retrieval pipeline chunks, indexes, searches, reranks, and cites source material. Tool use parses a proposed call, validates arguments, authorizes it independently, executes with least privilege, and returns a bounded observation. Side effects need idempotency and, when consequential, human approval.

Chunk size trades local focus against lost context. Lexical search preserves exact terms; embedding search recovers semantic similarity but can miss identifiers and blur distinctions. Hybrid retrieval and reranking combine signals. Access control must filter candidates using the caller's identity before content enters model context, and citations must identify the actual version retrieved.

A tool definition is a capability surface. Typed arguments reduce ambiguity, but the executor still validates ranges, object ownership, and current authorization. Results should be bounded and labeled as untrusted observations. Planning and execution remain separate so model output cannot silently widen its own privileges.

## See it yourself

Create five documents: two mention “PTO,” one says “paid time off,” one contains an unrelated product named PTO, and one is restricted. Query exact “paid time off,” then “PTO policy.” Record rank, access decision, and supporting span. Lexical search should miss the paraphrase or over-rank the product; semantic search may recover it but must still exclude the restricted document. The result demonstrates why relevance and authorization are independent filters.

## Where it shows up

An internal support assistant retrieves policy paragraphs visible to the employee, cites document version and section, and may propose opening a case. A case-creation service independently checks employee identity, category, and idempotency key before writing. Retrieval grounds the response; it does not grant case-system authority or prove that the selected passage is current.

## When it breaks

Chunks lose context, stale indexes mislead, retrieved text injects instructions, and tools execute duplicate or over-broad actions. For a wrong grounded answer, first preserve query, candidate IDs and scores, ACL decisions, reranker output, cited spans, and index version. If the right passage never appeared, debug retrieval; if it appeared but was ignored, debug generation. For duplicate actions, inspect idempotency records before retry behavior.

## Practice

**Build:** implement retrieval over five documents with source IDs and an allow-list, plus a mock side-effect tool that requires an idempotency key.

**Break:** add a restricted relevant document and an injected instruction inside an allowed document; retry the same tool request twice. Prove no restricted text enters context and only one effect occurs.

**Explain back:** trace relevance, authorization, grounding, approval, and execution as separate decisions and identify the first trace needed for a wrong answer.

## Check yourself

1. Why is retrieved text untrusted?
2. Where should authorization occur?
3. What makes a tool retry safe?

## Sources

### REQUIRED

- [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)

### RECOMMENDED

- [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling)

### DEEP DIVE

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)

## Next

Continue to [Evaluation, safety, and cost](03-evaluation-safety-and-cost.md).
