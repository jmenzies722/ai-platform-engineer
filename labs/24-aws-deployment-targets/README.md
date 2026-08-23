# Lab: Deploy One Immutable Workload to Lambda and ECS Fargate

This lab builds one tiny HTTP-shaped workload once, publishes one immutable OCI image to Amazon ECR, and deploys that exact digest to two AWS compute targets. It makes the different release, health, failure, and recovery mechanics of Lambda container images and an ECS Fargate service visible.

## Goal and DOP-C02 task mapping

This lab provides direct guided evidence for the **container** and **serverless** portions of **DOP-C02 Domain 1, task 1.4: Implement deployment strategies for instance, container, and serverless environments**. ECS Fargate is the container target and Lambda is the serverless target. No EC2 instance or instance deployment mechanism is created; the instance-target portion remains comparison-only and unproven, so this lab alone does not fully close task 1.4. It also supplies supporting evidence for task 1.3, artifact management; task 4.2, analysis of logs and metrics; and task 5.3, troubleshooting system and application failures.

Completion proves that the learner can:

- identify one image by its ECR digest and show that Lambda and ECS ran it;
- explain Lambda version/configuration activation versus ECS task-definition and rolling-service deployment;
- cause one bounded failed release on each target, diagnose the target-specific evidence, and restore the known-good configuration;
- distinguish deployment existence, release health, and user-visible recovery.

This does not cover EC2, EKS, API Gateway traffic shifting, production load, multi-account promotion, or a complete CI/CD system. Continue with [AWS compute, storage, and managed data](../../12-aws/03-compute-storage-data.md), [safe changes and recovery](../../13-devops/03-safe-change.md), and [artifacts, registries, and promotion](../../13-devops/04-artifacts-and-promotion.md).

## Before you start

### Authorization and identity assumptions

**Use only an explicitly authorized disposable AWS sandbox. Never run this lab in production, a shared account, or an account containing customer data.** The operator is a federated human or assumed role using temporary credentials. Root credentials and long-lived access keys are out of scope.

The operator principal needs narrowly scoped access to:

- call `sts:GetCallerIdentity`;
- create, describe, configure, and force-delete the one lab ECR repository; call `ecr:GetAuthorizationToken`; upload image layers and the image manifest; call `ecr:BatchGetImage` and `ecr:GetDownloadUrlForLayer`; and set and read the repository policy;
- create, inspect, update, invoke, and delete the one Lambda function;
- create, inspect, update, and delete the ECS cluster and service; list and describe tasks; and register and deregister only this lab's task-definition family;
- describe the default VPC, subnets, network interfaces, and the lab security group; create, authorize ingress on, and delete only that security group;
- create, set one-day retention on, read, and delete only the two named CloudWatch Logs groups;
- create and inspect the two uniquely named lab roles, attach and detach only the two named AWS-managed policies, pass each role only to its matching service, and delete only those roles.

This lab does not support supplied or precreated roles. The generated names must be absent before creation, which makes ownership unambiguous and keeps cleanup from mutating an administrator-owned identity. Organization policies, permissions boundaries, ECR policy, and KMS policy can still deny an identity-policy allow; do not broaden a denied principal during the exercise.

Required local tools are AWS CLI v2, Docker with Buildx, `curl`, `jq`, and a POSIX shell with `timeout`. Docker must be able to build `linux/amd64` images. Use one terminal for the lab so its shell variables remain available.

### Time, cost, and resource bounds

- Expected time: 75 to 120 minutes.
- Hard elapsed-time limit: 2 hours after the first AWS resource is created.
- Cost ceiling: **USD 2.00**, after checking current prices in the selected Region.
- Maximum resources: one image under 100 MB in one ECR repository, one Lambda function with 128 MB memory, one ECS cluster, one Fargate service with one `0.25 vCPU/0.5 GB` task, one public IPv4 address while the task runs, one security group, two IAM roles, and two log groups retained for one day.
- Maximum test load: 20 Lambda invocations and 20 HTTP requests. No load test, NAT gateway, load balancer, custom domain, persistent volume, or database is created.

