#!/usr/bin/env python3
"""Build a route pack for core-corpus phase gap review outcome scaffolds.

The route pack indexes the 204 outcome scaffold rows so a later reviewer can
open the routed files before filling human-reviewed outcomes. It does not
collect evidence, decide rights, promote sources or candidates, import corpus
rows, or make identity, component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_SCAFFOLD = (
    STAT_DIR / "204_core-corpus-phase-gap-review-outcome-scaffold.csv"
)
DEFAULT_OUTPUT = STAT_DIR / "205_core-corpus-phase-gap-review-outcome-route-pack.json"

UPDATED_AT = "2026-06-20"
ROUTE_STATUS = "not_started"
AUTOMATION_BOUNDARY = "routing_only_no_core_corpus_phase_gap_outcome_capture"
RESEARCH_BOUNDARY = "core_corpus_phase_gap_review_outcome_route_pack_not_scholarship"
CAUTION = (
    "This core corpus phase gap review outcome route pack is routing-only. "
    "It is not collected evidence, not a reviewed outcome, not a rights "
    "decision, not source or candidate promotion, not a corpus import, not an "
    "identity claim, not a component assignment, not an evolution-chain "
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
    return {
        "outcome_route_id": f"core-corpus-phase-gap-review-outcome-route-{index:03d}",
        "core_corpus_phase_gap_review_outcome_scaffold_id": row[
            "core_corpus_phase_gap_review_outcome_scaffold_id"
        ],
        "summary_route_id": row["summary_route_id"],
        "handoff_review_checklist_id": row["handoff_review_checklist_id"],
        "handoff_id": row["handoff_id"],
        "review_route_id": row["route_id"],
        "review_index_id": row["review_index_id"],
        "gap_queue_id": row["gap_queue_id"],
        "source_phase_row_id": row["source_phase_row_id"],
        "corpus_area": row["corpus_area"],
        "label_en": row["label_en"],
        "phase_name": row["phase_name"],
        "phase_status": row["phase_status"],
        "gap_type": row["gap_type"],
        "review_priority": row["review_priority"],
        "specialized_checklist_family": row["specialized_checklist_family"],
        "specialized_checklist_id": row["specialized_checklist_id"],
        "specialized_checklist_path": row["specialized_checklist_path"],
        "coverage_status": row["coverage_status"],
        "recommended_action": row["recommended_action"],
        "candidate_or_staging_boundary": row["candidate_or_staging_boundary"],
        "outcome_scaffold_path": CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_SCAFFOLD.as_posix(),
        "route_summary_path": row["route_summary_path"],
        "outcome_update_target_path": row["outcome_update_target_path"],
        "handoff_review_checklist_path": row["handoff_review_checklist_path"],
        "handoff_scaffold_path": row["handoff_scaffold_path"],
        "route_pack_path": row["route_pack_path"],
        "review_index_path": row["review_index_path"],
        "route_files_to_open": split_semicolon(row["route_files_to_open"]),
        "handoff_files_to_open": split_semicolon(row["handoff_files_to_open"]),
        "required_review_steps": split_semicolon(row["required_review_steps"]),
        "required_precheck_steps": split_semicolon(row["required_precheck_steps"]),
        "reserved_outcome_fields": split_semicolon(row["reserved_outcome_fields"]),
        "route_status": ROUTE_STATUS,
        "review_outcome_status": row["review_outcome_status"],
        "evidence_collection_status": row["evidence_collection_status"],
        "phase_gap_outcome_reviewed": row["phase_gap_outcome_reviewed"],
        "specialized_checklist_outcome_reviewed": row["specialized_checklist_outcome_reviewed"],
        "reviewed_evidence_paths": row["reviewed_evidence_paths"],
        "reviewed_outcome_summary": row["reviewed_outcome_summary"],
        "reviewed_rights_decision": row["reviewed_rights_decision"],
        "reviewed_source_or_candidate_promotion": row["reviewed_source_or_candidate_promotion"],
        "reviewed_corpus_import": row["reviewed_corpus_import"],
        "reviewed_decipherment_claim": row["reviewed_decipherment_claim"],
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


def build_route_pack(outcome_rows: list[dict[str, str]]) -> dict[str, object]:
    routes = [route_from_row(index, row) for index, row in enumerate(outcome_rows, start=1)]
    return {
        "route_pack_id": "core-corpus-phase-gap-review-outcome-route-pack-001",
        "updated_at": UPDATED_AT,
        "outcome_scaffold_path": CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_SCAFFOLD.as_posix(),
        "route_pack_path": DEFAULT_OUTPUT.as_posix(),
        "route_count": len(routes),
        "gap_count": len({route["gap_queue_id"] for route in routes}),
        "corpus_area_count": len({route["corpus_area"] for route in routes}),
        "specialized_checklist_family_count": len({route["specialized_checklist_family"] for route in routes}),
        "corpus_area_counts": dict(sorted(Counter(route["corpus_area"] for route in routes).items())),
        "phase_status_counts": dict(sorted(Counter(route["phase_status"] for route in routes).items())),
        "specialized_checklist_family_counts": dict(
            sorted(Counter(route["specialized_checklist_family"] for route in routes).items())
        ),
        "route_status_counts": dict(sorted(Counter(route["route_status"] for route in routes).items())),
        "review_outcome_status_counts": dict(
            sorted(Counter(route["review_outcome_status"] for route in routes).items())
        ),
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
        "identity_claim_status_counts": dict(sorted(Counter(route["identity_claim_status"] for route in routes).items())),
        "component_claim_status_counts": dict(
            sorted(Counter(route["component_claim_status"] for route in routes).items())
        ),
        "evolution_claim_status_counts": dict(
            sorted(Counter(route["evolution_claim_status"] for route in routes).items())
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
    parser = argparse.ArgumentParser(description="Build the core corpus phase gap review outcome route pack.")
    parser.add_argument("--outcome-scaffold", default=str(CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_SCAFFOLD))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_route_pack(read_csv_rows(root / args.outcome_scaffold))
    write_json(root / args.output, data)
    print(f"core_corpus_phase_gap_review_outcome_routes={data['route_count']} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
