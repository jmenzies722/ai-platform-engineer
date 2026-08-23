# OCI images and reproducible builds

An OCI image is a content-addressed manifest and ordered filesystem layers plus runtime configuration.

## Why it matters

Image contents become production dependencies. Unpinned bases, unnecessary tools, leaked build secrets, and mutable tags make behavior hard to reproduce and expand the attack surface.

## How it works

Each Dockerfile instruction can produce a cached layer. Deletions in later layers hide bytes but do not remove them from earlier layers. Multi-stage builds compile in a tool-rich stage and copy only runtime artifacts into a smaller final stage.

Registries store blobs and manifests by digest. Tags are convenient mutable pointers; deployment by digest identifies exact content. A reproducible build controls inputs, versions, timestamps, and network access, then records provenance and an SBOM.

## See it yourself

Use `docker history IMAGE` and `docker image inspect IMAGE`. Compare a tag with its `RepoDigests`. Build once after changing only a late source file and observe which layers are reused.

## Where it shows up

BuildKit caches dependency layers, registries distribute images, scanners inspect packages, and admission policy can require signatures or provenance.

## When it breaks

Copying the whole repository before dependency installation invalidates cache. Secrets passed with `ARG` can remain in metadata or layers. `latest` changes underneath deployments. An image built for the wrong CPU architecture fails at runtime.

## Practice

Write a multi-stage Dockerfile for a compiled or packaged application. Pin the base, use a non-root user, copy only runtime files, and compare final size and package list.

## Check yourself

1. Why does deleting a secret in a later layer not erase it?
2. What identity remains stable when a tag moves?

## Sources

### REQUIRED
- [OCI image specification](https://github.com/opencontainers/image-spec)

### RECOMMENDED
- [Docker build best practices](https://docs.docker.com/build/building/best-practices/)

### DEEP DIVE
- [SLSA specification](https://slsa.dev/spec/v1.0/)

## Next

[Runtime networking, storage, and security](03-runtime-operations.md)
