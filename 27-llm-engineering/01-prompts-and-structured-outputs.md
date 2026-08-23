# Prompts and structured outputs

Prompts are versioned inputs to a probabilistic component; schemas turn some of their output into a testable interface.

## Why it matters

Natural-language instructions alone are ambiguous. Downstream code needs explicit contracts and safe failure behavior.

## How it works

Separate trusted instructions from untrusted content, state the task and constraints, and request the smallest output needed. Validate structured output against a schema, reject unknown fields, and retry only bounded, recoverable failures. Treat model output as data, never executable authority.

Instruction hierarchy reduces ambiguity but does not create a security boundary: the model still processes trusted and untrusted tokens together. Delimiters and explicit provenance help the model distinguish roles; deterministic code must enforce permissions. Schemas constrain syntax and shape, while semantic validators enforce relationships such as confidence range, known identifiers, or totals.

Retries should classify failures. A transient transport error may repeat unchanged; malformed output may justify one repair attempt; a semantically unsupported answer needs different context or abstention. Every retry spends latency and tokens and can repeat a side effect if orchestration is careless.

## See it yourself

Define a schema with `category` limited to `billing|technical|other`, confidence from 0 to 1, and a bounded rationale. Validate `{"category":"billing","confidence":0.8,"rationale":"invoice mentioned"}`. Then test a missing rationale, confidence 8, an unknown category, an extra `command` field, and prose around JSON. The expected result is one acceptance and five explicit rejections, proving structural validation is fail-closed while saying nothing about factual classification.

## Where it shows up

In ticket routing, validated output becomes a queue choice. The service preserves the original ticket, prompt version, parsed result, validation result, and fallback. Low confidence can route to triage instead of forcing a category. The model proposes classification; queue authorization and supported destination IDs remain application responsibilities.

## When it breaks

Prompt injection crosses trust boundaries, schemas drift, retries multiply cost, and confident fields can still be semantically wrong. For malformed-output spikes, first compare raw responses, schema version, model revision, and finish reason. For plausible but wrong fields, inspect source evidence and slice errors rather than loosening validation. For unexpected actions, trace where output gained authority; do not attempt to “patch” authorization with stronger wording.

## Practice

**Build:** implement a prompt contract with size limits, schema validation, timeout, one fallback, and logged version metadata. Completion requires deterministic tests for every schema branch.

**Break:** embed contrary instructions in the user content and return an unknown destination plus an extra command field. Demonstrate that no unauthorized action executes.

**Explain back:** distinguish prompt instruction, schema validation, semantic validation, and authorization, naming what each can and cannot guarantee.

## Check yourself

1. What does schema validation prove?
2. Why delimit untrusted text?
3. When should a retry stop?

## Sources

### REQUIRED

- [OpenAI structured outputs](https://platform.openai.com/docs/guides/structured-outputs)

### RECOMMENDED

- [OWASP LLM Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

### DEEP DIVE

- [JSON Schema specification](https://json-schema.org/specification)

## Next

Continue to [Retrieval and tool use](02-retrieval-and-tool-use.md).
