#!/usr/bin/env python3
"""Build a review checklist for OBM access-boundary capture rows."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


CAPTURE_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "083_ai-agent-xxt-obm-access-boundary-capture-scaffold.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "084_ai-agent-xxt-obm-access-boundary-capture-review-checklist.csv"
)
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "xxt_obm_access_boundary_capture_review_checklist_not_scholarship"
OUTPUT_SCOPE = "xxt_obm_access_boundary_capture_review_checklist_only"

CHECKS = [
    (
        "open_capture_row",
        "Open the 083 capture row before editing any OBM follow-up evidence fields.",
        "先打开 083 capture row，再编辑任何 OBM follow-up 证据字段。",
    ),
    (
        "open_queue_and_draft",
        "Open the 074 queue row, the 075 review-log draft, and all cited route files before recording any availability status.",
        "记录任何 availability 状态前，先打开 074 queue row、075 review-log draft 和全部引用的 route files。",
    ),
    (
        "verify_registered_source_and_download_rows",
        "Verify the source-register, download-manifest, and download-log rows before copying any access-boundary status.",
        "复制任何 access-boundary 状态前，先核对 source-register、download-manifest 和 download-log 行。",
    ),
    (
        "check_access_profile_availability_only",
        "Record only whether access-profile metadata is available from the reviewed route evidence.",
        "只记录经复核 route evidence 中是否可获得 access-profile metadata。",
    ),
    (
        "check_staging_availability_only",
        "Record only whether staged abbreviation metadata is available from the reviewed route evidence.",
        "只记录经复核 route evidence 中是否可获得已暂存的 abbreviation metadata。",
    ),
    (
        "check_route_file_status_only",
        "Record only route-file availability and access-boundary status, not source-table import or catalog confirmation.",
        "只记录 route-file availability 与 access-boundary 状态，不记录 source-table 导入或著录确认。",
    ),
    (
        "block_old_catalog_holding_assignment_and_decipherment_claims",
        "Do not write old-catalog confirmation, holding match, formal assignment, component, evolution-chain, or decipherment claims from this checklist.",
        "不得从本 checklist 写入旧著录确认、馆藏匹配、正式分配、构件、演化链或释读判断。",
    ),
]

FIELDNAMES = [
    "checklist_item_id",
    "capture_row_id",
    "check_key",
    "followup_task_id",
    "targeted_download_id",
    "artifact_kind",
    "check_status",
    "human_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "decipherment_claim_status",
    "capture_scaffold_path",
    "review_log_draft_path",
    "route_files_to_open",
    "required_review_sections",
    "required_next_checks",
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
        "checklist_item_id": f"xxt-obm-access-check-{index:03d}",
        "capture_row_id": row["capture_row_id"],
        "check_key": check_key,
        "followup_task_id": row["followup_task_id"],
        "targeted_download_id": row["targeted_download_id"],
        "artifact_kind": row["artifact_kind"],
        "check_status": "not_started",
        "human_review_status": "needs_followup_capture_review",
        "rights_decision_status": "not_decided",
        "source_promotion_status": "not_promoted",
        "identity_claim_status": "no_identity_claim",
        "decipherment_claim_status": "no_claim",
        "capture_scaffold_path": CAPTURE_SCAFFOLD.as_posix(),
        "review_log_draft_path": row["review_log_draft_path"],
        "route_files_to_open": row["route_files_to_open"],
        "required_review_sections": row["required_review_sections"],
        "required_next_checks": row["required_next_checks"],
        "instruction": instruction,
        "instruction_zh": instruction_zh,
        "updated_at": UPDATED_AT,
        "research_boundary": RESEARCH_BOUNDARY,
        "output_scope": OUTPUT_SCOPE,
        "caution": (
            "Checklist item only. It does not contain source evidence, an old-catalog confirmation, "
            "a holding or collection match, a formal assignment, or a decipherment conclusion."
        ),
    }


def build_review_checklist(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    checklist: list[dict[str, str]] = []
    for row in rows:
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
    rows = build_review_checklist(read_csv_rows(root / args.capture_scaffold))
    write_csv(root / args.output, rows)
    print(
        f"checklist_item_count={len(rows)} "
        f"capture_row_count={len({row['capture_row_id'] for row in rows})} "
        "check_status=not_started"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
