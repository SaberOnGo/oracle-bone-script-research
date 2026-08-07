#!/usr/bin/env python3
"""Normalize HUST-OBC object-local visual observation dossiers.

The repository already contains several generations of direct visual notes.
This repair keeps their descriptive content, normalizes equivalent follow-up
and boundary headings, wraps Markdown to 80 characters, and adds concrete
questions only where a note has no follow-up section.  It never infers a
reading, identity, component, variant, period, or decipherment.
"""

from __future__ import annotations

import argparse
import json
import re
import textwrap
from pathlib import Path


CHARACTER_ROOT = Path("corpus/001_oracle-characters")
OBSERVATION_NAME = "14_material-visual-observation.md"
MAX_LINE_LENGTH = 80

NEXT_HEADING = "## Next Checks / 下一步核查"
BOUNDARY_HEADING = "## Boundary / 边界"
DIRECT_HEADING = "## Direct Visual Record / 直接可见记录"

NEXT_RE = re.compile(
    r"^\s*(?:#{1,6}\s*)?(?:next checks|follow-up questions|"
    r"concrete follow-up questions|concrete follow-up checks|pending checks|"
    r"missing items and next checks|missing items and follow-up questions)"
    r"(?:\s*/.*)?[:：]?\s*$",
    re.IGNORECASE,
)
BOUNDARY_RE = re.compile(
    r"^\s*(?:#{1,6}\s*)?(?:research boundary|boundary)"
    r"(?:\s*/.*)?[:：]?\s*$",
    re.IGNORECASE,
)
DIRECT_RE = re.compile(
    r"^\s*(?:#{1,6}\s*)?direct visual record"
    r"(?:\s*/.*)?[:：]?\s*$",
    re.IGNORECASE,
)

FOLLOW_UP_SECTION = [
    "",
    NEXT_HEADING,
    "",
    "- Which catalog entry, plate, page, collection, findspot, period, and",
    "  batch records this image or inscription?",
    "- Is a rubbing, full plate, reverse, neighboring context, or higher-",
    "  resolution derivative available?",
    "- Can the source package, checksum, extraction note, rights status, and",
    "  image route be checked against the provenance register?",
    "- Are variant, near-form, component, later-script, and inscription links",
    "  source-supported, or still pending?",
    "- 中文待查：哪条著录、图版、页码、馆藏、出土地、时期或批次记录了",
    "  当前图像或卜辞？",
    "- 中文待查：是否有拓片、整版、反面、邻近语境或更高分辨率派生图？",
    "- 中文待查：来源包、校验和、解包说明、权利状态和图像路线能否与",
    "  provenance 登记记录核对？",
]

BOUNDARY_SECTION = [
    "",
    BOUNDARY_HEADING,
    "",
    "- This record preserves source-linked visual material only. It does not",
    "  confirm identity, variant, component, inscription reading, period,",
    "  evolution, or decipherment.",
    "- 中文：本记录只保存有来源的可见材料，不确认字形身份、异体、构件、",
    "  卜辞释读、时期、演变或破译。",
]


def _wrap_line(line: str) -> list[str]:
    """Wrap one Markdown line without changing its words."""

    if len(line) <= MAX_LINE_LENGTH:
        return [line]
    leading = line[: len(line) - len(line.lstrip())]
    content = line[len(leading) :]
    prefix = ""
    if content.startswith(("- ", "* ", "+ ", "> ")):
        prefix, content = content[:2], content[2:]
    first_indent = leading + prefix
    continuation_indent = leading + ("  " if prefix else "")

    def make_parts(break_long_words: bool) -> list[str]:
        width = max(1, MAX_LINE_LENGTH - len(first_indent))
        return textwrap.wrap(
            content,
            width=width,
            initial_indent=first_indent,
            subsequent_indent=continuation_indent,
            break_long_words=break_long_words,
            break_on_hyphens=False,
        ) or [first_indent]

    parts = make_parts(False)
    if any(len(part) > MAX_LINE_LENGTH for part in parts):
        parts = make_parts(True)
    if any(len(part) > MAX_LINE_LENGTH for part in parts):
        # This is only a last resort for an unusually long unbroken token.
        flattened = "".join(parts)
        parts = [
            flattened[index : index + MAX_LINE_LENGTH]
            for index in range(0, len(flattened), MAX_LINE_LENGTH)
        ]
    return parts


def _normalize_headings(lines: list[str]) -> tuple[list[str], bool, bool]:
    normalized: list[str] = []
    has_next = False
    has_boundary = False
    for line in lines:
        if NEXT_RE.match(line):
            if not has_next:
                normalized.append(NEXT_HEADING)
                has_next = True
            continue
        if BOUNDARY_RE.match(line):
            if not has_boundary:
                normalized.append(BOUNDARY_HEADING)
                has_boundary = True
            continue
        if DIRECT_RE.match(line):
            normalized.append(DIRECT_HEADING)
            continue
        normalized.append(line)
    return normalized, has_next, has_boundary


def repair_text(text: str) -> tuple[str, dict[str, bool]]:
    lines, has_next, has_boundary = _normalize_headings(text.splitlines())
    added_next = not has_next
    added_boundary = not has_boundary
    if added_next:
        lines.extend(FOLLOW_UP_SECTION)
    if added_boundary:
        lines.extend(BOUNDARY_SECTION)

    wrapped: list[str] = []
    for line in lines:
        wrapped.extend(_wrap_line(line))
    repaired = "\n".join(wrapped).rstrip() + "\n"
    if any(len(line) > MAX_LINE_LENGTH for line in repaired.splitlines()):
        raise ValueError("repair produced a line longer than 80 characters")
    return repaired, {
        "added_next": added_next,
        "added_boundary": added_boundary,
    }


def repair(root: Path) -> dict[str, int]:
    root = root.resolve()
    scanned = 0
    changed = 0
    wrapped_files = 0
    added_next = 0
    added_boundary = 0
    for path in sorted((root / CHARACTER_ROOT).rglob(OBSERVATION_NAME)):
        if "hust-obc" not in path.parent.name:
            continue
        scanned += 1
        original = path.read_text(encoding="utf-8")
        repaired, details = repair_text(original)
        if repaired == original:
            continue
        path.write_text(repaired, encoding="utf-8", newline="\n")
        changed += 1
        if len(original.splitlines()) != len(repaired.splitlines()):
            wrapped_files += 1
        added_next += int(details["added_next"])
        added_boundary += int(details["added_boundary"])
    return {
        "scanned": scanned,
        "changed": changed,
        "wrapped_or_reformatted": wrapped_files,
        "next_sections_added": added_next,
        "boundary_sections_added": added_boundary,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    print(json.dumps(repair(args.root), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
