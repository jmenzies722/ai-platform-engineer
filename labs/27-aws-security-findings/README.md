# Lab: Route and Triage Bounded AWS Security Findings

This lab exercises the finding lifecycle without creating malicious traffic. It enables a minimal, single-Region Security Hub and GuardDuty slice in an empty sandbox, generates documented synthetic findings, routes one finding through EventBridge, records a time-bounded suppression decision, and removes everything it owns.

## Goal

Produce inspectable evidence that a synthetic security finding can be created, delivered to an encrypted triage queue under a source-restricted policy, triaged, suppressed only with an expiry, archived, and cleaned up. Compare other AWS controls by coverage and cost rather than enabling a service catalogue.

### DOP-C02 task mapping

| Direct task ID | Direct lab evidence |
|---|---|
| 6.3 | GuardDuty sample finding, custom Security Hub finding, EventBridge triage, suppression/archival, residual risk, Region, and cost record |

The route supports discussion of tasks 5.1 and 5.2, the bounded diagnosis supports 5.3, the permission review supports 6.1, and encryption/selection analysis supports 6.2. This synthetic, single-account, single-Region lab does **not** prove event management, response automation, IAM at scale, broad data protection, or troubleshooting in a complex production environment; those task IDs are supporting context, not direct completion evidence.

Canonical preparation: [AWS operations and observability](../../12-aws/05-operations-and-observability.md), [cloud and application security](../../20-security/06-cloud-and-application-security.md), [security detection and response](../../20-security/07-security-incident-response.md), and [structured logs](../../18-observability/04-logs.md).

## Before you start

### Identity and authorization assumptions

- Use AWS CLI v2 and temporary credentials in an **authorized, empty, disposable sandbox account**. Do not run in production, an organization delegated-administrator account, a security tooling account, or any account with customer workloads or existing findings.
- The sandbox owner has approved temporary enablement of Security Hub and GuardDuty in exactly one Region. These services inspect account activity while enabled; authorization must cover that side effect.
- The caller may use `sts:GetCallerIdentity`; the required regional Security Hub and GuardDuty create/read/update/delete APIs; one named EventBridge rule; and one named SQS queue and queue policy. It cannot change organization configuration, invite members, enable standards, create subscriptions, invoke remediation, or access unrelated queues and rules.
- `iam:PassRole`, IAM mutation, Lambda, SNS, EC2, S3, malware simulation, port scanning, credential misuse, and real attack generation are neither required nor authorized.
- A reviewer should compare the effective identity policy with the named actions and resources before mutation. Service APIs that do not support resource-level permissions may require `Resource: "*"`, constrained by Region, account, temporary principal, and session policy. Record that exception instead of claiming perfect resource scoping.

The command path uses this minimum action set:

- Security Hub: `EnableSecurityHub`, `DescribeHub`, `GetEnabledStandards`, `BatchImportFindings`, `BatchUpdateFindings`, `GetFindings`, `DisableSecurityHub`, and `securityhub:TagResource` because the enable command supplies tags;
- GuardDuty: `ListDetectors`, `CreateDetector`, `GetDetector`, `CreateSampleFindings`, `ListFindings`, `GetFindings`, `DeleteDetector`, and `guardduty:TagResource` because the create command supplies tags;
- EventBridge: `ListRules`, `PutRule`, `DescribeRule`, `PutTargets`, `ListTargetsByRule`, `EnableRule`, `DisableRule`, `RemoveTargets`, `DeleteRule`, and tagging for this rule;
- SQS: `ListQueues`, `CreateQueue`, `GetQueueAttributes`, `SetQueueAttributes`, `ReceiveMessage`, `DeleteMessage`, `DeleteQueue`, and tagging for this queue.

Constrain mutating EventBridge and SQS actions to names beginning with `LAB_ID` where the API supports it. The preflight reviewer records any action above that the effective policy grants more broadly and treats unapproved broad access as a stop condition.

The EventBridge target is an SQS queue using SQS-owned server-side encryption (`SqsManagedSseEnabled=true`). This choice avoids customer-key policy work in a short-lived lab. The queue policy allows `events.amazonaws.com` to call only `sqs:SendMessage`, only when `aws:SourceArn` equals this lab's rule ARN. Security Hub and GuardDuty encryption are service-managed; this lab does not create export buckets or customer managed keys.

### Bounds, cost, and stop conditions

