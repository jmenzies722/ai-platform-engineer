# Snapshots, Objects, and Commits

Git records snapshots addressed by content; commits connect those snapshots into history.

## Why it matters

A reviewer needs to know exactly which content a commit records, especially when the working directory also contains unfinished edits. Treating a commit as “everything I changed” leads to accidental secrets, generated files, or half a refactor entering history. The engineering decision is which snapshot is coherent enough to test, explain, and share.

## How it works

Blobs store file contents, trees map names to blobs and subtrees, and commits name a root tree plus parent commits and metadata. The working tree is what you edit. The index is the proposed next snapshot. `git add` copies selected content into the index; `git commit` creates objects and moves the current branch reference.

Git hashes object type and content to name immutable blobs, trees, commits, and annotated tags. A blob contains bytes but no pathname; a tree supplies names, modes, and references to blobs or subtrees. A commit points to one root tree, zero or more parent commits, and metadata, so history is a graph of complete snapshots. The index is a mutable staging table for the proposed tree. `git add` writes object content as needed and updates index entries; it does not simply set a flag on a working file. `HEAD` identifies the checked-out commit through a branch or detached reference. Committing writes the tree and commit, then advances the current branch atomically. Diffs are derived comparisons between states, which is why Git can present history as changes even though commits identify snapshots.

## See it yourself

**Tiny Proof:** predict that the commit contains `note.txt`, has one root tree, and becomes the target of the initial branch. Before committing in your own experiment, use both `git diff` and `git diff --cached` to predict the snapshot.

```bash
d=$(mktemp -d); git -C "$d" init -q
printf 'one\n' > "$d/note.txt"
git -C "$d" add note.txt
git -C "$d" -c user.name=Demo -c user.email=demo@example.com commit -qm 'add note'
git -C "$d" show --stat --oneline HEAD
rm -rf "$d"
```

Expected observation: The commit records a snapshot containing `note.txt`; it is not merely a patch stored as a line of history.

Limits of the snapshots, objects, and commits observation: The demonstration does not show object packing, remote synchronization, or whether the committed content is correct. A successful commit proves object creation and reference movement, not test quality.

## Where it shows up

A configuration repository benefits from snapshot precision because deployment can name one commit and reconstruct every tracked file at that point. If an operator stages only a policy file but leaves a local credentials file untracked, `git status` and the cached diff make the boundary visible before release. Signed or reviewed commits can strengthen provenance, but they still attest to a snapshot, not to runtime safety.

## When it breaks

A missing change after commit often means it never entered the index; an unexpected file means staging was broader than intended; a secret removed in a later commit still exists in earlier objects. First inspect `status`, the working diff, and `diff --cached`, then inspect `show --stat --name-status HEAD`. If sensitive data entered history, stop sharing and follow repository-specific credential rotation and history-remediation procedures rather than assuming an ordinary delete erases it.

## Practice

**Build:** initialize a disposable repository, create two files, stage one, and write down the exact first tree before committing. **Break:** modify a staged file again so index and working tree hold different versions; inspect all three states without using destructive restore. **Explain back:** map blob, tree, commit, parent, index, working tree, `HEAD`, and branch to object IDs or visible content. Success means your predicted snapshot matches `git show` byte for byte and cleanup removes only the disposable repository.

## Check yourself

1. How do the working tree, index, and `HEAD` differ?
2. Why can equal content share a blob?

## Sources

### REQUIRED

- [Git internals: objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

### RECOMMENDED

- [gitglossary](https://git-scm.com/docs/gitglossary)

### DEEP DIVE

- [Pro Git](https://git-scm.com/book/en/v2)

## Next

Continue to [Branches, Merges, and Conflicts](./02-branches-merges-and-conflicts.md).
