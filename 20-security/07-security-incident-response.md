# Security detection and incident response

Security response must contain adversary capability while preserving evidence and business function. The plan is built before compromise through logging, access, decision authority, exercises, and clean recovery paths.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Prepare asset and identity inventories, forensic-quality time, protected logs, contacts, playbooks, clean credentials, and recovery images. During an event, validate, scope, contain, eradicate, recover, and learn; phases overlap. Track confidence and chain of custody.

Containment choices affect evidence and attacker awareness. Isolate rather than casually power off when memory matters; revoke compromised sessions and rotate credentials from a clean environment; preserve snapshots and logs under controlled access. Recovery requires removing persistence and closing initial access before restoring trust.

## See it yourself

Rotating one leaked key does not contain an attacker who used it to create a new identity. The authority graph must be traversed from original capability to every derived session, role, artifact, and persistence mechanism.

## Where it shows up

Playbooks should cover credential theft, malicious dependency, cloud account compromise, data exfiltration, and ransomware. Define severity, legal and privacy escalation, customer communication authority, and recovery criteria.

## When it breaks

Attackers can delete local logs, responders can destroy volatile evidence, premature public claims can outrun facts, and restoring contaminated artifacts can reinfect systems. Use independent log sinks, evidence hashes, decision records, and clean-room rebuilds.

## Practice

Tabletop a stolen CI credential that published a signed malicious image. Scope derived artifacts and identities, choose containment, and define clean recovery. Completion means provenance identifies affected releases, revocation covers derived access, evidence is preserved, and users receive fact-based updates.

## Check yourself

1. Why can credential rotation fail to contain compromise?
2. When is isolation safer than shutdown?
3. What proves an artifact is safe to restore?
4. Which evidence must exist before the incident?

## Sources

### REQUIRED

- [NIST SP 800-61 Rev. 2](https://csrc.nist.gov/pubs/sp/800/61/r2/final)

### RECOMMENDED

- [CISA Incident Response Playbooks](https://www.cisa.gov/news-events/news/federal-government-cybersecurity-incident-and-vulnerability-response-playbooks)

### DEEP DIVE

- [MITRE ATT&CK](https://attack.mitre.org/)

## Next

[Platform Engineering](../21-platform-engineering/README.md)
