# Tags, Releases, and Repository Stewardship

A healthy repository makes important versions reproducible, keeps ownership and generated content clear, and treats sensitive history as an incident rather than a cosmetic mistake.

## Why it matters

“Version 2.1” is ambiguous unless it names an immutable commit and the build records its inputs. A mutable branch, local ignored file, or regenerated dependency can make the same command produce a different artifact. Repository stewardship establishes identity, provenance, retention, and response rules before a release or secret exposure forces them.

## How it works

A lightweight tag is a reference to an object. An annotated tag is a tag object containing a target, tagger, message, and optional signature. Tags do not move automatically with commits and are commonly used to name release points. Hosting-platform releases may attach notes and artifacts but remain a layer above Git’s object model. Reproducibility also depends on toolchain, dependencies, environment, and build instructions, not only source commit.

`.gitignore` controls which untracked paths ordinary status and add operations notice; it does not remove tracked files or erase history. Attributes define path-specific behavior such as text normalization and merge handling. Large or generated artifacts need an explicit ownership policy. Repository maintenance packs objects and prunes unreachable data after retention rules; routine maintenance is not a secret-removal strategy. If a credential is committed, rotate or revoke it first, assess exposure, then coordinate any history rewrite because every clone and artifact may retain the old bytes.

## See it yourself

**Tiny Proof:** predict that the annotated tag resolves first to a tag object and then, when peeled, to its commit.

```bash
d=$(mktemp -d); git -C "$d" init -q
git -C "$d" -c user.name=Lab -c user.email=lab@example.com commit --allow-empty -qm release
git -C "$d" -c user.name=Lab -c user.email=lab@example.com tag -am 'version 1' v1
git -C "$d" cat-file -t v1
git -C "$d" rev-parse v1^{}
git -C "$d" rev-parse HEAD
rm -rf "$d"
```

Expected observation: `v1` is a tag object and its peeled target equals `HEAD`.

Limits of this proof: the tag is unsigned, local, and attached to an empty commit. It does not establish release artifact reproducibility or remote immutability policy.

## Where it shows up

A release pipeline can require a reviewed annotated tag, build in a clean environment, record commit and dependency lock hashes, generate a software bill of materials, sign artifacts, and verify them before deployment. Those controls form a provenance chain. They do not prove the software has no defect, but they let responders identify exactly what was built and where a vulnerable component appears.

## When it breaks

A dirty tree during release suggests undeclared input; a tag resolving to an unexpected object suggests naming or movement; line-ending-only diffs suggest attributes or editor mismatch; a repository that balloons may contain generated or large binary history. First record `status`, exact commit, tag object, relevant attributes, build inputs, and object-size evidence. For secrets, revoke immediately and follow hosting and organizational procedures; deleting the working file and adding it to ignore is insufficient.

## Practice

**Build:** create a disposable release commit, annotated tag, ignore rule, and attributes rule; clone it and verify the peeled commit and clean build inputs. **Break:** track a file before ignoring it and prove it remains tracked, then remove it from the next snapshot without claiming old history vanished. **Explain back:** distinguish branch, lightweight tag, annotated tag, release artifact, ignore rule, and provenance. Success includes exact object IDs and a written credential-exposure response ordered with revocation first.

## Check yourself

1. Why does a tag alone not make a build reproducible?
2. Why does `.gitignore` not remove a secret from history?

## Sources

### REQUIRED

- [git-tag](https://git-scm.com/docs/git-tag)

### RECOMMENDED

- [gitignore](https://git-scm.com/docs/gitignore)
- [gitattributes](https://git-scm.com/docs/gitattributes)

### DEEP DIVE

- [SLSA specification](https://slsa.dev/spec/)

## Next

Continue to [Data Structures and Algorithms](../06-data-structures-algorithms/README.md).