| Bound | Limit |
|---|---|
| Expected time | 60 to 90 minutes |
| Region | Exactly one; no aggregation Region |
| Security Hub | 1 hub, default standards disabled, 1 custom finding |
| GuardDuty | 1 detector, 1 documented sample finding type, at most 30 minutes enabled |
| Routing | 1 EventBridge rule and 1 encrypted SQS queue; no subscription or automated remediation |
| Messages | At most 10 received, one receive attempt at a time |
| Spend ceiling | USD 1.00 calculated list-price estimate |
| Data | Synthetic IDs and account metadata only; no customer, vulnerability, object, or network data |
| Cleanup | Begin by minute 30 after detector creation; finish in the same session |

Stop before mutation if `list-detectors` returns an existing detector, `describe-hub` shows an existing hub, the account or Region is unexpected, the account has workloads or meaningful management-event volume, organization integration is present, authorization is unclear, a same-named queue/rule exists, current prices can exceed USD 1.00, or cleanup permissions are unproven. Stop immediately on a real finding, unexpected member/standard/control, customer identifier, secret, unexpected target delivery, unbounded cost, or inability to archive/delete a resource. Preserve evidence and ask the sandbox owner to clean up; do not disable a pre-existing service.

Never trigger an attack, probe an address, weaken a control, expose a resource, or use a real leaked credential. GuardDuty `create-sample-findings` and the Security Hub `BatchImportFindings` payload below are synthetic service features, not attack simulation.

### Establish identity, scope, and cost

```bash
export AWS_PAGER=""
export REGION="us-east-1"       # replace only with the approved Region
export LAB_ID="dop-c02-lab27-$(date -u +%Y%m%d%H%M%S)"
export RULE_NAME="${LAB_ID}-triage"
export QUEUE_NAME="${LAB_ID}-triage"

aws --version
aws sts get-caller-identity
aws configure get region
printf 'REGION=%s\nRULE=%s\nQUEUE=%s\n' \
  "$REGION" "$RULE_NAME" "$QUEUE_NAME"

aws guardduty list-detectors --region "$REGION"
aws securityhub describe-hub --region "$REGION" 2>&1 || true
aws events list-rules \
  --region "$REGION" \
  --name-prefix "$RULE_NAME"
aws sqs list-queues \
  --region "$REGION" \
  --queue-name-prefix "$QUEUE_NAME"
```

Proceed only when there is no detector, Security Hub reports that it is not enabled, and no matching queue or rule exists. Do not interpret an access-denied response as absence.

Prediction: the custom finding is accepted once, emits a Security Hub imported-finding event, matches the EventBridge rule, and becomes an encrypted SQS message. The GuardDuty sample appears as a sample finding without any hostile action. Suppression changes workflow, not the underlying risk; an expiry and owner remain necessary.

Complete this ledger with the current rates for `REGION` before enabling services. Use exact UTC enable/disable timestamps and do not round duration down.

| Billing dimension | Exact bounded quantity | Current regional unit price | List-price charge |
|---|---:|---:|---:|
| Security Hub security checks | `0`, because default standards remain disabled | USD/check | `0 * price` |
| Security Hub finding ingestion | 1 custom finding plus any one GuardDuty sample integration finding actually observed | USD/finding or documented tier | observed count times applicable price |
| GuardDuty foundational data | usage attributed during exact enabled interval; obtain the account's billed usage when available | regional USD per analyzed unit | exact usage times tiered price |
| GuardDuty optional protection plans | `0`; every non-runtime optional feature is explicitly disabled and runtime monitoring remains disabled | regional unit price | verify `0`, otherwise stop |
| EventBridge custom events | `0`; AWS service events are used | USD/million | `0` under documented AWS service-event pricing |
| SQS requests | exact 64 KiB request-unit count from the command log, bounded below 25 | USD/million requests | units divided by 1,000,000 times price; there is no separate in-session message-storage line item |
| **Total** | exact Region: `$REGION`; exact interval: enable UTC through disable UTC | | sum; must be at most USD 1.00 |

Free trials and free tiers change the invoice, not the engineering estimate. Record three values: calculated list-price charge, AWS billing charge when available, and the difference attributed to free tier or rounding. GuardDuty usage and billing can lag; if the final invoice is not yet available, mark only the **invoice** field pending and retain the exact Region, timestamps, usage query, rates, and formula. Do not call a provisional estimate an exact billed cost.

## Establish a baseline

Enable only the bounded services and record timestamps.

