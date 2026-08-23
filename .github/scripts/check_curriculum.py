#!/usr/bin/env python3
"""Validate the curriculum contract, experience inventory, and Markdown links."""

from __future__ import annotations

import re
import sys
import unicodedata
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
    "CONTRIBUTING.md",
    "QUALITY.md",
    "templates/LESSON.md",
]
MINIMUM_LESSONS = {
    **{number: 6 for number in range(1, 21)},
    **{number: 8 for number in range(21, 34)},
    34: 13,
    35: 14,
}
REQUIRED_CHEATSHEETS = {
    "linux.md",
    "git.md",
    "networking.md",
    "kubernetes.md",
    "aws.md",
    "opentelemetry.md",
}
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SYSTEM_SPECS: dict[str, tuple[int, tuple[str, ...]]] = {
    "tracks/README.md": (250, ("## Available tracks", "## Evidence-based placement", "## Switching tracks", "## How to use a track", "## Certification overlays")),
    "tracks/software-engineer.md": (300, ("## Outcome role", "## Prerequisites", "## Ordered module path", "## Required practice", "## Competency gates", "## Certification overlays")),
    "tracks/backend-engineer.md": (300, ("## Outcome role", "## Prerequisites", "## Ordered module path", "## Required practice", "## Competency gates", "## Certification overlays")),
    "tracks/cloud-devops-engineer.md": (300, ("## Outcome role", "## Prerequisites", "## Ordered module path", "## Required practice", "## Competency gates", "## Certification overlays")),
    "tracks/sre.md": (300, ("## Outcome role", "## Prerequisites", "## Ordered module path", "## Required practice", "## Competency gates", "## Certification overlays")),
    "tracks/platform-engineer.md": (300, ("## Outcome role", "## Prerequisites", "## Ordered module path", "## Required practice", "## Competency gates", "## Certification overlays")),
    "tracks/ai-platform-engineer.md": (300, ("## Outcome role", "## Prerequisites", "## Ordered module path", "## Required practice", "## Competency gates", "## Certification overlays")),
    "tracks/staff-ai-platform-engineer.md": (300, ("## Outcome role", "## Prerequisites", "## Ordered module path", "## Required practice", "## Competency gates", "## Certification overlays")),
    "assessments/README.md": (500, ("## Gate sequence", "## Roles", "## Standard assessment flow", "## Standard evidence packet", "## Evidence reuse", "## Integrity and safety", "## Outcomes")),
    "assessments/rubric.md": (700, ("## Scoring scale", "## Dimension anchors", "## Evidence quality", "## Integrity and safety conditions", "## Evaluator procedure", "## Pass and rework", "## Assessment record")),
    "assessments/gates/foundations.md": (700, ("## Prerequisites", "## Challenge", "## Evidence packet", "## Dimension requirements", "## Evaluator instructions", "## Review prompts", "## Pass and rework", "## Remediation")),
    "assessments/gates/systems-linux-networking.md": (700, ("## Prerequisites", "## Challenge", "## Evidence packet", "## Dimension requirements", "## Evaluator instructions", "## Review prompts", "## Pass and rework", "## Remediation")),
    "assessments/gates/cloud-delivery.md": (700, ("## Prerequisites", "## Challenge", "## Evidence packet", "## Dimension requirements", "## Evaluator instructions", "## Review prompts", "## Pass and rework", "## Remediation")),
    "assessments/gates/kubernetes-reliability.md": (700, ("## Prerequisites", "## Challenge", "## Evidence packet", "## Dimension requirements", "## Evaluator instructions", "## Review prompts", "## Pass and rework", "## Remediation")),
    "assessments/gates/platform.md": (700, ("## Prerequisites", "## Challenge", "## Evidence packet", "## Dimension requirements", "## Evaluator instructions", "## Review prompts", "## Pass and rework", "## Remediation")),
    "assessments/gates/ai-platform.md": (700, ("## Prerequisites", "## Challenge", "## Evidence packet", "## Dimension requirements", "## Evaluator instructions", "## Review prompts", "## Pass and rework", "## Remediation")),
    "assessments/gates/staff.md": (700, ("## Prerequisites", "## Challenge", "## Evidence packet", "## Dimension requirements", "## Evaluator instructions", "## Review prompts", "## Pass and rework", "## Remediation")),
    "certs/README.md": (80, ("## Overlay contract", "## Available overlays")),
    "certs/aws-dop-c02.md": (1200, ("## Official scope", "## Assessment gates used in the mapping", "## Complete task-statement map", "## Overlay study order", "## AWS-specific gap register", "## Practice and evidence plan")),
    "case-studies/README.md": (150, ("## Cases", "## How to use them", "## Curriculum map")),
    "case-studies/01-failed-kubernetes-rollout.md": (1200, ("## Context and constraints", "## Options and tradeoffs", "## Decision and reversible mitigation", "## Consequence and recovery review", "## Reusable engineering lessons", "## Evidence exercise", "## Teach-back prompts")),
    "case-studies/02-inference-latency-and-cost.md": (1200, ("## Context and constraints", "## Options and tradeoffs", "## Decision", "## Consequence and review", "## Reusable engineering lessons", "## Evidence exercise", "## Teach-back prompts")),
    "case-studies/03-platform-adoption.md": (1200, ("## Context and constraints", "## Decision", "## Consequence and review", "## Reusable engineering lessons", "## Evidence exercise", "## Teach-back prompts")),
    "QUALITY.md": (1200, ("## Universal definition of done", "## Factual and source quality", "## Evidence and reproducibility", "## Safety, privacy, and cost", "## Links and diagrams", "## Lessons", "## Guided labs", "## Incident drills", "## Projects", "## Assessments", "## Role tracks", "## Certification overlays", "## Case studies", "## Review ownership", "## Change maintenance")),
}
DISCOVERY_TARGETS = (
    "tracks/README.md",
    "assessments/README.md",
    "certs/README.md",
    "case-studies/README.md",
)
DISCOVERY_DOCS = (
    "README.md",
    "START-HERE.md",
    "CURRICULUM.md",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "QUALITY.md",
)
MINIMUM_DISCOVERY_DOCS = 2

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
    if len(text.split()) < 250:
        fail(rel, "lesson is too short for the substantive chapter contract")

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
    blocks: list[str] = []
    active: tuple[str, int, bool, int] | None = None
    block_lines: list[str] = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        fence = re.match(r"^(`{3,}|~{3,})(.*)$", line)
        if active is None:
            if not fence:
                continue
            marker, info = fence.groups()
            language = info.strip()
            is_mermaid = language == "mermaid"
            if language.lower().startswith("mermaid") and not is_mermaid:
                fail(rel, f"line {line_number}: Mermaid fence must contain only the language name")
            active = (marker[0], len(marker), is_mermaid, line_number)
            block_lines = []
            continue

        marker_char, marker_length, is_mermaid, opening_line = active
        closing = re.match(rf"^{re.escape(marker_char)}{{{marker_length},}}\s*$", line)
        if closing:
            if is_mermaid:
                blocks.append("\n".join(block_lines))
            active = None
            block_lines = []
        elif is_mermaid:
            block_lines.append(line)

    if active is not None and active[2]:
        fail(rel, f"line {active[3]}: Mermaid fence is not closed")

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


