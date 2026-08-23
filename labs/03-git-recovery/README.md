# Lab: Recover Git Work Without Rewriting Shared History

Build a disposable repository, lose several references in controlled ways, and recover commits by reasoning about objects, refs, the index, and reflogs.

## Prerequisites

- Git 2.30 or newer and Bash
- No network or remote repository
- Familiarity with commits, branches, and the staging area

## Safety

Run every command inside `.work/recovery-repo`. Verify `git rev-parse --show-toplevel` before any reset or clean operation. The exercise never uses `--hard`, force push, or an existing repository.

## Setup and baseline

```bash
mkdir -p .work/recovery-repo
cd .work/recovery-repo
git init -q
git config user.name "Lab User"
git config user.email "lab@example.invalid"
printf 'v1\n' > service.txt
git add service.txt && git commit -qm "baseline"
git symbolic-ref --short HEAD >../initial-branch.txt
git status --short
git log --oneline --decorate
```

Predict which data remains after deleting a branch name and which data remains after restoring a file from the index.

## Tasks

1. Create two commits and record their object IDs:

   ```bash
   printf 'v2\n' >> service.txt
   git commit -qam "add v2"
   V2=$(git rev-parse HEAD)
   git switch -c experiment
   printf 'experiment\n' > experiment.txt
   git add experiment.txt && git commit -qm "experiment"
   EXP=$(git rev-parse HEAD)
   printf '%s %s\n' "$V2" "$EXP" | tee ../known-ids.txt
   ```

2. Switch to the initial branch, delete `experiment`, and recover it using `git reflog --all` plus `git branch recovered <object-id>`.
3. Modify `service.txt`, stage it, modify it again, then capture `git diff` and `git diff --cached`. Restore only the worktree copy with `git restore service.txt`; prove the staged copy remains.
4. Detach at `V2`, make one commit, switch away, and recover the dangling commit from `git reflog` without running garbage collection.
5. Draw a three-column account of `HEAD`, index, and worktree after each operation.

## Evidence to keep

Store under `.work`: `known-ids.txt`, reflog excerpts, `git cat-file -t` results for recovered IDs, before-and-after graphs from `git log --graph --all --oneline`, and a recovery narrative. Redact real user configuration if your global config appears.

## Failure injection

Delete only the disposable branch:

```bash
git switch "$(<../initial-branch.txt)"
git branch -D recovered
```

Expected symptom: the name disappears from `show-ref`, while the object is still discoverable in the reflog. Recover it under `recovered-again` and verify its tree with `git show --stat`.

## Cleanup

```bash
cd ../..
test "$(pwd)" != "/"
rm -rf .work
```

## Rubric

- 2 points: distinguishes refs, objects, index, and worktree
- 3 points: recovers both deleted-branch and detached commits
- 2 points: uses reflog and object inspection rather than guessed hashes
- 2 points: demonstrates non-destructive staged-file recovery
- 1 point: operates only in the disposable repository and cleans it

## Sources

- [Git data recovery](https://git-scm.com/docs/user-manual#recovering-lost-changes)
- [`gitrevisions(7)`](https://git-scm.com/docs/gitrevisions)
- [`git-reflog(1)`](https://git-scm.com/docs/git-reflog)
