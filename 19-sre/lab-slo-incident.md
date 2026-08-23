# Lab: operate an SLO-driven incident

Use a deterministic request stream to calculate burn, trigger an incident, mitigate a bad release, and verify recovery.

## Goal

Produce an executable SLI classifier, multi-window burn calculation, incident decision log, and release guard for a checkout service.

## Before you start

Read lessons 1, 2, 3, and 7. Use Python 3 and temporary CSV files; no services, privileges, network, or cost are required. Predict budget and alert state before each run.

## Establish a baseline

`python3 --version` must show Python 3. Generate 10,000 baseline events with 0.05% bad outcomes and assert the classifier reports about 99.95% good. This establishes healthy SLI semantics.

## Make it work

Set a 99.9% objective. Generate timestamped baseline and version-B events, compute bad-event fraction and burn for five-minute and one-hour windows, and write an incident log containing impact, commander, mitigation, owner, and verification. Add a release gate requiring both windows.

## Break it

Raise version B to 2% bad outcomes. Expected symptoms are concentrated user failure, burn above sustainable rate, and a blocked release. Keep total traffic unchanged so demand is not a competing explanation.

## Diagnose it

Start at the SLI, split by version, inspect the release marker, and mitigate by routing B away. Rerun the same windows. Prove new events recover while the longer window remains elevated; do not declare recovery from an instantaneous green point.

## Clean up

Delete temporary events, scripts, and logs after retaining a redacted exercise record.

## What to keep

Keep predictions, SLI definition, budget math, alert output, incident decisions, disproved hypotheses, and recovery evidence. State the release policy and one action that reduces recurrence rather than only improving detection.

## Sources

- [Google SRE Workbook: Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
