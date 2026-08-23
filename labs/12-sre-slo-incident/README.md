# Lab: Calculate an SLO and Run a Bounded Incident Exercise

Turn a deterministic request dataset into an availability SLI, error budget, burn-rate alerts, incident timeline, and corrective-action review.

## Prerequisites

- Python 3.10 or newer and Bash
- No services, credentials, or network access
- Familiarity with ratios, rolling windows, and incident roles

## Safety

All events are synthetic. Do not mix real customer data into the fixture. The simulation spans 60 minutes and creates 3,600 rows. It sends no pages or external messages.

## Setup and baseline

```bash
mkdir -p .work
python3 - <<'PY' >.work/requests.csv
import csv, random, sys
r=random.Random(20260823)
w=csv.writer(sys.stdout); w.writerow(["second","status","latency_ms"])
for second in range(3600):
    bad = 1800 <= second < 1920
    failure = r.random() < (0.20 if bad else 0.0005)
    w.writerow([second, 503 if failure else 200, 900 if bad else 80+r.randrange(40)])
PY
wc -l .work/requests.csv
sha256sum .work/requests.csv | tee .work/fixture.sha256
```

Define a good request as status below 500 and latency at most 500 ms. Set the 30-day objective to 99.9%. Predict the incident's effect on one-hour compliance.

## Tasks

1. Write `.work/analyze.py` using only the standard library. Compute total, good, bad, SLI, target bad fraction, consumed error budget, and remaining budget.
2. Compute five-minute and one-hour burn rates. Use `observed bad fraction / allowed bad fraction`; document denominator and window.
3. Identify when a hypothetical alert first fires if five-minute burn is above 14 and one-hour burn is above 2. Both conditions must hold.
4. Produce `.work/incident.md` with impact, detection, start/end evidence, incident commander, communications lead, operations lead, mitigations, recovery proof, and unknowns.
5. Write three corrective actions, each with owner role, verification signal, and class: prevent, detect, or mitigate.
6. Explain why one synthetic hour cannot directly establish a 30-day SLO and how missing requests or telemetry loss bias the SLI.

## Evidence to keep

Keep fixture hash, SLI definition, analyzer source, result JSON, burn-rate series, alert timestamp, timeline, decision log, recovery criterion, and post-incident actions. Keep facts distinct from hypotheses.

## Failure injection

The seeded interval from second 1800 through 1919 is the only service fault. Inject a separate monitoring failure by deleting ten rows from a copy, not the canonical fixture. Your analyzer must report non-contiguous seconds or an unexpected count rather than silently calculate a healthy result.

## Cleanup

```bash
rm -rf .work
```

## Rubric

- 2 points: defines an unambiguous good-event SLI and objective
- 3 points: computes budget and multi-window burn rates correctly
- 2 points: detects incomplete telemetry and avoids false confidence
- 2 points: produces a role-based, evidence-timestamped incident record
- 1 point: corrective actions are owned and verifiable

## Sources

- [Google SRE Workbook: alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- [Google SRE Book: managing incidents](https://sre.google/sre-book/managing-incidents/)
- [OpenSLO specification](https://github.com/OpenSLO/OpenSLO)