def check_system_file(relative: str, minimum_words: int, headings: tuple[str, ...]) -> None:
    path = ROOT / relative
    if not path.is_file():
        fail(relative, "missing required curriculum-system file")
        return
    text = path.read_text(encoding="utf-8")
    words = re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE)
    if len(words) < minimum_words:
        fail(relative, f"must be substantive; expected at least {minimum_words} words, found {len(words)}")
    lines = text.splitlines()
    h1s = [line for line in lines if line.startswith("# ")]
    if len(h1s) != 1 or not lines or not lines[0].startswith("# "):
        fail(relative, "must begin with exactly one H1 title")
    ordered_headings(path, text, list(headings))


def arrow_glyphs(text: str) -> list[str]:
    return sorted(
        {
            character
            for character in text
            if "ARROW" in unicodedata.name(character, "")
        }
    )


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

for relative, (minimum_words, headings) in SYSTEM_SPECS.items():
    check_system_file(relative, minimum_words, headings)

track_files = sorted((ROOT / "tracks").glob("*.md"))
for path in (path for path in track_files if path.name != "README.md"):
    text = path.read_text(encoding="utf-8")
    for required_link_root in ("../labs/", "../incidents/", "../projects/", "../assessments/gates/"):
        if required_link_root not in text:
            fail(path.relative_to(ROOT), f"missing required practice link under {required_link_root}")

