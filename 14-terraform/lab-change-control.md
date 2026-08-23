# Lab: exercise Terraform change control locally

Use built-in `terraform_data` resources and local state to inspect language evaluation, graph edges, tests, plans, refactoring, drift signals, and recovery. No provider credentials or cloud resources are required.

## Safety and prerequisites

Use Terraform 1.6 or newer in `/tmp/curriculum-terraform`. Never copy the local-state commands to a shared backend without its locking, backup, and approval procedure.

```bash
rm -rf /tmp/curriculum-terraform
mkdir /tmp/curriculum-terraform
cd /tmp/curriculum-terraform
terraform version
```

## Build a graph and contract

Create `main.tf`:

```hcl
terraform {
  required_version = ">= 1.6.0"
}

variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "environment must be dev or prod"
  }
}

resource "terraform_data" "policy" {
  input = {
    environment = var.environment
    retention   = var.environment == "prod" ? 30 : 7
  }
}

resource "terraform_data" "service" {
  input = {
    policy_id = terraform_data.policy.id
    replicas  = var.environment == "prod" ? 3 : 1
  }
}

output "service_contract" {
  value = terraform_data.service.output
}
```

Create `main.tftest.hcl`:

```hcl
run "production_contract" {
  command = plan
  variables {
    environment = "prod"
  }
  assert {
    condition     = terraform_data.policy.input.retention == 30
    error_message = "production retention must be 30"
  }
  assert {
    condition     = terraform_data.service.input.replicas == 3
    error_message = "production needs three replicas"
  }
}
```

Run:

```bash
terraform init
terraform fmt -check
terraform validate
terraform test
terraform graph
```

Predict the dependency edge before reading graph output. Explain why file order does not establish it.

## Save and review the proposed change

```bash
terraform plan -var='environment=prod' -out=approved.tfplan
terraform show -no-color approved.tfplan >approved-plan.txt
sha256sum approved.tfplan approved-plan.txt
terraform apply approved.tfplan
terraform state list
terraform output
```

Record commit or file digest, plan digest, workspace, state lineage and serial from `terraform state pull`, and the exact apply identity. Do not publish state because real provider state can contain secrets.

## Prove tests catch policy failure

Change expected production retention in `main.tf` from 30 to 3. Run format, validate, and tests. Validation should pass because the language is valid; the contract test must fail. Restore 30 before continuing. This distinguishes structural validity from organizational correctness.

## Refactor without replacement

Rename `terraform_data.service` to `terraform_data.workload` and update the output reference. Run a plan and record the proposed delete and create. Then add:

```hcl
moved {
  from = terraform_data.service
  to   = terraform_data.workload
}
```

Run `terraform plan -var='environment=prod'`. Completion requires a plan that preserves object identity. Apply only after reviewing the saved plan.

## Model drift and ownership

Change `retention` to 45 in configuration and run:

```bash
terraform plan -var='environment=prod' -detailed-exitcode
printf 'exit=%s\n' "$?"
terraform plan -var='environment=prod' -refresh-only
```

The normal plan reports desired change; refresh-only should not adopt a configuration edit as remote drift. Classify how the response would differ for an approved emergency remote edit, an unauthorized edit, provider normalization, and a deleted object.

## Rehearse state recovery

Stop all writers. Preserve a state backup:

```bash
terraform state pull >state-backup.json
sha256sum state-backup.json
terraform state list
terraform state rm terraform_data.workload
terraform plan -var='environment=prod'
```

The plan now proposes creation because the mapping is absent even though this built-in resource has no meaningful external object. In real adoption, verify the remote immutable ID and use an import block or supported import workflow. Restore this local exercise with:

```bash
terraform state push state-backup.json
terraform state list
terraform plan -var='environment=prod'
```

If Terraform rejects the push due to serial or lineage, stop. Do not use force flags merely to finish the lab. Inspect active state and recreate the directory instead.

## Workflow design

Produce a pipeline table covering initialization, format, validate, tests, policy, speculative plan, protected saved-plan apply, post-apply verification, drift schedule, and exception handling. For each stage record input, credential, mutable side effect, evidence, timeout, concurrency control, and owner.

## Completion criteria

The lab passes when a reviewer can see the graph edge, a failing behavioral assertion, a hashed and applied saved plan, a refactor with no replacement, a classified drift signal, and a supported state recovery with final expected plan. Document why local state, a built-in resource, and an unsigned plan digest are simplifications rather than production patterns.

## Cleanup

```bash
cd /
rm -rf /tmp/curriculum-terraform
```
