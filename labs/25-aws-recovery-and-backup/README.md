# Lab: Measure AWS Backup Recovery and Tabletop Multi-Region Failover

This lab separates data recovery from traffic failover. The account-backed path backs up a tiny DynamoDB table with AWS Backup, introduces synthetic logical corruption, restores to a new table, and measures recovery. A local worksheet then accounts for Route 53, client DNS caching, multi-Region data freshness, and failback without creating an always-on second stack.

## Goal and DOP-C02 task mapping

This lab provides guided, operator-driven restore and recovery evidence relevant to **DOP-C02 Domain 3, task 3.3: Implement automated recovery processes to meet RTO and RPO requirements**. It does not automate recovery-point selection, restore initiation, data validation, or traffic movement, so it is not evidence of an automated recovery process and does not fully close task 3.3. It also supplies design evidence for task 3.1, highly available solutions, and guided data-protection evidence relevant to task 6.2.

Completion requires:

- a successful AWS Backup recovery point and a restore into a separately named DynamoDB table;
- a measured recovery time, recovery-point age, and explicit proof of which writes are present or absent;
- a Route 53 and multi-Region worksheet that bounds detection, DNS caching, stale or lost data, client behavior, traffic return, and failback;
- cleanup proof for every account-backed resource.

This is a low-cost recovery exercise, not proof of production disaster recovery. It does not test sustained load, regional evacuation, account isolation, ransomware resistance, application dependency recovery, or organizational backup policy. Continue with [availability, recovery, and resilient design](../../12-aws/04-availability-and-recovery.md) and [operations, observability, and safe automation](../../12-aws/05-operations-and-observability.md).

## Before you start

### Authorization and identity assumptions

**Use only an explicitly authorized disposable AWS sandbox. Production, shared services, customer data, and an organization's real backup vaults are out of scope.** Use a federated human or assumed role with temporary credentials. Never use the root user or create long-lived access keys.

The operator needs narrowly scoped access to:

- call `sts:GetCallerIdentity`;
- create, describe, tag, read from, write to, and delete only the two uniquely named DynamoDB tables;
- create, describe, tag, and delete only the uniquely named AWS Backup vault; start and inspect one on-demand backup, inspect and delete its recovery point, retrieve its restore metadata, and start and inspect one restore;
- create, tag, and inspect the uniquely named AWS Backup service role, attach and detach only `AWSBackupServiceRolePolicyForBackup` and `AWSBackupServiceRolePolicyForRestores`, pass only that role to AWS Backup, and delete only that role.

AWS Backup also needs permission to use the applicable encryption key. This lab uses AWS-owned or service-default encryption and synthetic data; customer-managed KMS keys are a separate recovery dependency. Supplied or precreated roles are not supported. The generated role name must be absent before creation, which makes ownership unambiguous and prevents cleanup from mutating an administrator-owned role.

Required tools are AWS CLI v2, `jq`, a POSIX shell, and GNU-compatible `date`. Use one terminal so shell variables persist.

### Time, cost, and resource bounds

- Core exercise time: 45 to 75 minutes.
- Core hard stop: 90 minutes after resource creation.
- Core cost ceiling: **USD 1.00**, after checking current prices in the chosen Region.
- Core resources: one on-demand DynamoDB table with at most 10 items and less than 10 KB, one restored table of the same bound, one backup vault, one recovery point retained for no more than one day, one AWS Backup role, and at most 50 DynamoDB API calls.
- The table uses on-demand capacity. No provisioned throughput, stream, global table, RDS/Aurora resource, EC2 instance, EBS volume, NAT gateway, Route 53 hosted zone, or health check is created.

