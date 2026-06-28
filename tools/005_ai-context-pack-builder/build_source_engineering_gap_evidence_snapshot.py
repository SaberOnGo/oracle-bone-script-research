#!/usr/bin/env python3
"""Build metadata-only evidence snapshots for source-engineering gaps.

The snapshot copies existing repository evidence for each 099 gap task into a
single review row: source-register facts, download manifest/log status,
field-map/package-manifest/metadata-profile presence, and route-file
availability. It does not download, re-check checksums, clear rights, import
corpus records, or promote source/scholarly claims.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


SOURCE_ENGINEERING_GAP_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/099_ai-agent-source-engineering-gap-queue.csv"
)
SOURCE_ENGINEERING_GAP_REVIEW_LOG_DRAFT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/102_ai-agent-source-engineering-gap-review-log-draft-manifest.csv"
)
SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_DOWNLOAD_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/003_source-download-manifest.csv"
)
SOURCE_FIELD_MAP = Path("corpus/006_research-sources-and-bibliography/000_source-registers/007_source-field-map.csv")
SOURCE_PACKAGE_FILE_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv"
)
DOWNLOADED_METADATA_PROFILE = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/010_downloaded-metadata-profile.csv"
)
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
SOURCE_PROCESSING_PIPELINE_AUDIT = Path(
    "corpus/009_statistics-and-derived-features/094_source-processing-pipeline-audit.csv"
)
SOURCE_COVERAGE_SUMMARY = Path("corpus/009_statistics-and-derived-features/007_source-coverage-summary.csv")
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/103_ai-agent-source-engineering-gap-evidence-snapshot.csv"
)

UPDATED_AT = "2026-06-19"
EVIDENCE_STATUS = "metadata_only_existing_records_snapshot"
SOURCE_PROMOTION_STATUS = "not_promoted"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
CORPUS_IMPORT_STATUS = "not_imported"
RESEARCH_BOUNDARY = "source_engineering_gap_evidence_snapshot_not_scholarship"
CAUTION = (
    "This row snapshots existing source-engineering metadata only. It is not a "
    "new download, not checksum recalculation, not rights clearance, not source "
    "promotion, not corpus import, not an oracle-character identity claim, and "
    "not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "evidence_snapshot_id",
    "source_engineering_gap_id",
    "review_log_draft_id",
    "source_id",
    "gap_type",
    "priority_rank",
    "current_stage",
    "source_title",
    "provider",
    "source_url",
    "authority_tier",
    "rights_status",
    "risk_note",
    "source_review_status",
    "download_manifest_ids",
    "download_manifest_artifact_kinds",
    "download_manifest_commit_policies",
    "download_log_ids",
    "download_log_status_counts",
    "download_log_http_status_counts",
    "download_log_file_size_bytes_total",
    "download_log_checksum_present_count",
    "download_log_risk_notes",
    "field_map_ids",
    "field_map_target_record_types",
    "field_map_review_status_counts",
    "package_file_ids",
    "package_file_kinds",
    "package_file_commit_policies",
    "metadata_profile_ids",
    "metadata_profile_metrics",
    "metadata_profile_review_status_counts",
    "pipeline_observed_counts",
    "coverage_observed_counts",
    "route_files_to_open",
    "route_file_missing_count",
    "draft_path",
    "required_next_checks",
    "evidence_status",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def compact_counter(counter: Counter[str]) -> str:
    return ";".join(f"{key}:{counter[key]}" for key in sorted(counter) if key)


def join_unique(values: list[str]) -> str:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value and value not in seen:
            output.append(value)
            seen.add(value)
    return ";".join(output)


def rows_by(rows: list[dict[str, str]], key: str) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row.get(key, ""), []).append(row)
    return grouped


def row_by(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row.get(key, ""): row for row in rows}


def int_value(value: str) -> int:
    return int(value) if value.isdigit() else 0


def count_missing_route_files(root: Path, route_files: str) -> int:
    missing = 0
    for route_file in [value for value in route_files.split(";") if value]:
        if not (root / route_file).exists():
            missing += 1
    return missing


def download_size_total(rows: list[dict[str, str]]) -> int:
    return sum(int_value(row.get("file_size_bytes", "")) for row in rows)


def pipeline_counts(row: dict[str, str]) -> str:
    fields = [
        "download_manifest_count",
        "download_log_count",
        "downloaded_count",
        "access_boundary_or_error_count",
        "checksum_present_count",
        "size_recorded_count",
        "field_map_count",
        "large_source_register_count",
        "package_manifest_count",
        "metadata_profile_count",
        "asset_count",
        "candidate_queue_count",
        "graph_edge_count",
    ]
    return ";".join(f"{field}={row.get(field, '0')}" for field in fields)


def coverage_counts(row: dict[str, str]) -> str:
    fields = [
        "download_manifest_count",
        "download_log_count",
        "downloaded_file_bytes",
        "metadata_profile_metric_count",
        "committed_asset_count",
        "committed_asset_bytes",
        "graph_edge_count",
        "graph_edge_type_count",
        "promotion_queue_candidate_count",
        "coverage_status",
    ]
    return ";".join(f"{field}={row.get(field, '')}" for field in fields)


def build_snapshot_rows(root: Path) -> list[dict[str, str]]:
    gap_rows = read_csv_rows(root / SOURCE_ENGINEERING_GAP_QUEUE)
    draft_rows = read_csv_rows(root / SOURCE_ENGINEERING_GAP_REVIEW_LOG_DRAFT_MANIFEST)
    source_by_id = row_by(read_csv_rows(root / SOURCE_INDEX), "source_id")
    manifests_by_source = rows_by(read_csv_rows(root / SOURCE_DOWNLOAD_MANIFEST), "source_id")
    logs_by_source = rows_by(read_csv_rows(root / SOURCE_DOWNLOAD_LOG), "source_id")
    field_maps_by_source = rows_by(read_csv_rows(root / SOURCE_FIELD_MAP), "source_id")
    package_files_by_source = rows_by(read_csv_rows(root / SOURCE_PACKAGE_FILE_MANIFEST), "source_id")
    profiles_by_source = rows_by(read_csv_rows(root / DOWNLOADED_METADATA_PROFILE), "source_id")
    pipeline_by_source = row_by(read_csv_rows(root / SOURCE_PROCESSING_PIPELINE_AUDIT), "source_id")
    coverage_by_source = row_by(read_csv_rows(root / SOURCE_COVERAGE_SUMMARY), "source_id")
    draft_by_gap_id = row_by(draft_rows, "source_engineering_gap_id")

    output_rows: list[dict[str, str]] = []
    for index, gap in enumerate(gap_rows, start=1):
        source_id = gap["source_id"]
        source = source_by_id.get(source_id, {})
        manifests = manifests_by_source.get(source_id, [])
        logs = logs_by_source.get(source_id, [])
        field_maps = field_maps_by_source.get(source_id, [])
        package_files = package_files_by_source.get(source_id, [])
        profiles = profiles_by_source.get(source_id, [])
        pipeline = pipeline_by_source.get(source_id, {})
        coverage = coverage_by_source.get(source_id, {})
        draft = draft_by_gap_id.get(gap["source_engineering_gap_id"], {})
        route_files = gap["route_files_to_open"]
        output_rows.append(
            {
                "evidence_snapshot_id": f"source-engineering-gap-evidence-snapshot-{index:04d}",
                "source_engineering_gap_id": gap["source_engineering_gap_id"],
                "review_log_draft_id": draft.get("review_log_draft_id", ""),
                "source_id": source_id,
                "gap_type": gap["gap_type"],
                "priority_rank": gap["priority_rank"],
                "current_stage": gap["current_stage"],
                "source_title": source.get("title", ""),
                "provider": source.get("provider", ""),
                "source_url": source.get("source_url", ""),
                "authority_tier": source.get("authority_tier", gap.get("authority_tier", "")),
                "rights_status": source.get("rights_status", gap.get("rights_status", "")),
                "risk_note": source.get("risk_note", ""),
                "source_review_status": source.get("review_status", ""),
                "download_manifest_ids": join_unique([row.get("download_id", "") for row in manifests]),
                "download_manifest_artifact_kinds": join_unique([row.get("artifact_kind", "") for row in manifests]),
                "download_manifest_commit_policies": join_unique([row.get("commit_policy", "") for row in manifests]),
                "download_log_ids": join_unique([row.get("download_id", "") for row in logs]),
                "download_log_status_counts": compact_counter(Counter(row.get("status", "") for row in logs)),
                "download_log_http_status_counts": compact_counter(Counter(row.get("http_status", "") for row in logs)),
                "download_log_file_size_bytes_total": str(download_size_total(logs)),
                "download_log_checksum_present_count": str(sum(1 for row in logs if row.get("checksum_sha256", ""))),
                "download_log_risk_notes": join_unique([row.get("risk_note", "") for row in logs]),
                "field_map_ids": join_unique([row.get("map_id", "") for row in field_maps]),
                "field_map_target_record_types": join_unique(
                    [row.get("target_record_type", "") for row in field_maps]
                ),
                "field_map_review_status_counts": compact_counter(
                    Counter(row.get("review_status", "") for row in field_maps)
                ),
                "package_file_ids": join_unique([row.get("package_file_id", "") for row in package_files]),
                "package_file_kinds": join_unique([row.get("file_kind", "") for row in package_files]),
                "package_file_commit_policies": join_unique(
                    [row.get("commit_policy", "") for row in package_files]
                ),
                "metadata_profile_ids": join_unique([row.get("profile_id", "") for row in profiles]),
                "metadata_profile_metrics": join_unique([row.get("profile_metric", "") for row in profiles]),
                "metadata_profile_review_status_counts": compact_counter(
                    Counter(row.get("review_status", "") for row in profiles)
                ),
                "pipeline_observed_counts": pipeline_counts(pipeline),
                "coverage_observed_counts": coverage_counts(coverage),
                "route_files_to_open": route_files,
                "route_file_missing_count": str(count_missing_route_files(root, route_files)),
                "draft_path": draft.get("draft_path", gap.get("expected_output_path", "")),
                "required_next_checks": gap["required_next_checks"],
                "evidence_status": EVIDENCE_STATUS,
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "corpus_import_status": CORPUS_IMPORT_STATUS,
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return output_rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def none_if_blank(value: str) -> str:
    return value if value else "none"


def review_log_evidence_block(row: dict[str, str]) -> str:
    lines = [
        "## Evidence Collection / 证据收集",
        "",
        "English: Existing metadata has been captured from routed records.",
        "It remains metadata-only and does not promote source content.",
        "",
        "简体中文：已从路线记录捕获现有 metadata。",
        "这些内容仍为 metadata-only，不提升为来源正文。",
        "",
        "## Existing Metadata Snapshot / 已有 metadata 快照",
        "",
        f"- Evidence snapshot ID / 证据快照 ID: `{row['evidence_snapshot_id']}`",
        f"- Evidence status / 证据状态: `{row['evidence_status']}`",
        f"- Source review status / 来源复核状态: `{row['source_review_status']}`",
        f"- Rights status / 权利状态: `{row['rights_status']}`",
        f"- Download manifest IDs / 下载 manifest ID: `{none_if_blank(row['download_manifest_ids'])}`",
        f"- Download log IDs / 下载日志 ID: `{none_if_blank(row['download_log_ids'])}`",
        f"- download_log_status_counts: `{none_if_blank(row['download_log_status_counts'])}`",
        f"- download_log_http_status_counts: `{none_if_blank(row['download_log_http_status_counts'])}`",
        f"- download_log_file_size_bytes_total: `{row['download_log_file_size_bytes_total']}`",
        f"- download_log_checksum_present_count: `{row['download_log_checksum_present_count']}`",
        f"- package_file_ids: `{none_if_blank(row['package_file_ids'])}`",
        f"- metadata_profile_ids: `{none_if_blank(row['metadata_profile_ids'])}`",
        f"- Route file missing count / 缺失路线文件数: `{row['route_file_missing_count']}`",
        "",
        "## Snapshot Boundary / 快照边界",
        "",
        f"- Rights decision status / 权利决策状态: `{row['rights_decision_status']}`",
        f"- Source promotion status / 来源提升状态: `{row['source_promotion_status']}`",
        f"- Corpus import status / 语料导入状态: `{row['corpus_import_status']}`",
        "- Identity, component, evolution, and decipherment claims: `blocked`",
        "- 身份、构件、演化链和释读结论：`blocked`",
        "",
    ]
    return "\n".join(lines)


def write_review_log_snapshot_notes(root: Path, rows: list[dict[str, str]]) -> int:
    written = 0
    start_marker = "## Evidence Collection / 证据收集"
    end_marker = "## Review Log / 复核日志"
    for row in rows:
        draft_path = row.get("draft_path", "")
        if not draft_path:
            continue
        path = root / draft_path
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        start = text.find(start_marker)
        end = text.find(end_marker)
        if start == -1 or end == -1 or end <= start:
            continue
        updated = text[:start] + review_log_evidence_block(row) + "\n" + text[end:]
        path.write_text(updated, encoding="utf-8", newline="\n")
        written += 1
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source-engineering gap evidence snapshot.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--skip-markdown", action="store_true")
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_snapshot_rows(root)
    write_csv(root / args.output, rows)
    markdown_written = 0 if args.skip_markdown else write_review_log_snapshot_notes(root, rows)
    print(
        f"wrote={len(rows)} markdown_written={markdown_written} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
