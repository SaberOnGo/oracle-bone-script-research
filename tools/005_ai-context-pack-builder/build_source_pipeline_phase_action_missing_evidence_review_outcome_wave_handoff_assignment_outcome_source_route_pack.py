#!/usr/bin/env python3
"""Build a routing-only pack for assignment outcome source checklists."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_CHECKLIST = (
    STAT_DIR
    / "169_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-checklist.csv"
)
DEFAULT_OUTPUT = (
    STAT_DIR
    / "170_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-route-pack.json"
)

UPDATED_AT = "2026-06-19"
ROUTE_STATUS = "not_started"
AUTOMATION_BOUNDARY = "assignment_outcome_source_route_pack_only_no_evidence_capture"
RESEARCH_BOUNDARY = (
    "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_route_pack_not_scholarship"
)
CAUTION = (
    "This source pipeline missing-evidence assignment outcome source route pack is routing-only. "
    "It is not collected evidence, not a reviewed outcome, not a rights decision, "
    "not source promotion, not a corpus import, not an identity claim, not a "
    "component assignment, not an evolution-chain assignment, and not a "
    "decipherment conclusion."
)

LIST_FIELDS = [
    "handoff_wave_ids",
    "assignment_wave_ids",
    "assignment_plan_item_ids",
    "assignment_review_checklist_ids",
    "assignment_outcome_scaffold_ids",
    "assignment_outcome_route_ids",
    "missing_file_roles",
    "priority_tags",
    "required_source_review_steps",
    "source_files_to_open",
    "draft_paths",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_semicolon(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def source_route_from_row(index: int, row: dict[str, str]) -> dict[str, object]:
    route: dict[str, object] = {
        "source_route_id": (
            "source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-route-"
            f"{index:03d}"
        ),
        "source_checklist_path": (
            SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_CHECKLIST.as_posix()
        ),
    }
    for field, value in row.items():
        route[field] = split_semicolon(value) if field in LIST_FIELDS else value
    route["route_status"] = ROUTE_STATUS
    route["automation_boundary"] = AUTOMATION_BOUNDARY
    route["research_boundary"] = RESEARCH_BOUNDARY
    route["caution"] = CAUTION
    return route


def build_source_route_pack(checklist_rows: list[dict[str, str]]) -> dict[str, object]:
    routes = [source_route_from_row(index, row) for index, row in enumerate(checklist_rows, start=1)]
    return {
        "route_pack_id": (
            "source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-route-pack-001"
        ),
        "updated_at": UPDATED_AT,
        "source_checklist_path": (
            SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_CHECKLIST.as_posix()
        ),
        "route_pack_path": DEFAULT_OUTPUT.as_posix(),
        "route_count": len(routes),
        "source_count": len({route["source_id"] for route in routes}),
        "source_counts": dict(sorted(Counter(route["source_id"] for route in routes).items())),
        "pipeline_gap_status_counts": dict(sorted(Counter(route["pipeline_gap_status"] for route in routes).items())),
        "source_review_status_counts": dict(sorted(Counter(route["source_review_status"] for route in routes).items())),
        "route_status_counts": dict(sorted(Counter(route["route_status"] for route in routes).items())),
        "evidence_collection_status_counts": dict(
            sorted(Counter(route["evidence_collection_status"] for route in routes).items())
        ),
        "human_review_status_counts": dict(sorted(Counter(route["human_review_status"] for route in routes).items())),
        "rights_decision_status_counts": dict(
            sorted(Counter(route["rights_decision_status"] for route in routes).items())
        ),
        "source_promotion_status_counts": dict(
            sorted(Counter(route["source_promotion_status"] for route in routes).items())
        ),
        "corpus_import_status_counts": dict(sorted(Counter(route["corpus_import_status"] for route in routes).items())),
        "decipherment_claim_status_counts": dict(
            sorted(Counter(route["decipherment_claim_status"] for route in routes).items())
        ),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "routes": routes,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build assignment outcome source route pack.")
    parser.add_argument(
        "--source-checklist",
        default=str(
            SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_CHECKLIST
        ),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_source_route_pack(read_csv_rows(root / args.source_checklist))
    write_json(root / args.output, data)
    print(f"assignment_outcome_source_routes={data['route_count']} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
