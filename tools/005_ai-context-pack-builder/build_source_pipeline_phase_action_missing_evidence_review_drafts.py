#!/usr/bin/env python3
"""Build empty source-level review drafts for missing source evidence.

The drafts materialize the 147 source-level missing-evidence summary as
human-readable work surfaces. They do not collect evidence, decide rights,
promote sources, import corpus rows, or make decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_SOURCE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/"
    "147_source-pipeline-phase-action-missing-evidence-source-summary.csv"
)
ALL_SOURCES_INDEX = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "001_all-sources-index.csv"
)
DOWNLOADED_METADATA_PROFILE = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "010_downloaded-metadata-profile.csv"
)
LARGE_SOURCE_REGISTER = Path(
    "project_registry/006_large-source-register/001_large-source-register.csv"
)
SOURCE_DOWNLOAD_LOG = Path(
    "project_registry/006_large-source-register/002_source-download-log.csv"
)
SOURCE_FIELD_MAP = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "007_source-field-map.csv"
)
SOURCE_PACKAGE_FILE_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "009_source-package-file-manifest.csv"
)
DEFAULT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/"
    "148_source-pipeline-phase-action-missing-evidence-review-draft-manifest.csv"
)
DRAFT_DIR = Path("doc/public/user_research/010_source-pipeline-missing-evidence-review-queues")
UPDATED_AT = "2026-06-19"
DRAFT_STATUS = "draft_not_collected"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_missing_evidence_review_draft_not_scholarship"
CAUTION = (
    "This source pipeline missing-evidence review draft is a human-review work "
    "surface only. It is not collected evidence, not a reviewed outcome, not a "
    "rights decision, not source promotion, not a corpus import, and not a "
    "decipherment conclusion."
)

OUTPUT_FIELDS = [
    "review_draft_id",
    "source_summary_id",
    "source_id",
    "source_type",
    "rights_status",
    "pipeline_gap_status",
    "missing_route_count",
    "missing_file_role_count",
    "missing_file_roles",
    "draft_path",
    "source_summary_path",
    "route_summary_path",
    "route_ids",
    "missing_evidence_action_ids",
    "missing_evidence_result_scaffold_ids",
    "evidence_presence_row_ids",
    "files_to_open",
    "required_review_actions",
    "draft_status",
    "evidence_collection_status",
    "human_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "reviewed_evidence_paths",
    "reviewed_outcome_summary",
    "required_followup_reviewed",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_semicolon(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def ids_from_rows(rows: list[dict[str, str]], field: str) -> str:
    values: list[str] = []
    for row in rows:
        value = row.get(field, "")
        if value and value not in values:
            values.append(value)
    return ";".join(values) if values else "none"


def status_counts(rows: list[dict[str, str]], field: str) -> str:
    counts: dict[str, int] = {}
    for row in rows:
        value = row.get(field, "") or "blank"
        counts[value] = counts.get(value, 0) + 1
    if not counts:
        return "none"
    return ";".join(f"{key}:{counts[key]}" for key in sorted(counts))


def rows_for_source(root: Path, path: Path, source_id: str) -> list[dict[str, str]]:
    full_path = root / path
    if not full_path.exists():
        return []
    return [row for row in read_csv_rows(full_path) if row.get("source_id") == source_id]


def collect_source_metadata_snapshot(root: Path, source_id: str) -> dict[str, str]:
    all_sources = rows_for_source(root, ALL_SOURCES_INDEX, source_id)
    metadata_profiles = rows_for_source(root, DOWNLOADED_METADATA_PROFILE, source_id)
    large_sources = rows_for_source(root, LARGE_SOURCE_REGISTER, source_id)
    download_logs = rows_for_source(root, SOURCE_DOWNLOAD_LOG, source_id)
    field_maps = rows_for_source(root, SOURCE_FIELD_MAP, source_id)
    package_files = rows_for_source(root, SOURCE_PACKAGE_FILE_MANIFEST, source_id)
    return {
        "all_sources_index_row_count": str(len(all_sources)),
        "downloaded_metadata_profile_row_count": str(len(metadata_profiles)),
        "large_source_register_row_count": str(len(large_sources)),
        "source_download_log_row_count": str(len(download_logs)),
        "source_field_map_row_count": str(len(field_maps)),
        "source_package_file_manifest_row_count": str(len(package_files)),
        "all_sources_review_status_counts": status_counts(all_sources, "review_status"),
        "metadata_profile_ids": ids_from_rows(metadata_profiles, "profile_id"),
        "large_source_package_ids": ids_from_rows(large_sources, "source_package_id"),
        "source_download_log_ids": ids_from_rows(download_logs, "download_id"),
        "source_field_map_ids": ids_from_rows(field_maps, "map_id"),
        "source_package_file_ids": ids_from_rows(package_files, "package_file_id"),
    }


def draft_path(index: int, source_id: str) -> str:
    return (DRAFT_DIR / f"{index:03d}_{source_id}.md").as_posix()


def build_manifest_rows(source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(source_rows, start=1):
        rows.append(
            {
                "review_draft_id": f"source-pipeline-missing-evidence-review-draft-{index:03d}",
                "source_summary_id": row["missing_evidence_source_summary_id"],
                "source_id": row["source_id"],
                "source_type": row["source_type"],
                "rights_status": row["rights_status"],
                "pipeline_gap_status": row["pipeline_gap_status"],
                "missing_route_count": row["missing_route_count"],
                "missing_file_role_count": row["missing_file_role_count"],
                "missing_file_roles": row["missing_file_roles"],
                "draft_path": draft_path(index, row["source_id"]),
                "source_summary_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_SOURCE_SUMMARY.as_posix(),
                "route_summary_path": row["route_summary_path"],
                "route_ids": row["route_ids"],
                "missing_evidence_action_ids": row["missing_evidence_action_ids"],
                "missing_evidence_result_scaffold_ids": row["missing_evidence_result_scaffold_ids"],
                "evidence_presence_row_ids": row["evidence_presence_row_ids"],
                "files_to_open": row["files_to_open"],
                "required_review_actions": row["remaining_blockers_reviewed"],
                "draft_status": DRAFT_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "human_review_status": HUMAN_REVIEW_STATUS,
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "corpus_import_status": CORPUS_IMPORT_STATUS,
                "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
                "reviewed_evidence_paths": "",
                "reviewed_outcome_summary": "",
                "required_followup_reviewed": "",
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def bullet_list(values: list[str]) -> list[str]:
    return [f"- `{value}`" for value in values] if values else ["- none"]


def build_markdown(row: dict[str, str]) -> str:
    lines = [
        "# Source Pipeline Missing-Evidence Review Draft / 来源流水线缺失证据复核草稿",
        "",
        "## Status / 状态",
        "",
        f"- Review draft ID / 复核草稿 ID: `{row['review_draft_id']}`",
        f"- Source summary ID / 来源汇总 ID: `{row['source_summary_id']}`",
        f"- Draft status / 草稿状态: `{row['draft_status']}`",
        f"- Evidence collection status / 证据收集状态: `{row['evidence_collection_status']}`",
        f"- Human review status / 人工复核状态: `{row['human_review_status']}`",
        f"- Research boundary / 研究边界: `{row['research_boundary']}`",
        f"- Updated at / 更新时间: `{row['updated_at']}`",
        "",
        "## Source / 来源",
        "",
        f"- Source ID / 来源 ID: `{row['source_id']}`",
        f"- Source type / 来源类型: `{row['source_type']}`",
        f"- Rights status / 权利状态: `{row['rights_status']}`",
        f"- Pipeline gap status / 流水线缺口状态: `{row['pipeline_gap_status']}`",
        "",
        "## Missing Evidence / 缺失证据",
        "",
        f"- Missing route count / 缺失路由数: `{row['missing_route_count']}`",
        f"- Missing file role count / 缺失文件角色数: `{row['missing_file_role_count']}`",
        "",
        "### Missing file roles / 缺失文件角色",
        "",
    ]
    lines.extend(bullet_list(split_semicolon(row["missing_file_roles"])))
    lines.extend(
        [
            "",
            "### Files to open / 待打开文件",
            "",
        ]
    )
    lines.extend(bullet_list(split_semicolon(row["files_to_open"])))
    lines.extend(
        [
            "",
            "### Required review actions / 必需复核动作",
            "",
        ]
    )
    lines.extend(bullet_list(split_semicolon(row["required_review_actions"])))
    lines.extend(
        [
            "",
            "## Route References / 路由引用",
            "",
            f"- Source summary path / 来源汇总路径: `{row['source_summary_path']}`",
            f"- Route summary path / 路由汇总路径: `{row['route_summary_path']}`",
            "",
            "### Route IDs / 路由 ID",
            "",
        ]
    )
    lines.extend(bullet_list(split_semicolon(row["route_ids"])))
    lines.extend(
        [
            "",
            "### Action IDs / 动作 ID",
            "",
        ]
    )
    lines.extend(bullet_list(split_semicolon(row["missing_evidence_action_ids"])))
    lines.extend(
        [
            "",
            "### Result scaffold IDs / 结果脚手架 ID",
            "",
        ]
    )
    lines.extend(bullet_list(split_semicolon(row["missing_evidence_result_scaffold_ids"])))
    lines.extend(
        [
            "",
            "## Review Outcome Placeholder / 复核结果占位",
            "",
            "English: No reviewed evidence has been collected in this draft. Fill this section only after opening the routed files and preserving source, rights, manifest, large-source, metadata-profile, and field-map boundaries.",
            "",
            "简体中文：本草稿尚未收集已复核证据。只有在打开路由文件，并保留来源、权利、manifest、大型来源、metadata profile 和 field-map 边界后，才可填写本节。",
            "",
            "- Reviewed evidence paths / 已复核证据路径: none",
            "- Reviewed outcome summary / 已复核结果摘要: not decided",
            "- Required follow-up / 必需后续动作: not decided",
            "",
            "## Boundary Status / 边界状态",
            "",
            f"- Rights decision status / 权利裁定状态: `{row['rights_decision_status']}`",
            f"- Source promotion status / 来源提升状态: `{row['source_promotion_status']}`",
            f"- Corpus import status / 语料导入状态: `{row['corpus_import_status']}`",
            f"- Decipherment claim status / 释读结论状态: `{row['decipherment_claim_status']}`",
            "",
            "## Caution / 警示",
            "",
            f"English: {CAUTION}",
            "",
            "简体中文：本来源流水线缺失证据复核草稿只作为人工复核工作界面；它不是已收集证据，不是已复核结果，不是权利裁定，不是来源提升，不是语料导入，也不是释读结论。",
            "",
        ]
    )
    return "\n".join(lines)


def metadata_snapshot_markdown(snapshot: dict[str, str]) -> str:
    lines = [
        "## Existing Source Metadata Snapshot / 已有来源 metadata 快照",
        "",
        "English: Current source-register and provenance rows are",
        "summarized here before any human outcome review.",
        "",
        "简体中文：这里先汇总当前来源登记和追溯行，",
        "不替代后续人工结论复核。",
        "",
        f"- all_sources_index_row_count: `{snapshot['all_sources_index_row_count']}`",
        f"- downloaded_metadata_profile_row_count: `{snapshot['downloaded_metadata_profile_row_count']}`",
        f"- large_source_register_row_count: `{snapshot['large_source_register_row_count']}`",
        f"- source_download_log_row_count: `{snapshot['source_download_log_row_count']}`",
        f"- source_field_map_row_count: `{snapshot['source_field_map_row_count']}`",
        f"- source_package_file_manifest_row_count: `{snapshot['source_package_file_manifest_row_count']}`",
        f"- all_sources_review_status_counts: `{snapshot['all_sources_review_status_counts']}`",
        f"- metadata_profile_ids: `{snapshot['metadata_profile_ids']}`",
        f"- large_source_package_ids: `{snapshot['large_source_package_ids']}`",
        f"- source_download_log_ids: `{snapshot['source_download_log_ids']}`",
        f"- source_field_map_ids: `{snapshot['source_field_map_ids']}`",
        f"- source_package_file_ids: `{snapshot['source_package_file_ids']}`",
        "",
        "## Review Outcome Boundary / 复核结果边界",
        "",
        "English: These rows are source and route evidence only.",
        "They do not decide rights, promote a source, import corpus rows,",
        "or make any decipherment claim.",
        "",
        "简体中文：这些行只作为来源和路线证据。",
        "它们不作权利裁定，不提升来源，不导入语料，",
        "也不提出任何释读结论。",
        "",
        "- Reviewed evidence paths / 已复核证据路径: pending human review",
        "- Reviewed outcome summary / 已复核结果摘要: pending human review",
        "- Required follow-up / 必需后续动作: open the routed rows above",
        "",
    ]
    return "\n".join(lines)


def build_markdown_with_snapshot(row: dict[str, str], snapshot: dict[str, str]) -> str:
    text = build_markdown(row)
    start_marker = "## Review Outcome Placeholder"
    end_marker = "## Boundary Status"
    start = text.index(start_marker)
    end = text.index(end_marker)
    return text[:start] + metadata_snapshot_markdown(snapshot) + text[end:]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown_drafts(root: Path, rows: list[dict[str, str]]) -> None:
    for row in rows:
        path = root / row["draft_path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        snapshot = collect_source_metadata_snapshot(root, row["source_id"])
        path.write_text(build_markdown_with_snapshot(row, snapshot), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build missing-evidence source review drafts.")
    parser.add_argument("--source-summary", default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_SOURCE_SUMMARY))
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    args = parser.parse_args(argv)

    root = repo_root()
    source_rows = read_csv_rows(root / args.source_summary)
    manifest_rows = build_manifest_rows(source_rows)
    write_markdown_drafts(root, manifest_rows)
    write_csv(root / args.manifest, manifest_rows)
    print(f"missing_evidence_review_draft_rows={len(manifest_rows)} manifest={args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
