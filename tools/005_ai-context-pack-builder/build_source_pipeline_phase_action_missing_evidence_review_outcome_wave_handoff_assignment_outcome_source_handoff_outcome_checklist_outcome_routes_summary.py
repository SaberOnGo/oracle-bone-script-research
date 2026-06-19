#!/usr/bin/env python3
"""Build a route summary for the 182 checklist outcome routes checklist."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST_OUTCOME_ROUTES_CHECKLIST = (
    STAT_DIR
    / "182_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-routes-checklist.csv"
)
DEFAULT_OUTPUT = (
    STAT_DIR
    / "183_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-routes-summary.json"
)

UPDATED_AT = "2026-06-19"
AUTOMATION_BOUNDARY = "assignment_outcome_source_handoff_outcome_checklist_outcome_routes_summary_only_no_evidence_capture"
RESEARCH_BOUNDARY = (
    "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_outcome_checklist_outcome_routes_summary_not_scholarship"
)
CAUTION = (
    "This source pipeline missing-evidence assignment outcome source handoff "
    "outcome routes summary is routing-only. It does not capture evidence, "
    "is not a reviewed outcome, is not a rights decision, is not a source "
    "promotion, is not a corpus import, is not an identity claim, is not a "
    "component assignment, is not an evolution-chain assignment, and is not a "
    "decipherment conclusion."
)

LIST_FIELDS = {
    "source_handoff_outcome_checklist_outcome_routes_summary_files_to_open",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_semicolon(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def unique_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return ";".join(seen)


def files_to_open(row: dict[str, str]) -> str:
    return unique_join(
        [
            DEFAULT_OUTPUT.as_posix(),
            SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST_OUTCOME_ROUTES_CHECKLIST.as_posix(),
            *split_semicolon(row.get("source_handoff_outcome_checklist_outcome_routes_checklist_files_to_open", "")),
        ]
    )


def route_from_row(index: int, row: dict[str, str]) -> dict[str, object]:
    copied = dict(row)
    copied["source_handoff_outcome_checklist_outcome_routes_summary_files_to_open"] = files_to_open(row)
    route = {
        key: split_semicolon(value) if key in LIST_FIELDS else value
        for key, value in copied.items()
    }
    route.update(
        {
            "source_handoff_outcome_checklist_outcome_routes_summary_route_id": (
                "source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-routes-summary-route-"
                f"{index:03d}"
            ),
            "source_handoff_outcome_checklist_outcome_routes_checklist_path": (
                SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST_OUTCOME_ROUTES_CHECKLIST.as_posix()
            ),
            "automation_boundary": AUTOMATION_BOUNDARY,
            "research_boundary": RESEARCH_BOUNDARY,
            "caution": CAUTION,
        }
    )
    return route


def status_counts(routes: list[dict[str, object]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(route.get(field, "")) for route in routes).items()))


def build_route_summary(checklist_rows: list[dict[str, str]]) -> dict[str, object]:
    routes = [route_from_row(index, row) for index, row in enumerate(checklist_rows, start=1)]
    source_counts = Counter(str(route["source_id"]) for route in routes)
    return {
        "route_summary_id": "source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-routes-summary-001",
        "updated_at": UPDATED_AT,
        "source_handoff_outcome_checklist_outcome_routes_checklist_path": (
            SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST_OUTCOME_ROUTES_CHECKLIST.as_posix()
        ),
        "route_count": len(routes),
        "source_count": len(source_counts),
        "source_counts": dict(sorted(source_counts.items())),
        "pipeline_gap_status_counts": status_counts(routes, "pipeline_gap_status"),
        "source_handoff_outcome_checklist_outcome_routes_checklist_status_counts": status_counts(
            routes, "source_handoff_outcome_checklist_outcome_routes_checklist_status"
        ),
        "evidence_collection_status_counts": status_counts(routes, "evidence_collection_status"),
        "human_review_status_counts": status_counts(routes, "human_review_status"),
        "rights_decision_status_counts": status_counts(routes, "rights_decision_status"),
        "source_promotion_status_counts": status_counts(routes, "source_promotion_status"),
        "corpus_import_status_counts": status_counts(routes, "corpus_import_status"),
        "decipherment_claim_status_counts": status_counts(routes, "decipherment_claim_status"),
        "identity_claim_status_counts": status_counts(routes, "identity_claim_status"),
        "component_claim_status_counts": status_counts(routes, "component_claim_status"),
        "evolution_claim_status_counts": status_counts(routes, "evolution_claim_status"),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "routes": routes,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build checklist outcome routes route summary.")
    parser.add_argument(
        "--checklist",
        default=str(
            SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST_OUTCOME_ROUTES_CHECKLIST
        ),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_route_summary(read_csv_rows(root / args.checklist))
    write_json(root / args.output, data)
    print(f"assignment_outcome_source_handoff_outcome_checklist_outcome_routes_summary_routes={data['route_count']} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
