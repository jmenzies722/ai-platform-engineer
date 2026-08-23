# Filesystem and Permissions

Linux presents persistent data and many devices through a hierarchical namespace; permissions decide who may traverse and modify it.

## Why it matters

A deployment can create a readable configuration file that the service still cannot open because one parent directory lacks traversal permission. Responding with `chmod -R 777` hides the actual boundary and creates a security defect. The right decision depends on pathname resolution, ownership, and the operation requested on each directory and final inode.

## How it works

Paths are absolute from `/` or relative to a working directory. Directory entries map names to inodes. Owner, group, and other mode bits govern read, write, and execute; directory execute means traversal. `stat` exposes metadata, while `chmod` changes mode bits.

Path resolution starts at `/` for an absolute path or the process working directory for a relative one, then walks directory entries component by component. Names refer to inodes within a mounted filesystem; hard links can give one inode several names, while symbolic links redirect resolution to another pathname. Directory read permission permits listing names, execute permits traversal, and write permits changing entries subject to additional rules. File read and write govern contents; deletion normally depends on the parent directory, not the target file’s write bit. The process umask removes requested mode bits at creation, and ownership or ACLs may refine access. An open descriptor continues to reference an inode even after its last directory name is removed, so storage is reclaimed only when links and open references are gone.

## See it yourself

Predict that `chmod 600` produces `-rw-------` and numeric mode 600 for the file. Also predict that the initial mode can vary with the current umask, which is why the first `stat` is observation rather than a fixed expected number.

```bash
d=$(mktemp -d)
printf 'hello\n' > "$d/note"
stat -c '%A %a %n' "$d/note"
chmod 600 "$d/note"
stat -c '%A %a %n' "$d/note"
rm -rf "$d"
```

Expected observation: The file changes from the mode chosen by `mktemp` and the process umask to owner read/write only.

Limits of the filesystem and permissions observation: The command does not test directory traversal, ACLs, mandatory access controls, mount flags, or the credentials of a service account. Mode bits are one layer of Linux access decisions.

## Where it shows up

Secret mounting in a service is a common production case. A file may be owned by the service and set to 0400, yet a root-owned parent directory set to 0700 prevents traversal. Inspecting every pathname component with the service identity reveals the failing boundary. Changing only the necessary group, directory mode, or deployment ownership preserves least privilege and avoids exposing every secret in the tree.

## When it breaks

`EACCES` suggests a denied permission or policy decision; `ENOENT` can also arise when a component is inaccessible or a symlink target is absent; disk usage that remains after deletion suggests an open unlinked inode. First capture the exact path, operation, effective user and groups, then inspect each component with `namei` or `stat`. For retained storage, inspect same-scope process descriptors before restarting or deleting more files.

## Practice

**Build:** create a temporary directory tree with a file readable only by its owner and record modes for every component. **Break:** remove traversal from the inner directory and predict whether listing, opening by known name, and deletion work; restore it immediately. **Explain back:** distinguish directory entry, inode, pathname, mode, and descriptor. Success is a permission matrix whose observed outcomes match your predictions and a cleanup that removes the entire temporary tree.

## Check yourself

1. Why does write permission on a file differ from permission to delete its name?
2. What does directory execute permit?

## Sources

### REQUIRED

- [path_resolution(7)](https://man7.org/linux/man-pages/man7/path_resolution.7.html)

### RECOMMENDED

- [chmod(2)](https://man7.org/linux/man-pages/man2/chmod.2.html)

### DEEP DIVE

- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html)

## Next

Continue to [Processes, Signals, and Services](./02-processes-signals-and-services.md).
