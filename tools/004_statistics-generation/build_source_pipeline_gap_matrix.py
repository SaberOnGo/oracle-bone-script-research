#!/usr/bin/env python3
"""Build a source-level pipeline gap matrix.

The matrix converts the source processing audit into a per-source review
surface. It records engineering gaps and next review lanes only; it does not
promote sources, import corpus records, decide rights, or make decipherment
claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/132_ai-agent-source-pipeline-gap-matrix.csv")
UPDATED_AT = "2026-06-19"
SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_PIPELINE_AUDIT = Path("corpus/009_statistics-and-derived-features/094_source-processing-pipeline-audit.csv")
SOURCE_ROUTE_REVIEW_QUEUE = Path("corpus/009_statistics-and-derived-features/009_ai-agent-source-route-review-queue.csv")
CLAIM_BOUNDARY = "source_pipeline_gap_matrix_not_scholarship_not_import_not_rights_decision"
CAUTION = (
    "Source pipeline gap matrix only; not a corpus import, not a rights decision, "
    "not source promotion, and not a decipherment conclusion."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def as_int(row: dict[str, str], field: str) -> int:
    value = row.get(field, "")
    return int(value) if value.isdigit() else 0


def gap_flags_for(row: dict[str, str]) -> list[str]:
    flags: list[str] = []
    if as_int(row, "downloaded_count") == 0:
        flags.append("not_downloaded_or_access_not_resolved")
    if as_int(row, "access_boundary_or_error_count"):
        flags.append("access_boundary_or_error_pending_review")
    if (
        as_int(row, "downloaded_count")
        and as_int(row, "download_log_count")
        and as_int(row, "checksum_present_count") < as_int(row, "download_log_count")
    ):
        flags.append("checksum_or_failed_download_status_pending_review")
    if as_int(row, "field_map_count") == 0:
        flags.append("missing_field_map")
    if as_int(row, "package_manifest_count") == 0:
        flags.append("missing_package_manifest")
    if as_int(row, "metadata_profile_count") == 0:
        flags.append("missing_metadata_profile")
    if as_int(row, "candidate_queue_count") or as_int(row, "graph_edge_count"):
        flags.append("candidate_or_graph_derivatives_pending_review")
    return flags or ["no_automatic_gap_detected_keep_monitoring"]


def pipeline_gap_status(row: dict[str, str], flags: list[str]) -> str:
    if "not_downloaded_or_access_not_resolved" in flags:
        return "needs_download_or_access_review"
    if "access_boundary_or_error_pending_review" in flags or "checksum_or_failed_download_status_pending_review" in flags:
        return "needs_access_boundary_review"
    if "candidate_or_graph_derivatives_pending_review" in flags:
        return "needs_safe_derived_record_review"
    if "missing_field_map" in flags:
        return "needs_field_map_review"
    if "missing_package_manifest" in flags:
        return "needs_package_manifest_review"
    if "missing_metadata_profile" in flags:
        return "needs_metadata_profile_review"
    return "ready_for_source_engineering_review"


def review_lane_for(status: str) -> str:
    if status in {"needs_download_or_access_review", "needs_access_boundary_review"}:
        return "access_and_checksum_boundary_resolution"
    if status == "needs_field_map_review":
        return "field_map_semantics_review"
    if status in {"needs_package_manifest_review", "needs_metadata_profile_review"}:
        return "metadata_profile_and_package_manifest_decision"
    if status == "needs_safe_derived_record_review":
        return "safe_derived_record_decision"
    return "source_register_monitoring"


def build_gap_rows(root: Path) -> list[dict[str, str]]:
    source_rows = read_csv_rows(root / SOURCE_INDEX)
    audit_rows = read_csv_rows(root / SOURCE_PIPELINE_AUDIT)
    sources_by_id = {row["source_id"]: row for row in source_rows}

    output_rows: list[dict[str, str]] = []
    for index, audit in enumerate(sorted(audit_rows, key=lambda item: item["source_id"]), start=1):
        source = sources_by_id[audit["source_id"]]
        flags = gap_flags_for(audit)
        status = pipeline_gap_status(audit, flags)
        output_rows.append(
            {
                "gap_matrix_row_id": f"source-pipeline-gap-{index:03d}",
                "source_id": audit["source_id"],
                "source_type": source["source_type"],
                "provider": source["provider"],
                "authority_tier": source["authority_tier"],
                "adoption_status": source["adoption_status"],
                "rights_status": source["rights_status"],
                "risk_note": source["risk_note"],
                "source_review_status": source["review_status"],
                "current_stage": audit["current_stage"],
                "pipeline_gap_status": status,
                "review_lane": review_lane_for(status),
                "gap_flags": ";".join(flags),
                "download_manifest_count": audit["download_manifest_count"],
                "download_log_count": audit["download_log_count"],
                "downloaded_count": audit["downloaded_count"],
                "access_boundary_or_error_count": audit["access_boundary_or_error_count"],
                "checksum_present_count": audit["checksum_present_count"],
                "size_recorded_count": audit["size_recorded_count"],
                "field_map_count": audit["field_map_count"],
                "large_source_register_count": audit["large_source_register_count"],
                "package_manifest_count": audit["package_manifest_count"],
                "metadata_profile_count": audit["metadata_profile_count"],
                "asset_count": audit["asset_count"],
                "candidate_queue_count": audit["candidate_queue_count"],
                "cross_source_crosswalk_match_count": audit["cross_source_crosswalk_match_count"],
                "graph_edge_count": audit["graph_edge_count"],
                "source_route_review_queue_count": audit["source_route_review_queue_count"],
                "source_register_path": SOURCE_INDEX.as_posix(),
                "pipeline_audit_path": SOURCE_PIPELINE_AUDIT.as_posix(),
                "next_entry_path": SOURCE_ROUTE_REVIEW_QUEUE.as_posix(),
                "claim_boundary": CLAIM_BOUNDARY,
                "rights_decision_status": "no_new_rights_decision",
                "source_promotion_status": "not_promoted",
                "corpus_import_status": "not_imported",
                "decipherment_claim_status": "no_decipherment_claim",
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return output_rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_gap_rows(root)
    write_csv(root / args.csv_output, rows)
    print(f"source_pipeline_gap_matrix_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
