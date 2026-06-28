#!/usr/bin/env python3
"""Build metadata-backed review-log drafts for top HUST-OBC undeciphered candidates."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


REVIEW_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/"
    "051_ai-agent-hust-obc-undeciphered-candidate-review-queue.csv"
)
DEFAULT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/"
    "052_ai-agent-hust-obc-undeciphered-candidate-review-log-draft-manifest.csv"
)
REVIEW_ROUTE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "053_ai-agent-hust-obc-undeciphered-candidate-review-route-results.csv"
)
EVIDENCE_READINESS_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/"
    "060_ai-agent-hust-obc-undeciphered-candidate-evidence-readiness-checklist.csv"
)
UPDATED_AT = "2026-06-11"
TARGET_PRIORITY_BUCKET = "image_count_050_plus"
DRAFT_STATUS = "draft_not_collected"
EVIDENCE_COLLECTION_STATUS = "not_collected"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
PROMOTION_STATUS = "not_promoted"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_candidate_review_log_draft_not_scholarship"
CAUTION_EN = (
    "This draft is a routing scaffold only. It is not source evidence, not an accepted "
    "oracle-character identity, not a formal obs-char assignment, not a reading, not a "
    "component assignment, not an evolution-chain assignment, and not a decipherment "
    "conclusion."
)
CAUTION_ZH = (
    "本草稿只是路由脚手架；不是来源证据，不是已接受的甲骨单字身份，"
    "不是正式 obs-char 分配，不是释读，不是构件判定，不是字形演化链判定，"
    "也不是破译或释读结论。"
)

OUTPUT_FIELDS = [
    "review_log_draft_id",
    "undeciphered_review_task_id",
    "context_pack_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "source_id",
    "source_package_id",
    "evidence_download_id",
    "priority_rank",
    "priority_bucket",
    "source_group",
    "source_group_label",
    "source_class_id",
    "source_class_path",
    "source_image_count",
    "bucket_directory",
    "bucket_manifest_path",
    "candidate_packet_path",
    "draft_path",
    "source_queue_path",
    "route_files_to_open",
    "required_evidence_sections",
    "required_next_checks",
    "route_result_id",
    "route_file_review_status",
    "draft_log_status",
    "candidate_packet_status",
    "candidate_packet_review_status",
    "source_register_match_count",
    "source_register_provider",
    "source_register_authority_tier",
    "source_register_rights_status",
    "large_source_file_size_bytes",
    "large_source_checksum_sha256",
    "download_log_status",
    "download_log_http_status",
    "download_log_local_temp_path",
    "readiness_check_id",
    "candidate_packet_capture_result_id",
    "source_register_capture_result_id",
    "download_log_capture_result_id",
    "large_source_register_capture_result_id",
    "captured_section_count",
    "required_section_count",
    "candidate_packet_evidence_status",
    "source_register_evidence_status",
    "download_log_evidence_status",
    "large_source_register_evidence_status",
    "overall_readiness_status",
    "missing_required_sections",
    "blocking_issue_count",
    "large_source_checksum_sha256_present",
    "checklist_status",
    "evidence_pack_action",
    "draft_status",
    "evidence_collection_status",
    "decipherment_status",
    "identity_claim_status",
    "assignment_status",
    "promotion_status",
    "rights_decision_status",
    "source_promotion_status",
    "research_boundary",
    "rights_status",
    "risk_note",
    "caution",
    "updated_at",
]

SECTION_LABELS = {
    "undeciphered_index_row": ("Undeciphered Index Row", "未释读候选索引行"),
    "bucket_manifest_row": ("Bucket Manifest Row", "分桶 manifest 行"),
    "candidate_packet": ("Candidate Packet", "候选资料包"),
    "source_register_row": ("Source Register Row", "来源登记行"),
    "large_source_register_row": ("Large Source Register Row", "大型来源登记行"),
    "download_log_row": ("Download Log Row", "下载日志行"),
    "rights_risk_boundary": ("Rights And Risk Boundary", "权利与风险边界"),
    "review_log": ("Review Log", "复核日志"),
}

SECTION_NOTES = {
    "undeciphered_index_row": (
        "Open the cited index row; verify candidate ID, image count, route, and review status.",
        "打开被引用索引行；核对候选 ID、图片数量、路线和复核状态。",
    ),
    "bucket_manifest_row": (
        "Open the bucket manifest row; confirm bucket range, path, image count, and status.",
        "打开分桶 manifest 行；确认分桶区间、路径、图片数量和状态。",
    ),
    "candidate_packet": (
        "Open the local packet; verify glyph image routes, source refs, rights, and gaps.",
        "打开本地资料包；核对字形图片路线、来源引用、权利和缺失项。",
    ),
    "source_register_row": (
        "Open the source register row; verify source ID, provider, rights status, and risk note.",
        "打开来源登记行；核对来源 ID、提供方、权利状态和风险说明。",
    ),
    "large_source_register_row": (
        "Open the large-source row; confirm raw storage, checksum, size, and derivatives.",
        "打开大型来源登记行；确认原始存放、checksum、大小和派生记录。",
    ),
    "download_log_row": (
        "Open the download log row; verify access date, size, checksum, and package name.",
        "打开下载日志行；核对访问日期、大小、checksum 和来源包名称。",
    ),
    "rights_risk_boundary": (
        "Compare register and download rights fields before any public asset decision.",
        "公开资产或派生文本前，对照登记和下载日志中的权利字段。",
    ),
    "review_log": (
        "Record only source-marked observations; keep identity and reading claims empty.",
        "只记录带来源标记的观察；保持身份和释读结论为空。",
    ),
}

NEXT_CHECK_LABELS = {
    "open_undeciphered_index_row": (
        "Open the cited undeciphered-candidate index row.",
        "打开被引用的未释读候选索引行。",
    ),
    "open_bucket_manifest_row": (
        "Open the cited bucket manifest row.",
        "打开被引用的分桶 manifest 行。",
    ),
    "open_candidate_packet": (
        "Open the local undeciphered-candidate packet.",
        "打开本地未释读候选资料包。",
    ),
    "verify_source_register_and_large_source_register": (
        "Verify source register and large-source register rows before evidence capture.",
        "记录证据前先复核来源登记和大型来源登记行。",
    ),
    "verify_download_log_checksum_size_and_risk_note": (
        "Verify download-log size, checksum, access, and risk note.",
        "复核下载日志中的大小、checksum、访问状态和风险说明。",
    ),
    "record_no_identity_assignment_or_decipherment_claim": (
        "Record that this task makes no identity, assignment, reading, or decipherment claim.",
        "记录本任务不提出身份、分配、释读或破译结论。",
    ),
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _split_compact(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def _target_rows(queue_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = [
        row
        for row in queue_rows
        if row["priority_bucket"] == TARGET_PRIORITY_BUCKET
        and row["priority_rank"] == "1"
        and row["evidence_collection_status"] == EVIDENCE_COLLECTION_STATUS
        and row["identity_claim_status"] == IDENTITY_CLAIM_STATUS
    ]
    rows.sort(key=lambda row: row["undeciphered_review_task_id"])
    return rows


def _index_by_draft_id(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["review_log_draft_id"]: row for row in rows}


def _copy_fields(row: dict[str, str], fields: list[str]) -> dict[str, str]:
    return {field: row.get(field, "") for field in fields}


def _field_lines(row: dict[str, str], fields: list[str]) -> list[str]:
    lines: list[str] = []
    for field in fields:
        value = row.get(field, "")
        lines.append(f"- `{field}`: `{value}`")
    return lines


def _metadata_snapshot_lines(row: dict[str, str]) -> list[str]:
    lines = [
        "## Metadata Snapshot / Metadata Snapshot",
        "",
        "These values are copied from reviewed route-result rows for human checking.",
        "",
    ]
    lines.extend(_field_lines(row, ROUTE_SNAPSHOT_FIELDS))
    lines.extend(
        [
            "",
            "## Evidence Readiness Snapshot / Evidence Readiness Snapshot",
            "",
            "These values summarize metadata capture readiness only; they are not evidence conclusions.",
            "",
        ]
    )
    lines.extend(_field_lines(row, READINESS_SNAPSHOT_FIELDS))
    return lines


def _concrete_next_check_lines(row: dict[str, str], next_checks: list[str]) -> list[str]:
    lines = [
        "## Concrete Next Checks / Concrete Next Checks",
        "",
        "- Open the 053 route-result row and verify every local route before adding evidence.",
        "- Open the 060 readiness row and cross-check 056, 057, 058, and 059 capture rows.",
        "- Cross-check Xiaoxuetang, OBIMD, Heji, or primary inscription context before any identity or reading claim.",
    ]
    for check in next_checks:
        label_en, label_zh = NEXT_CHECK_LABELS.get(check, (check, check))
        lines.extend(
            [
                f"- `{check}`",
                f"  - English: {label_en}",
                f"  - Simplified Chinese: {label_zh}",
            ]
        )
    readiness_checks = _split_compact(row.get("required_next_checks", ""))
    for check in readiness_checks:
        if check not in next_checks:
            lines.append(f"- `{check}`")
    return lines


ROUTE_SNAPSHOT_FIELDS = [
    "route_result_id",
    "route_file_review_status",
    "draft_log_status",
    "candidate_packet_status",
    "candidate_packet_review_status",
    "source_register_match_count",
    "source_register_provider",
    "source_register_authority_tier",
    "source_register_rights_status",
    "large_source_file_size_bytes",
    "large_source_checksum_sha256",
    "download_log_status",
    "download_log_http_status",
    "download_log_local_temp_path",
]

READINESS_SNAPSHOT_FIELDS = [
    "readiness_check_id",
    "candidate_packet_capture_result_id",
    "source_register_capture_result_id",
    "download_log_capture_result_id",
    "large_source_register_capture_result_id",
    "captured_section_count",
    "required_section_count",
    "candidate_packet_evidence_status",
    "source_register_evidence_status",
    "download_log_evidence_status",
    "large_source_register_evidence_status",
    "overall_readiness_status",
    "missing_required_sections",
    "blocking_issue_count",
    "large_source_checksum_sha256_present",
    "checklist_status",
    "evidence_pack_action",
]


def build_draft_manifest_rows(
    queue_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    readiness_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    route_by_draft_id = _index_by_draft_id(route_rows)
    readiness_by_draft_id = _index_by_draft_id(readiness_rows)
    rows: list[dict[str, str]] = []
    for index, row in enumerate(_target_rows(queue_rows), start=1):
        draft_id = f"hust-obc-undeciphered-review-log-draft-{index:04d}"
        route_row = route_by_draft_id[draft_id]
        readiness_row = readiness_by_draft_id[draft_id]
        rows.append(
            {
                "review_log_draft_id": draft_id,
                "undeciphered_review_task_id": row["undeciphered_review_task_id"],
                "context_pack_id": row["context_pack_id"],
                "unknown_candidate_id": row["unknown_candidate_id"],
                "primary_external_ref_id": row["primary_external_ref_id"],
                "source_id": row["source_id"],
                "source_package_id": row["source_package_id"],
                "evidence_download_id": row["evidence_download_id"],
                "priority_rank": row["priority_rank"],
                "priority_bucket": row["priority_bucket"],
                "source_group": row["source_group"],
                "source_group_label": row["source_group_label"],
                "source_class_id": row["source_class_id"],
                "source_class_path": row["source_class_path"],
                "source_image_count": row["source_image_count"],
                "bucket_directory": row["bucket_directory"],
                "bucket_manifest_path": row["bucket_manifest_path"],
                "candidate_packet_path": row["candidate_packet_path"],
                "draft_path": row["expected_output_path"],
                "source_queue_path": REVIEW_QUEUE.as_posix(),
                "route_files_to_open": row["route_files_to_open"],
                "required_evidence_sections": row["required_evidence_sections"],
                "required_next_checks": row["required_next_checks"],
                **_copy_fields(route_row, ROUTE_SNAPSHOT_FIELDS),
                **_copy_fields(readiness_row, READINESS_SNAPSHOT_FIELDS),
                "draft_status": DRAFT_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "decipherment_status": row["decipherment_status"],
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "assignment_status": ASSIGNMENT_STATUS,
                "promotion_status": PROMOTION_STATUS,
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "research_boundary": RESEARCH_BOUNDARY,
                "rights_status": row["rights_status"],
                "risk_note": row["risk_note"],
                "caution": CAUTION_EN,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def build_markdown(row: dict[str, str]) -> str:
    route_files = _split_compact(row["route_files_to_open"])
    evidence_sections = _split_compact(row["required_evidence_sections"])
    next_checks = _split_compact(row["required_next_checks"])
    lines = [
        "# HUST-OBC Undeciphered Candidate Review Log Draft / HUST-OBC 未释读候选复核日志草稿",
        "",
        "## Status / 状态",
        "",
        f"- Review log draft ID / 复核日志草稿 ID: `{row['review_log_draft_id']}`",
        f"- Undeciphered review task ID / 未释读复核任务 ID: `{row['undeciphered_review_task_id']}`",
        f"- Draft status / 草稿状态: `{DRAFT_STATUS}`",
        f"- Evidence collection status / 证据收集状态: `{EVIDENCE_COLLECTION_STATUS}`",
        f"- Identity claim status / 身份声明状态: `{IDENTITY_CLAIM_STATUS}`",
        f"- Assignment status / 分配状态: `{ASSIGNMENT_STATUS}`",
        f"- Promotion status / 提升状态: `{PROMOTION_STATUS}`",
        f"- Rights decision status / 权利决定状态: `{RIGHTS_DECISION_STATUS}`",
        f"- Source promotion status / 来源提升状态: `{SOURCE_PROMOTION_STATUS}`",
        f"- Research boundary / 研究边界: `{RESEARCH_BOUNDARY}`",
        f"- Updated at / 更新时间: `{UPDATED_AT}`",
        "",
        "## Candidate Route / 候选路由",
        "",
        f"- Context pack ID / 上下文包 ID: `{row['context_pack_id']}`",
        f"- Unknown candidate ID / 未知候选 ID: `{row['unknown_candidate_id']}`",
        f"- Primary external ref ID / 首选外部引用 ID: `{row['primary_external_ref_id']}`",
        f"- Source ID / 来源 ID: `{row['source_id']}`",
        f"- Source package ID / 来源包 ID: `{row['source_package_id']}`",
        f"- Evidence download ID / 证据下载 ID: `{row['evidence_download_id']}`",
        f"- Priority bucket / 优先级分组: `{row['priority_bucket']}`",
        f"- Source group / 来源组: `{row['source_group']}`",
        f"- Source group label / 来源组标签: `{row['source_group_label']}`",
        f"- Source class ID / 来源类别 ID: `{row['source_class_id']}`",
        f"- Source class path / 来源类别路径: `{row['source_class_path']}`",
        f"- Source image count / 来源图片数量: `{row['source_image_count']}`",
        f"- Bucket directory / 分桶目录: `{row['bucket_directory']}`",
        f"- Candidate packet path / 候选资料包路径: `{row['candidate_packet_path']}`",
        "",
        "## Route Files To Open / 待打开路由文件",
        "",
    ]
    lines.extend(f"- `{route_file}`" for route_file in route_files)
    lines.extend(
        [
            "",
            "## Evidence Sections / 证据章节",
            "",
            "English: All sections are deliberately empty until source-marked evidence is collected.",
            "",
            "简体中文：所有章节在收集带来源标记的证据前都必须保持为空。",
            "",
        ]
    )
    for section in evidence_sections:
        label_en, label_zh = SECTION_LABELS.get(section, (section, section))
        note_en, note_zh = SECTION_NOTES.get(
            section,
            ("Open routed evidence before recording notes.", "记录备注前先打开路由证据。"),
        )
        lines.extend(
            [
                f"### {label_en} / {label_zh}",
                "",
                "- Status / 状态: `not_collected`",
                "- Evidence items / 证据条目: none",
                "- Notes / 备注:",
                f"  - English: {note_en}",
                f"  - 简体中文：{note_zh}",
                "",
            ]
        )
    lines.extend(["## Required Next Checks / 必需下一步检查", ""])
    for check in next_checks:
        label_en, label_zh = NEXT_CHECK_LABELS.get(check, (check, check))
        lines.extend(
            [
                f"- `{check}`",
                f"  - English: {label_en}",
                f"  - 简体中文：{label_zh}",
            ]
        )
    lines.extend(
        [
            "",
            "## Rights And Risk / 权利与风险",
            "",
            f"- Rights status / 权利状态: `{row['rights_status']}`",
            f"- Risk note / 风险说明: {row['risk_note']}",
            "",
            "## Review Log / 复核日志",
            "",
            "- Status / 状态: `created_from_051_review_queue`",
            "- Evidence collection / 证据收集: `not_collected`",
            "- Decision / 决定: no identity, reading, obs-char assignment, component, evolution-chain, or decipherment decision.",
            "",
            "## Caution / 警示",
            "",
            f"English: {CAUTION_EN}",
            "",
            f"简体中文：{CAUTION_ZH}",
            "",
        ]
    )
    return "\n".join(lines)


def build_markdown(row: dict[str, str]) -> str:
    route_files = _split_compact(row["route_files_to_open"])
    evidence_sections = _split_compact(row["required_evidence_sections"])
    next_checks = _split_compact(row["required_next_checks"])
    lines = [
        "# HUST-OBC Undeciphered Candidate Review Log Draft / HUST-OBC 未释读候选复核日志草稿",
        "",
        "## Status / Status",
        "",
        f"- Review log draft ID: `{row['review_log_draft_id']}`",
        f"- Undeciphered review task ID: `{row['undeciphered_review_task_id']}`",
        f"- Draft status: `{DRAFT_STATUS}`",
        f"- Evidence collection status: `{EVIDENCE_COLLECTION_STATUS}`",
        f"- Identity claim status: `{IDENTITY_CLAIM_STATUS}`",
        f"- Assignment status: `{ASSIGNMENT_STATUS}`",
        f"- Promotion status: `{PROMOTION_STATUS}`",
        f"- Rights decision status: `{RIGHTS_DECISION_STATUS}`",
        f"- Source promotion status: `{SOURCE_PROMOTION_STATUS}`",
        f"- Research boundary: `{RESEARCH_BOUNDARY}`",
        f"- Updated at: `{UPDATED_AT}`",
        "",
        "## Candidate Route / Candidate Route",
        "",
        f"- Context pack ID: `{row['context_pack_id']}`",
        f"- Unknown candidate ID: `{row['unknown_candidate_id']}`",
        f"- Primary external ref ID: `{row['primary_external_ref_id']}`",
        f"- Source ID: `{row['source_id']}`",
        f"- Source package ID: `{row['source_package_id']}`",
        f"- Evidence download ID: `{row['evidence_download_id']}`",
        f"- Priority bucket: `{row['priority_bucket']}`",
        f"- Source group: `{row['source_group']}`",
        f"- Source group label: `{row['source_group_label']}`",
        f"- Source class ID: `{row['source_class_id']}`",
        f"- Source class path: `{row['source_class_path']}`",
        f"- Source image count: `{row['source_image_count']}`",
        f"- Bucket directory: `{row['bucket_directory']}`",
        f"- Candidate packet path: `{row['candidate_packet_path']}`",
        "",
        "## Route Files To Open / Route Files To Open",
        "",
    ]
    lines.extend(f"- `{route_file}`" for route_file in route_files)
    lines.extend([""])
    lines.extend(_metadata_snapshot_lines(row))
    lines.extend(
        [
            "",
            "## Evidence Sections / Evidence Sections",
            "",
            "English: Each section carries a metadata snapshot for human checking before evidence capture.",
            "",
            "Simplified Chinese: Check source-marked evidence before recording conclusions.",
            "",
        ]
    )
    for section in evidence_sections:
        label_en, label_zh = SECTION_LABELS.get(section, (section, section))
        note_en, note_zh = SECTION_NOTES.get(
            section,
            ("Open routed evidence before recording notes.", "Open routed evidence before recording notes."),
        )
        lines.extend(
            [
                f"### {label_en} / {label_zh}",
                "",
                "- Status: `not_collected_metadata_snapshot`",
                "- Metadata snapshot: route and readiness rows are listed above.",
                "- Human review task:",
                f"  - English: {note_en}",
                f"  - Simplified Chinese: {note_zh}",
                "",
            ]
        )
    lines.extend(_concrete_next_check_lines(row, next_checks))
    lines.extend(
        [
            "",
            "## Rights And Risk / Rights And Risk",
            "",
            f"- Rights status: `{row['rights_status']}`",
            f"- Risk note: {row['risk_note']}",
            "",
            "## Review Log / Review Log",
            "",
            "- Status: `created_from_051_review_queue`",
            "- Evidence collection: `not_collected`",
            "- Decision: no identity, reading, obs-char assignment, component, evolution-chain, or decipherment decision.",
            "",
            "## Caution / Caution",
            "",
            f"English: {CAUTION_EN}",
            "",
            f"Simplified Chinese: {CAUTION_ZH}",
            "",
        ]
    )
    return "\n".join(lines)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown_drafts(root: Path, rows: list[dict[str, str]]) -> None:
    for row in rows:
        output_path = root / row["draft_path"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(build_markdown(row), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", default=str(REVIEW_QUEUE))
    parser.add_argument("--route-results", default=str(REVIEW_ROUTE_RESULTS))
    parser.add_argument("--readiness-checklist", default=str(EVIDENCE_READINESS_CHECKLIST))
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    args = parser.parse_args(argv)

    root = repo_root()
    queue_rows = read_csv_rows(root / args.queue)
    route_rows = read_csv_rows(root / args.route_results)
    readiness_rows = read_csv_rows(root / args.readiness_checklist)
    manifest_rows = build_draft_manifest_rows(queue_rows, route_rows, readiness_rows)
    write_markdown_drafts(root, manifest_rows)
    write_csv(root / args.manifest, manifest_rows)
    print(f"wrote={len(manifest_rows)} manifest={(root / args.manifest).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
