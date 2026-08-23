# Lab: build an evidence-preserving delivery path

Model a delivery pipeline locally with shell tools and a tiny static artifact. The lab separates build, promotion, deployment, and release; it deliberately triggers a policy failure and recovery without needing cloud credentials.

## Safety and prerequisites

Use a disposable directory and do not load real signing keys or deployment credentials. Required tools are a POSIX shell, `git`, `sha256sum`, and `python3`. Commands create files only under `/tmp/curriculum-delivery`.

## Establish intent and source

```bash
rm -rf /tmp/curriculum-delivery
mkdir -p /tmp/curriculum-delivery/{source,registry,env}
cd /tmp/curriculum-delivery/source
git init
git config user.name curriculum
git config user.email curriculum@example.invalid
printf '{"message":"version one"}\n' > app.json
git add app.json
git commit -m 'add version one'
git rev-parse HEAD
```

Record the source commit and predict the artifact digest. Treat the commit as reviewed intent for this lab, not proof of authorship or secure review.

## Build once and preserve evidence

```bash
commit=$(git rev-parse HEAD)
python3 -m json.tool app.json >/tmp/curriculum-delivery/test-output.txt
cp app.json /tmp/curriculum-delivery/registry/app.json
digest=$(sha256sum /tmp/curriculum-delivery/registry/app.json | cut -d' ' -f1)
printf 'source=%s\nartifact_sha256=%s\ntest=json-parse-pass\nbuilder=local-lab\n' \
  "$commit" "$digest" >/tmp/curriculum-delivery/registry/evidence.txt
sha256sum /tmp/curriculum-delivery/registry/app.json
```

Inspect `evidence.txt`. The digest proves byte identity; the unsigned text does not prove builder identity. In production this record would be authenticated provenance plus test and SBOM attestations from an isolated builder.

## Promote without rebuilding

```bash
cp /tmp/curriculum-delivery/registry/evidence.txt /tmp/curriculum-delivery/env/staging.approval
cp /tmp/curriculum-delivery/registry/app.json /tmp/curriculum-delivery/env/staging.json
test "$(sha256sum /tmp/curriculum-delivery/env/staging.json | cut -d' ' -f1)" = "$digest"
```

Promotion copied immutable bytes and approval evidence. A real registry should reference the existing digest rather than copy arbitrary local files.

## Release and verify production behavior

```bash
cp /tmp/curriculum-delivery/env/staging.json /tmp/curriculum-delivery/env/production.json
python3 -c 'import json; assert json.load(open("/tmp/curriculum-delivery/env/production.json"))["message"] == "version one"'
printf 'artifact_sha256=%s\nreleased_cohort=100%%\nverification=message-v1-pass\n' \
  "$digest" >/tmp/curriculum-delivery/env/deployment-record.txt
```

Deployment places bytes; release identifies exposure; verification checks a user-visible assertion. State what this synthetic assertion misses.

## Trigger a supply-chain gate

Tamper with staging after approval:

```bash
printf '{"message":"tampered"}\n' >/tmp/curriculum-delivery/env/staging.json
actual=$(sha256sum /tmp/curriculum-delivery/env/staging.json | cut -d' ' -f1)
test "$actual" = "$digest"
```

The command must fail. Preserve expected digest, actual digest, source commit, and timestamp. Do not promote. Explain why reparsing JSON or scanning vulnerabilities would not detect this identity violation.

## Recover from a failed release guardrail

Create version two through source, rebuild it as a new artifact, and model a canary decision:

```bash
cd /tmp/curriculum-delivery/source
printf '{"message":"version two","error_rate":0.25}\n' > app.json
git add app.json
git commit -m 'add risky version two'
cp app.json /tmp/curriculum-delivery/registry/app-v2.json
v2digest=$(sha256sum /tmp/curriculum-delivery/registry/app-v2.json | cut -d' ' -f1)
python3 -c 'import json; d=json.load(open("/tmp/curriculum-delivery/registry/app-v2.json")); raise SystemExit(d["error_rate"] > 0.05)'
```

The guardrail exits nonzero, so version two must not replace production. Verify `production.json` still has version one and its digest matches the deployment record. This is rollback by retained artifact and controlled exposure; a one-way data migration would require a different roll-forward plan.

## Delivery review

Produce a value-stream and trust-boundary table with stage, input, immutable output, elapsed time, active work, credential, untrusted code, policy, failure evidence, owner, and recovery. Answer:

1. Where could a mutable reference enter?
2. Which job could safely process an untrusted pull request?
3. Which identity may publish, promote, deploy, and release?
4. What evidence links production to source and configuration?
5. Which change risks require human judgment?

## Completion criteria

The lab passes when a reviewer can independently verify the production digest, reproduce the policy denial, see that version one remained available after the failed guardrail, and identify how short-lived credentials, authenticated provenance, isolated builds, registry retention, and an exception-expiry process would replace the local simplifications.

## Cleanup

```bash
rm -rf /tmp/curriculum-delivery
```
