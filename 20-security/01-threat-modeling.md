# Threat modeling and trust boundaries

Threat modeling turns an architecture into explicit security decisions: what matters, who can act, where trust changes, how abuse succeeds, and which controls reduce credible harm.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Define scope, assets, actors, entry points, data flows, trust boundaries, dependencies, assumptions, and abuse cases. STRIDE is a prompt, not a scoring algorithm. Rank scenarios by plausible impact, exploitability, exposure, and existing controls; name owner and residual risk.

Model users, administrators, workloads, CI, vendors, and control planes. Controls can prevent, detect, limit, or recover. Revisit the model when data, authority, code provenance, or boundaries change.

## See it yourself

A service behind a firewall still crosses boundaries when CI publishes code or an administrator changes policy. If either identity can write the production artifact, the internet boundary is not the only path to asset compromise; tracing authority proves the hidden boundary.

## Where it shows up

For file upload, trace bytes through edge, scanner, object store, parser, and download. Decide what happens when scanning is unavailable and where content first becomes trusted.

## When it breaks

Diagrams can omit control planes, risk matrices can imply fake precision, and teams can list threats without decisions. Validate flows against deployed routes and identities; test the highest-risk assumptions.

## Practice

Threat-model password reset with assets, flows, five abuse cases, controls, evidence, and residual risk. Break the model by adding a support-admin path. Completion means the new authority appears in flows and changes at least one decision.

## Check yourself

1. What creates a meaningful trust boundary?
2. Why include CI and administrators as actors?
3. How does a recovery control differ from prevention?
4. Which assumption in your model is most dangerous if false?

## Sources

### REQUIRED

- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)

### RECOMMENDED

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)

### DEEP DIVE

- [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/)

## Next

[Identity, authentication, and authorization](02-identity-and-access.md)
