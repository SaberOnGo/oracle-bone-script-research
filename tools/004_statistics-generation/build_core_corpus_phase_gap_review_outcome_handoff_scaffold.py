#!/usr/bin/env python3
"""Build a planned handoff scaffold for core-corpus outcome routes.

The scaffold wraps the 205 outcome route pack as planned handoff rows. It does
not collect evidence, assign owners, decide rights, promote sources or
candidates, import corpus rows, or make identity, component, evolution, or
decipherment claims.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ROUTE_PACK = (
    STAT_DIR / "205_core-corpus-phase-gap-review-outcome-route-pack.json"
)
DEFAULT_OUTPUT = STAT_DIR / "206_core-corpus-phase-gap-review-outcome-handoff-scaffold.json"

UPDATED_AT = "2026-06-20"
ASSIGNMENT_STATUS = "planned_not_assigned"
HANDOFF_STATUS = "not_started"
AUTOMATION_BOUNDARY = "planned_handoff_only_no_core_corpus_phase_gap_outcome_capture"
RESEARCH_BOUNDARY = "core_corpus_phase_gap_review_outcome_handoff_scaffold_not_scholarship"
CAUTION = (
    "This core corpus phase gap review outcome handoff scaffold is planned-only. "
    "It is not collected evidence, not a reviewed outcome, not a rights "
    "decision, not source or candidate promotion, not a corpus import, not an "
    "identity claim, not a component assignment, not an evolution-chain "
    "assignment, and not a decipherment conclusion."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def handoff_from_route(index: int, route: dict[str, object]) -> dict[str, object]:
    handoff = {
        "outcome_handoff_id": f"core-corpus-phase-gap-review-outcome-handoff-{index:03d}",
        "outcome_route_pack_path": CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ROUTE_PACK.as_posix(),
        "assignment_status": ASSIGNMENT_STATUS,
        "handoff_status": HANDOFF_STATUS,
        "handoff_objective": "open_outcome_route_files_and_record_human_reviewed_core_corpus_phase_gap_outcome_later",
    }
    handoff.update(route)
    handoff["outcome_handoff_id"] = f"core-corpus-phase-gap-review-outcome-handoff-{index:03d}"
    handoff["outcome_route_pack_path"] = CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ROUTE_PACK.as_posix()
    handoff["assignment_status"] = ASSIGNMENT_STATUS
    handoff["handoff_status"] = HANDOFF_STATUS
    handoff["automation_boundary"] = AUTOMATION_BOUNDARY
    handoff["research_boundary"] = RESEARCH_BOUNDARY
    handoff["caution"] = CAUTION
    return handoff


def build_handoff_scaffold(route_pack: dict[str, object]) -> dict[str, object]:
    routes = route_pack.get("routes", [])
    handoffs = [
        handoff_from_route(index, route)
        for index, route in enumerate(routes, start=1)
        if isinstance(route, dict)
    ]
    return {
        "handoff_scaffold_id": "core-corpus-phase-gap-review-outcome-handoff-scaffold-001",
        "updated_at": UPDATED_AT,
        "outcome_route_pack_path": CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ROUTE_PACK.as_posix(),
        "outcome_scaffold_path": route_pack["outcome_scaffold_path"],
        "handoff_count": len(handoffs),
        "route_count": route_pack["route_count"],
        "gap_count": route_pack["gap_count"],
        "corpus_area_count": route_pack["corpus_area_count"],
        "specialized_checklist_family_count": route_pack["specialized_checklist_family_count"],
        "corpus_area_counts": route_pack["corpus_area_counts"],
        "specialized_checklist_family_counts": route_pack["specialized_checklist_family_counts"],
        "assignment_status_counts": dict(
            sorted(Counter(handoff["assignment_status"] for handoff in handoffs).items())
        ),
        "handoff_status_counts": dict(sorted(Counter(handoff["handoff_status"] for handoff in handoffs).items())),
        "review_outcome_status_counts": dict(
            sorted(Counter(handoff["review_outcome_status"] for handoff in handoffs).items())
        ),
        "evidence_collection_status_counts": dict(
            sorted(Counter(handoff["evidence_collection_status"] for handoff in handoffs).items())
        ),
        "human_review_status_counts": dict(
            sorted(Counter(handoff["human_review_status"] for handoff in handoffs).items())
        ),
        "rights_decision_status_counts": dict(
            sorted(Counter(handoff["rights_decision_status"] for handoff in handoffs).items())
        ),
        "source_promotion_status_counts": dict(
            sorted(Counter(handoff["source_promotion_status"] for handoff in handoffs).items())
        ),
        "corpus_import_status_counts": dict(
            sorted(Counter(handoff["corpus_import_status"] for handoff in handoffs).items())
        ),
        "decipherment_claim_status_counts": dict(
            sorted(Counter(handoff["decipherment_claim_status"] for handoff in handoffs).items())
        ),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "handoffs": handoffs,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the core corpus phase gap review outcome handoff scaffold.")
    parser.add_argument("--route-pack", default=str(CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ROUTE_PACK))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_handoff_scaffold(read_json(root / args.route_pack))
    write_json(root / args.output, data)
    print(f"core_corpus_phase_gap_review_outcome_handoffs={data['handoff_count']} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
