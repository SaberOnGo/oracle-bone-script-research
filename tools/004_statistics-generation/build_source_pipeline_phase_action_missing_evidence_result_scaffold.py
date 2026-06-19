#!/usr/bin/env python3
"""Build an empty result scaffold for missing source evidence actions."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


OUTPUT_CSV = Path(
    "corpus/009_statistics-and-derived-features/145_source-pipeline-phase-action-missing-evidence-result-scaffold.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ACTION_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/144_source-pipeline-phase-action-missing-evidence-action-queue.csv"
)
UPDATED_AT = "2026-06-19"
RESULT_STATUS = "not_started"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_missing_evidence_result_scaffold_not_scholarship"
RESERVED_OUTCOME_FIELDS = ";".join(
    [
        "missing_role_applicability_reviewed",
        "target_source_row_action_reviewed",
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
    "This source pipeline missing-evidence result scaffold is human-fillable "
    "and empty. It is not collected evidence, not a rights decision, not source "
    "promotion, not a corpus import, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "missing_evidence_result_scaffold_id",
    "missing_evidence_action_id",
    "evidence_presence_row_id",
    "source_id",
    "source_type",
    "rights_status",
    "pipeline_gap_status",
    "review_lanes",
    "phase_names",
    "missing_file_role",
    "file_to_open",
    "join_strategy",
    "missing_reason",
    "action_type",
    "action_priority",
    "action_queue_path",
    "evidence_presence_matrix_path",
    "file_checklist_path",
    "source_summary_path",
    "source_gap_summary_path",
    "route_ids",
    "result_scaffold_ids",
    "action_ids",
    "reserved_outcome_fields",
    "result_status",
    "evidence_collection_status",
    "missing_role_applicability_reviewed",
    "target_source_row_action_reviewed",
    "reviewed_evidence_paths",
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def build_missing_evidence_result_scaffold_rows(action_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, action in enumerate(action_rows, start=1):
        rows.append(
            {
                "missing_evidence_result_scaffold_id": (
                    f"source-pipeline-phase-action-missing-evidence-result-{index:03d}"
                ),
                "missing_evidence_action_id": action["missing_evidence_action_id"],
                "evidence_presence_row_id": action["evidence_presence_row_id"],
                "source_id": action["source_id"],
                "source_type": action["source_type"],
                "rights_status": action["rights_status"],
                "pipeline_gap_status": action["pipeline_gap_status"],
                "review_lanes": action["review_lanes"],
                "phase_names": action["phase_names"],
                "missing_file_role": action["missing_file_role"],
                "file_to_open": action["file_to_open"],
                "join_strategy": action["join_strategy"],
                "missing_reason": action["missing_reason"],
                "action_type": action["action_type"],
                "action_priority": action["action_priority"],
                "action_queue_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ACTION_QUEUE.as_posix(),
                "evidence_presence_matrix_path": action["evidence_presence_matrix_path"],
                "file_checklist_path": action["file_checklist_path"],
                "source_summary_path": action["source_summary_path"],
                "source_gap_summary_path": action["source_gap_summary_path"],
                "route_ids": action["route_ids"],
                "result_scaffold_ids": action["result_scaffold_ids"],
                "action_ids": action["action_ids"],
                "reserved_outcome_fields": RESERVED_OUTCOME_FIELDS,
                "result_status": RESULT_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "missing_role_applicability_reviewed": "",
                "target_source_row_action_reviewed": "",
                "reviewed_evidence_paths": "",
                "reviewed_outcome_summary": "",
                "remaining_blockers_reviewed": action["action_type"],
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
    parser.add_argument("--action-queue", default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ACTION_QUEUE))
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parents[2]
    rows = build_missing_evidence_result_scaffold_rows(read_csv_rows(root / args.action_queue))
    write_csv(root / args.csv_output, rows)
    print(f"source_pipeline_phase_action_missing_evidence_result_scaffold_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
