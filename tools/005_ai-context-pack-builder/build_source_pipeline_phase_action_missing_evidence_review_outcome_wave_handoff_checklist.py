#!/usr/bin/env python3
"""Build a precheck checklist for missing-evidence outcome wave handoffs."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_SCAFFOLD = (
    STAT_DIR / "161_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-scaffold.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ASSIGNMENT_PLAN = (
    STAT_DIR / "160_source-pipeline-phase-action-missing-evidence-review-outcome-assignment-plan.json"
)
DEFAULT_OUTPUT = STAT_DIR / "162_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-checklist.csv"

UPDATED_AT = "2026-06-19"
CHECKLIST_STATUS = "not_started"
AUTOMATION_BOUNDARY = "wave_handoff_precheck_only_no_missing_evidence_outcome_capture"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_checklist_not_scholarship"
CAUTION = (
    "This source pipeline missing-evidence review outcome wave handoff checklist "
    "is a precheck surface only. It is not collected evidence, not a reviewed "
    "outcome, not a rights decision, not source promotion, not a corpus import, "
    "not an identity claim, not a component assignment, not an evolution-chain "
    "assignment, and not a decipherment conclusion."
)
REQUIRED_PRECHECK_STEPS = [
    "verify_wave_handoff_row_against_161",
    "open_160_assignment_plan",
    "open_159_handoff_route_summary",
    "open_158_handoff_checklist",
    "open_157_handoff_scaffold",
    "open_156_outcome_route_pack",
    "open_155_outcome_scaffold",
    "open_all_wave_handoff_files_before_review",
    "verify_rights_status_and_risk_note",
    "verify_empty_reviewed_outcome_fields_before_review",
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


def wave_handoff_files_to_open(item: dict[str, object]) -> str:
    paths = [
        SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_SCAFFOLD.as_posix(),
        SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ASSIGNMENT_PLAN.as_posix(),
        str(item["previous_handoff_route_summary_path"]),
        str(item["review_checklist_path"]),
        str(item["handoff_scaffold_path"]),
        str(item["route_pack_path"]),
        str(item["outcome_scaffold_path"]),
        str(item["outcome_update_target_path"]),
        str(item["route_summary_path"]),
        str(item["result_scaffold_path"]),
        str(item["review_draft_manifest_path"]),
        str(item["draft_path"]),
        str(item["source_summary_path"]),
        str(item["source_gap_route_summary_path"]),
    ]
    for path in item.get("route_files_to_open", []):
        if str(path) not in paths:
            paths.append(str(path))
    return ";".join(paths)


def row_from_handoff_item(index: int, item: dict[str, object]) -> dict[str, str]:
    return {
        "wave_handoff_checklist_id": (
            f"source-pipeline-missing-evidence-review-outcome-wave-handoff-checklist-{index:03d}"
        ),
        "handoff_item_id": str(item["handoff_item_id"]),
        "handoff_wave_id": str(item["handoff_wave_id"]),
        "assignment_wave_id": str(item["assignment_wave_id"]),
        "assignment_plan_item_id": str(item["assignment_plan_item_id"]),
        "summary_route_id": str(item["summary_route_id"]),
        "outcome_handoff_checklist_id": str(item["outcome_handoff_checklist_id"]),
        "handoff_id_from_157": str(item["handoff_id_from_157"]),
        "route_id": str(item["route_id"]),
        "missing_evidence_review_outcome_scaffold_id": str(
            item["missing_evidence_review_outcome_scaffold_id"]
        ),
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
        "required_precheck_steps": ";".join(REQUIRED_PRECHECK_STEPS),
        "required_review_actions": join_list(item["required_review_actions"]),
        "handoff_scaffold_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_SCAFFOLD.as_posix(),
        "assignment_plan_path": str(item["assignment_plan_path"]),
        "route_summary_path": str(item["route_summary_path"]),
        "previous_handoff_route_summary_path": str(item["previous_handoff_route_summary_path"]),
        "previous_handoff_scaffold_path": str(item["handoff_scaffold_path"]),
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
        "wave_handoff_files_to_open": wave_handoff_files_to_open(item),
        "reserved_outcome_fields": join_list(item["reserved_outcome_fields"]),
        "checklist_status": CHECKLIST_STATUS,
        "handoff_status": str(item["handoff_status"]),
        "assignment_status": str(item["assignment_status"]),
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


def build_checklist_rows(scaffold: dict[str, object]) -> list[dict[str, str]]:
    return [
        row_from_handoff_item(index, item)
        for index, item in enumerate(scaffold.get("handoff_items", []), start=1)
        if isinstance(item, dict)
    ]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build missing-evidence outcome wave handoff checklist.")
    parser.add_argument(
        "--handoff-scaffold",
        default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_SCAFFOLD),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_checklist_rows(read_json(root / args.handoff_scaffold))
    write_csv(root / args.output, rows)
    print(f"missing_evidence_outcome_wave_handoff_checklist_rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
