# Lab: operate an SLO-driven incident

Use a deterministic request stream to calculate burn, trigger an incident, mitigate a bad release, and verify recovery.

## Goal

Produce an executable SLI classifier, multi-window burn calculation, incident decision log, and release guard for a checkout service.

## Before you start

Read lessons 1, 2, 3, and 7. Use Python 3 and temporary CSV files; no services, privileges, network, or cost are required. Predict budget and alert state before each run.

## Establish a baseline

`python3 --version` must show Python 3. Create `/tmp/sre-lab/burn.py`:

```bash
mkdir -p /tmp/sre-lab
cat > /tmp/sre-lab/burn.py <<'PY'
from collections import defaultdict

SLO = 0.999

def summarize(events):
    by_version = defaultdict(lambda: [0, 0])
    for version, good in events:
        by_version[version][0] += 1
        by_version[version][1] += not good
    total = sum(v[0] for v in by_version.values())
    bad = sum(v[1] for v in by_version.values())
    ratio = bad / total
    return {"total": total, "bad": bad, "burn": ratio / (1 - SLO), "versions": dict(by_version)}

baseline = [("a", n >= 5) for n in range(10_000)]
report = summarize(baseline)
assert report["bad"] == 5 and round(report["burn"], 1) == 0.5
print("baseline", report)
PY
python3 /tmp/sre-lab/burn.py
```

The five bad events produce 99.95% success and burn rate 0.5. This establishes classifier and budget arithmetic, not alert timing.

## Make it work

Extend the program with two windows and a release gate:

```python
fast = [("a", True)] * 4_950 + [("b", True)] * 4_950 + [("b", False)] * 100
slow = baseline * 5 + fast
fast_report, slow_report = summarize(fast), summarize(slow)
page = fast_report["burn"] > 8 and slow_report["burn"] > 2
print("fast", fast_report)
print("slow", slow_report)
print("release_allowed", not page)
assert page
```

Run it and write `/tmp/sre-lab/incident.md` with UTC declaration time, impact, commander, evidence, mitigation owner, rollback decision, and verification query. The exact thresholds are an exercise policy; production windows and thresholds must be derived from the objective and paging goals.

## Break it

The 100 bad version-B events are the controlled 2% cohort fault. First change them to good and observe the gate stay open; then restore them. Expected symptoms are concentrated user failure, burn above sustainable rate, and a blocked release. Keep total traffic unchanged so demand is not a competing explanation.

## Diagnose it

Start at the aggregate SLI, split `versions`, and inspect the synthetic release marker. Model rollback by replacing `fast` with healthy version-A events, but retain the original `slow` history. New events recover while the long window remains elevated; do not declare recovery from one green point. Add that verification and its output to the decision log.

## Clean up

```bash
rm -rf /tmp/sre-lab
test ! -e /tmp/sre-lab
```

## What to keep

Keep predictions, SLI definition, budget math, alert output, incident decisions, disproved hypotheses, and recovery evidence. State the release policy and one action that reduces recurrence rather than only improving detection.

## Sources

- [Google SRE Workbook: Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
