#!/usr/bin/env python3
"""Build a precheck handoff scaffold for core-corpus phase gap routes.

The scaffold wraps the 200 route pack as human-review handoff rows. It does
not collect evidence, record reviewed outcomes, decide rights, promote sources
or candidates, import corpus rows, or make decipherment claims.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CORE_CORPUS_PHASE_GAP_REVIEW_ROUTE_PACK = STAT_DIR / "200_core-corpus-phase-gap-review-route-pack.json"
DEFAULT_OUTPUT = STAT_DIR / "201_core-corpus-phase-gap-review-handoff-scaffold.json"
UPDATED_AT = "2026-06-20"
HANDOFF_STATUS = "not_started"
HUMAN_REVIEW_STATUS = "pending_human_review"
AUTOMATION_BOUNDARY = "handoff_precheck_only_no_core_corpus_phase_gap_outcome_capture"
RESEARCH_BOUNDARY = "core_corpus_phase_gap_review_handoff_scaffold_not_scholarship"
CAUTION = (
    "This core corpus phase gap review handoff scaffold is precheck-only. It is "
    "not collected evidence, not a reviewed outcome, not a rights decision, not "
    "source or candidate promotion, not a corpus import, and not a decipherment "
    "conclusion."
)
REQUIRED_PRECHECK_STEPS = [
    "open_200_route_pack",
    "open_199_review_index",
    "open_specialized_review_checklist_row",
    "confirm_route_matches_gap_queue_id",
    "verify_empty_reviewed_outcome_fields_before_review",
    "do_not_collect_evidence_or_record_outcome_in_handoff",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def unique_list(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def handoff_from_route(index: int, route: dict[str, object]) -> dict[str, object]:
    route_files = [str(value) for value in route.get("route_files_to_open", [])]
    handoff_files = unique_list(
        [
            DEFAULT_OUTPUT.as_posix(),
            CORE_CORPUS_PHASE_GAP_REVIEW_ROUTE_PACK.as_posix(),
            str(route.get("review_index_path", "")),
            str(route.get("specialized_checklist_path", "")),
            *route_files,
        ]
    )
    handoff = {
        "handoff_id": f"core-corpus-phase-gap-review-handoff-{index:03d}",
        "route_pack_path": CORE_CORPUS_PHASE_GAP_REVIEW_ROUTE_PACK.as_posix(),
        "handoff_status": HANDOFF_STATUS,
        "human_review_status": HUMAN_REVIEW_STATUS,
        "handoff_objective": "open_core_corpus_phase_gap_route_and_confirm_precheck_fields_before_later_human_review",
    }
    handoff.update(route)
    handoff["route_pack_path"] = CORE_CORPUS_PHASE_GAP_REVIEW_ROUTE_PACK.as_posix()
    handoff["handoff_files_to_open"] = handoff_files
    handoff["required_precheck_steps"] = REQUIRED_PRECHECK_STEPS
    handoff["handoff_status"] = HANDOFF_STATUS
    handoff["human_review_status"] = HUMAN_REVIEW_STATUS
    handoff["reviewed_evidence_paths"] = ""
    handoff["reviewed_outcome_summary"] = ""
    handoff["reviewed_rights_decision"] = ""
    handoff["reviewed_source_or_candidate_promotion"] = ""
    handoff["reviewed_corpus_import"] = ""
    handoff["reviewed_decipherment_claim"] = ""
    handoff["automation_boundary"] = AUTOMATION_BOUNDARY
    handoff["research_boundary"] = RESEARCH_BOUNDARY
    handoff["caution"] = CAUTION
    return handoff


def build_handoff_scaffold(route_pack: dict[str, object]) -> dict[str, object]:
    routes = route_pack.get("routes", [])
    handoffs = [handoff_from_route(index, route) for index, route in enumerate(routes, start=1)]
    return {
        "handoff_scaffold_id": "core-corpus-phase-gap-review-handoff-scaffold-001",
        "updated_at": UPDATED_AT,
        "route_pack_path": CORE_CORPUS_PHASE_GAP_REVIEW_ROUTE_PACK.as_posix(),
        "handoff_scaffold_path": DEFAULT_OUTPUT.as_posix(),
        "handoff_count": len(handoffs),
        "route_count": route_pack["route_count"],
        "gap_count": route_pack["gap_count"],
        "corpus_area_count": route_pack["corpus_area_count"],
        "specialized_checklist_family_count": route_pack["specialized_checklist_family_count"],
        "specialized_checklist_family_counts": route_pack["specialized_checklist_family_counts"],
        "corpus_area_counts": route_pack["corpus_area_counts"],
        "route_status_counts": route_pack["route_status_counts"],
        "handoff_status_counts": dict(sorted(Counter(handoff["handoff_status"] for handoff in handoffs).items())),
        "review_status_counts": dict(sorted(Counter(handoff["review_status"] for handoff in handoffs).items())),
        "human_review_status_counts": dict(
            sorted(Counter(handoff["human_review_status"] for handoff in handoffs).items())
        ),
        "evidence_collection_status_counts": route_pack["evidence_collection_status_counts"],
        "rights_decision_status_counts": route_pack["rights_decision_status_counts"],
        "source_promotion_status_counts": route_pack["source_promotion_status_counts"],
        "corpus_import_status_counts": route_pack["corpus_import_status_counts"],
        "decipherment_claim_status_counts": route_pack["decipherment_claim_status_counts"],
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "handoffs": handoffs,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the core corpus phase gap review handoff scaffold.")
    parser.add_argument("--route-pack", default=str(CORE_CORPUS_PHASE_GAP_REVIEW_ROUTE_PACK))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_handoff_scaffold(read_json(root / args.route_pack))
    write_json(root / args.output, data)
    print(f"core_corpus_phase_gap_review_handoffs={data['handoff_count']} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
