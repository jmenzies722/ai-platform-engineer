# Lab: Build and Diagnose a Bounded AWS Telemetry Pipeline

This lab makes a small CloudWatch Logs pipeline observable from ingestion through query and alarm evaluation. It closes the AWS-specific practice gap behind DOP-C02 monitoring tasks without claiming that a synthetic stream proves production readiness.

## Goal

Create an encrypted log group with explicit retention, derive a bounded custom metric from structured request events, find a synthetic fault with Logs Insights, alarm on a user-impact proxy, and prove that missing telemetry is not the same as health.

### DOP-C02 task mapping

| Direct task ID | Direct lab evidence |
|---|---|
| 4.1 | Log group encryption choice, retention, structured ingestion, metric filter, and cost worksheet |
| 4.2 | Fault query, alarm history, missing-data state, bounded diagnosis, and recovery |

The alarm workflow supports discussion of task 4.3, and the fault investigation supports discussion of task 5.3. This one-group synthetic exercise does **not** prove automated monitoring or troubleshooting in a complex, multi-account, multi-Region, or production environment; it is not direct completion evidence for 4.3 or 5.3.

Canonical preparation: [AWS operations and observability](../../12-aws/05-operations-and-observability.md), [metrics](../../18-observability/03-metrics.md), [structured logs](../../18-observability/04-logs.md), [telemetry cost](../../18-observability/06-cardinality-and-cost.md), and [evidence-led diagnosis](../../18-observability/07-instrumentation-and-diagnosis.md).

## Before you start

### Identity and environment assumptions

- Use AWS CLI v2 with temporary credentials in an **authorized, disposable sandbox account**. Do not run this lab in production, a shared operations account, or an account containing customer data.
- The caller may use `sts:GetCallerIdentity`; create, describe, write, query, and delete the named CloudWatch Logs resources; and create, inspect, and delete the named CloudWatch alarm. It does not need IAM mutation, application deployment, or access to unrelated log groups.
- Commands are scoped by the unique `LAB_ID`, one Region, one log group, one stream, one metric namespace, and one alarm. Do not replace those names with wildcards in a reusable policy.
- The local-only path needs Bash, Python 3, and `jq`; it uses no AWS identity and is static evidence only.

This lab deliberately chooses CloudWatch Logs' default service-managed encryption at rest. It does **not** associate a customer managed KMS key. A missing `kmsKeyId` in `describe-log-groups` proves that choice, not absence of encryption. If policy requires a customer managed key, stop and use an approved key whose policy permits CloudWatch Logs for this Region; key creation and key-policy editing are outside this lab.

### Bounds, cost, and stop conditions

| Bound | Limit |
|---|---|
| Expected time | 60 to 90 minutes, including alarm evaluation |
| Regions | Exactly one, recorded as `REGION` |
| Resources | 1 log group, 1 stream, 1 metric filter/custom metric, 1 alarm |
| Input | At most 20 events and 100 KiB uncompressed |
| Retention | 3 days |
| Logs Insights | At most 10 queries, each over at most 30 minutes and this one log group |
| Spend ceiling | USD 0.25 estimated incremental spend; use the worksheet before ingestion |
| Runtime | Delete cloud resources the same session; stop after 2 hours even if diagnosis is incomplete |

Stop before the first mutation if the account or Region is unexpected, credentials are long-lived, authorization is unclear, a same-named resource already exists, the current regional price makes the estimate exceed USD 0.25, or the fixture contains secrets or real identifiers. Stop during the lab on throttling, unexpected resources or data, more than 100 KiB ingested, more than 10 queries, unexplained access denial, or inability to begin cleanup. Never broaden permissions merely to finish.

CloudWatch custom metrics cannot be manually deleted. Cleanup stops publication and removes the filter and alarm; the inactive series ages out according to CloudWatch behavior and has no continuing metric-storage charge from this lab. Keep only redacted CLI JSON and the evidence table.

### Establish the identity and cost prediction

Set a Region approved by the sandbox owner. Read the identity output before continuing.

```bash
export AWS_PAGER=""
export REGION="us-east-1"       # replace only with the approved Region
export LAB_ID="dop-c02-lab26-$(date -u +%Y%m%d%H%M%S)"
export LOG_GROUP="/dop-c02/lab26/${LAB_ID}"
export LOG_STREAM="synthetic-requests"
export METRIC_NAMESPACE="DOPC02/Lab26"
export METRIC_NAME="UserImpactErrors"
export ALARM_NAME="${LAB_ID}-user-impact"

aws --version
aws sts get-caller-identity
aws configure get region
printf 'REGION=%s\nLOG_GROUP=%s\nALARM=%s\n' \
  "$REGION" "$LOG_GROUP" "$ALARM_NAME"
```

