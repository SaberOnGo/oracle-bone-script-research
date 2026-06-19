#!/usr/bin/env python3
"""Build precheck checklist rows from the 181 checklist outcome routes."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST_OUTCOME_ROUTE_SUMMARY_OUTCOME_ROUTE_SUMMARY = (
    STAT_DIR
    / "181_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-routes.json"
)
DEFAULT_OUTPUT = (
    STAT_DIR
    / "182_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-routes-checklist.csv"
)

UPDATED_AT = "2026-06-19"
CHECKLIST_STATUS = "not_started"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_rights_decision"
SOURCE_PROMOTION_STATUS = "no_source_promotion"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
COMPONENT_CLAIM_STATUS = "no_component_claim"
EVOLUTION_CLAIM_STATUS = "no_evolution_chain_claim"
AUTOMATION_BOUNDARY = "assignment_outcome_source_handoff_outcome_checklist_outcome_routes_checklist_only_no_evidence_capture"
RESEARCH_BOUNDARY = (
    "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_outcome_checklist_outcome_routes_checklist_not_scholarship"
)
REQUIRED_CHECK_STEPS = ";".join(
    [
        "open_181_outcome_route_summary",
        "open_180_outcome_scaffold",
        "open_179_outcome_route_summary",
        "confirm_reviewed_evidence_paths_empty",
        "confirm_reviewed_outcome_summary_empty",
        "confirm_no_rights_decision",
        "confirm_no_source_promotion",
        "confirm_no_corpus_import",
        "confirm_no_decipherment_claim",
        "route_to_human_source_outcome_review_only_after_source_files_are_opened",
    ]
)
CAUTION = (
    "This source pipeline missing-evidence assignment outcome source handoff "
    "outcome routes file is a precheck checklist. It does not capture evidence, "
    "is not a reviewed outcome, is not a rights decision, is not a source "
    "promotion, is not a corpus import, is not an identity claim, is not a "
    "component assignment, is not an evolution-chain assignment, and is not a "
    "decipherment conclusion."
)

PASSTHROUGH_FIELDS = [
    "source_handoff_outcome_checklist_outcome_route_summary_outcome_summary_route_id",
    "source_handoff_outcome_checklist_outcome_route_summary_outcome_scaffold_id",
    "source_handoff_outcome_checklist_outcome_summary_route_id",
    "source_handoff_outcome_checklist_outcome_scaffold_id",
    "source_handoff_outcome_checklist_summary_route_id",
    "source_handoff_outcome_checklist_id",
    "source_handoff_outcome_summary_route_id",
    "source_handoff_outcome_scaffold_id",
    "source_handoff_summary_route_id",
    "source_handoff_id",
    "source_route_id",
    "assignment_outcome_source_checklist_id",
    "assignment_outcome_source_summary_id",
    "source_id",
    "source_label",
    "source_type",
    "rights_status",
    "pipeline_gap_status",
    "source_handoff_outcome_checklist_outcome_route_summary_path",
    "source_handoff_outcome_checklist_outcome_route_summary_outcome_scaffold_path",
    "source_handoff_outcome_checklist_outcome_route_summary_outcome_status",
    "reviewed_evidence_paths",
    "reviewed_outcome_summary",
    "human_reviewer",
    "human_reviewed_at",
    "remaining_blockers_reviewed",
    "required_followup_reviewed",
    "blocking_condition",
]

CHECKLIST_FIELDS = [
    "source_handoff_outcome_checklist_outcome_routes_checklist_id",
    *PASSTHROUGH_FIELDS,
    "source_handoff_outcome_checklist_outcome_route_summary_outcome_route_summary_path",
    "source_handoff_outcome_checklist_outcome_routes_checklist_path",
    "source_handoff_outcome_checklist_outcome_routes_checklist_status",
    "required_source_handoff_outcome_checklist_outcome_routes_check_steps",
    "source_handoff_outcome_checklist_outcome_routes_checklist_files_to_open",
    "evidence_collection_status",
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


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def join_semicolon(value: object) -> str:
    if isinstance(value, list):
        return ";".join(str(part) for part in value if part)
    return str(value) if value is not None else ""


def split_semicolon(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def unique_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return ";".join(seen)


def files_to_open(route: dict[str, object]) -> str:
    route_files = route.get("source_handoff_outcome_checklist_outcome_route_summary_outcome_route_files_to_open", [])
    if not isinstance(route_files, list):
        route_files = split_semicolon(str(route_files))
    return unique_join(
        [
            DEFAULT_OUTPUT.as_posix(),
            SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST_OUTCOME_ROUTE_SUMMARY_OUTCOME_ROUTE_SUMMARY.as_posix(),
            *[str(path) for path in route_files],
        ]
    )


def build_checklist_rows(route_summary: dict[str, object]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    routes = route_summary.get("routes", [])
    if not isinstance(routes, list):
        return rows
    for index, route in enumerate(routes, start=1):
        route_row = route if isinstance(route, dict) else {}
        row = {
            "source_handoff_outcome_checklist_outcome_routes_checklist_id": (
                "source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-routes-checklist-"
                f"{index:03d}"
            )
        }
        for field in PASSTHROUGH_FIELDS:
            row[field] = join_semicolon(route_row.get(field))
        row.update(
            {
                "source_handoff_outcome_checklist_outcome_route_summary_outcome_route_summary_path": (
                    SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST_OUTCOME_ROUTE_SUMMARY_OUTCOME_ROUTE_SUMMARY.as_posix()
                ),
                "source_handoff_outcome_checklist_outcome_routes_checklist_path": DEFAULT_OUTPUT.as_posix(),
                "source_handoff_outcome_checklist_outcome_routes_checklist_status": CHECKLIST_STATUS,
                "required_source_handoff_outcome_checklist_outcome_routes_check_steps": REQUIRED_CHECK_STEPS,
                "source_handoff_outcome_checklist_outcome_routes_checklist_files_to_open": files_to_open(route_row),
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
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
        rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CHECKLIST_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build checklist outcome routes precheck checklist.")
    parser.add_argument(
        "--route-summary",
        default=str(
            SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST_OUTCOME_ROUTE_SUMMARY_OUTCOME_ROUTE_SUMMARY
        ),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_checklist_rows(read_json(root / args.route_summary))
    write_csv(root / args.output, rows)
    print(f"assignment_outcome_source_handoff_outcome_checklist_outcome_routes_checklist_rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
