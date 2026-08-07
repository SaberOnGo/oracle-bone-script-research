#!/usr/bin/env python3
"""Gate human-readable research material against machine-route drift.

This check exists because an object-local Markdown file is not human research
material merely because its filename says ``human``. A useful oracle-character
folder must foreground readable research facts, reviewed source evidence, and
explicit evidence gaps. JSON, CSV, route, packet, manifest, and checklist text
may support that work, but they must not become the main substance.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


BASELINE_PATH = Path("tools/validation/human_research_material_gate_baseline.json")
CORPUS_ROOT = Path("corpus")

MOJIBAKE_FRAGMENTS = [
    "绠€",
    "寰呮煡",
    "绾跨储",
    "鐮",
    "閻",
    "缂哄け",
    "鑰冨彜",
    "锟",
    "\ufffd",
]

MACHINE_ROUTE_TERMS = [
    "JSON",
    "CSV",
    "AI-readable",
    "machine-readable",
    "index",
    "packet",
    "route",
    "manifest",
    "staging",
    "schema",
    "graph edge",
    "checklist",
    "validation",
    "field",
    "review status",
    "support tools",
    "结构化",
    "索引",
    "字段",
    "路线",
    "图边",
    "校验",
    "复核流程",
    "机器",
    "模板",
]

HUMAN_RESEARCH_TERMS = [
    "字形",
    "释义",
    "释读",
    "释读史",
    "学者",
    "提出者",
    "争议",
    "构件",
    "组成",
    "异体",
    "近形",
    "卜辞",
    "全文",
    "OCR",
    "图版",
    "著录",
    "合集",
    "出土",
    "馆藏",
    "时期",
    "组类",
    "金文",
    "小篆",
    "今字",
    "演化",
    "轶事",
    "关系",
    "同构件",
    "rubbing",
    "inscription",
    "catalog",
    "provenance",
    "findspot",
    "collection",
    "period",
    "variant",
    "component",
    "dispute",
]

RESEARCH_SLOT_PATTERNS = {
    "glyph_image": r"字形|glyph|image|图像|拓片|照片",
    "meaning_or_reading": r"释义|释读|meaning|reading",
    "components": r"构件|组成|component",
    "scholarship": r"学者|提出者|论文|书目|释读史|dispute|争议",
    "excavation": r"出土|馆藏|时期|组类|findspot|collection|period",
    "inscription": r"卜辞|全文|OCR|图版|著录|合集|inscription|catalog",
    "relations": r"异体|近形|金文|小篆|今字|同构件|关系|variant",
}

MODERN_LABEL_RISK_PATTERNS = [
    re.compile(r"dataset label text:\s*`[^`]+`"),
    re.compile(r"来源标签文字:\s*`[^`]+`"),
    re.compile(r"source_modern_label_candidate"),
]

# These files are deliberately auxiliary review surfaces.  They tell a
# researcher which evidence to open, but they are not the human research
# dossier itself.  Keeping them out of the dossier-content score prevents a
# checklist full of route terms from being mistaken for human scholarship.
SUPPORT_ONLY_MARKDOWN_NAMES = {
    "04_human-review-sheet.md",
    "05_human-topic-review-sheet.md",
    "06_human-source-review-sheet.md",
    "08_human-visual-review-sheet.md",
    "06_human-topic-dossier.md",
    "08_topic-literature-context-dossier.md",
}


def git_command(root: Path, *args: str) -> list[str]:
    return ["git", "-c", f"safe.directory={root.as_posix()}", *args]


@dataclass(frozen=True)
class DocumentScore:
    path: str
    machine_hits: int
    research_hits: int
    missing_slots: list[str]
    mojibake_hits: list[str]
    modern_label_risk: bool

    @property
    def machine_dominant(self) -> bool:
        if self.research_hits < 8:
            return self.machine_hits >= self.research_hits
        return self.machine_hits > self.research_hits * 2

    @property
    def missing_core_research(self) -> bool:
        return len(self.missing_slots) >= 3


def count_terms(text: str, terms: list[str]) -> int:
    lowered = text.lower()
    return sum(lowered.count(term.lower()) for term in terms)


def has_modern_label_risk(text: str) -> bool:
    if "not an accepted" in text or "不是已接受" in text:
        return False
    return any(pattern.search(text) for pattern in MODERN_LABEL_RISK_PATTERNS)


def score_markdown(path: Path, root: Path) -> DocumentScore:
    text = path.read_text(encoding="utf-8")
    missing_slots = [
        slot
        for slot, pattern in RESEARCH_SLOT_PATTERNS.items()
        if not re.search(pattern, text, flags=re.IGNORECASE)
    ]
    mojibake_hits = [fragment for fragment in MOJIBAKE_FRAGMENTS if fragment in text]
    return DocumentScore(
        path=path.relative_to(root).as_posix(),
        machine_hits=count_terms(text, MACHINE_ROUTE_TERMS),
        research_hits=count_terms(text, HUMAN_RESEARCH_TERMS),
        missing_slots=missing_slots,
        mojibake_hits=mojibake_hits,
        modern_label_risk=has_modern_label_risk(text),
    )


def human_markdown_path(relative: str) -> bool:
    path = Path(relative)
    # Source briefs are verified by the source-object skeleton checks.  They
    # summarize provenance and research-use limits, so applying character
    # dossier slots (glyph, inscription, excavation, and relations) to them
    # would be a category error.
    if path.name == "22_source-research-brief.md":
        return False
    # This source-level access audit explains transport and provenance
    # boundaries. Requiring character dossier slots such as glyph form,
    # components, or inscription text would be a category error.
    if path.name == "225_source-access-boundary-human-review.md":
        return False
    if path.name == "230_preformal-research-preprocessing-closure.md":
        return True
    # Review sheets and topic routing dossiers are support materials.  Their
    # route/checklist language is intentional and must not be scored as the
    # substance of a human-readable character or source dossier.
    if path.name in SUPPORT_ONLY_MARKDOWN_NAMES:
        return False
    patterns = [
        "README.md",
        "*human*.md",
        "*review*.md",
        "*dossier*.md",
        "*evidence*.md",
        "*source*.md",
    ]
    if not relative.startswith("corpus/"):
        return False
    if not any(fnmatch.fnmatch(path.name, pattern) for pattern in patterns):
        return False
    parts = set(path.parts)
    if {".cache", ".working", "tmp", "_tmp", "scratch"} & parts:
        return False
    if any(part.endswith("registers") for part in parts):
        return False
    # Bucket and source-register README files describe directory mechanics or
    # registry scope.  Object-local READMEs remain in the gate; these two
    # categories are navigation aids rather than research dossiers.
    if path.name == "README.md":
        if any("bucket" in part for part in path.parts):
            return False
    return not path.name.startswith(".")


def iter_all_human_markdown(root: Path) -> list[Path]:
    result = subprocess.run(
        git_command(root, "ls-files", "corpus/**/*.md"),
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    seen: set[str] = set()
    filtered: list[Path] = []
    for relative in result.stdout.splitlines():
        if relative in seen:
            continue
        seen.add(relative)
        path = root / relative
        if not human_markdown_path(relative):
            continue
        filtered.append(path)
    return sorted(filtered)


def iter_changed_human_markdown(root: Path) -> list[Path]:
    commands = [
        git_command(
            root,
            "diff",
            "--name-only",
            "--diff-filter=ACMR",
            "HEAD",
            "--",
            "corpus",
        ),
        git_command(root, "ls-files", "--others", "--exclude-standard", "corpus"),
    ]
    seen: set[str] = set()
    filtered: list[Path] = []
    for command in commands:
        result = subprocess.run(
            command,
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        for relative in result.stdout.splitlines():
            if relative in seen or not human_markdown_path(relative):
                continue
            seen.add(relative)
            path = root / relative
            if path.exists():
                filtered.append(path)
    return sorted(filtered)


def iter_human_markdown(root: Path, full: bool = False) -> list[Path]:
    if full:
        return iter_all_human_markdown(root)
    return iter_changed_human_markdown(root)


def summarize(scores: list[DocumentScore]) -> dict[str, int]:
    return {
        "scanned_markdown_count": len(scores),
        "machine_dominant_docs": sum(score.machine_dominant for score in scores),
        "missing_core_research_docs": sum(
            score.missing_core_research for score in scores
        ),
        "modern_label_risk_docs": sum(score.modern_label_risk for score in scores),
        "mojibake_docs": sum(bool(score.mojibake_hits) for score in scores),
    }


def load_baseline(root: Path) -> dict[str, int]:
    path = root / BASELINE_PATH
    if not path.exists():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    return {key: int(value) for key, value in data["maximums"].items()}


def build_issues(root: Path, strict: bool = False, full: bool = False) -> list[str]:
    scores = [score_markdown(path, root) for path in iter_human_markdown(root, full)]
    summary = summarize(scores)
    issues: list[str] = []

    mojibake = [score for score in scores if score.mojibake_hits]
    for score in mojibake[:20]:
        hits = ", ".join(score.mojibake_hits)
        issues.append(f"{score.path} contains mojibake marker(s): {hits}")
    if len(mojibake) > 20:
        issues.append(f"{len(mojibake) - 20} more markdown files contain mojibake")

    if strict or not full:
        for score in scores:
            if score.machine_dominant:
                issues.append(f"{score.path} is dominated by machine-route language")
            if score.missing_core_research:
                missing = ", ".join(score.missing_slots)
                issues.append(f"{score.path} lacks research slots: {missing}")
            if score.modern_label_risk:
                issues.append(
                    f"{score.path} risks treating a modern label as the glyph"
                )
        return issues

    baseline = load_baseline(root)
    for key, value in summary.items():
        maximum = baseline.get(key)
        if maximum is None:
            issues.append(f"human research gate baseline missing key: {key}")
        elif value > maximum:
            issues.append(
                f"human research gate regression for {key}: "
                f"{value} exceeds baseline {maximum}"
            )
    return issues


def print_summary(root: Path, full: bool = False) -> None:
    scores = [score_markdown(path, root) for path in iter_human_markdown(root, full)]
    summary = summarize(scores)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument(
        "--full",
        action="store_true",
        help="scan all tracked human-facing corpus Markdown; otherwise scan changes",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if args.summary:
        print_summary(root, full=args.full)
        return 0

    issues = build_issues(root, strict=args.strict, full=args.full)
    if issues:
        print("FAIL human research material gate")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("PASS human research material gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