Storage, backup storage, restore, and DynamoDB requests are the billing dimensions. Consult [AWS Backup pricing](https://aws.amazon.com/backup/pricing/) and [Amazon DynamoDB pricing](https://aws.amazon.com/dynamodb/pricing/) before starting. Billing reports are delayed and are not a hard spending cap.

### Stop conditions

Stop mutation, preserve evidence, and clean up if:

- account, principal, Region, role ownership, or sandbox approval differs from the written boundary;
- any existing table, vault, recovery point, or role would be reused or modified;
- a command names production data, an existing KMS key not approved for the lab, or a destination account;
- backup or restore remains nonterminal for 15 minutes, reports `FAILED`, or asks for broader permissions;
- more than two tables, one core recovery point, or 10 KB of data would be created;
- the core exercise approaches 90 minutes or USD 1.00;
- credentials, sensitive identifiers, or non-synthetic data appear in evidence;
- deletion protection, Vault Lock, legal hold, or policy prevents bounded cleanup.

Do not weaken Vault Lock, key policy, organization policy, or service control policy. Do not repeatedly start backup or restore jobs. A denial is diagnostic evidence and a stop condition.

### Recovery objectives and prediction

Use these lab objectives:

| Objective | Lab target | Meaning |
|---|---:|---|
| RTO | 15 minutes | From declaration of synthetic corruption until the restored table passes data checks |
| RPO | 10 minutes | Maximum acceptable age of the selected recovery point when corruption is declared |
| Restore validation | 100% of protected fixtures | The pre-backup control item and marker exist with exact values |
| Expected unprotected loss | One marker | A marker written only after backup completion must not appear in the restore |

Before starting, predict the recovery-point age at fault time, which items the restore will contain, the first evidence that distinguishes a backup failure from a restore-role failure, and why a successful table status is weaker than application-level data validation.

## Static and local path

Without an AWS account, complete:

1. the recovery-objective table;
2. the identity and encryption dependency map;
3. the Route 53 and client worksheet below;
4. a paper timeline using the example measurements in this file;
5. cleanup and evidence review.

You may model a snapshot with two local JSON files, but local copying is not AWS Backup evidence. It cannot establish service-role authorization, recovery-point state, DynamoDB backup semantics, restore metadata, encryption access, cross-Region copy behavior, or cleanup in AWS. Claims about those mechanisms require the authorized account path.

## Establish the AWS boundary

```bash
set -euo pipefail
export AWS_PAGER=""
export AWS_REGION="${AWS_REGION:-us-east-1}"

LAB_ID="dop-c02-backup-$(date -u +%Y%m%d%H%M%S)"
WORK_DIR="/tmp/$LAB_ID"
mkdir -p "$WORK_DIR/evidence"
cd "$WORK_DIR"

aws --version | tee evidence/aws-cli-version.txt
aws sts get-caller-identity | tee evidence/caller.json
ACCOUNT_ID="$(jq -r .Account evidence/caller.json)"
PRINCIPAL_ARN="$(jq -r .Arn evidence/caller.json)"
printf 'account=%s\nprincipal=%s\nregion=%s\nlab=%s\n' \
  "$ACCOUNT_ID" "$PRINCIPAL_ARN" "$AWS_REGION" "$LAB_ID" \
  | tee evidence/scope.txt

START_EPOCH="$(date -u +%s)"
printf 'started_epoch=%s\nstop_epoch=%s\n' \
  "$START_EPOCH" "$((START_EPOCH+5400))" | tee evidence/time-bound.txt
```

Stop unless the scope exactly matches the approved sandbox. Record the credential source, session expiry, authorization owner, and whether an organization policy or permissions boundary limits the principal. Do not record credentials.

## Create a tiny protected data set

Create one table and two protected items. All data is synthetic:

```bash
SOURCE_TABLE="$LAB_ID-source"
RESTORE_TABLE="$LAB_ID-restored"
VAULT_NAME="$LAB_ID-vault"
BACKUP_ROLE="$LAB_ID-role"

aws dynamodb create-table \
  --table-name "$SOURCE_TABLE" \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --tags Key=lab,Value="$LAB_ID" \
  | tee evidence/source-table-create.json
aws dynamodb wait table-exists --table-name "$SOURCE_TABLE"

PROTECTED_EPOCH="$(date -u +%s)"
aws dynamodb put-item --table-name "$SOURCE_TABLE" --item \
  "{\"id\":{\"S\":\"control\"},\"state\":{\"S\":\"healthy\"},\"sequence\":{\"N\":\"1\"},\"written_epoch\":{\"N\":\"$PROTECTED_EPOCH\"}}"
aws dynamodb put-item --table-name "$SOURCE_TABLE" --item \
  "{\"id\":{\"S\":\"protected-marker\"},\"state\":{\"S\":\"committed-before-backup\"},\"sequence\":{\"N\":\"2\"},\"written_epoch\":{\"N\":\"$PROTECTED_EPOCH\"}}"

aws dynamodb scan --table-name "$SOURCE_TABLE" --consistent-read \
  | tee evidence/source-baseline.json
test "$(jq -r .Count evidence/source-baseline.json)" = "2"
```

The strongly consistent scan establishes the fixture immediately before backup. It does not establish when AWS Backup's recovery point will represent the table.

## Create the backup identity and recovery point

Create a service role trusted only by AWS Backup:

```bash
cat > backup-trust.json <<'JSON'
{"Version":"2012-10-17","Statement":[{"Effect":"Allow",
"Principal":{"Service":"backup.amazonaws.com"},"Action":"sts:AssumeRole"}]}
JSON

if aws iam get-role --role-name "$BACKUP_ROLE" >/dev/null 2>&1; then
  printf 'Refusing to reuse an existing IAM role.\n' >&2
  exit 1
fi
aws iam create-role --role-name "$BACKUP_ROLE" \
  --assume-role-policy-document file://backup-trust.json \
  --tags Key=lab,Value="$LAB_ID" \
  | tee evidence/backup-role-create.json
aws iam attach-role-policy --role-name "$BACKUP_ROLE" \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup
aws iam attach-role-policy --role-name "$BACKUP_ROLE" \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForRestores

BACKUP_ROLE_ARN="arn:aws:iam::$ACCOUNT_ID:role/$BACKUP_ROLE"
SOURCE_TABLE_ARN="arn:aws:dynamodb:$AWS_REGION:$ACCOUNT_ID:table/$SOURCE_TABLE"
sleep 10

aws backup create-backup-vault \
  --backup-vault-name "$VAULT_NAME" \
  --backup-vault-tags lab="$LAB_ID" \
  | tee evidence/vault-create.json

BACKUP_REQUEST_EPOCH="$(date -u +%s)"
BACKUP_JOB_ID="$(aws backup start-backup-job \
  --backup-vault-name "$VAULT_NAME" \
  --resource-arn "$SOURCE_TABLE_ARN" \
  --iam-role-arn "$BACKUP_ROLE_ARN" \
  --lifecycle DeleteAfterDays=1 \
  --recovery-point-tags lab="$LAB_ID" \
  --query BackupJobId --output text)"
printf 'backup_job_id=%s\nbackup_requested_epoch=%s\n' \
  "$BACKUP_JOB_ID" "$BACKUP_REQUEST_EPOCH" \
  | tee evidence/backup-job.txt
```

Poll with a bounded loop and preserve the terminal job:

```bash
BACKUP_STATUS="CREATED"
for attempt in $(seq 1 45); do
  aws backup describe-backup-job --backup-job-id "$BACKUP_JOB_ID" \
    > evidence/backup-job-latest.json
  BACKUP_STATUS="$(jq -r .State evidence/backup-job-latest.json)"
  case "$BACKUP_STATUS" in
    COMPLETED|FAILED|ABORTED|EXPIRED) break ;;
  esac
  sleep 20
done
jq . evidence/backup-job-latest.json
test "$BACKUP_STATUS" = "COMPLETED"

RECOVERY_POINT_ARN="$(jq -r .RecoveryPointArn \
  evidence/backup-job-latest.json)"
BACKUP_COMPLETE_EPOCH="$(date -u +%s)"
aws backup describe-recovery-point \
  --backup-vault-name "$VAULT_NAME" \
  --recovery-point-arn "$RECOVERY_POINT_ARN" \
  | tee evidence/recovery-point.json
```

If the job fails, inspect `StatusMessage`, role trust, attached policies, resource ARN, Region, and key access in that order. Do not respond by attaching administrator access.

## Break it: introduce one logical corruption

Write one explicitly unprotected marker only after the backup completed, then corrupt the control item in place:

```bash
UNPROTECTED_EPOCH="$(date -u +%s)"
aws dynamodb put-item --table-name "$SOURCE_TABLE" --item \
  "{\"id\":{\"S\":\"unprotected-marker\"},\"state\":{\"S\":\"written-after-backup\"},\"sequence\":{\"N\":\"3\"},\"written_epoch\":{\"N\":\"$UNPROTECTED_EPOCH\"}}"

FAULT_EPOCH="$(date -u +%s)"
aws dynamodb update-item \
  --table-name "$SOURCE_TABLE" \
  --key '{"id":{"S":"control"}}' \
  --update-expression 'SET #s = :corrupt, sequence = :seq' \
  --expression-attribute-names '{"#s":"state"}' \
  --expression-attribute-values \
    '{":corrupt":{"S":"synthetic-corruption"},":seq":{"N":"99"}}' \
  --return-values ALL_NEW \
  | tee evidence/fault-result.json
printf 'unprotected_epoch=%s\nfault_epoch=%s\n' \
  "$UNPROTECTED_EPOCH" "$FAULT_EPOCH" | tee evidence/fault-time.txt
```

The exact fault is one bad update to a disposable item. The expected user-visible symptom is `control.state=synthetic-corruption`. The source table remains available so rollback is possible; do not delete it.

## Diagnose before restoring

Start from the bad value:

```bash
aws dynamodb get-item --table-name "$SOURCE_TABLE" \
  --key '{"id":{"S":"control"}}' --consistent-read \
  | tee evidence/source-corrupt-control.json
jq -e '.Item.state.S == "synthetic-corruption" and
  .Item.sequence.N == "99"' evidence/source-corrupt-control.json

aws backup describe-backup-job --backup-job-id "$BACKUP_JOB_ID" \
  | tee evidence/backup-job-final.json
aws backup describe-recovery-point \
  --backup-vault-name "$VAULT_NAME" \
  --recovery-point-arn "$RECOVERY_POINT_ARN" \
  | tee evidence/recovery-point-before-restore.json
```

Rank these hypotheses:

1. application logical corruption after a valid recovery point;
2. backup never completed;
3. the selected recovery point protects a different resource or Region;
4. the restore role or encryption dependency cannot read the recovery point.

The current item value proves the symptom. The backup job's `COMPLETED` state, protected resource ARN, recovery-point status, creation time, and vault identity separate hypotheses 1 through 3. Hypothesis 4 remains unproven until a restore actually starts.

## Restore and measure recovery

Ask AWS Backup for service-generated restore metadata, preserve it, and change only the destination table name:

```bash
aws backup get-recovery-point-restore-metadata \
  --backup-vault-name "$VAULT_NAME" \
  --recovery-point-arn "$RECOVERY_POINT_ARN" \
  | tee evidence/restore-metadata-source.json

jq --arg target "$RESTORE_TABLE" \
  '.RestoreMetadata + {"targetTableName":$target}' \
  evidence/restore-metadata-source.json > restore-metadata.json

RESTORE_JOB_ID="$(aws backup start-restore-job \
  --recovery-point-arn "$RECOVERY_POINT_ARN" \
  --iam-role-arn "$BACKUP_ROLE_ARN" \
  --metadata file://restore-metadata.json \
  --resource-type DynamoDB \
  --query RestoreJobId --output text)"
printf 'restore_job_id=%s\nrestore_started_epoch=%s\n' \
  "$RESTORE_JOB_ID" "$(date -u +%s)" | tee evidence/restore-job.txt

RESTORE_STATUS="PENDING"
for attempt in $(seq 1 45); do
  aws backup describe-restore-job --restore-job-id "$RESTORE_JOB_ID" \
    > evidence/restore-job-latest.json
  RESTORE_STATUS="$(jq -r .Status evidence/restore-job-latest.json)"
  case "$RESTORE_STATUS" in
    COMPLETED|FAILED|ABORTED) break ;;
  esac
  sleep 20
done
jq . evidence/restore-job-latest.json
test "$RESTORE_STATUS" = "COMPLETED"
aws dynamodb wait table-exists --table-name "$RESTORE_TABLE"
```

If restore fails, preserve `StatusMessage`. Distinguish invalid metadata, destination-name conflict, denied `iam:PassRole`, role trust, DynamoDB restore permission, and KMS access. Do not start a second restore until the specific cause is proved and the first failed job is recorded.

Validate data, not only resource state:

```bash
aws dynamodb scan --table-name "$RESTORE_TABLE" --consistent-read \
  | tee evidence/restored-table.json

jq -e '
  ([.Items[] | select(.id.S=="control" and .state.S=="healthy" and .sequence.N=="1")] | length)==1
  and
  ([.Items[] | select(.id.S=="protected-marker" and .state.S=="committed-before-backup")] | length)==1
  and
  ([.Items[] | select(.id.S=="unprotected-marker")] | length)==0
' evidence/restored-table.json

RECOVERY_VALIDATED_EPOCH="$(date -u +%s)"
CREATION_TIME="$(jq -r .CreationDate evidence/recovery-point.json)"
RECOVERY_POINT_EPOCH="$(date -u -d "$CREATION_TIME" +%s)"
RTO_SECONDS="$((RECOVERY_VALIDATED_EPOCH-FAULT_EPOCH))"
RECOVERY_POINT_AGE_SECONDS="$((FAULT_EPOCH-RECOVERY_POINT_EPOCH))"
KNOWN_UNPROTECTED_WINDOW_SECONDS="$((FAULT_EPOCH-UNPROTECTED_EPOCH))"

printf '%s\n' \
  "rto_seconds=$RTO_SECONDS" \
  "rto_target_seconds=900" \
  "recovery_point_age_at_fault_seconds=$RECOVERY_POINT_AGE_SECONDS" \
  "rpo_target_seconds=600" \
  "known_unprotected_write_window_seconds=$KNOWN_UNPROTECTED_WINDOW_SECONDS" \
  "protected_marker_present=true" \
  "post_backup_marker_present=false" \
  | tee evidence/recovery-measurements.txt

test "$RTO_SECONDS" -le 900
test "$RECOVERY_POINT_AGE_SECONDS" -le 600
```

The recovery-point age is the measured RPO proxy for this event. The observed loss is exactly the synthetic post-backup marker. Do not claim that every write in the age interval would be lost: snapshot timing and application write history determine actual loss. Conversely, a zero-item difference in another test would not prove a zero RPO.

### Return to service and failback decision

For this isolated fixture, "return to service" is a client configuration decision, not a table rename:

1. keep writes to the corrupt source frozen;
2. compare key schema, table settings, item counts, checksums for critical fixtures, encryption, tags, and required integrations;
3. point a synthetic client explicitly at `RESTORE_TABLE`;
4. perform one read and one new idempotent write, then read it back;
5. preserve the source for diagnosis until the decision record is complete;
6. choose either the restored table as the new source of truth or repair and reconcile the original; never allow unconstrained writes to both.

Run the synthetic client proof:

```bash
aws dynamodb put-item --table-name "$RESTORE_TABLE" --item \
  '{"id":{"S":"recovery-probe"},"state":{"S":"accepted-after-restore"},"sequence":{"N":"4"}}' \
  --condition-expression 'attribute_not_exists(id)'
aws dynamodb get-item --table-name "$RESTORE_TABLE" \
  --key '{"id":{"S":"recovery-probe"}}' --consistent-read \
  | tee evidence/recovery-probe.json
jq -e '.Item.state.S == "accepted-after-restore"' evidence/recovery-probe.json
```

This proves a bounded read/write path on the restored table. It does not prove application configuration, secondary indexes, streams, downstream consumers, quotas, or production correctness.

## Local Route 53 and multi-Region worksheet

This section is deliberately tabletop-only in the core lab. It creates no Route 53 record, health check, second-region service, or replicated data. The explicit scenario is:

- active-passive API in `us-east-1` and `us-west-2`;
- target RTO 15 minutes and target RPO 5 minutes;
- asynchronous data replication with observed lag required before failover;
- Route 53 failover routing with health evaluation;
- authoritative record TTL of 60 seconds;
- client connection timeout of 2 seconds, one retry to the newly resolved endpoint, and no retry of a non-idempotent request without an idempotency key;
- a conservative 5-minute client/resolver stale-cache allowance, because implementations may cache or serve stale answers beyond the intended authoritative TTL.

These are design assumptions, not measured AWS behavior. Complete the worksheet before revealing the later steps of the scenario:

| Stage | Budget or bound | Evidence required | Decision and stop |
|---|---:|---|---|
| Detect regional user impact | 2 minutes | Multi-location synthetic failures and dependency signals | Do not fail over on one probe or missing telemetry |
| Confirm secondary data freshness | Replication lag at most 5 minutes | Last applied sequence/time and integrity check | Stop if lag is unknown or corruption is replicated |
| Authoritative traffic change | 2 minutes | Route 53 change/health state and endpoint identity | Stop if secondary health or capacity is unproved |
| Recursive/client DNS convergence | 60-second TTL plus 5-minute stale-cache allowance | Queries from multiple resolvers and client logs | Keep primary isolated; expect a mixed-endpoint interval |
| Client request behavior | 2-second connect timeout, one bounded retry | Request ID, resolved address, endpoint Region, result | Never blindly replay non-idempotent writes |
| Data-loss bound | At most 5 minutes by objective | Last acknowledged primary write versus last applied secondary write | Communicate exact missing sequence range |
| RTO declaration | At most 15 minutes | Successful user transaction through secondary | Infrastructure health alone does not end recovery |

### DNS caching exercise

Model six clients that resolve at different points in a 60-second TTL. This is synthetic output, not a Route 53 measurement:

```bash
python3 - <<'PY' | tee evidence/dns-cache-model.txt
ttl = 60
elapsed_at_change = [0, 10, 20, 30, 45, 59]
for client, elapsed in enumerate(elapsed_at_change, 1):
    remaining = ttl - elapsed
    print(f"client={client} authoritative_ttl_seconds={ttl} "
          f"cache_remaining_at_change_seconds={remaining}")
print("design_stale_cache_allowance_seconds=300")
print("claim=authoritative_change_does_not_invalidate_existing_client_caches")
PY
```

Explain why TTL is not a command sent to clients, why connection pools can outlive DNS cache entries, why resolver serve-stale behavior expands uncertainty, and why retry policy affects perceived RTO.

### Tabletop event and failover

At time zero, assume the primary Region stops serving requests. The secondary is healthy, but replication lag is 80 seconds. Walk the runbook:

1. Detect impact with user-level probes in both Regions and preserve UTC request IDs.
2. Freeze or fence primary writes. A DNS change alone does not prevent direct or cached clients from reaching the old endpoint.
3. Verify secondary endpoint capacity, dependencies, certificate, secrets, role, and last applied data sequence.
4. Record 80 seconds as the current stale-data bound. Identify writes acknowledged by primary but not present in secondary; this sequence range is the possible loss bound.
5. Approve traffic movement only because 80 seconds is below the 5-minute RPO objective.
6. Observe authoritative Route 53 state and query several recursive resolvers. Expect mixed client destinations during cache convergence.
7. Send an idempotent synthetic transaction through the normal hostname, recording resolved address, Region, response, and committed sequence.
8. Declare recovery only when the transaction succeeds and the data invariant holds. Record measured RTO from time zero.

If replication lag is unknown, secondary writes fail, corruption has replicated, or RTO/RPO is breached, stop the failover exercise and escalate under the disaster-recovery decision process. This tabletop runbook does not implement failover automation.

### Failback worksheet

Failback is another risky migration, not the inverse of a DNS edit:

| Failback gate | Required proof | Rollback trigger |
|---|---|---|
| Primary rebuilt or repaired | Versioned infrastructure, dependencies, identity, and synthetic health all pass | Any unknown drift or missing dependency |
| Data authority declared | One Region is the writer; reconciliation reports no unexplained conflicts | Writes observed in both Regions without conflict policy |
| Replication caught up | Applied sequence and checksum meet the approved convergence point | Lag grows or checksum differs |
| Client exposure staged | Internal cohort, then bounded percentage, with endpoint identity in telemetry | Error, latency, correctness, or stale-read guardrail fails |
| DNS/client convergence observed | Authoritative response plus multiple resolver and client observations | Material clients remain pinned beyond stale-cache allowance |
| Secondary retained safely | Defined observation window, write fencing, and rollback route | Primary user transaction fails |
| Return to normal completed | Primary transaction and data invariant pass; temporary controls removed | Any unresolved data gap |

If failback fails, restore traffic to the still-fenced secondary, preserve both write histories, and reconcile before another attempt. Never delete the secondary merely because authoritative DNS points to the primary.

## Optional real second-Region copy and restore

This drill is optional and requires separate authorization for a second Region. It adds one destination vault, one copied recovery point, and one restored DynamoDB table for at most 90 minutes. Increase the total ceiling to **USD 3.00** only after checking cross-Region copy, backup storage, restore, DynamoDB request, KMS, and transfer prices. It still does not create Route 53, a global table, or an active application stack.

Stop if the destination Region is not approved, the source uses a KMS key without an approved destination-key design, copy remains nonterminal for 20 minutes, or any destination name already exists.

Choose and verify a distinct approved Region:

```bash
if [ "$AWS_REGION" = "us-east-1" ]; then
  DR_REGION="us-west-2"
else
  DR_REGION="us-east-1"
fi
printf 'source_region=%s\ndestination_region=%s\n' \
  "$AWS_REGION" "$DR_REGION" | tee evidence/optional-dr-scope.txt

DR_VAULT="$LAB_ID-dr-vault"
DR_TABLE="$LAB_ID-dr-restored"
aws backup create-backup-vault --region "$DR_REGION" \
  --backup-vault-name "$DR_VAULT" \
  --backup-vault-tags lab="$LAB_ID" \
  | tee evidence/optional-dr-vault.json
DR_VAULT_ARN="arn:aws:backup:$DR_REGION:$ACCOUNT_ID:backup-vault:$DR_VAULT"

COPY_JOB_ID="$(aws backup start-copy-job \
  --recovery-point-arn "$RECOVERY_POINT_ARN" \
  --source-backup-vault-name "$VAULT_NAME" \
  --destination-backup-vault-arn "$DR_VAULT_ARN" \
  --iam-role-arn "$BACKUP_ROLE_ARN" \
  --lifecycle DeleteAfterDays=1 \
  --query CopyJobId --output text)"
```

Poll `aws backup describe-copy-job --copy-job-id "$COPY_JOB_ID"` at 30-second intervals for no more than 20 minutes. Require `COMPLETED`, preserve the destination recovery-point ARN, retrieve its restore metadata in `DR_REGION`, replace `targetTableName` with `DR_TABLE`, and start a DynamoDB restore in that Region using the same bounded procedure as the core restore. Validate that the protected marker exists and the post-backup marker is absent.

Measure three separate intervals:

1. source recovery point to copy completion;
2. copy completion to restored table validation;
3. fault declaration to hypothetical client traffic readiness.

The third interval remains a design estimate because this drill does not deploy an application endpoint or move DNS. A copied and restored table is evidence of regional data recoverability, not application failover.

Before core cleanup, delete the optional restored table, delete the destination recovery point, and delete the destination vault:

```bash
aws dynamodb delete-table --region "$DR_REGION" \
  --table-name "$DR_TABLE" >/dev/null 2>&1 || true
DR_RECOVERY_POINT_ARN="$(aws backup list-recovery-points-by-backup-vault \
  --region "$DR_REGION" --backup-vault-name "$DR_VAULT" \
  --query 'RecoveryPoints[0].RecoveryPointArn' --output text)"
if [ "$DR_RECOVERY_POINT_ARN" != "None" ]; then
  aws backup delete-recovery-point --region "$DR_REGION" \
    --backup-vault-name "$DR_VAULT" \
    --recovery-point-arn "$DR_RECOVERY_POINT_ARN"
fi
aws backup delete-backup-vault --region "$DR_REGION" \
  --backup-vault-name "$DR_VAULT"
```

## Evidence record

| Claim | Evidence | What it does not prove |
|---|---|---|
| Correct identity and boundary | `caller.json`, `scope.txt`, authorization record | That every requested action is allowed |
| Fixture existed before backup | consistent baseline scan and protected timestamps | Recovery-point contents |
| AWS Backup created a usable point | completed backup job, resource ARN, vault, recovery-point metadata | Restore authorization or application usability |
| Fault occurred after backup | unprotected and fault epochs, corrupt item response | Production corruption detection |
| Restore role and metadata worked | completed restore job and destination table identity | Every schema integration or KMS scenario |
| Protected state recovered | exact control and protected-marker assertions | Writes outside the fixture |
| Unprotected state was absent | explicit missing post-backup marker | That all writes during the RPO window are always lost |
| RTO/RPO were measured | epoch inputs and calculations with units | Future performance or a production SLA |
| Restored data accepted a transaction | conditional write and consistent read | Full application readiness |
| DNS behavior was reasoned about | worksheet and synthetic cache model | Actual Route 53 or resolver convergence |
| Optional regional copy worked | copy job, destination point, regional restore assertions | End-to-end regional traffic failover |

Record prediction, observation, interpretation, and decision separately. Preserve UTC timestamps, job IDs, request IDs, exact resource ARNs, AWS CLI version, and calculations. Redact account IDs only in public copies while retaining safe correlation. Missing data is unknown, not success.

## Clean up and prove removal

Delete both tables and wait for their absence:

```bash
aws dynamodb delete-table --table-name "$RESTORE_TABLE" \
  >/dev/null 2>&1 || true
aws dynamodb delete-table --table-name "$SOURCE_TABLE" \
  >/dev/null 2>&1 || true
aws dynamodb wait table-not-exists --table-name "$RESTORE_TABLE" || true
aws dynamodb wait table-not-exists --table-name "$SOURCE_TABLE" || true
```

Delete the recovery point before deleting its vault:

```bash
aws backup delete-recovery-point \
  --backup-vault-name "$VAULT_NAME" \
  --recovery-point-arn "$RECOVERY_POINT_ARN" \
  >/dev/null 2>&1 || true

for attempt in $(seq 1 20); do
  POINT_COUNT="$(aws backup list-recovery-points-by-backup-vault \
    --backup-vault-name "$VAULT_NAME" \
    --query 'length(RecoveryPoints)' --output text)"
  [ "$POINT_COUNT" = "0" ] && break
  sleep 15
done
test "$POINT_COUNT" = "0"
aws backup delete-backup-vault --backup-vault-name "$VAULT_NAME"
```

Detach and remove only the lab-created role. Its name passed the absence check before this lab created it; if that check was not observed, stop instead of running these IAM commands:

```bash
aws iam detach-role-policy --role-name "$BACKUP_ROLE" \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup \
  >/dev/null 2>&1 || true
aws iam detach-role-policy --role-name "$BACKUP_ROLE" \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForRestores \
  >/dev/null 2>&1 || true
aws iam delete-role --role-name "$BACKUP_ROLE" >/dev/null 2>&1 || true
```

Prove absence:

```bash
test "$(aws dynamodb describe-table --table-name "$SOURCE_TABLE" \
  --query 'Table.TableArn' --output text 2>/dev/null \
  || printf absent)" = "absent"
test "$(aws dynamodb describe-table --table-name "$RESTORE_TABLE" \
  --query 'Table.TableArn' --output text 2>/dev/null \
  || printf absent)" = "absent"
test "$(aws backup describe-backup-vault --backup-vault-name "$VAULT_NAME" \
  --query 'BackupVaultArn' --output text 2>/dev/null \
  || printf absent)" = "absent"
test "$(aws iam get-role --role-name "$BACKUP_ROLE" \
  --query 'Role.Arn' --output text 2>/dev/null \
  || printf absent)" = "absent"
printf 'cleanup_verified_at=%s\n' "$(date -u +%FT%TZ)" \
  | tee evidence/cleanup-proof.txt
```

If optional regional resources were created, rerun their absence checks with `--region "$DR_REGION"`. A lifecycle setting is a fallback, not cleanup proof. If a vault or point remains, stop other work and ask the sandbox owner to remove the exact ARN; never weaken a retention control.

## What to keep and explain back

Keep the identity proof, objectives, baseline, job metadata, fault timeline, ranked hypotheses, restore metadata, exact data assertions, measured durations, stale/lost-data bounds, DNS worksheet, failback gates, optional-drill status, and cleanup proof.

Explain without notes:

1. why backup completion does not make an application recovered;
2. how measured RTO differs from service restore duration;
3. how recovery-point age, replication lag, and observed missing writes differ;
4. why DNS failover can produce a mixed-endpoint interval;
5. why failback requires write authority, reconciliation, client observation, and a rollback route;
6. what an optional second-Region table restore still cannot prove.

## Sources

Product behavior and command shape were reviewed against the linked AWS documentation on 2026-08-23. Recheck restore metadata, service-role policies, pricing, and regional support when AWS Backup, DynamoDB, Route 53, or AWS CLI changes.

- [DOP-C02 Domain 3 task statements](https://docs.aws.amazon.com/aws-certification/latest/devops-engineer-professional-02/devops-engineer-professional-02-domain3.html)
- [Creating on-demand backups with AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/recov-point-create-on-demand-backup.html)
- [Restoring a backup with AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-a-backup.html)
- [AWS Backup advanced DynamoDB backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/advanced-ddb-backup.html)
- [Restore an Amazon DynamoDB table with AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-dynamodb.html)
- [AWS Backup service roles](https://docs.aws.amazon.com/aws-backup/latest/devguide/iam-service-roles.html)
- [Copying a backup across AWS Regions](https://docs.aws.amazon.com/aws-backup/latest/devguide/cross-region-backup.html)
- [DynamoDB on-demand backup and restore](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/BackupRestore.html)
- [Route 53 DNS failover](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html)
- [Route 53 TTL behavior](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-values-basic.html#rrsets-values-basic-ttl)
- [AWS disaster recovery options](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html)
