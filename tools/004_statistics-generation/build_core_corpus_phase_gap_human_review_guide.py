#!/usr/bin/env python3
"""Build a human-readable guide for core-corpus phase gap review.

The guide summarizes the 192 and 199 route tables as a human entry point. It
does not collect evidence, record outcomes, decide rights, promote sources or
candidate records, import corpus rows, or make decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CORE_CORPUS_PHASE_GAP_ACTION_QUEUE = STAT_DIR / "192_core-corpus-phase-gap-action-queue.csv"
CORE_CORPUS_PHASE_GAP_REVIEW_INDEX = STAT_DIR / "199_core-corpus-phase-gap-review-index.csv"
DEFAULT_OUTPUT = STAT_DIR / "213_core-corpus-phase-gap-human-review-guide.md"
UPDATED_AT = "2026-06-30"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def count_lines(title: str, counter: Counter[str]) -> list[str]:
    lines = [f"### {title}", ""]
    for key, count in sorted(counter.items()):
        lines.append(f"- {key}: {count}")
    lines.append("")
    return lines


def build_markdown(root: Path) -> str:
    gap_rows = read_csv_rows(root / CORE_CORPUS_PHASE_GAP_ACTION_QUEUE)
    index_rows = read_csv_rows(root / CORE_CORPUS_PHASE_GAP_REVIEW_INDEX)
    area_counts = Counter(row["corpus_area"] for row in gap_rows)
    phase_counts = Counter(row["phase_status"] for row in gap_rows)
    family_counts = Counter(row["specialized_checklist_family"] for row in index_rows)

    lines = [
        "# Core Corpus Phase Gap Human Review Guide / 核心语料阶段缺口人工复核指南",
        "",
        "English:",
        "This guide is the human-readable entry for core-corpus preprocessing",
        "phase gaps. It tells reviewers which support file to open after",
        "they have checked the relevant human-readable dossier, source object,",
        "or review sheet. It is not a reviewed outcome, not a rights decision,",
        "not source or candidate promotion, not corpus import approval, and",
        "not a decipherment conclusion.",
        "Each gap must lead back to images, rubbings, inscription text, catalog",
        "numbers, findspot or collection data, period evidence, component and",
        "variant comparison, and published scholarship or dispute notes.",
        "",
        "简体中文：",
        "本指南是核心语料预处理阶段缺口的人工入口。复核者应先打开",
        "相关对象的人类可读档案、来源对象或复核表，再按这里列出的",
        "辅助文件继续核查。本指南不是复核结论，不是权利决定，",
        "不是来源或候选记录提升，不是语料导入批准，也不是释读结论。",
        "每个缺口都必须回到字形图像、拓片、卜辞全文、著录号、出土地、",
        "馆藏、时期、构件、异体、近形、释读史、提出者和争议。",
        "",
        "## Summary / 摘要",
        "",
        f"- updated at / 更新日期: {UPDATED_AT}",
        f"- gap rows: {len(gap_rows)}",
        f"- review index rows: {len(index_rows)}",
        "",
        "| Route file | Path |",
        "| --- | --- |",
        f"| action queue | `{CORE_CORPUS_PHASE_GAP_ACTION_QUEUE.as_posix()}` |",
        f"| review index | `{CORE_CORPUS_PHASE_GAP_REVIEW_INDEX.as_posix()}` |",
        "",
    ]
    lines.extend(count_lines("Gap Rows By Corpus Area / 按语料区统计缺口", area_counts))
    lines.extend(count_lines("Gap Rows By Phase Status / 按阶段状态统计缺口", phase_counts))
    lines.extend(count_lines("Specialized Checklists / 专项复核清单", family_counts))
    lines.extend(
        [
            "## Human Review Entry Order / 人工复核入口顺序",
            "",
            "1. Open the related object-local human-readable dossier first.",
            "2. Check glyph images, rubbings, inscriptions, and catalog notes.",
            "3. Check source provenance, rights status, and review status.",
            "4. Check scholarship, reading history, authors, and disputes.",
            "5. Check findspot, collection, period, group, and batch evidence.",
            "6. Check component, variant, near-form, and later-form evidence.",
            "7. Open the support files named below only after those checks.",
            "8. Record reviewed results only in the matching outcome scaffold.",
            "9. Keep empty outcome fields empty until a human review pass.",
            "",
            "Support files to open after the human checks:",
            "",
            "1. Open `192_core-corpus-phase-gap-action-queue.csv`.",
            "2. Open `199_core-corpus-phase-gap-review-index.csv`.",
            "3. Open the specialized checklist named by the review index row.",
            "",
            "人工复核时，先打开对象内人类可读档案，再核对字形图像、拓片、",
            "卜辞全文、图版、著录号、出土地、馆藏、时期、构件、异体、",
            "近形、释读史、提出者、不同意见和争议。完成这些人工核查后，",
            "再查看 192 行动队列、199 复核索引和对应专项清单。只有完成",
            "人工复核后，才把结果写入匹配的 outcome scaffold。",
            "",
            "## Research Slots To Recover / 应回收的研究槽位",
            "",
            "- Glyph image, rubbing, photograph, and plate evidence.",
            "- Inscription text, OCR, catalog number, and collection number.",
            "- Findspot, collection, period, group, and batch evidence.",
            "- Component, variant, near-form, bronze, seal, and modern links.",
            "- Bibliography, scholarship history, proposer, and disputes.",
            "- Missing evidence and next source to check before formal research.",
            "- 字形图像、拓片、照片和图版证据。",
            "- 卜辞全文、OCR、著录号、合集号和馆藏编号。",
            "- 出土地、馆藏、时期、组类和批次证据。",
            "- 构件、异体、近形、金文、小篆和今字关联。",
            "- 书目、释读史、提出者、不同意见和争议。",
            "- 正式研究前仍缺的证据和下一步待查来源。",
            "",
            "## Support File Steps / 辅助文件步骤",
            "",
            "1. Open `192_core-corpus-phase-gap-action-queue.csv`.",
            "2. Open `199_core-corpus-phase-gap-review-index.csv`.",
            "3. Open the specialized checklist named by the review index row.",
            "",
            "## Concrete Questions To Check / 具体待查问题",
            "",
            "- Which gap row points to a missing human-readable dossier?",
            "- Which source still lacks checksum, package manifest, or risk note?",
            "- Which candidate route is still only staging or metadata?",
            "- Which phase gap requires returning to an object-local review sheet?",
            "- Which evidence path is a route rather than collected evidence?",
            "- Which outcome scaffold is intentionally empty before review?",
            "- Which glyph image, rubbing, plate, or photograph is still missing?",
            "- Which inscription text, OCR, catalog, or collection number is absent?",
            "- Which scholarship, proposer, alternate view, or dispute is missing?",
            "- Which component, variant, near-form, or later-form link is unreviewed?",
            "- 哪条缺口行指向仍缺人类可读档案的对象？",
            "- 哪个来源仍缺 checksum、package manifest 或风险提示？",
            "- 哪条候选路线仍只是 staging 或 metadata？",
            "- 哪个阶段缺口必须回到对象内人工复核表？",
            "- 哪条证据路径只是路线，而不是已收集证据？",
            "- 哪个 outcome scaffold 在复核前应按设计保持为空？",
            "- 哪个字形图像、拓片、图版或照片仍缺失？",
            "- 哪条卜辞全文、OCR、著录号或馆藏号仍缺失？",
            "- 哪条书目、提出者、不同意见或争议仍缺失？",
            "- 哪条构件、异体、近形或后世字形关联仍未复核？",
            "",
            "## Boundary / 边界",
            "",
            "This guide summarizes route tables for preprocessing review. It does not",
            "replace a human-readable dossier, a source record, a rights note, a",
            "bibliographic note, a graph-edge source file, or a review sheet.",
            "",
            "本指南只汇总预处理复核路线表。它不能替代人类可读档案、来源",
            "记录、权利说明、书目笔记、图边来源文件或人工复核表。",
            "",
        ]
    )
    return "\n".join(lines)


def write_markdown(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the core corpus phase gap human review guide."
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    text = build_markdown(root)
    write_markdown(root / args.output, text)
    print(f"core_corpus_phase_gap_human_review_guide={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
