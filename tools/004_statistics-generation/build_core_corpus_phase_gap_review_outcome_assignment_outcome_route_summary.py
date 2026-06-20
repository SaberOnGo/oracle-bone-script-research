#!/usr/bin/env python3
"""Build a route summary for core-corpus assignment outcome scaffolds.

The summary indexes the 211 empty outcome scaffold rows for later human-gated
review. It does not collect evidence, record reviewed outcomes, decide rights,
promote sources or candidates, import corpus rows, or make identity,
component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ASSIGNMENT_OUTCOME_SCAFFOLD = (
    STAT_DIR / "211_core-corpus-phase-gap-review-outcome-assignment-outcome-scaffold.csv"
)
DEFAULT_OUTPUT = STAT_DIR / "212_core-corpus-phase-gap-review-outcome-assignment-outcome-route-summary.json"

UPDATED_AT = "2026-06-21"
AUTOMATION_BOUNDARY = "assignment_outcome_route_summary_only_no_core_corpus_phase_gap_outcome_capture"
RESEARCH_BOUNDARY = "core_corpus_phase_gap_review_outcome_assignment_outcome_route_summary_not_scholarship"
CAUTION = (
    "This core corpus phase gap review assignment outcome route summary is "
    "routing-only. It is not collected evidence, not a reviewed outcome, not a "
    "rights decision, not source or candidate promotion, not a corpus import, "
    "not an identity claim, not a component assignment, not an evolution-chain "
    "assignment, and not a decipherment conclusion."
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
        "route_files_to_open",
        "assignment_files_to_open",
        "outcome_files_to_open",
        "required_review_steps",
        "required_precheck_steps",
        "required_assignment_check_steps",
        "required_outcome_steps",
        "reserved_outcome_fields",
    }
    route: dict[str, object] = {
        key: split_semicolon(value) if key in list_fields else value
        for key, value in row.items()
    }
    route.update(
        {
            "assignment_outcome_route_summary_id": (
                "core-corpus-phase-gap-review-outcome-assignment-outcome-summary-route-"
                f"{index:03d}"
            ),
            "assignment_outcome_scaffold_path": (
                CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ASSIGNMENT_OUTCOME_SCAFFOLD.as_posix()
            ),
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
    wave_counts = Counter(str(route["assignment_wave_id"]) for route in routes)
    corpus_area_counts = Counter(str(route["corpus_area"]) for route in routes)
    family_counts = Counter(str(route["specialized_checklist_family"]) for route in routes)
    return {
        "route_summary_id": "core-corpus-phase-gap-review-outcome-assignment-outcome-route-summary-001",
        "updated_at": UPDATED_AT,
        "assignment_outcome_scaffold_path": (
            CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ASSIGNMENT_OUTCOME_SCAFFOLD.as_posix()
        ),
        "route_count": len(routes),
        "assignment_wave_count": len(wave_counts),
        "corpus_area_count": len(corpus_area_counts),
        "specialized_checklist_family_count": len(family_counts),
        "gap_count": len({str(route["gap_queue_id"]) for route in routes}),
        "assignment_wave_counts": dict(sorted(wave_counts.items())),
        "corpus_area_counts": dict(sorted(corpus_area_counts.items())),
        "specialized_checklist_family_counts": dict(sorted(family_counts.items())),
        "phase_status_counts": status_counts(routes, "phase_status"),
        "assignment_status_counts": status_counts(routes, "assignment_status"),
        "checklist_status_counts": status_counts(routes, "checklist_status"),
        "assignment_outcome_status_counts": status_counts(routes, "assignment_outcome_status"),
        "review_outcome_status_counts": status_counts(routes, "review_outcome_status"),
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
    parser = argparse.ArgumentParser(description="Build core corpus assignment outcome route summary.")
    parser.add_argument(
        "--scaffold",
        default=str(CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ASSIGNMENT_OUTCOME_SCAFFOLD),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_route_summary(read_csv_rows(root / args.scaffold))
    write_json(root / args.output, data)
    print(f"core_corpus_phase_gap_review_outcome_assignment_outcome_summary_routes={data['route_count']} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