```bash
export ENABLED_AT="$(date -u +%FT%TZ)"

aws securityhub enable-security-hub \
  --region "$REGION" \
  --no-enable-default-standards \
  --tags "Purpose=dop-c02-lab27,LabId=${LAB_ID}"

export DETECTOR_ID="$(
  aws guardduty create-detector \
    --region "$REGION" \
    --enable \
    --finding-publishing-frequency FIFTEEN_MINUTES \
    --features \
      Name=S3_DATA_EVENTS,Status=DISABLED \
      Name=EKS_AUDIT_LOGS,Status=DISABLED \
      Name=EBS_MALWARE_PROTECTION,Status=DISABLED \
      Name=RDS_LOGIN_EVENTS,Status=DISABLED \
      Name=LAMBDA_NETWORK_LOGS,Status=DISABLED \
      Name=EKS_RUNTIME_MONITORING,Status=DISABLED \
      Name=AI_PROTECTION,Status=DISABLED \
      Name=AI_ANALYST,Status=DISABLED \
    --tags "Purpose=dop-c02-lab27,LabId=${LAB_ID}" \
    --query DetectorId --output text
)"

aws securityhub get-enabled-standards \
  --region "$REGION"
aws guardduty get-detector \
  --region "$REGION" \
  --detector-id "$DETECTOR_ID"
```

Expected baseline: `StandardsSubscriptions` is empty, detector status is enabled, all listed optional features are disabled, and only GuardDuty foundational data sources remain. `RUNTIME_MONITORING` is omitted because new detectors leave it disabled by default and AWS rejects specifying both it and `EKS_RUNTIME_MONITORING`; the latter is explicitly disabled above. If a standard or optional feature is enabled, stop and clean up. Enabling a hub without standards does not establish compliance, and enabling a detector does not establish that all data sources or Regions are covered.

## Make it work

### Create the encrypted triage route

```bash
export ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
export PARTITION="$(
  aws sts get-caller-identity --query Arn --output text | cut -d: -f2
)"
export QUEUE_URL="$(
  aws sqs create-queue \
    --region "$REGION" \
    --queue-name "$QUEUE_NAME" \
    --attributes SqsManagedSseEnabled=true,MessageRetentionPeriod=3600 \
    --tags "Purpose=dop-c02-lab27,LabId=${LAB_ID}" \
    --query QueueUrl --output text
)"
export QUEUE_ARN="$(
  aws sqs get-queue-attributes \
    --region "$REGION" \
    --queue-url "$QUEUE_URL" \
    --attribute-names QueueArn \
    --query Attributes.QueueArn --output text
)"

python3 - <<'PY' > /tmp/lab27-event-pattern.json
import json, os
print(json.dumps({
  "source": ["aws.securityhub"],
  "detail-type": ["Security Hub Findings - Imported"],
  "detail": {"findings": {"GeneratorId": [os.environ["LAB_ID"]]}}
}))
PY

export RULE_ARN="$(
  aws events put-rule \
    --region "$REGION" \
    --name "$RULE_NAME" \
    --description "Route only lab27 synthetic Security Hub findings" \
    --event-pattern file:///tmp/lab27-event-pattern.json \
    --state ENABLED \
    --tags "Key=Purpose,Value=dop-c02-lab27" "Key=LabId,Value=${LAB_ID}" \
    --query RuleArn --output text
)"

python3 - <<'PY' > /tmp/lab27-queue-policy.json
import json, os
print(json.dumps({
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "AllowOnlyThisEventBridgeRule",
    "Effect": "Allow",
    "Principal": {"Service": "events.amazonaws.com"},
    "Action": "sqs:SendMessage",
    "Resource": os.environ["QUEUE_ARN"],
    "Condition": {"ArnEquals": {"aws:SourceArn": os.environ["RULE_ARN"]}}
  }]
}))
PY

python3 - <<'PY' > /tmp/lab27-queue-attributes.json
import json
policy = open("/tmp/lab27-queue-policy.json", encoding="utf-8").read()
print(json.dumps({"Policy": policy, "SqsManagedSseEnabled": "true",
                  "MessageRetentionPeriod": "3600"}))
PY

aws sqs set-queue-attributes \
  --region "$REGION" \
  --queue-url "$QUEUE_URL" \
  --attributes file:///tmp/lab27-queue-attributes.json

aws events put-targets \
  --region "$REGION" \
  --rule "$RULE_NAME" \
  --targets "Id=triage-queue,Arn=${QUEUE_ARN}"
```

Verify encryption and least privilege before importing a finding:

```bash
aws sqs get-queue-attributes \
  --region "$REGION" \
  --queue-url "$QUEUE_URL" \
  --attribute-names QueueArn SqsManagedSseEnabled KmsMasterKeyId Policy

aws events list-targets-by-rule \
  --region "$REGION" \
  --rule "$RULE_NAME"
aws events describe-rule \
  --region "$REGION" \
  --name "$RULE_NAME"
```

