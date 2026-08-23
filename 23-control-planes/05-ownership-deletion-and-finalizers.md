# Ownership, deletion, and finalizers

Deletion is a reconciliation protocol, not the absence of an API record. Ownership metadata and finalizers preserve enough intent to clean up external state safely, survive retries, and make orphan decisions explicit.

## Why it matters

Deleting the control-plane record first can orphan costly or sensitive resources. Blocking forever on cleanup can prevent tenant retirement and API progress. Shared ownership can cause one controller to delete another system's resource.

## How it works

Define ownership separately for API lifecycle, fields, and external objects. An owner reference can request dependent lifecycle behavior inside one resource store. External objects need immutable controller UID and tenant correlation, plus explicit adoption rules.

On delete request, persist a deletion timestamp and retain the resource while finalizers remain. The controller stops normal mutation, observes external identity, requests idempotent cleanup, confirms the required terminal state, records evidence, and removes only its own finalizer. Absence is success only when identity and observation are trustworthy.

Specify propagation and retention. Some dependents delete foreground, some background, and some must be retained or transferred. Backups, snapshots, audit evidence, and legal holds may outlive the resource. Deletion APIs should expose consequence and progress.

Break-glass removal accepts orphan risk; it does not complete cleanup. Require impact analysis, external evidence, authority, audit record, residual owner, and follow-up inventory. Controllers must tolerate finalizer removal without assuming their cleanup ran.

## Vocabulary

- **owner reference:** lifecycle relationship between API resources
- **finalizer:** named cleanup obligation blocking record removal
- **orphan:** external or dependent object left without intended lifecycle owner
- **adoption:** controlled attachment of an existing external object to a resource

## See it yourself

Delete a paper resource, then inject provider denial after the deletion timestamp. Predict API state. It remains terminating with an actionable condition and retry backoff. Force-remove the finalizer and note that API deletion succeeds while the provider object remains. This proves record removal and cleanup are distinct outcomes.

## Where it shows up

A database resource owns an instance but retains snapshots for 30 days under a separate retention owner. Deletion status distinguishes instance cleanup from snapshot retention and records external IDs so inventory can verify both.

## When it breaks

Finalizers are added after side effects, old controller versions no longer understand them, cleanup uses a mutable display name, or controllers remove all finalizers. Cyclic ownership deadlocks. Provider credentials disappear before tenant cleanup. Track terminating age, finalizer owner/version, orphan scans, forced removals, cleanup latency, and deletion failures by reason.

## Practice

**Observe:** draw the lifecycle graph for one resource and its external objects, backups, secrets, and dependents. Assign delete, retain, or transfer semantics.

**Build:** write deletion reconciliation pseudocode with stable identity, finalizer, status, retries, confirmation, and audit evidence.

**Break:** revoke provider credentials, delete a dependent first, and force-remove a finalizer. Write the operator runbook and residual-risk record.

**Say it out loud:** explain why a finalizer is a promise to attempt and verify cleanup, not proof cleanup will always succeed.

## Check yourself

1. When should a dependent be retained rather than cascade-deleted?
2. Why must controllers remove only their own finalizers?
3. Which evidence is required before treating external absence as success?
4. What responsibility remains after break-glass finalizer removal?

## Sources

### REQUIRED

- [Kubernetes finalizers](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/)

### RECOMMENDED

- [Kubernetes garbage collection](https://kubernetes.io/docs/concepts/architecture/garbage-collection/)

### DEEP DIVE

- [Kubernetes API conventions: late initialization and finalizers](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)

## Next

Continue to [API evolution and compatibility](06-api-evolution-and-compatibility.md).
