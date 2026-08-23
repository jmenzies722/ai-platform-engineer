# Reviewable History, Rebase, and Integration

History is both a technical graph and a communication artifact. Integration should preserve shared work while presenting changes in units that can be reviewed, tested, reverted, and understood.

## Why it matters

A single commit mixing a rename, dependency upgrade, behavior change, and formatting makes review and rollback needlessly risky. Rewriting published commits to improve appearance can be worse because collaborators may already depend on their identities. Good history balances clarity with the graph’s shared-state constraints.

## How it works

Each commit should represent one coherent change with a message explaining intent and consequences. Interactive rebase can reorder, combine, edit, or reword unshared commits by replaying them and creating new object IDs. Ordinary rebase finds commits unique to a branch and applies equivalent changes onto a new base; even unchanged-looking commits are new graph nodes. Cherry-pick similarly applies the change introduced by selected commits and records new commits.

Merge preserves existing commits and records ancestry with multiple parents. Squash integration creates one combined commit without preserving feature-branch commits as ancestors. The right strategy depends on repository policy, audit needs, bisectability, and whether the commits are shared. Review should inspect the intended range, tests, generated artifacts, migrations, security effects, and operational plan. Passing checks establishes only what those checks cover. Commit signatures can authenticate a signing key relationship but do not certify correctness.

## See it yourself

**Tiny Proof:** predict that rebasing changes the feature commit ID while preserving its file result.

```bash
d=$(mktemp -d); git -C "$d" init -q
git -C "$d" -c user.name=Lab -c user.email=lab@example.com commit --allow-empty -qm base
git -C "$d" switch -qc feature
printf 'feature\n' > "$d/f"; git -C "$d" add f
git -C "$d" -c user.name=Lab -c user.email=lab@example.com commit -qm feature
before=$(git -C "$d" rev-parse HEAD)
git -C "$d" switch -q master 2>/dev/null || git -C "$d" switch -q main
git -C "$d" -c user.name=Lab -c user.email=lab@example.com commit --allow-empty -qm main
git -C "$d" switch -q feature; git -C "$d" rebase -q @{-1}
printf 'changed=%s content=%s\n' "$([ "$before" != "$(git -C "$d" rev-parse HEAD)" ] && echo yes)" "$(cat "$d/f")"
rm -rf "$d"
```

Expected observation: the rebased commit has a new ID and still produces `feature` in the file.

Limits of this proof: the base branch name varies by Git configuration, the change has no conflict, and equivalent content does not imply equivalent metadata or review context.

## Where it shows up

Before review, an author may split an unshared exploratory commit into one refactor and one behavior change, with tests passing after each. The reviewer can then verify that the first preserves behavior and focus semantic attention on the second. Once other people base work on those commits, a merge usually preserves coordination better than rewriting them for neatness.

## When it breaks

Repeated conflicts during rebase suggest a long-lived branch or commits that mix concerns; commits that fail their own tests weaken bisectability; missing collaborators’ commits after force push indicate shared history was rewritten. First save current references, inspect `status` and the graph, and identify which commits are published. If a rebase is in progress, inspect the current patch and conflict base before continuing or aborting. Never force push unless repository policy and collaborators explicitly permit the rewrite.

## Practice

**Build:** create three unshared commits, use interactive rebase in a disposable repository to reword and combine them, and compare old and new graphs. **Break:** introduce one controlled conflict and resolve it from intent. **Explain back:** contrast merge, rebase, cherry-pick, and squash by parents and object identity. Success means tests pass at every retained commit and all pre-rewrite tips remain temporarily named until verification completes.

## Check yourself

1. Why does rebase create new commit IDs?
2. When does a tidy linear graph impose unacceptable collaboration cost?

## Sources

### REQUIRED

- [git-rebase](https://git-scm.com/docs/git-rebase)

### RECOMMENDED

- [git-cherry-pick](https://git-scm.com/docs/git-cherry-pick)
- [Pro Git: rewriting history](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History)

### DEEP DIVE

- [Git project submission guidelines](https://git-scm.com/docs/SubmittingPatches)

## Next

Continue to [Tags, Releases, and Repository Stewardship](./06-tags-releases-and-repository-stewardship.md).
