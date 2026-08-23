#!/usr/bin/env python3
"""Render every Mermaid block with the same CLI used by GitHub tooling."""

from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FENCE_RE = re.compile(r"^```mermaid\s*$([\s\S]*?)^```\s*$", re.MULTILINE)


def main() -> None:
    diagrams: list[tuple[Path, int, str]] = []
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        diagrams.extend(
            (path.relative_to(ROOT), index, block.strip() + "\n")
            for index, block in enumerate(FENCE_RE.findall(text), start=1)
        )

    with tempfile.TemporaryDirectory(prefix="curriculum-mermaid-") as raw_directory:
        directory = Path(raw_directory)
        for sequence, (path, index, diagram) in enumerate(diagrams, start=1):
            source = directory / f"{sequence:04d}.mmd"
            output = directory / f"{sequence:04d}.svg"
            source.write_text(diagram, encoding="utf-8")
            result = subprocess.run(
                [
                    "npx",
                    "--yes",
                    "@mermaid-js/mermaid-cli@latest",
                    "--input",
                    str(source),
                    "--output",
                    str(output),
                    "--quiet",
                ],
                text=True,
                capture_output=True,
            )
            if result.returncode:
                detail = (result.stderr or result.stdout).strip()
                raise SystemExit(f"{path}: Mermaid block {index} failed to render\n{detail}")

    print(f"Rendered {len(diagrams)} Mermaid diagrams.")


if __name__ == "__main__":
    main()
