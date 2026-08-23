# Lab: Operate a Small AWS Fleet and Bounded Event Remediation

This lab makes fleet state, configuration drift, event delivery, idempotency, partial failure, and rollback visible. The fully runnable local path uses a static one-instance fixture. The optional cloud path creates one disposable EC2 instance managed by AWS Systems Manager, records inventory with State Manager, evaluates tag drift with AWS Config, and sends noncompliance events through EventBridge and SQS to a narrowly scoped Lambda remediation.

The one-node fixture provides guided mechanism evidence mapped to DOP-C02 task statements **2.1** (infrastructure lifecycle), **2.3** (operational automation), **4.3** (monitoring and event management), **5.1** (event processing), **5.2** (event-driven configuration change), and **5.3** (failure troubleshooting). It does not demonstrate complex or large-scale fleet operation, multi-account automation, sustained patching, or production readiness.

## Goal

Produce evidence that one managed node reports inventory, AWS Config detects a deliberately removed tag, a durable event path restores only that tag, a duplicate does not create a second effect, an unsafe termination request is rejected, one failed record does not undo a successful record, failed work reaches a dead-letter queue, and rollback and cleanup are proven.

## Before you start

Read [Operations, observability, and safe automation](../../12-aws/05-operations-and-observability.md), [Accounts, IAM, and the AWS API](../../12-aws/01-identity-and-api.md), and the fleet and event gaps in the [DOP-C02 overlay](../../certs/aws-dop-c02.md#aws-specific-gap-register).

### Choose one path

The local path requires Python 3.9 or newer and a POSIX shell. It takes 45 to 60 minutes, writes less than 100 KB under `.work`, creates no network traffic, and has no cloud cost.

The cloud path requires AWS CLI v2, Python 3, an isolated AWS sandbox with a default or disposable VPC, and permission to create the exact CloudFormation resources in this lab. It takes 90 to 150 minutes. It creates one `t3.micro` EC2 instance, one public IPv4 address when the selected subnet assigns internet reachability, an instance profile and scoped service roles, Systems Manager associations, one Config recorder and rule, one small S3 bucket, two EventBridge rules, two SQS queues, one Lambda function, one DynamoDB on-demand table, and short-retention CloudWatch Logs.

At the published service rates for the chosen Region, the instance, public IPv4 address, Config items and rule evaluations, S3 requests and storage, Lambda, SQS, DynamoDB, EventBridge, and logs are billable dimensions. Verify current regional pricing before starting. Set a USD 5 incremental cost ceiling, a three-hour runtime ceiling, and one-instance ceiling. AWS Budgets is not a hard spending cap. Stop and clean up at the first ceiling.

### Identity assumptions

For the local path, use an unprivileged local user. All account IDs and instance IDs in the fixture are synthetic.

For the cloud path, use a short-lived federated profile named `approved-fleet-lab`. It must be restricted to the isolated sandbox and approved Region. The deployment principal may create and delete the listed stack resources and pass only the stack-created EC2, Config, and Lambda roles. The instance receives `AmazonSSMManagedInstanceCore`; it has no inbound security-group rules and no SSH key. The remediation role can read EC2 instance metadata and add tags only to an existing instance carrying this stack's `LabId`. It cannot stop, start, reboot, terminate, replace, or resize an instance.

> **Do not run the cloud path in production, a shared account, a shared VPC, or any Region that already has an AWS Config recorder or delivery channel.** The supplied template owns both resources and cannot coexist with an existing regional setup. The fixture is disposable. Never broaden the remediation role to make a failed action pass.

### Stop conditions

Stop immediately if any of these occurs:

- Caller account, role, Region, VPC, subnet, or stack name differs from the approved scope.
- The selected Region already has any Config recorder or delivery channel. This is a hard stop; do not deploy the supplied template or delete the existing setup.
- More than one instance would be created, an instance has inbound rules, or a command targets an instance without the exact stack `LabId`.
- Systems Manager does not report the instance online within 15 minutes, Config does not start recording within 15 minutes, or the remediation does not converge within 15 minutes.
- The queue grows beyond 20 messages, Lambda invocations exceed 100, retries continue after the dead-letter threshold, or the DLQ receives more than the one deliberately invalid test record.
- An unsafe request changes EC2 state, a duplicate creates an additional effect, logs contain credentials or customer data, any unexpected resource is modified, or cost/time bounds are reached.
- Stack deletion fails, the Config bucket cannot be emptied safely, or cleanup proof is incomplete.

Before running commands, predict: removing `LabManaged=true` makes the instance noncompliant; EventBridge delivers at least once; SQS retains failed work; the handler's semantic key and idempotent tag operation prevent repeated side effects; `terminate` is rejected; and the valid record in a mixed batch can succeed while an invalid record is retried.

## Establish a local baseline

Refuse to overwrite prior evidence, then create a desired-state document, one current instance, and a bounded event batch. These are synthetic fixtures.

```bash
test ! -e .work || { printf '%s\n' '.work already exists; inspect or remove it first' >&2; exit 1; }
mkdir -p .work/input .work/evidence
python3 --version | tee .work/evidence/python-version.txt
date -u +%Y-%m-%dT%H:%M:%SZ | tee .work/evidence/started-at.txt

cat >.work/input/desired.json <<'JSON'
{
  "fleetLimit": 2,
  "requiredTag": {"key": "LabManaged", "value": "true"},
  "allowedAction": "tag",
  "maxReceives": 3
}
JSON

cat >.work/input/state.json <<'JSON'
{
  "instances": {
    "i-00000000000000001": {
      "ssmPingStatus": "Online",
      "inventoryStatus": "Success",
      "configCompliance": "NON_COMPLIANT",
      "tags": {
        "LabId": "fleet-fixture",
        "Name": "fleet-fixture-node"
      }
    }
  }
}
JSON

cat >.work/input/events.json <<'JSON'
[
  {
    "eventId": "evt-001",
    "semanticKey": "i-00000000000000001|required-tag|capture-001",
    "resourceId": "i-00000000000000001",
    "requestedAction": "tag"
  },
  {
    "eventId": "evt-001-replay",
    "semanticKey": "i-00000000000000001|required-tag|capture-001",
    "resourceId": "i-00000000000000001",
    "requestedAction": "tag"
  },
  {
    "eventId": "evt-unsafe",
    "semanticKey": "i-00000000000000001|terminate|test-001",
    "resourceId": "i-00000000000000001",
    "requestedAction": "terminate"
  },
  {
    "eventId": "evt-missing",
    "semanticKey": "i-00000000000009999|required-tag|test-001",
    "resourceId": "i-00000000000009999",
    "requestedAction": "tag"
  }
]
JSON
```

Verify the starting envelope. The node is online and inventoried but intentionally noncompliant.

```bash
python3 - <<'PY' | tee .work/evidence/baseline.txt
import json
from pathlib import Path

root = Path(".work/input")
desired = json.loads((root / "desired.json").read_text())
state = json.loads((root / "state.json").read_text())
events = json.loads((root / "events.json").read_text())
assert len(state["instances"]) == 1
assert len(state["instances"]) <= desired["fleetLimit"]
node = next(iter(state["instances"].values()))
assert node["ssmPingStatus"] == "Online"
assert node["inventoryStatus"] == "Success"
assert node["configCompliance"] == "NON_COMPLIANT"
assert len(events) == 4
print("PASS one bounded managed node")
print("PASS inventory is current")
print("PASS controlled tag drift is present")
PY
```

## Make local remediation work

Create a small worker. Its ledger is keyed by semantic work rather than transport event ID. Final `SUCCEEDED` and `REJECTED` records are skipped on replay. Failed work is retried three times and then moved to a durable local DLQ. The only mutation is setting `LabManaged=true` on a fixture node already carrying `LabId=fleet-fixture`.

```bash
cp .work/input/state.json .work/input/state.before-remediation.json

cat >.work/worker.py <<'PY'
import json
from pathlib import Path

root = Path(".work")
desired = json.loads((root / "input/desired.json").read_text())
state = json.loads((root / "input/state.json").read_text())
events = json.loads((root / "input/events.json").read_text())
ledger = {}
dlq = []
audit = []
side_effects = 0

pending = [(event, 1) for event in events]
while pending:
    event, receive = pending.pop(0)
    key = event["semanticKey"]
    prior = ledger.get(key)
    if prior and prior["status"] in {"SUCCEEDED", "REJECTED"}:
        audit.append({"eventId": event["eventId"], "result": "DUPLICATE", "receive": receive})
        continue

    if event["requestedAction"] != desired["allowedAction"]:
        ledger[key] = {"status": "REJECTED", "reason": "action outside allowlist"}
        audit.append({"eventId": event["eventId"], "result": "REJECTED", "receive": receive})
        continue

    node = state["instances"].get(event["resourceId"])
    if not node:
        ledger[key] = {"status": "FAILED", "reason": "resource does not exist"}
        audit.append({"eventId": event["eventId"], "result": "FAILED", "receive": receive})
        if receive >= desired["maxReceives"]:
            dlq.append(event)
        else:
            pending.append((event, receive + 1))
        continue

    if node["tags"].get("LabId") != "fleet-fixture":
        ledger[key] = {"status": "REJECTED", "reason": "resource outside lab ownership"}
        audit.append({"eventId": event["eventId"], "result": "REJECTED", "receive": receive})
        continue

    required = desired["requiredTag"]
    if node["tags"].get(required["key"]) != required["value"]:
        node["tags"][required["key"]] = required["value"]
        node["configCompliance"] = "COMPLIANT"
        side_effects += 1
    ledger[key] = {"status": "SUCCEEDED", "reason": "required tag converged"}
    audit.append({"eventId": event["eventId"], "result": "SUCCEEDED", "receive": receive})

(root / "input/state.json").write_text(json.dumps(state, indent=2) + "\n")
(root / "evidence/ledger.json").write_text(json.dumps(ledger, indent=2) + "\n")
(root / "evidence/audit.json").write_text(json.dumps(audit, indent=2) + "\n")
(root / "evidence/dlq.json").write_text(json.dumps(dlq, indent=2) + "\n")
(root / "evidence/summary.json").write_text(json.dumps({
    "sideEffects": side_effects,
    "duplicates": sum(item["result"] == "DUPLICATE" for item in audit),
    "rejected": sum(item["result"] == "REJECTED" for item in audit),
    "failedAttempts": sum(item["result"] == "FAILED" for item in audit),
    "dlqMessages": len(dlq)
}, indent=2) + "\n")
PY

python3 .work/worker.py
python3 - <<'PY' | tee .work/evidence/remediation-check.txt
import json
from pathlib import Path

root = Path(".work")
state = json.loads((root / "input/state.json").read_text())
summary = json.loads((root / "evidence/summary.json").read_text())
ledger = json.loads((root / "evidence/ledger.json").read_text())
node = state["instances"]["i-00000000000000001"]
assert node["tags"]["LabManaged"] == "true"
assert node["configCompliance"] == "COMPLIANT"
assert summary == {
    "sideEffects": 1,
    "duplicates": 1,
    "rejected": 1,
    "failedAttempts": 3,
    "dlqMessages": 1
}
assert ledger["i-00000000000000001|terminate|test-001"]["status"] == "REJECTED"
print("PASS one remediation side effect")
print("PASS duplicate skipped")
print("PASS unsafe terminate rejected")
print("PASS invalid work retried three times and retained in DLQ")
print("PASS valid work survived partial batch failure")
PY

sha256sum .work/input/*.json .work/evidence/*.json \
  | tee .work/evidence/hashes.txt
```

The valid and invalid events share one bounded run. The valid item converges despite the invalid item's retries. The duplicate has a different transport event ID but the same semantic key, so it does not repeat the side effect.

## Break it

Introduce one fault in the worker's authority boundary by changing the node's ownership tag. Do not change the action allowlist.

```bash
cp .work/input/state.before-remediation.json .work/input/state.known-good.json
python3 - <<'PY'
import json
from pathlib import Path

path = Path(".work/input/state.json")
state = json.loads(path.read_text())
node = state["instances"]["i-00000000000000001"]
node["tags"]["LabId"] = "outside-fleet-fixture"
path.write_text(json.dumps(state, indent=2) + "\n")
PY

python3 .work/worker.py
python3 - <<'PY' | tee .work/evidence/broken-check.txt
import json
from pathlib import Path

ledger = json.loads(Path(".work/evidence/ledger.json").read_text())
record = ledger["i-00000000000000001|required-tag|capture-001"]
assert record["status"] == "REJECTED"
assert record["reason"] == "resource outside lab ownership"
print("PASS out-of-scope resource rejected")
PY
```

The expected symptom is rejection, not a broader permission or a forced tag.

## Diagnose, roll back, and recover locally

Start with the ledger's rejection reason. Competing explanations are an unsafe requested action, a missing resource, a duplicate final record, or a failed ownership condition. Inspect the event and resource together.

```bash
python3 - <<'PY'
import json
from pathlib import Path

event = json.loads(Path(".work/input/events.json").read_text())[0]
state = json.loads(Path(".work/input/state.json").read_text())
node = state["instances"][event["resourceId"]]
print("requestedAction=" + event["requestedAction"])
print("resourceId=" + event["resourceId"])
print("LabId=" + node["tags"]["LabId"])
PY
```

The mismatched `LabId` discriminates the authority failure. Roll back all local remediation effects by restoring the pre-remediation state, prove drift is present again, then restore the known-good ownership and rerun to convergence.

```bash
cp .work/input/state.known-good.json .work/input/state.json
python3 - <<'PY' | tee .work/evidence/rollback-proof.txt
import json
from pathlib import Path

state = json.loads(Path(".work/input/state.json").read_text())
node = state["instances"]["i-00000000000000001"]
assert "LabManaged" not in node["tags"]
assert node["configCompliance"] == "NON_COMPLIANT"
print("PASS rollback restored pre-remediation drift")
PY

python3 .work/worker.py
grep -q '"LabManaged": "true"' .work/input/state.json
printf '%s\n' 'PASS recovered to compliant state' | tee .work/evidence/recovery-proof.txt
```

## Optional cloud path

Run this section only in the approved isolated account. The CloudFormation stack is the ownership boundary. It creates one instance and no inbound route to that instance. Systems Manager still needs outbound HTTPS access, provided here by a public subnet with internet routing. A private subnet with approved Systems Manager, S3, and related VPC endpoints is preferable when already available.

### Verify the account and select the network

```bash
test ! -e .work/cloud || { printf '%s\n' '.work/cloud already exists; inspect it first' >&2; exit 1; }
mkdir -p .work/cloud
export AWS_PROFILE=approved-fleet-lab
export AWS_REGION=us-east-1
export AWS_PAGER=
export STACK_NAME=dop-c02-fleet-remediation

aws --version 2>&1 | tee .work/cloud/aws-version.txt
aws sts get-caller-identity | tee .work/cloud/caller.json
aws configure get region | tee .work/cloud/configured-region.txt
aws configservice describe-configuration-recorders \
  | tee .work/cloud/existing-recorders.json
aws configservice describe-delivery-channels \
  | tee .work/cloud/existing-delivery-channels.json
RECORDER_COUNT=$(aws configservice describe-configuration-recorders \
  --query 'length(ConfigurationRecorders)' --output text)
CHANNEL_COUNT=$(aws configservice describe-delivery-channels \
  --query 'length(DeliveryChannels)' --output text)
printf 'recorders=%s\nchannels=%s\n' "$RECORDER_COUNT" "$CHANNEL_COUNT" \
  | tee .work/cloud/config-prerequisite-counts.txt
test "$RECORDER_COUNT" -eq 0 && test "$CHANNEL_COUNT" -eq 0
```

The final test is intentionally a hard stop. If either count is nonzero, do not continue and do not alter the existing Config setup. This lab does not provide an integration mode for an existing recorder or delivery channel. Select one approved VPC and one public subnet; never take the first result without reviewing it.

```bash
aws ec2 describe-vpcs --filters Name=state,Values=available \
  --query 'Vpcs[].{VpcId:VpcId,Default:IsDefault,Tags:Tags}' \
  --output table
read -r VPC_ID
aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'Subnets[].{SubnetId:SubnetId,AZ:AvailabilityZone,PublicIp:MapPublicIpOnLaunch,Tags:Tags}' \
  --output table
read -r SUBNET_ID
test -n "$VPC_ID" && test -n "$SUBNET_ID"
EXISTING_LAB_INSTANCE_COUNT=$(aws ec2 describe-instances \
  --filters "Name=tag:LabId,Values=$STACK_NAME" \
    Name=instance-state-name,Values=pending,running,stopping,stopped \
  --query 'length(Reservations[].Instances[])' --output text)
printf 'existing_lab_instances=%s\n' "$EXISTING_LAB_INSTANCE_COUNT" \
  | tee .work/cloud/existing-lab-instance-count.txt
test "$EXISTING_LAB_INSTANCE_COUNT" -eq 0

AMI_ID=$(aws ssm get-parameter \
  --name /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \
  --query 'Parameter.Value' --output text)
test -n "$AMI_ID"
printf 'vpc=%s\nsubnet=%s\nami=%s\n' "$VPC_ID" "$SUBNET_ID" "$AMI_ID" \
  | tee .work/cloud/selected-target.txt
```

### Create the one-instance stack

Write the complete template locally.

```bash
cat >.work/cloud/stack.yaml <<'YAML'
AWSTemplateFormatVersion: '2010-09-09'
Description: DOP-C02 one-node fleet and safe tag remediation lab
Parameters:
  VpcId:
    Type: AWS::EC2::VPC::Id
  SubnetId:
    Type: AWS::EC2::Subnet::Id
  AmiId:
    Type: AWS::EC2::Image::Id
Resources:
  NodeSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: No inbound access for the fleet lab
      VpcId: !Ref VpcId
      SecurityGroupIngress: []
      Tags:
        - Key: LabId
          Value: !Ref AWS::StackName
  InstanceRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal: {Service: ec2.amazonaws.com}
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
  InstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Roles: [!Ref InstanceRole]
  Node:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !Ref AmiId
      InstanceType: t3.micro
      IamInstanceProfile: !Ref InstanceProfile
      NetworkInterfaces:
        - AssociatePublicIpAddress: true
          DeviceIndex: '0'
          GroupSet: [!Ref NodeSecurityGroup]
          SubnetId: !Ref SubnetId
      Tags:
        - Key: Name
          Value: dop-c02-fleet-node
        - Key: LabId
          Value: !Ref AWS::StackName
        - Key: LabManaged
          Value: 'true'
  InventoryAssociation:
    Type: AWS::SSM::Association
    Properties:
      Name: AWS-GatherSoftwareInventory
      AssociationName: !Sub '${AWS::StackName}-inventory'
      ScheduleExpression: rate(30 minutes)
      Targets:
        - Key: InstanceIds
          Values: [!Ref Node]
  ConfigBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault: {SSEAlgorithm: AES256}
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      LifecycleConfiguration:
        Rules:
          - Id: expire-lab-config
            Status: Enabled
            ExpirationInDays: 1
  ConfigBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref ConfigBucket
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Sid: ConfigBucketAcl
            Effect: Allow
            Principal: {Service: config.amazonaws.com}
            Action: s3:GetBucketAcl
            Resource: !GetAtt ConfigBucket.Arn
            Condition:
              StringEquals:
                AWS:SourceAccount: !Ref AWS::AccountId
          - Sid: ConfigBucketDelivery
            Effect: Allow
            Principal: {Service: config.amazonaws.com}
            Action: s3:PutObject
            Resource: !Sub '${ConfigBucket.Arn}/AWSLogs/${AWS::AccountId}/Config/*'
            Condition:
              StringEquals:
                s3:x-amz-acl: bucket-owner-full-control
                AWS:SourceAccount: !Ref AWS::AccountId
  ConfigRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal: {Service: config.amazonaws.com}
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWS_ConfigRole
  DeliveryChannel:
    Type: AWS::Config::DeliveryChannel
    DependsOn: ConfigBucketPolicy
    Properties:
      S3BucketName: !Ref ConfigBucket
  Recorder:
    Type: AWS::Config::ConfigurationRecorder
    DependsOn: DeliveryChannel
    Properties:
      RoleARN: !GetAtt ConfigRole.Arn
      RecordingGroup:
        AllSupported: false
        IncludeGlobalResourceTypes: false
        ResourceTypes:
          - AWS::EC2::Instance
  RequiredTagRule:
    Type: AWS::Config::ConfigRule
    DependsOn: Recorder
    Properties:
      ConfigRuleName: !Sub '${AWS::StackName}-required-tag'
      InputParameters:
        tag1Key: LabManaged
        tag1Value: 'true'
      Scope:
        ComplianceResourceTypes:
          - AWS::EC2::Instance
        TagKey: LabId
        TagValue: !Ref AWS::StackName
      Source:
        Owner: AWS
        SourceIdentifier: REQUIRED_TAGS
  IdempotencyTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: WorkKey
          AttributeType: S
      KeySchema:
        - AttributeName: WorkKey
          KeyType: HASH
      TimeToLiveSpecification:
        AttributeName: ExpiresAt
        Enabled: true
  DeadLetterQueue:
    Type: AWS::SQS::Queue
    Properties:
      MessageRetentionPeriod: 1209600
  WorkQueue:
    Type: AWS::SQS::Queue
    Properties:
      VisibilityTimeout: 180
      RedrivePolicy:
        deadLetterTargetArn: !GetAtt DeadLetterQueue.Arn
        maxReceiveCount: 3
  RemediationRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal: {Service: lambda.amazonaws.com}
            Action: sts:AssumeRole
      Policies:
        - PolicyName: bounded-remediation
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action: ec2:DescribeInstances
                Resource: '*'
              - Effect: Allow
                Action: ec2:CreateTags
                Resource: !Sub 'arn:${AWS::Partition}:ec2:${AWS::Region}:${AWS::AccountId}:instance/${Node}'
              - Effect: Allow
                Action:
                  - dynamodb:GetItem
                  - dynamodb:PutItem
                  - dynamodb:UpdateItem
                Resource: !GetAtt IdempotencyTable.Arn
              - Effect: Allow
                Action:
                  - sqs:ReceiveMessage
                  - sqs:DeleteMessage
                  - sqs:GetQueueAttributes
                Resource: !GetAtt WorkQueue.Arn
              - Effect: Allow
                Action:
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                Resource: !Sub '${RemediationLogGroup.Arn}:*'
  RemediationFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-remediator'
      Runtime: python3.13
      Handler: index.handler
      Role: !GetAtt RemediationRole.Arn
      Timeout: 30
      Environment:
        Variables:
          TABLE_NAME: !Ref IdempotencyTable
          LAB_ID: !Ref AWS::StackName
          INSTANCE_ID: !Ref Node
      Code:
        ZipFile: |
          import hashlib, json, os, time
          import boto3
          from botocore.exceptions import ClientError
          ddb = boto3.client("dynamodb")
          ec2 = boto3.client("ec2")
          table = os.environ["TABLE_NAME"]
          lab_id = os.environ["LAB_ID"]
          expected_instance_id = os.environ["INSTANCE_ID"]

          def final_status(key):
              item = ddb.get_item(TableName=table, Key={"WorkKey": {"S": key}},
                                  ConsistentRead=True).get("Item", {})
              return item.get("Status", {}).get("S")

          def set_status(key, status, reason):
              ddb.put_item(TableName=table, Item={
                  "WorkKey": {"S": key},
                  "Status": {"S": status},
                  "Reason": {"S": reason[:500]},
                  "ExpiresAt": {"N": str(int(time.time()) + 86400)}
              })

          def claim(key):
              try:
                  ddb.put_item(
                      TableName=table,
                      Item={
                          "WorkKey": {"S": key},
                          "Status": {"S": "IN_PROGRESS"},
                          "Reason": {"S": "claimed"},
                          "ExpiresAt": {"N": str(int(time.time()) + 86400)}
                      },
                      ConditionExpression="attribute_not_exists(WorkKey) OR #status = :failed",
                      ExpressionAttributeNames={"#status": "Status"},
                      ExpressionAttributeValues={":failed": {"S": "FAILED"}}
                  )
                  return True
              except ClientError as error:
                  if error.response["Error"]["Code"] != "ConditionalCheckFailedException":
                      raise
                  return False

          def handler(event, context):
              failures = []
              for record in event.get("Records", []):
                  message_id = record["messageId"]
                  key = None
                  claimed = False
                  try:
                      envelope = json.loads(record["body"])
                      detail = envelope.get("detail", {})
                      resource_id = detail.get("resourceId")
                      action = detail.get("requestedAction", "tag")
                      capture = detail.get("configurationItemCaptureTime",
                                           detail.get("testKey", envelope.get("id", message_id)))
                      key = hashlib.sha256(
                          f"{resource_id}|{action}|{capture}".encode()
                      ).hexdigest()
                      claimed = claim(key)
                      if not claimed:
                          status = final_status(key)
                          if status in {"SUCCEEDED", "REJECTED"}:
                              print(json.dumps({"result": "DUPLICATE", "key": key}))
                              continue
                          raise RuntimeError("semantic work is already in progress")
                      if action != "tag":
                          set_status(key, "REJECTED", "action outside allowlist")
                          print(json.dumps({"result": "REJECTED", "key": key, "action": action}))
                          continue
                      if resource_id != expected_instance_id:
                          set_status(key, "REJECTED", "resource is not the stack instance")
                          print(json.dumps({"result": "REJECTED", "key": key}))
                          continue
                      if envelope.get("source") == "lab.fixture" and detail.get("forceFailure") is True:
                          raise RuntimeError("approved durable-failure injection")
                      response = ec2.describe_instances(InstanceIds=[resource_id])
                      instance = response["Reservations"][0]["Instances"][0]
                      tags = {item["Key"]: item["Value"] for item in instance.get("Tags", [])}
                      if tags.get("LabId") != lab_id:
                          set_status(key, "REJECTED", "resource outside stack ownership")
                          print(json.dumps({"result": "REJECTED", "key": key}))
                          continue
                      ec2.create_tags(Resources=[resource_id],
                                      Tags=[{"Key": "LabManaged", "Value": "true"}])
                      set_status(key, "SUCCEEDED", "required tag converged")
                      print(json.dumps({"result": "SUCCEEDED", "key": key}))
                  except Exception as error:
                      try:
                          if key and claimed:
                              set_status(key, "FAILED", type(error).__name__)
                      finally:
                          print(json.dumps({"result": "FAILED", "messageId": message_id,
                                            "error": type(error).__name__}))
                          failures.append({"itemIdentifier": message_id})
              return {"batchItemFailures": failures}
  RemediationLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/lambda/${AWS::StackName}-remediator'
      RetentionInDays: 1
  EventSourceMapping:
    Type: AWS::Lambda::EventSourceMapping
    Properties:
      EventSourceArn: !GetAtt WorkQueue.Arn
      FunctionName: !Ref RemediationFunction
      BatchSize: 5
      MaximumBatchingWindowInSeconds: 5
      FunctionResponseTypes:
        - ReportBatchItemFailures
  ConfigEventRule:
    Type: AWS::Events::Rule
    Properties:
      EventPattern:
        source: [aws.config]
        detail-type: [Config Rules Compliance Change]
        detail:
          configRuleName: [!Ref RequiredTagRule]
          newEvaluationResult:
            complianceType: [NON_COMPLIANT]
      Targets:
        - Arn: !GetAtt WorkQueue.Arn
          Id: work-queue
  FixtureEventRule:
    Type: AWS::Events::Rule
    Properties:
      EventPattern:
        source: [lab.fixture]
        detail-type: [Lab Remediation Request]
      Targets:
        - Arn: !GetAtt WorkQueue.Arn
          Id: work-queue
  QueuePolicy:
    Type: AWS::SQS::QueuePolicy
    Properties:
      Queues: [!Ref WorkQueue]
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal: {Service: events.amazonaws.com}
            Action: sqs:SendMessage
            Resource: !GetAtt WorkQueue.Arn
            Condition:
              ArnEquals:
                aws:SourceArn:
                  - !GetAtt ConfigEventRule.Arn
                  - !GetAtt FixtureEventRule.Arn
Outputs:
  InstanceId:
    Value: !Ref Node
  ConfigRuleName:
    Value: !Ref RequiredTagRule
  ConfigBucket:
    Value: !Ref ConfigBucket
  WorkQueueUrl:
    Value: !Ref WorkQueue
  DeadLetterQueueUrl:
    Value: !Ref DeadLetterQueue
  TableName:
    Value: !Ref IdempotencyTable
  ConfigEventRuleName:
    Value: !Ref ConfigEventRule
  FixtureEventRuleName:
    Value: !Ref FixtureEventRule
YAML

aws cloudformation validate-template --template-body file://.work/cloud/stack.yaml \
  | tee .work/cloud/template-validation.json
aws cloudformation deploy \
  --stack-name "$STACK_NAME" \
  --template-file .work/cloud/stack.yaml \
  --parameter-overrides VpcId="$VPC_ID" SubnetId="$SUBNET_ID" AmiId="$AMI_ID" \
  --capabilities CAPABILITY_IAM \
  --no-fail-on-empty-changeset
```

Capture outputs without copying identifiers into public evidence.

```bash
aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
  | tee .work/cloud/stack.json
INSTANCE_ID=$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='InstanceId'].OutputValue" --output text)
RULE_NAME=$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='ConfigRuleName'].OutputValue" --output text)
WORK_QUEUE_URL=$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='WorkQueueUrl'].OutputValue" --output text)
DLQ_URL=$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='DeadLetterQueueUrl'].OutputValue" --output text)
TABLE_NAME=$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='TableName'].OutputValue" --output text)
test -n "$INSTANCE_ID" && test -n "$RULE_NAME" && test -n "$WORK_QUEUE_URL"
```

### Prove Systems Manager and inventory baseline

Wait only within the 15-minute stop condition. Query rather than opening a shell.

```bash
aws ssm describe-instance-information \
  --filters "Key=InstanceIds,Values=$INSTANCE_ID" \
  | tee .work/cloud/ssm-instance.json
aws ssm describe-association \
  --association-name "${STACK_NAME}-inventory" \
  | tee .work/cloud/inventory-association.json
aws ssm list-inventory-entries \
  --instance-id "$INSTANCE_ID" --type-name AWS:InstanceInformation \
  | tee .work/cloud/inventory.json
```

Required baseline evidence is `PingStatus=Online`, the intended platform and agent version, successful association status, and at least one inventory entry. An online ping does not prove every SSM document can execute.

### Introduce Config drift and observe remediation

Record the tag and Config status before the change.

```bash
aws ec2 describe-tags \
  --filters "Name=resource-id,Values=$INSTANCE_ID" \
  | tee .work/cloud/tags-before.json
aws configservice get-compliance-details-by-config-rule \
  --config-rule-name "$RULE_NAME" --limit 20 \
  | tee .work/cloud/config-before.json
```

Remove only `LabManaged`. This is the controlled fault.

```bash
aws ec2 delete-tags --resources "$INSTANCE_ID" --tags Key=LabManaged
date -u +%Y-%m-%dT%H:%M:%SZ | tee .work/cloud/drift-started-at.txt
```

Within 15 minutes, capture the noncompliant Config evaluation, then the restored tag and compliant reevaluation.

```bash
aws configservice get-compliance-details-by-config-rule \
  --config-rule-name "$RULE_NAME" --limit 20 \
  | tee .work/cloud/config-after-drift.json
aws ec2 describe-tags \
  --filters "Name=resource-id,Values=$INSTANCE_ID" \
  | tee .work/cloud/tags-after-remediation.json
aws configservice get-compliance-details-by-config-rule \
  --config-rule-name "$RULE_NAME" --limit 20 \
  | tee .work/cloud/config-after-remediation.json
aws sqs get-queue-attributes --queue-url "$WORK_QUEUE_URL" \
  --attribute-names All | tee .work/cloud/work-queue-after.json
```

Do not claim convergence until `LabManaged=true` is present and Config reports `COMPLIANT`. Event delivery and resource evaluation are asynchronous; preserve timestamps rather than treating one immediate query as final.

### Test duplicates and reject an unsafe action

Send the same semantic safe request twice. EventBridge assigns different transport IDs, but `testKey` makes the worker key identical. A conditional DynamoDB claim serializes concurrent duplicates, `create-tags` is itself idempotent, and the final ledger state supplies an auditable duplicate decision.

```bash
export INSTANCE_ID
python3 - <<'PY'
import json
import os
from pathlib import Path

instance_id = os.environ["INSTANCE_ID"]
entries = [{
    "Source": "lab.fixture",
    "DetailType": "Lab Remediation Request",
    "Detail": json.dumps({
        "resourceId": instance_id,
        "requestedAction": "tag",
        "testKey": "duplicate-001"
    })
}]
Path(".work/cloud/duplicate-entry.json").write_text(json.dumps(entries) + "\n")
entries[0]["Detail"] = json.dumps({
    "resourceId": instance_id,
    "requestedAction": "terminate",
    "testKey": "unsafe-001"
})
Path(".work/cloud/unsafe-entry.json").write_text(json.dumps(entries) + "\n")
PY

for copy in 1 2; do
  aws events put-events --entries file://.work/cloud/duplicate-entry.json \
    | tee ".work/cloud/duplicate-${copy}.json"
done

aws events put-events --entries file://.work/cloud/unsafe-entry.json \
  | tee .work/cloud/unsafe-request.json
```

Inspect the idempotency ledger and instance state. There must be one `SUCCEEDED` record for the duplicate key, one `REJECTED` record for the unsafe key, and the instance must remain running.

```bash
aws dynamodb scan --table-name "$TABLE_NAME" --limit 20 \
  | tee .work/cloud/idempotency-ledger.json
aws ec2 describe-instances --instance-ids "$INSTANCE_ID" \
  --query 'Reservations[0].Instances[0].{State:State.Name,Tags:Tags}' \
  | tee .work/cloud/instance-after-negative-tests.json
```

The rejected event proves application allowlisting. The remediation role's absence of EC2 lifecycle actions supplies a separate least-privilege boundary.

### Demonstrate partial failure and durable handling

Send one valid record and one record carrying the explicit `forceFailure=true` lab fixture flag directly to the work queue. Both name the exact stack instance, so this test does not target another resource. Direct delivery makes the records eligible for one Lambda batch. The valid action is harmless convergence; the injected failure is returned in `batchItemFailures`, retried, and moved to the DLQ after the configured receive threshold.

```bash
export INSTANCE_ID
python3 - <<'PY'
import json
import os
from pathlib import Path

entries = [
    {
        "Id": "valid",
        "MessageBody": json.dumps({
            "id": "partial-valid",
            "source": "lab.fixture",
            "detail": {
                "resourceId": os.environ["INSTANCE_ID"],
                "requestedAction": "tag",
                "testKey": "partial-001"
            }
        })
    },
    {
        "Id": "invalid",
        "MessageBody": json.dumps({
            "id": "partial-injected-failure",
            "source": "lab.fixture",
            "detail": {
                "resourceId": os.environ["INSTANCE_ID"],
                "requestedAction": "tag",
                "testKey": "partial-failure-001",
                "forceFailure": True
            }
        })
    }
]
Path(".work/cloud/partial-entries.json").write_text(json.dumps(entries) + "\n")
PY
aws sqs send-message-batch --queue-url "$WORK_QUEUE_URL" \
  --entries file://.work/cloud/partial-entries.json \
  | tee .work/cloud/partial-batch-submit.json
```

Run the submission again only if it failed before SQS accepted any entry. Never duplicate the invalid test after acceptance. Within 15 minutes, the work queue should drain and the DLQ should contain exactly one message. Confirm from the Lambda request ID that both records were handled in the same invocation; if they were not, retain the result but do not claim cloud partial-batch evidence. The local path remains the deterministic partial-failure proof.

```bash
aws sqs get-queue-attributes --queue-url "$WORK_QUEUE_URL" \
  --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible \
  | tee .work/cloud/work-queue-partial.json
aws sqs get-queue-attributes --queue-url "$DLQ_URL" \
  --attribute-names ApproximateNumberOfMessages \
  | tee .work/cloud/dlq-count.json
aws sqs receive-message --queue-url "$DLQ_URL" \
  --max-number-of-messages 1 --visibility-timeout 0 \
  --attribute-names ApproximateReceiveCount \
  | tee .work/cloud/dlq-evidence.json
```

Do not delete the DLQ message until its body, receive count, timestamps, and corresponding Lambda failure records are retained. The valid ledger record proves successful work was not replayed merely because another item failed.

### Roll back and recover in the cloud

Rollback must not race the remediator. Disable both EventBridge rules and the Lambda event source mapping before removing the managed tag. Read the rule names from stack outputs, identify the mapping by the stack function, and continue only after the mapping state is `Disabled` and the work queue is empty.

```bash
CONFIG_EVENT_RULE=$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='ConfigEventRuleName'].OutputValue" --output text)
FIXTURE_EVENT_RULE=$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='FixtureEventRuleName'].OutputValue" --output text)
aws events disable-rule --name "$CONFIG_EVENT_RULE"
aws events disable-rule --name "$FIXTURE_EVENT_RULE"
MAPPING_UUID=$(aws lambda list-event-source-mappings \
  --function-name "${STACK_NAME}-remediator" \
  --query 'EventSourceMappings[0].UUID' --output text)
test -n "$MAPPING_UUID" && test "$MAPPING_UUID" != "None"
aws lambda update-event-source-mapping --uuid "$MAPPING_UUID" --no-enabled \
  | tee .work/cloud/rollback-mapping-disable.json
aws lambda get-event-source-mapping --uuid "$MAPPING_UUID" \
  | tee .work/cloud/rollback-mapping-state.json
aws sqs get-queue-attributes --queue-url "$WORK_QUEUE_URL" \
  --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible \
  | tee .work/cloud/rollback-queue-state.json
```

The mapping update is asynchronous. Repeat only the two read-only state queries within the 15-minute bound until the mapping says `Disabled` and both queue counts are zero; otherwise stop before deleting the tag. After those conditions hold, remove the tag and capture the rollback state.

```bash
aws ec2 delete-tags --resources "$INSTANCE_ID" --tags Key=LabManaged
aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" \
  | tee .work/cloud/rollback-tags.json
```

The missing tag is rollback proof for the one remediation effect. It deliberately leaves Config drift and is not the final recovered state. Re-enable the mapping and rules, then send one safe request to restore the tag.

```bash
aws lambda update-event-source-mapping --uuid "$MAPPING_UUID" --enabled \
  | tee .work/cloud/recovery-mapping-enable.json
aws events enable-rule --name "$CONFIG_EVENT_RULE"
aws events enable-rule --name "$FIXTURE_EVENT_RULE"
python3 - <<'PY'
import json
import os
from pathlib import Path

entries = [{
    "Source": "lab.fixture",
    "DetailType": "Lab Remediation Request",
    "Detail": json.dumps({
        "resourceId": os.environ["INSTANCE_ID"],
        "requestedAction": "tag",
        "testKey": "recovery-001"
    })
}]
Path(".work/cloud/recovery-entry.json").write_text(json.dumps(entries) + "\n")
PY
aws events put-events --entries file://.work/cloud/recovery-entry.json \
  | tee .work/cloud/recovery-request.json
aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" \
  | tee .work/cloud/recovery-tags.json
```

Recovery requires the restored tag, a running instance, drained work queue, and no DLQ message beyond the one expected injected-failure fixture.

## Exact evidence record

Complete every row. Cloud-only rows cannot be satisfied by local output. Every mapped DOP-C02 row is guided mechanism evidence for this bounded fixture; none establishes organization-wide or large-scale competency.

| Evidence ID | DOP-C02 ID | Exact artifact and required observation | Path | Claim limit |
|---|---|---|---|---|
| FLT-01 | 2.1, 2.3 | Approved caller, Region, VPC, subnet, AMI ID, stack ID, and exactly one instance | Cloud | Does not prove production suitability |
| FLT-02 | 2.3 | SSM managed node is online with agent/platform metadata | Cloud | Online does not prove all documents work |
| FLT-03 | 2.1, 2.3 | `AWS-GatherSoftwareInventory` association succeeds and inventory has an observed timestamp | Cloud | One inventory sample does not prove continuous freshness |
| CFG-01 | 4.3, 5.2 | Required-tags rule records `NON_COMPLIANT` after tag removal | Cloud | Evaluation latency must be recorded |
| EVT-01 | 4.3, 5.1 | EventBridge rule, SQS queue, Lambda log, and ledger correlate one semantic event | Cloud | At-least-once delivery is not ordering |
| REM-01 | 5.2 | Tag returns as `LabManaged=true` and Config later reports `COMPLIANT` | Cloud | One tag does not establish a full baseline |
| IDE-01 | 2.3, 5.1 | Two transport events share one semantic key, with one success and one duplicate audit result | Local and cloud | Does not prove concurrency safety at large scale |
| SAF-01 | 5.2 | `terminate` request is `REJECTED`; instance remains running; role lacks lifecycle actions | Local and cloud | Application rejection and IAM denial are distinct controls |
| PAR-01 | 5.1, 5.3 | Mixed batch has valid success and one controlled failure; only failed item is retried | Local and cloud | Guided one-node evidence; does not measure high-volume behavior |
| DLQ-01 | 5.1, 5.3 | Controlled failure reaches DLQ with a configured maximum receive count of three; retain its observed receive count and body | Local and cloud | DLQ retention still requires an owner and alarm |
| RBK-01 | 5.2, 5.3 | Disabled trigger plus removed tag proves rollback; recovery request restores tag | Local and cloud | Tag rollback does not revert unrelated state |
| LOC-01 | 2.3, 5.1 | Local summary is exactly one side effect, one duplicate, one rejection, three failed attempts, one DLQ item | Local | Static fixture is not AWS service evidence |
| CLN-01 | 2.1, 5.3 | Instance absent, stack absent, Config recorder/channel absent, queues/table/function absent, bucket absent, and local workspace removed | Cloud and local | Billing data can lag cleanup |

Every record needs a timestamp, exact command or fixture input, raw output path, SHA-256, interpretation, contradictory evidence, and limitation. Approximate SQS counts are operational hints; use message and Lambda records for the exact test claim.

## Failure diagnosis and recovery

Start from the visible symptom and preserve event times before changing anything.

| Symptom | Ranked competing explanations | First discriminating evidence | Safe recovery |
|---|---|---|---|
| Node never becomes SSM managed | No outbound HTTPS path, wrong instance profile, agent failure, or wrong Region | EC2 state, profile attachment, subnet route, and SSM registration | Stop at 15 minutes; fix only the disposable network or role and redeploy |
| Inventory is empty | Association pending/failed, wrong target, unsupported inventory type, or stale query | Association execution status and instance ID | Wait within bound or correct the association target |
| Config never reports drift | Recorder stopped, wrong resource scope, rule pending, or tag was not removed | Recorder status, rule status, and live tags | Do not remove another control; correct recording in the disposable stack |
| Event reaches no queue | Pattern mismatch, rule disabled, missing queue policy, or wrong Region | Event rule metrics/configuration and queue policy | Correct the exact pattern or policy through the template |
| Queue grows | Lambda mapping disabled, permission failure, timeout, or poison record | Mapping state, oldest message age, and structured Lambda failure | Disable rules at 20 messages, retain one failure, then correct narrowly |
| Tag is not restored | Ownership condition failed, instance missing, role denied, or handler rejected action | Ledger status, Lambda error type, live `LabId`, and CloudTrail request | Restore only the correct ownership tag or policy condition; never add lifecycle permissions |
| Duplicate causes repeated mutation | Semantic key changed, final state not retained, or concurrent processing | Ledger keys, transport IDs, and CloudTrail `CreateTags` count | Disable fixture rule, repair key derivation, and replay once |
| Unsafe action changes state | Handler allowlist bypass or role too broad | Instance state, request detail, role policy, and CloudTrail | Stop immediately, disable both rules and mapping, preserve evidence, notify owner |
| Invalid item never reaches DLQ | Redrive policy wrong, visibility timeout, mapping response mode, or worker not retrying | queue redrive policy, receive count, mapping `FunctionResponseTypes` | Correct template and use one fresh invalid key only |
| Stack deletion fails | Config delivery still writing or S3 bucket not empty | CloudFormation failure event and bucket versions | Stop recorder, empty only the stack bucket, then retry deletion |

Recovery is complete when the expected tag and Config compliance return, the instance remains running, the work queue drains, the DLQ contains only the expected retained failure until cleanup, and all trigger rules are in their intended state.

## Clean up and prove it

Delete the cloud fixture before removing local evidence. First stop Config recording to prevent new delivery, purge the two lab queues, and empty only the bucket named by the stack output.

```bash
CONFIG_BUCKET=$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='ConfigBucket'].OutputValue" --output text)
RECORDER_NAME=$(aws configservice describe-configuration-recorders \
  --query 'ConfigurationRecorders[0].name' --output text)
test -n "$CONFIG_BUCKET" && test -n "$RECORDER_NAME"
aws configservice stop-configuration-recorder \
  --configuration-recorder-name "$RECORDER_NAME"
aws sqs purge-queue --queue-url "$WORK_QUEUE_URL"
aws sqs purge-queue --queue-url "$DLQ_URL"
aws s3 rm "s3://$CONFIG_BUCKET" --recursive
aws cloudformation delete-stack --stack-name "$STACK_NAME"
aws cloudformation wait stack-delete-complete --stack-name "$STACK_NAME"
```

Prove billable resources and control-plane fixtures are gone. Empty results are expected.

```bash
aws ec2 describe-instances --instance-ids "$INSTANCE_ID" \
  --query 'Reservations[].Instances[?State.Name!=`terminated`].[InstanceId,State.Name]' \
  | tee .work/cloud/cleanup-instance.json
aws configservice describe-configuration-recorders \
  | tee .work/cloud/cleanup-recorders.json
aws configservice describe-delivery-channels \
  | tee .work/cloud/cleanup-channels.json
set +e
aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
  >.work/cloud/cleanup-stack.txt 2>&1
stack_lookup_status=$?
set -e
test "$stack_lookup_status" -ne 0
date -u +%Y-%m-%dT%H:%M:%SZ | tee .work/cloud/cleanup-at.txt
```

Inspect CloudFormation events if deletion fails. Do not manually delete unrelated account resources. Billing and Config dashboards may lag, so retain the deletion timestamp and stack absence as immediate proof, then follow the sandbox owner's delayed billing check.

After transferring redacted evidence to its approved location, remove local files and environment variables.

```bash
unset AWS_PROFILE AWS_REGION AWS_PAGER STACK_NAME VPC_ID SUBNET_ID AMI_ID
unset INSTANCE_ID RULE_NAME WORK_QUEUE_URL DLQ_URL TABLE_NAME CONFIG_BUCKET
unset CONFIG_EVENT_RULE FIXTURE_EVENT_RULE MAPPING_UUID RECORDER_NAME
unset RECORDER_COUNT CHANNEL_COUNT EXISTING_LAB_INSTANCE_COUNT
rm -rf .work
test ! -e .work && printf '%s\n' 'PASS local cleanup'
```

## What to keep

Keep the prediction, identity and target proof, service versions, stack template hash, inventory timestamp, Config transition, event correlation, idempotency ledger, rejected unsafe request, mixed-batch timeline, DLQ record, rollback and recovery proof, cleanup proof, cost window, and limitations.

Explain without notes why Systems Manager managed status and inventory are different evidence, why EventBridge and SQS imply duplicate-aware processing, why a DLQ is durable failure evidence rather than automatic recovery, why partial batch responses matter, and why remediation authority excludes instance lifecycle actions.

The local path demonstrates bounded control-flow reasoning mapped to DOP-C02 **2.3**, **5.1**, **5.2**, and **5.3**, but it does not close AWS product gaps. The cloud path supplies only guided mechanism evidence for the six mapped IDs within this one-node, one-Region fixture. Task **2.3** explicitly includes complex and large-scale environments, which this lab does not prove. Production fleet scale, patch compliance across operating systems, multi-account operation, concurrency under load, and sustained automation all remain open.

## Sources

- [AWS Systems Manager managed node concepts](https://docs.aws.amazon.com/systems-manager/latest/userguide/managed_nodes.html)
- [AWS Systems Manager Inventory](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-inventory.html)
- [AWS Systems Manager State Manager associations](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-state.html)
- [AWS Systems Manager Patch Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager.html)
- [AWS Config managed rule required-tags](https://docs.aws.amazon.com/config/latest/developerguide/required-tags.html)
- [AWS Config configuration recorder](https://docs.aws.amazon.com/config/latest/developerguide/stop-start-recorder.html)
- [Amazon EventBridge events from AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/monitor-config-with-cloudwatchevents.html)
- [Amazon EventBridge event patterns](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html)
- [Amazon SQS dead-letter queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html)
- [AWS Lambda partial batch responses for SQS](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html)
- [AWS Lambda idempotency guidance](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Amazon EC2 resource-level permissions for tagging](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-policy-example-create-tags.html)
