# Virtual Memory and Address Translation

Virtual memory gives each process an address space whose pages can map to physical memory, files, shared regions, or nothing at all.

## Why it matters

A process with a 20 GB virtual size may use little physical memory, while a process with moderate resident memory can still be killed under a cgroup limit. Treating virtual, resident, shared, and committed memory as one number leads to false leak diagnoses and unsafe capacity decisions.

## How it works

The processor issues virtual addresses. Page tables maintained under operating-system control translate virtual page numbers to physical frames and attach permissions such as readable, writable, executable, and user-accessible. A translation lookaside buffer caches recent translations. If translation is absent or disallowed, a page fault transfers control to the kernel. The kernel may allocate a zero-filled page, load file-backed data, perform copy-on-write, reject the access, or wait for storage.

Mappings reserve ranges with properties; reservation does not mean every page is resident. Anonymous mappings hold process data, while file-backed mappings connect pages to file content. After `fork`, copy-on-write lets parent and child initially share physical pages until a writer needs a private copy. Shared libraries and page cache complicate attribution: summing process RSS can double-count shared pages. Swap can preserve infrequently used pages at high latency. Allocators obtain regions and manage smaller objects internally, so freeing a language object need not immediately reduce process RSS.

## See it yourself

**Tiny Proof:** predict several regions with different permissions and sources, including executable code, heap or anonymous data, shared libraries, and stack.

```bash
python3 - <<'PY2'
import os
print("pid", os.getpid())
with open("/proc/self/maps", encoding="utf-8") as mappings:
    for _, line in zip(range(12), mappings):
        print(line, end="")
PY2
```

Expected observation: address ranges are virtual, permissions vary, and some mappings name files while others use labels or no pathname.

Limits of this proof: `/proc/self/maps` is a snapshot, does not list physical addresses, and does not prove each mapped page is resident. Container permissions and non-Linux systems differ.

## Where it shows up

Copy-on-write workers preload application code and then fork, allowing clean pages to remain shared. Mutating large preloaded structures makes pages private and can erase the expected memory saving. Measuring proportional set size and per-mapping dirty pages before and after representative traffic can test that explanation. Another common case is memory-mapped file access: page faults load data on demand, so a fast `mmap` call does not mean the whole file is in memory.

## When it breaks

A segmentation fault indicates an invalid or disallowed memory access in native execution; rising anonymous private memory suggests allocations or fragmentation; major faults with latency suggest storage-backed paging; an out-of-memory kill reflects system or cgroup policy, not a catchable allocation exception. First identify the exact process and limit, then capture mappings, RSS categories, fault counters, and workload. Avoid claiming a leak from one rising sample; retention requires repeated evidence and object or allocation attribution.

## Practice

**Build:** allocate and touch anonymous memory in controlled increments while sampling `/proc/self/status` and fault counts. **Break:** reserve more virtual space than you touch, then compare virtual and resident measurements without exhausting the host. **Explain back:** distinguish mapping, page, frame, fault, RSS, and allocator object. Success includes strict allocation bounds, before-and-after samples, cleanup, and no claim that the experiment reveals physical addresses.

## Check yourself

1. Why can mapped virtual space exceed resident physical memory?
2. What does copy-on-write defer, and what event ends sharing?

## Sources

### REQUIRED

- [proc_pid_maps(5)](https://man7.org/linux/man-pages/man5/proc_pid_maps.5.html)

### RECOMMENDED

- [mmap(2)](https://man7.org/linux/man-pages/man2/mmap.2.html)

### DEEP DIVE

- [What Every Programmer Should Know About Memory](https://www.akkadia.org/drepper/cpumemory.pdf)

## Next

Continue to [Storage, Filesystems, and Durable I/O](./06-storage-filesystems-and-durable-io.md).
