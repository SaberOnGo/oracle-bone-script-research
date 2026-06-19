#!/usr/bin/env python3
"""Build an empty result scaffold for source pipeline phase actions."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/138_source-pipeline-phase-action-result-scaffold.csv")
SOURCE_PIPELINE_PHASE_ACTION_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/137_source-pipeline-phase-action-queue.csv"
)
UPDATED_AT = "2026-06-19"
RESULT_STATUS = "not_started"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_result_scaffold_not_scholarship"
RESERVED_OUTCOME_FIELDS = ";".join(
    [
        "access_outcome_reviewed",
        "package_manifest_outcome_reviewed",
        "metadata_extraction_outcome_reviewed",
        "cleaning_outcome_reviewed",
        "structured_derivative_outcome_reviewed",
        "linkage_outcome_reviewed",
        "verification_outcome_reviewed",
        "reviewed_evidence_paths",
        "reviewed_outcome_summary",
        "remaining_blockers_reviewed",
        "required_followup_reviewed",
        "human_reviewer_id",
        "human_review_date",
        "human_review_notes",
    ]
)
CAUTION = (
    "This source pipeline phase action result scaffold is human-fillable and empty. "
    "It is not collected evidence, not a rights decision, not source promotion, "
    "not a corpus import, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "result_scaffold_id",
    "action_id",
    "phase_row_id",
    "source_id",
    "source_type",
    "rights_status",
    "pipeline_gap_status",
    "review_lane",
    "phase_name",
    "phase_status",
    "action_type",
    "action_priority",
    "downloaded_count",
    "checksum_present_count",
    "package_manifest_count",
    "metadata_profile_count",
    "candidate_queue_count",
    "cross_source_crosswalk_match_count",
    "graph_edge_count",
    "action_queue_path",
    "phase_coverage_path",
    "phase_evidence_paths",
    "route_files_to_open",
    "reserved_outcome_fields",
    "result_status",
    "evidence_collection_status",
    "reviewed_evidence_paths",
    "access_outcome_reviewed",
    "package_manifest_outcome_reviewed",
    "metadata_extraction_outcome_reviewed",
    "cleaning_outcome_reviewed",
    "structured_derivative_outcome_reviewed",
    "linkage_outcome_reviewed",
    "verification_outcome_reviewed",
    "reviewed_outcome_summary",
    "remaining_blockers_reviewed",
    "required_followup_reviewed",
    "human_reviewer_id",
    "human_review_date",
    "human_review_notes",
    "human_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def build_result_scaffold_rows(root: Path) -> list[dict[str, str]]:
    action_rows = read_csv_rows(root / SOURCE_PIPELINE_PHASE_ACTION_QUEUE)
    rows: list[dict[str, str]] = []
    for index, action in enumerate(action_rows, start=1):
        rows.append(
            {
                "result_scaffold_id": f"source-pipeline-phase-action-result-scaffold-{index:03d}",
                "action_id": action["action_id"],
                "phase_row_id": action["phase_row_id"],
                "source_id": action["source_id"],
                "source_type": action["source_type"],
                "rights_status": action["rights_status"],
                "pipeline_gap_status": action["pipeline_gap_status"],
                "review_lane": action["review_lane"],
                "phase_name": action["phase_name"],
                "phase_status": action["phase_status"],
                "action_type": action["action_type"],
                "action_priority": action["action_priority"],
                "downloaded_count": action["downloaded_count"],
                "checksum_present_count": action["checksum_present_count"],
                "package_manifest_count": action["package_manifest_count"],
                "metadata_profile_count": action["metadata_profile_count"],
                "candidate_queue_count": action["candidate_queue_count"],
                "cross_source_crosswalk_match_count": action["cross_source_crosswalk_match_count"],
                "graph_edge_count": action["graph_edge_count"],
                "action_queue_path": SOURCE_PIPELINE_PHASE_ACTION_QUEUE.as_posix(),
                "phase_coverage_path": action["phase_coverage_path"],
                "phase_evidence_paths": action["phase_evidence_paths"],
                "route_files_to_open": action["route_files_to_open"],
                "reserved_outcome_fields": RESERVED_OUTCOME_FIELDS,
                "result_status": RESULT_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "reviewed_evidence_paths": "",
                "access_outcome_reviewed": "",
                "package_manifest_outcome_reviewed": "",
                "metadata_extraction_outcome_reviewed": "",
                "cleaning_outcome_reviewed": "",
                "structured_derivative_outcome_reviewed": "",
                "linkage_outcome_reviewed": "",
                "verification_outcome_reviewed": "",
                "reviewed_outcome_summary": "",
                "remaining_blockers_reviewed": action["next_review_steps"],
                "required_followup_reviewed": "",
                "human_reviewer_id": "",
                "human_review_date": "",
                "human_review_notes": "",
                "human_review_status": HUMAN_REVIEW_STATUS,
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "corpus_import_status": CORPUS_IMPORT_STATUS,
                "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_result_scaffold_rows(root)
    write_csv(root / args.csv_output, rows)
    print(f"source_pipeline_phase_action_result_scaffold_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