Pass only if SQS-managed encryption is `true`, the sole principal is `events.amazonaws.com`, the sole action is `sqs:SendMessage`, the resource equals `QUEUE_ARN`, the source condition equals `RULE_ARN`, the event pattern includes this `LAB_ID`, and there is one target. This checks the resource policy and target, not the caller's complete effective permissions or organization guardrails.

### Import one deterministic synthetic finding

```bash
export FINDING_ID="${LAB_ID}/synthetic-config-check"
export PRODUCT_ARN="arn:${PARTITION}:securityhub:${REGION}:${ACCOUNT_ID}:product/${ACCOUNT_ID}/default"
export CREATED_AT="$(date -u +%FT%TZ)"

python3 - <<'PY' > /tmp/lab27-finding.json
import json, os
finding = {
  "SchemaVersion": "2018-10-08",
  "Id": os.environ["FINDING_ID"],
  "ProductArn": os.environ["PRODUCT_ARN"],
  "GeneratorId": os.environ["LAB_ID"],
  "AwsAccountId": os.environ["ACCOUNT_ID"],
  "Types": ["Software and Configuration Checks/AWS Security Best Practices"],
  "CreatedAt": os.environ["CREATED_AT"],
  "UpdatedAt": os.environ["CREATED_AT"],
  "Severity": {"Label": "LOW"},
  "Title": "Synthetic lab encryption review",
  "Description": "Synthetic training finding; no real resource or exposure exists.",
  "Resources": [{
    "Type": "AwsAccount",
    "Id": "AWS::::Account:" + os.environ["ACCOUNT_ID"],
    "Partition": os.environ["PARTITION"],
    "Region": os.environ["REGION"]
  }],
  "Compliance": {"Status": "WARNING"},
  "RecordState": "ACTIVE",
  "Workflow": {"Status": "NEW"},
  "UserDefinedFields": {
    "evidence_class": "synthetic",
    "lab_id": os.environ["LAB_ID"]
  }
}
print(json.dumps([finding]))
PY

aws securityhub batch-import-findings \
  --region "$REGION" \
  --findings file:///tmp/lab27-finding.json \
  > /tmp/lab27-import-result.json
jq . /tmp/lab27-import-result.json
```

Require `SuccessCount: 1` and `FailedCount: 0`. Reusing `FINDING_ID` updates the same finding rather than creating a new identity; this limits duplicate triage. It does not make an arbitrary downstream consumer idempotent.

Wait up to five minutes, receive the baseline route evidence, validate it, record its message identity, and delete it before the controlled routing fault:

```bash
aws sqs receive-message \
  --region "$REGION" \
  --queue-url "$QUEUE_URL" \
  --max-number-of-messages 1 \
  --wait-time-seconds 10 \
  --visibility-timeout 60 \
  --attribute-names All \
  --message-attribute-names All \
  > /tmp/lab27-message.json

jq --arg id "$FINDING_ID" --arg generator "$LAB_ID" -e '
  (.Messages | length) == 1 and
  (.Messages[0].Body | fromjson |
    .source == "aws.securityhub" and
    ."detail-type" == "Security Hub Findings - Imported" and
    .detail.findings[0].Id == $id and
    .detail.findings[0].GeneratorId == $generator)' \
  /tmp/lab27-message.json

export BASELINE_MESSAGE_ID="$(jq -r '.Messages[0].MessageId' /tmp/lab27-message.json)"
export BASELINE_RECEIPT="$(jq -r '.Messages[0].ReceiptHandle' /tmp/lab27-message.json)"
test -n "$BASELINE_MESSAGE_ID" && test "$BASELINE_MESSAGE_ID" != "null"
test -n "$BASELINE_RECEIPT" && test "$BASELINE_RECEIPT" != "null"

aws sqs delete-message \
  --region "$REGION" \
  --queue-url "$QUEUE_URL" \
  --receipt-handle "$BASELINE_RECEIPT"
printf 'deleted_baseline_message_id=%s deleted_at=%s\n' \
  "$BASELINE_MESSAGE_ID" "$(date -u +%FT%TZ)" \
  > /tmp/lab27-baseline-deletion.txt

aws sqs get-queue-attributes \
  --region "$REGION" \
  --queue-url "$QUEUE_URL" \
  --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible
```

The validation must exit `0`, and the deletion record must name the baseline message ID without exposing its receipt handle. Wait for the approximate queue counts to settle at zero before disabling the rule. If another baseline delivery appears, validate, record, and delete it within the ten-message bound; do not start the fault window with an unexplained message present. SQS and EventBridge can redeliver, so the later negative test must also inspect any received body's finding update rather than assuming every message is new.

