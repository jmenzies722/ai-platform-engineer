# Branches, Merges, and Conflicts

A branch is a movable name for a commit; collaboration combines histories and sometimes requires a human decision.

## Why it matters

Two teams can edit different files and still create a semantic conflict, while Git can mark the same line as a textual conflict it cannot resolve. Deciding whether to merge, rebase, or redesign work starts with the commit graph and the intent represented by each branch. A conflict is a request for a human decision, not an instruction to delete markers until the command succeeds.

## How it works

Creating a branch creates a reference, not a copy of every file. Commits advance the checked-out branch. A fast-forward moves a reference when no histories diverged. A three-way merge compares two tips with a common ancestor. Conflicts mark regions Git cannot combine safely.

A branch reference stores one commit ID and moves when new commits are made on that branch. Divergence occurs when two tips have commits not reachable from the other. For a three-way merge Git finds a common ancestor, compares each tip with that base, and combines compatible path changes into a new index and working tree. If one tip already contains the other, moving the lagging reference is a fast-forward and needs no merge commit. Conflicted index entries retain base, ours, and theirs versions so tools can show the competing changes. After a human creates the intended result and stages it, a merge commit records both parent tips. Rebase instead copies changes onto another base and creates new commits, which changes object IDs and should be coordinated when history is shared.

## See it yourself

Predict that both newly created branch names initially resolve to the same empty commit. In the lab, predict which line conflicts by comparing each branch with the common ancestor before invoking merge.

```bash
d=$(mktemp -d); git -C "$d" init -q
git -C "$d" -c user.name=Demo -c user.email=demo@example.com commit --allow-empty -qm base
git -C "$d" branch feature
git -C "$d" show-ref --heads
rm -rf "$d"
```

Expected observation: Both branch names initially point at the same commit; no project directory was duplicated.

Limits of the branches, merges, and conflicts observation: The branch listing does not prove future merges will be clean, and a conflict-free merge does not prove compatible behavior. Git compares stored content and graph ancestry, not business meaning.

## Where it shows up

A schema change and application change often merge cleanly in separate directories but fail when deployed in the wrong order. Reviewers need both the textual merge result and compatibility tests against the shared base. Short-lived branches reduce graph divergence, while feature flags or expand-and-contract migrations handle operational overlap that source merging cannot solve.

## When it breaks

Conflict markers and `UU` status identify unresolved textual paths; tests failing after a clean merge point toward semantic interaction; a surprising history shape suggests the wrong base or unintended rewrite. First preserve `status`, `log --graph --all`, and `merge-base`, then inspect the three versions of each conflicted path. Abort only after saving any intentional resolution work, and never choose ours or theirs wholesale without reading the shared intent.

## Practice

**Build:** complete [Create, Merge, and Recover a Git Repository](./lab-branch-merge-recover.md) and annotate the two-parent merge graph. **Break:** create one textual conflict and one clean semantic conflict caught by a test. **Explain back:** describe base, tips, three-way comparison, index stages, resolution, and resulting parents. Success requires a resolved file that satisfies both stated requirements, passing tests, and a graph matching your prediction.

## Check yourself

1. What makes a merge fast-forward?
2. Why can Git merge cleanly while the program is still wrong?

## Sources

### REQUIRED

- [git-merge](https://git-scm.com/docs/git-merge)

### RECOMMENDED

- [Pro Git: branching](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)

### DEEP DIVE

- [A Note About Git Commit Messages](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)

## Next

Continue to [Inspecting and Recovering History](./03-inspecting-and-recovering-history.md).
