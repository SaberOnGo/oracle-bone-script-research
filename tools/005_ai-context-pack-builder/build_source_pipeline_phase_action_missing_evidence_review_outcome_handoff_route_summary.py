#!/usr/bin/env python3
"""Build a route summary for missing-evidence outcome handoff checklists.

The summary indexes the 158 checklist rows by source and pipeline gap for later
human review. It does not collect evidence, record outcomes, decide rights,
promote sources, import corpus rows, or make identity, component, evolution, or
decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_CHECKLIST = (
    STAT_DIR / "158_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-checklist.csv"
)
DEFAULT_OUTPUT = STAT_DIR / "159_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-route-summary.json"

UPDATED_AT = "2026-06-19"
AUTOMATION_BOUNDARY = "route_summary_only_no_missing_evidence_outcome_capture"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_missing_evidence_review_outcome_handoff_route_summary_not_scholarship"
CAUTION = (
    "This source pipeline missing-evidence outcome handoff route summary is routing-only. "
    "It is not collected evidence, not a reviewed outcome, not a rights decision, "
    "not source promotion, not a corpus import, not an identity claim, not a "
    "component assignment, not an evolution-chain assignment, and not a "
    "decipherment conclusion."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_semicolon(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def route_from_row(index: int, row: dict[str, str]) -> dict[str, object]:
    return {
        "summary_route_id": f"source-pipeline-missing-evidence-review-outcome-handoff-summary-route-{index:03d}",
        "outcome_handoff_checklist_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_CHECKLIST.as_posix(),
        "outcome_handoff_checklist_id": row["outcome_handoff_checklist_id"],
        "handoff_id": row["handoff_id"],
        "route_id": row["route_id"],
        "missing_evidence_review_outcome_scaffold_id": row["missing_evidence_review_outcome_scaffold_id"],
        "summary_route_id_from_154": row["summary_route_id"],
        "handoff_review_checklist_id": row["handoff_review_checklist_id"],
        "review_route_id": row["review_route_id"],
        "review_checklist_id": row["review_checklist_id"],
        "result_scaffold_id": row["result_scaffold_id"],
        "review_draft_id": row["review_draft_id"],
        "source_summary_id": row["source_summary_id"],
        "source_id": row["source_id"],
        "source_type": row["source_type"],
        "rights_status": row["rights_status"],
        "pipeline_gap_status": row["pipeline_gap_status"],
        "missing_route_count": row["missing_route_count"],
        "missing_file_role_count": row["missing_file_role_count"],
        "missing_file_roles": split_semicolon(row["missing_file_roles"]),
        "priority_rank": row["priority_rank"],
        "priority_tags": split_semicolon(row["priority_tags"]),
        "required_review_steps": split_semicolon(row["required_review_steps"]),
        "required_precheck_steps": split_semicolon(row["required_precheck_steps"]),
        "required_review_actions": split_semicolon(row["required_review_actions"]),
        "blocking_condition": row["blocking_condition"],
        "handoff_scaffold_path": row["handoff_scaffold_path"],
        "route_pack_path": row["route_pack_path"],
        "outcome_scaffold_path": row["outcome_scaffold_path"],
        "outcome_update_target_path": row["outcome_update_target_path"],
        "route_summary_path": row["route_summary_path"],
        "previous_handoff_scaffold_path": row["previous_handoff_scaffold_path"],
        "review_checklist_path": row["review_checklist_path"],
        "result_scaffold_path": row["result_scaffold_path"],
        "result_update_target_path": row["result_update_target_path"],
        "review_draft_manifest_path": row["review_draft_manifest_path"],
        "draft_path": row["draft_path"],
        "source_summary_path": row["source_summary_path"],
        "source_gap_route_summary_path": row["source_gap_route_summary_path"],
        "route_ids": split_semicolon(row["route_ids"]),
        "missing_evidence_action_ids": split_semicolon(row["missing_evidence_action_ids"]),
        "missing_evidence_result_scaffold_ids": split_semicolon(row["missing_evidence_result_scaffold_ids"]),
        "evidence_presence_row_ids": split_semicolon(row["evidence_presence_row_ids"]),
        "files_to_open": split_semicolon(row["files_to_open"]),
        "handoff_files_to_open": split_semicolon(row["handoff_files_to_open"]),
        "outcome_handoff_files_to_open": split_semicolon(row["outcome_handoff_files_to_open"]),
        "reserved_outcome_fields": split_semicolon(row["reserved_outcome_fields"]),
        "checklist_status": row["checklist_status"],
        "assignment_status": row["assignment_status"],
        "handoff_status": row["handoff_status"],
        "handoff_objective": row["handoff_objective"],
        "route_status": row["route_status"],
        "review_outcome_status": row["review_outcome_status"],
        "evidence_collection_status": row["evidence_collection_status"],
        "reviewed_evidence_paths": row["reviewed_evidence_paths"],
        "reviewed_outcome_summary": row["reviewed_outcome_summary"],
        "remaining_blockers_reviewed": row["remaining_blockers_reviewed"],
        "required_followup_reviewed": row["required_followup_reviewed"],
        "human_review_status": row["human_review_status"],
        "rights_decision_status": row["rights_decision_status"],
        "source_promotion_status": row["source_promotion_status"],
        "corpus_import_status": row["corpus_import_status"],
        "decipherment_claim_status": row["decipherment_claim_status"],
        "identity_claim_status": row["identity_claim_status"],
        "component_claim_status": row["component_claim_status"],
        "evolution_claim_status": row["evolution_claim_status"],
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
    }


def build_route_summary(checklist_rows: list[dict[str, str]]) -> dict[str, object]:
    routes = [route_from_row(index, row) for index, row in enumerate(checklist_rows, start=1)]
    source_counts = Counter(route["source_id"] for route in routes)
    return {
        "route_summary_id": "source-pipeline-missing-evidence-review-outcome-handoff-route-summary-001",
        "updated_at": UPDATED_AT,
        "outcome_handoff_checklist_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_CHECKLIST.as_posix(),
        "route_count": len(routes),
        "source_count": len(source_counts),
        "source_counts": dict(sorted(source_counts.items())),
        "pipeline_gap_status_counts": dict(sorted(Counter(route["pipeline_gap_status"] for route in routes).items())),
        "checklist_status_counts": dict(sorted(Counter(route["checklist_status"] for route in routes).items())),
        "assignment_status_counts": dict(sorted(Counter(route["assignment_status"] for route in routes).items())),
        "handoff_status_counts": dict(sorted(Counter(route["handoff_status"] for route in routes).items())),
        "review_outcome_status_counts": dict(sorted(Counter(route["review_outcome_status"] for route in routes).items())),
        "human_review_status_counts": dict(sorted(Counter(route["human_review_status"] for route in routes).items())),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "routes": routes,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source pipeline outcome handoff route summary.")
    parser.add_argument(
        "--checklist",
        default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_CHECKLIST),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_route_summary(read_csv_rows(root / args.checklist))
    write_json(root / args.output, data)
    print(f"missing_evidence_outcome_handoff_summary_routes={data['route_count']} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
