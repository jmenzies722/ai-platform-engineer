# Facilitator solution: RAG Corpus Poisoning or ACL Bypass

This is one evidence-supported path. Learners should change course if their
tests produce different evidence.

## Diagnosis

The primary disclosure mechanism is an ACL bypass in retriever cache revision
deployed at 08:40. The cache key represents classification but omits tenant and
principal security context. On a cache hit, the batch authorization call checks
the requested result count against the request-level policy but does not bind
each chunk's resource owner to the decision. A cached `nova-labs` chunk is
therefore returned to `acme-demo`.

`doc-acme-44` is genuine corpus poisoning and should be contained, but it does
not explain the foreign chunk. It is a concurrent control failure and a
deliberate distractor, not the disclosure's primary cause.

## Evidence-led reasoning

1. `chk-91d` resolves to `doc-nova-7`, whose metadata owner is `nova-labs`.
2. The requesting tenant is `acme-demo`, while direct source authorization
   correctly denies access for tenant mismatch.
3. The requested filter includes tenant ownership, but cached filter `f98c`
   omits it. The high cache-hit ratio and incident timing align with the cache
   rollout.
4. The retrieval authorization log records a batch count, not per-resource
   decision bindings. An `allow` line therefore does not prove each chunk was
   authorized.
5. The flagged poisoned document belongs to the requesting tenant. It can
   manipulate model behavior but cannot account for retrieving a foreign
   document.

The critical distinction is between content integrity and access control. A
response filter cannot repair disclosure after unauthorized text has entered
the model context.

## Discriminating investigation

| Test | Expected result | Conclusion supported |
|---|---|---|
| Replay `req-7f2` with cache bypass | Only `acme-demo` chunks return | Cache path is causal |
| Compare cache keys for two tenants with equal classification | Keys collide | Security context is omitted |
| Authorize each result by resource ID | `doc-nova-7` is denied | Batch check is insufficient |
| Remove `doc-acme-44` and replay cache hit | Foreign chunk still returns | Poisoning is not needed for disclosure |
| Replay poisoned content with tenant-safe retrieval | Model behavior may change, no foreign source appears | Separate content-integrity failure |

If cache bypass still returns foreign chunks, investigate index metadata and
filter construction before accepting this solution.

## Decision analysis

Deleting suspicious content alone leaves the disclosure path open. Rebuilding
the full index is slow, destroys useful state, and does not fix an unsafe cache
key. Disabling the assistant globally contains impact but has unnecessary blast
radius if the retrieval tier can deny unsafe results.

The preferred bounded action is to bypass shared cache reads, enforce
resource-level authorization after candidate retrieval, and fail closed on
missing or mismatched ownership. Quarantine `doc-acme-44` under a separate
incident workstream so concurrent poisoning evidence remains intact.

## Mitigation sequence

1. Freeze retriever and ingestion deployments. Record image digest, cache
   revision, policy revision, and index generation.
2. Preserve the affected cache metadata, authorization decisions, chunk
   provenance, and request IDs in access-controlled evidence storage. Do not
   preserve response text unless approved by privacy and security owners.
3. Disable cache reads for one affected tenant and enable per-resource
   authorization. Compare with a control using synthetic probes.
4. Expand to all tenants when foreign-chunk count is zero and latency and error
   guardrails hold. Block answers whose citations lack a matching allow
   decision.
5. Evict unsafe cache entries only after evidence preservation. Keep writes
   disabled until corrected key isolation tests pass.
6. Quarantine the poisoned document and inspect its ingestion path without
   conflating it with the ACL root cause.
7. Start the applicable privacy, legal, and customer-notification procedure
   using the bounded recipient and resource inventory.

Rollback only the latency-increasing enforcement change if it breaches the
declared service threshold; retain fail-closed ownership checks. If capacity
cannot support safe retrieval, disable retrieval for the affected cohort rather
than fail open.

## Recovery proof

- Cross-tenant probes across cache hit and miss paths return zero unauthorized
  chunks for `<full probe interval>`.
- Audit joins show one resource-bound allow decision for every generated
  citation.
- The affected request inventory is stable across two independent queries.
- Direct document access and assistant retrieval agree for sampled principals.
- Poisoned-content probes cannot override instructions or trigger access to
  unauthorized sources.
- Temporary cache and ingestion controls are tracked and removed only after
  replacement controls are verified.

## Prevention plan

| Control | Acceptance evidence |
|---|---|
| Security-context cache isolation | Property tests show no collision across tenant, principal, policy revision, filter, and index generation |
| Resource-level authorization | Every candidate has a decision ID bound to principal and resource; missing decisions deny |
| End-to-end provenance | Source owner, chunk digest, index generation, and citation are cryptographically or immutably linked |
| Poison-content quarantine | Adversarial ingestion suite is quarantined before indexing with measured false-positive handling |
| Continuous isolation canary | Cross-tenant retrieval alert pages before any synthetic canary receives foreign content |
| Evidence readiness | Quarterly exercise produces a recipient and resource inventory without exposing document text |

## Debrief guide

- Ask who treated `decision=allow` as proof without checking decision
  granularity.
- Ask whether the poisoning alert anchored the team on a vivid but incomplete
  explanation.
- Verify that containment did not copy sensitive text into lower-control
  systems.
- Separate the trigger, unsafe cache design, missing result-level enforcement,
  and detection gaps in the causal analysis.

## Authoritative sources

- [NIST AI Risk Management Framework Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [OWASP Top 10 for LLM Applications: Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm08-vector-and-embedding-weaknesses/)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [NIST SP 800-53 Rev. 5, Access Control and Audit controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
