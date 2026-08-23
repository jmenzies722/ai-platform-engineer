# 03 — Computer Systems

Connect representation and machine instructions to the layered system that actually runs a program. The sequence follows execution through caches, privilege boundaries, virtual memory, and durable storage so that performance and failure symptoms have a concrete home.

## What you will learn

By the end, you can decode common representations, distinguish bytecode from machine instructions, reason about locality, explain user and kernel mode, read a process memory map, follow buffered I/O toward storage, and select measurements that support rather than merely decorate a systems claim.

## Lessons

1. [Bits, Bytes, and Representation](./01-bits-bytes-and-representation.md)
2. [Instructions, CPU, and Memory](./02-instructions-cpu-and-memory.md)
3. [Caches, Locality, and Measurement](./03-caches-locality-and-measurement.md)
4. [System Calls, Interrupts, and Privilege](./04-system-calls-interrupts-and-privilege.md)
5. [Virtual Memory and Address Translation](./05-virtual-memory-and-address-translation.md)
6. [Storage, Filesystems, and Durable I/O](./06-storage-filesystems-and-durable-io.md)

## Practice

Run each lesson’s bounded proof, then complete [Follow One Program Through the System](./lab-follow-one-program.md). The lab joins executable identity, mappings, descriptors, syscall evidence, and write visibility in one disposable run.

Practice is part of the path, not an optional recap. Predict first, work only in disposable or explicitly scoped resources, compare expected and actual observations, and perform the documented cleanup.

## Ready to continue

Continue when you can explain one byte’s meaning from schema to storage, identify which instruction stream the processor executes, separate cache claims from timing, distinguish library calls from system calls, explain why a virtual address is not a physical location, and state what `write`, `flush`, and durable commit each guarantee.

## Next

Start with [Bits, Bytes, and Representation](./01-bits-bytes-and-representation.md).
