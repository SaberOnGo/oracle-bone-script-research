#!/usr/bin/env python3
"""Build a review checklist for source-register capture scaffold rows."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


CAPTURE_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "032_ai-agent-graph-source-source-register-evidence-capture-scaffold.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "033_ai-agent-graph-source-source-register-capture-review-checklist.csv"
)
UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "evidence_collection_source_register_capture_review_checklist_not_scholarship"
OUTPUT_SCOPE = "graph_source_evidence_collection_source_register_capture_review_checklist_only"

CHECKS = [
    (
        "open_capture_row",
        "Open the 032 capture row before editing any source-register evidence fields.",
        "先打开 032 capture row，再编辑任何来源登记证据字段。",
    ),
    (
        "open_source_register_row",
        "Open the cited source-register row and verify source_id before copying evidence.",
        "打开被引用的来源登记行，并在复制证据前核对 source_id。",
    ),
    (
        "verify_primary_external_ref",
        "Verify the primary external reference against the source-register row; leave evidence blank if not found.",
        "用来源登记行核对首选外部引用；未找到时保持证据字段空白。",
    ),
    (
        "verify_title_and_type",
        "Copy title and source type only from the source-register row, not from memory.",
        "title 和 source type 只能从来源登记行复制，不得凭记忆填写。",
    ),
    (
        "verify_rights_and_risk",
        "Record rights and risk only when the register row states them; do not infer rights from access or dataset labels.",
        "只有来源登记行明确记载时才记录权利和风险；不得从访问状态或数据集标签推断权利。",
    ),
    (
        "keep_capture_boundary",
        "Keep capture_status empty or reviewed metadata-only until source-marked evidence is recorded.",
        "在带来源标记的证据记录前，capture_status 保持空白或仅限已复核 metadata。",
    ),
    (
        "block_source_promotion",
        "Do not promote the source, staging row, graph edge, component relation, or evolution relation from this checklist.",
        "不得从本 checklist 提升来源、staging row、图谱边、构件关系或演化关系。",
    ),
    (
        "block_decipherment_claim",
        "Do not write a decipherment claim or AI hypothesis as scholarship from this checklist.",
        "不得从本 checklist 写入释读声明，也不得把 AI 假说写成学术结论。",
    ),
]

FIELDNAMES = [
    "checklist_item_id",
    "capture_row_id",
    "check_key",
    "source_id",
    "primary_external_ref_id",
    "target_evidence_section",
    "check_status",
    "review_status",
    "evidence_collection_status",
    "rights_decision_status",
    "source_promotion_status",
    "decipherment_claim_status",
    "source_register_path",
    "capture_scaffold_path",
    "note_draft_path",
    "route_files_to_open",
    "required_review_checks",
    "instruction",
    "instruction_zh",
    "updated_at",
    "research_boundary",
    "output_scope",
    "caution",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _checklist_item(
    index: int,
    row: dict[str, str],
    check_key: str,
    instruction: str,
    instruction_zh: str,
) -> dict[str, str]:
    return {
        "checklist_item_id": f"graph-source-evidence-source-register-check-{index:03d}",
        "capture_row_id": row["capture_row_id"],
        "check_key": check_key,
        "source_id": row["source_id"],
        "primary_external_ref_id": row["primary_external_ref_id"],
        "target_evidence_section": row["target_evidence_section"],
        "check_status": "not_started",
        "review_status": "needs_source_register_capture_review",
        "evidence_collection_status": "not_collected",
        "rights_decision_status": "not_decided",
        "source_promotion_status": "not_promoted",
        "decipherment_claim_status": "no_claim",
        "source_register_path": row["source_register_path"],
        "capture_scaffold_path": CAPTURE_SCAFFOLD.as_posix(),
        "note_draft_path": row["note_draft_path"],
        "route_files_to_open": row["route_files_to_open"],
        "required_review_checks": row["required_review_checks"],
        "instruction": instruction,
        "instruction_zh": instruction_zh,
        "updated_at": UPDATED_AT,
        "research_boundary": RESEARCH_BOUNDARY,
        "output_scope": OUTPUT_SCOPE,
        "caution": (
            "Checklist item only. It does not contain collected evidence, a rights "
            "decision, source promotion, component or evolution-chain assignment, "
            "or decipherment conclusion."
        ),
    }


def build_review_checklist(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    checklist: list[dict[str, str]] = []
    for row in rows:
        if row.get("target_evidence_section") != "source_register":
            raise ValueError("review checklist only supports source_register rows")
        for check_key, instruction, instruction_zh in CHECKS:
            checklist.append(
                _checklist_item(
                    len(checklist) + 1,
                    row,
                    check_key,
                    instruction,
                    instruction_zh,
                )
            )
    return checklist


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture-scaffold", default=str(CAPTURE_SCAFFOLD))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    checklist = build_review_checklist(read_csv_rows(root / args.capture_scaffold))
    write_csv(root / args.output, checklist)
    print(
        f"checklist_item_count={len(checklist)} "
        f"capture_row_count={len({row['capture_row_id'] for row in checklist})} "
        "check_status=not_started"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