Prediction: healthy `request.completed` events publish zero errors; one HTTP 503 event publishes one `UserImpactErrors` count, appears in the fault query, and moves the alarm to `ALARM`. When events stop, the alarm eventually becomes `INSUFFICIENT_DATA`, because missing data is configured as `missing`, not silently treated as good.

Before cloud work, fill the unit-price column from the current price page for `REGION`. The equations are explicit because prices and free-tier eligibility vary by Region and account.

| Billing dimension | Bounded quantity | Current regional unit price | Estimated charge |
|---|---:|---:|---:|
| Log ingestion | `fixture_uncompressed_bytes / 1,073,741,824` GiB; 100 KiB is exactly `102,400 / 1,073,741,824` GiB, approximately 0.00009537 GiB | USD/GiB, or convert to the pricing page's stated unit | quantity times price |
| Log archival storage | `ingested_GB * 72 / hours_in_actual_UTC_billing_month` GB-month | USD/GB-month | quantity times price |
| Logs Insights scan | `query_scanned_bytes / 1,073,741,824` GB, at most 10 queries | USD/GB scanned | sum of query GB times price |
| Custom metric | one metric for `ceil(active_minutes/60) / hours_in_actual_UTC_billing_month` month | USD/metric-month, applying documented hourly proration | quantity times price |
| Alarm | one standard-resolution alarm for `ceil(active_minutes/60) / hours_in_actual_UTC_billing_month` month | USD/alarm-month, applying documented hourly proration | quantity times price |
| **Total** | | | sum; must be at most USD 0.25 |

Do not enter `0` merely because a free tier may cover the run. Record both the calculated list-price estimate and the final billed or free-tier-adjusted amount when billing data becomes available. The query result's `statistics.bytesScanned` supplies the exact scan input.

## Establish a baseline

Create the group and stream, set three-day retention, and install the metric filter **before** events arrive because metric filters do not backfill old data.

```bash
aws logs create-log-group \
  --region "$REGION" \
  --log-group-name "$LOG_GROUP" \
  --tags "Purpose=dop-c02-lab26,LabId=${LAB_ID}"

aws logs put-retention-policy \
  --region "$REGION" \
  --log-group-name "$LOG_GROUP" \
  --retention-in-days 3

aws logs create-log-stream \
  --region "$REGION" \
  --log-group-name "$LOG_GROUP" \
  --log-stream-name "$LOG_STREAM"

aws logs put-metric-filter \
  --region "$REGION" \
  --log-group-name "$LOG_GROUP" \
  --filter-name "${LAB_ID}-errors" \
  --filter-pattern '{ $.event = "request.completed" && $.status >= 500 }' \
  --metric-transformations \
    "metricName=${METRIC_NAME},metricNamespace=${METRIC_NAMESPACE},metricValue=1,defaultValue=0,unit=Count"

aws cloudwatch put-metric-alarm \
  --region "$REGION" \
  --alarm-name "$ALARM_NAME" \
  --alarm-description "Synthetic user-impact proxy; owner: lab operator; runbook: this README" \
  --namespace "$METRIC_NAMESPACE" \
  --metric-name "$METRIC_NAME" \
  --statistic Sum \
  --period 60 \
  --evaluation-periods 1 \
  --datapoints-to-alarm 1 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --treat-missing-data missing
```

Prove the starting configuration. Expect `retentionInDays` to be `3`, no `kmsKeyId`, the exact filter pattern, and alarm state `INSUFFICIENT_DATA` before data arrives.

```bash
aws logs describe-log-groups \
  --region "$REGION" \
  --log-group-name-prefix "$LOG_GROUP" \
  --query 'logGroups[?logGroupName==`'"$LOG_GROUP"'`].{name:logGroupName,retention:retentionInDays,kmsKeyId:kmsKeyId,bytes:storedBytes}'

aws logs describe-metric-filters \
  --region "$REGION" \
  --log-group-name "$LOG_GROUP"

aws cloudwatch describe-alarms \
  --region "$REGION" \
  --alarm-names "$ALARM_NAME" \
  --query 'MetricAlarms[0].{state:StateValue,missing:TreatMissingData,period:Period,threshold:Threshold}'
```

