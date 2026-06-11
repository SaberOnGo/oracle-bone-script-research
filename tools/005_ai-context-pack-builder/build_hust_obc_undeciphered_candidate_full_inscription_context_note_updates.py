#!/usr/bin/env python3
"""Write inscription-context route prechecks into HUST-OBC collection notes."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


PRECHECK_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "066_ai-agent-hust-obc-undeciphered-candidate-full-inscription-context-precheck-results.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "067_ai-agent-hust-obc-undeciphered-candidate-full-inscription-context-note-update-results.csv"
)
UPDATED_AT = "2026-06-11"
NOTE_STATUS = "route_precheck_written_from_066"
EVIDENCE_COLLECTION_STATUS = "full_inscription_context_not_collected"
HUMAN_REVIEW_STATUS = "not_started"
FORMAL_SCHEMA_COMPATIBILITY_STATUS = "not_formal_obs_char_schema"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
NO_CLAIM = "no_claim"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_full_inscription_context_note_update_not_scholarship"
CAUTION_EN = (
    "This note records a route precheck only. The current candidate packet supplies "
    "HUST-OBC dataset source-image paths, but no primary catalog number, inscription "
    "transcription, Heji crosswalk, old catalog number, collection number, or excavation "
    "context has been captured yet. It is not proof of full inscription context and not "
    "a decipherment conclusion."
)
CAUTION_ZH = (
    "本记录只写入路线预检结果。当前候选包只提供 HUST-OBC 数据集来源图片路径；"
    "尚未捕获一手著录号、卜辞释文、《合集》交叉索引、旧著录号、馆藏号或出土上下文。"
    "这不是已取得完整卜辞上下文的证明，也不是释读结论。"
)

OUTPUT_FIELDS = [
    "note_update_result_id",
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
    "source_class_path",
    "source_image_count",
    "source_image_reference_status",
    "candidate_packet_context_status",
    "primary_catalog_context_status",
    "inscription_context_evidence_status",
    "route_precheck_status",
    "next_registered_source_routes",
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
    route_files = _bullet_paths(row["route_files_to_open"])
    next_sources = _bullet_paths(row["next_registered_source_routes"])
    lines = [
        "# HUST-OBC Undeciphered Candidate Full Inscription Context Precheck / HUST-OBC 未释读候选完整卜辞上下文预检",
        "",
        "## Status / 状态",
        "",
        f"- Full inscription context precheck result ID / 完整卜辞上下文预检结果 ID: `{row['full_inscription_context_precheck_result_id']}`",
        f"- Source metadata evidence capture result ID / 来源 metadata 证据捕获结果 ID: `{row['source_metadata_evidence_capture_result_id']}`",
        f"- Evidence collection note draft ID / 证据收集记录草稿 ID: `{row['evidence_collection_note_draft_id']}`",
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
        "## Candidate Route / 候选路由",
        "",
        f"- Unknown candidate ID / 未知候选 ID: `{row['unknown_candidate_id']}`",
        f"- Primary external ref ID / 首选外部引用 ID: `{row['primary_external_ref_id']}`",
        f"- Source ID / 来源 ID: `{row['source_id']}`",
        f"- Source package ID / 来源包 ID: `{row['source_package_id']}`",
        f"- Download ID / 下载 ID: `{row['download_id']}`",
        f"- Candidate packet path / 候选包路径: `{row['candidate_packet_path']}`",
        f"- Bucket manifest path / 分桶 manifest 路径: `{row['bucket_manifest_path']}`",
        f"- Undeciphered index path / 未释读索引路径: `{row['undeciphered_index_path']}`",
        "",
        "## Current Packet Evidence / 当前候选包证据",
        "",
        f"- Source class path / 来源类别路径: `{row['source_class_path']}`",
        f"- Source image count / 来源图片数量: `{row['source_image_count']}`",
        f"- First source image path / 首个来源图片路径: `{row['first_source_image_path']}`",
        f"- Last source image path / 末个来源图片路径: `{row['last_source_image_path']}`",
        f"- Source image reference status / 来源图片引用状态: `{row['source_image_reference_status']}`",
        f"- Candidate packet context status / 候选包上下文状态: `{row['candidate_packet_context_status']}`",
        "",
        "## Inscription Context Precheck / 卜辞上下文预检",
        "",
        f"- Primary catalog context status / 一手著录上下文状态: `{row['primary_catalog_context_status']}`",
        f"- Heji crosswalk status / 《合集》交叉索引状态: `{row['heji_crosswalk_status']}`",
        f"- Old catalog context status / 旧著录上下文状态: `{row['old_catalog_context_status']}`",
        f"- Collection context status / 馆藏上下文状态: `{row['collection_context_status']}`",
        f"- Excavation context status / 出土上下文状态: `{row['excavation_context_status']}`",
        f"- Transcription context status / 卜辞释文上下文状态: `{row['transcription_context_status']}`",
        f"- Inscription context evidence status / 卜辞上下文证据状态: `{row['inscription_context_evidence_status']}`",
        f"- Route precheck status / 路线预检状态: `{row['route_precheck_status']}`",
        "",
        "## Registered Source Routes To Search Next / 下一步应检索的已登记来源路线",
        "",
        *next_sources,
        "",
        f"Search scope / 检索范围: {row['next_source_search_scope']}",
        "",
        "## Route Files To Open / 待打开路由文件",
        "",
        *route_files,
        "",
        "## Required Next Checks / 后续必查项",
        "",
        "- Open 066 precheck result row / 打开 066 预检结果行。",
        "- Open candidate-packet source image references / 打开候选包来源图片路径引用。",
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
                "note_update_result_id": f"hust-obc-undeciphered-full-inscription-context-note-update-{index:04d}",
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
                "source_class_path": row["source_class_path"],
                "source_image_count": row["source_image_count"],
                "source_image_reference_status": row["source_image_reference_status"],
                "candidate_packet_context_status": row["candidate_packet_context_status"],
                "primary_catalog_context_status": row["primary_catalog_context_status"],
                "inscription_context_evidence_status": row["inscription_context_evidence_status"],
                "route_precheck_status": row["route_precheck_status"],
                "next_registered_source_routes": row["next_registered_source_routes"],
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
                    "open_066_precheck_result;open_updated_full_inscription_context_note;"
                    "search_registered_catalog_routes_before_any_identity_or_decipherment_claim"
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
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--skip-markdown", action="store_true")
    args = parser.parse_args(argv)

    root = repo_root()
    precheck_rows = read_csv_rows(root / args.precheck_results)
    update_rows = build_note_update_rows(precheck_rows)
    if not args.skip_markdown:
        write_markdown_notes(root, precheck_rows)
    write_csv(root / args.output, update_rows)
    print(
        f"full_inscription_context_note_update_count={len(update_rows)} "
        f"markdown_written={str(not args.skip_markdown).lower()} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
