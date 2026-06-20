#!/usr/bin/env python3
"""Build an empty outcome scaffold for core-corpus outcome assignments.

The scaffold gives each 210 assignment checklist row a human-fillable outcome
row. It does not collect evidence, record reviewed outcomes, decide rights,
promote sources or candidates, import corpus rows, or make identity,
component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ASSIGNMENT_PLAN = (
    STAT_DIR / "209_core-corpus-phase-gap-review-outcome-assignment-plan.json"
)
CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ASSIGNMENT_CHECKLIST = (
    STAT_DIR / "210_core-corpus-phase-gap-review-outcome-assignment-checklist.csv"
)
DEFAULT_OUTPUT = STAT_DIR / "211_core-corpus-phase-gap-review-outcome-assignment-outcome-scaffold.csv"

UPDATED_AT = "2026-06-20"
ASSIGNMENT_OUTCOME_STATUS = "not_started"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
COMPONENT_CLAIM_STATUS = "no_component_claim"
EVOLUTION_CLAIM_STATUS = "no_evolution_chain_claim"
AUTOMATION_BOUNDARY = "assignment_outcome_scaffold_only_no_core_corpus_phase_gap_outcome_capture"
RESEARCH_BOUNDARY = "core_corpus_phase_gap_review_outcome_assignment_outcome_scaffold_not_scholarship"
RESERVED_OUTCOME_FIELDS = ";".join(
    [
        "assignment_precheck_reviewed",
        "phase_gap_outcome_reviewed",
        "specialized_checklist_outcome_reviewed",
        "reviewed_evidence_paths",
        "reviewed_outcome_summary",
        "reviewed_rights_decision",
        "reviewed_source_or_candidate_promotion",
        "reviewed_corpus_import",
        "reviewed_decipherment_claim",
        "remaining_blockers_reviewed",
        "required_followup_reviewed",
        "human_reviewer_id",
        "human_review_date",
        "human_review_notes",
    ]
)
REQUIRED_OUTCOME_STEPS = [
    "open_211_assignment_outcome_scaffold",
    "open_210_assignment_checklist",
    "open_209_assignment_plan",
    "open_208_outcome_handoff_route_summary",
    "open_assignment_route_files_before_review",
    "verify_assignment_checklist_row_is_not_started",
    "verify_empty_reviewed_evidence_and_outcome_fields",
    "record_only_human_gated_outcome_after_source_review",
    "confirm_no_rights_decision_until_reviewed",
    "confirm_no_source_or_candidate_promotion_until_reviewed",
    "confirm_no_corpus_import_until_reviewed",
    "confirm_no_identity_component_evolution_or_decipherment_claim",
]
CAUTION = (
    "This core corpus phase gap review assignment outcome scaffold is empty and "
    "human-fillable only. It is not collected evidence, not a reviewed outcome, "
    "not a rights decision, not source or candidate promotion, not a corpus "
    "import, not an identity claim, not a component assignment, not an "
    "evolution-chain assignment, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "assignment_outcome_scaffold_id",
    "assignment_checklist_id",
    "assignment_plan_item_id",
    "assignment_wave_id",
    "summary_route_id",
    "gap_queue_id",
    "source_phase_row_id",
    "corpus_area",
    "label_en",
    "phase_name",
    "phase_status",
    "gap_type",
    "review_priority",
    "specialized_checklist_family",
    "specialized_checklist_id",
    "specialized_checklist_path",
    "coverage_status",
    "recommended_action",
    "candidate_or_staging_boundary",
    "assignment_outcome_scaffold_path",
    "assignment_checklist_path",
    "assignment_plan_path",
    "route_summary_path",
    "previous_route_summary_path",
    "outcome_handoff_checklist_path",
    "outcome_handoff_scaffold_path",
    "outcome_route_pack_path",
    "outcome_scaffold_path",
    "outcome_update_target_path",
    "checklist_update_target_path",
    "route_files_to_open",
    "assignment_files_to_open",
    "outcome_files_to_open",
    "route_file_count",
    "required_review_steps",
    "required_precheck_steps",
    "required_assignment_check_steps",
    "required_outcome_steps",
    "reserved_outcome_fields",
    "checklist_status",
    "assignment_status",
    "handoff_readiness_status",
    "handoff_review_status",
    "handoff_status",
    "route_status",
    "assignment_outcome_status",
    "review_outcome_status",
    "evidence_collection_status",
    "human_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "identity_claim_status",
    "component_claim_status",
    "evolution_claim_status",
    "assignment_precheck_reviewed",
    "phase_gap_outcome_reviewed",
    "specialized_checklist_outcome_reviewed",
    "reviewed_evidence_paths",
    "reviewed_outcome_summary",
    "reviewed_rights_decision",
    "reviewed_source_or_candidate_promotion",
    "reviewed_corpus_import",
    "reviewed_decipherment_claim",
    "remaining_blockers_reviewed",
    "required_followup_reviewed",
    "human_reviewer_id",
    "human_review_date",
    "human_review_notes",
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


def unique_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return ";".join(seen)


def outcome_files_to_open(row: dict[str, str]) -> str:
    return unique_join(
        [
            DEFAULT_OUTPUT.as_posix(),
            CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ASSIGNMENT_CHECKLIST.as_posix(),
            CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ASSIGNMENT_PLAN.as_posix(),
            row.get("route_summary_path", ""),
            *row.get("assignment_files_to_open", "").split(";"),
        ]
    )


def row_from_assignment_checklist(index: int, row: dict[str, str]) -> dict[str, str]:
    return {
        "assignment_outcome_scaffold_id": (
            f"core-corpus-phase-gap-review-outcome-assignment-outcome-scaffold-{index:03d}"
        ),
        "assignment_checklist_id": row["assignment_checklist_id"],
        "assignment_plan_item_id": row["assignment_plan_item_id"],
        "assignment_wave_id": row["assignment_wave_id"],
        "summary_route_id": row["summary_route_id"],
        "gap_queue_id": row["gap_queue_id"],
        "source_phase_row_id": row["source_phase_row_id"],
        "corpus_area": row["corpus_area"],
        "label_en": row["label_en"],
        "phase_name": row["phase_name"],
        "phase_status": row["phase_status"],
        "gap_type": row["gap_type"],
        "review_priority": row["review_priority"],
        "specialized_checklist_family": row["specialized_checklist_family"],
        "specialized_checklist_id": row["specialized_checklist_id"],
        "specialized_checklist_path": row["specialized_checklist_path"],
        "coverage_status": row["coverage_status"],
        "recommended_action": row["recommended_action"],
        "candidate_or_staging_boundary": row["candidate_or_staging_boundary"],
        "assignment_outcome_scaffold_path": DEFAULT_OUTPUT.as_posix(),
        "assignment_checklist_path": row["assignment_checklist_path"],
        "assignment_plan_path": row["assignment_plan_path"],
        "route_summary_path": row["route_summary_path"],
        "previous_route_summary_path": row["previous_route_summary_path"],
        "outcome_handoff_checklist_path": row["outcome_handoff_checklist_path"],
        "outcome_handoff_scaffold_path": row["outcome_handoff_scaffold_path"],
        "outcome_route_pack_path": row["outcome_route_pack_path"],
        "outcome_scaffold_path": row["outcome_scaffold_path"],
        "outcome_update_target_path": row["outcome_update_target_path"],
        "checklist_update_target_path": row["checklist_update_target_path"],
        "route_files_to_open": row["route_files_to_open"],
        "assignment_files_to_open": row["assignment_files_to_open"],
        "outcome_files_to_open": outcome_files_to_open(row),
        "route_file_count": row["route_file_count"],
        "required_review_steps": row["required_review_steps"],
        "required_precheck_steps": row["required_precheck_steps"],
        "required_assignment_check_steps": row["required_assignment_check_steps"],
        "required_outcome_steps": ";".join(REQUIRED_OUTCOME_STEPS),
        "reserved_outcome_fields": RESERVED_OUTCOME_FIELDS,
        "checklist_status": row["checklist_status"],
        "assignment_status": row["assignment_status"],
        "handoff_readiness_status": row["handoff_readiness_status"],
        "handoff_review_status": row["handoff_review_status"],
        "handoff_status": row["handoff_status"],
        "route_status": row["route_status"],
        "assignment_outcome_status": ASSIGNMENT_OUTCOME_STATUS,
        "review_outcome_status": row["review_outcome_status"],
        "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
        "human_review_status": HUMAN_REVIEW_STATUS,
        "rights_decision_status": RIGHTS_DECISION_STATUS,
        "source_promotion_status": SOURCE_PROMOTION_STATUS,
        "corpus_import_status": CORPUS_IMPORT_STATUS,
        "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
        "identity_claim_status": IDENTITY_CLAIM_STATUS,
        "component_claim_status": COMPONENT_CLAIM_STATUS,
        "evolution_claim_status": EVOLUTION_CLAIM_STATUS,
        "assignment_precheck_reviewed": "",
        "phase_gap_outcome_reviewed": "",
        "specialized_checklist_outcome_reviewed": "",
        "reviewed_evidence_paths": "",
        "reviewed_outcome_summary": "",
        "reviewed_rights_decision": "",
        "reviewed_source_or_candidate_promotion": "",
        "reviewed_corpus_import": "",
        "reviewed_decipherment_claim": "",
        "remaining_blockers_reviewed": "",
        "required_followup_reviewed": "",
        "human_reviewer_id": "",
        "human_review_date": "",
        "human_review_notes": "",
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_outcome_scaffold_rows(checklist_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row_from_assignment_checklist(index, row) for index, row in enumerate(checklist_rows, start=1)]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build core corpus phase gap assignment outcome scaffold.")
    parser.add_argument(
        "--assignment-checklist",
        default=str(CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ASSIGNMENT_CHECKLIST),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_outcome_scaffold_rows(read_csv_rows(root / args.assignment_checklist))
    write_csv(root / args.output, rows)
    print(f"core_corpus_phase_gap_review_outcome_assignment_outcome_scaffold_rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