An absent `kmsKeyId` supports the stated default-encryption choice. These calls do not prove key-policy suitability, log confidentiality in transit, or access-control correctness outside this resource.

## Make it work

Create four synthetic events. They contain no customer data, secrets, IP addresses, or real request IDs.

```bash
python3 - <<'PY' > /tmp/lab26-events.json
import json, time
base = int(time.time() * 1000)
rows = [
    {"event":"request.completed","schema":1,"request_id":"synthetic-001","trace_id":"1-65f00000-000000000000000000000001","route":"/checkout","status":200,"latency_ms":82,"outcome":"success"},
    {"event":"request.completed","schema":1,"request_id":"synthetic-002","trace_id":"1-65f00000-000000000000000000000002","route":"/checkout","status":200,"latency_ms":91,"outcome":"success"},
    {"event":"dependency.call","schema":1,"request_id":"synthetic-003","trace_id":"1-65f00000-000000000000000000000003","dependency":"payments-fixture","status":200,"latency_ms":40,"outcome":"success"},
    {"event":"request.completed","schema":1,"request_id":"synthetic-003","trace_id":"1-65f00000-000000000000000000000003","route":"/checkout","status":200,"latency_ms":88,"outcome":"success"},
]
print(json.dumps([{"timestamp":base+i, "message":json.dumps(row, separators=(",",":"))}
                  for i, row in enumerate(rows)]))
PY

wc -c /tmp/lab26-events.json
aws logs put-log-events \
  --region "$REGION" \
  --log-group-name "$LOG_GROUP" \
  --log-stream-name "$LOG_STREAM" \
  --log-events file:///tmp/lab26-events.json
```

Wait no more than two 60-second periods, then inspect the metric and alarm. A zero datapoint and `OK` establish that ingestion, parsing, metric publication, and alarm evaluation work for the healthy fixture.

```bash
START_10M="$(date -u -d '10 minutes ago' +%FT%TZ)"
END_NOW="$(date -u +%FT%TZ)"

aws cloudwatch get-metric-data \
  --region "$REGION" \
  --start-time "$START_10M" \
  --end-time "$END_NOW" \
  --metric-data-queries \
    '[{"Id":"errors","MetricStat":{"Metric":{"Namespace":"DOPC02/Lab26","MetricName":"UserImpactErrors"},"Period":60,"Stat":"Sum"},"ReturnData":true}]'

aws cloudwatch describe-alarms \
  --region "$REGION" \
  --alarm-names "$ALARM_NAME"
```

If no datapoint appears after two periods, do not inject the fault. Check event presence, timestamps, filter syntax, and `describe-metric-filters`; then clean up at the two-hour limit.

## Break it

Inject exactly one reversible fault event: a synthetic checkout result with HTTP 503. This does not call an application or dependency.

```bash
python3 - <<'PY' > /tmp/lab26-fault.json
import json, time
row = {"event":"request.completed","schema":1,"request_id":"synthetic-fault-001",
       "trace_id":"1-65f00000-ffffffffffffffffffffffff","route":"/checkout","status":503,"latency_ms":1200,
       "outcome":"error","error_type":"dependency_unavailable"}
print(json.dumps([{"timestamp":int(time.time()*1000),
                   "message":json.dumps(row, separators=(",",":"))}]))
PY

aws logs put-log-events \
  --region "$REGION" \
  --log-group-name "$LOG_GROUP" \
  --log-stream-name "$LOG_STREAM" \
  --log-events file:///tmp/lab26-fault.json
```

Expected symptom: `UserImpactErrors` has sum `1` for the event's minute and the alarm becomes `ALARM` within two evaluation periods. The metric is only a proxy: one synthetic 503 does not establish a real user outage or error ratio.

## Diagnose it

Start with the alarm history and then query the one log group over a bounded window.

```bash
aws cloudwatch describe-alarm-history \
  --region "$REGION" \
  --alarm-name "$ALARM_NAME" \
  --history-item-type StateUpdate \
  --max-records 10

QUERY_ID="$(
  aws logs start-query \
    --region "$REGION" \
    --log-group-name "$LOG_GROUP" \
    --start-time "$(date -u -d '30 minutes ago' +%s)" \
    --end-time "$(date -u +%s)" \
    --query-string 'fields @timestamp, request_id, trace_id, route, status, latency_ms, error_type | filter event = "request.completed" and status >= 500 | sort @timestamp desc | limit 20' \
    --query queryId --output text
)"
sleep 5
aws logs get-query-results \
  --region "$REGION" \
  --query-id "$QUERY_ID" \
  > /tmp/lab26-query-result.json
jq '{status,statistics,results}' /tmp/lab26-query-result.json
```

