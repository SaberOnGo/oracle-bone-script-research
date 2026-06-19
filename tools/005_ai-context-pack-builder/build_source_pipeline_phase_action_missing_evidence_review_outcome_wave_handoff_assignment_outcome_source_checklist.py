#!/usr/bin/env python3
"""Build human-gated source checklists for assignment outcome source summaries."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_SUMMARY = (
    Path("corpus/009_statistics-and-derived-features")
    / "168_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-summary.csv"
)
DEFAULT_OUTPUT = (
    Path("corpus/009_statistics-and-derived-features")
    / "169_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-checklist.csv"
)

UPDATED_AT = "2026-06-19"
SOURCE_REVIEW_STATUS = "needs_assignment_outcome_source_review"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
COMPONENT_CLAIM_STATUS = "no_component_claim"
EVOLUTION_CLAIM_STATUS = "no_evolution_chain_claim"
AUTOMATION_BOUNDARY = "human_gated_assignment_outcome_source_checklist_only"
RESEARCH_BOUNDARY = (
    "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_checklist_not_scholarship"
)
CAUTION = (
    "This source pipeline missing-evidence assignment outcome source checklist is a "
    "human-gated review route only. It is not collected evidence, not a reviewed "
    "outcome, not a rights decision, not source promotion, not a corpus import, "
    "not an identity claim, not a component assignment, not an evolution-chain "
    "assignment, and not a decipherment conclusion."
)

COMMON_SOURCE_REVIEW_STEPS = [
    "open_assignment_outcome_source_summary",
    "open_assignment_outcome_route_summary",
    "open_assignment_outcome_routes_for_source",
    "open_all_source_files_to_open",
    "verify_rights_status_and_risk_note",
    "record_only_human_reviewed_source_outcomes",
    "leave_unreviewed_outcome_fields_empty",
    "do_not_import_or_promote_until_reviewed",
    "do_not_write_ai_hypothesis_as_scholarship",
]
ROLE_REVIEW_STEPS = {
    "downloaded_metadata_profile": "verify_downloaded_metadata_profile_or_not_applicable_boundary",
    "large_source_register": "verify_large_source_register_applicability",
    "source_field_map": "verify_source_field_map_or_create_reviewed_row",
    "source_package_file_manifest": "verify_package_manifest_or_not_applicable_boundary",
}

OUTPUT_FIELDS = [
    "assignment_outcome_source_checklist_id",
    "assignment_outcome_source_summary_id",
    "source_id",
    "source_type",
    "rights_status",
    "pipeline_gap_status",
    "assignment_outcome_route_count",
    "handoff_wave_ids",
    "assignment_wave_ids",
    "assignment_plan_item_ids",
    "assignment_review_checklist_ids",
    "assignment_outcome_scaffold_ids",
    "assignment_outcome_route_ids",
    "missing_file_role_count",
    "missing_file_roles",
    "priority_tags",
    "required_source_review_steps",
    "blocking_condition",
    "source_files_to_open",
    "draft_paths",
    "source_summary_path",
    "assignment_outcome_route_summary_path",
    "source_review_status",
    "assignment_review_status_counts",
    "review_outcome_status_counts",
    "evidence_collection_status_counts",
    "human_review_status_counts",
    "evidence_collection_status",
    "human_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "identity_claim_status",
    "component_claim_status",
    "evolution_claim_status",
    "reviewed_evidence_paths",
    "reviewed_outcome_summary",
    "automation_boundary",
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


def unique_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return ";".join(seen)


def required_source_review_steps(row: dict[str, str]) -> str:
    steps = list(COMMON_SOURCE_REVIEW_STEPS)
    for role in split_semicolon(row["missing_file_roles"]):
        step = ROLE_REVIEW_STEPS.get(role)
        if step:
            steps.append(step)
    return ";".join(dict.fromkeys(steps))


def build_source_checklist_rows(source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(source_rows, start=1):
        rows.append(
            {
                "assignment_outcome_source_checklist_id": (
                    "source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-checklist-"
                    f"{index:03d}"
                ),
                "assignment_outcome_source_summary_id": row["assignment_outcome_source_summary_id"],
                "source_id": row["source_id"],
                "source_type": row["source_type"],
                "rights_status": row["rights_status"],
                "pipeline_gap_status": row["pipeline_gap_status"],
                "assignment_outcome_route_count": row["assignment_outcome_route_count"],
                "handoff_wave_ids": row["handoff_wave_ids"],
                "assignment_wave_ids": row["assignment_wave_ids"],
                "assignment_plan_item_ids": row["assignment_plan_item_ids"],
                "assignment_review_checklist_ids": row["assignment_review_checklist_ids"],
                "assignment_outcome_scaffold_ids": row["assignment_outcome_scaffold_ids"],
                "assignment_outcome_route_ids": row["assignment_outcome_route_ids"],
                "missing_file_role_count": row["missing_file_role_count"],
                "missing_file_roles": row["missing_file_roles"],
                "priority_tags": row["priority_tags"],
                "required_source_review_steps": required_source_review_steps(row),
                "blocking_condition": "open_all_routed_source_files_before_recording_assignment_outcome_source_review",
                "source_files_to_open": unique_join(
                    [*split_semicolon(row["assignment_files_to_open"]), *split_semicolon(row["draft_paths"])]
                ),
                "draft_paths": row["draft_paths"],
                "source_summary_path": (
                    SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_SUMMARY.as_posix()
                ),
                "assignment_outcome_route_summary_path": row["assignment_outcome_route_summary_path"],
                "source_review_status": SOURCE_REVIEW_STATUS,
                "assignment_review_status_counts": row["assignment_review_status_counts"],
                "review_outcome_status_counts": row["review_outcome_status_counts"],
                "evidence_collection_status_counts": row["evidence_collection_status_counts"],
                "human_review_status_counts": row["human_review_status_counts"],
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "human_review_status": HUMAN_REVIEW_STATUS,
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "corpus_import_status": CORPUS_IMPORT_STATUS,
                "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "component_claim_status": COMPONENT_CLAIM_STATUS,
                "evolution_claim_status": EVOLUTION_CLAIM_STATUS,
                "reviewed_evidence_paths": "",
                "reviewed_outcome_summary": "",
                "automation_boundary": AUTOMATION_BOUNDARY,
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
    parser = argparse.ArgumentParser(description="Build assignment outcome source checklist.")
    parser.add_argument(
        "--source-summary",
        default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_SUMMARY),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_source_checklist_rows(read_csv_rows(root / args.source_summary))
    write_csv(root / args.output, rows)
    print(f"missing_evidence_assignment_outcome_source_checklist_rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
