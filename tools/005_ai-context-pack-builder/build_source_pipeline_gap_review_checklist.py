#!/usr/bin/env python3
"""Build a review checklist from the source pipeline gap matrix.

The checklist gives one not-started review row per registered source. It points
reviewers at existing provenance and pipeline files, but it does not collect
evidence, decide rights, promote sources, import corpus records, or make
decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/133_ai-agent-source-pipeline-gap-review-checklist.csv")
SOURCE_PIPELINE_GAP_MATRIX = Path("corpus/009_statistics-and-derived-features/132_ai-agent-source-pipeline-gap-matrix.csv")
SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_DOWNLOAD_MANIFEST = Path("corpus/006_research-sources-and-bibliography/000_source-registers/003_source-download-manifest.csv")
SOURCE_FIELD_MAP = Path("corpus/006_research-sources-and-bibliography/000_source-registers/007_source-field-map.csv")
SOURCE_PACKAGE_FILE_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv"
)
DOWNLOADED_METADATA_PROFILE = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/010_downloaded-metadata-profile.csv"
)
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
LARGE_SOURCE_REGISTER = Path("project_registry/006_large-source-register/001_large-source-register.csv")
SOURCE_PROCESSING_PIPELINE_AUDIT = Path("corpus/009_statistics-and-derived-features/094_source-processing-pipeline-audit.csv")
SOURCE_ROUTE_REVIEW_QUEUE = Path("corpus/009_statistics-and-derived-features/009_ai-agent-source-route-review-queue.csv")
UPDATED_AT = "2026-06-19"
CLAIM_BOUNDARY = "source_pipeline_gap_review_checklist_not_evidence_not_import_not_scholarship"
CAUTION = (
    "Source pipeline gap review checklist only; not collected evidence, not a rights decision, "
    "not source promotion, not a corpus import, and not a decipherment conclusion."
)

BASE_ROUTE_PATHS = [
    SOURCE_PIPELINE_GAP_MATRIX,
    SOURCE_INDEX,
    SOURCE_PROCESSING_PIPELINE_AUDIT,
    SOURCE_ROUTE_REVIEW_QUEUE,
    SOURCE_DOWNLOAD_MANIFEST,
    SOURCE_DOWNLOAD_LOG,
    SOURCE_FIELD_MAP,
    SOURCE_PACKAGE_FILE_MANIFEST,
    DOWNLOADED_METADATA_PROFILE,
    LARGE_SOURCE_REGISTER,
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def required_steps(flags: str) -> list[str]:
    flag_set = set(flags.split(";"))
    steps = ["open_source_register_and_risk_note", "verify_rights_status_before_any_use"]
    if "not_downloaded_or_access_not_resolved" in flag_set:
        steps.append("verify_download_or_access_boundary")
    if "access_boundary_or_error_pending_review" in flag_set:
        steps.append("verify_access_boundary_or_error_status")
    if "checksum_or_failed_download_status_pending_review" in flag_set:
        steps.append("verify_checksum_and_download_status")
    if "missing_field_map" in flag_set:
        steps.append("verify_field_map_absence_or_plan")
    if "missing_package_manifest" in flag_set:
        steps.append("review_package_manifest_or_not_applicable")
    if "missing_metadata_profile" in flag_set or "missing_package_manifest" in flag_set:
        steps.append("review_metadata_profile_or_not_applicable")
    if "candidate_or_graph_derivatives_pending_review" in flag_set:
        steps.append("review_candidate_or_graph_derivatives")
    steps.append("record_human_review_outcome_before_promotion")
    return steps


def route_files_to_open() -> str:
    return ";".join(path.as_posix() for path in BASE_ROUTE_PATHS)


def build_checklist_rows(root: Path) -> list[dict[str, str]]:
    gap_rows = read_csv_rows(root / SOURCE_PIPELINE_GAP_MATRIX)
    route_files = route_files_to_open()
    rows: list[dict[str, str]] = []
    for index, gap in enumerate(gap_rows, start=1):
        rows.append(
            {
                "checklist_id": f"source-pipeline-gap-review-checklist-{index:03d}",
                "gap_matrix_row_id": gap["gap_matrix_row_id"],
                "source_id": gap["source_id"],
                "source_type": gap["source_type"],
                "provider": gap["provider"],
                "rights_status": gap["rights_status"],
                "pipeline_gap_status": gap["pipeline_gap_status"],
                "review_lane": gap["review_lane"],
                "gap_flags": gap["gap_flags"],
                "required_review_steps": ";".join(required_steps(gap["gap_flags"])),
                "route_files_to_open": route_files,
                "gap_matrix_path": SOURCE_PIPELINE_GAP_MATRIX.as_posix(),
                "checklist_status": "not_started",
                "evidence_collection_status": "not_collected",
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
    rows = build_checklist_rows(root)
    write_csv(root / args.csv_output, rows)
    print(f"source_pipeline_gap_review_checklist_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
