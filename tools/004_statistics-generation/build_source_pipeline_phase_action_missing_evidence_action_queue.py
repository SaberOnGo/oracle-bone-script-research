#!/usr/bin/env python3
"""Build human-review actions for missing source-pipeline evidence rows."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


OUTPUT_CSV = Path(
    "corpus/009_statistics-and-derived-features/144_source-pipeline-phase-action-missing-evidence-action-queue.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_PRESENCE_MATRIX = Path(
    "corpus/009_statistics-and-derived-features/142_source-pipeline-phase-action-evidence-presence-matrix.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_FILE_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/141_source-pipeline-phase-action-file-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_GAP_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/143_source-pipeline-phase-action-evidence-gap-summary.csv"
)
UPDATED_AT = "2026-06-19"
REVIEW_STATUS = "pending_human_review"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_missing_evidence_action_queue_not_scholarship"
CAUTION = (
    "This source pipeline missing-evidence action queue only expands existing "
    "missing source-file presence signals into human-review tasks. It does not "
    "collect new evidence, decide rights, promote sources, import corpus "
    "records, or make decipherment conclusions."
)

ACTION_BY_ROLE = {
    "source_field_map": (
        "review_or_create_source_field_map_row",
        "field_map_gap_review",
    ),
    "source_package_file_manifest": (
        "review_package_manifest_applicability_or_create_row",
        "package_manifest_gap_review",
    ),
    "downloaded_metadata_profile": (
        "review_downloaded_metadata_profile_or_mark_not_applicable",
        "metadata_profile_gap_review",
    ),
    "large_source_register": (
        "review_large_source_register_applicability_or_mark_not_applicable",
        "large_source_register_gap_review",
    ),
}

OUTPUT_FIELDS = [
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
    "action_status",
    "evidence_presence_matrix_path",
    "file_checklist_path",
    "source_summary_path",
    "source_gap_summary_path",
    "route_ids",
    "result_scaffold_ids",
    "action_ids",
    "review_status",
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


def action_for_role(role: str) -> tuple[str, str]:
    return ACTION_BY_ROLE.get(role, ("review_missing_source_evidence_role", "missing_evidence_gap_review"))


def build_missing_evidence_action_rows(evidence_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    missing_rows = sorted(
        (row for row in evidence_rows if row["match_status"] == "missing_for_source"),
        key=lambda row: (row["source_id"], row["file_role"]),
    )
    rows: list[dict[str, str]] = []
    for index, row in enumerate(missing_rows, start=1):
        action_type, action_priority = action_for_role(row["file_role"])
        rows.append(
            {
                "missing_evidence_action_id": f"source-pipeline-phase-action-missing-evidence-{index:03d}",
                "evidence_presence_row_id": row["evidence_presence_row_id"],
                "source_id": row["source_id"],
                "source_type": row["source_type"],
                "rights_status": row["rights_status"],
                "pipeline_gap_status": row["pipeline_gap_status"],
                "review_lanes": row["review_lanes"],
                "phase_names": row["phase_names"],
                "missing_file_role": row["file_role"],
                "file_to_open": row["file_to_open"],
                "join_strategy": row["join_strategy"],
                "missing_reason": "no_source_matched_rows_in_review_file",
                "action_type": action_type,
                "action_priority": action_priority,
                "action_status": "pending_human_review",
                "evidence_presence_matrix_path": SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_PRESENCE_MATRIX.as_posix(),
                "file_checklist_path": SOURCE_PIPELINE_PHASE_ACTION_FILE_CHECKLIST.as_posix(),
                "source_summary_path": row["source_summary_path"],
                "source_gap_summary_path": SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_GAP_SUMMARY.as_posix(),
                "route_ids": row["route_ids"],
                "result_scaffold_ids": row["result_scaffold_ids"],
                "action_ids": row["action_ids"],
                "review_status": REVIEW_STATUS,
                "rights_decision_status": "no_new_rights_decision",
                "source_promotion_status": "not_promoted",
                "corpus_import_status": "not_imported",
                "decipherment_claim_status": "no_decipherment_claim",
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
    parser.add_argument("--evidence-presence", default=str(SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_PRESENCE_MATRIX))
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parents[2]
    rows = build_missing_evidence_action_rows(read_csv_rows(root / args.evidence_presence))
    write_csv(root / args.csv_output, rows)
    print(f"source_pipeline_phase_action_missing_evidence_action_queue_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
