#!/usr/bin/env python3
"""Build an action queue from per-source preprocessing phase gaps."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/137_source-pipeline-phase-action-queue.csv")
SOURCE_PIPELINE_PHASE_COVERAGE_MATRIX = Path(
    "corpus/009_statistics-and-derived-features/136_source-pipeline-phase-coverage-matrix.csv"
)
UPDATED_AT = "2026-06-19"
CLAIM_BOUNDARY = "source_pipeline_phase_action_queue_not_review_outcome_not_scholarship"
CAUTION = (
    "Source pipeline phase action queue only; rows identify human-review actions "
    "from existing phase gaps and do not decide rights, promote sources, import "
    "corpus records, or make decipherment claims."
)

ACTION_TYPES = {
    "downloaded": "resolve_download_or_access_boundary",
    "unpacked": "review_package_manifest_or_raw_package_handling",
    "extracted": "plan_metadata_or_record_extraction",
    "cleaned": "review_cleaning_and_normalization_rules",
    "structured": "create_or_review_structured_derivatives",
    "linked": "review_cross_source_or_graph_linkage",
    "verified": "record_human_review_outcome",
}

ACTION_PRIORITIES = {
    "downloaded": "high_access_boundary_review",
    "unpacked": "high_package_boundary_review",
    "extracted": "source_pipeline_review",
    "cleaned": "source_pipeline_review",
    "structured": "source_pipeline_review",
    "linked": "source_pipeline_review",
    "verified": "human_outcome_review",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def phases_for_action(row: dict[str, str]) -> list[str]:
    return [phase for phase in row["missing_or_review_needed_phases"].split(";") if phase]


def build_action_rows(root: Path) -> list[dict[str, str]]:
    phase_rows = read_csv_rows(root / SOURCE_PIPELINE_PHASE_COVERAGE_MATRIX)
    rows: list[dict[str, str]] = []
    for phase_row in phase_rows:
        for phase_name in phases_for_action(phase_row):
            rows.append(
                {
                    "action_id": f"source-pipeline-phase-action-{len(rows) + 1:03d}",
                    "phase_row_id": phase_row["phase_row_id"],
                    "source_id": phase_row["source_id"],
                    "source_type": phase_row["source_type"],
                    "rights_status": phase_row["rights_status"],
                    "pipeline_gap_status": phase_row["pipeline_gap_status"],
                    "review_lane": phase_row["review_lane"],
                    "phase_name": phase_name,
                    "phase_status": phase_row[f"{phase_name}_status"],
                    "action_type": ACTION_TYPES[phase_name],
                    "action_priority": ACTION_PRIORITIES[phase_name],
                    "downloaded_count": phase_row["downloaded_count"],
                    "checksum_present_count": phase_row["checksum_present_count"],
                    "package_manifest_count": phase_row["package_manifest_count"],
                    "metadata_profile_count": phase_row["metadata_profile_count"],
                    "candidate_queue_count": phase_row["candidate_queue_count"],
                    "cross_source_crosswalk_match_count": phase_row["cross_source_crosswalk_match_count"],
                    "graph_edge_count": phase_row["graph_edge_count"],
                    "missing_or_review_needed_phases": phase_row["missing_or_review_needed_phases"],
                    "next_review_steps": phase_row["next_review_steps"],
                    "phase_evidence_paths": phase_row["phase_evidence_paths"],
                    "route_files_to_open": phase_row["route_files_to_open"],
                    "phase_coverage_path": SOURCE_PIPELINE_PHASE_COVERAGE_MATRIX.as_posix(),
                    "queue_status": "pending_human_review",
                    "review_outcome_status": "not_recorded",
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
    rows = build_action_rows(root)
    write_csv(root / args.csv_output, rows)
    print(f"source_pipeline_phase_action_queue_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
