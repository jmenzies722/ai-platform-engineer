# Remotes, Fetching, and Collaborative State

A Git remote is a named repository location. Fetching copies objects and updates remote-tracking references; it does not silently merge those commits into your branch.

## Why it matters

“I pulled and my code changed” hides two separate operations: obtaining shared history and integrating it locally. That ambiguity makes conflict response and automation unsafe. Collaboration becomes predictable when local branches, remote-tracking references, upstream configuration, and server policy are named separately.

## How it works

Each repository has its own object database and references. A remote name such as `origin` stores URLs and fetch configuration. `git fetch` negotiates reachable objects, transfers missing ones, and updates references such as `refs/remotes/origin/main` to represent the fetched remote state. Your local `main` does not move merely because `origin/main` moved. An upstream association tells status and argument-free pull or push which branch is related; it does not make the references identical.

`git pull` runs fetch followed by a configured integration strategy, usually merge or rebase. Separating those steps leaves an inspection point. `git push` asks the receiver to update a reference after transferring objects. The server can reject a non-fast-forward update, missing permission, failed hook, or policy violation. Remote-tracking references are local records and can be stale until fetched. Authentication establishes who may request transport operations; commit authorship is metadata and does not by itself prove authenticated origin.

## See it yourself

**Tiny Proof:** use two local repositories so no network or credentials are involved. Predict that fetching updates `origin/main` while the clone’s local `main` remains at its old commit.

```bash
root=$(mktemp -d)
git -C "$root" init -q --bare shared.git
git -C "$root" clone -q shared.git one
git -C "$root/one" -c user.name=Lab -c user.email=lab@example.com commit --allow-empty -qm base
git -C "$root/one" push -q origin HEAD:main
git -C "$root" clone -q shared.git two
git -C "$root/one" -c user.name=Lab -c user.email=lab@example.com commit --allow-empty -qm later
git -C "$root/one" push -q origin HEAD:main
git -C "$root/two" fetch -q origin
git -C "$root/two" show-ref
rm -rf "$root"
```

Expected observation: repository `two` has fetched the later remote-tracking reference; its checked-out local state does not automatically integrate it.

Limits of this proof: local-path transport does not exercise authentication, network interruption, hosting policy, or concurrent push races. Empty commits simplify content but preserve graph behavior.

## Where it shows up

A CI job should fetch the exact pull-request and base references it intends to test, then record their commit IDs. Assuming a checkout’s `main` is current can test stale code. For developers, `fetch`, graph inspection, and explicit merge or rebase make the collaboration decision visible before files change. Protected branches and required checks add server-side policy but do not repair an incorrect local model.

## When it breaks

“Rejected non-fast-forward” means the receiver would lose commits from the updated reference; “repository not found” can mean URL or authorization; a missing remote commit may mean stale tracking state or shallow history. First record remotes without embedded credentials, current branch and upstream, `status`, and `log --graph --all`. Never place tokens in remote URLs or paste credential-bearing configuration into reports.

## Practice

**Build:** create a bare local remote and two clones, make divergent commits, fetch in each, and predict every reference before integration. **Break:** attempt a non-fast-forward push and preserve the rejection, then integrate without force. **Explain back:** distinguish remote, remote-tracking reference, local branch, upstream, fetch, pull, and push. Success means both unique commits remain reachable and the final graph matches a drawing made before commands.

## Check yourself

1. What state does fetch update, and what does it normally leave unchanged?
2. Why can `origin/main` be stale?

## Sources

### REQUIRED

- [git-fetch](https://git-scm.com/docs/git-fetch)

### RECOMMENDED

- [git-push](https://git-scm.com/docs/git-push)
- [Pro Git: working with remotes](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes)

### DEEP DIVE

- [Git transfer protocols](https://git-scm.com/book/en/v2/Git-Internals-Transfer-Protocols)

## Next

Continue to [Reviewable History, Rebase, and Integration](./05-reviewable-history-rebase-and-integration.md).
