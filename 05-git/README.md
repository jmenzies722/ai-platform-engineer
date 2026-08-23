# 05 — Git and Version Control

Build a graph-and-snapshot model of Git strong enough to support collaboration under pressure. The sequence moves from local objects through merges and recovery to remotes, reviewable integration, releases, and repository stewardship.

## What you will learn

By the end, you can predict the next snapshot, read a commit graph, resolve conflicts from intent, recover local references, explain fetch and push without “cloud” metaphors, choose merge or rebase deliberately, verify release identities, and prevent generated or sensitive material from entering shared history.

## Lessons

1. [Snapshots, Objects, and Commits](./01-snapshots-objects-and-commits.md)
2. [Branches, Merges, and Conflicts](./02-branches-merges-and-conflicts.md)
3. [Inspecting and Recovering History](./03-inspecting-and-recovering-history.md)
4. [Remotes, Fetching, and Collaborative State](./04-remotes-fetching-and-collaborative-state.md)
5. [Reviewable History, Rebase, and Integration](./05-reviewable-history-rebase-and-integration.md)
6. [Tags, Releases, and Repository Stewardship](./06-tags-releases-and-repository-stewardship.md)

## Practice

[Create, Merge, and Recover a Repository](./lab-branch-merge-recover.md) after lesson 3. Repeat its graph inspection after lessons 4 and 5 using a second local repository as a remote, then annotate which references are local, remote-tracking, and shared.

Practice is part of the path, not an optional recap. Predict first, work only in disposable or explicitly scoped resources, compare expected and actual observations, and perform the documented cleanup.

## Ready to continue

Continue when you can account for unique content in working tree, index, and commits; draw merge parents; recover a deleted local branch; explain why fetch does not change your branch; integrate without rewriting others’ work; identify the commit a tag names; and respond safely if a credential enters history.

## Next

Start with [Snapshots, Objects, and Commits](./01-snapshots-objects-and-commits.md).
