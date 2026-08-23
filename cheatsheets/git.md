# Git operator sheet

Use this sheet to identify which graph, reference, index, or working-tree state
differs before rewriting anything.

## Frame the question

Ask: Which repository and branch? Is the missing work committed, staged,
unstaged, untracked, stashed, or only on a remote? Is history already shared?

```bash
# Read-only
git rev-parse --show-toplevel
git status --short --branch
git remote -v
git log --graph --decorate --oneline --all -20
```

`status` separates index changes from working-tree changes. `ahead N` means
local commits are not in the configured upstream; `behind N` means upstream
commits are absent locally. Remote-tracking refs are cached observations, not
live server state.

## What exactly differs?

```bash
# Read-only
git diff                         # working tree versus index
git diff --cached                # index versus HEAD
git diff HEAD                    # working tree and index versus HEAD
git diff --stat <base>...HEAD    # branch work from merge base
git log --left-right --cherry-pick --oneline <upstream>...HEAD
```

No output from one `diff` only means that specific pair matches. Three dots in
the branch diff use the merge base; two dots compare endpoint trees. In the
left/right log, `<` belongs only to upstream and `>` only to `HEAD`;
`--cherry-pick` suppresses patch-equivalent commits.

**Caution:** Untracked and ignored files do not appear in normal diffs. Inspect
with `git status --short --untracked-files=all` and `git status --ignored`
before cleanup.

## Is remote state stale or history divergent?

```bash
# Remote read and local reference update; no remote mutation
git fetch --prune origin
git status --short --branch
git merge-base HEAD origin/<branch>
git log --left-right --oneline origin/<branch>...HEAD
```

Fetch updates remote-tracking refs and may trigger credential or network access.
`--prune` removes stale remote-tracking refs, not server branches. Divergence
means both sides have unique commits; choose merge or rebase based on the
repository policy and whether commits are shared.

## Can missing work be recovered?

```bash
# Read-only
git reflog --date=iso
git stash list
git fsck --no-reflogs --unreachable
```

Reflogs record local reference movement and often reveal pre-rebase or
pre-reset commits. Stashes are commits with special refs. Unreachable objects
are candidates, not proof of ownership, and garbage collection eventually
removes them.

```bash
# Local mutation; create a rescue reference before further work
git branch rescue/<date-and-purpose> <object-id>
```

Verify with `git show --stat <object-id>` first. A rescue branch makes the
object reachable and gives rollback a named point.

## Integrate without surprising collaborators

```bash
# Read-only previews
git merge-tree "$(git merge-base HEAD <upstream>)" HEAD <upstream>
git rebase --show-current-patch   # only during a rebase
```

For unshared local commits, rebase can produce a linear series. For shared
history, merge preserves existing commit identities. Conflicts are semantic:
successful conflict-marker removal does not prove correct behavior.

```bash
# Local mutation
git merge --no-commit --no-ff <upstream>
# inspect and test, then commit; or roll back:
git merge --abort
```

`--no-commit` pauses before the merge commit when a merge commit would be
created. It does not prevent a fast-forward, hence `--no-ff`. Abort can fail if
uncommitted work overlapped; commit or stash intentionally before integration.

```bash
# Local mutation; only for unshared commits
git rebase <upstream>
# resolve and use git rebase --continue, or roll back:
git rebase --abort
```

## Undo according to publication state

- Unpublished commit: create a rescue branch, then a policy-approved reset or
  rebase may be appropriate.
- Published commit: prefer `git revert <commit>` to add an inverse commit.
- Working-tree mistake: restore only named paths after inspecting the diff.
- Secret committed: reverting does not remove history or exposure. Revoke the
  secret immediately and escalate to repository security owners.

```bash
# Local mutation; preserves history
git revert --no-commit <commit>
git diff --cached
# commit after tests, or cancel with:
git revert --abort
```

**Caution:** `reset --hard`, `clean`, force-push, and broad `restore` can destroy
work. They are intentionally omitted. A lease reduces force-push races but does
not make published history rewriting socially safe.

## Before push

```bash
# Read-only or hook-defined local effects
git diff --check
git diff --stat origin/<branch>...HEAD
git log --oneline origin/<branch>..HEAD
```

Confirm intended commits, generated files, tests, authorship, and target branch.
Push is a remote mutation. Follow branch protection and review policy; never
bypass a rejected non-fast-forward without understanding the remote commits.

Escalate for ambiguous repository ownership, shared-history rewrites, signed
commit requirements, suspected credential leakage, or recovery after object
pruning.

## Authoritative sources

- [Git reference](https://git-scm.com/docs)
- [Git user manual](https://git-scm.com/docs/user-manual)
- [Pro Git](https://git-scm.com/book/en/v2)
- Repository lesson: [Git](../05-git/README.md)
