# Inspecting and Recovering History

Safe Git recovery starts by identifying which state changed and whether the commit is already shared.

## Why it matters

Recovery commands differ radically depending on whether unique work lives in the working tree, index, an unshared commit, or published history. Running a remembered `reset --hard` before locating that work can turn a reversible mistake into loss. The first decision is not which command to type; it is which state changed and who else may rely on it.

## How it works

`git status`, `diff`, and `log` inspect the working tree, index, and history. `restore` can replace working or staged content; it may discard local work. `revert` creates a new commit that inverses an earlier change and preserves shared history. Reflogs record recent local reference movements and can help recover reachable commits.

`status` summarizes relationships among `HEAD`, index, and working tree; `diff` can compare any chosen pair. `restore` copies selected content from a source into the working tree or index and can therefore discard unique edits. `reset` moves a branch or adjusts index and working state according to mode, so its scope must be explicit. `revert` computes an inverse patch and records a new commit, preserving the existing graph for collaborators. Reflogs record local updates to references such as branch movement and `HEAD` checkout, making recently unreachable commits discoverable by prior object ID. They are local maintenance records, not shared history, and expiration means they are not a backup. Once an object ID is known, creating a branch or tag makes the commit reachable again without rewriting anything.

## See it yourself

Predict that the unstaged diff shows `changed`, then `restore a` replaces the working file from the index, whose content matches `HEAD`. Copy the changed text elsewhere first if it has value.

```bash
d=$(mktemp -d); git -C "$d" init -q
printf 'kept\n' > "$d/a"; git -C "$d" add a
git -C "$d" -c user.name=Demo -c user.email=demo@example.com commit -qm kept
printf 'changed\n' > "$d/a"
git -C "$d" diff -- a
git -C "$d" restore a
rm -rf "$d"
```

Expected observation: The diff shows an unstaged change, and restore deliberately returns the working file to the indexed version.

Limits of the inspecting and recovering history observation: This example does not recover unstaged content after restoration, show published-history policy, or guarantee reflog retention. It demonstrates a deliberate destructive copy in a repository whose unique content is disposable.

## Where it shows up

A bad production commit on a shared main branch is usually safer to revert than to erase. The inverse commit is reviewable, deployable, and visible to every clone, while later work remains based on a stable graph. A local accidental branch deletion is different: reflog inspection and a new branch can restore the old tip without creating an inverse change.

## When it breaks

Missing working edits call for editor history, stash inspection, or filesystem recovery; a lost staged version requires checking index and dangling objects; a deleted branch with committed work suggests reflog; a harmful shared commit suggests revert. First stop mutating the repository and capture `status`, `log --all --graph`, and relevant reflogs. Write down candidate object IDs and inspect them with `show` before moving any reference.

## Practice

**Build:** in a disposable repository, create unique content in working tree, index, and three commits, then label where each version exists. **Break:** delete a temporary branch and restore it from a verified reflog object; separately revert a shared-style commit. **Explain back:** justify why each recovery preserves or changes history. Success means checksums of recovered files match saved expectations and no command depends on guessing a reference name.

## Check yourself

1. When is revert safer than reset?
2. Which Git states can contain unique work before a commit?

## Sources

### REQUIRED

- [git-restore](https://git-scm.com/docs/git-restore)
- [git-revert](https://git-scm.com/docs/git-revert)

### RECOMMENDED

- [git-reflog](https://git-scm.com/docs/git-reflog)

### DEEP DIVE

- [Git data recovery](https://git-scm.com/book/en/v2/Git-Internals-Maintenance-and-Data-Recovery)

## Next

Continue to [Data Structures and Algorithms](../06-data-structures-algorithms/README.md).
