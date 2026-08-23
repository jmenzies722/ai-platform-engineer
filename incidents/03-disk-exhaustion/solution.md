# Facilitator solution: Disk Exhaustion

This is one evidence-supported resolution path, not permission to skip investigation. Read the learner’s timeline and hypotheses before revealing it.

## Diagnosis

Higher export concurrency fills `/var`; most apparently missing space is held by the reporter’s deleted but still-open log file.

## Reasoning from evidence

1. Free inodes remain high, so inode exhaustion does not explain `ENOSPC`.
2. The affected paths share `/var`, localizing the failure to that filesystem.
3. Rotation without recovered space plus elevated open FDs supports a deleted-open-file hypothesis.
4. Concurrency increased before available bytes declined, explaining the initial capacity pressure.

No single symptom is enough. The diagnosis requires the observations above to agree and plausible alternatives to be tested.

## Discriminating investigation

| Test | Expected observation | What it establishes |
|---|---|---|
| Map paths with `df` and mount data | Both failures map to `/var` | Shared filesystem |
| Compare `du` with filesystem usage | Allocated space exceeds visible files | Hidden allocation likely |
| List deleted-open files with `lsof +L1` | Reporter owns large deleted log | Space retained by open descriptor |

Stop if a result differs. Update the hypothesis rather than forcing this solution.

## Decision analysis

The first priority is user and data safety, followed by preserving enough evidence to distinguish recurrence from a new failure. Avoid broad restarts, unbounded capacity increases, disabled verification, or destructive cleanup: each can conceal the mechanism or enlarge the blast radius.

The preferred response is: Pause new exports, reserve space for durability-critical components, remove only verified disposable temporary files, and restart or signal the process holding deleted files after capturing ownership evidence.

## Mitigation sequence

1. Declare scope, owner, and a measurable rollback trigger.
2. Capture the smallest decisive evidence set, including timestamps and version or resource identity.
3. Stop new work that amplifies impact while preserving durable work.
4. Apply the reversible mitigation to a canary or narrow cohort.
5. Compare canary and control signals, then expand only if the expected causal signal changes.

## Recovery proof

- Sustained free-byte headroom above the defined threshold
- No ENOSPC in service or co-located dependencies
- A canary export completes and cleanup removes its temporary data

Continue monitoring for a full relevant workload cycle. Remove temporary controls only with the same evidence standard.

## Prevention plan

- Bound export concurrency and temporary-file size
- Alert on bytes, inodes, quotas, and projected time to full
- Place disposable exports on an isolated filesystem
- Verify rotation reopens file descriptors

“Be more careful” is not an action. Convert each item into a tested control with an owner and objective completion evidence.

## Debrief guide

- Strong investigations separate the immediate failure mechanism from the condition that triggered it.
- Strong mitigations reduce offered harm without converting a transient incident into hidden permanent risk.
- Strong recovery checks include a user-visible signal, a subsystem signal, and evidence that temporary changes were removed.
- Ask which observation would falsify this diagnosis. If the team cannot name one, it is telling a story rather than testing a hypothesis.

## Authoritative sources

- [GNU Coreutils df](https://www.gnu.org/software/coreutils/manual/html_node/df-invocation.html)
- [Linux open(2)](https://man7.org/linux/man-pages/man2/open.2.html)
- [Linux lsof manual](https://man7.org/linux/man-pages/man8/lsof.8.html)
