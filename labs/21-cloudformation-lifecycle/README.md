# Lab: Operate a CloudFormation Resource Lifecycle

Use AWS CloudFormation to create a small stack, review change sets for
replacement, observe failed-update rollback, detect deliberate drift, and
reconcile the resource through the stack. A separate fixture bounds a StackSets
review to one Region and, only in an organization sandbox, one target account.

This lab addresses the CloudFormation lifecycle portion of GAP-2 in the
[DOP-C02 overlay](../../certs/aws-dop-c02.md#aws-specific-gap-register).
Terraform experience is useful, but Terraform state and plans are not evidence
that CloudFormation lifecycle behavior has been operated. It does not close
the separate account-onboarding evidence gap.

## Goal and DOP-C02 tasks

Produce evidence that distinguishes template intent, a reviewed change set,
physical-resource replacement, update rollback, out-of-band drift, and
reconciliation. Explain where CloudFormation's control ends and why StackSets
requires a separate organization authority boundary.

This lab supplies direct guided evidence for these exact DOP-C02 task IDs:

- **2.1 Define cloud infrastructure and reusable components to provision and manage systems throughout their lifecycle**
- **2.3 Design and build automated solutions for complex tasks and large-scale environments**

The drift, event-timeline, and rollback work provides supporting practice for
tasks **4.2**, **5.2**, and **5.3**, but does not directly satisfy their broader
monitoring and response requirements.

The StackSets fixture provides design and review support for task **2.2 Deploy
automation to create, onboard, and secure AWS accounts in a multi-account or
multi-Region environment**. Even when the optional organization-sandbox
operation runs, this lab distributes one marker to an existing account; it
does not create, onboard, baseline, or secure an account. Direct task 2.2
evidence still requires authorized organization-level account onboarding,
governance, identity, security controls, failure handling, and teardown proof.

## Safety, identity, cost, and stop conditions

**Run cloud mutations only in an authorized disposable sandbox account. Do not
use production, a shared development account, an AWS Organizations management
account used for real workloads, or any account containing customer data.**

For the single-account lifecycle, use a short-lived federated role that can
validate templates and create, inspect, update, detect drift on, and delete the
one named CloudFormation stack. It also needs bounded SQS and Systems Manager
Parameter Store permissions for resources with the lab prefix. The role must
not rely on an IAM user access key.

The optional StackSets exercise has a different identity assumption: use the
management account or a registered delegated administrator in a disposable
organization, with CloudFormation StackSets trusted access already approved.
The target must be one non-management sandbox account in one approved
organizational unit (OU). Do not enable trusted access, register a delegated
administrator, create an organization, or move an account as part of this lab.
Those are governance changes outside the fixture.

Expected working time is 60 to 90 minutes for the single-account lifecycle and
up to 30 additional minutes for an already-approved StackSets sandbox. Bound
the single-account work to one stack, one SQS standard queue, one SSM parameter,
six change sets, ten drift detections, 100 SQS requests, one Region, and two
hours. Bound the optional StackSet to one stack set, one OU intersected with
one explicit account, one Region, one stack instance, failure tolerance zero,
and maximum concurrency one.

Set a USD 1 ceiling for the single-account work and a USD 2 total ceiling if
the StackSet instance is run. Billing dimensions can include SQS requests,
Parameter Store advanced parameters if selected accidentally, CloudTrail or
AWS Config features already enabled by the account, and network use.
CloudFormation and standard parameters have no additional service charge, but
the resources they manage can. This lab uses only a standard parameter.

Stop immediately if:

- the caller identity, account, Region, OU, or target account is not the
  pre-approved sandbox value;
- the target is an Organizations management account;
- a stack, stack set, change set, queue, or parameter lacks the recorded lab
  prefix;
- a change set contains IAM, networking, encryption-key, organization, account,
  or resource types not declared in this lab;
- replacement is shown for anything except the disposable SQS queue;
- a stack operation remains in progress for 15 minutes, a StackSets operation
  remains in progress for 20 minutes, or an operation would be retried more
  than once;
- estimated spend reaches its ceiling, more than one stack instance is
  targeted, failure tolerance is nonzero, or maximum concurrency exceeds one;
- authorization changes, sensitive output appears, rollback stops in
  `UPDATE_ROLLBACK_FAILED`, or cleanup cannot be proved.

If rollback reaches `UPDATE_ROLLBACK_FAILED`, do not repeatedly call continue
or skip resources. Preserve events, stop mutations, and involve the sandbox
owner. Skipping a resource can leave stack state inconsistent with reality.

## Prerequisites

- AWS CLI v2, Bash, `jq`, and `sha256sum`
- an approved sandbox account and Region with CloudFormation, SQS, and
  Systems Manager Parameter Store
- familiarity with
  [Terraform plan and state safety](../08-terraform-safety/README.md) so that
  similarities are compared without treating the products as equivalent
- account-owner approval for identity, bounds, rollback, and cleanup
- for optional real StackSets work only: a disposable organization, trusted
  access already configured, one approved OU, and one explicit non-management
  target account

Record the CLI version and date. These commands use current AWS CLI v2 service
models and CloudFormation resource specifications.

## Establish identity and local scope

```bash
export AWS_PROFILE=approved-sandbox
export AWS_REGION=us-east-1
export AWS_PAGER=
export LAB_ID="dop-cfn-$(openssl rand -hex 4)"
export STACK_NAME="$LAB_ID"
export QUEUE_NAME="$LAB_ID-queue"
export PARAMETER_NAME="/$LAB_ID/owner"
export WORK_DIR="/tmp/$LAB_ID"
mkdir -p "$WORK_DIR"
chmod 700 "$WORK_DIR"

aws sts get-caller-identity >"$WORK_DIR/identity.json"
aws configure get region
aws --version
jq '{Account,Arn}' "$WORK_DIR/identity.json"
```

Have the account owner confirm the account, role, Region, prefix, spend ceiling,
and resource inventory. Predict these outcomes before continuing:

1. the baseline creates one queue and one standard parameter;
2. changing `QueueName` appears as a replacement in a change set;
3. an invalid new parameter causes the update to roll back;
4. changing queue visibility outside CloudFormation appears as drift;
5. a later stack update reconciles the explicit property.

## Write and validate the baseline template

The queue is a disposable resource with no messages. Its explicit
`VisibilityTimeout` gives drift detection a property to compare. The parameter
provides a second resource whose value is synthetic.

```bash
cat >"$WORK_DIR/baseline.yaml" <<'YAML'
AWSTemplateFormatVersion: '2010-09-09'
Description: Bounded CloudFormation lifecycle lab
Parameters:
  QueueName:
    Type: String
    AllowedPattern: '[a-z0-9-]+'
  OwnerParameterName:
    Type: String
    AllowedPattern: '/[a-z0-9/-]+'
Resources:
  LabQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: !Ref QueueName
      VisibilityTimeout: 30
      MessageRetentionPeriod: 300
      SqsManagedSseEnabled: true
      Tags:
        - Key: purpose
          Value: dop-c02-lifecycle-lab
  OwnerParameter:
    Type: AWS::SSM::Parameter
    Properties:
      Name: !Ref OwnerParameterName
      Type: String
      Tier: Standard
      Value: synthetic-lab-owner
      Description: Synthetic value for the CloudFormation lifecycle lab
Outputs:
  QueueUrl:
    Value: !Ref LabQueue
  QueueArn:
    Value: !GetAtt LabQueue.Arn
  OwnerParameterName:
    Value: !Ref OwnerParameter
YAML

sha256sum "$WORK_DIR/baseline.yaml" | tee "$WORK_DIR/template-hashes.txt"
aws cloudformation validate-template \
  --template-body "file://$WORK_DIR/baseline.yaml" \
  >"$WORK_DIR/validate-baseline.json"
```

`validate-template` checks template syntax and some schema constraints. It does
not prove permissions, resource availability, successful creation, safe
replacement, or application correctness.

## Create and review the baseline change set

Create a change set rather than deploying directly. Do not execute it until the
resource types and action counts match the prediction.

```bash
export BASELINE_CHANGE_SET="$LAB_ID-baseline"
aws cloudformation create-change-set \
  --stack-name "$STACK_NAME" \
  --change-set-name "$BASELINE_CHANGE_SET" \
  --change-set-type CREATE \
  --template-body "file://$WORK_DIR/baseline.yaml" \
  --parameters \
    ParameterKey=QueueName,ParameterValue="$QUEUE_NAME" \
    ParameterKey=OwnerParameterName,ParameterValue="$PARAMETER_NAME" \
  --description "Create bounded lifecycle baseline" >/dev/null
aws cloudformation wait change-set-create-complete \
  --stack-name "$STACK_NAME" \
  --change-set-name "$BASELINE_CHANGE_SET"
aws cloudformation describe-change-set \
  --stack-name "$STACK_NAME" \
  --change-set-name "$BASELINE_CHANGE_SET" \
  >"$WORK_DIR/baseline-change-set.json"
jq -r '.Changes[].ResourceChange |
  [.Action,.LogicalResourceId,.ResourceType,.Replacement] | @tsv' \
  "$WORK_DIR/baseline-change-set.json"
```

Require exactly two `Add` actions, for `AWS::SQS::Queue` and
`AWS::SSM::Parameter`. Stop if any other type appears.

```bash
test "$(jq '[.Changes[].ResourceChange] | length' \
  "$WORK_DIR/baseline-change-set.json")" -eq 2
test "$(jq -r '[.Changes[].ResourceChange.ResourceType] | sort | join(",")' \
  "$WORK_DIR/baseline-change-set.json")" = \
  "AWS::SQS::Queue,AWS::SSM::Parameter"

aws cloudformation execute-change-set \
  --stack-name "$STACK_NAME" \
  --change-set-name "$BASELINE_CHANGE_SET"
aws cloudformation wait stack-create-complete --stack-name "$STACK_NAME"
```

## Establish a healthy baseline

Capture stack state, physical identities, queue attributes, and the parameter
value. Do not put account identifiers or URLs into public evidence.

```bash
aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
  >"$WORK_DIR/baseline-stack.json"
aws cloudformation describe-stack-resources --stack-name "$STACK_NAME" \
  >"$WORK_DIR/baseline-resources.json"
export QUEUE_URL="$(jq -r '.Stacks[0].Outputs[] |
  select(.OutputKey=="QueueUrl") | .OutputValue' \
  "$WORK_DIR/baseline-stack.json")"
export BASELINE_QUEUE_ID="$(jq -r '.StackResources[] |
  select(.LogicalResourceId=="LabQueue") | .PhysicalResourceId' \
  "$WORK_DIR/baseline-resources.json")"

aws sqs get-queue-attributes --queue-url "$QUEUE_URL" \
  --attribute-names VisibilityTimeout MessageRetentionPeriod \
  >"$WORK_DIR/baseline-queue.json"
aws ssm get-parameter --name "$PARAMETER_NAME" \
  --query 'Parameter.{Name:Name,Type:Type,Value:Value}' \
  >"$WORK_DIR/baseline-parameter.json"
jq -e '.Attributes.VisibilityTimeout == "30" and
  .Attributes.MessageRetentionPeriod == "300"' \
  "$WORK_DIR/baseline-queue.json"
test "$(jq -r .Value "$WORK_DIR/baseline-parameter.json")" = \
  "synthetic-lab-owner"
```

The physical ID and attributes prove the bounded starting state at one point in
time. They do not establish that no other principal can mutate the resources.

## Review a replacement without executing it

Changing a named SQS queue's `QueueName` requires replacement. Keep the
template unchanged, change only the parameter that supplies that effective
property, and inspect the generated change set.

```bash
cp "$WORK_DIR/baseline.yaml" "$WORK_DIR/replacement.yaml"
export REPLACEMENT_QUEUE_NAME="$LAB_ID-replacement"
export REPLACEMENT_CHANGE_SET="$LAB_ID-replacement-review"

aws cloudformation create-change-set \
  --stack-name "$STACK_NAME" \
  --change-set-name "$REPLACEMENT_CHANGE_SET" \
  --change-set-type UPDATE \
  --template-body "file://$WORK_DIR/replacement.yaml" \
  --parameters \
    ParameterKey=QueueName,ParameterValue="$REPLACEMENT_QUEUE_NAME" \
    ParameterKey=OwnerParameterName,UsePreviousValue=true \
  --description "Review queue replacement; do not execute" >/dev/null
aws cloudformation wait change-set-create-complete \
  --stack-name "$STACK_NAME" \
  --change-set-name "$REPLACEMENT_CHANGE_SET"
aws cloudformation describe-change-set \
  --stack-name "$STACK_NAME" \
  --change-set-name "$REPLACEMENT_CHANGE_SET" \
  --include-property-values \
  >"$WORK_DIR/replacement-change-set.json"
jq -r '.Changes[].ResourceChange |
  [.Action,.LogicalResourceId,.ResourceType,.Replacement,
   ([.Details[]?.Target.Name] | unique | join(","))] | @tsv' \
  "$WORK_DIR/replacement-change-set.json"
```

Require `LabQueue` to show `Modify` and `Replacement` of `True` or
`Conditional`, with `QueueName` in the details. Do not execute the change set.
Deleting an unexecuted change set leaves the running stack unchanged.

```bash
test "$(jq -r '.Changes[] |
  select(.ResourceChange.LogicalResourceId=="LabQueue") |
  .ResourceChange.Action' "$WORK_DIR/replacement-change-set.json")" = "Modify"
REPLACEMENT_MODE="$(jq -r '.Changes[] |
  select(.ResourceChange.LogicalResourceId=="LabQueue") |
  .ResourceChange.Replacement' "$WORK_DIR/replacement-change-set.json")"
case "$REPLACEMENT_MODE" in
  True|Conditional) ;;
  *) printf 'Expected queue replacement, observed %s\n' \
       "$REPLACEMENT_MODE" >&2; exit 1 ;;
esac
aws cloudformation delete-change-set \
  --stack-name "$STACK_NAME" \
  --change-set-name "$REPLACEMENT_CHANGE_SET"
test "$(aws cloudformation describe-stack-resources \
  --stack-name "$STACK_NAME" --query \
  'StackResources[?LogicalResourceId==`LabQueue`].PhysicalResourceId | [0]' \
  --output text)" = "$BASELINE_QUEUE_ID"
```

Replacement analysis must consider data and references, not only a
CloudFormation flag. This queue is empty and disposable. Replacing a stateful
production resource could lose data, change endpoints, or exceed a recovery
objective.

## Execute a no-replacement update

Change the explicit visibility timeout from 30 to 31 seconds. Review and
execute the change set, then prove the physical queue identity is unchanged.

```bash
sed 's/VisibilityTimeout: 30/VisibilityTimeout: 31/' \
  "$WORK_DIR/baseline.yaml" >"$WORK_DIR/visibility-31.yaml"
export SAFE_CHANGE_SET="$LAB_ID-visibility-31"
aws cloudformation create-change-set \
  --stack-name "$STACK_NAME" \
  --change-set-name "$SAFE_CHANGE_SET" \
  --change-set-type UPDATE \
  --template-body "file://$WORK_DIR/visibility-31.yaml" \
  --parameters \
    ParameterKey=QueueName,UsePreviousValue=true \
    ParameterKey=OwnerParameterName,UsePreviousValue=true >/dev/null
aws cloudformation wait change-set-create-complete \
  --stack-name "$STACK_NAME" --change-set-name "$SAFE_CHANGE_SET"
aws cloudformation describe-change-set \
  --stack-name "$STACK_NAME" --change-set-name "$SAFE_CHANGE_SET" \
  >"$WORK_DIR/safe-change-set.json"
jq -r '.Changes[].ResourceChange |
  [.Action,.LogicalResourceId,.Replacement] | @tsv' \
  "$WORK_DIR/safe-change-set.json"
test "$(jq -r '.Changes[] |
  select(.ResourceChange.LogicalResourceId=="LabQueue") |
  .ResourceChange.Replacement' "$WORK_DIR/safe-change-set.json")" = "False"

aws cloudformation execute-change-set \
  --stack-name "$STACK_NAME" --change-set-name "$SAFE_CHANGE_SET"
aws cloudformation wait stack-update-complete --stack-name "$STACK_NAME"
test "$(aws cloudformation describe-stack-resources \
  --stack-name "$STACK_NAME" --query \
  'StackResources[?LogicalResourceId==`LabQueue`].PhysicalResourceId | [0]' \
  --output text)" = "$BASELINE_QUEUE_ID"
test "$(aws sqs get-queue-attributes --queue-url "$QUEUE_URL" \
  --attribute-names VisibilityTimeout \
  --query 'Attributes.VisibilityTimeout' --output text)" = "31"
```

## Failure injection: observe failed-update rollback

Introduce one fault: a new standard SSM parameter whose name begins with the
reserved `/aws/` hierarchy. The same template requests a queue visibility
change to 32 seconds. CloudFormation may schedule independent resources in
either order, so do not assume the queue update completes before the parameter
fails.

```bash
sed 's/VisibilityTimeout: 30/VisibilityTimeout: 32/' \
  "$WORK_DIR/baseline.yaml" |
  sed '/^Outputs:/i\
  RejectedParameter:\
    Type: AWS::SSM::Parameter\
    Properties:\
      Name: /aws/dop-c02-reserved-name\
      Type: String\
      Tier: Standard\
      Value: synthetic-invalid-update' \
  >"$WORK_DIR/failing-update.yaml"
aws cloudformation validate-template \
  --template-body "file://$WORK_DIR/failing-update.yaml" >/dev/null

set +e
aws cloudformation update-stack \
  --stack-name "$STACK_NAME" \
  --template-body "file://$WORK_DIR/failing-update.yaml" \
  --parameters \
    ParameterKey=QueueName,UsePreviousValue=true \
    ParameterKey=OwnerParameterName,UsePreviousValue=true \
  >"$WORK_DIR/failing-update-request.json" \
  2>"$WORK_DIR/failing-update-request.err"
REQUEST_STATUS=$?
set -e
test "$REQUEST_STATUS" -eq 0

set +e
aws cloudformation wait stack-update-complete --stack-name "$STACK_NAME"
WAIT_STATUS=$?
set -e
test "$WAIT_STATUS" -ne 0
aws cloudformation wait stack-update-rollback-complete \
  --stack-name "$STACK_NAME"
```

If the update request itself is rejected before stack execution, preserve that
evidence, verify the template transformation, and stop this fault rather than
substituting an unbounded failure. The intended observation is a stack update
that enters rollback and reaches `UPDATE_ROLLBACK_COMPLETE`.

### Diagnose the rollback

Start from stack status, then inspect events in chronological context. The
first resource-level failure separates the trigger from later rollback events.

```bash
aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
  >"$WORK_DIR/rollback-stack.json"
aws cloudformation describe-stack-events --stack-name "$STACK_NAME" \
  >"$WORK_DIR/rollback-events.json"
jq -r '.Stacks[0] |
  [.StackStatus,.StackStatusReason] | @tsv' \
  "$WORK_DIR/rollback-stack.json"
jq -r '.StackEvents[] |
  [.Timestamp,.LogicalResourceId,.ResourceStatus,
   (.ResourceStatusReason // "")] | @tsv' \
  "$WORK_DIR/rollback-events.json" \
  >"$WORK_DIR/rollback-timeline.tsv"
```

Rank at least these hypotheses before reading the failure reason: template
validation, caller authorization, reserved parameter name, queue update
constraint, and timeout. The `RejectedParameter` failure with an SSM validation
reason discriminates the injected cause. Later `UPDATE_ROLLBACK_*` entries are
effects of recovery, not additional root causes.

Prove recovery at stack and resource boundaries:

```bash
test "$(jq -r '.Stacks[0].StackStatus' \
  "$WORK_DIR/rollback-stack.json")" = "UPDATE_ROLLBACK_COMPLETE"
test "$(aws cloudformation describe-stack-resources \
  --stack-name "$STACK_NAME" --query \
  'StackResources[?LogicalResourceId==`LabQueue`].PhysicalResourceId | [0]' \
  --output text)" = "$BASELINE_QUEUE_ID"
test "$(aws sqs get-queue-attributes --queue-url "$QUEUE_URL" \
  --attribute-names VisibilityTimeout \
  --query 'Attributes.VisibilityTimeout' --output text)" = "31"
test "$(aws ssm get-parameter --name /aws/dop-c02-reserved-name \
  >/dev/null 2>&1; printf '%s' "$?")" != "0"
```

This proves the bounded stack returned to the prior declared value. It does not
prove rollback is possible for every resource; some operations and external
side effects are not reversible.

## Failure injection: detect and reconcile drift

The previous fault is recovered. Now introduce one separate, reversible
out-of-band change to the queue:

```bash
aws sqs set-queue-attributes \
  --queue-url "$QUEUE_URL" \
  --attributes VisibilityTimeout=45
test "$(aws sqs get-queue-attributes --queue-url "$QUEUE_URL" \
  --attribute-names VisibilityTimeout \
  --query 'Attributes.VisibilityTimeout' --output text)" = "45"

export DRIFT_ID="$(aws cloudformation detect-stack-drift \
  --stack-name "$STACK_NAME" \
  --query StackDriftDetectionId --output text)"
for attempt in $(seq 1 30); do
  DRIFT_STATUS="$(aws cloudformation describe-stack-drift-detection-status \
    --stack-drift-detection-id "$DRIFT_ID" \
    --query DetectionStatus --output text)"
  case "$DRIFT_STATUS" in
    DETECTION_COMPLETE) break ;;
    DETECTION_FAILED) exit 1 ;;
  esac
  sleep 10
done
test "$DRIFT_STATUS" = "DETECTION_COMPLETE"
aws cloudformation describe-stack-resource-drifts \
  --stack-name "$STACK_NAME" \
  --stack-resource-drift-status-filters MODIFIED \
  >"$WORK_DIR/drift.json"
jq -r '.StackResourceDrifts[] |
  [.LogicalResourceId,.StackResourceDriftStatus,
   (.PropertyDifferences[]? |
    [.PropertyPath,.ExpectedValue,.ActualValue,.DifferenceType] |
    join(":"))] | @tsv' "$WORK_DIR/drift.json"
```

The expected difference is `LabQueue` visibility, with declared `31` and actual
`45`. Drift detection compares supported, explicitly set properties. `IN_SYNC`
does not prove that every runtime setting, external dependency, or unsupported
resource is unchanged.

Reconcile through CloudFormation by making a reviewed desired-state change to
33 seconds. This forces an update instead of assuming that re-submitting an
unchanged value repairs drift.

```bash
sed 's/VisibilityTimeout: 30/VisibilityTimeout: 33/' \
  "$WORK_DIR/baseline.yaml" >"$WORK_DIR/reconcile.yaml"
export RECONCILE_CHANGE_SET="$LAB_ID-reconcile"
aws cloudformation create-change-set \
  --stack-name "$STACK_NAME" \
  --change-set-name "$RECONCILE_CHANGE_SET" \
  --change-set-type UPDATE \
  --template-body "file://$WORK_DIR/reconcile.yaml" \
  --parameters \
    ParameterKey=QueueName,UsePreviousValue=true \
    ParameterKey=OwnerParameterName,UsePreviousValue=true >/dev/null
aws cloudformation wait change-set-create-complete \
  --stack-name "$STACK_NAME" --change-set-name "$RECONCILE_CHANGE_SET"
aws cloudformation describe-change-set \
  --stack-name "$STACK_NAME" --change-set-name "$RECONCILE_CHANGE_SET" \
  >"$WORK_DIR/reconcile-change-set.json"
jq -r '.Changes[].ResourceChange |
  [.Action,.LogicalResourceId,.Replacement] | @tsv' \
  "$WORK_DIR/reconcile-change-set.json"
test "$(jq -r '.Changes[] |
  select(.ResourceChange.LogicalResourceId=="LabQueue") |
  .ResourceChange.Replacement' "$WORK_DIR/reconcile-change-set.json")" = "False"
aws cloudformation execute-change-set \
  --stack-name "$STACK_NAME" --change-set-name "$RECONCILE_CHANGE_SET"
aws cloudformation wait stack-update-complete --stack-name "$STACK_NAME"
test "$(aws sqs get-queue-attributes --queue-url "$QUEUE_URL" \
  --attribute-names VisibilityTimeout \
  --query 'Attributes.VisibilityTimeout' --output text)" = "33"
```

Run drift detection once more and require `StackDriftStatus` to be `IN_SYNC`.
Retain both detection IDs and timestamps.

```bash
export RECOVERY_DRIFT_ID="$(aws cloudformation detect-stack-drift \
  --stack-name "$STACK_NAME" \
  --query StackDriftDetectionId --output text)"
for attempt in $(seq 1 30); do
  RECOVERY_DRIFT_STATUS="$(aws cloudformation \
    describe-stack-drift-detection-status \
    --stack-drift-detection-id "$RECOVERY_DRIFT_ID" \
    --query DetectionStatus --output text)"
  case "$RECOVERY_DRIFT_STATUS" in
    DETECTION_COMPLETE) break ;;
    DETECTION_FAILED) exit 1 ;;
  esac
  sleep 10
done
test "$RECOVERY_DRIFT_STATUS" = "DETECTION_COMPLETE"
test "$(aws cloudformation describe-stack-drift-detection-status \
  --stack-drift-detection-id "$RECOVERY_DRIFT_ID" \
  --query StackDriftStatus --output text)" = "IN_SYNC"
```

## Bounded StackSets review fixture

This fixture is useful locally and in a normal sandbox account without creating
a stack set. It makes the intended target and concurrency contract
inspectable:

```bash
cat >"$WORK_DIR/stackset-template.yaml" <<'YAML'
AWSTemplateFormatVersion: '2010-09-09'
Description: One-account StackSets review marker
Parameters:
  LabPrefix:
    Type: String
    AllowedPattern: '[a-z0-9-]+'
Resources:
  ReviewMarker:
    Type: AWS::SSM::Parameter
    Properties:
      Name: !Sub /${LabPrefix}/stackset-review
      Type: String
      Tier: Standard
      Value: synthetic-stackset-review
      Description: Synthetic marker for bounded StackSets review
YAML

cat >"$WORK_DIR/stackset-review.json" <<JSON
{
  "permissionModel": "SERVICE_MANAGED",
  "regions": ["$AWS_REGION"],
  "targetMode": "one approved OU intersected with one explicit account",
  "failureToleranceCount": 0,
  "maxConcurrentCount": 1,
  "regionConcurrencyType": "SEQUENTIAL",
  "autoDeployment": false,
  "resourceTypes": ["AWS::SSM::Parameter"],
  "maximumStackInstances": 1
}
JSON
jq -e '
  (.regions | length) == 1 and
  .failureToleranceCount == 0 and
  .maxConcurrentCount == 1 and
  .maximumStackInstances == 1 and
  .autoDeployment == false and
  .resourceTypes == ["AWS::SSM::Parameter"]
' "$WORK_DIR/stackset-review.json"
aws cloudformation validate-template \
  --template-body "file://$WORK_DIR/stackset-template.yaml" >/dev/null
```

Template validation is a real AWS read-only API call. The review JSON is a local
fixture, not a StackSets API result. Together they test configuration review;
they do not prove Organizations trust, target resolution, execution, failure
handling, or cleanup.

### Optional real organization-sandbox operation

Skip this section unless the organization owner has approved the exact OU and
target account and trusted access already exists. An OU can contain many
accounts; the `INTERSECTION` filter below is essential because it restricts the
operation to the one explicit account.

```bash
: "${LAB_OU_ID:?set the approved sandbox OU ID}"
: "${LAB_TARGET_ACCOUNT_ID:?set the approved non-management sandbox account ID}"
export MANAGEMENT_ACCOUNT_ID="$(aws organizations describe-organization \
  --query 'Organization.ManagementAccountId' --output text)"
test "$LAB_TARGET_ACCOUNT_ID" != "$MANAGEMENT_ACCOUNT_ID"
export STACKSET_CALL_AS=SELF
# Use DELEGATED_ADMIN only when the current account is the approved registered
# delegated administrator.
export STACK_SET_NAME="$LAB_ID-review"

aws cloudformation create-stack-set \
  --stack-set-name "$STACK_SET_NAME" \
  --description "Bounded DOP-C02 StackSets review" \
  --template-body "file://$WORK_DIR/stackset-template.yaml" \
  --permission-model SERVICE_MANAGED \
  --auto-deployment Enabled=false,RetainStacksOnAccountRemoval=false \
  --call-as "$STACKSET_CALL_AS" >/dev/null

export STACKSET_OPERATION_ID="$(aws cloudformation create-stack-instances \
  --stack-set-name "$STACK_SET_NAME" \
  --deployment-targets \
    "OrganizationalUnitIds=$LAB_OU_ID,Accounts=$LAB_TARGET_ACCOUNT_ID,AccountFilterType=INTERSECTION" \
  --regions "$AWS_REGION" \
  --parameter-overrides ParameterKey=LabPrefix,ParameterValue="$LAB_ID" \
  --operation-preferences \
    FailureToleranceCount=0,MaxConcurrentCount=1,RegionConcurrencyType=SEQUENTIAL \
  --call-as "$STACKSET_CALL_AS" \
  --query OperationId --output text)"
```

Inspect status no more than once every 15 seconds and stop after 20 minutes:

```bash
for attempt in $(seq 1 80); do
  OPERATION_STATUS="$(aws cloudformation describe-stack-set-operation \
    --stack-set-name "$STACK_SET_NAME" \
    --operation-id "$STACKSET_OPERATION_ID" \
    --call-as "$STACKSET_CALL_AS" \
    --query 'StackSetOperation.Status' --output text)"
  printf '%s %s\n' "$(date -u +%FT%TZ)" "$OPERATION_STATUS"
  case "$OPERATION_STATUS" in
    SUCCEEDED) break ;;
    FAILED|STOPPED) exit 1 ;;
  esac
  sleep 15
done
test "$OPERATION_STATUS" = "SUCCEEDED"
aws cloudformation list-stack-instances \
  --stack-set-name "$STACK_SET_NAME" \
  --call-as "$STACKSET_CALL_AS" \
  >"$WORK_DIR/stack-instances.json"
test "$(jq --arg account "$LAB_TARGET_ACCOUNT_ID" \
  --arg region "$AWS_REGION" '[.Summaries[] |
  select(.Account==$account and .Region==$region)] | length' \
  "$WORK_DIR/stack-instances.json")" -eq 1
test "$(jq '.Summaries | length' \
  "$WORK_DIR/stack-instances.json")" -eq 1
```

A successful stack instance proves the bounded target accepted this template.
It does not prove safe organization-wide rollout, delegated-administrator
design, heterogeneous-account compatibility, Region scaling, or recovery from
partial fleet failure.

## Evidence record

Complete the table with observations rather than expected output. Redact
account IDs, ARNs, queue URLs, OU IDs, and request IDs before public use.

| Claim | Observation to record | Limits of the observation |
|---|---|---|
| Identity and bounds were approved | timestamp, role type, Region, prefix, resource-count contract | does not prove all effective permissions are least privilege |
| Baseline matched intent | template hash, two `Add` actions, stack status, resource types and selected attributes | one read does not prove continued conformance |
| Queue name change requires replacement | unexecuted change-set action, replacement value, changed property | does not quantify data loss or downstream impact |
| Safe property update preserved identity | `Replacement=False`, same physical queue ID, visibility 31 | does not prove all updates are non-disruptive |
| Invalid update rolled back | first failed resource event, rollback timeline, final stack status, visibility 31 | this reversible fixture does not represent every resource |
| Out-of-band change caused drift | direct mutation timestamp and property difference showing 31 versus 45 | drift covers supported explicit properties, not all reality |
| Reconciliation restored declared control | reviewed update, visibility 33, later `IN_SYNC` detection | `IN_SYNC` is not an application health check |
| StackSets scope was bounded | fixture or API result showing one existing account, one Region, concurrency one, tolerance zero | fixture-only review is not operational evidence; one marker instance neither proves fleet operation nor closes task 2.2 account onboarding |

Also preserve predictions, ranked hypotheses, event ordering, correction,
template hashes, CLI version, cleanup proof, and the distinction between
trigger, rollback activity, and final recovery.

## Cleanup

If the optional StackSet was created, delete its one instance before deleting
the stack set. Never retain the instance during this lab.

```bash
if test -n "${STACK_SET_NAME:-}"; then
  export STACKSET_DELETE_OPERATION_ID="$(aws cloudformation delete-stack-instances \
    --stack-set-name "$STACK_SET_NAME" \
    --deployment-targets \
      "OrganizationalUnitIds=$LAB_OU_ID,Accounts=$LAB_TARGET_ACCOUNT_ID,AccountFilterType=INTERSECTION" \
    --regions "$AWS_REGION" \
    --no-retain-stacks \
    --operation-preferences \
      FailureToleranceCount=0,MaxConcurrentCount=1,RegionConcurrencyType=SEQUENTIAL \
    --call-as "$STACKSET_CALL_AS" \
    --query OperationId --output text)"
  for attempt in $(seq 1 80); do
    DELETE_STATUS="$(aws cloudformation describe-stack-set-operation \
      --stack-set-name "$STACK_SET_NAME" \
      --operation-id "$STACKSET_DELETE_OPERATION_ID" \
      --call-as "$STACKSET_CALL_AS" \
      --query 'StackSetOperation.Status' --output text)"
    case "$DELETE_STATUS" in
      SUCCEEDED) break ;;
      FAILED|STOPPED) exit 1 ;;
    esac
    sleep 15
  done
  test "$DELETE_STATUS" = "SUCCEEDED"
  test "$(aws cloudformation list-stack-instances \
    --stack-set-name "$STACK_SET_NAME" \
    --call-as "$STACKSET_CALL_AS" \
    --query 'length(Summaries)' --output text)" = "0"
  aws cloudformation delete-stack-set \
    --stack-set-name "$STACK_SET_NAME" \
    --call-as "$STACKSET_CALL_AS"
fi
```

Delete the single-account stack and wait for completion:

```bash
aws cloudformation delete-stack --stack-name "$STACK_NAME"
aws cloudformation wait stack-delete-complete --stack-name "$STACK_NAME"
```

Cleanup proof must show absence at the stack, queue, and parameter boundaries:

```bash
test "$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
  >/dev/null 2>&1; printf '%s' "$?")" != "0"
test "$(aws sqs get-queue-url --queue-name "$QUEUE_NAME" \
  >/dev/null 2>&1; printf '%s' "$?")" != "0"
test "$(aws sqs get-queue-url --queue-name "$REPLACEMENT_QUEUE_NAME" \
  >/dev/null 2>&1; printf '%s' "$?")" != "0"
test "$(aws ssm get-parameter --name "$PARAMETER_NAME" \
  >/dev/null 2>&1; printf '%s' "$?")" != "0"

rm -rf "$WORK_DIR"
unset AWS_PROFILE AWS_REGION AWS_PAGER LAB_ID STACK_NAME QUEUE_NAME \
  PARAMETER_NAME WORK_DIR BASELINE_CHANGE_SET QUEUE_URL BASELINE_QUEUE_ID \
  REPLACEMENT_QUEUE_NAME REPLACEMENT_CHANGE_SET REPLACEMENT_MODE \
  SAFE_CHANGE_SET DRIFT_ID \
  DRIFT_STATUS RECONCILE_CHANGE_SET RECOVERY_DRIFT_ID \
  RECOVERY_DRIFT_STATUS LAB_OU_ID LAB_TARGET_ACCOUNT_ID \
  MANAGEMENT_ACCOUNT_ID STACKSET_CALL_AS STACK_SET_NAME \
  STACKSET_OPERATION_ID STACKSET_DELETE_OPERATION_ID
```

Check the CloudFormation, SQS, Systems Manager, and billing/resource inventory
views for the prefix. A failed deletion is unresolved cloud state: retain the
failure evidence, notify the sandbox owner, and finish teardown before the
spend ceiling.

## Completion conditions

The lab is complete only when a reviewer can inspect the baseline, rejected
replacement, no-replacement update, first rollback failure, restored resource
state, drift difference, controlled reconciliation, and cleanup proof. The
StackSets portion must be labeled either local/static review or real
organization-sandbox execution. Never present the former as account-operation
evidence, and never present either path as account creation, onboarding, or
security-baseline evidence.

## Sources

Checked against official AWS documentation on 2026-08-23:

- [CloudFormation stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html)
- [Creating CloudFormation change sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets-create.html)
- [Viewing CloudFormation change sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets-view.html)
- [CloudFormation update behaviors](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html)
- [Continue update rollback](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html)
- [Detect unmanaged configuration changes with drift detection](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html)
- [CloudFormation drift-status codes](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift-status-codes.html)
- [AWS::SQS::Queue resource reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-sqs-queue.html)
- [AWS::SSM::Parameter resource reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ssm-parameter.html)
- [Systems Manager parameter naming constraints](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-su-create.html)
- [CloudFormation StackSets concepts](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html)
- [Service-managed StackSets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-enable-trusted-access.html)
- [StackSets deployment targets and account filters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-deployment-targets.html)
- [StackSets operation options](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-concepts.html#stacksets-concepts-ops)
- [Deleting CloudFormation stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-delete-stack.html)
