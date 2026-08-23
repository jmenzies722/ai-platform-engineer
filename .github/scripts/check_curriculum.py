#!/usr/bin/env python3
"""Validate the repository's lean lesson contract and Markdown links."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LESSON_HEADINGS = [
    "## Why it matters",
    "## How it works",
    "## See it yourself",
    "## Where it shows up",
    "## When it breaks",
    "## Practice",
    "## Check yourself",
    "## Sources",
    "## Next",
]
MODULE_HEADINGS = [
    "## What you will learn",
    "## Lessons",
    "## Practice",
    "## Ready to continue",
    "## Next",
]
ROOT_DOCS = [
    "README.md",
    "START-HERE.md",
    "HOW-TO-LEARN.md",
    "CONCEPT-INDEX.md",
    "TEACH-BACK.md",
    "CURRICULUM.md",
    "ROADMAP.md",
    "PROGRESS.md",
    "GLOSSARY.md",
    "REFERENCES.md",
    "INTERVIEW-MAP.md",
    "PROJECTS.md",
    "templates/LESSON.md",
]
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^```mermaid\s*$([\s\S]*?)^```\s*$", re.MULTILINE)

errors: list[str] = []


def fail(path: Path | str, message: str) -> None:
    errors.append(f"{path}: {message}")


def ordered_headings(path: Path, text: str, headings: list[str]) -> None:
    previous = -1
    lines = text.splitlines()
    for heading in headings:
        try:
            position = lines.index(heading)
        except ValueError:
            fail(path.relative_to(ROOT), f"missing heading {heading!r}")
            continue
        if position <= previous:
            fail(path.relative_to(ROOT), f"heading out of order: {heading!r}")
        previous = position


def check_lesson(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)
    ordered_headings(path, text, LESSON_HEADINGS)

    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        fail(rel, "lesson must begin with one H1 title")
    first_section = next((i for i, line in enumerate(lines) if line.startswith("## ")), 0)
    opening = " ".join(line.strip() for line in lines[1:first_section] if line.strip())
    if len(opening.split()) < 8:
        fail(rel, "add a useful opening paragraph before the first section")

    for source_heading in ("### REQUIRED", "### RECOMMENDED", "### DEEP DIVE"):
        if source_heading not in lines:
            fail(rel, f"missing source tier {source_heading!r}")

    next_match = re.search(r"^## Next\s*$([\s\S]*)", text, re.MULTILINE)
    next_links = (
        re.findall(r"\[[^\]]+\]\([^)]+\.md(?:#[^)]+)?\)", next_match.group(1))
        if next_match
        else []
    )
    if len(next_links) != 1:
        fail(rel, f"Next must contain exactly one linked Markdown file; found {len(next_links)}")


def check_mermaid(path: Path, text: str) -> None:
    rel = path.relative_to(ROOT)
    starts = len(re.findall(r"^```mermaid\s*$", text, re.MULTILINE))
    blocks = FENCE_RE.findall(text)
    if starts != len(blocks):
        fail(rel, "Mermaid fence is not closed or has text after the language name")
    for index, block in enumerate(blocks, start=1):
        first = next((line.strip() for line in block.splitlines() if line.strip()), "")
        if not re.match(r"^(flowchart|sequenceDiagram|stateDiagram-v2)\b", first):
            fail(rel, f"Mermaid block {index} uses an unsupported or missing diagram type")
        if "\t" in block:
            fail(rel, f"Mermaid block {index} contains a tab")
        if any(mark in block for mark in ("“", "”", "‘", "’")):
            fail(rel, f"Mermaid block {index} contains smart quotes")
        if re.search(r"<[^>]+>", block):
            fail(rel, f"Mermaid block {index} contains HTML")


def check_links(path: Path, text: str) -> None:
    rel = path.relative_to(ROOT)
    for raw_target in LINK_RE.findall(text):
        target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
        if (
            not target
            or target.startswith(("#", "http://", "https://", "mailto:"))
            or "://" in target
        ):
            continue
        file_part, separator, fragment = target.partition("#")
        linked_path = (path.parent / file_part).resolve() if file_part else path
        if file_part and not linked_path.exists():
            fail(rel, f"broken local link: {raw_target}")
            continue
        if separator and linked_path.is_file() and linked_path.suffix.lower() == ".md":
            linked_text = linked_path.read_text(encoding="utf-8")
            slugs: set[str] = set()
            counts: dict[str, int] = {}
            for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", linked_text, re.MULTILINE):
                plain = re.sub(r"[`*_~]", "", heading).lower()
                base = re.sub(r"[^\w\- ]", "", plain, flags=re.UNICODE)
                base = re.sub(r"[\s\-]+", "-", base).strip("-")
                count = counts.get(base, 0)
                counts[base] = count + 1
                slugs.add(base if count == 0 else f"{base}-{count}")
            if fragment.lower() not in slugs:
                fail(rel, f"broken local heading link: {raw_target}")


for root_doc in ROOT_DOCS:
    path = ROOT / root_doc
    if not path.is_file() or path.stat().st_size == 0:
        fail(root_doc, "missing or empty required document")

module_dirs: list[Path] = []
for number in range(36):
    matches = sorted(ROOT.glob(f"{number:02d}-*"))
    matches = [path for path in matches if path.is_dir()]
    if len(matches) != 1:
        fail(f"module {number:02d}", f"expected one module directory, found {len(matches)}")
        continue
    module = matches[0]
    module_dirs.append(module)
    readme = module / "README.md"
    if not readme.is_file():
        fail(readme.relative_to(ROOT), "missing module README")
        continue
    ordered_headings(readme, readme.read_text(encoding="utf-8"), MODULE_HEADINGS)
    lessons = sorted(
        path
        for path in module.glob("[0-9][0-9]-*.md")
        if "lab" not in path.stem.lower()
    )
    minimum = 20 if number == 0 else 2
    if len(lessons) < minimum:
        fail(module.relative_to(ROOT), f"needs at least {minimum} real lessons; found {len(lessons)}")
    for lesson in lessons:
        check_lesson(lesson)

markdown_files = sorted(ROOT.glob("*.md"))
markdown_files += sorted((ROOT / "templates").glob("*.md"))
for directory in module_dirs + [ROOT / "labs", ROOT / "incidents"]:
    if directory.exists():
        markdown_files += sorted(directory.rglob("*.md"))

for path in set(markdown_files):
    text = path.read_text(encoding="utf-8")
    if "→" in text or "⇒" in text:
        fail(path.relative_to(ROOT), "contains arrow-chain glyph; write prose or use Mermaid")
    if "Visual Model" in text:
        fail(path.relative_to(ROOT), "contains a Visual Model placeholder")
    check_mermaid(path, text)
    check_links(path, text)

if errors:
    print("Curriculum validation failed:", file=sys.stderr)
    for error in sorted(set(errors)):
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

lesson_count = sum(
    1
    for module in module_dirs
    for path in module.glob("[0-9][0-9]-*.md")
    if "lab" not in path.stem.lower()
)
print(f"Validated {len(module_dirs)} modules and {lesson_count} lessons.")