### Create one GuardDuty sample finding

Use the documented sample API; do not reproduce the behavior named by the sample.

```bash
export SAMPLE_TYPE="Recon:EC2/PortProbeUnprotectedPort"
aws guardduty create-sample-findings \
  --region "$REGION" \
  --detector-id "$DETECTOR_ID" \
  --finding-types "$SAMPLE_TYPE"

aws guardduty list-findings \
  --region "$REGION" \
  --detector-id "$DETECTOR_ID" \
  --finding-criteria '{"Criterion":{"service.additionalInfo.sample":{"Eq":["true"]}}}' \
  --max-results 10 \
  > /tmp/lab27-guardduty-findings.json

mapfile -t SAMPLE_FINDING_IDS \
  < <(jq -r '.FindingIds[]?' /tmp/lab27-guardduty-findings.json)
test "${#SAMPLE_FINDING_IDS[@]}" -eq 1 || {
  printf 'expected exactly one GuardDuty sample finding\n' >&2
  exit 1
}

aws guardduty get-findings \
  --region "$REGION" \
  --detector-id "$DETECTOR_ID" \
  --finding-ids "${SAMPLE_FINDING_IDS[@]}" \
  > /tmp/lab27-guardduty-finding-details.json

jq --arg type "$SAMPLE_TYPE" -e '
  (.Findings | length) == 1 and
  all(.Findings[];
    .Type == $type and
    (((.Service.AdditionalInfo.Value // "{}") | fromjson? | .sample) == true))' \
  /tmp/lab27-guardduty-finding-details.json
jq '.Findings[] | {Id,Type,Service}' \
  /tmp/lab27-guardduty-finding-details.json
```

Require exactly one result whose `Type` equals `SAMPLE_TYPE` and whose retrieved additional information marks it as a sample. If AWS rejects that documented type in the selected Region, no ID appears, or `get-findings` does not prove both fields, record the response and stop this step. Do not substitute a real probe. A sample validates finding presentation and permissions; it does not validate live data-source detection, containment, or adversary coverage.

## Break it

Introduce one safe routing fault: disable this lab's EventBridge rule, confirm its state, update the same finding's note, and perform one bounded 10-second long poll for a new queue message.

```bash
aws events disable-rule \
  --region "$REGION" \
  --name "$RULE_NAME"

test "$(
  aws events describe-rule \
    --region "$REGION" \
    --name "$RULE_NAME" \
    --query State --output text
)" = "DISABLED"

# Rule state and event routing converge asynchronously. Wait before creating
# the negative-test event.
sleep 60

aws securityhub batch-update-findings \
  --region "$REGION" \
  --finding-identifiers "Id=${FINDING_ID},ProductArn=${PRODUCT_ARN}" \
  --note "Text=Synthetic update while route disabled,UpdatedBy=${LAB_ID}"

aws sqs receive-message \
  --region "$REGION" \
  --queue-url "$QUEUE_URL" \
  --max-number-of-messages 1 \
  --wait-time-seconds 10 \
  > /tmp/lab27-disabled-route-message.json

jq -e '((.Messages // []) | length) == 0' \
  /tmp/lab27-disabled-route-message.json
```

Expected symptom: the validation exits `0`, showing no message for the update
during this bounded disabled window. If a message contains `Synthetic update
while route disabled`, record the propagation delay, delete that message, wait
another 60 seconds, and repeat the update with a distinct attempt suffix. Make
at most three attempts and stop if every attempt routes. Delete and record any
delayed baseline delivery before retrying. An empty receive is bounded negative
evidence, not proof that no delayed message can ever arrive.

## Diagnose it

Start with the missing triage message. Rank the hypotheses before changing state.

| Hypothesis | Discriminating evidence | Decision |
|---|---|---|
| Finding update failed | `get-findings` lacks the new note | Correct finding identity or update request |
| Rule is disabled or pattern does not match | `describe-rule` state/pattern versus finding event fields | Re-enable this exact rule or correct the bounded pattern |
| EventBridge cannot send to SQS | Queue policy source ARN differs or target invocation metrics show failure | Repair only the queue policy/target |
| Message is delayed or invisible | Queue approximate visible/not-visible counts and receipt history | Wait within the five-minute bound; do not duplicate findings |
| Wrong account or Region | Identity, finding ARN, rule ARN, and queue ARN disagree | Stop; do not recreate cross-Region resources |