for path in sorted((ROOT / "assessments" / "gates").glob("*.md")):
    text = path.read_text(encoding="utf-8")
    for dimension in ("Explain", "Build", "Debug", "Operate", "Design"):
        if f"- **{dimension}:**" not in text:
            fail(path.relative_to(ROOT), f"missing substantive {dimension} dimension requirement")

dop_path = ROOT / "certs" / "aws-dop-c02.md"
if dop_path.is_file():
    dop_text = dop_path.read_text(encoding="utf-8")
    mapped_tasks = set(re.findall(r"^\|\s+\*\*(\d\.\d)\s", dop_text, re.MULTILINE))
    expected_tasks = {
        "1.1", "1.2", "1.3", "1.4",
        "2.1", "2.2", "2.3",
        "3.1", "3.2", "3.3",
        "4.1", "4.2", "4.3",
        "5.1", "5.2", "5.3",
        "6.1", "6.2", "6.3",
    }
    if mapped_tasks != expected_tasks:
        missing = sorted(expected_tasks - mapped_tasks)
        unexpected = sorted(mapped_tasks - expected_tasks)
        fail(dop_path.relative_to(ROOT), f"task map mismatch; missing {missing}, unexpected {unexpected}")

discovery_references: dict[str, list[str]] = {target: [] for target in DISCOVERY_TARGETS}
for discovery_doc in DISCOVERY_DOCS:
    path = ROOT / discovery_doc
    if not path.is_file():
        continue
    linked_targets = {
        target.strip().split(maxsplit=1)[0].strip("<>").split("#", maxsplit=1)[0]
        for target in LINK_RE.findall(path.read_text(encoding="utf-8"))
    }
    for target in DISCOVERY_TARGETS:
        if target in linked_targets:
            discovery_references[target].append(discovery_doc)
for target, documents in discovery_references.items():
    if len(documents) < MINIMUM_DISCOVERY_DOCS:
        fail(
            target,
            f"must be linked from at least {MINIMUM_DISCOVERY_DOCS} root discovery documents; found {documents}",
        )

lab_dirs = sorted(path for path in (ROOT / "labs").glob("[0-9][0-9]-*") if path.is_dir())
if len(lab_dirs) < 19:
    fail("labs", f"expected at least 19 guided labs; found {len(lab_dirs)}")
for lab in lab_dirs:
    if not (lab / "README.md").is_file():
        fail(lab.relative_to(ROOT), "lab directory is missing README.md")

incident_dirs = sorted(
    path for path in (ROOT / "incidents").glob("[0-9][0-9]-*") if path.is_dir()
)
if len(incident_dirs) < 12:
    fail("incidents", f"expected at least 12 incident drills; found {len(incident_dirs)}")
for incident in incident_dirs:
    for required in ("README.md", "solution.md"):
        if not (incident / required).is_file():
            fail(incident.relative_to(ROOT), f"incident is missing {required}")

project_dirs = sorted(
    path for path in (ROOT / "projects").glob("[0-9][0-9]-*") if path.is_dir()
)
if len(project_dirs) != 15:
    fail("projects", f"expected exactly 15 portfolio briefs; found {len(project_dirs)}")
for project in project_dirs:
    if not (project / "README.md").is_file():
        fail(project.relative_to(ROOT), "project directory is missing README.md")

cheatsheets = {path.name for path in (ROOT / "cheatsheets").glob("*.md")}
missing_cheatsheets = REQUIRED_CHEATSHEETS - cheatsheets
if missing_cheatsheets:
    fail("cheatsheets", f"missing operator sheets: {sorted(missing_cheatsheets)}")

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
        if not path.stem.lower().endswith("-lab")
    )
    minimum = 20 if number == 0 else MINIMUM_LESSONS[number]
    if len(lessons) < minimum:
        fail(module.relative_to(ROOT), f"needs at least {minimum} real lessons; found {len(lessons)}")
    for lesson in lessons:
        check_lesson(lesson)

markdown_files = sorted(
    path
    for path in ROOT.rglob("*.md")
    if ".git" not in path.parts
)

for path in set(markdown_files):
    text = path.read_text(encoding="utf-8")
    arrows = arrow_glyphs(text)
    if arrows:
        fail(
            path.relative_to(ROOT),
            f"contains Unicode arrow glyphs {arrows!r}; write prose or use Mermaid edge syntax",
        )
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
    if not path.stem.lower().endswith("-lab")
)
print(f"Validated {len(module_dirs)} modules and {lesson_count} lessons.")
