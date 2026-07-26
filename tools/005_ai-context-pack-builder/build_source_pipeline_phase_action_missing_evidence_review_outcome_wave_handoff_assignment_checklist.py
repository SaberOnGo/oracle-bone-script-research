#!/usr/bin/env python3
"""Build a precheck checklist for missing-evidence outcome handoff assignments."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_PLAN = (
    STAT_DIR / "164_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-plan.json"
)
DEFAULT_OUTPUT = STAT_DIR / "165_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-checklist.csv"

UPDATED_AT = "2026-06-19"
CHECKLIST_STATUS = "not_started"
AUTOMATION_BOUNDARY = "assignment_checklist_only_no_missing_evidence_outcome_capture"
RESEARCH_BOUNDARY = (
    "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_checklist_not_scholarship"
)
CAUTION = (
    "This source pipeline missing-evidence review outcome wave handoff assignment "
    "checklist is a precheck surface only. It is not collected evidence, not a "
    "reviewed outcome, not a rights decision, not source promotion, not a corpus "
    "import, not an identity claim, not a component assignment, not an "
    "evolution-chain assignment, and not a decipherment conclusion."
)
REQUIRED_ASSIGNMENT_CHECK_STEPS = [
    "verify_assignment_item_against_164",
    "open_163_route_summary",
    "open_162_wave_handoff_checklist",
    "open_161_wave_handoff_scaffold",
    "open_160_assignment_plan",
    "open_all_assignment_files_before_review",
    "verify_empty_reviewed_evidence_and_outcome_fields",
    "verify_rights_status_and_risk_note",
    "do_not_collect_evidence_or_record_outcome_in_checklist",
    "keep_source_promotion_and_corpus_import_blocked",
    "do_not_write_ai_hypothesis_as_scholarship",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def join_list(value: object) -> str:
    if isinstance(value, list):
        return ";".join(str(item) for item in value)
    return str(value)


def assignment_files_to_open(item: dict[str, object]) -> str:
    paths = [
        SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_PLAN.as_posix(),
        str(item["route_summary_path"]),
        str(item["wave_handoff_checklist_path"]),
        str(item["handoff_scaffold_path"]),
        str(item["assignment_plan_path"]),
        str(item["previous_route_summary_path"]),
        str(item["previous_handoff_route_summary_path"]),
        str(item["previous_handoff_scaffold_path"]),
        str(item["route_pack_path"]),
        str(item["outcome_scaffold_path"]),
        str(item["outcome_update_target_path"]),
        str(item["review_checklist_path"]),
        str(item["result_scaffold_path"]),
        str(item["result_update_target_path"]),
        str(item["review_draft_manifest_path"]),
        str(item["draft_path"]),
        str(item["source_summary_path"]),
        str(item["source_gap_route_summary_path"]),
    ]
    for path in item.get("route_files_to_open", []):
        text = str(path)
        if text not in paths:
            paths.append(text)
    return ";".join(paths)


def row_from_assignment_item(index: int, item: dict[str, object]) -> dict[str, str]:
    return {
        "assignment_review_checklist_id": (
            "source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-checklist-"
            f"{index:03d}"
        ),
        "assignment_plan_item_id": str(item["assignment_plan_item_id"]),
        "summary_route_id": str(item["summary_route_id"]),
        "wave_handoff_checklist_id": str(item["wave_handoff_checklist_id"]),
        "handoff_item_id": str(item["handoff_item_id"]),
        "handoff_wave_id": str(item["handoff_wave_id"]),
        "assignment_wave_id": str(item["assignment_wave_id"]),
        "assignment_plan_item_id_from_160": str(item["assignment_plan_item_id_from_160"]),
        "outcome_handoff_checklist_id": str(item["outcome_handoff_checklist_id"]),
        "handoff_id_from_157": str(item["handoff_id_from_157"]),
        "route_id": str(item["route_id"]),
        "missing_evidence_review_outcome_scaffold_id": str(item["missing_evidence_review_outcome_scaffold_id"]),
        "source_id": str(item["source_id"]),
        "source_type": str(item["source_type"]),
        "rights_status": str(item["rights_status"]),
        "pipeline_gap_status": str(item["pipeline_gap_status"]),
        "missing_route_count": str(item["missing_route_count"]),
        "missing_file_role_count": str(item["missing_file_role_count"]),
        "missing_file_roles": join_list(item["missing_file_roles"]),
        "priority_rank": str(item["priority_rank"]),
        "priority_tags": join_list(item["priority_tags"]),
        "required_review_steps": join_list(item["required_review_steps"]),
        "required_precheck_steps": join_list(item["required_precheck_steps"]),
        "required_review_actions": join_list(item["required_review_actions"]),
        "required_assignment_check_steps": ";".join(REQUIRED_ASSIGNMENT_CHECK_STEPS),
        "route_summary_path": str(item["route_summary_path"]),
        "wave_handoff_checklist_path": str(item["wave_handoff_checklist_path"]),
        "handoff_scaffold_path": str(item["handoff_scaffold_path"]),
        "assignment_plan_path": str(item["assignment_plan_path"]),
        "previous_route_summary_path": str(item["previous_route_summary_path"]),
        "previous_handoff_route_summary_path": str(item["previous_handoff_route_summary_path"]),
        "previous_handoff_scaffold_path": str(item["previous_handoff_scaffold_path"]),
        "route_pack_path": str(item["route_pack_path"]),
        "outcome_scaffold_path": str(item["outcome_scaffold_path"]),
        "outcome_update_target_path": str(item["outcome_update_target_path"]),
        "review_checklist_path": str(item["review_checklist_path"]),
        "result_scaffold_path": str(item["result_scaffold_path"]),
        "result_update_target_path": str(item["result_update_target_path"]),
        "review_draft_manifest_path": str(item["review_draft_manifest_path"]),
        "draft_path": str(item["draft_path"]),
        "source_summary_path": str(item["source_summary_path"]),
        "source_gap_route_summary_path": str(item["source_gap_route_summary_path"]),
        "route_files_to_open": join_list(item["route_files_to_open"]),
        "route_file_count": str(item["route_file_count"]),
        "assignment_files_to_open": assignment_files_to_open(item),
        "reserved_outcome_fields": join_list(item["reserved_outcome_fields"]),
        "checklist_status": CHECKLIST_STATUS,
        "assignment_status": str(item["assignment_status"]),
        "handoff_status": str(item["handoff_status"]),
        "handoff_readiness_status": str(item["handoff_readiness_status"]),
        "source_checklist_status": str(item["checklist_status"]),
        "route_status": str(item["route_status"]),
        "review_outcome_status": str(item["review_outcome_status"]),
        "evidence_collection_status": str(item["evidence_collection_status"]),
        "reviewed_evidence_paths": str(item["reviewed_evidence_paths"]),
        "reviewed_outcome_summary": str(item["reviewed_outcome_summary"]),
        "remaining_blockers_reviewed": str(item["remaining_blockers_reviewed"]),
        "required_followup_reviewed": str(item["required_followup_reviewed"]),
        "human_review_status": str(item["human_review_status"]),
        "rights_decision_status": str(item["rights_decision_status"]),
        "source_promotion_status": str(item["source_promotion_status"]),
        "corpus_import_status": str(item["corpus_import_status"]),
        "decipherment_claim_status": str(item["decipherment_claim_status"]),
        "identity_claim_status": str(item["identity_claim_status"]),
        "component_claim_status": str(item["component_claim_status"]),
        "evolution_claim_status": str(item["evolution_claim_status"]),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_checklist_rows(plan: dict[str, object]) -> list[dict[str, str]]:
    return [
        row_from_assignment_item(index, item)
        for index, item in enumerate(plan.get("assignment_items", []), start=1)
        if isinstance(item, dict)
    ]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        fieldnames = list(rows[0]) if rows else list(row_from_assignment_item(0, defaultdict(str)))
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build missing-evidence outcome handoff assignment checklist.")
    parser.add_argument(
        "--assignment-plan",
        default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_PLAN),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_checklist_rows(read_json(root / args.assignment_plan))
    write_csv(root / args.output, rows)
    print(f"missing_evidence_outcome_assignment_checklist_rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
