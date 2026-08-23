# RAG pipeline engineering

Retrieval-augmented generation is a measurable information pipeline: ingest, authorize, retrieve, rerank, assemble context, answer, and cite.

## Why it matters

[Evaluation, safety, and cost](03-evaluation-safety-and-cost.md) defines application evidence. A grounded answer can still be wrong because the needed source was absent, stale, unauthorized, truncated, or misused.

## How it works

Ingestion parses documents, preserves structure and provenance, chunks content, computes sparse or dense representations, and writes an index version. Query processing may rewrite the request, apply tenant and identity filters, retrieve candidates, fuse lexical and semantic ranks, rerank, and pack evidence within a token budget.

Retrieval recall asks whether supporting evidence appeared among candidates. Context precision asks how much selected material is relevant. Answer faithfulness asks whether claims follow from supplied evidence. Answer correctness is separate because a faithful source can itself be stale or wrong.

Chunk boundaries should preserve meaningful units and parent context. Hybrid search protects exact identifiers while embeddings recover paraphrases. Access control is enforced before model context, and citations bind to immutable source versions and exact spans.

## See it yourself

Index three passages: one exact product code, one semantic paraphrase, and one restricted policy. Lexical search wins the code query; semantic search wins the paraphrase. A fused rank can recover both, but the restricted passage must be removed regardless of score.

This fixture proves relevance and authorization are independent. It does not prove the generated claim follows from the allowed passage.

## Where it shows up

An incident assistant retrieves runbooks by service, environment, and caller access, cites commit and heading, and abstains when no supporting span clears a threshold. Traces preserve candidates and filters without storing prohibited document bodies.

## When it breaks

OCR drops negation, chunks separate exceptions, index updates lag, embeddings change without reindexing, and prompt injection arrives inside documents. Large context can bury the best evidence.

For a wrong answer, inspect in order: corpus presence, parser output, ACL filter, candidate recall, reranker, packed spans, then claim support. This stage-wise trace prevents prompt tuning from masking retrieval defects.

## Practice

**Observe:** label retrieval and generation failures separately. **Build:** implement hybrid retrieval over ten documents with span citations and ACLs. **Break:** separate a policy exception from its rule and repair chunk context.

## Check yourself

1. Why is faithfulness different from correctness?
2. Where must access control run?
3. Which metric isolates candidate retrieval?
4. How can extra context reduce answer quality?

## Sources

### REQUIRED

- [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)

### RECOMMENDED

- [Sentence Transformers retrieve and rerank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)

### DEEP DIVE

- [Lost in the Middle](https://arxiv.org/abs/2307.03172)

## Next

Continue to [Tool contracts and secure execution](05-tool-contracts-and-secure-execution.md).
