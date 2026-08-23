# Lab: Build a Tested Streaming Package

Build a dependency-free package that streams integer records, reports line-specific errors, and exposes calculation separately from command-line I/O.

## Create the package

```bash
lab=$(mktemp -d)
mkdir -p "$lab/streamstats"
touch "$lab/streamstats/__init__.py"
cat > "$lab/streamstats/core.py" <<'PY2'
def parse(lines):
    for number, raw in enumerate(lines, 1):
        text = raw.strip()
        if not text:
            continue
        try:
            yield int(text)
        except ValueError as error:
            raise ValueError(f"line {number}: expected integer") from error

def summarize(values):
    count = total = 0
    for value in values:
        count += 1
        total += value
    return {"count": count, "total": total}
PY2
```

Predict when a malformed line raises: package creation, generator creation, or iteration.

## Add a command boundary

```bash
cat > "$lab/streamstats/__main__.py" <<'PY2'
import json, sys
from .core import parse, summarize

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: python -m streamstats FILE", file=sys.stderr)
        return 2
    try:
        with open(argv[0], encoding="utf-8") as source:
            print(json.dumps(summarize(parse(source)), sort_keys=True))
        return 0
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1

raise SystemExit(main())
PY2
printf '2\n3\n5\n' > "$lab/good.txt"
PYTHONPATH="$lab" python3 -m streamstats "$lab/good.txt"
```

Expected observation: the result is `{"count": 3, "total": 10}` and the status is zero.

## Test public behavior

Create `test_streamstats.py` with `unittest` cases for valid input, blank lines, malformed line numbers, an empty iterable, usage status 2, and missing-file status 1. Run:

```bash
cd "$lab"
python3 -m unittest -v
```

Tests should import `streamstats.core` rather than duplicate its logic. For command tests, redirect stdout and stderr and call `main` after moving the final `raise SystemExit(main())` behind an `if __name__ == "__main__":` guard.

## Controlled failures

Run a file containing `1`, `bad`, and `3`. Confirm no success JSON appears, stderr names line 2, and status is 1. Then pass no path and confirm status 2. Explain why these failures have different callers and why broad `except Exception` would hide programming defects.

## Evidence and cleanup

Record the package tree, exact test command, statuses, and one explanation of when generator work executes. Then remove only the disposable workspace:

```bash
cd /
rm -rf "$lab"
```

## Next

Continue to [Iteration, Resources, and Program Boundaries](./06-iteration-resources-and-program-boundaries.md).
