# Storage, Filesystems, and Durable I/O

Storage is a hierarchy of volatile buffers, kernel caches, device controllers, media, and filesystem metadata. “The write succeeded” names only one point in that path.

## Why it matters

A service can acknowledge a transaction after copying bytes into a process or kernel buffer and lose it when power fails. Conversely, forcing every tiny write to stable media can destroy throughput. Correct design identifies which data must survive which failures and pays the synchronization cost at an explicit commit boundary.

## How it works

Block devices expose addressable sectors or logical blocks; filesystems organize those blocks into files, directories, allocation metadata, and recovery structures. Applications use descriptors and byte offsets, while the kernel page cache commonly satisfies reads and absorbs writes. A successful `write` normally means bytes were accepted by the kernel, not that storage media committed them. Language-level `flush` pushes runtime buffers toward the kernel. `fsync` requests synchronization of a file’s data and required metadata, subject to operating-system and device contracts.

Filesystems use techniques such as journaling or copy-on-write to recover metadata consistency, but consistency is not identical to application atomicity or data durability. Rename within one filesystem is an atomic namespace operation for observers; a robust replacement pattern writes a temporary file, flushes and synchronizes it as required, renames it, and may synchronize the containing directory so the name change survives. RAID, snapshots, and replication address availability or recovery dimensions but are not substitutes for tested backups. SSDs and disks have different latency and endurance behavior, while access patterns, queueing, and write amplification affect both.

## See it yourself

**Tiny Proof:** predict that data becomes visible through the pathname after atomic replacement and that no reader sees the temporary name as the final name.

```bash
d=$(mktemp -d)
printf 'old\n' > "$d/state"
python3 - "$d" <<'PY2'
import os, pathlib, sys
directory = pathlib.Path(sys.argv[1])
temporary = directory / ".state.tmp"
with temporary.open("w", encoding="utf-8") as output:
    output.write("new\n")
    output.flush()
    os.fsync(output.fileno())
os.replace(temporary, directory / "state")
PY2
cat "$d/state"
rm -rf "$d"
```

Expected observation: `state` contains `new` after replacement.

Limits of this proof: it does not simulate a crash, synchronize the directory, certify the device’s power-loss behavior, or prove cross-filesystem atomicity. Visibility after normal execution is weaker than durability.

## Where it shows up

Database systems group log records and synchronize them at transaction commit, often batching several transactions to amortize device latency. Acknowledgment policy determines the failure window. Application code that writes configuration directly in place risks leaving truncation or mixed content after interruption; temporary write and atomic replacement narrows that window. Backups must then be restored in drills, because successful creation does not prove usable recovery.

## When it breaks

Truncated files suggest interrupted in-place writes; acknowledged but missing records suggest a durability-contract gap; growing I/O latency with queue depth suggests saturation; filesystem-full errors may involve data blocks, inodes, quotas, or deleted-but-open files. First preserve exact errors, mount and filesystem identity, free-space and inode evidence, device latency, and the application’s flush or commit sequence. Avoid destructive repair until a backup and filesystem-specific procedure are established.

## Practice

**Build:** implement atomic replacement of a small state file with explicit flush, file synchronization, rename, and documented directory-sync policy. **Break:** inject exceptions before write, before rename, and after rename, then classify visible states. **Explain back:** separate runtime buffering, page cache, filesystem metadata, device cache, atomicity, durability, and backup. Success means every injection leaves either old or complete new content and the claims do not exceed the tested failure model.

## Check yourself

1. What does a successful `write` usually guarantee?
2. Why are filesystem consistency, atomic replacement, and durability different properties?

## Sources

### REQUIRED

- [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html)

### RECOMMENDED

- [rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html)

### DEEP DIVE

- [File Systems: Crash Consistency](https://pages.cs.wisc.edu/~remzi/OSTEP/file-journaling.pdf)

## Next

Continue to [Linux](../04-linux/README.md).
