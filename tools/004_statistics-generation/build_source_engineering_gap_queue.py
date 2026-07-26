#!/usr/bin/env python3
"""Build a source-engineering gap queue from current preprocessing audits."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_PROCESSING_PIPELINE_AUDIT = Path(
    "corpus/009_statistics-and-derived-features/094_source-processing-pipeline-audit.csv"
)
SOURCE_COVERAGE_SUMMARY = Path("corpus/009_statistics-and-derived-features/007_source-coverage-summary.csv")
SOURCE_ROUTE_REVIEW_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/009_ai-agent-source-route-review-queue.csv"
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
SOURCE_DOWNLOAD_STATUS_CODEBOOK = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/013_source-download-status-codebook.csv"
)
BROWSER_VERIFIED_METADATA_CAPTURE = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "014_browser-verified-metadata-capture.csv"
)
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
LARGE_SOURCE_REGISTER = Path("project_registry/006_large-source-register/001_large-source-register.csv")
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/099_ai-agent-source-engineering-gap-queue.csv"
)

UPDATED_AT = "2026-07-27"
SIZE_LIMIT_BYTES = 30 * 1024 * 1024
RESEARCH_BOUNDARY = "source_engineering_gap_queue_metadata_only_not_scholarship"
CAUTION = (
    "This row is a source-engineering gap task only. It routes agents to current "
    "provenance, download, manifest, field-map, and derived-record evidence; it is "
    "not a source promotion decision, not rights clearance, not a corpus import, "
    "not an identity claim, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "source_engineering_gap_id",
    "source_id",
    "priority_rank",
    "gap_type",
    "current_stage",
    "authority_tier",
    "rights_status",
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
    "downloaded_file_bytes",
    "download_status_counts",
    "observed_gap_evidence",
    "required_next_checks",
    "route_files_to_open",
    "expected_output_path",
    "commit_policy_boundary",
    "source_promotion_status",
    "research_boundary",
    "review_status",
    "caution",
    "updated_at",
]

GAP_PRIORITY = {
    "access_boundary_or_error_followup": 1,
    "checksum_or_failed_download_status_review_needed": 2,
    "large_source_register_review_needed": 3,
    "metadata_profile_extraction_needed": 4,
    "source_field_map_needed": 5,
    "package_file_manifest_or_not_applicable_decision_needed": 6,
    "safe_derived_record_decision_needed": 7,
}

GAP_CHECKS = {
    "access_boundary_or_error_followup": [
        "open_download_log_and_status_codebook",
        "record_retry_manual_access_or_metadata_only_boundary",
        "do_not_promote_failed_or_restricted_download_as_source_content",
    ],
    "checksum_or_failed_download_status_review_needed": [
        "open_download_log",
        "separate_failed_or_restricted_rows_from checksum-bearing downloads",
        "record_no_source_package_or_metadata_promotion_without verified checksum",
    ],
    "large_source_register_review_needed": [
        "open_source_coverage_bytes_and_large_source_register",
        "record_external_or_ignored_storage_for_over_size_limit_source",
        "commit_only_manifest_checksum_and_reviewed_derivatives",
    ],
    "metadata_profile_extraction_needed": [
        "open_download_log_and_source_register",
        "extract_metadata_only_counts_or_scope_from_committed_evidence",
        "record_review_status_and_no_scholarly_claim",
    ],
    "source_field_map_needed": [
        "open_source_register_and_available_metadata_profile",
        "define_source_fields_or_units_to_project_record_targets",
        "record_rights_boundary_for_each mapped field",
    ],
    "package_file_manifest_or_not_applicable_decision_needed": [
        "open_download_manifest_download_log_and_package_manifest",
        "record_package_file_manifest_rows_or_explicit_not_applicable_decision",
        "keep_raw_or_temporary_files_outside_regular_git",
    ],
    "safe_derived_record_decision_needed": [
        "open_metadata_profile_source_route_and_rights_status",
        "decide_next_safe_derivative_staging_or_review_queue",
        "record_no_corpus_promotion_without_source_marked_review",
    ],
}

ROUTE_FILES_BY_GAP = {
    "access_boundary_or_error_followup": [
        SOURCE_PROCESSING_PIPELINE_AUDIT,
        SOURCE_COVERAGE_SUMMARY,
        SOURCE_INDEX,
        SOURCE_DOWNLOAD_MANIFEST,
        SOURCE_DOWNLOAD_LOG,
        SOURCE_DOWNLOAD_STATUS_CODEBOOK,
        BROWSER_VERIFIED_METADATA_CAPTURE,
        SOURCE_ROUTE_REVIEW_QUEUE,
    ],
    "checksum_or_failed_download_status_review_needed": [
        SOURCE_PROCESSING_PIPELINE_AUDIT,
        SOURCE_DOWNLOAD_LOG,
        SOURCE_DOWNLOAD_STATUS_CODEBOOK,
        BROWSER_VERIFIED_METADATA_CAPTURE,
        SOURCE_ROUTE_REVIEW_QUEUE,
    ],
    "large_source_register_review_needed": [
        SOURCE_PROCESSING_PIPELINE_AUDIT,
        SOURCE_COVERAGE_SUMMARY,
        LARGE_SOURCE_REGISTER,
        SOURCE_DOWNLOAD_LOG,
    ],
    "metadata_profile_extraction_needed": [
        SOURCE_PROCESSING_PIPELINE_AUDIT,
        SOURCE_INDEX,
        SOURCE_DOWNLOAD_LOG,
        DOWNLOADED_METADATA_PROFILE,
        SOURCE_ROUTE_REVIEW_QUEUE,
    ],
    "source_field_map_needed": [
        SOURCE_PROCESSING_PIPELINE_AUDIT,
        SOURCE_INDEX,
        SOURCE_FIELD_MAP,
        DOWNLOADED_METADATA_PROFILE,
        SOURCE_ROUTE_REVIEW_QUEUE,
    ],
    "package_file_manifest_or_not_applicable_decision_needed": [
        SOURCE_PROCESSING_PIPELINE_AUDIT,
        SOURCE_DOWNLOAD_MANIFEST,
        SOURCE_DOWNLOAD_LOG,
        SOURCE_PACKAGE_FILE_MANIFEST,
        SOURCE_ROUTE_REVIEW_QUEUE,
    ],
    "safe_derived_record_decision_needed": [
        SOURCE_PROCESSING_PIPELINE_AUDIT,
        SOURCE_COVERAGE_SUMMARY,
        DOWNLOADED_METADATA_PROFILE,
        SOURCE_ROUTE_REVIEW_QUEUE,
    ],
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def int_value(row: dict[str, str], key: str) -> int:
    value = row.get(key, "")
    return int(value) if value else 0


def download_access_boundary_count(status_counts: str) -> int:
    count = 0
    for item in status_counts.split(";"):
        if not item or ":" not in item:
            continue
        status, raw_count = item.rsplit(":", 1)
        if (
            "access_restricted" in status
            or status == "download_error"
            or status == "http_error"
        ):
            count += int(raw_count)
    return count


def reviewed_browser_capture_counts(
    rows: list[dict[str, str]],
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        if (
            row.get("review_status") == "reviewed_metadata_only"
            and row.get("payload_status") == "no_page_payload_saved"
            and row.get("source_checksum_status") == "no_source_payload_checksum"
            and row.get("research_boundary")
            == "metadata_route_only_not_scholarship"
        ):
            source_id = row.get("source_id", "")
            counts[source_id] = counts.get(source_id, 0) + 1
    return counts


def source_gap_types(
    pipeline_row: dict[str, str],
    coverage_row: dict[str, str],
    reviewed_browser_capture_count: int = 0,
) -> list[str]:
    gap_types: list[str] = []
    status_counts = pipeline_row.get("download_status_counts", "")
    access_boundary_count = max(
        download_access_boundary_count(status_counts)
        - reviewed_browser_capture_count,
        0,
    )
    if access_boundary_count > 0:
        gap_types.append("access_boundary_or_error_followup")
    checksum_exception_count = max(
        int_value(pipeline_row, "download_log_count")
        - int_value(pipeline_row, "checksum_present_count")
        - reviewed_browser_capture_count,
        0,
    )
    # A failed or access-restricted attempt has no source payload to hash. Its
    # absent checksum is evidence of the same access condition, not a second
    # human task. Only checksum exceptions beyond unresolved access attempts
    # remain an independent gap.
    if checksum_exception_count > access_boundary_count:
        gap_types.append("checksum_or_failed_download_status_review_needed")
    if (
        int_value(coverage_row, "downloaded_file_bytes") >= SIZE_LIMIT_BYTES
        and int_value(pipeline_row, "large_source_register_count") == 0
    ):
        gap_types.append("large_source_register_review_needed")
    if int_value(pipeline_row, "downloaded_count") > 0 and int_value(pipeline_row, "metadata_profile_count") == 0:
        gap_types.append("metadata_profile_extraction_needed")
    if int_value(pipeline_row, "downloaded_count") > 0 and int_value(pipeline_row, "field_map_count") == 0:
        gap_types.append("source_field_map_needed")
    if int_value(pipeline_row, "downloaded_count") > 0 and int_value(pipeline_row, "package_manifest_count") == 0:
        gap_types.append("package_file_manifest_or_not_applicable_decision_needed")
    if (
        int_value(pipeline_row, "metadata_profile_count") > 0
        and (
            int_value(pipeline_row, "downloaded_count") > 0
            or reviewed_browser_capture_count == 0
        )
        and int_value(pipeline_row, "package_manifest_count") == 0
        and int_value(pipeline_row, "graph_edge_count") == 0
        and int_value(pipeline_row, "candidate_queue_count") == 0
        and int_value(pipeline_row, "asset_count") == 0
    ):
        gap_types.append("safe_derived_record_decision_needed")
    return gap_types


def observed_gap_evidence(pipeline_row: dict[str, str], coverage_row: dict[str, str], gap_type: str) -> str:
    evidence = [
        f"current_stage={pipeline_row['current_stage']}",
        f"download_status_counts={pipeline_row['download_status_counts']}",
        f"downloaded_count={pipeline_row['downloaded_count']}",
        f"download_log_count={pipeline_row['download_log_count']}",
        f"checksum_present_count={pipeline_row['checksum_present_count']}",
        f"field_map_count={pipeline_row['field_map_count']}",
        f"package_manifest_count={pipeline_row['package_manifest_count']}",
        f"metadata_profile_count={pipeline_row['metadata_profile_count']}",
        f"graph_edge_count={pipeline_row['graph_edge_count']}",
        f"downloaded_file_bytes={coverage_row.get('downloaded_file_bytes', '0')}",
        f"gap_type={gap_type}",
    ]
    return ";".join(evidence)


def expected_output_path(source_id: str, gap_type: str, index: int) -> str:
    return (
        "doc/public/user_research/009_source-engineering-gap-review-queues/"
        f"{index:04d}_{source_id}_{gap_type}_review-log.md"
    )


def build_gap_rows(
    pipeline_rows: list[dict[str, str]],
    coverage_rows: list[dict[str, str]],
    browser_metadata_rows: list[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    coverage_by_source = {row["source_id"]: row for row in coverage_rows}
    capture_counts = reviewed_browser_capture_counts(browser_metadata_rows or [])
    draft_rows: list[tuple[dict[str, str], str]] = []
    for pipeline_row in pipeline_rows:
        source_id = pipeline_row["source_id"]
        coverage_row = coverage_by_source[source_id]
        for gap_type in source_gap_types(
            pipeline_row,
            coverage_row,
            capture_counts.get(source_id, 0),
        ):
            draft_rows.append((pipeline_row, gap_type))

    draft_rows.sort(key=lambda item: (GAP_PRIORITY[item[1]], item[0]["source_id"]))
    output_rows: list[dict[str, str]] = []
    for index, (pipeline_row, gap_type) in enumerate(draft_rows, start=1):
        source_id = pipeline_row["source_id"]
        coverage_row = coverage_by_source[source_id]
        output_rows.append(
            {
                "source_engineering_gap_id": f"source-engineering-gap-{index:04d}",
                "source_id": source_id,
                "priority_rank": str(GAP_PRIORITY[gap_type]),
                "gap_type": gap_type,
                "current_stage": pipeline_row["current_stage"],
                "authority_tier": pipeline_row["authority_tier"],
                "rights_status": pipeline_row["rights_status"],
                "download_manifest_count": pipeline_row["download_manifest_count"],
                "download_log_count": pipeline_row["download_log_count"],
                "downloaded_count": pipeline_row["downloaded_count"],
                "access_boundary_or_error_count": pipeline_row["access_boundary_or_error_count"],
                "checksum_present_count": pipeline_row["checksum_present_count"],
                "size_recorded_count": pipeline_row["size_recorded_count"],
                "field_map_count": pipeline_row["field_map_count"],
                "large_source_register_count": pipeline_row["large_source_register_count"],
                "package_manifest_count": pipeline_row["package_manifest_count"],
                "metadata_profile_count": pipeline_row["metadata_profile_count"],
                "asset_count": pipeline_row["asset_count"],
                "candidate_queue_count": pipeline_row["candidate_queue_count"],
                "graph_edge_count": pipeline_row["graph_edge_count"],
                "downloaded_file_bytes": coverage_row.get("downloaded_file_bytes", "0"),
                "download_status_counts": pipeline_row["download_status_counts"],
                "observed_gap_evidence": observed_gap_evidence(pipeline_row, coverage_row, gap_type),
                "required_next_checks": ";".join(GAP_CHECKS[gap_type]),
                "route_files_to_open": ";".join(path.as_posix() for path in ROUTE_FILES_BY_GAP[gap_type]),
                "expected_output_path": expected_output_path(source_id, gap_type, index),
                "commit_policy_boundary": "metadata_review_only_raw_or_temporary_material_stays_outside_regular_git",
                "source_promotion_status": "not_promoted",
                "research_boundary": RESEARCH_BOUNDARY,
                "review_status": "needs_source_engineering_review",
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Build source-engineering gap review queue.")
    parser.add_argument("--repo-root", type=Path, default=repo_root())
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    root = args.repo_root.resolve()
    rows = build_gap_rows(
        read_csv_rows(root / SOURCE_PROCESSING_PIPELINE_AUDIT),
        read_csv_rows(root / SOURCE_COVERAGE_SUMMARY),
        read_csv_rows(root / BROWSER_VERIFIED_METADATA_CAPTURE),
    )
    output = args.output if args.output.is_absolute() else root / args.output
    write_csv(output, rows)
    print(f"wrote={len(rows)} {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
