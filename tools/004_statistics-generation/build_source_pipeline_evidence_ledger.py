#!/usr/bin/env python3
"""Build a source-level evidence ledger for preprocessing review.

The ledger records the source-engineering evidence already present on disk for
each registered source. It is a factual routing surface only: counts and paths
are not rights decisions, corpus imports, source promotions, or decipherment
claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/134_ai-agent-source-pipeline-evidence-ledger.csv")
SOURCE_PROCESSING_PIPELINE_AUDIT = Path("corpus/009_statistics-and-derived-features/094_source-processing-pipeline-audit.csv")
SOURCE_PIPELINE_GAP_MATRIX = Path("corpus/009_statistics-and-derived-features/132_ai-agent-source-pipeline-gap-matrix.csv")
SOURCE_PIPELINE_GAP_REVIEW_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/133_ai-agent-source-pipeline-gap-review-checklist.csv"
)
UPDATED_AT = "2026-06-19"
CLAIM_BOUNDARY = "source_pipeline_evidence_ledger_not_review_outcome_not_scholarship"
CAUTION = (
    "Source pipeline evidence ledger only; counts and paths are not collected review evidence, "
    "not a rights decision, not source promotion, not a corpus import, and not a decipherment conclusion."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def as_int(row: dict[str, str], field: str) -> int:
    value = row.get(field, "")
    return int(value) if value.isdigit() else 0


def download_evidence_status(pipeline: dict[str, str]) -> str:
    downloaded = as_int(pipeline, "downloaded_count")
    access_or_error = as_int(pipeline, "access_boundary_or_error_count")
    checksum_present = as_int(pipeline, "checksum_present_count")
    download_logs = as_int(pipeline, "download_log_count")
    if downloaded == 0:
        return "access_or_download_not_resolved"
    if access_or_error or checksum_present < download_logs:
        return "downloaded_with_access_or_checksum_review_needed"
    return "downloaded_with_size_and_checksum_evidence"


def manifest_evidence_status(pipeline: dict[str, str]) -> str:
    if as_int(pipeline, "package_manifest_count"):
        return "package_manifest_present"
    return "package_manifest_missing_or_not_applicable_unreviewed"


def metadata_profile_status(pipeline: dict[str, str]) -> str:
    if as_int(pipeline, "metadata_profile_count"):
        return "metadata_profile_present"
    return "metadata_profile_missing_or_not_applicable_unreviewed"


def derivative_evidence_status(pipeline: dict[str, str]) -> str:
    if as_int(pipeline, "candidate_queue_count") or as_int(pipeline, "graph_edge_count"):
        return "candidate_or_graph_derivatives_present_pending_review"
    return "no_candidate_or_graph_derivatives_recorded"


def evidence_completeness_status(pipeline: dict[str, str]) -> str:
    if (
        as_int(pipeline, "downloaded_count")
        and as_int(pipeline, "checksum_present_count")
        and as_int(pipeline, "package_manifest_count")
        and as_int(pipeline, "metadata_profile_count")
        and (as_int(pipeline, "candidate_queue_count") or as_int(pipeline, "graph_edge_count"))
    ):
        return "source_evidence_and_derivatives_present_pending_review"
    return "source_evidence_has_gaps_pending_review"


def evidence_counts_summary(pipeline: dict[str, str]) -> str:
    fields = [
        "download_manifest_count",
        "download_log_count",
        "downloaded_count",
        "checksum_present_count",
        "size_recorded_count",
        "package_manifest_count",
        "metadata_profile_count",
        "large_source_register_count",
        "candidate_queue_count",
        "graph_edge_count",
    ]
    return ";".join(f"{field.replace('_count', '')}:{pipeline[field]}" for field in fields)


def build_ledger_rows(root: Path) -> list[dict[str, str]]:
    pipeline_rows = read_csv_rows(root / SOURCE_PROCESSING_PIPELINE_AUDIT)
    checklist_rows = read_csv_rows(root / SOURCE_PIPELINE_GAP_REVIEW_CHECKLIST)
    checklist_by_source = {row["source_id"]: row for row in checklist_rows}

    rows: list[dict[str, str]] = []
    for index, pipeline in enumerate(sorted(pipeline_rows, key=lambda item: item["source_id"]), start=1):
        checklist = checklist_by_source[pipeline["source_id"]]
        rows.append(
            {
                "ledger_id": f"source-pipeline-evidence-ledger-{index:03d}",
                "checklist_id": checklist["checklist_id"],
                "source_id": pipeline["source_id"],
                "source_type": pipeline["source_type"],
                "rights_status": checklist["rights_status"],
                "pipeline_gap_status": checklist["pipeline_gap_status"],
                "review_lane": checklist["review_lane"],
                "required_review_steps": checklist["required_review_steps"],
                "download_manifest_count": pipeline["download_manifest_count"],
                "download_log_count": pipeline["download_log_count"],
                "downloaded_count": pipeline["downloaded_count"],
                "access_boundary_or_error_count": pipeline["access_boundary_or_error_count"],
                "checksum_present_count": pipeline["checksum_present_count"],
                "size_recorded_count": pipeline["size_recorded_count"],
                "field_map_count": pipeline["field_map_count"],
                "large_source_register_count": pipeline["large_source_register_count"],
                "package_manifest_count": pipeline["package_manifest_count"],
                "metadata_profile_count": pipeline["metadata_profile_count"],
                "asset_count": pipeline["asset_count"],
                "candidate_queue_count": pipeline["candidate_queue_count"],
                "cross_source_crosswalk_match_count": pipeline["cross_source_crosswalk_match_count"],
                "graph_edge_count": pipeline["graph_edge_count"],
                "download_evidence_status": download_evidence_status(pipeline),
                "manifest_evidence_status": manifest_evidence_status(pipeline),
                "metadata_profile_status": metadata_profile_status(pipeline),
                "derivative_evidence_status": derivative_evidence_status(pipeline),
                "evidence_completeness_status": evidence_completeness_status(pipeline),
                "evidence_counts_summary": evidence_counts_summary(pipeline),
                "route_files_to_open": checklist["route_files_to_open"],
                "checklist_path": SOURCE_PIPELINE_GAP_REVIEW_CHECKLIST.as_posix(),
                "pipeline_audit_path": SOURCE_PROCESSING_PIPELINE_AUDIT.as_posix(),
                "gap_matrix_path": SOURCE_PIPELINE_GAP_MATRIX.as_posix(),
                "ledger_status": "pending_human_review",
                "reviewed_evidence_paths": "",
                "review_outcome_summary": "",
                "claim_boundary": CLAIM_BOUNDARY,
                "rights_decision_status": "no_new_rights_decision",
                "source_promotion_status": "not_promoted",
                "corpus_import_status": "not_imported",
                "decipherment_claim_status": "no_decipherment_claim",
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


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
    rows = build_ledger_rows(root)
    write_csv(root / args.csv_output, rows)
    print(f"source_pipeline_evidence_ledger_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
