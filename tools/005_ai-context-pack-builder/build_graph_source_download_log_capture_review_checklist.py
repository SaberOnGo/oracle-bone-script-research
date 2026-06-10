#!/usr/bin/env python3
"""Build a review checklist for download-log capture scaffold rows."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


CAPTURE_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "035_ai-agent-graph-source-download-log-evidence-capture-scaffold.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "036_ai-agent-graph-source-download-log-capture-review-checklist.csv"
)
UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "evidence_collection_download_log_capture_review_checklist_not_scholarship"
OUTPUT_SCOPE = "graph_source_evidence_collection_download_log_capture_review_checklist_only"

CHECKS = [
    (
        "open_capture_row",
        "Open the 035 download-log capture row before editing any download-log evidence fields.",
        "先打开 035 下载日志 capture row，再编辑任何下载日志证据字段。",
    ),
    (
        "open_download_log_row",
        "Open the cited download-log row and verify source_id before copying evidence.",
        "打开被引用的下载日志行，并在复制证据前核对 source_id。",
    ),
    (
        "verify_download_id_and_url",
        "Copy download_id and URL only from the download log; leave evidence blank if no matching row is found.",
        "download_id 和 URL 只能从下载日志复制；未找到匹配行时保持证据字段空白。",
    ),
    (
        "verify_download_and_http_status",
        "Record download status and HTTP status only from the download log, not from memory or route labels.",
        "下载状态和 HTTP 状态只能从下载日志记录，不得凭记忆或 route 标签填写。",
    ),
    (
        "verify_file_size",
        "Record file size only from the download log and keep size_review_status not_started until reviewed.",
        "文件大小只能从下载日志记录，并在复核前保持 size_review_status 为 not_started。",
    ),
    (
        "verify_checksum",
        "Record checksum only from the download log and keep checksum_review_status not_started until reviewed.",
        "checksum 只能从下载日志记录，并在复核前保持 checksum_review_status 为 not_started。",
    ),
    (
        "verify_local_temp_path_and_risk",
        "Verify local temp path and risk note from the download log; temporary files must stay in ignored directories.",
        "从下载日志核对本地临时路径和风险说明；临时文件必须留在已忽略目录。",
    ),
    (
        "block_rights_inference",
        "Do not infer rights status from download success, HTTP status, file size, checksum, or local file presence.",
        "不得从下载成功、HTTP 状态、文件大小、checksum 或本地文件存在推断权利状态。",
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
    "download_log_evidence_status",
    "checksum_review_status",
    "size_review_status",
    "access_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "decipherment_claim_status",
    "source_download_log_path",
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
        "checklist_item_id": f"graph-source-evidence-download-log-check-{index:03d}",
        "capture_row_id": row["capture_row_id"],
        "check_key": check_key,
        "source_id": row["source_id"],
        "primary_external_ref_id": row["primary_external_ref_id"],
        "target_evidence_section": row["target_evidence_section"],
        "check_status": "not_started",
        "review_status": "needs_download_log_capture_review",
        "evidence_collection_status": "not_collected",
        "download_log_evidence_status": "not_collected",
        "checksum_review_status": "not_started",
        "size_review_status": "not_started",
        "access_review_status": "not_started",
        "rights_decision_status": "not_decided",
        "source_promotion_status": "not_promoted",
        "decipherment_claim_status": "no_claim",
        "source_download_log_path": row["source_download_log_path"],
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
            "Checklist item only. It does not contain collected evidence, a "
            "checksum review, a size review, an access review, a rights "
            "decision, source promotion, component or evolution-chain "
            "assignment, or decipherment conclusion."
        ),
    }


def build_review_checklist(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    checklist: list[dict[str, str]] = []
    for row in rows:
        if row.get("target_evidence_section") != "download_log":
            raise ValueError("review checklist only supports download_log rows")
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
