#!/usr/bin/env python3
"""Build human-readable review-log drafts for first-priority codepoint routes."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


CODEPOINT_CROSSWALK_REVIEW_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/"
    "041_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-queue.csv"
)
DEFAULT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/"
    "042_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-log-draft-manifest.csv"
)
ROUTE_AVAILABILITY_SNAPSHOT = Path(
    "corpus/009_statistics-and-derived-features/"
    "049_ai-agent-hust-obimd-evobc-codepoint-crosswalk-route-availability-snapshot.csv"
)
UPDATED_AT = "2026-06-10"
PRIORITY_RANK = "1"
PRIORITY_BUCKET = "both_obimd_and_evobc_codepoint_match"
MATCH_STATUS = "matched_obimd_and_evobc_by_codepoint"
DRAFT_STATUS = "draft_not_collected"
EVIDENCE_COLLECTION_STATUS = "not_collected"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
PROMOTION_STATUS = "not_promoted"
RESEARCH_BOUNDARY = "codepoint_crosswalk_review_log_draft_not_scholarship"
CAUTION_EN = (
    "This draft is a routing scaffold only. It is not source evidence, not a confirmed "
    "oracle-character identity, not an accepted reading, not a component assignment, "
    "not an evolution-chain assignment, and not a decipherment conclusion."
)
CAUTION_ZH = (
    "本草稿只是路由脚手架；不是来源证据，不是已确认的甲骨单字身份，"
    "不是已接受释读，不是构件判定，不是字形演化链判定，也不是释读结论。"
)

OUTPUT_FIELDS = [
    "review_log_draft_id",
    "codepoint_review_task_id",
    "context_pack_id",
    "crosswalk_candidate_id",
    "suggested_oracle_character_id",
    "promotion_queue_id",
    "priority_rank",
    "priority_bucket",
    "cross_source_status",
    "matched_source_ids",
    "hust_primary_external_ref_id",
    "hust_label_codepoints",
    "obimd_match_count",
    "obimd_candidate_main_character_ids",
    "evobc_match_count",
    "evobc_candidate_evolution_category_ids",
    "evobc_image_reference_count_total",
    "evobc_has_oracle_bone_refs_any",
    "route_availability_id",
    "hust_candidate_packet_id",
    "hust_candidate_packet_exists",
    "hust_packet_status",
    "hust_packet_review_status",
    "hust_packet_rights_status",
    "obimd_row_count",
    "obimd_source_uids",
    "obimd_review_statuses",
    "obimd_rights_statuses",
    "evobc_row_count",
    "evobc_source_category_ids",
    "evobc_has_bronze_refs_any",
    "evobc_has_seal_refs_any",
    "evobc_review_statuses",
    "evobc_rights_statuses",
    "source_register_match_count",
    "source_register_rights_statuses",
    "source_register_review_statuses",
    "download_log_match_count",
    "download_total_file_size_bytes",
    "download_checksum_present_count",
    "download_access_statuses",
    "route_file_count",
    "missing_route_file_count",
    "route_file_review_status",
    "availability_status",
    "route_availability_evidence_collection_status",
    "draft_path",
    "source_queue_path",
    "route_files_to_open",
    "required_evidence_sections",
    "required_next_checks",
    "draft_status",
    "evidence_collection_status",
    "identity_claim_status",
    "promotion_status",
    "research_boundary",
    "caution",
    "updated_at",
]

SECTION_LABELS = {
    "crosswalk_row": ("Codepoint Crosswalk Row", "codepoint 交叉表行"),
    "hust_candidate_packet": ("HUST Candidate Packet", "HUST 候选资料包"),
    "obimd_main_character_staging_row": ("OBIMD Main Character Staging Row", "OBIMD 主字暂存行"),
    "evobc_evolution_category_staging_row": ("EVOBC Evolution Category Staging Row", "EVOBC 演化类别暂存行"),
    "source_register": ("Source Register", "来源登记表"),
    "download_log": ("Download Log", "下载日志"),
    "rights_risk_boundary": ("Rights And Risk Boundary", "权利与风险边界"),
    "review_log": ("Review Log", "复核日志"),
}

SECTION_NOTES = {
    "crosswalk_row": (
        "Open 011 crosswalk row; compare HUST, OBIMD, and EVOBC IDs.",
        "打开 011 crosswalk 行，核对三方 ID。",
    ),
    "hust_candidate_packet": (
        "Open the HUST packet; treat packet fields as review routes.",
        "打开 HUST packet；字段只作复核路线。",
    ),
    "obimd_main_character_staging_row": (
        "Verify the OBIMD row; do not promote main-character matches.",
        "核对 OBIMD 行；不得提升主字匹配。",
    ),
    "evobc_evolution_category_staging_row": (
        "Verify EVOBC row and image refs; keep evolution links candidate.",
        "核对 EVOBC 行和图像引用；演化仅为候选。",
    ),
    "source_register": (
        "Verify source rows for HUST, OBIMD, EVOBC rights and risk.",
        "核对三方来源、权利和风险说明。",
    ),
    "download_log": (
        "Check access or download logs before using source evidence.",
        "使用证据前先查访问或下载日志。",
    ),
    "rights_risk_boundary": (
        "Record rights and risk limits before evidence capture.",
        "采集证据前记录权利和风险边界。",
    ),
    "review_log": (
        "Record no identity, reading, component, evolution, or claim.",
        "记录不作身份、释读、构件或演化结论。",
    ),
}

NEXT_CHECK_LABELS = {
    "open_codepoint_crosswalk_row": (
        "Open the cited codepoint crosswalk row.",
        "打开被引用的 codepoint 交叉表行。",
    ),
    "open_hust_candidate_packet": (
        "Open the HUST candidate packet.",
        "打开 HUST 候选资料包。",
    ),
    "open_obimd_main_character_staging_row": (
        "Open the OBIMD main-character staging row.",
        "打开 OBIMD 主字暂存行。",
    ),
    "open_evobc_evolution_category_staging_row": (
        "Open the EVOBC evolution-category staging row.",
        "打开 EVOBC 演化类别暂存行。",
    ),
    "verify_source_register_and_download_log_rights_risk": (
        "Check source rows, download log, rights, and risk before capture.",
        "记录证据前先复核来源登记、下载日志、权利状态和风险说明。",
    ),
    "record_no_identity_or_decipherment_claim": (
        "Record that this task makes no identity or decipherment claim.",
        "记录本任务不提出身份确认或释读结论。",
    ),
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _split_compact(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def _availability_by_task(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["codepoint_review_task_id"]: row for row in rows}


def _first_priority_rows(queue_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = [
        row
        for row in queue_rows
        if row["priority_rank"] == PRIORITY_RANK
        and row["priority_bucket"] == PRIORITY_BUCKET
        and row["cross_source_status"] == MATCH_STATUS
    ]
    rows.sort(key=lambda row: row["codepoint_review_task_id"])
    return rows


def build_draft_manifest_rows(
    queue_rows: list[dict[str, str]],
    availability_rows: list[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    availability_by_task = _availability_by_task(availability_rows or [])
    rows: list[dict[str, str]] = []
    for index, row in enumerate(_first_priority_rows(queue_rows), start=1):
        availability = availability_by_task.get(row["codepoint_review_task_id"], {})
        rows.append(
            {
                "review_log_draft_id": f"codepoint-crosswalk-review-log-draft-{index:03d}",
                "codepoint_review_task_id": row["codepoint_review_task_id"],
                "context_pack_id": row["context_pack_id"],
                "crosswalk_candidate_id": row["crosswalk_candidate_id"],
                "suggested_oracle_character_id": row["suggested_oracle_character_id"],
                "promotion_queue_id": row["promotion_queue_id"],
                "priority_rank": row["priority_rank"],
                "priority_bucket": row["priority_bucket"],
                "cross_source_status": row["cross_source_status"],
                "matched_source_ids": row["matched_source_ids"],
                "hust_primary_external_ref_id": row["hust_primary_external_ref_id"],
                "hust_label_codepoints": row["hust_label_codepoints"],
                "obimd_match_count": row["obimd_match_count"],
                "obimd_candidate_main_character_ids": row["obimd_candidate_main_character_ids"],
                "evobc_match_count": row["evobc_match_count"],
                "evobc_candidate_evolution_category_ids": row[
                    "evobc_candidate_evolution_category_ids"
                ],
                "evobc_image_reference_count_total": row["evobc_image_reference_count_total"],
                "evobc_has_oracle_bone_refs_any": row["evobc_has_oracle_bone_refs_any"],
                "route_availability_id": availability.get("route_availability_id", ""),
                "hust_candidate_packet_id": availability.get("hust_candidate_packet_id", ""),
                "hust_candidate_packet_exists": availability.get("hust_candidate_packet_exists", ""),
                "hust_packet_status": availability.get("hust_packet_status", ""),
                "hust_packet_review_status": availability.get("hust_packet_review_status", ""),
                "hust_packet_rights_status": availability.get("hust_packet_rights_status", ""),
                "obimd_row_count": availability.get("obimd_row_count", ""),
                "obimd_source_uids": availability.get("obimd_source_uids", ""),
                "obimd_review_statuses": availability.get("obimd_review_statuses", ""),
                "obimd_rights_statuses": availability.get("obimd_rights_statuses", ""),
                "evobc_row_count": availability.get("evobc_row_count", ""),
                "evobc_source_category_ids": availability.get("evobc_source_category_ids", ""),
                "evobc_has_bronze_refs_any": availability.get("evobc_has_bronze_refs_any", ""),
                "evobc_has_seal_refs_any": availability.get("evobc_has_seal_refs_any", ""),
                "evobc_review_statuses": availability.get("evobc_review_statuses", ""),
                "evobc_rights_statuses": availability.get("evobc_rights_statuses", ""),
                "source_register_match_count": availability.get("source_register_match_count", ""),
                "source_register_rights_statuses": availability.get("source_register_rights_statuses", ""),
                "source_register_review_statuses": availability.get("source_register_review_statuses", ""),
                "download_log_match_count": availability.get("download_log_match_count", ""),
                "download_total_file_size_bytes": availability.get("download_total_file_size_bytes", ""),
                "download_checksum_present_count": availability.get("download_checksum_present_count", ""),
                "download_access_statuses": availability.get("download_access_statuses", ""),
                "route_file_count": availability.get("route_file_count", ""),
                "missing_route_file_count": availability.get("missing_route_file_count", ""),
                "route_file_review_status": availability.get("route_file_review_status", ""),
                "availability_status": availability.get("availability_status", ""),
                "route_availability_evidence_collection_status": availability.get(
                    "evidence_collection_status", ""
                ),
                "draft_path": row["expected_output_path"],
                "source_queue_path": CODEPOINT_CROSSWALK_REVIEW_QUEUE.as_posix(),
                "route_files_to_open": row["route_files_to_open"],
                "required_evidence_sections": row["required_evidence_sections"],
                "required_next_checks": row["required_next_checks"],
                "draft_status": DRAFT_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "promotion_status": PROMOTION_STATUS,
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION_EN,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def _pair_lines(label: str, value: str) -> list[str]:
    if ";" in value:
        return [f"- {label}:"] + [f"  - `{part}`" for part in _split_compact(value)]
    return [f"- {label}: `{value}`"]


def _route_availability_snapshot_lines(row: dict[str, str]) -> list[str]:
    values = [
        ("Status", "not_collected_route_snapshot"),
        ("Route availability ID", row["route_availability_id"]),
        ("Source snapshot", ROUTE_AVAILABILITY_SNAPSHOT.as_posix()),
        ("Review task ID", row["codepoint_review_task_id"]),
        ("Crosswalk candidate ID", row["crosswalk_candidate_id"]),
        ("Suggested oracle character ID", row["suggested_oracle_character_id"]),
        ("HUST candidate packet ID", row["hust_candidate_packet_id"]),
        ("HUST packet exists", row["hust_candidate_packet_exists"]),
        ("HUST packet status", row["hust_packet_status"]),
        ("HUST packet review status", row["hust_packet_review_status"]),
        ("HUST packet rights status", row["hust_packet_rights_status"]),
        ("OBIMD row count", row["obimd_row_count"]),
        ("OBIMD source UIDs", row["obimd_source_uids"]),
        ("OBIMD review statuses", row["obimd_review_statuses"]),
        ("OBIMD rights statuses", row["obimd_rights_statuses"]),
        ("EVOBC row count", row["evobc_row_count"]),
        ("EVOBC source category IDs", row["evobc_source_category_ids"]),
        ("EVOBC has bronze refs", row["evobc_has_bronze_refs_any"]),
        ("EVOBC has seal refs", row["evobc_has_seal_refs_any"]),
        ("EVOBC review statuses", row["evobc_review_statuses"]),
        ("EVOBC rights statuses", row["evobc_rights_statuses"]),
        ("source_register_match_count", row["source_register_match_count"]),
        ("Source register rights statuses", row["source_register_rights_statuses"]),
        ("Source register review statuses", row["source_register_review_statuses"]),
        ("download_log_match_count", row["download_log_match_count"]),
        ("Download total file size bytes", row["download_total_file_size_bytes"]),
        ("download_checksum_present_count", row["download_checksum_present_count"]),
        ("Download access statuses", row["download_access_statuses"]),
        ("Route file count", row["route_file_count"]),
        ("Missing route file count", row["missing_route_file_count"]),
        ("Route file review status", row["route_file_review_status"]),
        ("Availability status", row["availability_status"]),
        ("Evidence collection status", row["route_availability_evidence_collection_status"]),
    ]
    lines: list[str] = []
    for label, value in values:
        lines.extend(_pair_lines(label, value))
    return lines


def _concrete_next_check_lines(row: dict[str, str]) -> list[str]:
    return [
        "- Which 011 crosswalk row proves the codepoint route?",
        "- Which HUST packet fields are source-marked review routes only?",
        "- Which OBIMD and EVOBC rows should be opened before comparison?",
        "- Which source-register and download-log rows prove rights and checksums?",
        "- Which Xiaoxuetang, OBM, or primary inscription context is still missing?",
        f"- Does `{row['crosswalk_candidate_id']}` remain unpromoted and undeciphered?",
    ]


def build_markdown(row: dict[str, str]) -> str:
    route_files = _split_compact(row["route_files_to_open"])
    evidence_sections = _split_compact(row["required_evidence_sections"])
    next_checks = _split_compact(row["required_next_checks"])
    lines = [
        "# Codepoint Crosswalk Review Log Draft / codepoint 交叉复核日志草稿",
        "",
        "## Status / 状态",
        "",
        f"- Review log draft ID / 复核日志草稿 ID: `{row['review_log_draft_id']}`",
        f"- Codepoint review task ID / codepoint 复核任务 ID: `{row['codepoint_review_task_id']}`",
        f"- Draft status / 草稿状态: `{DRAFT_STATUS}`",
        f"- Evidence collection status / 证据收集状态: `{EVIDENCE_COLLECTION_STATUS}`",
        f"- Identity claim status / 身份声明状态: `{IDENTITY_CLAIM_STATUS}`",
        f"- Promotion status / 提升状态: `{PROMOTION_STATUS}`",
        f"- Research boundary / 研究边界: `{RESEARCH_BOUNDARY}`",
        f"- Updated at / 更新时间: `{UPDATED_AT}`",
        "",
        "## Candidate Route / 候选路由",
        "",
        f"- Context pack ID / 上下文包 ID: `{row['context_pack_id']}`",
        f"- Crosswalk candidate ID / 交叉候选 ID: `{row['crosswalk_candidate_id']}`",
        f"- Suggested oracle character ID / 建议甲骨单字 ID: `{row['suggested_oracle_character_id']}`",
        f"- Promotion queue ID / 提升队列 ID: `{row['promotion_queue_id']}`",
        f"- Priority bucket / 优先级分组: `{row['priority_bucket']}`",
        f"- Cross-source status / 跨来源状态: `{row['cross_source_status']}`",
        f"- Matched source IDs / 命中来源 ID: `{row['matched_source_ids']}`",
        f"- HUST external ref / HUST 外部引用: `{row['hust_primary_external_ref_id']}`",
        f"- HUST label codepoints / HUST 标签 codepoint: `{row['hust_label_codepoints']}`",
        f"- OBIMD main candidates / OBIMD 主字候选: `{row['obimd_candidate_main_character_ids']}`",
        f"- EVOBC category candidates / EVOBC 类别候选: `{row['evobc_candidate_evolution_category_ids']}`",
        f"- EVOBC image reference count / EVOBC 图像引用数: `{row['evobc_image_reference_count_total']}`",
        f"- EVOBC has oracle-bone refs / EVOBC 是否含甲骨引用: `{row['evobc_has_oracle_bone_refs_any']}`",
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
            "English: These sections record route availability only; they are not source evidence or scholarship.",
            "",
            "简体中文：以下章节只记录路线可用性；不是来源证据，也不是学术结论。",
            "",
            "## Route Availability Snapshot / 路由可用性快照",
            "",
            *_route_availability_snapshot_lines(row),
            "",
            "## Concrete Next Checks / 具体下一步待查",
            "",
            *_concrete_next_check_lines(row),
            "",
        ]
    )
    for section in evidence_sections:
        label_en, label_zh = SECTION_LABELS.get(section, (section, section))
        lines.extend(
            [
                f"### {label_en} / {label_zh}",
                "",
                "- Status / 状态: `not_collected_route_snapshot`",
                "- Route snapshot / 路线快照: see `Route Availability Snapshot` above.",
                "- Notes / 备注:",
                f"  - English: {SECTION_NOTES[section][0]}",
                f"  - 简体中文：{SECTION_NOTES[section][1]}",
                "",
            ]
        )
    lines.extend(
        [
            "## Required Next Checks / 必需下一步检查",
            "",
        ]
    )
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
            "## Review Log / 复核日志",
            "",
            "- Status / 状态: `created_from_041_review_queue`",
            "- Evidence collection / 证据收集: `not_collected`",
            "- Decision / 决定: no identity, reading, component, evolution-chain, or decipherment decision.",
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


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown_drafts(root: Path, rows: list[dict[str, str]]) -> None:
    for row in rows:
        draft_path = root / row["draft_path"]
        draft_path.parent.mkdir(parents=True, exist_ok=True)
        draft_path.write_text(build_markdown(row), encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", default=str(CODEPOINT_CROSSWALK_REVIEW_QUEUE))
    parser.add_argument("--route-availability-snapshot", default=str(ROUTE_AVAILABILITY_SNAPSHOT))
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    args = parser.parse_args(argv)

    root = repo_root()
    queue_rows = read_csv_rows(root / args.queue)
    availability_rows = read_csv_rows(root / args.route_availability_snapshot)
    manifest_rows = build_draft_manifest_rows(queue_rows, availability_rows)
    write_markdown_drafts(root, manifest_rows)
    write_csv(root / args.manifest, manifest_rows)
    print(f"wrote={len(manifest_rows)} manifest={(root / args.manifest).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