If status is `Running`, repeat `get-query-results` only until it is `Complete`, `Failed`, `Cancelled`, or `Timeout`; do not exceed the ten-query bound. Record `recordsMatched`, `recordsScanned`, and `bytesScanned`.

Rank and discriminate these hypotheses:

| Hypothesis | Discriminating evidence | Interpretation |
|---|---|---|
| A request fault occurred | Query returns `synthetic-fault-001` with status 503 | Supports the synthetic user-impact event |
| Filter or metric semantics are wrong | Event exists but no metric datapoint is published after two periods | Pipeline/configuration fault, not service recovery |
| Alarm is reacting to missing data | Alarm reason names missing data and the query has no 5xx event | Telemetry gap, not observed user failure |
| Query window or Region is wrong | `describe-log-streams` has a recent ingestion time but query returns none | Correct scope before changing instrumentation |

### Missing-telemetry test

Do not publish more events. The alarm can evaluate more historical datapoints
than `EvaluationPeriods` alone suggests, so two empty periods do not guarantee
an immediate state change. Inspect the alarm once per minute for at most ten
minutes:

```bash
aws cloudwatch describe-alarms \
  --region "$REGION" \
  --alarm-names "$ALARM_NAME" \
  --query 'MetricAlarms[0].{state:StateValue,reason:StateReason,updated:StateUpdatedTimestamp}'
```

The test passes when the old datapoint ages out of CloudWatch's evaluation
range and the alarm becomes `INSUFFICIENT_DATA`. If it remains `OK` or `ALARM`
after ten minutes, preserve the alarm history and recent datapoints and mark
this post-fault check inconclusive; do not manufacture a state. The initial
pre-data `INSUFFICIENT_DATA` state is still direct evidence of the configured
missing-data behavior. Missing telemetry proves uncertainty about the proxy;
it does not prove either health or failure.

Correct the controlled fault by publishing one healthy event and confirm the alarm returns to `OK` within two periods:

```bash
python3 - <<'PY' > /tmp/lab26-recovery.json
import json, time
row = {"event":"request.completed","schema":1,"request_id":"synthetic-recovery-001",
       "trace_id":"1-65f00000-eeeeeeeeeeeeeeeeeeeeeeee","route":"/checkout","status":200,"latency_ms":85,
       "outcome":"success"}
print(json.dumps([{"timestamp":int(time.time()*1000),
                   "message":json.dumps(row, separators=(",",":"))}]))
PY
aws logs put-log-events \
  --region "$REGION" \
  --log-group-name "$LOG_GROUP" \
  --log-stream-name "$LOG_STREAM" \
  --log-events file:///tmp/lab26-recovery.json
```

### Optional X-Ray correlation design

Do not enable X-Ray merely to complete this lab. If the sandbox already has an approved, sampled X-Ray source, take an actual trace ID from that source; X-Ray trace IDs have the form `1-8hex-24hex`. Validate the format before the read-only retrieval:

```bash
export XRAY_TRACE_ID="1-65f00000-0123456789abcdef01234567" # replace with an actual approved trace ID
[[ "$XRAY_TRACE_ID" =~ ^1-[0-9a-f]{8}-[0-9a-f]{24}$ ]] || {
  printf 'invalid X-Ray trace ID\n' >&2
  exit 1
}
aws xray batch-get-traces \
  --region "$REGION" \
  --trace-ids "$XRAY_TRACE_ID"
```

Do not run the example value unchanged: the synthetic log fixtures are not X-Ray segments and cannot establish correlation. Preserve an actual trace's segment times and fault flags, and state that a shared identifier supports correlation but does not prove causality. Before adding X-Ray, budget sampled traces, retention, indexed trace summaries, encryption choice, and permissions using the official X-Ray pricing and security documentation.

## Local fixture option

Use this path when no authorized AWS sandbox exists. Save the four healthy JSON objects and one fault object above as newline-delimited JSON in `/tmp/lab26-local.ndjson`, then run:

```bash
jq -c 'select(.event == "request.completed" and .status >= 500)' \
  /tmp/lab26-local.ndjson
jq -s '[.[] | select(.event == "request.completed")] |
  {requests:length, errors:map(select(.status >= 500))|length}' \
  /tmp/lab26-local.ndjson
```

