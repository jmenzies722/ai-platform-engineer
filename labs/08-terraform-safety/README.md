# Lab: Review Terraform Plans and Protect State

Use Terraform's built-in resource to practice initialization, saved-plan review, state inspection, drift-like configuration changes, and recovery boundaries without creating cloud resources.

## Prerequisites

- Terraform 1.5 or newer and Bash
- No cloud credentials
- A private local workstation; state can contain sensitive values

## Safety

Work only in `.work`. The configuration uses `terraform_data`, which requires no provider or remote service. Never hand-edit state, upload it to public systems, or apply a plan you have not reviewed. Do not use `-lock=false`, `-auto-approve`, or state subcommands against shared state.

## Setup and baseline

```bash
mkdir -p .work && cd .work
cat >main.tf <<'HCL'
terraform {
  required_version = ">= 1.5"
}
variable "environment" {
  type    = string
  default = "lab"
}
resource "terraform_data" "contract" {
  input = {
    environment = var.environment
    owner       = "learner"
  }
}
output "contract" {
  value = terraform_data.contract.output
}
HCL
terraform fmt -check
terraform init -input=false
terraform validate
terraform plan -input=false -out=baseline.tfplan
terraform show baseline.tfplan
```

Predict which files are configuration, dependency metadata, saved plan, and state.

## Tasks

1. Inspect `terraform show -json baseline.tfplan` with `jq`; identify actions and before/after values.
2. Apply only the reviewed saved plan with `terraform apply baseline.tfplan`.
3. Run `terraform state list`, `terraform state show terraform_data.contract`, and `terraform state pull >state-backup.json`. Restrict backup permissions with `chmod 600`.
4. Change `owner` to `platform-team`, save a second plan, and explain why a fresh plan is required.
5. Add `sensitive = true` to the output, plan again, and inspect plan/state JSON locally. Explain why CLI redaction is not state encryption.
6. Calculate SHA-256 hashes for configuration, lock file if present, and saved plan.

## Evidence to keep

Keep Terraform version, validation output, plan action summaries, hashes, state resource addresses, and a written approval checklist. Never retain values labeled secret. State backups are temporary evidence and must be deleted during cleanup.

## Failure injection

After creating `baseline.tfplan`, change `main.tf` before applying it. Run `terraform apply baseline.tfplan` only if the plan contains solely `terraform_data`; observe that a saved plan represents earlier configuration. Then create and review a fresh plan to reconcile intent. This demonstrates stale-plan risk without external effects.

For a validation failure, temporarily change `environment` default to `{ invalid = true }` while its type remains string and run `terraform validate`; restore the file afterward.

## Cleanup

```bash
terraform destroy -auto-approve
cd ..
rm -rf .work
```

Confirm no `.tfstate`, plan, or backup remains.

## Rubric

- 2 points: initializes and validates a provider-free configuration
- 3 points: reviews machine-readable and human-readable plan actions
- 2 points: explains saved-plan staleness, locking, and state sensitivity
- 2 points: preserves and then securely removes a temporary backup
- 1 point: destroys local resource state and removes artifacts

## Sources

- [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)
- [Terraform state](https://developer.hashicorp.com/terraform/language/state)
- [Sensitive data in state](https://developer.hashicorp.com/terraform/language/manage-sensitive-data)