Fargate runtime, public IPv4 time, ECR storage, Lambda requests/duration, and log ingestion are the relevant billing dimensions. Prices differ by Region and date; consult the [AWS Fargate pricing page](https://aws.amazon.com/fargate/pricing/), [AWS Lambda pricing page](https://aws.amazon.com/lambda/pricing/), and [Amazon ECR pricing page](https://aws.amazon.com/ecr/pricing/) before starting.

### Stop conditions

Stop before mutation, preserve the evidence already collected, and clean up if:

- `get-caller-identity` shows an unexpected account or principal, the Region is prohibited, or sandbox authorization is uncertain;
- the default VPC is absent, Docker cannot build `linux/amd64`, required permissions are denied, or a command would require opening access beyond the single client `/32`;
- an image exceeds 100 MB, desired ECS task count exceeds one, the service does not stabilize within 12 minutes, or total elapsed time reaches 2 hours;
- estimated or observed spend can exceed USD 2.00;
- credentials, tokens, account-sensitive policy documents, or non-synthetic data appear in output;
- rollback does not begin as expected or cleanup cannot remove a billable resource.

Do not repeatedly retry a failing deployment. One baseline release, one failed release per target, and one recovery per target are the lab boundary.

### Prediction

Before running commands, write down:

1. where each target stores its desired artifact and configuration identity;
2. what symptom a nonexistent Python handler produces in Lambda;
3. what ECS does when a replacement task exits before becoming stable;
4. which evidence will prove that recovery used the original image digest rather than a rebuild.

## Static and local design path

Without an AWS account, complete the prediction, target comparison, identity and permission design, failure hypotheses, evidence table, and cleanup review. You can also build and run the ECS mode locally:

```bash
rm -rf /tmp/dop-c02-targets-local
mkdir -p /tmp/dop-c02-targets-local
cd /tmp/dop-c02-targets-local

cat > app.py <<'PY'
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

WORKLOAD = "dop-c02-targets"
RELEASE = os.environ.get("RELEASE_ID", "v1")

def document():
    return {"workload": WORKLOAD, "release": RELEASE, "artifact_contract": "oci-v1"}

def handler(event, context):
    return {"statusCode": 200, "headers": {"content-type": "application/json"},
            "body": json.dumps(document(), sort_keys=True)}

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps(document(), sort_keys=True).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, fmt, *args):
        print(fmt % args, flush=True)

if __name__ == "__main__":
    if "--self-test" in sys.argv:
        assert document()["workload"] == WORKLOAD
        print(json.dumps(document(), sort_keys=True))
    else:
        HTTPServer(("0.0.0.0", 8080), RequestHandler).serve_forever()
PY

cat > Dockerfile <<'DOCKER'
FROM public.ecr.aws/lambda/python:3.12
COPY app.py ${LAMBDA_TASK_ROOT}/app.py
CMD ["app.handler"]
DOCKER

docker buildx build --platform linux/amd64 --load -t dop-c02-targets:local .
docker image inspect dop-c02-targets:local --format '{{json .RepoDigests}} {{.Id}}'
docker run --rm --entrypoint python dop-c02-targets:local app.py --self-test
```

The local image identity and self-test prove local bytes and the shared workload contract. They do **not** prove ECR digest resolution, IAM authorization, Lambda Runtime API behavior, ECS scheduling, Fargate networking, service rollback, CloudWatch evidence, or AWS cleanup. Account-backed claims require the AWS path below.

## Establish the AWS boundary and workspace

Run in a new shell directory. The commands generate unique names; they contain no reusable credentials.

```bash
set -euo pipefail
export AWS_PAGER=""
export AWS_REGION="${AWS_REGION:-us-east-1}"

LAB_ID="dop-c02-targets-$(date -u +%Y%m%d%H%M%S)"
WORK_DIR="/tmp/$LAB_ID"
mkdir -p "$WORK_DIR/evidence"
cd "$WORK_DIR"

aws --version | tee evidence/aws-cli-version.txt
docker version --format '{{.Server.Version}}' | tee evidence/docker-version.txt
aws sts get-caller-identity | tee evidence/caller.json

ACCOUNT_ID="$(jq -r .Account evidence/caller.json)"
PRINCIPAL_ARN="$(jq -r .Arn evidence/caller.json)"
printf 'account=%s\nprincipal=%s\nregion=%s\nlab=%s\n' \
  "$ACCOUNT_ID" "$PRINCIPAL_ARN" "$AWS_REGION" "$LAB_ID" | tee evidence/scope.txt
```

Stop unless every value matches the approved sandbox. Record the credential source and expected session expiry without recording credential material. Record the authorization ticket or owner in your private completion record.

Set a UTC deadline exactly two hours from now and check it before every deployment:

```bash
date -u +%s | awk '{print "started_epoch=" $1 "\nstop_epoch=" $1+7200}' \
  | tee evidence/time-bound.txt
```

## Build once and publish by digest

Create the same files used by the local path:

```bash
cat > app.py <<'PY'
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

WORKLOAD = "dop-c02-targets"
RELEASE = os.environ.get("RELEASE_ID", "v1")

def document():
    return {"workload": WORKLOAD, "release": RELEASE, "artifact_contract": "oci-v1"}

def handler(event, context):
    return {"statusCode": 200, "headers": {"content-type": "application/json"},
            "body": json.dumps(document(), sort_keys=True)}

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps(document(), sort_keys=True).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, fmt, *args):
        print(fmt % args, flush=True)

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), RequestHandler).serve_forever()
PY

cat > Dockerfile <<'DOCKER'
FROM public.ecr.aws/lambda/python:3.12
COPY app.py ${LAMBDA_TASK_ROOT}/app.py
CMD ["app.handler"]
DOCKER

REPOSITORY="$LAB_ID"
FUNCTION_NAME="$LAB_ID-lambda"
aws ecr create-repository \
  --repository-name "$REPOSITORY" \
  --image-tag-mutability IMMUTABLE \
  --image-scanning-configuration scanOnPush=true \
  | tee evidence/ecr-create.json

cat > lambda-ecr-policy.json <<JSON
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "LambdaECRImageRetrievalPolicy",
    "Effect": "Allow",
    "Principal": {"Service": "lambda.amazonaws.com"},
    "Action": ["ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer"],
    "Condition": {
      "ArnLike": {
        "aws:SourceArn": "arn:aws:lambda:$AWS_REGION:$ACCOUNT_ID:function:$FUNCTION_NAME"
      }
    }
  }]
}
JSON
aws ecr set-repository-policy \
  --repository-name "$REPOSITORY" \
  --policy-text file://lambda-ecr-policy.json \
  | tee evidence/ecr-lambda-policy.json
aws ecr get-repository-policy --repository-name "$REPOSITORY" \
  | tee evidence/ecr-lambda-policy-readback.json

REGISTRY="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
aws ecr get-login-password |
  docker login --username AWS --password-stdin "$REGISTRY"

docker buildx build --platform linux/amd64 --load \
  -t "$REGISTRY/$REPOSITORY:v1" .
docker push "$REGISTRY/$REPOSITORY:v1" | tee evidence/ecr-push.txt

IMAGE_DIGEST="$(aws ecr describe-images \
  --repository-name "$REPOSITORY" \
  --image-ids imageTag=v1 \
  --query 'imageDetails[0].imageDigest' --output text)"
IMAGE_URI="$REGISTRY/$REPOSITORY@$IMAGE_DIGEST"
IMAGE_BYTES="$(aws ecr describe-images --repository-name "$REPOSITORY" \
  --image-ids imageDigest="$IMAGE_DIGEST" \
  --query 'imageDetails[0].imageSizeInBytes' --output text)"
printf 'image_uri=%s\nimage_bytes=%s\n' "$IMAGE_URI" "$IMAGE_BYTES" \
  | tee evidence/artifact.txt
test "$IMAGE_BYTES" -lt 104857600
```

The digest is the shared artifact identity. The `v1` tag is only a human reference and cannot be moved because the repository is immutable. Scanning is useful evidence about known findings; it does not prove the image is safe or behaves correctly.

## Create bounded service identities

Create separate trust policies and roles so Lambda cannot assume the ECS role and ECS cannot assume the Lambda role:

```bash
cat > lambda-trust.json <<'JSON'
{"Version":"2012-10-17","Statement":[{"Effect":"Allow",
"Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}
JSON

cat > ecs-trust.json <<'JSON'
{"Version":"2012-10-17","Statement":[{"Effect":"Allow",
"Principal":{"Service":"ecs-tasks.amazonaws.com"},"Action":"sts:AssumeRole"}]}
JSON

LAMBDA_ROLE="$LAB_ID-lambda"
ECS_EXEC_ROLE="$LAB_ID-ecs-exec"
if aws iam get-role --role-name "$LAMBDA_ROLE" >/dev/null 2>&1 ||
   aws iam get-role --role-name "$ECS_EXEC_ROLE" >/dev/null 2>&1; then
  printf 'Refusing to reuse an existing IAM role.\n' >&2
  exit 1
fi
aws iam create-role --role-name "$LAMBDA_ROLE" \
  --assume-role-policy-document file://lambda-trust.json \
  | tee evidence/lambda-role.json
aws iam attach-role-policy --role-name "$LAMBDA_ROLE" \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam create-role --role-name "$ECS_EXEC_ROLE" \
  --assume-role-policy-document file://ecs-trust.json \
  | tee evidence/ecs-role.json
aws iam attach-role-policy --role-name "$ECS_EXEC_ROLE" \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

LAMBDA_ROLE_ARN="arn:aws:iam::$ACCOUNT_ID:role/$LAMBDA_ROLE"
ECS_EXEC_ROLE_ARN="arn:aws:iam::$ACCOUNT_ID:role/$ECS_EXEC_ROLE"
sleep 10
```

The Lambda execution role permits the function to create log streams and write log events; the Lambda service retrieves the image under the ECR repository policy, not under the function execution role. The ECS task execution role permits the ECS agent to authenticate to ECR, pull image layers, and write container logs. No ECS task role is configured, so application code in either target receives no AWS data-plane permission from this lab.

## Target 1: Lambda container image

### Healthy baseline

```bash
LAMBDA_LOG_GROUP="/aws/lambda/$FUNCTION_NAME"
aws logs create-log-group --log-group-name "$LAMBDA_LOG_GROUP"
aws logs put-retention-policy \
  --log-group-name "$LAMBDA_LOG_GROUP" --retention-in-days 1

aws lambda create-function \
  --function-name "$FUNCTION_NAME" \
  --package-type Image \
  --code ImageUri="$IMAGE_URI" \
  --role "$LAMBDA_ROLE_ARN" \
  --memory-size 128 \
  --timeout 5 \
  --environment 'Variables={RELEASE_ID=v1}' \
  | tee evidence/lambda-create.json

aws lambda wait function-active-v2 --function-name "$FUNCTION_NAME"
aws lambda invoke --function-name "$FUNCTION_NAME" \
  --cli-binary-format raw-in-base64-out \
  --payload '{}' evidence/lambda-baseline-body.json \
  | tee evidence/lambda-baseline-meta.json
jq -e '.statusCode == 200 and
  (.body | fromjson | .workload == "dop-c02-targets")' \
  evidence/lambda-baseline-body.json

aws lambda get-function --function-name "$FUNCTION_NAME" \
  | tee evidence/lambda-get-function.json
test "$(jq -r .Code.ImageUri evidence/lambda-get-function.json)" = "$IMAGE_URI"
```

Expected behavior is a `200` response whose body names the workload and release. `get-function` proves the desired ECR digest; the successful invocation proves the handler contract for one synthetic request, not availability under load.

### Failed Lambda release

Predict the invocation symptom, then alter only the image command. The artifact remains unchanged:

```bash
LAMBDA_FAILURE_START="$(date -u +%s)"
aws lambda update-function-configuration \
  --function-name "$FUNCTION_NAME" \
  --image-config '{"Command":["app.missing"]}' \
  | tee evidence/lambda-failed-release.json
aws lambda wait function-updated-v2 --function-name "$FUNCTION_NAME"

aws lambda invoke --function-name "$FUNCTION_NAME" \
  --cli-binary-format raw-in-base64-out \
  --payload '{}' evidence/lambda-failure-body.json \
  | tee evidence/lambda-failure-meta.json
jq -e '.FunctionError == "Unhandled"' evidence/lambda-failure-meta.json
aws logs tail "/aws/lambda/$FUNCTION_NAME" --since 5m \
  | tee evidence/lambda-failure-logs.txt
```

Start with the user-visible `FunctionError`. Rank at least these hypotheses: wrong handler command, incompatible image architecture, denied ECR pull, and application exception. The function is `Active`, the update completed, and the log reports handler import failure; together these discriminate bad runtime configuration from scheduling or image-pull failure. Do not infer root cause from `Active` alone.

### Lambda recovery

Restore the known-good command; do not rebuild or repush:

```bash
aws lambda update-function-configuration \
  --function-name "$FUNCTION_NAME" \
  --image-config '{"Command":["app.handler"]}' \
  | tee evidence/lambda-recovery-update.json
aws lambda wait function-updated-v2 --function-name "$FUNCTION_NAME"
aws lambda invoke --function-name "$FUNCTION_NAME" \
  --cli-binary-format raw-in-base64-out \
  --payload '{}' evidence/lambda-recovery-body.json \
  | tee evidence/lambda-recovery-meta.json
jq -e '.statusCode == 200 and
  (.body | fromjson | .release == "v1")' evidence/lambda-recovery-body.json
LAMBDA_RECOVERY_END="$(date -u +%s)"
printf 'lambda_recovery_seconds=%s\n' \
  "$((LAMBDA_RECOVERY_END-LAMBDA_FAILURE_START))" \
  | tee evidence/lambda-recovery-time.txt
test "$(aws lambda get-function --function-name "$FUNCTION_NAME" \
  --query 'Code.ImageUri' --output text)" = "$IMAGE_URI"
```

This is configuration rollback to a compatible handler using retained immutable bytes. It would not repair irreversible external side effects or an incompatible data migration.

## Target 2: ECS Fargate service

### Network and task definition

Use the default VPC to avoid NAT gateway cost. The service has one task with a public IP, and ingress is restricted to the operator's current public IPv4 `/32`.

```bash
VPC_ID="$(aws ec2 describe-vpcs \
  --filters Name=isDefault,Values=true \
  --query 'Vpcs[0].VpcId' --output text)"
test "$VPC_ID" != "None"
SUBNET_ID="$(aws ec2 describe-subnets \
  --filters Name=vpc-id,Values="$VPC_ID" \
  --query 'Subnets[?MapPublicIpOnLaunch==`true`].SubnetId | [0]' \
  --output text)"
test "$SUBNET_ID" != "None"
CLIENT_IP="$(curl -4 -fsS https://checkip.amazonaws.com | tr -d '[:space:]')"
CLIENT_CIDR="$CLIENT_IP/32"

SG_ID="$(aws ec2 create-security-group \
  --group-name "$LAB_ID-ecs" \
  --description "Temporary DOP-C02 target lab" \
  --vpc-id "$VPC_ID" \
  --query GroupId --output text)"
aws ec2 authorize-security-group-ingress \
  --group-id "$SG_ID" --protocol tcp --port 8080 --cidr "$CLIENT_CIDR"
printf 'vpc=%s\nsubnet=%s\nsecurity_group=%s\nclient_cidr=%s\n' \
  "$VPC_ID" "$SUBNET_ID" "$SG_ID" "$CLIENT_CIDR" \
  | tee evidence/ecs-network.txt

CLUSTER="$LAB_ID"
SERVICE="$LAB_ID-service"
TASK_FAMILY="$LAB_ID-task"
LOG_GROUP="/aws/ecs/$LAB_ID"
aws logs create-log-group --log-group-name "$LOG_GROUP"
aws logs put-retention-policy --log-group-name "$LOG_GROUP" --retention-in-days 1
aws ecs create-cluster --cluster-name "$CLUSTER" | tee evidence/ecs-cluster.json

jq -n \
  --arg family "$TASK_FAMILY" \
  --arg role "$ECS_EXEC_ROLE_ARN" \
  --arg image "$IMAGE_URI" \
  --arg region "$AWS_REGION" \
  --arg logs "$LOG_GROUP" \
  '{
    family:$family,
    networkMode:"awsvpc",
    requiresCompatibilities:["FARGATE"],
    cpu:"256",
    memory:"512",
    executionRoleArn:$role,
    containerDefinitions:[{
      name:"app",
      image:$image,
      essential:true,
      entryPoint:["python"],
      command:["app.py"],
      environment:[{name:"RELEASE_ID",value:"v1"}],
      portMappings:[{containerPort:8080,protocol:"tcp"}],
      logConfiguration:{
        logDriver:"awslogs",
        options:{
          "awslogs-group":$logs,
          "awslogs-region":$region,
          "awslogs-stream-prefix":"app"
        }
      }
    }]
  }' > task-good.json

GOOD_TASK_DEF="$(aws ecs register-task-definition \
  --cli-input-json file://task-good.json \
  --query 'taskDefinition.taskDefinitionArn' --output text)"
printf 'good_task_definition=%s\n' "$GOOD_TASK_DEF" \
  | tee evidence/ecs-good-task-definition.txt
```

The ECS task definition adds target-specific entry point, resource, network, and logging configuration around the same image digest.

### Healthy ECS baseline

```bash
NETWORK_CONFIG="awsvpcConfiguration={subnets=[$SUBNET_ID],securityGroups=[$SG_ID],assignPublicIp=ENABLED}"
aws ecs create-service \
  --cluster "$CLUSTER" \
  --service-name "$SERVICE" \
  --task-definition "$GOOD_TASK_DEF" \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "$NETWORK_CONFIG" \
  --deployment-configuration \
    'deploymentCircuitBreaker={enable=true,rollback=true},maximumPercent=200,minimumHealthyPercent=100' \
  | tee evidence/ecs-service-create.json

timeout 12m aws ecs wait services-stable \
  --cluster "$CLUSTER" --services "$SERVICE"
TASK_ARN="$(aws ecs list-tasks --cluster "$CLUSTER" \
  --service-name "$SERVICE" --desired-status RUNNING \
  --query 'taskArns[0]' --output text)"
ENI_ID="$(aws ecs describe-tasks --cluster "$CLUSTER" --tasks "$TASK_ARN" \
  --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value | [0]' \
  --output text)"
TASK_IP="$(aws ec2 describe-network-interfaces \
  --network-interface-ids "$ENI_ID" \
  --query 'NetworkInterfaces[0].Association.PublicIp' --output text)"
curl --fail --max-time 5 "http://$TASK_IP:8080/" \
  | tee evidence/ecs-baseline-body.json
jq -e '.workload == "dop-c02-targets" and .release == "v1"' \
  evidence/ecs-baseline-body.json

aws ecs describe-tasks --cluster "$CLUSTER" --tasks "$TASK_ARN" \
  | tee evidence/ecs-baseline-task.json
test "$(jq -r '.tasks[0].containers[0].imageDigest' \
  evidence/ecs-baseline-task.json)" = "$IMAGE_DIGEST"
```

The task's reported `imageDigest` joins runtime evidence to the same ECR artifact used by Lambda. One request does not establish service capacity or availability.

### Failed ECS release

Create a new task-definition revision that refers to the same digest but overrides the Python script with a nonexistent file:

```bash
jq '.containerDefinitions[0].command=["missing.py"]' \
  task-good.json > task-bad.json
BAD_TASK_DEF="$(aws ecs register-task-definition \
  --cli-input-json file://task-bad.json \
  --query 'taskDefinition.taskDefinitionArn' --output text)"

ECS_FAILURE_START="$(date -u +%s)"
aws ecs update-service \
  --cluster "$CLUSTER" --service "$SERVICE" \
  --task-definition "$BAD_TASK_DEF" \
  | tee evidence/ecs-failed-release.json
```

Watch bounded service and task evidence instead of retrying:

```bash
for attempt in $(seq 1 24); do
  aws ecs describe-services --cluster "$CLUSTER" --services "$SERVICE" \
    --query 'services[0].{deployments:deployments,events:events[0:8]}' \
    > evidence/ecs-deployment-latest.json
  jq . evidence/ecs-deployment-latest.json
  PRIMARY_DEF="$(jq -r '.deployments[] |
    select(.status=="PRIMARY") | .taskDefinition' \
    evidence/ecs-deployment-latest.json)"
  [ "$PRIMARY_DEF" = "$GOOD_TASK_DEF" ] && break
  sleep 15
done

aws ecs list-tasks --cluster "$CLUSTER" --family "$TASK_FAMILY" \
  --desired-status STOPPED --max-results 10 \
  | tee evidence/ecs-stopped-task-arns.json
STOPPED_TASKS="$(jq -r '.taskArns | join(" ")' \
  evidence/ecs-stopped-task-arns.json)"
if [ -n "$STOPPED_TASKS" ]; then
  aws ecs describe-tasks --cluster "$CLUSTER" --tasks $STOPPED_TASKS \
    | tee evidence/ecs-stopped-tasks.json
fi
aws logs tail "$LOG_GROUP" --since 10m | tee evidence/ecs-failure-logs.txt
```

The expected symptom is replacement tasks stopping with a nonzero exit while the known-good task continues serving. Rank wrong command, image-pull denial, insufficient Fargate capacity, and failed application health as hypotheses. Container reason, stop code, exit code, service events, and logs separate them. If automatic rollback has not made the good revision primary after six minutes, stop the experiment and explicitly recover:

```bash
if [ "$PRIMARY_DEF" != "$GOOD_TASK_DEF" ]; then
  aws ecs update-service --cluster "$CLUSTER" --service "$SERVICE" \
    --task-definition "$GOOD_TASK_DEF" \
    | tee evidence/ecs-explicit-recovery.json
fi
timeout 12m aws ecs wait services-stable \
  --cluster "$CLUSTER" --services "$SERVICE"
```

### ECS recovery proof

Resolve the current task rather than reusing the old IP:

```bash
RECOVERED_TASK="$(aws ecs list-tasks --cluster "$CLUSTER" \
  --service-name "$SERVICE" --desired-status RUNNING \
  --query 'taskArns[0]' --output text)"
RECOVERED_ENI="$(aws ecs describe-tasks --cluster "$CLUSTER" \
  --tasks "$RECOVERED_TASK" \
  --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value | [0]' \
  --output text)"
RECOVERED_IP="$(aws ec2 describe-network-interfaces \
  --network-interface-ids "$RECOVERED_ENI" \
  --query 'NetworkInterfaces[0].Association.PublicIp' --output text)"
curl --fail --max-time 5 "http://$RECOVERED_IP:8080/" \
  | tee evidence/ecs-recovery-body.json
jq -e '.workload == "dop-c02-targets" and .release == "v1"' \
  evidence/ecs-recovery-body.json

aws ecs describe-tasks --cluster "$CLUSTER" --tasks "$RECOVERED_TASK" \
  | tee evidence/ecs-recovery-task.json
test "$(jq -r '.tasks[0].taskDefinitionArn' \
  evidence/ecs-recovery-task.json)" = "$GOOD_TASK_DEF"
test "$(jq -r '.tasks[0].containers[0].imageDigest' \
  evidence/ecs-recovery-task.json)" = "$IMAGE_DIGEST"
ECS_RECOVERY_END="$(date -u +%s)"
printf 'ecs_recovery_seconds=%s\n' \
  "$((ECS_RECOVERY_END-ECS_FAILURE_START))" \
  | tee evidence/ecs-recovery-time.txt
```

Recovery requires all four facts: desired service revision is good, one good task is running, its runtime digest matches ECR, and the user-visible request succeeds.

## Compare the target mechanics

Complete this comparison from observed evidence:

| Question | Lambda container image | ECS Fargate service |
|---|---|---|
| Immutable deployment input | ECR URI with digest | Task definition whose container image is the same digest |
| Configuration identity | Function configuration and image command | Task-definition revision, service deployment, network configuration |
| Scheduling unit | Invocation environment managed by Lambda | Explicit task with CPU, memory, ENI, and desired count |
| Healthy baseline evidence | Successful invocation plus `get-function` | Successful HTTP request plus running task and runtime `imageDigest` |
| Failed-release signal | Invocation `FunctionError` and function logs | Stopped replacement task, exit code, service event, deployment state |
| Exposure control used here | Function configuration becomes active after update | Rolling service deployment keeps one old task while replacing it |
| Recovery action | Restore handler command | Circuit-breaker rollback or explicit service update to good revision |
| State caveat | Stateless handler; external side effects need separate recovery | Stateless task; task replacement does not restore durable data |

Explain why the digest alone does not identify environment variables, command overrides, IAM roles, network policy, desired count, or traffic exposure.

## Evidence record

Retain redacted machine-readable files, not credentials or Docker login data:

| Claim | Evidence | What it does not prove |
|---|---|---|
| Correct sandbox boundary | `caller.json`, `scope.txt`, authorization record | That every downstream action is authorized |
| One artifact was built and retained | `artifact.txt`, ECR response, local build output | Reproducible build, trusted provenance, or absence of vulnerabilities |
| Lambda ran that artifact | `lambda-get-function.json`, baseline body and metadata | Load behavior or all invocation paths |
| Lambda failed for the predicted reason | failure metadata and correlated logs | That every handler error has the same cause |
| Lambda recovered without rebuild | recovery body, duration, final image URI | Recovery from incompatible data changes |
| ECS ran that artifact | baseline task `imageDigest`, task definition, HTTP body | Multi-AZ availability or load-balancer health |
| ECS replacement failed for the predicted reason | stopped-task details, exit code, logs, service events | Every possible ECS placement failure |
| ECS recovered to the known-good revision | recovery task definition, digest, body, duration | Production rollout safety at larger desired counts |

Record prediction, observation, interpretation, and decision separately. Preserve UTC timestamps and AWS request IDs where present. Redact account IDs only in copies intended for public sharing while retaining a stable correlation token.

## Clean up and prove removal

Run cleanup even after a failed step. First remove the billable runtime and image:

```bash
aws ecs update-service --cluster "$CLUSTER" --service "$SERVICE" \
  --desired-count 0 >/dev/null 2>&1 || true
aws ecs delete-service --cluster "$CLUSTER" --service "$SERVICE" \
  --force >/dev/null 2>&1 || true
timeout 12m aws ecs wait services-inactive \
  --cluster "$CLUSTER" --services "$SERVICE" || true

aws ecs list-task-definitions --family-prefix "$TASK_FAMILY" \
  --query 'taskDefinitionArns[]' --output text |
  xargs -r -n1 aws ecs deregister-task-definition \
    --task-definition >/dev/null
aws ecs delete-cluster --cluster "$CLUSTER" >/dev/null 2>&1 || true
aws lambda delete-function --function-name "$FUNCTION_NAME" \
  >/dev/null 2>&1 || true
aws ecr delete-repository --repository-name "$REPOSITORY" --force \
  >/dev/null 2>&1 || true
```

Then remove network, logs, and identities. Both IAM names passed the absence check before this lab created them; if that check was not observed, stop instead of running the IAM deletion commands:

```bash
aws ec2 delete-security-group --group-id "$SG_ID" \
  >/dev/null 2>&1 || true
aws logs delete-log-group --log-group-name "$LOG_GROUP" \
  >/dev/null 2>&1 || true
aws logs delete-log-group --log-group-name "$LAMBDA_LOG_GROUP" \
  >/dev/null 2>&1 || true

aws iam detach-role-policy --role-name "$LAMBDA_ROLE" \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole \
  >/dev/null 2>&1 || true
aws iam delete-role --role-name "$LAMBDA_ROLE" >/dev/null 2>&1 || true
aws iam detach-role-policy --role-name "$ECS_EXEC_ROLE" \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy \
  >/dev/null 2>&1 || true
aws iam delete-role --role-name "$ECS_EXEC_ROLE" >/dev/null 2>&1 || true
docker logout "$REGISTRY" >/dev/null 2>&1 || true
```

Prove that billable resources and access paths are gone:

```bash
test "$(aws ecs list-tasks --cluster "$CLUSTER" \
  --desired-status RUNNING --query 'length(taskArns)' \
  --output text 2>/dev/null || printf 0)" = "0"
test "$(aws lambda get-function --function-name "$FUNCTION_NAME" \
  --query 'Configuration.FunctionArn' --output text 2>/dev/null \
  || printf absent)" = "absent"
test "$(aws ecr describe-repositories --repository-names "$REPOSITORY" \
  --query 'repositories[0].repositoryArn' --output text 2>/dev/null \
  || printf absent)" = "absent"
test "$(aws ec2 describe-security-groups --group-ids "$SG_ID" \
  --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null \
  || printf absent)" = "absent"
test "$(aws logs describe-log-groups \
  --log-group-name-prefix "$LOG_GROUP" \
  --query 'length(logGroups)' --output text)" = "0"
test "$(aws logs describe-log-groups \
  --log-group-name-prefix "$LAMBDA_LOG_GROUP" \
  --query 'length(logGroups)' --output text)" = "0"
test "$(aws iam get-role --role-name "$LAMBDA_ROLE" \
  --query 'Role.Arn' --output text 2>/dev/null \
  || printf absent)" = "absent"
test "$(aws iam get-role --role-name "$ECS_EXEC_ROLE" \
  --query 'Role.Arn' --output text 2>/dev/null \
  || printf absent)" = "absent"
printf 'cleanup_verified_at=%s\n' "$(date -u +%FT%TZ)" \
  | tee evidence/cleanup-proof.txt
```

If any assertion fails, stop other work and remove the named resource in the AWS console or with the approved sandbox administrator. Keep only redacted evidence locally, then remove the working images and directory when the review is complete.

## What to keep and explain back

Keep the prediction, shared digest, configuration identities, baseline outputs, failed hypotheses, discriminating evidence, recovery durations, target comparison, and cleanup proof. Explain without notes:

1. why one image can be healthy on one target and unhealthy on another;
2. why Lambda `Active` and ECS `RUNNING` are weaker than user-visible assertions;
3. how immutable artifact identity enabled recovery but did not make configuration immutable;
4. which production controls are missing, including staged traffic, alarms, signed provenance, deployment approvals, multiple tasks across Availability Zones, and durable-state recovery.

## Sources

Product behavior and command shape were reviewed against the linked AWS documentation on 2026-08-23 and should be rechecked when AWS CLI, Lambda, ECS, Fargate, or ECR behavior changes.

- [Deploy Python Lambda functions with container images](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html)
- [Lambda ECR repository permissions](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html#images-permissions)
- [Lambda function states](https://docs.aws.amazon.com/lambda/latest/dg/functions-states.html)
- [Amazon ECS task definitions](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)
- [Amazon ECS deployment circuit breaker](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-circuit-breaker.html)
- [Fargate task networking](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-networking.html)
- [Amazon ECR image tag mutability](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-tag-mutability.html)
- [Amazon ECS task execution IAM role](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html)
- [AWS Lambda execution role](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html)
