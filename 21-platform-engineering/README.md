# 21 — Platform Engineering

Platform engineering treats shared delivery capabilities as products. Its job is not to centralize every tool, but to make repeated engineering work safer, faster, and economically sustainable without erasing team autonomy.

## What you will learn

- Discover user problems and manage a platform as a product and service.
- Define capability contracts, paved roads, self-service boundaries, and tenant isolation.
- Govern risk, drive voluntary adoption, and measure outcomes and unit economics.

## Lessons

1. [Platforms as products](01-platform-as-product.md)
2. [Paved roads and capability contracts](02-paved-roads.md)
3. [Adoption, governance, and measurement foundations](03-adoption-and-governance.md)
4. [Self-service and tenancy](04-self-service-and-tenancy.md)
5. [Platform operating model and support](05-operating-model-and-support.md)
6. [Policy, exceptions, and deprecation](06-policy-exceptions-and-deprecation.md)
7. [Adoption and organizational change](07-adoption-and-change.md)
8. [Metrics and platform economics](08-metrics-and-economics.md)

## Practice

1. Complete lessons 1 through 7 and write the capability contract, service boundary, tenant model, support path, and exception policy for one researched journey.
2. Run the [platform adoption experiment](lab-platform-adoption-experiment.md). Preserve the baseline, failed and abandoned attempts, segment differences, old-path use, support burden, and the evidence for an expand, narrow, redesign, or stop decision.
3. Complete lesson 8 and its design review. The review must connect the adoption evidence to outcome guardrails, full cost, explicit stop criteria, and a versioned capability decision.
4. Carry the validated problem and contract into the [platform control-plane lab](../labs/14-platform-control-plane/README.md). Do not treat a convergent implementation as proof of product value; it is the system proof that follows the adoption proof.
5. Use both evidence sets to begin milestone 1 of the [Secure Developer Platform Control Plane project](../projects/09-developer-platform-control-plane/README.md). The project is the integration proof, not a substitute for the research or bounded lab.

## Ready to continue

You can defend or reject a platform investment with reproducible user and operational evidence; specify contracts, tenancy, support, and escape hatches; detect coerced or misleading adoption; and hand a validated capability boundary to an implementation team.

## Next

Continue to [Developer Platforms](../22-developer-platforms/README.md).