```bash
aws securityhub get-findings \
  --region "$REGION" \
  --filters "Id=[{Value=${FINDING_ID},Comparison=EQUALS}]" \
  --max-results 10
aws events describe-rule \
  --region "$REGION" \
  --name "$RULE_NAME"
aws sqs get-queue-attributes \
  --region "$REGION" \
  --queue-url "$QUEUE_URL" \
  --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible Policy
```

Correct the controlled fault by re-enabling the rule. Update the finding again with a distinct note, receive the message, and require the exact finding ID before claiming recovery.

```bash
aws events enable-rule \
  --region "$REGION" \
  --name "$RULE_NAME"

test "$(
  aws events describe-rule \
    --region "$REGION" \
    --name "$RULE_NAME" \
    --query State --output text
)" = "ENABLED"

# Allow the data-plane route to converge before publishing recovery evidence.
sleep 60

export RECOVERY_NOTE="Synthetic route recovery check"
aws securityhub batch-update-findings \
  --region "$REGION" \
  --finding-identifiers "Id=${FINDING_ID},ProductArn=${PRODUCT_ARN}" \
  --note "Text=${RECOVERY_NOTE},UpdatedBy=${LAB_ID}"

aws sqs receive-message \
  --region "$REGION" \
  --queue-url "$QUEUE_URL" \
  --max-number-of-messages 1 \
  --wait-time-seconds 10 \
  --visibility-timeout 60 \
  --attribute-names All \
  > /tmp/lab27-recovery-message.json

jq --arg id "$FINDING_ID" --arg generator "$LAB_ID" \
  --arg note "$RECOVERY_NOTE" -e '
  (.Messages | length) == 1 and
  (.Messages[0].Body | fromjson |
    .source == "aws.securityhub" and
    ."detail-type" == "Security Hub Findings - Imported" and
    .detail.findings[0].Id == $id and
    .detail.findings[0].GeneratorId == $generator and
    .detail.findings[0].Note.Text == $note)' \
  /tmp/lab27-recovery-message.json
```

If no matching message arrives, first repeat the bounded receive for up to one
minute to allow ordinary delivery latency. Then repeat the complete
update-and-receive pair with `RECOVERY_NOTE` set to a distinct attempt suffix;
an update emitted before route convergence cannot be recovered by polling SQS.
Make at most three updates over five minutes. Recovery passes only when the
message matches the exact note for its attempt. Record the recovery message ID
and retain its receipt handle privately for cleanup.

## Triage and suppression decision

The finding is synthetic, low severity, has no affected resource, and exists solely to test the route. The correct lab decision is to suppress it temporarily while preserving the workflow record, with a named owner and an expiry one hour from now. A real finding may require containment rather than suppression.

```bash
export SUPPRESSION_EXPIRES_AT="$(date -u -d '+1 hour' +%FT%TZ)"

aws securityhub batch-update-findings \
  --region "$REGION" \
  --finding-identifiers "Id=${FINDING_ID},ProductArn=${PRODUCT_ARN}" \
  --workflow Status=SUPPRESSED \
  --note "Text=Synthetic lab finding only; archive during cleanup; expires ${SUPPRESSION_EXPIRES_AT},UpdatedBy=${LAB_ID}" \
  --user-defined-fields \
    "suppression_expires_at=${SUPPRESSION_EXPIRES_AT},suppression_owner=${LAB_ID},suppression_reason=synthetic_training"

aws securityhub get-findings \
  --region "$REGION" \
  --filters "Id=[{Value=${FINDING_ID},Comparison=EQUALS}]" \
  --max-results 10 \
  > /tmp/lab27-suppressed-finding.json
jq '.Findings[] |
  {Id,RecordState,Workflow,Note,UserDefinedFields,UpdatedAt}' \
  /tmp/lab27-suppressed-finding.json
```

The evidence must contain `SUPPRESSED`, owner, reason, and the exact UTC expiry. If the lab were interrupted, the owner would review at expiry and restore `NEW` unless the reason still holds. Cleanup archives this synthetic finding before expiry and records that archival superseded the temporary decision. Never use suppression to make an unresolved risk disappear from reporting.

### Residual risk and service-selection exercise

Do **not** enable more services. Complete this table for one actual sandbox architecture and justify `select`, `defer`, or `not applicable`.

