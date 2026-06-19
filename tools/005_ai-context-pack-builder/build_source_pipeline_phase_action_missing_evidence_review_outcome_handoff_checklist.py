#!/usr/bin/env python3
"""Build a precheck checklist for missing-evidence outcome handoffs.

The checklist gives later reviewers a per-handoff precheck surface before any
missing-evidence outcome is recorded. It does not collect evidence, assign
owners, decide rights, promote sources, import corpus rows, or make identity,
component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_SCAFFOLD = (
    STAT_DIR / "157_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-scaffold.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_CHECKLIST = (
    STAT_DIR / "153_source-pipeline-phase-action-missing-evidence-review-handoff-checklist.csv"
)
DEFAULT_OUTPUT = STAT_DIR / "158_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-checklist.csv"

UPDATED_AT = "2026-06-19"
CHECKLIST_STATUS = "not_started"
AUTOMATION_BOUNDARY = "outcome_handoff_precheck_only_no_missing_evidence_outcome_capture"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_missing_evidence_review_outcome_handoff_checklist_not_scholarship"
CAUTION = (
    "This source pipeline missing-evidence review outcome handoff checklist is a "
    "precheck surface only. It is not collected evidence, not a reviewed outcome, "
    "not a rights decision, not source promotion, not a corpus import, not an "
    "identity claim, not a component assignment, not an evolution-chain assignment, "
    "and not a decipherment conclusion."
)
REQUIRED_PRECHECK_STEPS = [
    "verify_outcome_handoff_row_against_157",
    "open_156_outcome_route_pack",
    "open_155_outcome_scaffold",
    "open_154_handoff_route_summary",
    "open_153_handoff_checklist",
    "open_all_outcome_handoff_files_before_review",
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


def outcome_handoff_files_to_open(handoff: dict[str, object]) -> str:
    paths = [
        SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_SCAFFOLD.as_posix(),
        str(handoff["route_pack_path"]),
        str(handoff["outcome_scaffold_path"]),
        str(handoff["route_summary_path"]),
        SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_CHECKLIST.as_posix(),
        str(handoff["handoff_scaffold_path"]),
        str(handoff["review_checklist_path"]),
        str(handoff["result_scaffold_path"]),
        str(handoff["review_draft_manifest_path"]),
        str(handoff["draft_path"]),
        str(handoff["source_summary_path"]),
        str(handoff["source_gap_route_summary_path"]),
    ]
    for path in handoff.get("handoff_files_to_open", []):
        if str(path) not in paths:
            paths.append(str(path))
    for path in handoff.get("files_to_open", []):
        if str(path) not in paths:
            paths.append(str(path))
    return ";".join(paths)


def row_from_handoff(index: int, handoff: dict[str, object]) -> dict[str, str]:
    return {
        "outcome_handoff_checklist_id": (
            f"source-pipeline-missing-evidence-review-outcome-handoff-checklist-{index:03d}"
        ),
        "handoff_id": str(handoff["handoff_id"]),
        "route_id": str(handoff["route_id"]),
        "missing_evidence_review_outcome_scaffold_id": str(
            handoff["missing_evidence_review_outcome_scaffold_id"]
        ),
        "summary_route_id": str(handoff["summary_route_id"]),
        "handoff_review_checklist_id": str(handoff["handoff_review_checklist_id"]),
        "review_route_id": str(handoff["review_route_id"]),
        "review_checklist_id": str(handoff["review_checklist_id"]),
        "result_scaffold_id": str(handoff["result_scaffold_id"]),
        "review_draft_id": str(handoff["review_draft_id"]),
        "source_summary_id": str(handoff["source_summary_id"]),
        "source_id": str(handoff["source_id"]),
        "source_type": str(handoff["source_type"]),
        "rights_status": str(handoff["rights_status"]),
        "pipeline_gap_status": str(handoff["pipeline_gap_status"]),
        "missing_route_count": str(handoff["missing_route_count"]),
        "missing_file_role_count": str(handoff["missing_file_role_count"]),
        "missing_file_roles": join_list(handoff["missing_file_roles"]),
        "priority_rank": str(handoff["priority_rank"]),
        "priority_tags": join_list(handoff["priority_tags"]),
        "required_review_steps": join_list(handoff["required_review_steps"]),
        "required_precheck_steps": ";".join(REQUIRED_PRECHECK_STEPS),
        "required_review_actions": join_list(handoff["required_review_actions"]),
        "blocking_condition": str(handoff["blocking_condition"]),
        "handoff_scaffold_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_SCAFFOLD.as_posix(),
        "route_pack_path": str(handoff["route_pack_path"]),
        "outcome_scaffold_path": str(handoff["outcome_scaffold_path"]),
        "outcome_update_target_path": str(handoff["outcome_update_target_path"]),
        "route_summary_path": str(handoff["route_summary_path"]),
        "previous_handoff_scaffold_path": str(handoff["handoff_scaffold_path"]),
        "review_checklist_path": str(handoff["review_checklist_path"]),
        "result_scaffold_path": str(handoff["result_scaffold_path"]),
        "result_update_target_path": str(handoff["result_update_target_path"]),
        "review_draft_manifest_path": str(handoff["review_draft_manifest_path"]),
        "draft_path": str(handoff["draft_path"]),
        "source_summary_path": str(handoff["source_summary_path"]),
        "source_gap_route_summary_path": str(handoff["source_gap_route_summary_path"]),
        "route_ids": join_list(handoff["route_ids"]),
        "missing_evidence_action_ids": join_list(handoff["missing_evidence_action_ids"]),
        "missing_evidence_result_scaffold_ids": join_list(handoff["missing_evidence_result_scaffold_ids"]),
        "evidence_presence_row_ids": join_list(handoff["evidence_presence_row_ids"]),
        "files_to_open": join_list(handoff["files_to_open"]),
        "handoff_files_to_open": join_list(handoff["handoff_files_to_open"]),
        "outcome_handoff_files_to_open": outcome_handoff_files_to_open(handoff),
        "reserved_outcome_fields": join_list(handoff["reserved_outcome_fields"]),
        "checklist_status": CHECKLIST_STATUS,
        "assignment_status": str(handoff["assignment_status"]),
        "handoff_status": str(handoff["handoff_status"]),
        "handoff_objective": str(handoff["handoff_objective"]),
        "route_status": str(handoff["route_status"]),
        "review_outcome_status": str(handoff["review_outcome_status"]),
        "evidence_collection_status": str(handoff["evidence_collection_status"]),
        "reviewed_evidence_paths": str(handoff["reviewed_evidence_paths"]),
        "reviewed_outcome_summary": str(handoff["reviewed_outcome_summary"]),
        "remaining_blockers_reviewed": str(handoff["remaining_blockers_reviewed"]),
        "required_followup_reviewed": str(handoff["required_followup_reviewed"]),
        "human_review_status": str(handoff["human_review_status"]),
        "rights_decision_status": str(handoff["rights_decision_status"]),
        "source_promotion_status": str(handoff["source_promotion_status"]),
        "corpus_import_status": str(handoff["corpus_import_status"]),
        "decipherment_claim_status": str(handoff["decipherment_claim_status"]),
        "identity_claim_status": str(handoff["identity_claim_status"]),
        "component_claim_status": str(handoff["component_claim_status"]),
        "evolution_claim_status": str(handoff["evolution_claim_status"]),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_checklist_rows(handoff_scaffold: dict[str, object]) -> list[dict[str, str]]:
    return [
        row_from_handoff(index, handoff)
        for index, handoff in enumerate(handoff_scaffold.get("handoffs", []), start=1)
        if isinstance(handoff, dict)
    ]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source pipeline outcome handoff checklist.")
    parser.add_argument(
        "--handoff-scaffold",
        default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_SCAFFOLD),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_checklist_rows(read_json(root / args.handoff_scaffold))
    write_csv(root / args.output, rows)
    print(f"missing_evidence_review_outcome_handoff_checklist_rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
