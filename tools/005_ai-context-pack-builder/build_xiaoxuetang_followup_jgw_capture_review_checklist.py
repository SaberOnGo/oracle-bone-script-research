#!/usr/bin/env python3
"""Build a review checklist for first-wave Xiaoxuetang JGW follow-up capture rows."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


CAPTURE_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "080_ai-agent-xiaoxuetang-followup-jgw-capture-scaffold.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "081_ai-agent-xiaoxuetang-followup-jgw-capture-review-checklist.csv"
)
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "xxt_followup_jgw_capture_review_checklist_not_scholarship"
OUTPUT_SCOPE = "xiaoxuetang_followup_jgw_capture_review_checklist_only"

CHECKS = [
    (
        "open_capture_row",
        "Open the 080 capture row before editing any JGW follow-up evidence fields.",
        "先打开 080 capture row，再编辑任何 JGW follow-up 证据字段。",
    ),
    (
        "open_handoff_and_route_files",
        "Open the 079 handoff row, review-log draft, and all cited route files before recording any availability status.",
        "记录任何 availability 状态前，先打开 079 handoff row、review-log 草稿和全部引用的 route files。",
    ),
    (
        "verify_registered_source_rows",
        "Verify the source-register, download-manifest, and download-log rows before copying any route status.",
        "复制任何路由状态前，先核对 source-register、download-manifest 和 download-log 行。",
    ),
    (
        "check_catalog_availability_only",
        "Record only whether catalog information is available from the reviewed route; leave the evidence field blank if unavailable.",
        "只记录经复核路由中是否可获得 catalog 信息；若不可得，则保持 evidence 字段空白。",
    ),
    (
        "check_heji_crosswalk_only",
        "Record only whether a Heji crosswalk is available from reviewed route evidence; do not infer one from filename tokens.",
        "只记录经复核路由证据中是否可获得 Heji 对照；不得从文件名 token 推断。",
    ),
    (
        "check_collection_match_only",
        "Record only whether a collection or holding match is explicitly available from reviewed route evidence.",
        "只记录经复核路由证据中是否明确可获得馆藏或收藏匹配。",
    ),
    (
        "check_inscription_context_only",
        "Record only whether full inscription context becomes available from the reviewed route, not a decipherment or reading claim.",
        "只记录经复核路由中是否可获得完整卜辞上下文，不记录释读或读法判断。",
    ),
    (
        "block_identity_and_decipherment_claims",
        "Do not write identity, assignment, component, evolution-chain, or decipherment claims from this checklist.",
        "不得从本 checklist 写入字形身份、正式分配、构件、演化链或释读判断。",
    ),
]

FIELDNAMES = [
    "checklist_item_id",
    "capture_row_id",
    "check_key",
    "followup_task_id",
    "targeted_download_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
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
        "checklist_item_id": f"xxt-jgw-followup-check-{index:03d}",
        "capture_row_id": row["capture_row_id"],
        "check_key": check_key,
        "followup_task_id": row["followup_task_id"],
        "targeted_download_id": row["targeted_download_id"],
        "unknown_candidate_id": row["unknown_candidate_id"],
        "primary_external_ref_id": row["primary_external_ref_id"],
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
            "Checklist item only. It does not contain collected evidence, a rights decision, "
            "a catalog or collection match, a formal assignment, or a decipherment conclusion."
        ),
    }


def build_review_checklist(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    checklist: list[dict[str, str]] = []
    for row in rows:
        if row.get("followup_family_id") != "xxt_jgw_tls_access_boundary_followup":
            raise ValueError("review checklist only supports Xiaoxuetang JGW capture rows")
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
