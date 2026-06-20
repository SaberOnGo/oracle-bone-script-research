#!/usr/bin/env python3
"""Build a precheck checklist for core-corpus outcome assignments.

The checklist expands the 209 assignment plan into one CSV row per planned
outcome-review assignment. It is a navigation and precheck surface only: it
does not collect evidence, record reviewed outcomes, decide rights, promote
sources or candidates, import corpus rows, or make identity, component,
evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ASSIGNMENT_PLAN = (
    STAT_DIR / "209_core-corpus-phase-gap-review-outcome-assignment-plan.json"
)
CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY = (
    STAT_DIR / "208_core-corpus-phase-gap-review-outcome-handoff-route-summary.json"
)
DEFAULT_OUTPUT = STAT_DIR / "210_core-corpus-phase-gap-review-outcome-assignment-checklist.csv"

UPDATED_AT = "2026-06-20"
CHECKLIST_STATUS = "not_started"
AUTOMATION_BOUNDARY = "assignment_checklist_only_no_core_corpus_phase_gap_outcome_capture"
RESEARCH_BOUNDARY = "core_corpus_phase_gap_review_outcome_assignment_checklist_not_scholarship"
CAUTION = (
    "This core corpus phase gap review outcome assignment checklist is a "
    "precheck surface only. It is not collected evidence, not a reviewed "
    "outcome, not a rights decision, not source or candidate promotion, not a "
    "corpus import, not an identity claim, not a component assignment, not an "
    "evolution-chain assignment, and not a decipherment conclusion."
)
REQUIRED_ASSIGNMENT_CHECK_STEPS = [
    "open_210_assignment_checklist",
    "open_209_assignment_plan",
    "open_208_outcome_handoff_route_summary",
    "open_assignment_route_files_before_review",
    "verify_assignment_item_against_209",
    "verify_empty_reviewed_evidence_and_outcome_fields",
    "confirm_no_rights_decision",
    "confirm_no_source_or_candidate_promotion",
    "confirm_no_corpus_import",
    "confirm_no_identity_component_evolution_or_decipherment_claim",
    "do_not_collect_evidence_or_record_outcome_in_checklist",
]
CHECKLIST_FIELDS = [
    "assignment_checklist_id",
    "assignment_plan_item_id",
    "assignment_wave_id",
    "summary_route_id",
    "outcome_handoff_checklist_id",
    "outcome_handoff_id",
    "outcome_route_id",
    "core_corpus_phase_gap_review_outcome_scaffold_id",
    "handoff_review_checklist_id",
    "handoff_id",
    "review_route_id",
    "review_index_id",
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
    "assignment_plan_path",
    "assignment_checklist_path",
    "route_summary_path",
    "previous_route_summary_path",
    "outcome_handoff_checklist_path",
    "outcome_handoff_scaffold_path",
    "outcome_route_pack_path",
    "outcome_scaffold_path",
    "outcome_update_target_path",
    "checklist_update_target_path",
    "handoff_review_checklist_path",
    "handoff_scaffold_path",
    "previous_route_pack_path",
    "review_index_path",
    "route_files_to_open",
    "assignment_files_to_open",
    "route_file_count",
    "required_review_steps",
    "required_precheck_steps",
    "required_assignment_check_steps",
    "reserved_outcome_fields",
    "checklist_status",
    "assignment_status",
    "handoff_readiness_status",
    "handoff_review_status",
    "handoff_status",
    "route_status",
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
    "phase_gap_outcome_reviewed",
    "specialized_checklist_outcome_reviewed",
    "reviewed_evidence_paths",
    "reviewed_outcome_summary",
    "reviewed_rights_decision",
    "reviewed_source_or_candidate_promotion",
    "reviewed_corpus_import",
    "reviewed_decipherment_claim",
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


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def join_list(value: object) -> str:
    if isinstance(value, list):
        return ";".join(str(item) for item in value if str(item))
    return str(value) if value is not None else ""


def unique_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return ";".join(seen)


def wave_id_by_item_id(plan: dict[str, object]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for wave in plan.get("assignment_waves", []):
        if not isinstance(wave, dict):
            continue
        wave_id = str(wave.get("assignment_wave_id", ""))
        for item_id in wave.get("assignment_plan_item_ids", []):
            mapping[str(item_id)] = wave_id
    return mapping


def assignment_files_to_open(item: dict[str, object]) -> str:
    return unique_join(
        [
            DEFAULT_OUTPUT.as_posix(),
            CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ASSIGNMENT_PLAN.as_posix(),
            CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY.as_posix(),
            *[str(path) for path in item.get("route_files_to_open", [])],
        ]
    )


def row_from_assignment_item(index: int, item: dict[str, object], wave_map: dict[str, str]) -> dict[str, str]:
    assignment_plan_item_id = str(item["assignment_plan_item_id"])
    return {
        "assignment_checklist_id": f"core-corpus-phase-gap-review-outcome-assignment-checklist-{index:03d}",
        "assignment_plan_item_id": assignment_plan_item_id,
        "assignment_wave_id": wave_map.get(assignment_plan_item_id, ""),
        "summary_route_id": str(item["summary_route_id"]),
        "outcome_handoff_checklist_id": str(item["outcome_handoff_checklist_id"]),
        "outcome_handoff_id": str(item["outcome_handoff_id"]),
        "outcome_route_id": str(item["outcome_route_id"]),
        "core_corpus_phase_gap_review_outcome_scaffold_id": str(
            item["core_corpus_phase_gap_review_outcome_scaffold_id"]
        ),
        "handoff_review_checklist_id": str(item["handoff_review_checklist_id"]),
        "handoff_id": str(item["handoff_id"]),
        "review_route_id": str(item["review_route_id"]),
        "review_index_id": str(item["review_index_id"]),
        "gap_queue_id": str(item["gap_queue_id"]),
        "source_phase_row_id": str(item["source_phase_row_id"]),
        "corpus_area": str(item["corpus_area"]),
        "label_en": str(item["label_en"]),
        "phase_name": str(item["phase_name"]),
        "phase_status": str(item["phase_status"]),
        "gap_type": str(item["gap_type"]),
        "review_priority": str(item["review_priority"]),
        "specialized_checklist_family": str(item["specialized_checklist_family"]),
        "specialized_checklist_id": str(item["specialized_checklist_id"]),
        "specialized_checklist_path": str(item["specialized_checklist_path"]),
        "coverage_status": str(item["coverage_status"]),
        "recommended_action": str(item["recommended_action"]),
        "candidate_or_staging_boundary": str(item["candidate_or_staging_boundary"]),
        "assignment_plan_path": CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ASSIGNMENT_PLAN.as_posix(),
        "assignment_checklist_path": DEFAULT_OUTPUT.as_posix(),
        "route_summary_path": str(item["route_summary_path"]),
        "previous_route_summary_path": str(item["previous_route_summary_path"]),
        "outcome_handoff_checklist_path": str(item["outcome_handoff_checklist_path"]),
        "outcome_handoff_scaffold_path": str(item["outcome_handoff_scaffold_path"]),
        "outcome_route_pack_path": str(item["outcome_route_pack_path"]),
        "outcome_scaffold_path": str(item["outcome_scaffold_path"]),
        "outcome_update_target_path": str(item["outcome_update_target_path"]),
        "checklist_update_target_path": str(item["checklist_update_target_path"]),
        "handoff_review_checklist_path": str(item["handoff_review_checklist_path"]),
        "handoff_scaffold_path": str(item["handoff_scaffold_path"]),
        "previous_route_pack_path": str(item["previous_route_pack_path"]),
        "review_index_path": str(item["review_index_path"]),
        "route_files_to_open": join_list(item["route_files_to_open"]),
        "assignment_files_to_open": assignment_files_to_open(item),
        "route_file_count": str(item["route_file_count"]),
        "required_review_steps": join_list(item["required_review_steps"]),
        "required_precheck_steps": join_list(item["required_precheck_steps"]),
        "required_assignment_check_steps": ";".join(REQUIRED_ASSIGNMENT_CHECK_STEPS),
        "reserved_outcome_fields": join_list(item["reserved_outcome_fields"]),
        "checklist_status": CHECKLIST_STATUS,
        "assignment_status": str(item["assignment_status"]),
        "handoff_readiness_status": str(item["handoff_readiness_status"]),
        "handoff_review_status": str(item["handoff_review_status"]),
        "handoff_status": str(item["handoff_status"]),
        "route_status": str(item["route_status"]),
        "review_outcome_status": str(item["review_outcome_status"]),
        "evidence_collection_status": str(item["evidence_collection_status"]),
        "human_review_status": str(item["human_review_status"]),
        "rights_decision_status": str(item["rights_decision_status"]),
        "source_promotion_status": str(item["source_promotion_status"]),
        "corpus_import_status": str(item["corpus_import_status"]),
        "decipherment_claim_status": str(item["decipherment_claim_status"]),
        "identity_claim_status": str(item["identity_claim_status"]),
        "component_claim_status": str(item["component_claim_status"]),
        "evolution_claim_status": str(item["evolution_claim_status"]),
        "phase_gap_outcome_reviewed": str(item["phase_gap_outcome_reviewed"]),
        "specialized_checklist_outcome_reviewed": str(item["specialized_checklist_outcome_reviewed"]),
        "reviewed_evidence_paths": str(item["reviewed_evidence_paths"]),
        "reviewed_outcome_summary": str(item["reviewed_outcome_summary"]),
        "reviewed_rights_decision": str(item["reviewed_rights_decision"]),
        "reviewed_source_or_candidate_promotion": str(item["reviewed_source_or_candidate_promotion"]),
        "reviewed_corpus_import": str(item["reviewed_corpus_import"]),
        "reviewed_decipherment_claim": str(item["reviewed_decipherment_claim"]),
        "required_followup_reviewed": str(item["required_followup_reviewed"]),
        "human_reviewer_id": str(item["human_reviewer_id"]),
        "human_review_date": str(item["human_review_date"]),
        "human_review_notes": str(item["human_review_notes"]),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_checklist_rows(plan: dict[str, object]) -> list[dict[str, str]]:
    wave_map = wave_id_by_item_id(plan)
    return [
        row_from_assignment_item(index, item, wave_map)
        for index, item in enumerate(plan.get("assignment_items", []), start=1)
        if isinstance(item, dict)
    ]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CHECKLIST_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build core corpus phase gap outcome assignment checklist.")
    parser.add_argument(
        "--assignment-plan",
        default=str(CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ASSIGNMENT_PLAN),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_checklist_rows(read_json(root / args.assignment_plan))
    write_csv(root / args.output, rows)
    print(f"core_corpus_phase_gap_review_outcome_assignment_checklist_rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
