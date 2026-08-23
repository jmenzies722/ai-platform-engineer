# Lab: Review AWS Organization Governance and Audit Controls

This lab turns organization governance claims into inspectable evidence. The local path is fully runnable without AWS and tests service control policy reasoning against a static single-account fixture. The optional cloud extension is deliberately limited to an existing, isolated AWS Organizations sandbox whose owner has authorized organization-wide reads, one non-mutating SCP authorization probe, and one denied deletion of a retained synthetic archive object.

The lab supports DOP-C02 task statements **2.2** (account onboarding and governance in multi-account environments), **4.2** (audit and analyze logs), **6.1** (identity and access management at scale), and **6.3** (security monitoring and auditing). A local pass demonstrates policy reasoning and evidence discipline. It does not demonstrate operation of AWS Organizations, an organization trail, delegated administration, or a cross-account AWS Config aggregator.

## Goal

Produce an evidence bundle that explains an explicit SCP deny, distinguishes a permissions ceiling from a permission grant, checks an account baseline and delegated-administrator record, reviews centralized CloudTrail and AWS Config evidence, attributes a harmless dry-run denial to the SCP, and attributes a separate archive deletion denial to S3 Object Lock compliance retention.

## Before you start

Read [Accounts, IAM, and the AWS API](../../12-aws/01-identity-and-api.md), [Operations, observability, and safe automation](../../12-aws/05-operations-and-observability.md), and [Cost models, allocation, and optimization](../../12-aws/06-cost-and-governance.md). The relevant certification gaps are recorded in the [DOP-C02 overlay](../../certs/aws-dop-c02.md#aws-specific-gap-register).

### Choose one path

The local path requires Python 3.9 or newer, a POSIX shell, and no credentials. It takes 45 to 60 minutes, creates less than 100 KB under `.work`, and has no AWS cost.

The cloud extension takes 60 to 90 minutes. It is a review of controls that already exist in a purpose-built organization sandbox. The commands create no accounts, organization, SCP, trail, bucket, aggregator, or delegated administrator. AWS Organizations itself has no additional charge, but existing CloudTrail, S3, KMS, and AWS Config usage continues to incur the sandbox owner's normal charges. The extension makes fewer than 100 control-plane requests and should add less than USD 1 of request or log-event cost. Stop after 90 minutes or if the owner reports USD 1 of incremental spend, whichever occurs first.

### Identity assumptions

For the local path, use an unprivileged local user. The fixture's `AuditReviewer` and `MemberOperator` names are synthetic identities, not credentials.

For the cloud extension, the organization owner must provide two short-lived federated profiles:

- `approved-org-audit` is a read-only role in the management account or a separately approved audit account. It can read Organizations, CloudTrail, S3 protection settings, and AWS Config aggregator metadata. It cannot alter those controls.
- `approved-member-scp-probe` is a role in one disposable member account. Its identity policy allows `ec2:CreateTags` on one approved disposable instance and `sts:DecodeAuthorizationMessage`. The SCP explicitly denies `ec2:CreateTags` when the request contains the tag key `GovernanceProbe`. The command uses EC2 dry-run, so authorization is evaluated but no tag can be written.
- `approved-archive-retention-test` is a role approved by the archive owner. Its identity policy and the bucket policy allow `s3:DeleteObjectVersion` only for one pre-created synthetic test-object version. That version is under active S3 Object Lock `COMPLIANCE` retention. The role cannot bypass governance retention, change retention, delete CloudTrail log objects, or change the bucket.

Do not use the root user, long-lived access keys, a production management account, a personal account, or an ordinary single-account sandbox. An ordinary sandbox cannot create or control an organization and is not suitable evidence for the cloud extension. Never create an organization merely to complete this lab.

> **Do not run the cloud extension in production, a shared organization, or an organization containing customer data.** Use only an explicitly isolated organization sandbox with written approval for the named roles, trail, member account, Region, time window, and denied API call.

### Stop conditions

Stop immediately if any of these conditions occurs:

- `get-caller-identity` returns an unapproved account or role, credentials are not short lived, or the Region differs from the approved trail home Region.
- The organization has more than 10 accounts, the target is not a disposable member account, or any output contains customer data or secrets.
- The trail is not an existing organization trail, is already not logging, or its bucket and encryption protections do not match the owner's baseline.
- The probe SCP, identity-policy allow, exact disposable instance, encoded authorization-message decoder, synthetic archive object version, delete allow, and active compliance retention have not all been reviewed before the negative tests.
- Any command would create, invite, move, close, remove, deregister, delete, detach, disable, or modify an account or organization control.
- A supposedly denied command succeeds, a cost or time bound is reached, audit evidence cannot be retained safely, or cleanup proof is incomplete.

Do not automate account removal. Removing an account has prerequisites and billing and recovery consequences that are outside this lab. Organization teardown is never a cleanup step here.

Before either path, predict the result: an identity-policy allow cannot override an applicable explicit deny; the protected operation should fail, and the protected trail should remain logging.

## Establish a local baseline

Create a clean local workspace and verify the interpreter. Refuse to overwrite evidence from an earlier run.

```bash
test ! -e .work || { printf '%s\n' '.work already exists; inspect or remove it first' >&2; exit 1; }
mkdir -p .work/input .work/evidence
python3 --version | tee .work/evidence/python-version.txt
date -u +%Y-%m-%dT%H:%M:%SZ | tee .work/evidence/started-at.txt
```

Create the synthetic SCP. One statement supplies a harmless, condition-specific governance probe by denying `ec2:CreateTags` only when the request includes `GovernanceProbe`. A separate statement models protection for audit controls and exposes its break-glass exception. The local evaluator tests the probe statement; it does not claim to reproduce service-specific CloudTrail or S3 authorization.

```bash
cat >.work/input/scp.json <<'JSON'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyGovernanceProbeTag",
      "Effect": "Deny",
      "Action": "ec2:CreateTags",
      "Resource": "*",
      "Condition": {
        "ForAnyValue:StringEquals": {
          "aws:TagKeys": "GovernanceProbe"
        }
      }
    },
    {
      "Sid": "DenyAuditTamperingExceptBreakGlass",
      "Effect": "Deny",
      "Action": [
        "cloudtrail:DeleteTrail",
        "cloudtrail:StopLogging",
        "s3:DeleteBucketPolicy",
        "s3:PutBucketPolicy",
        "s3:PutBucketVersioning"
      ],
      "Resource": "*",
      "Condition": {
        "ArnNotLike": {
          "aws:PrincipalArn": "arn:aws:iam::*:role/OrganizationAuditBreakGlass"
        }
      }
    }
  ]
}
JSON
```

Create a single-account review fixture. It represents one member account, its baseline, a delegated administrator record, an organization trail backed by a versioned archive, and a Config aggregator source. These records are synthetic and cannot close the organization-scale evidence gap.

```bash
cat >.work/input/org-state.json <<'JSON'
{
  "organization": {
    "id": "o-examplefixture",
    "managementAccountId": "111122223333",
    "featureSet": "ALL"
  },
  "accounts": [
    {
      "id": "444455556666",
      "name": "lab-member",
      "status": "ACTIVE",
      "baseline": {
        "federatedAccessRole": true,
        "rootMfaRecorded": true,
        "rootAccessKeys": 0,
        "organizationTrailCovered": true,
        "configAggregatorCovered": true
      }
    }
  ],
  "delegatedAdministrators": [
    {
      "accountId": "777788889999",
      "servicePrincipal": "config-multiaccountsetup.amazonaws.com"
    }
  ],
  "trail": {
    "name": "organization-audit",
    "isOrganizationTrail": true,
    "isLogging": true,
    "multiRegion": true,
    "logFileValidation": true,
    "archiveVersioning": "Enabled",
    "archiveDeletionDeniedForMembers": true
  },
  "configAggregator": {
    "name": "organization-config",
    "allAccounts": true,
    "allRegions": true,
    "lastUpdatedStatus": "SUCCEEDED"
  }
}
JSON

cat >.work/input/requests.json <<'JSON'
[
  {
    "case": "governance-probe-tag",
    "principalArn": "arn:aws:iam::444455556666:role/GovernanceProbe",
    "action": "ec2:CreateTags",
    "tagKeys": ["GovernanceProbe"],
    "identityAllows": true,
    "expected": "DENY"
  },
  {
    "case": "ordinary-owner-tag",
    "principalArn": "arn:aws:iam::444455556666:role/GovernanceProbe",
    "action": "ec2:CreateTags",
    "tagKeys": ["Owner"],
    "identityAllows": true,
    "expected": "ALLOW"
  },
  {
    "case": "ungranted-probe-tag",
    "principalArn": "arn:aws:iam::444455556666:role/UnprivilegedFixture",
    "action": "ec2:CreateTags",
    "tagKeys": ["GovernanceProbe"],
    "identityAllows": false,
    "expected": "DENY"
  },
  {
    "case": "member-read-instance",
    "principalArn": "arn:aws:iam::444455556666:role/GovernanceProbe",
    "action": "ec2:DescribeInstances",
    "tagKeys": [],
    "identityAllows": true,
    "expected": "ALLOW"
  }
]
JSON
```

The baseline is healthy only if the files parse and the fixture remains bounded to one member account.

```bash
python3 - <<'PY' | tee .work/evidence/baseline.txt
import json
from pathlib import Path

root = Path(".work/input")
scp = json.loads((root / "scp.json").read_text())
state = json.loads((root / "org-state.json").read_text())
requests = json.loads((root / "requests.json").read_text())
assert scp["Version"] == "2012-10-17"
assert len(state["accounts"]) == 1
assert len(requests) == 4
print("PASS parsed fixture")
print("PASS one disposable member account")
print("PASS four bounded authorization cases")
PY
```

## Make the policy and audit review work

Create a reviewer that evaluates only the policy shape used by this fixture. It is not a general IAM evaluator. It makes the decision order explicit: an applicable SCP deny wins; otherwise the identity layer still needs an allow. It also checks the account, delegated administrator, trail, archive, and aggregator claims.

```bash
cat >.work/review.py <<'PY'
import json
from pathlib import Path

inputs = Path(".work/input")
evidence = Path(".work/evidence")
scp = json.loads((inputs / "scp.json").read_text())
state = json.loads((inputs / "org-state.json").read_text())
requests = json.loads((inputs / "requests.json").read_text())

statement = next(
    item for item in scp["Statement"]
    if item["Sid"] == "DenyGovernanceProbeTag"
)
denied_action = statement["Action"]
denied_tag_key = statement["Condition"]["ForAnyValue:StringEquals"]["aws:TagKeys"]

def decision(request):
    action_matches = request["action"] == denied_action
    tag_condition_matches = denied_tag_key in request["tagKeys"]
    if action_matches and tag_condition_matches:
        return "DENY", "applicable explicit SCP deny for GovernanceProbe tag key"
    if not request["identityAllows"]:
        return "DENY", "no identity-policy allow"
    return "ALLOW", "no applicable SCP deny and identity layer allows"

rows = []
failures = []
for request in requests:
    observed, reason = decision(request)
    status = "PASS" if observed == request["expected"] else "FAIL"
    rows.append((f"policy:{request['case']}", request["expected"], observed, status, reason))
    if status == "FAIL":
        failures.append(request["case"])

account = state["accounts"][0]
baseline = account["baseline"]
checks = {
    "account:active": account["status"] == "ACTIVE",
    "account:federated-role": baseline["federatedAccessRole"],
    "account:root-mfa-recorded": baseline["rootMfaRecorded"],
    "account:no-root-keys": baseline["rootAccessKeys"] == 0,
    "delegated-admin:config": any(
        item["servicePrincipal"] == "config-multiaccountsetup.amazonaws.com"
        for item in state["delegatedAdministrators"]
    ),
    "trail:organization-and-logging": (
        state["trail"]["isOrganizationTrail"] and state["trail"]["isLogging"]
    ),
    "trail:validation-and-archive": (
        state["trail"]["logFileValidation"]
        and state["trail"]["archiveVersioning"] == "Enabled"
        and state["trail"]["archiveDeletionDeniedForMembers"]
    ),
    "config:organization-aggregation": (
        state["configAggregator"]["allAccounts"]
        and state["configAggregator"]["allRegions"]
        and state["configAggregator"]["lastUpdatedStatus"] == "SUCCEEDED"
    ),
}
for claim, passed in checks.items():
    observed = "true" if passed else "false"
    status = "PASS" if passed else "FAIL"
    rows.append((claim, "true", observed, status, "synthetic fixture field"))
    if not passed:
        failures.append(claim)

with (evidence / "review.tsv").open("w") as output:
    output.write("claim\texpected\tobserved\tstatus\treason\n")
    for row in rows:
        output.write("\t".join(row) + "\n")

print(f"reviewed={len(rows)} failures={len(failures)}")
print("result=" + ("PASS" if not failures else "FAIL"))
if failures:
    print("failed=" + ",".join(failures))
    raise SystemExit(1)
PY

python3 .work/review.py | tee .work/evidence/review-summary.txt
sed -n '1,20p' .work/evidence/review.tsv
sha256sum .work/input/*.json .work/evidence/review.tsv | tee .work/evidence/hashes.txt
```

The expected summary is `result=PASS`. The first authorization row must say `DENY` because the explicit SCP deny applies to the `GovernanceProbe` tag key even though the identity layer allows `ec2:CreateTags`. The ordinary tag case says `ALLOW` only at the two layers represented by the fixture. It does not prove that a live request would be authorized by every applicable AWS policy and service control.

## Break it

Introduce one local fault: change the synthetic archive versioning status from `Enabled` to `Suspended`. This does not call AWS.

```bash
cp .work/input/org-state.json .work/input/org-state.good.json
python3 - <<'PY'
import json
from pathlib import Path

path = Path(".work/input/org-state.json")
data = json.loads(path.read_text())
data["trail"]["archiveVersioning"] = "Suspended"
path.write_text(json.dumps(data, indent=2) + "\n")
PY

set +e
python3 .work/review.py >.work/evidence/broken-review.txt 2>&1
status=$?
set -e
test "$status" -eq 1
grep 'trail:validation-and-archive' .work/evidence/review.tsv
```

The expected symptom is a failed `trail:validation-and-archive` claim. Do not change the SCP at the same time.

## Diagnose it and recover

Start with the failed claim, not with a policy edit. The main competing explanations are malformed input, disabled log-file validation, suspended versioning, and missing member deletion protection.

```bash
python3 - <<'PY'
import json
from pathlib import Path

state = json.loads(Path(".work/input/org-state.json").read_text())
trail = state["trail"]
for key in ("logFileValidation", "archiveVersioning", "archiveDeletionDeniedForMembers"):
    print(f"{key}={trail[key]}")
PY
```

`archiveVersioning=Suspended` discriminates this fault from the other hypotheses. Restore the known-good fixture and prove the complete review passes again.

```bash
mv .work/input/org-state.good.json .work/input/org-state.json
python3 .work/review.py | tee .work/evidence/recovery-summary.txt
grep $'trail:validation-and-archive\ttrue\ttrue\tPASS' .work/evidence/review.tsv
```

This proves recovery of the local fixture, not repair of an S3 bucket.

## Optional authorized AWS Organizations extension

Run this section only when every cloud identity assumption and approval is satisfied. The organization owner must pre-provision the organization, accounts, baseline, SCP attachment, organization trail, protected archive, and Config aggregator. This extension reviews and safely challenges those controls; it does not build them.

### Capture identity and organization scope

```bash
test ! -e .work/cloud || { printf '%s\n' '.work/cloud already exists; inspect it first' >&2; exit 1; }
mkdir -p .work/cloud/audit .work/cloud/member .work/cloud/archive
export AWS_PROFILE=approved-org-audit
export AWS_PAGER=
export AWS_REGION=us-east-1

aws --version 2>&1 | tee .work/cloud/aws-version.txt
aws sts get-caller-identity | tee .work/cloud/audit/caller.json
aws organizations describe-organization | tee .work/cloud/audit/organization.json
aws organizations list-accounts --max-results 10 | tee .work/cloud/audit/accounts.json
aws organizations list-delegated-administrators --max-results 10 \
  | tee .work/cloud/audit/delegated-administrators.json
```

Manually compare the caller account and role, organization ID, management account, account count, and active member account with the signed approval. Redact account IDs and email addresses only in derivative evidence; preserve raw files in the approved encrypted location.

Record the exact SCP attached to the disposable member target. `list-policies-for-target` requires the member account ID, which is selected from the approved record rather than guessed.

```bash
read -r MEMBER_ACCOUNT_ID
test -n "$MEMBER_ACCOUNT_ID"
aws organizations list-policies-for-target \
  --target-id "$MEMBER_ACCOUNT_ID" --filter SERVICE_CONTROL_POLICY \
  | tee .work/cloud/audit/member-scps.json
```

For each returned custom SCP ID, retrieve its content and save it under `.work/cloud/audit/`. Do not detach or edit it.

```bash
read -r SCP_ID
test -n "$SCP_ID"
aws organizations describe-policy --policy-id "$SCP_ID" \
  | tee ".work/cloud/audit/scp-${SCP_ID}.json"
```

The review must identify `DenyGovernanceProbeTag` or an equivalent approved statement: `Effect=Deny`, `Action=ec2:CreateTags`, and a condition matching only the `GovernanceProbe` request tag key. Record its target attachment and the probe role's separate identity-policy allow on the exact disposable instance. An SCP does not grant the operation. Stop if the identity allow, tag-key condition, target attachment, disposable instance ownership, or permission to decode the authorization message is absent.

### Review the account baseline and delegated administration

For the approved member account, retain evidence for active status, approved OU placement, federated access path, root MFA monitoring, absence of root access keys, organization-trail coverage, Config coverage, and owner/cost tags. Some baseline controls are visible only through the owner's control system; record `unknown` rather than inferring compliance.

Delegated administration evidence must contain the delegated account ID, service principal, registration time when available, and approval record. `list-delegated-administrators` proves registration state; it does not prove the delegated administrator is healthy or least privileged.

### Review the organization trail and protected archive

```bash
aws cloudtrail describe-trails --include-shadow-trails \
  | tee .work/cloud/audit/trails.json
```

Read the approved organization trail name and home Region from that output, then set them exactly.

```bash
read -r TRAIL_NAME
read -r TRAIL_HOME_REGION
test -n "$TRAIL_NAME" && test -n "$TRAIL_HOME_REGION"
aws cloudtrail get-trail --name "$TRAIL_NAME" --region "$TRAIL_HOME_REGION" \
  | tee .work/cloud/audit/trail.json
aws cloudtrail get-trail-status --name "$TRAIL_NAME" --region "$TRAIL_HOME_REGION" \
  | tee .work/cloud/audit/trail-status-before.json
```

Continue only if `IsOrganizationTrail` and `IsMultiRegionTrail` are true, log-file validation is enabled, and `IsLogging` is true. Read the archive bucket name from the trail record.

```bash
read -r ARCHIVE_BUCKET
test -n "$ARCHIVE_BUCKET"
aws s3api get-bucket-versioning --bucket "$ARCHIVE_BUCKET" \
  | tee .work/cloud/audit/archive-versioning.json
aws s3api get-public-access-block --bucket "$ARCHIVE_BUCKET" \
  | tee .work/cloud/audit/archive-public-access.json
aws s3api get-bucket-policy --bucket "$ARCHIVE_BUCKET" \
  | tee .work/cloud/audit/archive-policy.json
aws s3api get-bucket-encryption --bucket "$ARCHIVE_BUCKET" \
  | tee .work/cloud/audit/archive-encryption.json
```

If the approved design uses S3 Object Lock, review it without treating absence as an API error to ignore:

```bash
set +e
aws s3api get-object-lock-configuration --bucket "$ARCHIVE_BUCKET" \
  >.work/cloud/audit/archive-object-lock.json \
  2>.work/cloud/audit/archive-object-lock-error.txt
object_lock_status=$?
set -e
printf 'object_lock_query_status=%s\n' "$object_lock_status" \
  | tee .work/cloud/audit/archive-object-lock-status.txt
```

Protection evidence must show the intended retention mechanism, principals allowed to write and read, denial of member-account deletion or policy weakening, encryption, and versioning. Versioning alone is not immutability. A bucket policy alone also does not override permissions held by the bucket-owning account's administrators.

### Review the AWS Config aggregator

```bash
aws configservice describe-configuration-aggregators \
  | tee .work/cloud/audit/config-aggregators.json
aws configservice describe-configuration-aggregator-sources-status \
  | tee .work/cloud/audit/config-source-status.json
```

Set the approved aggregator name from the returned record and request a bounded resource count.

```bash
read -r AGGREGATOR_NAME
test -n "$AGGREGATOR_NAME"
aws configservice get-aggregate-discovered-resource-counts \
  --configuration-aggregator-name "$AGGREGATOR_NAME" \
  --limit 20 \
  | tee .work/cloud/audit/config-resource-counts.json
```

The source status must account for the disposable member and expected Regions. A successful source status proves recent aggregation for that source; it does not prove every resource type is recorded or every rule is compliant.

### Prove the SCP with a non-mutating authorization probe

Select the one approved disposable instance from the member-account baseline. Confirm its `LabId` before the probe. EC2 dry-run checks authorization but does not perform `CreateTags`, whether authorization succeeds or fails.

```bash
export AWS_PROFILE=approved-member-scp-probe
aws sts get-caller-identity | tee .work/cloud/member/caller.json
read -r PROBE_INSTANCE_ID
test -n "$PROBE_INSTANCE_ID"
aws ec2 describe-instances --instance-ids "$PROBE_INSTANCE_ID" \
  --query 'Reservations[0].Instances[0].{State:State.Name,Tags:Tags}' \
  | tee .work/cloud/member/probe-instance.json

set +e
aws ec2 create-tags --resources "$PROBE_INSTANCE_ID" \
  --tags Key=GovernanceProbe,Value=denied --dry-run \
  >.work/cloud/member/probe-output.txt \
  2>.work/cloud/member/probe-error.txt
probe_status=$?
set -e
printf 'probe_exit_status=%s\n' "$probe_status" \
  | tee .work/cloud/member/probe-status.txt
test "$probe_status" -ne 0
```

The expected error is `UnauthorizedOperation`, not `DryRunOperation`. `DryRunOperation` means the request would be allowed and is a stop condition. Read the encoded authorization message from the error into the shell without publishing it, then decode it with the approved role.

```bash
read -r ENCODED_MESSAGE
test -n "$ENCODED_MESSAGE"
aws sts decode-authorization-message --encoded-message "$ENCODED_MESSAGE" \
  | tee .work/cloud/member/probe-decoded.json
aws ec2 describe-tags \
  --filters "Name=resource-id,Values=$PROBE_INSTANCE_ID" \
  | tee .work/cloud/member/probe-tags-after.json
```

Count this as live SCP evidence only when the decoded decision identifies an Organizations policy explicit deny matching the retrieved SCP statement and the `GovernanceProbe` condition, while the identity-policy allow and exact target attachment are present. The after-query must show that no `GovernanceProbe` tag was created. A plain `UnauthorizedOperation` without the decoded policy evidence is an unattributed denial and does not satisfy the evidence row.

### Test archive tamper resistance independently

The archive owner must pre-create one synthetic object version solely for this test and place that version under active S3 Object Lock `COMPLIANCE` retention. Do not target a CloudTrail log object. Switch to the narrow archive test role, set the owner-provided object key and version ID, and inspect the exact version.

```bash
export AWS_PROFILE=approved-archive-retention-test
aws sts get-caller-identity | tee .work/cloud/archive/caller.json
read -r TEST_OBJECT_KEY
read -r TEST_OBJECT_VERSION
test -n "$TEST_OBJECT_KEY" && test -n "$TEST_OBJECT_VERSION"
aws s3api head-object --bucket "$ARCHIVE_BUCKET" --key "$TEST_OBJECT_KEY" \
  --version-id "$TEST_OBJECT_VERSION" \
  | tee .work/cloud/archive/object-before.json
aws s3api get-object-retention --bucket "$ARCHIVE_BUCKET" --key "$TEST_OBJECT_KEY" \
  --version-id "$TEST_OBJECT_VERSION" \
  | tee .work/cloud/archive/retention.json
```

Continue only if the returned mode is `COMPLIANCE`, `RetainUntilDate` is in the future, the identity and bucket policies allow `s3:DeleteObjectVersion` for only this synthetic version, and no separate explicit deny applies to the test request. Attempt exactly one deletion.

```bash
set +e
aws s3api delete-object --bucket "$ARCHIVE_BUCKET" --key "$TEST_OBJECT_KEY" \
  --version-id "$TEST_OBJECT_VERSION" \
  >.work/cloud/archive/delete-output.txt \
  2>.work/cloud/archive/delete-error.txt
archive_delete_status=$?
set -e
printf 'archive_delete_exit_status=%s\n' "$archive_delete_status" \
  | tee .work/cloud/archive/delete-status.txt
test "$archive_delete_status" -ne 0
aws s3api head-object --bucket "$ARCHIVE_BUCKET" --key "$TEST_OBJECT_KEY" \
  --version-id "$TEST_OBJECT_VERSION" \
  | tee .work/cloud/archive/object-after.json
```

The expected error is `AccessDenied`, and the same version remains readable by the approved test role. Under the stated policy preconditions, the active compliance retention is the denying mechanism: a protected object version cannot be overwritten or deleted, including by the root user, before its retention date. If another explicit deny applies or retention is not active compliance mode, record the result as unattributed and do not count it.

```bash
export AWS_PROFILE=approved-org-audit
aws cloudtrail get-trail-status --name "$TRAIL_NAME" --region "$TRAIL_HOME_REGION" \
  | tee .work/cloud/audit/trail-status-after.json
date -u +%Y-%m-%dT%H:%M:%SZ | tee .work/cloud/completed-at.txt
sha256sum .work/cloud/audit/* .work/cloud/member/* .work/cloud/archive/* \
  | tee .work/cloud/evidence-hashes.txt
```

Ask the audit owner to locate both denied requests by principal, event name, Region, and test timestamp in the central event store. Preserve event IDs, times, error codes, recipient accounts, session issuers, resources, and trail source without publishing account IDs, object keys, or source IP addresses.

## Exact evidence record

Complete every row. `Local` means the static fixture can support the claim. `Organization required` means only the authorized cloud extension can supply valid evidence.

| Evidence ID | DOP-C02 ID | Exact artifact and required observation | Path | Claim limit |
|---|---|---|---|---|
| GOV-01 | 6.1 | Caller identity, credential source, account, role, and approval match | Organization required | Does not prove least privilege |
| GOV-02 | 2.2 | Organization ID, management account, feature set, active member count, and approved OU placement | Organization required | Does not prove onboarding controls operate |
| GOV-03 | 2.2, 6.1 | Account baseline records federated role, root controls, trail coverage, Config coverage, and owner | Local reasoning; organization required for live proof | Local fixture is synthetic |
| GOV-04 | 2.2, 6.1 | Delegated administrator account and service principal match approval | Local reasoning; organization required for live proof | Registration does not prove service health |
| GOV-05 | 6.1 | Attached SCP contains the reviewed `GovernanceProbe` explicit deny, tag-key condition, and target attachment | Local reasoning; organization required for attachment proof | SCP does not grant permissions |
| AUD-01 | 4.2, 6.3 | Trail record says organization trail, multi-Region, validation enabled, and logging | Organization required | Configuration does not prove delivery |
| AUD-02 | 6.3 | Archive evidence shows versioning, encryption, public-access block, writer/readers, deletion controls, and retention mechanism | Organization required | Versioning alone is not immutability |
| AUD-03 | 4.2, 6.3 | Config aggregator source status covers the approved account and Regions, with bounded resource counts | Organization required | Does not prove all resource types are recorded |
| SCP-01 | 6.1 | EC2 dry-run returns `UnauthorizedOperation`; decoded authorization identifies the attached Organizations explicit deny; no probe tag exists afterward | Organization required | Proves this bounded SCP condition, not every SCP path |
| ARC-01 | 6.3 | Exact synthetic object version has active compliance retention; allowed delete fails; the same version remains | Organization required | Valid only when no other deny applies and retention is still active |
| NEG-01 | 4.2, 6.3 | Central audit events correlate both probes by event ID, time, principal session, action, resource, account, and error | Organization required | Two events do not prove retention duration |
| REC-01 | 6.3 | Before and after trail status show `IsLogging=true`, and retained synthetic object version is unchanged | Organization required | Does not prove no unrelated control changed |
| LOC-01 | 6.1 | `review.tsv` passes all policy cases, including explicit deny precedence and missing-allow denial | Local | Simplified evaluator is not AWS authorization |
| LOC-02 | 4.2, 6.3 | Broken archive fixture fails, diagnosis identifies suspended versioning, and restored fixture passes | Local | Does not repair or inspect AWS |
| CLN-01 | 2.2, 6.3 | Local files removed; cloud extension records that it created no AWS resources and owner confirms controls remain | Both | Organization/account teardown is out of scope |

For each row, add timestamp, raw file, SHA-256, observation, interpretation, contradictory evidence, redactions, and reviewer. Missing permission or missing telemetry is `unknown`, not `pass`.

## Failure diagnosis and recovery

Use the symptom to select the first discriminating check.

| Symptom | Competing explanations | First evidence | Recovery |
|---|---|---|---|
| `AccessDenied` on organization reads | Wrong role, management-only API, SCP, or session boundary | Caller identity and exact API error | Stop; have the owner correct only the approved read path |
| Trail absent | Wrong Region, shadow-trail behavior, missing permission, or no trail | `describe-trails` output and caller | Correct Region or record an evidence gap; never create a trail here |
| Trail not logging before test | Existing incident or wrong trail | `trail-status-before.json` | Stop and hand control to the owner |
| Archive protection query fails | Missing read permission, unsupported control, or absent protection | API error code and approved design | Record unknown; owner validates out of band |
| Config source stale or failed | Recorder, delivery, authorization, or aggregator issue | Per-source status and last error | Do not change Config; give the evidence to its owner |
| Dry-run returns `DryRunOperation` | Probe SCP missing, wrong target attachment, or condition mismatch | Decoded result, retrieved SCP, target, and requested tag key | Stop; do not run a non-dry-run request |
| Dry-run denial cannot be decoded to an SCP statement | Missing decoder permission, another policy layer, or no encoded context | Exact EC2 error and decoded authorization document | Record unattributed denial; do not claim SCP enforcement |
| Synthetic object deletion succeeds | Retention expired, wrong version, wrong mode, or archive protection failure | Retention record, version ID, delete event, and after-query | Stop immediately, notify the archive owner, and preserve evidence |
| Object deletion fails but another deny applies | Bucket, identity, boundary, session, or SCP deny also matches | All applicable policies and retention record | Record unattributed denial; do not claim Object Lock caused it |
| Local reviewer unexpectedly passes broken fixture | Wrong file edited or check bypassed | Hashes, current JSON field, and `review.tsv` | Restore the script from the lab and repeat from a clean `.work` |

Recovery is complete only when the local fixture passes after restoration and, if the extension ran, the owner verifies the organization trail still logs, the Config aggregator remains unchanged, the synthetic archive version remains retained, and neither probe mutated a resource.

## Clean up and prove it

The cloud extension created no AWS resource, so there is no cloud deletion command. The owner-created synthetic retained version remains until its compliance retention expires and must be handled by the archive owner's lifecycle policy. Do not delete the trail, archive, aggregator, SCP, delegated administrator, member account, or organization. The account owner must confirm the reviewed controls remain in their starting state and retain the raw cloud evidence according to policy.

Remove local copies only after approved evidence has been transferred. First prove that no credential-shaped environment variables will be retained in the evidence:

```bash
env | awk -F= '/^AWS_(ACCESS_KEY_ID|SECRET_ACCESS_KEY|SESSION_TOKEN)=/{print $1}' \
  | tee .work/credential-variable-names.txt
unset AWS_PROFILE AWS_REGION AWS_PAGER MEMBER_ACCOUNT_ID SCP_ID
unset TRAIL_NAME TRAIL_HOME_REGION ARCHIVE_BUCKET AGGREGATOR_NAME
unset PROBE_INSTANCE_ID ENCODED_MESSAGE TEST_OBJECT_KEY TEST_OBJECT_VERSION
rm -rf .work
test ! -e .work && printf '%s\n' 'PASS local cleanup'
```

If credential variable names were printed, do not publish the output values and follow the credential issuer's revocation procedure. The commands never need static access keys.

## What to keep

Keep the initial prediction, exact approved identities and scope, redacted evidence index, hashes, decoded SCP decision, active compliance-retention record, failed local hypothesis, correction, denied-event correlation, limits, and cleanup attestation. Explain without notes why an SCP is a maximum-permissions guardrail rather than a grant, why dry-run plus decoded authorization supports SCP attribution, why the archive test needs an otherwise allowed delete, and why centralized logs are only as strong as their delivery, retention, access, and break-glass controls.

Completing only the local path provides guided reasoning evidence for DOP-C02 **6.1** and **6.3**. It leaves the live parts of **2.2**, **4.2**, **6.1**, and **6.3** open. Only the rows marked `Organization required`, reproduced in an authorized organization sandbox, can support organization-scale operation claims.

## Sources

- [AWS Organizations terminology and concepts](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started_concepts.html)
- [AWS Organizations service control policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)
- [AWS Organizations SCP effects on permissions](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html#scp-effects-on-permissions)
- [AWS Organizations delegated administrator](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_delegate_policies.html)
- [AWS CloudTrail organization trails](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html)
- [AWS CloudTrail log file integrity validation](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html)
- [AWS CloudTrail security best practices](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/best-practices-security.html)
- [Amazon S3 Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)
- [Amazon S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)
- [AWS Config multi-account multi-Region aggregation](https://docs.aws.amazon.com/config/latest/developerguide/aggregate-data.html)
- [AWS IAM policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
- [Amazon EC2 API common parameters, including DryRun](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/Common-Parameters.html)
- [AWS STS DecodeAuthorizationMessage](https://docs.aws.amazon.com/STS/latest/APIReference/API_DecodeAuthorizationMessage.html)
