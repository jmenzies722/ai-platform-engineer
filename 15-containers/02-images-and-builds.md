# OCI images and reproducible builds

An OCI image is a content-addressed manifest and ordered filesystem layers plus runtime configuration.

## Why it matters

Image contents become production dependencies. Unpinned bases, unnecessary tools, leaked build secrets, and mutable tags make behavior hard to reproduce and expand the attack surface.

## How it works

Each Dockerfile instruction can produce a cached layer. Deletions in later layers hide bytes but do not remove them from earlier layers. Multi-stage builds compile in a tool-rich stage and copy only runtime artifacts into a smaller final stage.

Registries store blobs and manifests by digest. Tags are convenient mutable pointers; deployment by digest identifies exact content. A reproducible build controls inputs, versions, timestamps, and network access, then records provenance and an SBOM.

An image index can select manifests by architecture and operating system. Each manifest references configuration and compressed layers by digest. The runtime overlays layers and adds a writable layer, but image history is not a complete or trustworthy build recipe.

Use a narrow build context and `.dockerignore`, lock dependencies with integrity checks, order stable dependency steps before changing source, and use BuildKit secret mounts for ephemeral access. Set a non-root runtime user. Rebuilding from one Dockerfile still depends on builder, platform, base digest, network inputs, and timestamps.

## See it yourself

Use `docker history`, `docker image inspect`, and a manifest inspection tool. Compare a mutable tag with `RepoDigests`, platform manifests, config, and layer digests. Build twice, change only a late source file, and observe cache reuse and final digest. Equal digests support reproducibility for those runs; they do not prove the source was safe.

## Where it shows up

BuildKit caches dependency layers, registries distribute images, scanners inspect packages, and admission policy can require digest identity, signatures, provenance, and approved base lineage. A release record carries image digest and runtime configuration because identical bytes can run with different authority.

## When it breaks

Copying the repository before dependency installation invalidates cache. Secrets passed with `ARG`, `ENV`, or copied files remain in metadata or lower layers despite later deletion. `latest` changes underneath deployments. A wrong CPU architecture fails or uses slow emulation. Package indexes change, caches cross trust boundaries, and a tiny image can still contain a vulnerable static binary.

Investigate build context, base and dependency digests, builder identity, network inputs, cache source, image config, SBOM, provenance subject, registry audit events, and deployed digest.

## Practice

**Observe:** inventory one image's manifest, platform, config, layers, packages, provenance, signatures, and runtime user.

**Build:** write a multi-stage Dockerfile. Pin the base digest, lock dependencies, use secret mounts, run non-root, copy only runtime files, and compare size, package list, and repeated-build digest.

**Break safely:** leak a fake token in an early layer, move a local tag, and target the wrong platform. Completion means each problem is detected without deploying it and the repaired build emits traceable immutable output.

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
