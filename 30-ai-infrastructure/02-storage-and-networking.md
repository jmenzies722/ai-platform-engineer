# Storage and networking

AI workloads depend on data paths that can sustain large sequential reads, many small objects, checkpoints, and synchronized communication.

## Why it matters

An accelerator waiting for bytes is costly idle capacity, regardless of its theoretical throughput.

## How it works

Object storage provides durable scale; local NVMe provides fast ephemeral caching; distributed filesystems offer shared semantics at operational cost. Sharding and prefetching increase sequential access. Checksums protect artifacts. Network design separates bulk data, collective traffic, and control paths while accounting for oversubscription and locality.

The right path follows access pattern and failure semantics. Immutable shards make parallel reads and cache identity simple; many tiny files amplify metadata round trips. Prefetch overlaps I/O with compute but consumes memory and can fetch unused data. Checkpoints need atomic publication: write a unique object, verify it, then publish a manifest last.

## See it yourself

A job consuming 256 examples of 1 MiB each at four steps per second needs at least 1 GiB/s of useful reads. If decoding adds 25% overhead and cache hit rate is 60%, estimate source bandwidth separately from local bandwidth. Measure achieved step stalls; meeting nominal link bandwidth does not prove the parser or metadata path can feed the job.

## Where it shows up

At job start, workers fetch an immutable dataset manifest, populate node-local shards with checksum verification, and reuse them across runs. A per-node cache avoids every worker stampeding object storage. The manifest preserves reproducibility while local NVMe supplies speed; losing the node only removes a reconstructible copy.

## When it breaks

Small-file metadata storms, synchronized checkpoints, cache stampedes, and cross-zone traffic saturate shared paths. First separate time spent opening, reading, decoding, waiting, and transferring by worker and storage tier. Correlated stalls at checkpoint boundaries suggest synchronization; low bytes with high operations suggests metadata pressure; one zone differing suggests locality.

## Practice

**Build:** design a cache keyed by immutable dataset digest with checksum, eviction, and miss metrics. **Break:** launch simultaneous cold readers and corrupt one shard; prove single-flight loading and validation work. **Explain back:** calculate the bandwidth budget and state which storage copies are durable versus reconstructible.

## Check yourself

1. Why shard datasets?
2. What belongs in a cache key?
3. When is local storage unsafe?

## Sources

### REQUIRED

- [Kubernetes storage concepts](https://kubernetes.io/docs/concepts/storage/)

### RECOMMENDED

- [Amazon S3 consistency model](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html#ConsistencyModel)

### DEEP DIVE

- [GPUDirect RDMA](https://docs.nvidia.com/cuda/gpudirect-rdma/)

## Next

Continue to [Reliable distributed jobs](03-reliable-distributed-jobs.md).
