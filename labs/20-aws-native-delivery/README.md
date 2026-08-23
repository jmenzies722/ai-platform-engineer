# Lab: Operate an AWS-Native Delivery Path

Build a small CodePipeline and CodeBuild path that tests source, publishes an
immutable Amazon ECR image, deploys it to AWS Lambda by digest, fails two
different gates, and recovers the last known-good deployment. The lab closes a
bounded part of GAP-1 in the
[DOP-C02 overlay](../../certs/aws-dop-c02.md#aws-specific-gap-register). It does
not create a separate certification course or claim production readiness.

## Goal and DOP-C02 tasks

Produce evidence that one reviewed source bundle passed a build gate, became an
ECR digest, and ran as the Lambda deployment. Then prove that a pre-deployment
gate prevents change and that a failed post-deployment check can be diagnosed
and recovered by selecting the retained digest.

This lab supplies direct guided evidence for these exact DOP-C02 task IDs:

- **1.1 Implement CI/CD pipelines**
- **1.2 Integrate automated testing into CI/CD pipelines**
- **1.3 Build and manage artifacts**
- **1.4 Implement deployment strategies for instance, container, and serverless environments**

The diagnosis, role-policy inspection, and CloudTrail lookup provide supporting
practice for tasks **4.2**, **5.3**, **6.1**, and **6.3**. They do not directly
satisfy those tasks: this lab does not build a monitoring system, exercise IAM
at scale, or establish a durable security-audit architecture.

The canonical delivery concepts remain in
[DevOps](../../13-devops/README.md). This exercise adds AWS product practice.

## Safety, identity, cost, and stop conditions

**Run the AWS steps only in an authorized disposable sandbox account. Never run
them in production, a shared development account, or an account containing
customer data.** The source and responses in this lab are synthetic.

Use a short-lived federated role. Because this template does not assign a
CloudFormation service role, the human lab role performs stack operations with
its own permissions. It must be allowed to create, inspect, update, and delete
the one stack and its bounded S3, ECR, Secrets Manager, IAM, CodeBuild, and
CodePipeline resources. That includes creating and deleting the three service
roles, attaching the Lambda basic logging managed policy, putting the inline
role policies, passing those roles to their declared AWS services, and setting
the lab ECR repository policy. The operator also uploads and removes lab S3
objects, starts and inspects pipeline and build executions, reads the lab build
logs, gets the lab ECR repository policy, describes and deletes lab images,
invokes and rolls back the one Lambda function, reads CloudTrail event history,
and performs the cleanup checks. It needs `iam:GetRole` and
`iam:SimulatePrincipalPolicy` for the read-only policy check.

The CodePipeline role can read only the lab source bucket, use the artifact
bucket, and start the one build project. The CodeBuild role can write only the
named build project's CloudWatch Logs group and streams, use the artifact
bucket and one ECR repository, read the one generated secret, and create or
update the one Lambda function while passing only its execution role. Lambda
receives a separate basic logging role. The ECR repository policy grants the
Lambda service only image-layer retrieval for this lab function. No long-lived
IAM user key is needed.

Expected working time is 75 to 105 minutes. Keep all work in one account and
one Region, one pipeline, one CodeBuild `BUILD_GENERAL1_SMALL` project with a
15-minute timeout, one ECR repository, one Lambda function, one secret, and two
S3 buckets. Keep at most five images and five source object versions. Stop and
clean up before two hours or USD 3 of estimated lab spend, whichever comes
first. Billing dimensions include CodeBuild minutes, CodePipeline activity,
ECR and S3 storage, Secrets Manager secret time and API calls, Lambda requests
and duration, CloudWatch Logs ingestion and retention, and data transfer.
Actual prices vary by Region and account benefits; check the AWS Billing
console before starting.

Stop immediately if any of these conditions occurs:

- `aws sts get-caller-identity` shows an unapproved account or principal.
- the configured Region is not the approved sandbox Region;
- a command would affect a resource whose name does not begin with the recorded
  lab prefix;
- CloudFormation proposes resources outside the bounded inventory above;
- a build runs for 15 minutes, a pipeline execution remains active for 20
  minutes, or retries would exceed two source uploads per fault;
- output contains a secret value, credentials, customer data, or an unredacted
  account identifier intended for public evidence;
- the estimated spend reaches USD 3, authorization changes, cleanup fails, or
  any resource appears outside this lab stack.

Do not print the generated secret. CloudTrail records API request metadata, not
permission to publish raw event records. Keep cloud evidence in an approved
encrypted location and redact account IDs, ARNs, bucket names, request IDs, and
log content before sharing it.

## Prerequisites

- AWS CLI v2, Docker, `jq`, `zip`, Bash, and Git
- an approved sandbox Region that supports CodePipeline, CodeBuild, ECR,
  Lambda container images, Secrets Manager, CloudFormation, and CloudTrail
  event history
- Docker able to build Linux AMD64 images
- familiarity with the
  [local evidence-preserving delivery lab](../../13-devops/lab-delivery-evidence.md)
- account-owner approval for the identity and maximum spend above

The commands use the current AWS CLI service models. Record `aws --version`,
`docker version`, the date, and the Region with the evidence.

## Before you start

Create a private local directory and establish identity. The random suffix
prevents collisions; it is not a security boundary.

```bash
export AWS_PROFILE=approved-sandbox
export AWS_REGION=us-east-1
export AWS_PAGER=
export LAB_ID="dop-delivery-$(openssl rand -hex 4)"
export STACK_NAME="$LAB_ID"
export WORK_DIR="/tmp/$LAB_ID"
mkdir -p "$WORK_DIR/source"
chmod 700 "$WORK_DIR"

aws sts get-caller-identity >"$WORK_DIR/identity.json"
aws configure get region
aws --version
docker version --format '{{.Server.Version}}'
jq '{Account,Arn}' "$WORK_DIR/identity.json"
```

Have the account owner confirm the account, role, Region, prefix, resource
count, and spend ceiling. Stop if any value is unexpected. Before creating
anything, predict:

1. a healthy source bundle will reach `Succeeded` and Lambda will return
   `{"version":"one","healthy":true}`;
2. a source gate set to `fail` will stop in CodeBuild before `docker build`;
3. an image that reports unhealthy will be deployed, fail post-deployment
   verification, and require explicit recovery to the recorded baseline digest.

## Create the bounded infrastructure

Write the CloudFormation template locally. The ECR repository rejects tag
overwrites. CodeBuild nevertheless deploys the digest URI, so the running
identity does not depend on a mutable tag.

```bash
cat >"$WORK_DIR/infrastructure.yaml" <<'YAML'
AWSTemplateFormatVersion: '2010-09-09'
Description: Bounded DOP-C02 native delivery lab
Resources:
  SourceBucket:
    Type: AWS::S3::Bucket
    Properties:
      VersioningConfiguration:
        Status: Enabled
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
  ArtifactBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      LifecycleConfiguration:
        Rules:
          - Id: expire-artifacts
            Status: Enabled
            ExpirationInDays: 1
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
  Repository:
    Type: AWS::ECR::Repository
    Properties:
      ImageTagMutability: IMMUTABLE
      ImageScanningConfiguration:
        ScanOnPush: true
      RepositoryPolicyText:
        Version: '2012-10-17'
        Statement:
          - Sid: LambdaECRImageRetrievalPolicy
            Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action:
              - ecr:BatchGetImage
              - ecr:GetDownloadUrlForLayer
            Condition:
              ArnLike:
                aws:SourceArn: !Sub arn:${AWS::Partition}:lambda:${AWS::Region}:${AWS::AccountId}:function:${AWS::StackName}-function
      LifecyclePolicy:
        LifecyclePolicyText: >-
          {"rules":[{"rulePriority":1,"description":"retain five",
          "selection":{"tagStatus":"any","countType":"imageCountMoreThan",
          "countNumber":5},"action":{"type":"expire"}}]}
  BuildSecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Description: Synthetic secret used only to test build-time retrieval
      GenerateSecretString:
        PasswordLength: 32
        ExcludePunctuation: true
  LambdaRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
  BuildRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: codebuild.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: bounded-build
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogGroup
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                Resource:
                  - !Sub arn:${AWS::Partition}:logs:${AWS::Region}:${AWS::AccountId}:log-group:/aws/codebuild/${AWS::StackName}-build
                  - !Sub arn:${AWS::Partition}:logs:${AWS::Region}:${AWS::AccountId}:log-group:/aws/codebuild/${AWS::StackName}-build:*
              - Effect: Allow
                Action:
                  - s3:GetBucketAcl
                  - s3:GetBucketLocation
                  - s3:GetObject
                  - s3:GetObjectVersion
                  - s3:PutObject
                Resource:
                  - !GetAtt ArtifactBucket.Arn
                  - !Sub ${ArtifactBucket.Arn}/*
              - Effect: Allow
                Action: ecr:GetAuthorizationToken
                Resource: '*'
              - Effect: Allow
                Action:
                  - ecr:BatchCheckLayerAvailability
                  - ecr:BatchGetImage
                  - ecr:CompleteLayerUpload
                  - ecr:GetDownloadUrlForLayer
                  - ecr:InitiateLayerUpload
                  - ecr:PutImage
                  - ecr:UploadLayerPart
                Resource: !GetAtt Repository.Arn
              - Effect: Allow
                Action: secretsmanager:GetSecretValue
                Resource: !Ref BuildSecret
              - Effect: Allow
                Action:
                  - lambda:CreateFunction
                  - lambda:GetFunction
                  - lambda:GetFunctionConfiguration
                  - lambda:InvokeFunction
                  - lambda:UpdateFunctionCode
                Resource: !Sub arn:${AWS::Partition}:lambda:${AWS::Region}:${AWS::AccountId}:function:${AWS::StackName}-function
              - Effect: Allow
                Action: iam:PassRole
                Resource: !GetAtt LambdaRole.Arn
                Condition:
                  StringEquals:
                    iam:PassedToService: lambda.amazonaws.com
  BuildProject:
    Type: AWS::CodeBuild::Project
    Properties:
      Name: !Sub ${AWS::StackName}-build
      ServiceRole: !GetAtt BuildRole.Arn
      TimeoutInMinutes: 15
      QueuedTimeoutInMinutes: 15
      Artifacts:
        Type: CODEPIPELINE
      Source:
        Type: CODEPIPELINE
        BuildSpec: buildspec.yml
      Environment:
        Type: LINUX_CONTAINER
        ComputeType: BUILD_GENERAL1_SMALL
        Image: aws/codebuild/standard:7.0
        PrivilegedMode: true
        EnvironmentVariables:
          - Name: REPOSITORY_URI
            Value: !GetAtt Repository.RepositoryUri
          - Name: FUNCTION_NAME
            Value: !Sub ${AWS::StackName}-function
          - Name: LAMBDA_ROLE_ARN
            Value: !GetAtt LambdaRole.Arn
          - Name: SECRET_ARN
            Value: !Ref BuildSecret
  PipelineRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: codepipeline.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: bounded-pipeline
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetBucketVersioning
                  - s3:GetObject
                  - s3:GetObjectVersion
                Resource:
                  - !GetAtt SourceBucket.Arn
                  - !Sub ${SourceBucket.Arn}/*
              - Effect: Allow
                Action:
                  - s3:GetBucketVersioning
                  - s3:GetObject
                  - s3:GetObjectVersion
                  - s3:PutObject
                Resource:
                  - !GetAtt ArtifactBucket.Arn
                  - !Sub ${ArtifactBucket.Arn}/*
              - Effect: Allow
                Action:
                  - codebuild:StartBuild
                  - codebuild:BatchGetBuilds
                Resource: !GetAtt BuildProject.Arn
  Pipeline:
    Type: AWS::CodePipeline::Pipeline
    Properties:
      RoleArn: !GetAtt PipelineRole.Arn
      ArtifactStore:
        Type: S3
        Location: !Ref ArtifactBucket
      Stages:
        - Name: Source
          Actions:
            - Name: S3Source
              ActionTypeId:
                Category: Source
                Owner: AWS
                Provider: S3
                Version: '1'
              Configuration:
                S3Bucket: !Ref SourceBucket
                S3ObjectKey: source.zip
                PollForSourceChanges: false
              OutputArtifacts:
                - Name: SourceOutput
              RunOrder: 1
        - Name: BuildTestDeploy
          Actions:
            - Name: Build
              ActionTypeId:
                Category: Build
                Owner: AWS
                Provider: CodeBuild
                Version: '1'
              Configuration:
                ProjectName: !Ref BuildProject
              InputArtifacts:
                - Name: SourceOutput
              OutputArtifacts:
                - Name: BuildEvidence
              RunOrder: 1
Outputs:
  SourceBucket:
    Value: !Ref SourceBucket
  ArtifactBucket:
    Value: !Ref ArtifactBucket
  RepositoryUri:
    Value: !GetAtt Repository.RepositoryUri
  PipelineName:
    Value: !Ref Pipeline
  FunctionName:
    Value: !Sub ${AWS::StackName}-function
  SecretArn:
    Value: !Ref BuildSecret
  BuildRoleArn:
    Value: !GetAtt BuildRole.Arn
YAML

aws cloudformation validate-template \
  --template-body "file://$WORK_DIR/infrastructure.yaml" >/dev/null
aws cloudformation deploy \
  --stack-name "$STACK_NAME" \
  --template-file "$WORK_DIR/infrastructure.yaml" \
  --capabilities CAPABILITY_IAM \
  --no-fail-on-empty-changeset
aws cloudformation wait stack-create-complete --stack-name "$STACK_NAME"
```

Inspect the stack resources before continuing. Stop if the inventory exceeds
the declared resources.

```bash
aws cloudformation list-stack-resources --stack-name "$STACK_NAME" \
  >"$WORK_DIR/stack-resources.json"
jq -r '.StackResourceSummaries[] |
  [.ResourceType,.ResourceStatus] | @tsv' "$WORK_DIR/stack-resources.json"

export SOURCE_BUCKET="$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" --query \
  'Stacks[0].Outputs[?OutputKey==`SourceBucket`].OutputValue' --output text)"
export ARTIFACT_BUCKET="$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" --query \
  'Stacks[0].Outputs[?OutputKey==`ArtifactBucket`].OutputValue' --output text)"
export REPOSITORY_URI="$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" --query \
  'Stacks[0].Outputs[?OutputKey==`RepositoryUri`].OutputValue' --output text)"
export PIPELINE_NAME="$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" --query \
  'Stacks[0].Outputs[?OutputKey==`PipelineName`].OutputValue' --output text)"
export SECRET_ARN="$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" --query \
  'Stacks[0].Outputs[?OutputKey==`SecretArn`].OutputValue' --output text)"
export BUILD_ROLE_ARN="$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" --query \
  'Stacks[0].Outputs[?OutputKey==`BuildRoleArn`].OutputValue' --output text)"
export FUNCTION_NAME="$STACK_NAME-function"
```

## Establish a healthy baseline

Create the synthetic function and build instructions. The secret is checked for
presence and immediately unset; its value is neither an image build argument
nor an artifact.

```bash
cat >"$WORK_DIR/source/app.py" <<'PY'
import json

def handler(event, context):
    return {"version": "one", "healthy": True}
PY

cat >"$WORK_DIR/source/Dockerfile" <<'DOCKER'
FROM public.ecr.aws/lambda/python:3.12
COPY app.py ${LAMBDA_TASK_ROOT}/
CMD ["app.handler"]
DOCKER

printf 'pass\n' >"$WORK_DIR/source/gate.txt"

cat >"$WORK_DIR/source/buildspec.yml" <<'YAML'
version: 0.2
phases:
  pre_build:
    commands:
      - test "$(tr -d '\r\n' < gate.txt)" = "pass"
      - BUILD_SECRET="$(aws secretsmanager get-secret-value --secret-id "$SECRET_ARN" --query SecretString --output text)"
      - test -n "$BUILD_SECRET"
      - unset BUILD_SECRET
      - ACCOUNT_REGISTRY="${REPOSITORY_URI%/*}"
      - aws ecr get-login-password | docker login --username AWS --password-stdin "$ACCOUNT_REGISTRY"
      - IMAGE_TAG="build-${CODEBUILD_BUILD_NUMBER}"
  build:
    commands:
      - docker build --platform linux/amd64 -t "$REPOSITORY_URI:$IMAGE_TAG" .
      - docker push "$REPOSITORY_URI:$IMAGE_TAG"
      - DIGEST="$(aws ecr describe-images --repository-name "${REPOSITORY_URI##*/}" --image-ids imageTag="$IMAGE_TAG" --query 'imageDetails[0].imageDigest' --output text)"
      - IMAGE_URI="$REPOSITORY_URI@$DIGEST"
  post_build:
    commands:
      - if aws lambda get-function --function-name "$FUNCTION_NAME" >/dev/null 2>&1; then aws lambda update-function-code --function-name "$FUNCTION_NAME" --image-uri "$IMAGE_URI" >/dev/null; else aws lambda create-function --function-name "$FUNCTION_NAME" --package-type Image --code ImageUri="$IMAGE_URI" --role "$LAMBDA_ROLE_ARN" --timeout 10 >/dev/null; fi
      - aws lambda wait function-updated --function-name "$FUNCTION_NAME"
      - aws lambda invoke --function-name "$FUNCTION_NAME" --cli-binary-format raw-in-base64-out --payload '{}' response.json >/dev/null
      - jq -e '.healthy == true' response.json
      - printf '{"image_uri":"%s","build_id":"%s"}\n' "$IMAGE_URI" "$CODEBUILD_BUILD_ID" > deployment.json
artifacts:
  files:
    - deployment.json
    - response.json
YAML

(cd "$WORK_DIR/source" && zip -q -r "$WORK_DIR/source.zip" .)
aws s3 cp "$WORK_DIR/source.zip" "s3://$SOURCE_BUCKET/source.zip"
export EXECUTION_ID="$(aws codepipeline start-pipeline-execution \
  --name "$PIPELINE_NAME" --query pipelineExecutionId --output text)"
```

Poll no more than once every 15 seconds and stop after 20 minutes:

```bash
for attempt in $(seq 1 80); do
  STATUS="$(aws codepipeline get-pipeline-execution \
    --pipeline-name "$PIPELINE_NAME" \
    --pipeline-execution-id "$EXECUTION_ID" \
    --query pipelineExecution.status --output text)"
  printf '%s %s\n' "$(date -u +%FT%TZ)" "$STATUS"
  case "$STATUS" in
    Succeeded) break ;;
    Failed|Stopped|Superseded|Cancelled) exit 1 ;;
  esac
  sleep 15
done
test "$STATUS" = "Succeeded"

aws codepipeline list-action-executions \
  --pipeline-name "$PIPELINE_NAME" \
  --filter "pipelineExecutionId=$EXECUTION_ID" \
  >"$WORK_DIR/baseline-actions.json"
export BASELINE_BUILD_ID="$(jq -r '.actionExecutionDetails[] |
  select(.actionName=="Build") |
  .output.executionResult.externalExecutionId' \
  "$WORK_DIR/baseline-actions.json")"
aws codebuild batch-get-builds --ids "$BASELINE_BUILD_ID" \
  >"$WORK_DIR/baseline-build.json"
export BASELINE_BUILD_START="$(jq -r '.builds[0].startTime' \
  "$WORK_DIR/baseline-build.json")"
export BASELINE_BUILD_END="$(jq -r '.builds[0].endTime' \
  "$WORK_DIR/baseline-build.json")"
test "$BASELINE_BUILD_START" != "null"
test "$BASELINE_BUILD_END" != "null"
```

Prove the baseline at the artifact and runtime boundaries:

```bash
aws lambda get-function --function-name "$FUNCTION_NAME" \
  --query 'Code.ImageUri' --output text | tee "$WORK_DIR/baseline-image-uri.txt"
aws lambda invoke --function-name "$FUNCTION_NAME" \
  --cli-binary-format raw-in-base64-out --payload '{}' \
  "$WORK_DIR/baseline-response.json" >/dev/null
jq -e '.version == "one" and .healthy == true' \
  "$WORK_DIR/baseline-response.json"
export BASELINE_IMAGE_URI="$(cat "$WORK_DIR/baseline-image-uri.txt")"
case "$BASELINE_IMAGE_URI" in
  "$REPOSITORY_URI"@sha256:*) ;;
  *) printf 'Lambda is not pinned to the expected repository digest\n' >&2; exit 1 ;;
esac

export FUNCTION_ARN="$(aws lambda get-function \
  --function-name "$FUNCTION_NAME" \
  --query 'Configuration.FunctionArn' --output text)"
aws ecr get-repository-policy \
  --repository-name "${REPOSITORY_URI##*/}" \
  >"$WORK_DIR/repository-policy.json"
jq --arg function_arn "$FUNCTION_ARN" -e '
  .policyText | fromjson |
  any(.Statement[];
    .Principal.Service == "lambda.amazonaws.com" and
    (.Action | index("ecr:BatchGetImage")) != null and
    (.Action | index("ecr:GetDownloadUrlForLayer")) != null and
    .Condition.ArnLike."aws:SourceArn" == $function_arn
  )' "$WORK_DIR/repository-policy.json"
```

The observed digest links ECR bytes to Lambda configuration. It does not prove
source authorship, reproducibility, vulnerability absence, or that every
request is healthy. The repository-policy observation proves that Lambda's
service principal can retrieve layers for this function ARN; it does not grant
another function or human principal access.

## Failure injection 1: stop at the source gate

Change only `gate.txt`, rebuild the ZIP, upload it, and start one execution.
Predict failure before Docker emits a build step and no change to Lambda.

```bash
printf 'fail\n' >"$WORK_DIR/source/gate.txt"
(cd "$WORK_DIR/source" && zip -q -r "$WORK_DIR/source-gate-fail.zip" .)
aws s3 cp "$WORK_DIR/source-gate-fail.zip" \
  "s3://$SOURCE_BUCKET/source.zip"
export GATE_EXECUTION_ID="$(aws codepipeline start-pipeline-execution \
  --name "$PIPELINE_NAME" --query pipelineExecutionId --output text)"
```

Use the bounded polling loop from the baseline, substituting
`GATE_EXECUTION_ID`. The expected terminal state is `Failed`.

### Diagnose the gate failure

Start from the pipeline symptom. First identify the failed action and external
execution ID; that separates source acquisition from build failure. Then
inspect only that build's status and log metadata.

```bash
aws codepipeline list-action-executions \
  --pipeline-name "$PIPELINE_NAME" \
  --filter "pipelineExecutionId=$GATE_EXECUTION_ID" \
  >"$WORK_DIR/gate-actions.json"
jq -r '.actionExecutionDetails[] |
  [.stageName,.actionName,.status,
   (.output.executionResult.externalExecutionId // ""),
   (.output.executionResult.externalExecutionSummary // "")] | @tsv' \
  "$WORK_DIR/gate-actions.json"

export GATE_BUILD_ID="$(jq -r \
  '.actionExecutionDetails[] |
   select(.actionName=="Build") |
   .output.executionResult.externalExecutionId' \
  "$WORK_DIR/gate-actions.json")"
aws codebuild batch-get-builds --ids "$GATE_BUILD_ID" \
  >"$WORK_DIR/gate-build.json"
jq -r '.builds[0] |
  {buildStatus,currentPhase,phases,
   logGroup:.logs.groupName,logStream:.logs.streamName}' \
  "$WORK_DIR/gate-build.json"

test "$(aws lambda get-function --function-name "$FUNCTION_NAME" \
  --query 'Code.ImageUri' --output text)" = "$BASELINE_IMAGE_URI"
```

Rank at least these hypotheses before inspecting the phase context: S3 source
failure, CodeBuild role denial, source gate rejection, and Docker build
failure. A failed `PRE_BUILD` command containing the gate test discriminates
the intended fault. An unchanged Lambda digest proves no deployment change; it
does not prove that no other principal changed unrelated resources.

Restore `gate.txt` to `pass`, upload it, run the pipeline once, and require
`Succeeded` before introducing the next fault.

## Failure injection 2: fail post-deployment verification

Change only the synthetic behavior. This image is valid and deployable but
reports unhealthy. Predict that CodeBuild reaches `POST_BUILD`, Lambda points
to a new digest, and the `jq` assertion fails.

```bash
python3 - <<'PY' "$WORK_DIR/source/app.py"
from pathlib import Path
import sys
p = Path(sys.argv[1])
p.write_text('def handler(event, context):\n'
             '    return {"version": "two", "healthy": False}\n')
PY
printf 'pass\n' >"$WORK_DIR/source/gate.txt"
(cd "$WORK_DIR/source" && zip -q -r "$WORK_DIR/source-unhealthy.zip" .)
aws s3 cp "$WORK_DIR/source-unhealthy.zip" \
  "s3://$SOURCE_BUCKET/source.zip"
export DEPLOY_EXECUTION_ID="$(aws codepipeline start-pipeline-execution \
  --name "$PIPELINE_NAME" --query pipelineExecutionId --output text)"
```

Use the same action and build inspection commands with
`DEPLOY_EXECUTION_ID`. Confirm that the failed command is the health assertion,
then capture the unhealthy digest and response:

```bash
export UNHEALTHY_IMAGE_URI="$(aws lambda get-function \
  --function-name "$FUNCTION_NAME" --query 'Code.ImageUri' --output text)"
test "$UNHEALTHY_IMAGE_URI" != "$BASELINE_IMAGE_URI"
aws lambda invoke --function-name "$FUNCTION_NAME" \
  --cli-binary-format raw-in-base64-out --payload '{}' \
  "$WORK_DIR/unhealthy-response.json" >/dev/null
jq -e '.version == "two" and .healthy == false' \
  "$WORK_DIR/unhealthy-response.json"
```

This is a deployment failure, not a build failure: image publication and
Lambda update succeeded before the user-visible assertion failed.

## Recover the deployment

The rollback trigger is the failed health assertion. Recover with the smallest
reversible action: select the retained baseline digest. Do not rebuild version
one or retag version two.

```bash
aws lambda update-function-code \
  --function-name "$FUNCTION_NAME" \
  --image-uri "$BASELINE_IMAGE_URI" >/dev/null
aws lambda wait function-updated --function-name "$FUNCTION_NAME"
aws lambda invoke --function-name "$FUNCTION_NAME" \
  --cli-binary-format raw-in-base64-out --payload '{}' \
  "$WORK_DIR/recovery-response.json" >/dev/null
jq -e '.version == "one" and .healthy == true' \
  "$WORK_DIR/recovery-response.json"
test "$(aws lambda get-function --function-name "$FUNCTION_NAME" \
  --query 'Code.ImageUri' --output text)" = "$BASELINE_IMAGE_URI"
```

Record recovery start and verification timestamps. One successful invocation
proves the bounded fixture recovered; it does not establish an availability
SLO. A production path should automate a sustained health decision and account
for aliases, traffic shifting, concurrency, and data compatibility.

## Secrets and audit evidence

The build role retrieves one generated secret. The build never prints or
packages it. Inspect policy scope, then correlate the CloudTrail event to the
secret ARN, baseline build time window, and CodeBuild assumed-role session.
Keep raw event JSON private because it contains account and session identity.

```bash
aws iam simulate-principal-policy \
  --policy-source-arn "$BUILD_ROLE_ARN" \
  --action-names secretsmanager:GetSecretValue \
  --resource-arns "$SECRET_ARN" \
  >"$WORK_DIR/secret-policy-simulation.json"
jq -r '.EvaluationResults[] |
  [.EvalActionName,.EvalDecision] | @tsv' \
  "$WORK_DIR/secret-policy-simulation.json"

aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=GetSecretValue \
  --start-time "$BASELINE_BUILD_START" \
  --end-time "$BASELINE_BUILD_END" \
  --max-results 50 \
  >"$WORK_DIR/secret-audit-raw.json"
jq --arg secret "$SECRET_ARN" --arg role "$BUILD_ROLE_ARN" '
  [.Events[] |
    . as $summary |
    (.CloudTrailEvent | fromjson) as $event |
    select(
      $event.requestParameters.secretId == $secret or
      (([$summary.Resources[]?.ResourceName] | index($secret)) != null)
    ) |
    select(
      $event.userIdentity.sessionContext.sessionIssuer.arn == $role
    ) |
    {
      Time: $summary.EventTime,
      EventId: $summary.EventId,
      EventName: $summary.EventName,
      SessionArn: $event.userIdentity.arn,
      IssuerArn: $event.userIdentity.sessionContext.sessionIssuer.arn
    }
  ]' "$WORK_DIR/secret-audit-raw.json" \
  >"$WORK_DIR/secret-audit-summary.json"
test "$(jq 'length' "$WORK_DIR/secret-audit-summary.json")" -ge 1
```

CloudTrail event history is a Region-scoped, recent management-event view. A
matching event supports the narrower claim that a session issued from this
build role requested this secret during the recorded baseline build. Event
history can be delayed; if no event appears, wait up to five minutes and repeat
only this read. Absence after that bound is missing evidence, not proof of no
access. A match does not prove the caller used the value safely, that log
storage is immutable, or that an organization trail is correctly retained.

## Comparison practice: services not deployed here

Adding CodeDeploy, CodeArtifact, and EC2 Image Builder would expand roles,
agents, targets, storage, and billing without improving this lab's bounded
serverless recovery proof. Review their official models and complete this
comparison table. This is local/static design practice, not hands-on evidence
for those services.

| Service | Appropriate artifact or target | State and identity to inspect | Failure and recovery question |
|---|---|---|---|
| CodeDeploy | EC2/on-premises agent, Lambda, or ECS deployment | application revision, deployment group, deployment and lifecycle event | Which alarm, hook, or deployment state stops traffic and selects rollback? |
| CodeArtifact | versioned package in a domain and repository | package namespace, version, revision, upstream, and repository policy | How is an already-consumed compromised version blocked without pretending it never existed? |
| EC2 Image Builder | AMI or container image pipeline | recipe version, component versions, build/test workflow, output image ID | Which failed test prevents distribution, and how are consumers returned to an approved image? |

The table tests service selection and evidence boundaries. It does not close
the overlay's missing hands-on practice for those products.

## Evidence record

Complete this table with redacted observations. Keep raw records only in the
approved evidence location.

| Claim | Observation to record | Limits of the observation |
|---|---|---|
| Identity and scope were approved | timestamp, role type, Region, prefix, stack resource types | does not prove every attached permission is least privilege |
| Healthy source passed the path | pipeline execution ID, action states, build phase states | one execution does not establish reliability |
| Artifact identity was immutable | ECR `sha256` digest and tag-mutability setting | digest identity does not prove provenance or safety |
| Lambda image retrieval was authorized | repository policy grants two read actions to the Lambda service with this function ARN condition | policy presence does not prove every retrieval or invocation succeeded |
| Deployment used the built bytes | Lambda `Code.ImageUri` equals the ECR digest URI | configuration equality does not prove every invocation ran successfully |
| Source gate prevented deployment | failed pre-build command and unchanged Lambda digest | does not test every policy or approval path |
| Post-deployment check found user-visible failure | new digest, failed health assertion, synthetic unhealthy response | one assertion does not cover production behavior |
| Recovery selected retained bytes | baseline digest restored and healthy response observed | one invocation does not prove sustained recovery |
| Secret access was bounded and recorded | allowed simulation result plus event matching secret ARN, build interval, and build-role session issuer | does not prove secret non-disclosure or durable log retention |

Also retain the initial predictions, ranked hypotheses, correction, timestamps,
CLI versions, template hash, source ZIP hashes, and one production implication.
Explain without notes why build success, deployment success, release health,
and recovery are separate decisions.

## Cleanup

Cleanup is part of the lab. Delete the Lambda function first because CodeBuild
created it outside CloudFormation, then empty versioned S3 buckets and ECR,
delete the stack, and prove the named resources are absent.

```bash
aws lambda delete-function --function-name "$FUNCTION_NAME"

aws s3api list-object-versions --bucket "$SOURCE_BUCKET" --output json |
  jq -r '.Versions[]?,.DeleteMarkers[]? |
    [.Key,.VersionId] | @tsv' |
  while IFS=$'\t' read -r key version; do
    aws s3api delete-object --bucket "$SOURCE_BUCKET" \
      --key "$key" --version-id "$version" >/dev/null
  done
aws s3 rm "s3://$ARTIFACT_BUCKET" --recursive

aws ecr list-images --repository-name "${REPOSITORY_URI##*/}" \
  --query 'imageIds' --output json >"$WORK_DIR/image-ids.json"
if test "$(jq 'length' "$WORK_DIR/image-ids.json")" -gt 0; then
  aws ecr batch-delete-image \
    --repository-name "${REPOSITORY_URI##*/}" \
    --image-ids "file://$WORK_DIR/image-ids.json" >/dev/null
fi

aws cloudformation delete-stack --stack-name "$STACK_NAME"
aws cloudformation wait stack-delete-complete --stack-name "$STACK_NAME"
```

Cleanup proof must all succeed:

```bash
test "$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
  >/dev/null 2>&1; printf '%s' "$?")" != "0"
test "$(aws lambda get-function --function-name "$FUNCTION_NAME" \
  >/dev/null 2>&1; printf '%s' "$?")" != "0"
test "$(aws ecr describe-repositories \
  --repository-names "${REPOSITORY_URI##*/}" \
  >/dev/null 2>&1; printf '%s' "$?")" != "0"
test "$(aws s3api head-bucket --bucket "$SOURCE_BUCKET" \
  >/dev/null 2>&1; printf '%s' "$?")" != "0"
test "$(aws s3api head-bucket --bucket "$ARTIFACT_BUCKET" \
  >/dev/null 2>&1; printf '%s' "$?")" != "0"
test "$(aws secretsmanager describe-secret --secret-id "$SECRET_ARN" \
  >/dev/null 2>&1; printf '%s' "$?")" != "0"
rm -rf "$WORK_DIR"
unset AWS_PROFILE AWS_REGION AWS_PAGER LAB_ID STACK_NAME WORK_DIR \
  SOURCE_BUCKET ARTIFACT_BUCKET REPOSITORY_URI PIPELINE_NAME SECRET_ARN \
  BUILD_ROLE_ARN FUNCTION_NAME BASELINE_BUILD_ID BASELINE_BUILD_START \
  BASELINE_BUILD_END FUNCTION_ARN \
  EXECUTION_ID GATE_EXECUTION_ID GATE_BUILD_ID DEPLOY_EXECUTION_ID \
  BASELINE_IMAGE_URI UNHEALTHY_IMAGE_URI
```

Check the CloudFormation console and billing/resource inventory for the lab
prefix. If deletion fails, do not hide it: retain the failure, notify the
account owner, and continue cleanup before the spend ceiling.

## Completion conditions

The lab is complete only when another reviewer can trace source ZIP to build,
ECR digest, Lambda configuration, gate failure, post-deployment failure,
recovery, secret-access metadata, and cleanup proof. Stop without claiming
completion if any link relies only on an assumed or illustrative result.

## Sources

Checked against official AWS documentation on 2026-08-23:

- [CodePipeline concepts](https://docs.aws.amazon.com/codepipeline/latest/userguide/concepts.html)
- [CodePipeline S3 source action](https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-S3.html)
- [CodeBuild build specification reference](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html)
- [CodeBuild Docker sample and privileged mode](https://docs.aws.amazon.com/codebuild/latest/userguide/sample-docker.html)
- [Amazon ECR tag immutability](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-tag-mutability.html)
- [Amazon ECR image digest deployment for Lambda](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)
- [Lambda container image deployment](https://docs.aws.amazon.com/lambda/latest/dg/configuration-images.html)
- [Secrets Manager use in CodeBuild](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec.env.secrets-manager)
- [CloudTrail event history](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html)
- [CodeDeploy deployment types](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html)
- [CodeArtifact package concepts](https://docs.aws.amazon.com/codeartifact/latest/ug/packages-overview.html)
- [EC2 Image Builder concepts](https://docs.aws.amazon.com/imagebuilder/latest/userguide/concepts.html)
- [Deleting CloudFormation stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-delete-stack.html)
