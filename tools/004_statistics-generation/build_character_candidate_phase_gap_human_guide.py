#!/usr/bin/env python3
"""Build a human guide for character-candidate phase gaps.

The guide turns the 198 checklist into a researcher-facing entrance for
oracle-character and undeciphered-character candidate dossiers. It does not
collect evidence, decide rights, promote candidates, import formal character
records, confirm identity, or make decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CHECKLIST = STAT_DIR / "198_character-candidate-phase-gap-review-checklist.csv"
ACTION_QUEUE = STAT_DIR / "192_core-corpus-phase-gap-action-queue.csv"
CHAR_REGISTER_DIR = Path("corpus/001_oracle-characters/000_character-registers")
HUST_PROMOTION_QUEUE = (
    CHAR_REGISTER_DIR / "009_hust-obc-obs-char-promotion-review-queue.csv"
)
HUST_PROMOTION_BUCKET_SUMMARY = (
    CHAR_REGISTER_DIR / "010_hust-obc-promotion-bucket-review-summary.csv"
)
UNDECIPHERED_INDEX = (
    CHAR_REGISTER_DIR / "003_undeciphered-oracle-characters-index.csv"
)
UNDECIPHERED_REVIEW_QUEUE = (
    STAT_DIR / "051_ai-agent-hust-obc-undeciphered-candidate-review-queue.csv"
)
CANDIDATE_EVIDENCE_REQUEST_QUEUE = (
    STAT_DIR / "005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv"
)
UNDECIPHERED_EVIDENCE_READINESS_CHECKLIST = (
    STAT_DIR
    / "060_ai-agent-hust-obc-undeciphered-candidate-evidence-readiness-checklist.csv"
)
CHARACTER_OBJECT_MATERIAL_COVERAGE_AUDIT = (
    STAT_DIR / "186_character-object-material-coverage-audit.csv"
)
CHARACTER_OBJECT_MATERIAL_COVERAGE_SUMMARY = (
    STAT_DIR / "187_character-object-material-coverage-summary.json"
)
DEFAULT_OUTPUT = STAT_DIR / "218_character-candidate-phase-gap-human-guide.md"
UPDATED_AT = "2026-06-30"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_values(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def unique_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            output.append(value)
    return output


def append_wrapped_bullet(lines: list[str], text: str) -> None:
    if len(text) <= 78:
        lines.append(f"- {text}")
        return
    words = text.split(" ")
    current = "- "
    for word in words:
        next_value = f"{current}{word}" if current == "- " else f"{current} {word}"
        if len(next_value) <= 78:
            current = next_value
            continue
        lines.append(current)
        current = f"  {word}"
    if current.strip():
        lines.append(current)


def build_markdown(root: Path) -> str:
    rows = read_csv_rows(root / CHECKLIST)
    first = rows[0]
    phase_statuses = [
        f"{row['corpus_area']}: {row['phase_name']} `{row['phase_status']}`"
        for row in rows
    ]
    dossier_slots = unique_values(
        [
            slot
            for row in rows
            for slot in split_values(row["required_character_dossier_slots"])
        ]
    )
    source_fields = unique_values(
        [
            field
            for row in rows
            for field in split_values(row["source_context_fields_to_verify"])
        ]
    )
    next_checks = unique_values(
        [
            check
            for row in rows
            for check in split_values(row["concrete_next_checks"])
        ]
    )

    slot_labels = {
        "glyph_image": "glyph image",
        "glyph_observation": "glyph observation",
        "variant_forms": "variant forms",
        "near_forms": "near forms",
        "component_clues": "component clues",
        "inscription_occurrence": "inscription occurrence",
        "inscription_context": "inscription context",
        "plate_route": "plate",
        "catalog_number": "catalog number",
        "heji_number": "Heji number",
        "findspot": "findspot",
        "collection": "collection",
        "period": "period",
        "group": "group",
        "source_evidence": "source evidence",
        "decipherment_history": "decipherment history",
        "dispute_notes": "dispute notes",
        "later_script_routes": "later script routes",
        "missing_items": "missing items",
        "next_sources_to_check": "next sources to check",
    }

    lines = [
        "# Character Candidate Phase Gap Human Guide /",
        "单字候选阶段缺口人工复核指南",
        "",
        "English:",
        "This guide is the human entrance for oracle-character and",
        "undeciphered-character candidate phase gaps. It sends reviewers",
        "back to concrete `obs-char-*` and `obs-unk-*` object folders,",
        "where glyph images, observations, variants, near forms,",
        "components, inscription context, plates, catalog numbers,",
        "findspot, collection, period, group, sources, reading history,",
        "disputes, and next sources must be checked by people.",
        "It is not a rights decision, not candidate promotion,",
        "not formal character import, not a character identity claim,",
        "not confirmed scholarship, and not a decipherment conclusion.",
        "",
        "简体中文：",
        "本指南是甲骨单字候选和未释字候选阶段缺口的人工入口。",
        "复核者应回到具体 `obs-char-*` 或 `obs-unk-*` 对象目录，",
        "先看字形图片、观察记录、异体、近形、构件线索、",
        "卜辞语境、图版、著录号、出土地、馆藏、时期、组类、",
        "来源证据、释读史、争议和下一步待查来源。",
        "它不是权利决定，不是候选提升，不是正式单字导入，",
        "不是字形身份结论，不是已确认学术结论，也不是释读结论。",
        "",
        "## Summary / 摘要",
        "",
        f"- updated at: {UPDATED_AT}",
        f"- checklist rows: {len(rows)}",
        f"- HUST promotion review rows: {first['hust_promotion_review_count']}",
        "- candidate evidence request rows: "
        f"{first['candidate_evidence_request_count']}",
        f"- undeciphered index rows: {first['undeciphered_index_count']}",
        "- undeciphered review queue rows: "
        f"{first['undeciphered_review_queue_count']}",
        "- undeciphered evidence readiness rows: "
        f"{first['undeciphered_evidence_readiness_count']}",
        "- character object material audit rows: "
        f"{first['character_object_material_audit_count']}",
        "- source ids:",
    ]
    for source_id in split_values(first["source_ids"]):
        lines.append(f"  - `{source_id}`")
    lines.append("- phase gap statuses:")
    for status in phase_statuses:
        lines.append(f"  - {status}")

    lines.extend(
        [
            "",
            "## Human Review Entry Order / 人工复核入口顺序",
            "",
            "1. Open the concrete character object directory first.",
            "2. Open a sample `obs-char-*` or `obs-unk-*` folder.",
            "3. Read the human README, dossier, and review sheet.",
            "4. Inspect glyph images, rubbings, photos, and plates.",
            "5. Check variants, near forms, and component clues.",
            "6. Check inscription occurrence and surrounding context.",
            "7. Check catalog number, Heji number, findspot, collection,",
            "   period, group, and batch evidence.",
            "8. Check source evidence, rights status, risk note, and review.",
            "9. Check decipherment history, proposer, disagreement, dispute.",
            "10. Write unresolved items as concrete next-source questions.",
            "11. Open support files only after the human object dossier.",
            "12. Do not promote candidates from this guide.",
            "",
            "人工复核时，先打开具体单字或未释字对象目录，",
            "再看人类 README、研究档案和复核表。",
            "清单、索引和统计只帮助定位对象，不能替代人工档案。",
            "",
            "## Support Files / 辅助文件",
            "",
            "| File | Path |",
            "| --- | --- |",
            f"| checklist | `{CHECKLIST.as_posix()}` |",
            f"| action queue | `{ACTION_QUEUE.as_posix()}` |",
            f"| HUST promotion queue | `{HUST_PROMOTION_QUEUE.as_posix()}` |",
            "| HUST promotion buckets | "
            f"`{HUST_PROMOTION_BUCKET_SUMMARY.as_posix()}` |",
            "| candidate evidence requests | "
            f"`{CANDIDATE_EVIDENCE_REQUEST_QUEUE.as_posix()}` |",
            f"| undeciphered index | `{UNDECIPHERED_INDEX.as_posix()}` |",
            "| undeciphered review queue | "
            f"`{UNDECIPHERED_REVIEW_QUEUE.as_posix()}` |",
            "| undeciphered readiness | "
            f"`{UNDECIPHERED_EVIDENCE_READINESS_CHECKLIST.as_posix()}` |",
            "| character material audit | "
            f"`{CHARACTER_OBJECT_MATERIAL_COVERAGE_AUDIT.as_posix()}` |",
            "| character material summary | "
            f"`{CHARACTER_OBJECT_MATERIAL_COVERAGE_SUMMARY.as_posix()}` |",
            "",
            "Open these files after the object-local human materials.",
            "They are review pointers, not evidence or scholarship by themselves.",
            "",
            "## Required Character Dossier Slots / 单字档案槽位",
            "",
        ]
    )
    for slot in dossier_slots:
        lines.append(f"- {slot_labels.get(slot, slot)}")

    lines.extend(
        [
            "",
            "Every opened candidate folder should let a researcher see",
            "what is present, what is only a candidate, what is disputed,",
            "and which exact source must be checked next.",
            "每个候选目录都应让研究者看清已有什么、什么仍是候选、",
            "哪里存在争议，以及下一步必须打开哪一个具体来源。",
            "",
            "## Source Context Fields / 来源语境字段",
            "",
        ]
    )
    for field in source_fields:
        lines.append(f"- `{field}`")

    lines.extend(
        [
            "",
            "These fields support provenance review only.",
            "They do not confirm identity, reading, component, or correspondence.",
            "这些字段只服务来源复核，不确认字形身份、释读、构件或对应关系。",
            "",
            "## Concrete Questions To Check / 具体待查问题",
            "",
        ]
    )
    for check in next_checks:
        append_wrapped_bullet(lines, check)
    lines.extend(
        [
            "- Which glyph image, rubbing, photograph, or plate is visible?",
            "- Which inscription occurrence and context can be opened?",
            "- Which catalog number, Heji number, findspot, collection,",
            "  period, group, or batch evidence is still absent?",
            "- Which decipherment history, proposer, or dispute is documented?",
            "- Which source evidence and rights note must be opened next?",
            "- Which candidate is still only metadata or staging?",
            "- 哪张字形图片、拓片、照片或图版可以直接查看？",
            "- 哪条卜辞出现位置和上下文可以打开？",
            "- 还缺哪一个著录号、合集号、出土地、馆藏、时期、组类或批次？",
            "- 哪条释读史、提出者记录或争议已经有来源？",
            "- 下一步必须打开哪条来源证据和权利说明？",
            "- 哪个候选仍只是 metadata 或 staging？",
            "",
            "## Boundary / 边界",
            "",
            "Do not record reviewed outcomes in this guide.",
            "Do not treat a checklist row, queue row, object count,",
            "metadata packet, graph edge, or staging row as scholarship.",
            "Do not decide rights.",
            "Do not promote candidates.",
            "Do not import formal character records.",
            "Do not make a character identity claim.",
            "Do not write any candidate as confirmed scholarship.",
            "Do not write any candidate as a decipherment conclusion.",
            "",
            "不得在本指南中记录复核结论。",
            "不得把清单行、队列行、对象计数、metadata packet、",
            "图边或 staging 行当成学术结论。",
            "不得裁定权利，不得提升候选，不得导入正式单字记录。",
            "不得作出字形身份结论。",
            "不得把任何候选写成已确认学术结论或释读结论。",
            "",
        ]
    )
    return "\n".join(lines)


def write_markdown(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the character candidate phase gap human guide."
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    write_markdown(root / args.output, build_markdown(root))
    print(f"character_candidate_phase_gap_human_guide={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
