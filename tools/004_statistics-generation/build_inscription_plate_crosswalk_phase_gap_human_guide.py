#!/usr/bin/env python3
"""Build a human guide for inscription/plate phase gaps.

The guide turns the 195 checklist into a human-readable review entrance. It is
navigation only: no evidence collection, rights decision, formal inscription
import, inscription identity claim, or decipherment claim.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
INSCRIPTION_DIR = Path("corpus/002_oracle-bone-inscriptions")
CHECKLIST = STAT_DIR / "195_inscription-plate-crosswalk-phase-gap-review-checklist.csv"
ACTION_QUEUE = STAT_DIR / "192_core-corpus-phase-gap-action-queue.csv"
REVIEW_QUEUE = STAT_DIR / "098_ai-agent-cambridge-hopkins-inscription-crosswalk-review-queue.csv"
DEFAULT_OUTPUT = STAT_DIR / "214_inscription-plate-crosswalk-phase-gap-human-guide.md"
UPDATED_AT = "2026-06-30"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def count_files(root: Path, pattern: str) -> int:
    return sum(1 for path in root.glob(pattern) if path.is_file())


def split_values(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def build_markdown(root: Path) -> str:
    rows = read_csv_rows(root / CHECKLIST)
    phase_statuses = [f"{row['phase_name']}: `{row['phase_status']}`" for row in rows]
    source_ids = sorted({sid for row in rows for sid in split_values(row["source_ids"])})
    candidate_count = count_files(
        root,
        "corpus/002_oracle-bone-inscriptions/**/"
        "01_candidate-inscription-crosswalk-packet.json",
    )
    route_count = count_files(
        root,
        "corpus/002_oracle-bone-inscriptions/**/05_plate-text-route-index.csv",
    )
    gallery_count = count_files(
        root,
        "corpus/002_oracle-bone-inscriptions/**/06_plate-text-gallery.md",
    )

    lines = [
        "# Inscription Plate Crosswalk Phase Gap Human Guide / "
        "卜辞图版互证阶段缺口人工复核指南",
        "",
        "English:",
        "This guide is the human entrance for the inscription and plate",
        "crosswalk phase gaps. It helps a reviewer move from the phase",
        "queue to object-local dossiers, plate/text routes, source rows,",
        "and review queues before any formal inscription record is made.",
        "It is not a formal inscription record, not confirmed scholarship,",
        "not a rights decision, and not a decipherment conclusion.",
        "",
        "简体中文：",
        "本指南是卜辞与图版互证阶段缺口的人工入口。",
        "复核者应从阶段缺口回到对象目录内档案、图版/文本路线、",
        "来源登记和复核队列，再判断下一步是否具备人工复核条件。",
        "它不是正式卜辞记录，不是已确认学术结论，不是权利决定，",
        "也不是释读结论。",
        "",
        "## Summary / 摘要",
        "",
        f"- updated at: {UPDATED_AT}",
        f"- checklist rows: {len(rows)}",
        f"- inscription candidates: {candidate_count}",
        f"- plate/text route indexes: {route_count}",
        f"- plate/text galleries: {gallery_count}",
        f"- source id: `{';'.join(source_ids)}`",
    ]
    for status in phase_statuses:
        lines.append(f"- {status}")
    lines.extend(
        [
            "",
            "## Human Review Entry Order / 人工复核入口顺序",
            "",
            "1. Open the object-local inscription dossier first.",
            "2. Open `07_human-inscription-dossier.md` first.",
            "3. Open `09_inscription-plate-evidence-dossier.md`.",
            "4. Check inscription number, catalog number, and source row.",
            "5. Check full text or OCR, text quality, and missing text.",
            "6. Check plate number, page number, Heji route, or OBM route.",
            "7. Check image path, rubbing route, thumbnail, and rights note.",
            "8. Check collection object, findspot, period, or batch.",
            "9. Check components, variants, and related glyph relations.",
            "10. Check scholarship, catalog history, proposer, and disputes.",
            "11. Record only reviewed outcomes in the matching scaffold.",
            "",
            "人工复核时，先打开对象目录内的卜辞档案和图版证据档案。",
            "随后核对卜辞编号、著录号、全文或 OCR、图版号、页码、",
            "合集或 OBM 路线、图像路径、馆藏、出土地、时期和批次。",
            "缺失项必须写成具体待查问题，不得写成空泛状态。",
            "",
            "## Support Files / 辅助文件",
            "",
            "| File | Path |",
            "| --- | --- |",
            f"| checklist | `{CHECKLIST.as_posix()}` |",
            f"| action queue | `{ACTION_QUEUE.as_posix()}` |",
            f"| review queue | `{REVIEW_QUEUE.as_posix()}` |",
            "| object root | `corpus/002_oracle-bone-inscriptions/` |",
            "| source map | `project_registry/002_project-id-to-source-reference-map/` |",
            "",
            "Use these files after opening the object-local human dossiers.",
            "They are support routes, not reviewed evidence by themselves.",
            "",
            "## Concrete Questions To Check / 具体待查问题",
            "",
            "- Which candidate row identifies the inscription crosswalk?",
            "- Which full text or OCR route can be opened?",
            "- Which text quality issue blocks review?",
            "- Which plate number, page number, Heji route, or OBM route",
            "  locates the inscription?",
            "- Which local image path, rubbing route, or thumbnail exists?",
            "- Which catalog source and page or plate reference support it?",
            "- Which collection object, findspot, period, or batch is recorded?",
            "- Which related glyph routes must be checked before promotion?",
            "- Which components, variants, or near-form relations need review?",
            "- Which scholarship note, proposer, or dispute remains missing?",
            "- Which missing item should a human reviewer open next?",
            "- 哪一条候选行能定位这条卜辞互证记录？",
            "- 哪一条全文或 OCR 路线可以打开？",
            "- 哪个文本质量问题阻碍复核？",
            "- 哪个图版号、页码、合集路线或 OBM 路线能定位卜辞？",
            "- 哪个本地图像、拓片路线或缩略图已经存在？",
            "- 哪个著录来源和页码或图版引用支持它？",
            "- 哪个馆藏对象、出土地、时期或批次已经记录？",
            "- 哪些关联字形路线在提升前必须复核？",
            "- 哪些构件、异体或近形关系仍需复核？",
            "- 哪条学术文献、提出者或争议记录仍缺失？",
            "- 下一步应由人工打开哪一项缺失证据？",
            "",
            "## Boundary / 边界",
            "",
            "Do not create a formal `obi-*` record from this guide.",
            "Do not treat a crosswalk row, review queue, graph edge,",
            "OCR route, or catalog route as confirmed scholarship.",
            "Do not treat it as a formal inscription record.",
            "It is not a decipherment conclusion.",
            "",
            "不得根据本指南创建正式 `obi-*` 记录。",
            "不得把互证行、复核队列、图边、OCR 路线或著录路线",
            "当作已确认学术结论。",
            "不得把它当作正式卜辞记录，也不得当作释读结论。",
            "",
        ]
    )
    return "\n".join(lines)


def write_markdown(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the inscription plate crosswalk phase gap guide."
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    write_markdown(root / args.output, build_markdown(root))
    print(f"inscription_plate_crosswalk_phase_gap_human_guide={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
