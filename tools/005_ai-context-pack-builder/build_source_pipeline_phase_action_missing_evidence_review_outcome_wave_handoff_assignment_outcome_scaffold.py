#!/usr/bin/env python3
"""Build empty outcome scaffold rows for missing-evidence handoff assignments."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/"
    "165_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-checklist.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "166_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-scaffold.csv"
)

UPDATED_AT = "2026-06-19"
ASSIGNMENT_REVIEW_STATUS = "not_started"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
COMPONENT_CLAIM_STATUS = "no_component_claim"
EVOLUTION_CLAIM_STATUS = "no_evolution_chain_claim"
AUTOMATION_BOUNDARY = "assignment_outcome_scaffold_only_human_gated_no_evidence_capture"
RESEARCH_BOUNDARY = (
    "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_scaffold_not_scholarship"
)
RESERVED_OUTCOME_FIELDS = ";".join(
    [
        "source_metadata_outcome_reviewed",
        "access_boundary_outcome_reviewed",
        "download_or_access_outcome_reviewed",
        "large_source_register_outcome_reviewed",
        "field_map_outcome_reviewed",
        "package_manifest_outcome_reviewed",
        "safe_derived_record_outcome_reviewed",
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
    "This source pipeline missing-evidence assignment file is a human-gated outcome scaffold. "
    "It is not collected evidence, not a reviewed outcome, not a rights decision, "
    "not source promotion, not a corpus import, not an identity claim, not a "
    "component assignment, not an evolution-chain assignment, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "assignment_outcome_scaffold_id",
    "assignment_review_checklist_id",
    "assignment_plan_item_id",
    "summary_route_id",
    "wave_handoff_checklist_id",
    "handoff_item_id",
    "handoff_wave_id",
    "assignment_wave_id",
    "assignment_plan_item_id_from_160",
    "outcome_handoff_checklist_id",
    "handoff_id_from_157",
    "route_id",
    "missing_evidence_review_outcome_scaffold_id",
    "source_id",
    "source_type",
    "rights_status",
    "pipeline_gap_status",
    "missing_route_count",
    "missing_file_role_count",
    "missing_file_roles",
    "priority_rank",
    "priority_tags",
    "required_review_steps",
    "required_precheck_steps",
    "required_review_actions",
    "required_assignment_check_steps",
    "assignment_checklist_path",
    "route_summary_path",
    "wave_handoff_checklist_path",
    "handoff_scaffold_path",
    "assignment_plan_path",
    "previous_route_summary_path",
    "previous_handoff_route_summary_path",
    "previous_handoff_scaffold_path",
    "route_pack_path",
    "outcome_scaffold_path",
    "outcome_update_target_path",
    "review_checklist_path",
    "result_scaffold_path",
    "result_update_target_path",
    "review_draft_manifest_path",
    "draft_path",
    "source_summary_path",
    "source_gap_route_summary_path",
    "route_files_to_open",
    "assignment_files_to_open",
    "reserved_outcome_fields",
    "checklist_status",
    "assignment_status",
    "handoff_status",
    "handoff_readiness_status",
    "source_checklist_status",
    "route_status",
    "assignment_review_status",
    "review_outcome_status",
    "evidence_collection_status",
    "source_metadata_outcome_reviewed",
    "access_boundary_outcome_reviewed",
    "download_or_access_outcome_reviewed",
    "large_source_register_outcome_reviewed",
    "field_map_outcome_reviewed",
    "package_manifest_outcome_reviewed",
    "safe_derived_record_outcome_reviewed",
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
    "identity_claim_status",
    "component_claim_status",
    "evolution_claim_status",
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


def build_outcome_scaffold_rows(checklist_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(checklist_rows, start=1):
        rows.append(
            {
                "assignment_outcome_scaffold_id": (
                    "source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-outcome-scaffold-"
                    f"{index:03d}"
                ),
                "assignment_review_checklist_id": row["assignment_review_checklist_id"],
                "assignment_plan_item_id": row["assignment_plan_item_id"],
                "summary_route_id": row["summary_route_id"],
                "wave_handoff_checklist_id": row["wave_handoff_checklist_id"],
                "handoff_item_id": row["handoff_item_id"],
                "handoff_wave_id": row["handoff_wave_id"],
                "assignment_wave_id": row["assignment_wave_id"],
                "assignment_plan_item_id_from_160": row["assignment_plan_item_id_from_160"],
                "outcome_handoff_checklist_id": row["outcome_handoff_checklist_id"],
                "handoff_id_from_157": row["handoff_id_from_157"],
                "route_id": row["route_id"],
                "missing_evidence_review_outcome_scaffold_id": row["missing_evidence_review_outcome_scaffold_id"],
                "source_id": row["source_id"],
                "source_type": row["source_type"],
                "rights_status": row["rights_status"],
                "pipeline_gap_status": row["pipeline_gap_status"],
                "missing_route_count": row["missing_route_count"],
                "missing_file_role_count": row["missing_file_role_count"],
                "missing_file_roles": row["missing_file_roles"],
                "priority_rank": row["priority_rank"],
                "priority_tags": row["priority_tags"],
                "required_review_steps": row["required_review_steps"],
                "required_precheck_steps": row["required_precheck_steps"],
                "required_review_actions": row["required_review_actions"],
                "required_assignment_check_steps": row["required_assignment_check_steps"],
                "assignment_checklist_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_CHECKLIST.as_posix(),
                "route_summary_path": row["route_summary_path"],
                "wave_handoff_checklist_path": row["wave_handoff_checklist_path"],
                "handoff_scaffold_path": row["handoff_scaffold_path"],
                "assignment_plan_path": row["assignment_plan_path"],
                "previous_route_summary_path": row["previous_route_summary_path"],
                "previous_handoff_route_summary_path": row["previous_handoff_route_summary_path"],
                "previous_handoff_scaffold_path": row["previous_handoff_scaffold_path"],
                "route_pack_path": row["route_pack_path"],
                "outcome_scaffold_path": row["outcome_scaffold_path"],
                "outcome_update_target_path": row["outcome_update_target_path"],
                "review_checklist_path": row["review_checklist_path"],
                "result_scaffold_path": row["result_scaffold_path"],
                "result_update_target_path": row["result_update_target_path"],
                "review_draft_manifest_path": row["review_draft_manifest_path"],
                "draft_path": row["draft_path"],
                "source_summary_path": row["source_summary_path"],
                "source_gap_route_summary_path": row["source_gap_route_summary_path"],
                "route_files_to_open": row["route_files_to_open"],
                "assignment_files_to_open": row["assignment_files_to_open"],
                "reserved_outcome_fields": RESERVED_OUTCOME_FIELDS,
                "checklist_status": row["checklist_status"],
                "assignment_status": row["assignment_status"],
                "handoff_status": row["handoff_status"],
                "handoff_readiness_status": row["handoff_readiness_status"],
                "source_checklist_status": row["source_checklist_status"],
                "route_status": row["route_status"],
                "assignment_review_status": ASSIGNMENT_REVIEW_STATUS,
                "review_outcome_status": row["review_outcome_status"],
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "source_metadata_outcome_reviewed": "",
                "access_boundary_outcome_reviewed": "",
                "download_or_access_outcome_reviewed": "",
                "large_source_register_outcome_reviewed": "",
                "field_map_outcome_reviewed": "",
                "package_manifest_outcome_reviewed": "",
                "safe_derived_record_outcome_reviewed": "",
                "reviewed_evidence_paths": "",
                "reviewed_outcome_summary": "",
                "remaining_blockers_reviewed": "",
                "required_followup_reviewed": "",
                "human_reviewer_id": "",
                "human_review_date": "",
                "human_review_notes": "",
                "human_review_status": HUMAN_REVIEW_STATUS,
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "corpus_import_status": CORPUS_IMPORT_STATUS,
                "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "component_claim_status": COMPONENT_CLAIM_STATUS,
                "evolution_claim_status": EVOLUTION_CLAIM_STATUS,
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
    parser = argparse.ArgumentParser(description="Build missing-evidence assignment outcome scaffold.")
    parser.add_argument(
        "--checklist",
        default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_CHECKLIST),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_outcome_scaffold_rows(read_csv_rows(root / args.checklist))
    write_csv(root / args.output, rows)
    print(f"missing_evidence_assignment_outcome_scaffold_rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
