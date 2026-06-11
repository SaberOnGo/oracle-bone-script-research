#!/usr/bin/env python3
"""Write source/asset metadata into HUST-OBC unknown-candidate collection notes."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_METADATA_CAPTURE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "064_ai-agent-hust-obc-undeciphered-candidate-source-metadata-evidence-capture-results.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "065_ai-agent-hust-obc-undeciphered-candidate-source-metadata-note-update-results.csv"
)
UPDATED_AT = "2026-06-11"
NOTE_STATUS = "metadata_captured_from_064"
EVIDENCE_COLLECTION_STATUS = "source_metadata_collected_metadata_only"
HUMAN_REVIEW_STATUS = "not_started"
FORMAL_SCHEMA_COMPATIBILITY_STATUS = "not_formal_obs_char_schema"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
NO_CLAIM = "no_claim"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_source_metadata_note_update_not_scholarship"
CAUTION_EN = (
    "This note records source-marked metadata copied from reviewed project rows. "
    "It is not a new download, not a raw image commit, not a checksum recalculation, "
    "not a rights decision, not source promotion, not an accepted glyph identity, "
    "not a formal obs-char assignment, not an accepted reading, not a component "
    "assignment, not an evolution-chain assignment, and not a decipherment conclusion."
)
CAUTION_ZH = (
    "本记录只写入从已复核项目行复制而来的带来源 metadata；不是重新下载，"
    "不是提交原始图片，不是重新计算 checksum，不是权利决定，不是来源提升，"
    "不是已接受的字形身份，不是正式 obs-char 分配，不是已接受释读，"
    "不是构件判定，不是演化链判定，也不是破译或释读结论。"
)

OUTPUT_FIELDS = [
    "note_update_result_id",
    "source_metadata_evidence_capture_result_id",
    "evidence_collection_note_draft_id",
    "evidence_collection_task_id",
    "evidence_pack_scaffold_id",
    "readiness_check_id",
    "route_result_id",
    "review_log_draft_id",
    "undeciphered_review_task_id",
    "context_pack_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "target_evidence_section",
    "note_draft_path",
    "source_register_capture_result_id",
    "download_log_capture_result_id",
    "large_source_register_capture_result_id",
    "candidate_packet_capture_result_id",
    "source_id",
    "download_id",
    "source_package_id",
    "source_class_path",
    "source_image_count",
    "source_reported_undeciphered_class_count",
    "zip_observed_undeciphered_class_count",
    "zip_observed_undeciphered_image_count",
    "evidence_item_count",
    "evidence_item_ids",
    "note_status",
    "evidence_collection_status",
    "human_review_status",
    "formal_schema_compatibility_status",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "assignment_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
    "research_boundary",
    "required_next_checks",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _list_items(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def _bullet_paths(value: str) -> list[str]:
    return [f"- `{item}`" for item in _list_items(value)]


def build_markdown(row: dict[str, str]) -> str:
    route_hints = _bullet_paths(row["route_hints"])
    route_files = _bullet_paths(row["route_files_to_open"])
    derived_paths = _bullet_paths(row["large_source_derived_record_paths"])
    lines = [
        "# HUST-OBC Undeciphered Candidate Source Metadata Collection Note / HUST-OBC 未释读候选来源 metadata 收集记录",
        "",
        "## Status / 状态",
        "",
        f"- Source metadata evidence capture result ID / 来源 metadata 证据捕获结果 ID: `{row['source_metadata_evidence_capture_result_id']}`",
        f"- Evidence collection note draft ID / 证据收集记录草稿 ID: `{row['evidence_collection_note_draft_id']}`",
        f"- Evidence collection task ID / 证据收集任务 ID: `{row['evidence_collection_task_id']}`",
        f"- Evidence pack scaffold ID / evidence-pack 脚手架 ID: `{row['evidence_pack_scaffold_id']}`",
        f"- Note status / 记录状态: `{NOTE_STATUS}`",
        f"- Evidence collection status / 证据收集状态: `{EVIDENCE_COLLECTION_STATUS}`",
        f"- Human review status / 人工复核状态: `{HUMAN_REVIEW_STATUS}`",
        f"- Formal schema compatibility / 正式 schema 兼容状态: `{FORMAL_SCHEMA_COMPATIBILITY_STATUS}`",
        f"- Identity claim status / 身份声明状态: `{IDENTITY_CLAIM_STATUS}`",
        f"- Assignment status / 分配状态: `{ASSIGNMENT_STATUS}`",
        f"- Decipherment claim status / 释读声明状态: `{NO_CLAIM}`",
        f"- Component claim status / 构件声明状态: `{NO_CLAIM}`",
        f"- Evolution-chain claim status / 演化链声明状态: `{NO_CLAIM}`",
        f"- Research boundary / 研究边界: `{RESEARCH_BOUNDARY}`",
        f"- Updated at / 更新时间: `{UPDATED_AT}`",
        "",
        "## Candidate Route / 候选路由",
        "",
        f"- Unknown candidate ID / 未知候选 ID: `{row['unknown_candidate_id']}`",
        f"- Primary external ref ID / 首选外部引用 ID: `{row['primary_external_ref_id']}`",
        f"- Readiness check ID / readiness check ID: `{row['readiness_check_id']}`",
        f"- Route result ID / 路由结果 ID: `{row['route_result_id']}`",
        f"- Review log draft ID / 复核日志草稿 ID: `{row['review_log_draft_id']}`",
        f"- Context pack ID / 上下文包 ID: `{row['context_pack_id']}`",
        f"- Target evidence section / 目标证据章节: `{row['target_evidence_section']}`",
        f"- Collection scope / 收集范围: `{row['task_collection_scope']}`",
        "",
        "## Route Hints / 路由提示",
        "",
        *route_hints,
        "",
        "## Route Files To Open / 待打开路由文件",
        "",
        *route_files,
        "",
        "## Source Register Metadata / 来源登记 metadata",
        "",
        f"- Source register capture result ID / 来源登记捕获结果 ID: `{row['source_register_capture_result_id']}`",
        f"- Source ID / 来源 ID: `{row['source_id']}`",
        f"- Title / 题名: {row['source_title']}",
        f"- Provider / 提供方: {row['source_provider']}",
        f"- Authority tier / 权威层级: `{row['source_authority_tier']}`",
        f"- Source URL / 来源 URL: {row['source_url']}",
        f"- Scope / 范围: {row['source_scope']}",
        f"- Rights status / 权利状态: `{row['source_rights_status']}`",
        f"- Review status / 复核状态: `{row['source_review_status']}`",
        f"- Source register path / 来源登记路径: `{row['source_register_path']}`",
        f"- Risk note / 风险说明: {row['source_risk_note']}",
        "",
        "## Download Log Metadata / 下载日志 metadata",
        "",
        f"- Download log capture result ID / 下载日志捕获结果 ID: `{row['download_log_capture_result_id']}`",
        f"- Download ID / 下载 ID: `{row['download_id']}`",
        f"- URL / URL: {row['download_url']}",
        f"- Downloaded at / 下载时间: `{row['downloaded_at']}`",
        f"- Status / 状态: `{row['download_status']}`",
        f"- HTTP status / HTTP 状态: `{row['http_status']}`",
        f"- File size bytes / 文件大小字节数: `{row['download_file_size_bytes']}`",
        f"- SHA-256 / SHA-256: `{row['download_checksum_sha256']}`",
        f"- Local archive path / 本地归档路径: `{row['local_archive_path']}`",
        f"- Download log path / 下载日志路径: `{row['download_log_path']}`",
        f"- Risk note / 风险说明: {row['download_risk_note']}",
        "",
        "## Large Source Register Metadata / 大型来源登记 metadata",
        "",
        f"- Large source register capture result ID / 大型来源登记捕获结果 ID: `{row['large_source_register_capture_result_id']}`",
        f"- Source package ID / 来源包 ID: `{row['source_package_id']}`",
        f"- Title / 题名: {row['large_source_title']}",
        f"- Access method / 获取方式: {row['large_source_access_method']}",
        f"- Storage status / 存储状态: `{row['large_source_storage_status']}`",
        f"- Storage hint / 存储线索: `{row['large_source_storage_hint']}`",
        f"- Handling strategy / 处理策略: {row['large_source_handling_strategy']}",
        f"- Rights status / 权利状态: `{row['large_source_rights_status']}`",
        f"- Register path / 登记路径: `{row['large_source_register_path']}`",
        f"- Risk note / 风险说明: {row['large_source_risk_note']}",
        "",
        "### Derived Record Paths / 派生记录路径",
        "",
        *derived_paths,
        "",
        "## Candidate Packet Metadata / 候选包 metadata",
        "",
        f"- Candidate packet capture result ID / 候选包捕获结果 ID: `{row['candidate_packet_capture_result_id']}`",
        f"- Candidate packet path / 候选包路径: `{row['candidate_packet_path']}`",
        f"- Bucket manifest path / 分桶 manifest 路径: `{row['bucket_manifest_path']}`",
        f"- Undeciphered index path / 未释读索引路径: `{row['undeciphered_index_path']}`",
        f"- Source group / 来源组: `{row['source_group']}`",
        f"- Source group label / 来源组标签: {row['source_group_label']}",
        f"- Source class ID / 来源类别 ID: `{row['source_class_id']}`",
        f"- Source class path / 来源类别路径: `{row['source_class_path']}`",
        f"- Source image count / 来源图片数量: `{row['source_image_count']}`",
        f"- First source image path / 首个来源图片路径: `{row['first_source_image_path']}`",
        f"- Last source image path / 末个来源图片路径: `{row['last_source_image_path']}`",
        f"- Filename source prefixes / 文件名前缀: `{row['filename_source_prefixes']}`",
        f"- Bucket sequence / 分桶序号: `{row['bucket_sequence']}`",
        f"- Source-reported undeciphered class count / 来源报告未释读类别数: `{row['source_reported_undeciphered_class_count']}`",
        f"- Zip-observed undeciphered class count / zip 观测未释读类别数: `{row['zip_observed_undeciphered_class_count']}`",
        f"- Zip-observed undeciphered image count / zip 观测未释读图片数: `{row['zip_observed_undeciphered_image_count']}`",
        f"- Materialization status / 物化状态: `{row['candidate_materialization_status']}`",
        f"- Candidate packet review status / 候选包复核状态: `{row['candidate_packet_review_status']}`",
        "",
        "## Evidence Collection / 证据收集",
        "",
        "### Source References And Asset Metadata / 来源引用与资产 metadata",
        "",
        f"- Status / 状态: `{EVIDENCE_COLLECTION_STATUS}`",
        "- Evidence item count / 证据条目数量: `4`",
        "- Evidence item IDs / 证据条目 ID: "
        f"`{row['source_register_capture_result_id']};{row['download_log_capture_result_id']};"
        f"{row['large_source_register_capture_result_id']};{row['candidate_packet_capture_result_id']}`",
        "- Source-marked notes / 带来源标注备注: captured from reviewed 056, 057, 058, 059, and 064 rows only.",
        "",
        "## Review Log / 复核日志",
        "",
        "- Status / 状态: `metadata_captured_from_064`",
        "- Decision / 决定: metadata captured for later human review; no identity, reading, formal assignment, component, evolution-chain, rights, source-promotion, or decipherment decision.",
        "",
        "## Required Next Checks / 后续必查项",
        "",
        "- Open 064 capture result row / 打开 064 捕获结果行。",
        "- Cross-check against primary catalog or inscription context before any identity or decipherment claim / 在任何身份或释读声明前，先与一手著录或卜辞上下文交叉复核。",
        "- Keep raw HUST-OBC package outside regular Git / 保持 HUST-OBC 原始大包不进入普通 Git。",
        "",
        "## Caution / 警示",
        "",
        f"English: {CAUTION_EN}",
        "",
        f"简体中文：{CAUTION_ZH}",
        "",
    ]
    return "\n".join(lines)


def build_note_update_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        if row["target_evidence_section"] != "source_references_and_asset_metadata":
            raise ValueError(f"unexpected target evidence section: {row['target_evidence_section']}")
        evidence_ids = ";".join(
            [
                row["source_register_capture_result_id"],
                row["download_log_capture_result_id"],
                row["large_source_register_capture_result_id"],
                row["candidate_packet_capture_result_id"],
            ]
        )
        results.append(
            {
                "note_update_result_id": f"hust-obc-undeciphered-source-metadata-note-update-{index:04d}",
                "source_metadata_evidence_capture_result_id": row[
                    "source_metadata_evidence_capture_result_id"
                ],
                "evidence_collection_note_draft_id": row["evidence_collection_note_draft_id"],
                "evidence_collection_task_id": row["evidence_collection_task_id"],
                "evidence_pack_scaffold_id": row["evidence_pack_scaffold_id"],
                "readiness_check_id": row["readiness_check_id"],
                "route_result_id": row["route_result_id"],
                "review_log_draft_id": row["review_log_draft_id"],
                "undeciphered_review_task_id": row["undeciphered_review_task_id"],
                "context_pack_id": row["context_pack_id"],
                "unknown_candidate_id": row["unknown_candidate_id"],
                "primary_external_ref_id": row["primary_external_ref_id"],
                "target_evidence_section": row["target_evidence_section"],
                "note_draft_path": row["note_draft_path"],
                "source_register_capture_result_id": row["source_register_capture_result_id"],
                "download_log_capture_result_id": row["download_log_capture_result_id"],
                "large_source_register_capture_result_id": row["large_source_register_capture_result_id"],
                "candidate_packet_capture_result_id": row["candidate_packet_capture_result_id"],
                "source_id": row["source_id"],
                "download_id": row["download_id"],
                "source_package_id": row["source_package_id"],
                "source_class_path": row["source_class_path"],
                "source_image_count": row["source_image_count"],
                "source_reported_undeciphered_class_count": row[
                    "source_reported_undeciphered_class_count"
                ],
                "zip_observed_undeciphered_class_count": row["zip_observed_undeciphered_class_count"],
                "zip_observed_undeciphered_image_count": row["zip_observed_undeciphered_image_count"],
                "evidence_item_count": "4",
                "evidence_item_ids": evidence_ids,
                "note_status": NOTE_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "human_review_status": HUMAN_REVIEW_STATUS,
                "formal_schema_compatibility_status": FORMAL_SCHEMA_COMPATIBILITY_STATUS,
                "rights_decision_status": "no_new_rights_decision",
                "source_promotion_status": "not_promoted",
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "assignment_status": ASSIGNMENT_STATUS,
                "decipherment_claim_status": NO_CLAIM,
                "component_claim_status": NO_CLAIM,
                "evolution_chain_claim_status": NO_CLAIM,
                "research_boundary": RESEARCH_BOUNDARY,
                "required_next_checks": (
                    "open_064_capture_result;open_updated_source_metadata_note;"
                    "cross_check_against_primary_catalog_or_inscription_context_before_identity_or_decipherment_claim"
                ),
                "caution": CAUTION_EN,
                "updated_at": UPDATED_AT,
            }
        )
    return results


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown_notes(root: Path, rows: list[dict[str, str]]) -> None:
    for row in rows:
        path = root / row["note_draft_path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(build_markdown(row), encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-metadata-capture-results", default=str(SOURCE_METADATA_CAPTURE_RESULTS))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--skip-markdown", action="store_true")
    args = parser.parse_args(argv)

    root = repo_root()
    source_rows = read_csv_rows(root / args.source_metadata_capture_results)
    update_rows = build_note_update_rows(source_rows)
    if not args.skip_markdown:
        write_markdown_notes(root, source_rows)
    write_csv(root / args.output, update_rows)
    print(
        f"source_metadata_note_update_count={len(update_rows)} "
        f"markdown_written={str(not args.skip_markdown).lower()} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
