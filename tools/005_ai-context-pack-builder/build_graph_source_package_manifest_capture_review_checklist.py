#!/usr/bin/env python3
"""Build a review checklist for package-manifest capture scaffold rows."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


CAPTURE_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "038_ai-agent-graph-source-package-manifest-evidence-capture-scaffold.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "039_ai-agent-graph-source-package-manifest-capture-review-checklist.csv"
)
UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "evidence_collection_package_manifest_capture_review_checklist_not_scholarship"
OUTPUT_SCOPE = "graph_source_evidence_collection_package_manifest_capture_review_checklist_only"

CHECKS = [
    (
        "open_capture_row",
        "Open the 038 package-manifest capture row before editing any package-manifest evidence fields.",
        "先打开 038 package manifest capture row，再编辑任何 package manifest 证据字段。",
    ),
    (
        "open_package_manifest_row",
        "Open the cited source package file manifest row and verify source_id before copying evidence.",
        "打开被引用的来源包文件 manifest 行，并在复制证据前核对 source_id。",
    ),
    (
        "verify_package_file_and_source_package_ids",
        (
            "Copy package_file_id and source_package_id only from the source package file "
            "manifest; leave evidence blank if no matching row is found."
        ),
        (
            "package_file_id 和 source_package_id 只能从来源包文件 manifest 复制；"
            "未找到匹配行时保持证据字段空白。"
        ),
    ),
    (
        "verify_file_name_kind_and_url",
        "Record file name, file kind, and source URL only from the source package file manifest.",
        "文件名、文件类型和来源 URL 只能从来源包文件 manifest 记录。",
    ),
    (
        "verify_file_size_and_download_id",
        (
            "Record file size and download ID only from the source package file manifest "
            "and keep file_size_review_status not_started until reviewed."
        ),
        (
            "文件大小和 download ID 只能从来源包文件 manifest 记录，"
            "并在复核前保持 file_size_review_status 为 not_started。"
        ),
    ),
    (
        "verify_checksum_boundary",
        (
            "Keep checksum evidence blank unless a source-marked checksum is present; "
            "keep checksum_review_status not_started until reviewed."
        ),
        (
            "除非有带来源标记的 checksum，否则保持 checksum 证据字段空白；"
            "复核前保持 checksum_review_status 为 not_started。"
        ),
    ),
    (
        "verify_commit_policy_and_handling_strategy",
        (
            "Record commit policy and handling strategy only from the package manifest; "
            "do not infer repository safety from file size alone."
        ),
        (
            "提交策略和处理策略只能从 package manifest 记录；"
            "不得仅凭文件大小推断仓库安全性。"
        ),
    ),
    (
        "verify_rights_and_review_status_boundary",
        (
            "Record rights and review status only from the package manifest; "
            "do not turn them into a rights decision."
        ),
        "权利和复核状态只能从 package manifest 记录；不得把它们转换成权利决定。",
    ),
    (
        "block_source_promotion",
        (
            "Do not promote the source, package row, staging row, graph edge, component "
            "relation, or evolution relation from this checklist."
        ),
        "不得从本 checklist 提升来源、package row、staging row、图谱边、构件关系或演化关系。",
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
    "package_manifest_evidence_status",
    "file_size_review_status",
    "checksum_review_status",
    "storage_boundary_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "decipherment_claim_status",
    "source_package_file_manifest_path",
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
        "checklist_item_id": f"graph-source-evidence-package-manifest-check-{index:03d}",
        "capture_row_id": row["capture_row_id"],
        "check_key": check_key,
        "source_id": row["source_id"],
        "primary_external_ref_id": row["primary_external_ref_id"],
        "target_evidence_section": row["target_evidence_section"],
        "check_status": "not_started",
        "review_status": "needs_package_manifest_capture_review",
        "evidence_collection_status": "not_collected",
        "package_manifest_evidence_status": "not_collected",
        "file_size_review_status": "not_started",
        "checksum_review_status": "not_started",
        "storage_boundary_review_status": "not_started",
        "rights_decision_status": "not_decided",
        "source_promotion_status": "not_promoted",
        "decipherment_claim_status": "no_claim",
        "source_package_file_manifest_path": row["source_package_file_manifest_path"],
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
            "file-size review, a checksum review, a storage-boundary review, "
            "a rights decision, source promotion, component or evolution-chain "
            "assignment, or decipherment conclusion."
        ),
    }


def build_review_checklist(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    checklist: list[dict[str, str]] = []
    for row in rows:
        if row.get("target_evidence_section") != "package_manifest":
            raise ValueError("review checklist only supports package_manifest rows")
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
