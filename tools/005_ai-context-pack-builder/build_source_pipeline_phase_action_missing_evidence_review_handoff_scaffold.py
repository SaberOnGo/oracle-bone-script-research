#!/usr/bin/env python3
"""Build a planned handoff scaffold for missing-evidence review routes.

The scaffold turns the 151 source-level route pack into a reviewer handoff
surface. It does not collect evidence, assign owners, decide rights, promote
sources, import corpus rows, or make identity, component, evolution, or
decipherment claims.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_ROUTE_PACK = (
    STAT_DIR / "151_source-pipeline-phase-action-missing-evidence-review-route-pack.json"
)
DEFAULT_OUTPUT = STAT_DIR / "152_source-pipeline-phase-action-missing-evidence-review-handoff-scaffold.json"

UPDATED_AT = "2026-06-19"
ASSIGNMENT_STATUS = "planned_not_assigned"
HANDOFF_STATUS = "not_started"
AUTOMATION_BOUNDARY = "planned_handoff_only_no_missing_evidence_outcome_capture"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_missing_evidence_review_handoff_scaffold_not_scholarship"
CAUTION = (
    "This source pipeline missing-evidence review handoff scaffold is planned-only. "
    "It is not collected evidence, not a reviewed outcome, not a rights decision, "
    "not source promotion, not a corpus import, not an identity claim, not a "
    "component assignment, not an evolution-chain assignment, and not a "
    "decipherment conclusion."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def handoff_from_route(index: int, route: dict[str, object]) -> dict[str, object]:
    handoff = {
        "handoff_id": f"source-pipeline-missing-evidence-review-handoff-{index:03d}",
        "route_pack_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_ROUTE_PACK.as_posix(),
        "assignment_status": ASSIGNMENT_STATUS,
        "handoff_status": HANDOFF_STATUS,
        "handoff_objective": "open_route_pack_and_record_human_reviewed_missing_evidence_outcome_later",
    }
    handoff.update(route)
    handoff["route_pack_path"] = SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_ROUTE_PACK.as_posix()
    handoff["assignment_status"] = ASSIGNMENT_STATUS
    handoff["handoff_status"] = HANDOFF_STATUS
    handoff["automation_boundary"] = AUTOMATION_BOUNDARY
    handoff["research_boundary"] = RESEARCH_BOUNDARY
    handoff["caution"] = CAUTION
    return handoff


def build_handoff_scaffold(route_pack: dict[str, object]) -> dict[str, object]:
    routes = route_pack.get("routes", [])
    handoffs = [handoff_from_route(index, route) for index, route in enumerate(routes, start=1)]
    return {
        "handoff_scaffold_id": "source-pipeline-missing-evidence-review-handoff-scaffold-001",
        "updated_at": UPDATED_AT,
        "route_pack_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_ROUTE_PACK.as_posix(),
        "handoff_count": len(handoffs),
        "route_count": route_pack["route_count"],
        "source_count": route_pack["source_count"],
        "route_status_counts": route_pack["route_status_counts"],
        "assignment_status_counts": dict(
            sorted(Counter(handoff["assignment_status"] for handoff in handoffs).items())
        ),
        "handoff_status_counts": dict(sorted(Counter(handoff["handoff_status"] for handoff in handoffs).items())),
        "review_status_counts": dict(sorted(Counter(handoff["review_status"] for handoff in handoffs).items())),
        "human_review_status_counts": dict(
            sorted(Counter(handoff["human_review_status"] for handoff in handoffs).items())
        ),
        "rights_decision_status_counts": dict(
            sorted(Counter(handoff["rights_decision_status"] for handoff in handoffs).items())
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
    parser = argparse.ArgumentParser(description="Build source pipeline missing-evidence review handoff scaffold.")
    parser.add_argument("--route-pack", default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_ROUTE_PACK))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_handoff_scaffold(read_json(root / args.route_pack))
    write_json(root / args.output, data)
    print(f"missing_evidence_review_handoffs={data['handoff_count']} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