| Service/control | Primary question it can answer | Required data or scope | Cost/blast-radius consideration | Decision and residual risk |
|---|---|---|---|---|
| Amazon Inspector | Which supported compute workloads or images have detected vulnerabilities/exposure? | EC2, ECR, or Lambda coverage | Continuous scanning and account/Region coverage | |
| Amazon Macie | Which selected S3 objects may contain sensitive data? | Explicit S3 bucket scope | Object sampling/classification cost and data access | |
| IAM Access Analyzer | Which resource/IAM policies grant external, public, or unused access? | Analyzer zone of trust and policy scope | Organization/account analyzer ownership | |
| AWS WAF | Which HTTP requests should be observed or blocked at supported edge/application resources? | Associated web ACL and request traffic | Request/rule charges; false-positive user impact | |
| AWS Shield | What DDoS protections and response level are required? | Internet-facing resources | Standard versus Advanced commercial/operational commitment | |
| AWS Network Firewall | Which VPC flows require centralized inspection? | Routed subnets and firewall policy | Endpoint/hour and traffic-processing charges; routing failure risk | |
| Amazon Detective | Which accepted findings need graph-based investigation context? | Supported telemetry and account graph | Ingested behavior-graph volume and retention | |

Selection is constraint-driven. GuardDuty does not replace vulnerability scanning, Macie does not classify non-S3 data, Access Analyzer does not inspect runtime attacks, and WAF does not protect non-associated protocols. Record what remains uncovered after the bounded Security Hub/GuardDuty exercise.

## Clean up

Archive the custom finding, delete visible queue messages, remove target before rule, delete the queue, then disable only the hub and detector whose IDs this lab created.

```bash
export ARCHIVED_AT="$(date -u +%FT%TZ)"
python3 - <<'PY' > /tmp/lab27-archived-finding.json
import json, os
with open("/tmp/lab27-finding.json", encoding="utf-8") as source:
    findings = json.load(source)
finding = findings[0]
finding["UpdatedAt"] = os.environ["ARCHIVED_AT"]
finding["RecordState"] = "ARCHIVED"
finding["Workflow"] = {"Status": "RESOLVED"}
print(json.dumps([finding]))
PY

aws securityhub batch-import-findings \
  --region "$REGION" \
  --findings file:///tmp/lab27-archived-finding.json

aws securityhub get-findings \
  --region "$REGION" \
  --filters "Id=[{Value=${FINDING_ID},Comparison=EQUALS}]" \
  --max-results 10 \
  > /tmp/lab27-archived-finding-proof.json
jq -e '
  (.Findings | length) == 1 and
  .Findings[0].RecordState == "ARCHIVED" and
  .Findings[0].Workflow.Status == "RESOLVED"' \
  /tmp/lab27-archived-finding-proof.json

for RECEIPT in $(
  jq -r '.Messages[]?.ReceiptHandle' \
    /tmp/lab27-disabled-route-message.json \
    /tmp/lab27-recovery-message.json 2>/dev/null
); do
  aws sqs delete-message \
    --region "$REGION" \
    --queue-url "$QUEUE_URL" \
    --receipt-handle "$RECEIPT" || true
done

aws events remove-targets \
  --region "$REGION" \
  --rule "$RULE_NAME" \
  --ids triage-queue
aws events delete-rule \
  --region "$REGION" \
  --name "$RULE_NAME"
aws sqs delete-queue \
  --region "$REGION" \
  --queue-url "$QUEUE_URL"

aws guardduty delete-detector \
  --region "$REGION" \
  --detector-id "$DETECTOR_ID"
aws securityhub disable-security-hub \
  --region "$REGION"
export DISABLED_AT="$(date -u +%FT%TZ)"
printf 'enabled=%s\ndisabled=%s\nregion=%s\n' \
  "$ENABLED_AT" "$DISABLED_AT" "$REGION"
```

Prove teardown:

```bash
aws guardduty list-detectors \
  --region "$REGION" \
  --query 'DetectorIds'
aws securityhub describe-hub \
  --region "$REGION" 2>&1 || true
aws events list-rules \
  --region "$REGION" \
  --name-prefix "$RULE_NAME" \
  --query 'length(Rules)'
aws sqs list-queues \
  --region "$REGION" \
  --queue-name-prefix "$QUEUE_NAME" \
  --query 'length(QueueUrls || `[]`)'
```

Cleanup passes only when detector IDs are empty, Security Hub reports not enabled rather than access denied, and rule/queue counts are `0`. Recheck after eventual-consistency delay, but stop after five minutes and escalate exact resource IDs rather than deleting unrelated resources. Remove local temporary files only after preserving redacted evidence:

```bash
rm -f /tmp/lab27-event-pattern.json /tmp/lab27-queue-policy.json \
  /tmp/lab27-queue-attributes.json /tmp/lab27-finding.json \
  /tmp/lab27-import-result.json /tmp/lab27-message.json \
  /tmp/lab27-baseline-deletion.txt \
  /tmp/lab27-disabled-route-message.json \
  /tmp/lab27-guardduty-findings.json \
  /tmp/lab27-guardduty-finding-details.json \
  /tmp/lab27-recovery-message.json \
  /tmp/lab27-archived-finding.json \
  /tmp/lab27-archived-finding-proof.json \
  /tmp/lab27-suppressed-finding.json
```

