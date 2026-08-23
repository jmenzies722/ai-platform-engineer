# Users, Privilege, and Software Installation

Linux associates operations with numeric identities and capabilities, while distributions and language tools install software into distinct ownership domains. Safe administration keeps both boundaries explicit.

## Why it matters

Running an installer with `sudo` can place root-owned files in a developer environment, execute unreviewed lifecycle scripts with broad authority, and make later upgrades irreproducible. Permission failures do not automatically justify elevation. First determine which identity performs the operation and which package system should own the destination.

## How it works

Users and groups are represented by numeric UIDs and GIDs; names are resolved through configured identity sources. A process has real, effective, saved, and filesystem-related credentials used for different checks. Supplementary groups add access. Traditional root has broad authority, while Linux capabilities split portions of that authority. `sudo` applies policy to execute a command as another user; it is an auditable boundary, not a general fix for writable paths.

Distribution package managers install signed or authenticated artifacts, track files and dependencies, and coordinate system upgrades. Language package managers manage a different ecosystem and should normally target an isolated environment or user-scoped tool mechanism rather than overwrite distribution-managed libraries. Containers and virtual environments isolate some paths and dependencies but do not make artifacts trustworthy. Provenance includes source repository, version, checksum or signature, build process, and update owner. Least privilege means granting only the identity and operations required, for only the needed duration.

## See it yourself

**Tiny Proof:** predict that the shell and Python report the same effective numeric identity and groups. Names are labels resolved from those numbers.

```bash
id
python3 - <<'PY2'
import os
print("real_uid", os.getuid())
print("effective_uid", os.geteuid())
print("groups", os.getgroups())
PY2
```

Expected observation: the process credentials correspond to the current shell identity; real and effective UID are usually equal in an ordinary session.

Limits of this proof: it does not exercise `sudo`, capabilities, user namespaces, ACLs, or remote identity services. Group membership changes may require a new login session.

## Where it shows up

A production service should run under a dedicated identity with access only to its configuration, state, and required sockets. The deployment system installs artifacts with known provenance, while the service process cannot modify its executable. A Python application can use a virtual environment built from pinned inputs without replacing the system Python packages used by host tools. Ownership boundaries then support both security and predictable upgrades.

## When it breaks

`Permission denied` suggests credentials or policy, not necessarily a need for root; “externally managed environment” indicates distribution ownership protections; files changing owner after an install suggest elevation crossed the wrong boundary; an unknown binary suggests provenance loss. First capture `id`, exact path metadata, mount context, executable path, and package ownership query appropriate to the distribution. Never paste credentials into command lines or disable signature checks to bypass a repository problem.

## Practice

**Build:** create a virtual environment in a temporary directory, inspect its interpreter and installation path, and compare them with the system interpreter without installing external packages. **Break:** make one temporary destination read-only and observe the precise failure as your own user; restore it without elevation. **Explain back:** distinguish UID, group, capability, `sudo`, distribution package, language distribution, and virtual environment. Success means no system path changes and every created file is removed.

## Check yourself

1. Why can `sudo pip install` damage both security and package ownership?
2. How do a user name and numeric UID differ?

## Sources

### REQUIRED

- [credentials(7)](https://man7.org/linux/man-pages/man7/credentials.7.html)

### RECOMMENDED

- [capabilities(7)](https://man7.org/linux/man-pages/man7/capabilities.7.html)
- [Python externally managed environments](https://packaging.python.org/en/latest/specifications/externally-managed-environments/)

### DEEP DIVE

- [sudoers(5)](https://www.sudo.ws/docs/man/sudoers.man/)

## Next

Continue to [Linux Networking and Name Resolution](./05-linux-networking-and-name-resolution.md).
