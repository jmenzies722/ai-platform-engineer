# Lab: Create, Merge, and Recover a Git Repository

This lab uses a disposable repository to make snapshots, divergence, conflict resolution, and recovery visible. It never touches the curriculum repository.

## Create two snapshots

```bash
lab=$(mktemp -d)
git -C "$lab" init -q
printf 'color=blue\n' > "$lab/app.conf"
git -C "$lab" add app.conf
git -C "$lab" -c user.name=Lab -c user.email=lab@example.com commit -qm 'add configuration'
git -C "$lab" switch -c feature
printf 'color=green\n' > "$lab/app.conf"
git -C "$lab" -c user.name=Lab -c user.email=lab@example.com commit -am 'use green' -q
```

Expected observation: `feature` points to the green commit and its parent contains blue. Confirm with `git -C "$lab" log --oneline --decorate --all --graph`.

## Create divergence and a conflict

```bash
git -C "$lab" switch -q master 2>/dev/null || git -C "$lab" switch -q main
printf 'color=red\n' > "$lab/app.conf"
git -C "$lab" -c user.name=Lab -c user.email=lab@example.com commit -am 'use red' -q
git -C "$lab" merge feature || true
git -C "$lab" status --short
```

Expected observation: both branches changed the same line from a common ancestor, so Git marks `app.conf` unresolved. Inspect the file and `git -C "$lab" diff --cc` before editing.

## Resolve from intent

Choose either red or green and document why in a second line:

```bash
printf 'color=green\nreason=feature requirement\n' > "$lab/app.conf"
git -C "$lab" add app.conf
git -C "$lab" -c user.name=Lab -c user.email=lab@example.com commit -qm 'resolve color choice'
git -C "$lab" log --oneline --decorate --all --graph
```

Expected observation: the merge commit has two parents. A clean merge records your decision; it does not prove the chosen configuration is correct.

## Recover a discarded branch name

```bash
git -C "$lab" branch recovery-demo
tip=$(git -C "$lab" rev-parse recovery-demo)
git -C "$lab" branch -D recovery-demo
git -C "$lab" reflog --all --oneline | sed -n '1,8p'
git -C "$lab" branch recovered "$tip"
test "$(git -C "$lab" rev-parse recovered)" = "$tip" && echo recovered
```

Expected observation: `recovered` points to the saved commit. The reflog is local and temporary, so record object IDs before destructive experiments.

## Cleanup

```bash
rm -rf "$lab"
```

Expected observation: the disposable repository is gone and the curriculum working tree was never used.

## Next

Continue to [Inspecting and Recovering History](./03-inspecting-and-recovering-history.md).
