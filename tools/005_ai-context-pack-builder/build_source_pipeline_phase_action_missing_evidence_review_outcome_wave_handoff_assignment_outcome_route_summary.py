#!/usr/bin/env python3
"""Build a route summary for missing-evidence assignment outcome scaffolds."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SCAFFOLD = (
    STAT_DIR / "166_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-scaffold.csv"
)
DEFAULT_OUTPUT = (
    STAT_DIR / "167_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-route-summary.json"
)

UPDATED_AT = "2026-06-19"
AUTOMATION_BOUNDARY = "assignment_outcome_route_summary_only_no_evidence_capture"
RESEARCH_BOUNDARY = (
    "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_route_summary_not_scholarship"
)
CAUTION = (
    "This source pipeline missing-evidence assignment outcome route summary is routing-only. "
    "It is not collected evidence, not a reviewed outcome, not a rights decision, "
    "not source promotion, not a corpus import, not an identity claim, not a component "
    "assignment, not an evolution-chain assignment, and not a decipherment conclusion."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_semicolon(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def route_from_row(index: int, row: dict[str, str]) -> dict[str, object]:
    list_fields = {
        "missing_file_roles",
        "priority_tags",
        "required_review_steps",
        "required_precheck_steps",
        "required_review_actions",
        "required_assignment_check_steps",
        "route_files_to_open",
        "assignment_files_to_open",
        "reserved_outcome_fields",
    }
    route: dict[str, object] = {
        key: split_semicolon(value) if key in list_fields else value
        for key, value in row.items()
    }
    route.update(
        {
            "summary_route_id": (
                "source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-outcome-summary-route-"
                f"{index:03d}"
            ),
            "assignment_outcome_scaffold_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SCAFFOLD.as_posix(),
            "automation_boundary": AUTOMATION_BOUNDARY,
            "research_boundary": RESEARCH_BOUNDARY,
            "caution": CAUTION,
        }
    )
    return route


def status_counts(routes: list[dict[str, object]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(route.get(field, "")) for route in routes).items()))


def build_route_summary(scaffold_rows: list[dict[str, str]]) -> dict[str, object]:
    routes = [route_from_row(index, row) for index, row in enumerate(scaffold_rows, start=1)]
    source_counts = Counter(str(route["source_id"]) for route in routes)
    wave_counts = Counter(str(route["handoff_wave_id"]) for route in routes)
    return {
        "route_summary_id": "source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-outcome-route-summary-001",
        "updated_at": UPDATED_AT,
        "assignment_outcome_scaffold_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SCAFFOLD.as_posix(),
        "route_count": len(routes),
        "source_count": len(source_counts),
        "handoff_wave_count": len(wave_counts),
        "source_counts": dict(sorted(source_counts.items())),
        "handoff_wave_counts": dict(sorted(wave_counts.items())),
        "pipeline_gap_status_counts": status_counts(routes, "pipeline_gap_status"),
        "assignment_review_status_counts": status_counts(routes, "assignment_review_status"),
        "review_outcome_status_counts": status_counts(routes, "review_outcome_status"),
        "evidence_collection_status_counts": status_counts(routes, "evidence_collection_status"),
        "human_review_status_counts": status_counts(routes, "human_review_status"),
        "rights_decision_status_counts": status_counts(routes, "rights_decision_status"),
        "source_promotion_status_counts": status_counts(routes, "source_promotion_status"),
        "corpus_import_status_counts": status_counts(routes, "corpus_import_status"),
        "decipherment_claim_status_counts": status_counts(routes, "decipherment_claim_status"),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "routes": routes,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build missing-evidence assignment outcome route summary.")
    parser.add_argument(
        "--scaffold",
        default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SCAFFOLD),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_route_summary(read_csv_rows(root / args.scaffold))
    write_json(root / args.output, data)
    print(f"missing_evidence_assignment_outcome_summary_routes={data['route_count']} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
