#!/usr/bin/env python3
"""Build a route summary for assignment outcome source handoff checklists."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_CHECKLIST = (
    STAT_DIR
    / "172_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-checklist.csv"
)
DEFAULT_OUTPUT = (
    STAT_DIR
    / "173_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-route-summary.json"
)

UPDATED_AT = "2026-06-19"
AUTOMATION_BOUNDARY = "assignment_outcome_source_handoff_route_summary_only_no_evidence_capture"
RESEARCH_BOUNDARY = (
    "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_route_summary_not_scholarship"
)
CAUTION = (
    "This source pipeline missing-evidence assignment outcome source handoff route "
    "summary is routing-only. It is not collected evidence, not a reviewed "
    "outcome, not a rights decision, not source promotion, not a corpus import, "
    "not an identity claim, not a component assignment, not an evolution-chain "
    "assignment, and not a decipherment conclusion."
)

LIST_FIELDS = {
    "handoff_wave_ids",
    "assignment_wave_ids",
    "assignment_plan_item_ids",
    "assignment_review_checklist_ids",
    "assignment_outcome_scaffold_ids",
    "assignment_outcome_route_ids",
    "missing_file_roles",
    "priority_tags",
    "required_source_review_steps",
    "required_source_handoff_check_steps",
    "source_files_to_open",
    "source_handoff_files_to_open",
    "source_handoff_route_files_to_open",
    "draft_paths",
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


def route_files_to_open(row: dict[str, str]) -> str:
    return unique_join(
        [
            SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_CHECKLIST.as_posix(),
            *split_semicolon(row.get("source_handoff_files_to_open", "")),
        ]
    )


def route_from_row(index: int, row: dict[str, str]) -> dict[str, object]:
    copied = dict(row)
    copied["source_handoff_route_files_to_open"] = route_files_to_open(row)
    route = {
        key: split_semicolon(value) if key in LIST_FIELDS else value
        for key, value in copied.items()
    }
    route.update(
        {
            "source_handoff_summary_route_id": (
                "source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-summary-route-"
                f"{index:03d}"
            ),
            "source_handoff_checklist_path": (
                SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_CHECKLIST.as_posix()
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
        "route_summary_id": (
            "source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-route-summary-001"
        ),
        "updated_at": UPDATED_AT,
        "source_handoff_checklist_path": (
            SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_CHECKLIST.as_posix()
        ),
        "route_count": len(routes),
        "source_count": len(source_counts),
        "source_counts": dict(sorted(source_counts.items())),
        "pipeline_gap_status_counts": status_counts(routes, "pipeline_gap_status"),
        "checklist_status_counts": status_counts(routes, "checklist_status"),
        "assignment_status_counts": status_counts(routes, "assignment_status"),
        "handoff_status_counts": status_counts(routes, "handoff_status"),
        "route_status_counts": status_counts(routes, "route_status"),
        "evidence_collection_status_counts": status_counts(routes, "evidence_collection_status"),
        "human_review_status_counts": status_counts(routes, "human_review_status"),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "routes": routes,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build assignment outcome source handoff route summary.")
    parser.add_argument(
        "--checklist",
        default=str(
            SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_CHECKLIST
        ),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_route_summary(read_csv_rows(root / args.checklist))
    write_json(root / args.output, data)
    print(f"assignment_outcome_source_handoff_summary_routes={data['route_count']} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
