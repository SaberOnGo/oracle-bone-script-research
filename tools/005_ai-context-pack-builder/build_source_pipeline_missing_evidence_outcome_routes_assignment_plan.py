#!/usr/bin/env python3
"""Build an assignment plan for the 183 missing-evidence outcome routes."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_MISSING_EVIDENCE_OUTCOME_ROUTES_SUMMARY = (
    STAT_DIR
    / "183_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-routes-summary.json"
)
DEFAULT_OUTPUT = STAT_DIR / "184_source-pipeline-missing-evidence-outcome-routes-assignment-plan.json"

UPDATED_AT = "2026-06-19"
ASSIGNMENT_STATUS = "not_started"
AUTOMATION_BOUNDARY = "source_pipeline_missing_evidence_outcome_routes_assignment_plan_only_no_evidence_capture"
RESEARCH_BOUNDARY = "source_pipeline_missing_evidence_outcome_routes_assignment_plan_not_scholarship"
CAUTION = (
    "This source pipeline missing-evidence outcome routes assignment plan only "
    "groups route-summary rows for later human review. It is not collected "
    "evidence, not a reviewed outcome, not a rights decision, not a source "
    "promotion, not a corpus import, not an identity claim, not a component "
    "assignment, not an evolution-chain assignment, and not a decipherment "
    "conclusion."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def unique_sorted(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def route_id(route: dict[str, object]) -> str:
    return str(route.get("source_handoff_outcome_checklist_outcome_routes_summary_route_id", ""))


def listify(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if isinstance(value, str) and value:
        return [part.strip() for part in value.split(";") if part.strip()]
    return []


def assignment_files_to_open(group_routes: list[dict[str, object]]) -> list[str]:
    route_files = [
        route_file
        for route in group_routes
        for route_file in listify(route.get("source_handoff_outcome_checklist_outcome_routes_summary_files_to_open"))
    ]
    return unique_sorted([DEFAULT_OUTPUT.as_posix(), SOURCE_PIPELINE_MISSING_EVIDENCE_OUTCOME_ROUTES_SUMMARY.as_posix(), *route_files])


def build_assignment(index: int, status: str, group_routes: list[dict[str, object]]) -> dict[str, object]:
    source_ids = unique_sorted([str(route.get("source_id", "")) for route in group_routes])
    return {
        "assignment_id": f"source-pipeline-missing-evidence-outcome-routes-assignment-{index:03d}",
        "pipeline_gap_status": status,
        "assignment_status": ASSIGNMENT_STATUS,
        "route_summary_path": SOURCE_PIPELINE_MISSING_EVIDENCE_OUTCOME_ROUTES_SUMMARY.as_posix(),
        "assignment_plan_path": DEFAULT_OUTPUT.as_posix(),
        "route_count": len(group_routes),
        "source_count": len(source_ids),
        "source_ids": source_ids,
        "route_ids": [route_id(route) for route in group_routes],
        "source_handoff_outcome_checklist_ids": unique_sorted(
            [str(route.get("source_handoff_outcome_checklist_id", "")) for route in group_routes]
        ),
        "source_handoff_outcome_checklist_outcome_routes_checklist_ids": [
            str(route.get("source_handoff_outcome_checklist_outcome_routes_checklist_id", ""))
            for route in group_routes
        ],
        "assignment_files_to_open": assignment_files_to_open(group_routes),
        "reviewed_evidence_paths": "",
        "reviewed_outcome_summary": "",
        "human_reviewer": "",
        "human_reviewed_at": "",
        "evidence_collection_status": "not_collected",
        "rights_decision_status": "no_rights_decision",
        "source_promotion_status": "no_source_promotion",
        "corpus_import_status": "not_imported",
        "decipherment_claim_status": "no_decipherment_claim",
        "identity_claim_status": "no_identity_claim",
        "component_claim_status": "no_component_claim",
        "evolution_claim_status": "no_evolution_chain_claim",
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
    }


def build_assignment_plan(route_summary: dict[str, object]) -> dict[str, object]:
    routes = [route for route in route_summary.get("routes", []) if isinstance(route, dict)]
    grouped: dict[str, list[dict[str, object]]] = {}
    for route in routes:
        grouped.setdefault(str(route.get("pipeline_gap_status", "")), []).append(route)
    assignments = [
        build_assignment(index, status, grouped[status])
        for index, status in enumerate(sorted(grouped), start=1)
    ]
    source_ids = unique_sorted([str(route.get("source_id", "")) for route in routes])
    return {
        "assignment_plan_id": "source-pipeline-missing-evidence-outcome-routes-assignment-plan-001",
        "updated_at": UPDATED_AT,
        "route_summary_path": SOURCE_PIPELINE_MISSING_EVIDENCE_OUTCOME_ROUTES_SUMMARY.as_posix(),
        "upstream_route_summary_id": route_summary.get("route_summary_id", ""),
        "route_count": len(routes),
        "source_count": len(source_ids),
        "assignment_count": len(assignments),
        "pipeline_gap_status_counts": dict(sorted(Counter(str(route.get("pipeline_gap_status", "")) for route in routes).items())),
        "assignment_status_counts": dict(sorted(Counter(assignment["assignment_status"] for assignment in assignments).items())),
        "evidence_collection_status_counts": dict(sorted(Counter(assignment["evidence_collection_status"] for assignment in assignments).items())),
        "rights_decision_status_counts": dict(sorted(Counter(assignment["rights_decision_status"] for assignment in assignments).items())),
        "source_promotion_status_counts": dict(sorted(Counter(assignment["source_promotion_status"] for assignment in assignments).items())),
        "corpus_import_status_counts": dict(sorted(Counter(assignment["corpus_import_status"] for assignment in assignments).items())),
        "decipherment_claim_status_counts": dict(sorted(Counter(assignment["decipherment_claim_status"] for assignment in assignments).items())),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "assignments": assignments,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source pipeline missing-evidence outcome routes assignment plan.")
    parser.add_argument("--route-summary", default=str(SOURCE_PIPELINE_MISSING_EVIDENCE_OUTCOME_ROUTES_SUMMARY))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_assignment_plan(read_json(root / args.route_summary))
    write_json(root / args.output, data)
    print(
        f"missing_evidence_outcome_route_assignments={data['assignment_count']} "
        f"routes={data['route_count']} output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