## What to keep

Use this exact evidence table. Raw artifacts must be JSON or text, not screenshots alone. Redact account IDs consistently while retaining Region, finding suffix, ordering, and UTC timestamps.

| Evidence ID | Evidence class | Exact artifact or output | Claim supported | Does not prove |
|---|---|---|---|---|
| L27-E01 | Real AWS | CLI version, redacted caller identity, Region, approval reference | Authorized execution scope recorded | Effective policy is least privilege |
| L27-E02 | Real AWS | Empty preflight detector/hub/rule/queue outputs | Lab did not knowingly take ownership of existing resources | Account has no hidden or cross-Region controls |
| L27-E03 | Real AWS | Hub standards and detector configuration JSON | Bounded subset and no default standards | Organization-wide detection coverage |
| L27-E04 | Real AWS | SQS attributes, decoded policy, rule, and target JSON | Encryption and source-restricted delivery policy | Message confidentiality after consumption |
| L27-E05 | Synthetic input | `/tmp/lab27-finding.json` hash and import counts | One deterministic custom finding was accepted | A real misconfiguration exists |
| L27-E06 | Real AWS from synthetic event | Redacted baseline queue message, exact finding ID/generator, and `/tmp/lab27-baseline-deletion.txt` | EventBridge delivered the finding and the baseline message was removed before fault injection | Every event is delivered exactly once |
| L27-E07 | Real AWS sample | GuardDuty sample finding IDs/type and `sample=true` | Sample API and finding retrieval work | Real attack detection or data-source completeness |
| L27-E08 | Real AWS from controlled fault | Disabled-rule state, validated empty bounded receive, diagnosis, and `/tmp/lab27-recovery-message.json` passing ID/generator/note checks | Routing fault was observed and corrected | No delayed/duplicate delivery outside the window |
| L27-E09 | Real AWS workflow state | Suppressed finding JSON with owner, reason, exact expiry, then archival result | Suppression was bounded and cleanup resolved synthetic state | Suppression is appropriate for a real finding |
| L27-E10 | Analysis | Completed service-selection table and residual-risk statement | Controls were selected by architecture and threat | Deferred controls are unnecessary |
| L27-E11 | Real AWS plus calculation | Exact Region, enable/disable UTC, usage inputs, source-date prices, list-price and final billed charge | Cost and exposure interval are accounted for | Immediate billing data when AWS reporting lags |
| L27-E12 | Real AWS | Empty detector list, hub-not-enabled response, zero rules, zero queues | Named billable lab resources were removed | No unrelated resource or retained AWS billing record exists |

Finish with an explain-back: distinguish detector, finding aggregator, event router, encrypted durable target, and responder decision; explain why a sample finding is not a detection test; name the policy condition that prevents another rule from writing; state the suppression expiry behavior; report exact Region and calculated/final costs; and list residual risks. Label every observation as real AWS evidence from synthetic input, static analysis, or prediction.

## Sources

Official AWS sources, checked 2026-08-23:

- [Enabling Security Hub](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-settingup.html)
- [AWS Security Finding Format](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-findings-format.html)
- [Importing custom findings with BatchImportFindings](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-custom-providers.html)
- [Security Hub EventBridge events](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-cwe-event-formats.html)
- [Security Hub workflow status](https://docs.aws.amazon.com/securityhub/latest/userguide/finding-workflow-status.html)
- [Security Hub pricing](https://aws.amazon.com/security-hub/pricing/)
- [GuardDuty sample findings](https://docs.aws.amazon.com/guardduty/latest/ug/sample_findings.html)
- [GuardDuty foundational data sources](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_data-sources.html)
- [GuardDuty pricing](https://aws.amazon.com/guardduty/pricing/)
- [EventBridge targets and SQS permissions](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-use-resource-based.html)
- [SQS encryption at rest](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html)
- [Amazon Inspector](https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html)
- [Amazon Macie](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html)
- [IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html)
- [AWS WAF](https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html)
- [AWS Shield](https://docs.aws.amazon.com/waf/latest/developerguide/shield-chapter.html)
- [AWS Network Firewall](https://docs.aws.amazon.com/network-firewall/latest/developerguide/what-is-aws-network-firewall.html)
- [Amazon Detective](https://docs.aws.amazon.com/detective/latest/userguide/what-is-detective.html)
