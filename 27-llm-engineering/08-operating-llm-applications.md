# Operating LLM applications

LLM operations balance quality, safety, latency, availability, and spend while upstream models and traffic evolve.

## Why it matters

[LLM application evaluations](07-llm-application-evaluations.md) supports release. Production adds queues, rate limits, provider changes, delayed outcomes, abuse, and costs that offline tests cannot simulate completely.

## How it works

Define service-level indicators for availability, time to first token, inter-token latency, task completion, fallback and refusal rates. Trace model and prompt revision, retrieval index, tool calls, token counts, cache status, finish reason, policy decisions, and cost without logging secrets or unnecessary user content.

Budgets are enforced before and during work: maximum input and output tokens, retrieval count, tool actions, wall time, retries, and currency. Cache only where identity, permissions, model settings, freshness, and privacy permit reuse. Route by task and risk; a smaller model may handle classification while a stronger path handles rare ambiguity.

Release with offline gates, shadow traffic, canary, bounded ramp, and rollback. Provider drift requires contract tests and pinned versions where available. Graceful degradation can disable tools, use stale-but-labeled data under policy, route to humans, or return a clear failure.

## See it yourself

At $3 per million input tokens and $12 per million output tokens, a request with 8,000 input and 1,000 output tokens costs $0.036 before retrieval and tools. A retry doubles model cost unless cached or deduplicated. At 100,000 requests, that is $3,600.

This arithmetic shows why token distributions and retries matter more than a single average price.

## Where it shows up

A production assistant tags every trace with an application release manifest. Alerts combine error budget, safety invariant failures, quality proxies, token spend, and provider status. Operators can disable one tool or route without redeploying unrelated code.

## When it breaks

Retry storms amplify provider errors, unbounded context drives cost, semantic caches cross users, fallbacks change safety behavior, and content logging leaks data. Average latency hides long-generation tails.

Start with request waterfall and release identity. Separate queue, retrieval, provider prefill, decode, tool, and retry time. For spend anomalies, decompose requests, input tokens, output tokens, retries, and route mix.

## Practice

**Observe:** calculate cost at median and p99 token counts. **Build:** define an SLO and trace schema with redaction. **Break:** simulate a retry storm and enforce one total attempt and spend budget.

## Check yourself

1. Why is token count a capacity and cost signal?
2. What belongs in a safe cache key?
3. How can a fallback violate policy?
4. Which trace separates provider latency from queueing?

## Sources

### REQUIRED

- [Google SRE: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)

### RECOMMENDED

- [OpenTelemetry tracing specification](https://opentelemetry.io/docs/specs/otel/trace/)

### DEEP DIVE

- [AWS Builders' Library: Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

## Next

Continue to [Safe assistant lab](lab-safe-assistant.md).
