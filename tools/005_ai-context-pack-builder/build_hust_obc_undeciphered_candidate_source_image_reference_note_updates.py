#!/usr/bin/env python3
"""Write source-image reference summaries into HUST-OBC inscription-context notes."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


PRECHECK_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "066_ai-agent-hust-obc-undeciphered-candidate-full-inscription-context-precheck-results.csv"
)
SOURCE_IMAGE_REFERENCE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/"
    "069_ai-agent-hust-obc-undeciphered-candidate-source-image-reference-extraction-summary.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "070_ai-agent-hust-obc-undeciphered-candidate-source-image-reference-note-update-results.csv"
)
UPDATED_AT = "2026-06-11"
NOTE_STATUS = "source_image_reference_summary_written_from_069"
EVIDENCE_COLLECTION_STATUS = (
    "full_inscription_context_not_collected_with_source_image_reference_paths_recorded"
)
HUMAN_REVIEW_STATUS = "not_started"
FORMAL_SCHEMA_COMPATIBILITY_STATUS = "not_formal_obs_char_schema"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
NO_CLAIM = "no_claim"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_source_image_reference_note_update_not_scholarship"
CAUTION_EN = (
    "This note records extracted source-image path metadata only. Filename number tokens "
    "are search hints only, not catalog confirmation, not proof of primary inscription "
    "context, not a Heji crosswalk, not an accepted glyph identity, not a formal obs-char "
    "assignment, not a rights decision, not source promotion, and not a decipherment conclusion."
)
CAUTION_ZH = (
    "本记录只写入已抽取的来源图片路径 metadata。文件名中的数字 token 仅可作为检索提示，"
    "不是著录确认，不是完整卜辞上下文证明，不是《合集》交叉索引，不是已接受字形身份，"
    "不是正式 obs-char 分配，不是权利决定，不是来源提升，也不是释读结论。"
)

OUTPUT_FIELDS = [
    "note_update_result_id",
    "source_image_reference_extraction_summary_id",
    "full_inscription_context_precheck_result_id",
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
    "source_id",
    "source_package_id",
    "download_id",
    "source_class_id",
    "source_class_path",
    "source_image_count_expected",
    "source_image_count_extracted",
    "source_image_count_match_status",
    "first_extracted_source_image_path",
    "last_extracted_source_image_path",
    "filename_source_prefixes",
    "filename_catalog_candidate_number_tokens",
    "filename_catalog_candidate_number_token_count",
    "filename_variant_sequence_token_count",
    "filename_token_interpretation_status",
    "detail_output_path",
    "summary_output_path",
    "registered_storage_hint",
    "resolved_local_archive_path",
    "local_archive_resolution_status",
    "primary_catalog_context_status",
    "heji_crosswalk_status",
    "old_catalog_context_status",
    "collection_context_status",
    "excavation_context_status",
    "transcription_context_status",
    "inscription_context_evidence_status",
    "route_precheck_status",
    "catalog_context_status",
    "source_rights_status",
    "large_source_rights_status",
    "risk_note",
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


def _bullet_items(value: str) -> list[str]:
    return [f"- `{item}`" for item in _list_items(value)]


def merge_rows(
    precheck_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    summary_by_precheck = {
        row["full_inscription_context_precheck_result_id"]: row for row in summary_rows
    }
    merged: list[dict[str, str]] = []
    for row in precheck_rows:
        precheck_id = row["full_inscription_context_precheck_result_id"]
        if precheck_id not in summary_by_precheck:
            raise ValueError(f"missing source-image summary for {precheck_id}")
        summary = summary_by_precheck[precheck_id]
        if row["unknown_candidate_id"] != summary["unknown_candidate_id"]:
            raise ValueError(f"unknown candidate mismatch for {precheck_id}")
        merged.append({**row, **summary})
    return merged


def build_markdown(row: dict[str, str]) -> str:
    next_sources = _bullet_items(row["next_registered_source_routes"])
    route_files = _bullet_items(row["route_files_to_open"])
    lines = [
        "# HUST-OBC Undeciphered Candidate Full Inscription Context Source Image Reference Summary / HUST-OBC 未释读候选完整卜辞上下文来源图片路径摘要",
        "",
        "## Status / 状态",
        "",
        f"- Full inscription context precheck result ID / 完整卜辞上下文预检结果 ID: `{row['full_inscription_context_precheck_result_id']}`",
        f"- Source image reference extraction summary ID / 来源图片路径抽取摘要 ID: `{row['source_image_reference_extraction_summary_id']}`",
        f"- Evidence collection task ID / 证据收集任务 ID: `{row['evidence_collection_task_id']}`",
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
        "## Candidate Route / 候选路径",
        "",
        f"- Unknown candidate ID / 未知候选 ID: `{row['unknown_candidate_id']}`",
        f"- Primary external ref ID / 首选外部引用 ID: `{row['primary_external_ref_id']}`",
        f"- Source ID / 来源 ID: `{row['source_id']}`",
        f"- Source package ID / 来源包 ID: `{row['source_package_id']}`",
        f"- Download ID / 下载 ID: `{row['download_id']}`",
        f"- Source class path / 来源类别路径: `{row['source_class_path']}`",
        "",
        "## Source Image Reference Extraction Summary / 来源图片路径抽取摘要",
        "",
        f"- Source image count expected / 预期来源图片数量: `{row['source_image_count_expected']}`",
        f"- Source image count extracted / 已抽取来源图片数量: `{row['source_image_count_extracted']}`",
        f"- Source image count match status / 数量匹配状态: `{row['source_image_count_match_status']}`",
        f"- First extracted source image path / 首个已抽取来源图片路径: `{row['first_extracted_source_image_path']}`",
        f"- Last extracted source image path / 末个已抽取来源图片路径: `{row['last_extracted_source_image_path']}`",
        f"- Filename source prefixes / 文件名前缀: `{row['filename_source_prefixes']}`",
        f"- Filename catalog candidate number tokens / 文件名候选编号 token: `{row['filename_catalog_candidate_number_tokens']}`",
        f"- Filename catalog candidate number token count / 文件名候选编号 token 数: `{row['filename_catalog_candidate_number_token_count']}`",
        f"- Filename variant sequence token count / 文件名变体序列 token 数: `{row['filename_variant_sequence_token_count']}`",
        f"- Filename token interpretation status / 文件名 token 解释状态: `{row['filename_token_interpretation_status']}`",
        f"- Detail output path / 明细输出路径: `{row['detail_output_path']}`",
        f"- Summary output path / 摘要输出路径: `{SOURCE_IMAGE_REFERENCE_SUMMARY.as_posix()}`",
        f"- Local archive resolution / 本地归档解析状态: `{row['local_archive_resolution_status']}`",
        f"- Registered storage hint / 已登记存储线索: `{row['registered_storage_hint']}`",
        f"- Resolved local archive path / 解析后的本地归档路径: `{row['resolved_local_archive_path']}`",
        "",
        "## Catalog And Inscription Context Boundary / 著录与卜辞上下文边界",
        "",
        f"- Primary catalog context status / 一手著录上下文状态: `{row['primary_catalog_context_status']}`",
        f"- Catalog context status / 著录上下文状态: `{row['catalog_context_status']}`",
        f"- Heji crosswalk status / 《合集》交叉索引状态: `{row['heji_crosswalk_status']}`",
        f"- Old catalog context status / 旧著录上下文状态: `{row['old_catalog_context_status']}`",
        f"- Collection context status / 馆藏上下文状态: `{row['collection_context_status']}`",
        f"- Excavation context status / 出土上下文状态: `{row['excavation_context_status']}`",
        f"- Transcription context status / 释文上下文状态: `{row['transcription_context_status']}`",
        f"- Inscription context evidence status / 卜辞上下文证据状态: `{row['inscription_context_evidence_status']}`",
        f"- Route precheck status / 路线预检状态: `{row['route_precheck_status']}`",
        "",
        "## Registered Source Routes To Search Next / 下一步应检索的已登记来源路线",
        "",
        *next_sources,
        "",
        "## Route Files To Open / 待打开路径文件",
        "",
        *route_files,
        "",
        "## Required Next Checks / 后续必查项",
        "",
        "- Open 069 summary row and 068 detail rows before using any filename token / 在使用任何文件名 token 前先打开 069 摘要行和 068 明细行。",
        "- Treat filename number tokens as search hints only, not catalog confirmation / 把文件名数字 token 仅作为检索提示，不得当作著录确认。",
        "- Search registered catalog routes before claiming full inscription context / 在声称取得完整卜辞上下文前，先检索已登记著录路线。",
        "- Keep identity, formal assignment, component, evolution-chain, rights, source-promotion, and decipherment decisions blocked / 继续阻断身份、正式分配、构件、演化链、权利、来源提升和释读决定。",
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
        if row["target_evidence_section"] != "full_inscription_context":
            raise ValueError(f"unexpected target evidence section: {row['target_evidence_section']}")
        results.append(
            {
                "note_update_result_id": f"hust-obc-undeciphered-source-image-reference-note-update-{index:04d}",
                "source_image_reference_extraction_summary_id": row[
                    "source_image_reference_extraction_summary_id"
                ],
                "full_inscription_context_precheck_result_id": row[
                    "full_inscription_context_precheck_result_id"
                ],
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
                "source_id": row["source_id"],
                "source_package_id": row["source_package_id"],
                "download_id": row["download_id"],
                "source_class_id": row["source_class_id"],
                "source_class_path": row["source_class_path"],
                "source_image_count_expected": row["source_image_count_expected"],
                "source_image_count_extracted": row["source_image_count_extracted"],
                "source_image_count_match_status": row["source_image_count_match_status"],
                "first_extracted_source_image_path": row["first_extracted_source_image_path"],
                "last_extracted_source_image_path": row["last_extracted_source_image_path"],
                "filename_source_prefixes": row["filename_source_prefixes"],
                "filename_catalog_candidate_number_tokens": row[
                    "filename_catalog_candidate_number_tokens"
                ],
                "filename_catalog_candidate_number_token_count": row[
                    "filename_catalog_candidate_number_token_count"
                ],
                "filename_variant_sequence_token_count": row[
                    "filename_variant_sequence_token_count"
                ],
                "filename_token_interpretation_status": row[
                    "filename_token_interpretation_status"
                ],
                "detail_output_path": row["detail_output_path"],
                "summary_output_path": SOURCE_IMAGE_REFERENCE_SUMMARY.as_posix(),
                "registered_storage_hint": row["registered_storage_hint"],
                "resolved_local_archive_path": row["resolved_local_archive_path"],
                "local_archive_resolution_status": row["local_archive_resolution_status"],
                "primary_catalog_context_status": row["primary_catalog_context_status"],
                "heji_crosswalk_status": row["heji_crosswalk_status"],
                "old_catalog_context_status": row["old_catalog_context_status"],
                "collection_context_status": row["collection_context_status"],
                "excavation_context_status": row["excavation_context_status"],
                "transcription_context_status": row["transcription_context_status"],
                "inscription_context_evidence_status": row["inscription_context_evidence_status"],
                "route_precheck_status": row["route_precheck_status"],
                "catalog_context_status": row["catalog_context_status"],
                "source_rights_status": row["source_rights_status"],
                "large_source_rights_status": row["large_source_rights_status"],
                "risk_note": row["risk_note"],
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
                    "open_070_note_update_result;open_069_summary_row;open_068_detail_rows;"
                    "verify_filename_number_tokens_before_any_catalog_or_inscription_context_claim"
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
    parser.add_argument("--precheck-results", default=str(PRECHECK_RESULTS))
    parser.add_argument("--source-image-reference-summary", default=str(SOURCE_IMAGE_REFERENCE_SUMMARY))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--skip-markdown", action="store_true")
    args = parser.parse_args(argv)

    root = repo_root()
    precheck_rows = read_csv_rows(root / args.precheck_results)
    summary_rows = read_csv_rows(root / args.source_image_reference_summary)
    merged_rows = merge_rows(precheck_rows, summary_rows)
    update_rows = build_note_update_rows(merged_rows)
    if not args.skip_markdown:
        write_markdown_notes(root, merged_rows)
    write_csv(root / args.output, update_rows)
    print(
        f"source_image_reference_note_update_count={len(update_rows)} "
        f"markdown_written={str(not args.skip_markdown).lower()} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