This proves fixture structure and local filter logic only. It is **static/local evidence**, not evidence of CloudWatch encryption, retention, ingestion, metric publication, query billing, alarm evaluation, IAM, or cleanup.

## Clean up

Capture evidence first, then remove the alarm and log group. Deleting the group removes its stream and metric filter. Remove local fixtures after recording hashes or redacted excerpts.

```bash
aws cloudwatch delete-alarms \
  --region "$REGION" \
  --alarm-names "$ALARM_NAME"

aws logs delete-log-group \
  --region "$REGION" \
  --log-group-name "$LOG_GROUP"

aws cloudwatch describe-alarms \
  --region "$REGION" \
  --alarm-name-prefix "$LAB_ID" \
  --query 'length(MetricAlarms)'

aws logs describe-log-groups \
  --region "$REGION" \
  --log-group-name-prefix "$LOG_GROUP" \
  --query 'length(logGroups[?logGroupName==`'"$LOG_GROUP"'`])'

rm -f /tmp/lab26-events.json /tmp/lab26-fault.json \
  /tmp/lab26-recovery.json /tmp/lab26-query-result.json \
  /tmp/lab26-local.ndjson
```

Cleanup passes only when both length commands return `0`. Also run `list-tags-for-resource` or inspect the console if a command was interrupted. An inactive custom metric may remain discoverable until it ages out; prove no log group, filter, alarm, or publisher remains and record that residual platform behavior.

## What to keep

Use this exact evidence table. Store machine-readable outputs separately and reference their paths; redact account IDs without destroying timestamps or correlation.

| Evidence ID | Mode | Exact artifact or output | Claim supported | Does not prove |
|---|---|---|---|---|
| L26-E01 | AWS | UTC timestamp, CLI version, redacted `get-caller-identity`, exact Region | Authorized execution context recorded | Permission policy is least privilege |
| L26-E02 | AWS | `describe-log-groups` JSON with retention, absent `kmsKeyId`, and bytes | Three-day retention and chosen default encryption configuration | Customer managed key use or access-policy correctness |
| L26-E03 | AWS | Metric-filter and alarm JSON | Filter semantics, threshold, window, and missing-data treatment | Events are arriving |
| L26-E04 | AWS | Fixture byte count and `put-log-events` response | Bounded synthetic input accepted | Durable queryability or completeness |
| L26-E05 | AWS | Metric datapoints and alarm transition history | Fault changed the proxy and alarm state | Real user impact or causation |
| L26-E06 | AWS | `/tmp/lab26-query-result.json`, including `bytesScanned` | Exact fault event was queryable and scan cost input known | Unsampled events outside the window |
| L26-E07 | AWS | Missing-data state and reason | Telemetry absence is surfaced as unknown | Workload failure or health |
| L26-E08 | AWS | Recovery event, datapoint, and `OK` transition | Controlled signal recovered | Sustained production recovery |
| L26-E09 | AWS | Completed cost worksheet with source date and Region | Bounded list-price estimate and billing dimensions | Final invoice until billing data settles |
| L26-E10 | AWS | Both cleanup queries returning `0` | Named billable resources removed | Account-wide absence of unrelated resources |
| L26-L01 | Local | Fixture hash and `jq` output | Static schema and filter behavior | Any AWS control or runtime behavior |

Finish with a short explain-back: why the filter publishes a bounded aggregate, why logs retain high-cardinality request IDs, why alarm state depends on missing-data policy, which bytes are billed at ingestion/storage/query, one disproved hypothesis, and one production implication. Record whether evidence is real AWS observation, local/static evidence, or an unexecuted prediction.

## Sources

Official AWS sources, checked 2026-08-23:

- [CloudWatch Logs data protection and encryption](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/data-protection.html)
- [Encrypt log data with AWS KMS](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html)
- [CloudWatch Logs retention](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html)
- [Metric filters for JSON log events](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntaxForMetricFilters.html)
- [CloudWatch alarm missing-data behavior](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
- [CloudWatch Logs Insights query syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html)
- [CloudWatch Logs Insights query statistics API](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_GetQueryResults.html)
- [CloudWatch pricing](https://aws.amazon.com/cloudwatch/pricing/)
- [X-Ray trace retrieval](https://docs.aws.amazon.com/xray/latest/api/API_BatchGetTraces.html)
- [X-Ray security](https://docs.aws.amazon.com/xray/latest/devguide/security.html)
