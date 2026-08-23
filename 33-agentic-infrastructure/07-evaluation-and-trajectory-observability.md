# Human approval, escalation, and kill-switch operation

Human control is an operational protocol: consequential effects pause on an exact proposal, uncertainty escalates to an accountable owner, and independent kill switches bound new harm while in-flight effects are reconciled.

## Why it matters

An approval button is not safety if the reviewer cannot understand the consequence, the payload can change afterward, or denial merely causes the agent to ask again. Cancellation is incomplete if remote executors continue committing effects.

## How it works

Policy classifies actions as automatic, approval-required, forbidden, or escalation-required. Before approval, the runtime resolves the target, canonicalizes arguments, computes the effect and reversibility, evaluates current policy, and creates an expiring digest over run, principal, tool, target, normalized payload, policy version, and precondition version. The reviewer sees a human-readable diff or consequence, affected tenant, data exposure, cost bound, alternatives, rollback limits, and expiration. Commit re-resolves the target and verifies the digest; any changed field invalidates approval.

Denial is terminal for that exact proposal unless a changed fact or explicit appeal policy permits escalation. Repeated requests do not accumulate consent. Escalation routes by consequence and authority, not model preference, and has a deadline plus safe default. Unavailable approvers leave the run paused or safely aborted; emergency procedures cannot silently convert timeout into approval. Separation of duties may require requester and approver to differ.

Controls form a scope ladder: pause one run, revoke one capability, quarantine one tenant, disable one tool or model revision, stop all new consequential effects, then stop all admissions. A kill switch uses an authenticated path independent of the planner and normal policy dependency. Executors consume a monotonically versioned control epoch, reject commits under an older epoch, acknowledge the new epoch, and report active effects. Draining stops new effects while bounded in-flight calls finish or are cancelled; reconciliation determines what actually committed.

Operators define cancellation and containment SLOs. The evidence includes command identity, scope, epoch, distribution lag, executor acknowledgements, last accepted effect, remote cancellation result, unresolved receipts, and guarded resume decision. Resume is a separate authorized operation after root cause, credential state, policy, and external effects are reviewed.

## See it yourself

Approval digest \(d\) binds normalized effect \(E\). If the agent changes recipient, amount, tenant, or revision, it produces \(E'\ne E\), so a collision-resistant digest check requires a new approval. Binding only the displayed text is insufficient because target resolution or preconditions can change while wording stays constant.

For containment, assume 120 executors poll a control epoch every five seconds with uniformly distributed poll phase. Ignoring network delay, all should observe a new epoch within five seconds. If effect dispatch is fenced on epoch and each executor can begin at most two effects per second, the loose upper bound after command issuance is \(120\times2\times5=1{,}200\) newly started effects. That bound is unacceptable for destructive work, which motivates push invalidation, shorter polling, or synchronous epoch checks at commit. Measure the actual last accepted effect; planner cancellation alone proves none of this.

## Where it shows up

An operator console shows pending approvals separately from escalations and incidents. It supports deny with reason, request changes, pause, scoped containment, effect inventory, and resume. On-call runbooks identify decision owner, first safe action, communication path, and evidence to preserve.

Use [Lab 19: Bound an Agent Runtime](../labs/19-agent-runtime-safety/README.md) to prove exact approval binding. Then add epoch-fenced global commit disable and cancellation acknowledgements. The [retry-storm drill](../incidents/08-retry-storm/README.md) supplies the discipline for bounded retries during control-plane recovery, and the [Governed Agent Runtime](../projects/14-governed-agent-runtime/README.md) requires approval UX and incident evidence.

## When it breaks

Approval fatigue produces rubber-stamping; opaque summaries hide the actual target; stale approval races changed state; denial loops pressure reviewers; and an unavailable approver causes unsafe fallback. Kill switches fail when they share the failed policy service, stop only planners, lack executor acknowledgement, or automatically replay quarantined work after restart.

During an incident, stop new consequential effects at the narrowest sufficient scope, preserve events and receipts, inventory in-flight calls, revoke exposed credentials, and reconcile remote state. Do not delete runs or declare success from an empty local queue. A failed acknowledgement is unresolved containment and must remain visible.

## Practice

**Build:** implement an approval state machine with exact digest binding, expiry, deny, change request, escalation deadline, separation of duties, and safe unavailable-approver behavior. Add a versioned control epoch checked at effect commit and executor acknowledgements. **Break:** mutate an approved payload, change a target precondition, replay approval, delay one executor, lose the normal policy service, and complete one remote effect after planner cancellation.

**Prove:** no changed proposal commits under old approval; denial does not loop; control still operates without the planner; all executor acknowledgements or exceptions are enumerated; effect count after the stop command is bounded and measured; resume cannot occur until ambiguous effects are reconciled.

## Check yourself

1. Which fields must an approval bind?
2. Why is planner cancellation not proof of containment?
3. What evidence is required before a quarantined run resumes?

## Sources

### REQUIRED

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

### RECOMMENDED

- [Google SRE: managing incidents](https://sre.google/sre-book/managing-incidents/)

### DEEP DIVE

- [OAuth 2.0 Security Best Current Practice](https://www.rfc-editor.org/rfc/rfc9700)

## Next

Continue to [Fleet reliability and recovery](08-safety-controls-and-fleet-operations.md).
