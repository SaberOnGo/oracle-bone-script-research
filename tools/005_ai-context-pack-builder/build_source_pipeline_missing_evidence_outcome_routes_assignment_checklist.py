#!/usr/bin/env python3
"""Build precheck checklist rows from the 184 outcome routes assignment plan."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_MISSING_EVIDENCE_OUTCOME_ROUTES_ASSIGNMENT_PLAN = (
    STAT_DIR / "184_source-pipeline-missing-evidence-outcome-routes-assignment-plan.json"
)
SOURCE_PIPELINE_MISSING_EVIDENCE_OUTCOME_ROUTES_SUMMARY = (
    STAT_DIR
    / "183_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-routes-summary.json"
)
DEFAULT_OUTPUT = STAT_DIR / "185_source-pipeline-missing-evidence-outcome-routes-assignment-checklist.csv"

UPDATED_AT = "2026-06-19"
CHECKLIST_STATUS = "not_started"
AUTOMATION_BOUNDARY = "source_pipeline_missing_evidence_outcome_routes_assignment_checklist_only_no_evidence_capture"
RESEARCH_BOUNDARY = "source_pipeline_missing_evidence_outcome_routes_assignment_checklist_not_scholarship"
REQUIRED_ASSIGNMENT_CHECK_STEPS = ";".join(
    [
        "open_185_assignment_checklist",
        "open_184_assignment_plan",
        "open_183_routes_summary",
        "confirm_assignment_group_status_not_started",
        "confirm_route_ids_cover_assignment_group",
        "confirm_reviewed_evidence_paths_empty",
        "confirm_reviewed_outcome_summary_empty",
        "confirm_no_rights_decision",
        "confirm_no_source_promotion",
        "confirm_no_corpus_import",
        "confirm_no_decipherment_claim",
        "do_not_collect_evidence_or_record_outcome_in_checklist",
    ]
)
CAUTION = (
    "This source pipeline missing-evidence outcome routes assignment checklist "
    "is a precheck checklist. It does not capture evidence, is not a reviewed "
    "outcome, is not a rights decision, is not a source promotion, is not a "
    "corpus import, is not an identity claim, is not a component assignment, "
    "is not an evolution-chain assignment, and is not a decipherment conclusion."
)

CHECKLIST_FIELDS = [
    "assignment_checklist_id",
    "assignment_id",
    "pipeline_gap_status",
    "route_summary_path",
    "assignment_plan_path",
    "assignment_checklist_path",
    "route_count",
    "source_count",
    "source_ids",
    "route_ids",
    "source_handoff_outcome_checklist_ids",
    "source_handoff_outcome_checklist_outcome_routes_checklist_ids",
    "required_assignment_check_steps",
    "assignment_checklist_files_to_open",
    "assignment_checklist_status",
    "assignment_status",
    "reviewed_evidence_paths",
    "reviewed_outcome_summary",
    "human_reviewer",
    "human_reviewed_at",
    "evidence_collection_status",
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


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def join_semicolon(value: object) -> str:
    if isinstance(value, list):
        return ";".join(str(item) for item in value if str(item))
    return str(value) if value is not None else ""


def split_semicolon(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if isinstance(value, str):
        return [part for part in value.split(";") if part]
    return []


def unique_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return ";".join(seen)


def files_to_open(assignment: dict[str, object]) -> str:
    return unique_join(
        [
            DEFAULT_OUTPUT.as_posix(),
            SOURCE_PIPELINE_MISSING_EVIDENCE_OUTCOME_ROUTES_ASSIGNMENT_PLAN.as_posix(),
            SOURCE_PIPELINE_MISSING_EVIDENCE_OUTCOME_ROUTES_SUMMARY.as_posix(),
            *split_semicolon(assignment.get("assignment_files_to_open")),
        ]
    )


def row_from_assignment(index: int, assignment: dict[str, object]) -> dict[str, str]:
    return {
        "assignment_checklist_id": f"source-pipeline-missing-evidence-outcome-routes-assignment-checklist-{index:03d}",
        "assignment_id": str(assignment.get("assignment_id", "")),
        "pipeline_gap_status": str(assignment.get("pipeline_gap_status", "")),
        "route_summary_path": str(assignment.get("route_summary_path", "")),
        "assignment_plan_path": SOURCE_PIPELINE_MISSING_EVIDENCE_OUTCOME_ROUTES_ASSIGNMENT_PLAN.as_posix(),
        "assignment_checklist_path": DEFAULT_OUTPUT.as_posix(),
        "route_count": str(assignment.get("route_count", "")),
        "source_count": str(assignment.get("source_count", "")),
        "source_ids": join_semicolon(assignment.get("source_ids")),
        "route_ids": join_semicolon(assignment.get("route_ids")),
        "source_handoff_outcome_checklist_ids": join_semicolon(
            assignment.get("source_handoff_outcome_checklist_ids")
        ),
        "source_handoff_outcome_checklist_outcome_routes_checklist_ids": join_semicolon(
            assignment.get("source_handoff_outcome_checklist_outcome_routes_checklist_ids")
        ),
        "required_assignment_check_steps": REQUIRED_ASSIGNMENT_CHECK_STEPS,
        "assignment_checklist_files_to_open": files_to_open(assignment),
        "assignment_checklist_status": CHECKLIST_STATUS,
        "assignment_status": str(assignment.get("assignment_status", "")),
        "reviewed_evidence_paths": str(assignment.get("reviewed_evidence_paths", "")),
        "reviewed_outcome_summary": str(assignment.get("reviewed_outcome_summary", "")),
        "human_reviewer": str(assignment.get("human_reviewer", "")),
        "human_reviewed_at": str(assignment.get("human_reviewed_at", "")),
        "evidence_collection_status": str(assignment.get("evidence_collection_status", "")),
        "rights_decision_status": str(assignment.get("rights_decision_status", "")),
        "source_promotion_status": str(assignment.get("source_promotion_status", "")),
        "corpus_import_status": str(assignment.get("corpus_import_status", "")),
        "decipherment_claim_status": str(assignment.get("decipherment_claim_status", "")),
        "identity_claim_status": str(assignment.get("identity_claim_status", "")),
        "component_claim_status": str(assignment.get("component_claim_status", "")),
        "evolution_claim_status": str(assignment.get("evolution_claim_status", "")),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_checklist_rows(plan: dict[str, object]) -> list[dict[str, str]]:
    assignments = plan.get("assignments", [])
    if not isinstance(assignments, list):
        return []
    return [
        row_from_assignment(index, assignment)
        for index, assignment in enumerate(assignments, start=1)
        if isinstance(assignment, dict)
    ]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CHECKLIST_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build missing-evidence outcome routes assignment checklist.")
    parser.add_argument("--assignment-plan", default=str(SOURCE_PIPELINE_MISSING_EVIDENCE_OUTCOME_ROUTES_ASSIGNMENT_PLAN))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_checklist_rows(read_json(root / args.assignment_plan))
    write_csv(root / args.output, rows)
    print(f"missing_evidence_outcome_routes_assignment_checklist_rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
