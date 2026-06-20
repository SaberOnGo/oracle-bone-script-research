#!/usr/bin/env python3
"""Build an assignment plan for core-corpus phase gap outcome routes.

The plan groups the 208 route-summary rows into phase-status review waves for
navigation only. It does not assign reviewers, collect evidence, record
reviewed outcomes, decide rights, promote sources or candidates, import corpus
rows, or make identity, component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY = (
    STAT_DIR / "208_core-corpus-phase-gap-review-outcome-handoff-route-summary.json"
)
DEFAULT_OUTPUT = STAT_DIR / "209_core-corpus-phase-gap-review-outcome-assignment-plan.json"

UPDATED_AT = "2026-06-20"
PHASE_STATUS_ORDER = ["missing", "mixed_or_partial"]
REVIEW_PRIORITY_ORDER = ["high_batch_review", "targeted_review", "graph_derivative_boundary_review"]
ASSIGNMENT_STATUS = "planned_not_assigned"
HANDOFF_READINESS_STATUS = "planned_for_core_corpus_phase_gap_outcome_review"
AUTOMATION_BOUNDARY = "assignment_plan_only_no_core_corpus_phase_gap_outcome_capture"
RESEARCH_BOUNDARY = "core_corpus_phase_gap_review_outcome_assignment_plan_not_scholarship"
CAUTION = (
    "This core corpus phase gap review outcome assignment plan is routing-only. "
    "It is not collected evidence, not a reviewed outcome, not a rights decision, "
    "not source or candidate promotion, not a corpus import, not an identity claim, "
    "not a component assignment, not an evolution-chain assignment, and not a "
    "decipherment conclusion."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def unique_sorted(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def ordered_index(value: object, order: list[str]) -> int:
    text = str(value)
    try:
        return order.index(text)
    except ValueError:
        return len(order)


def route_sort_key(route: dict[str, object]) -> tuple[int, int, str, str]:
    return (
        ordered_index(route.get("phase_status", ""), PHASE_STATUS_ORDER),
        ordered_index(route.get("review_priority", ""), REVIEW_PRIORITY_ORDER),
        str(route.get("corpus_area", "")),
        str(route.get("summary_route_id", "")),
    )


def assignment_item(index: int, route: dict[str, object]) -> dict[str, object]:
    route_files = unique_sorted(
        list(route.get("checklist_files_to_open", []))
        + list(route.get("handoff_files_to_open", []))
        + list(route.get("route_files_to_open", []))
    )
    return {
        "assignment_plan_item_id": f"core-corpus-phase-gap-review-outcome-assignment-{index:03d}",
        "summary_route_id": route["summary_route_id"],
        "outcome_handoff_checklist_id": route["outcome_handoff_checklist_id"],
        "outcome_handoff_id": route["outcome_handoff_id"],
        "outcome_route_id": route["outcome_route_id"],
        "core_corpus_phase_gap_review_outcome_scaffold_id": route[
            "core_corpus_phase_gap_review_outcome_scaffold_id"
        ],
        "handoff_review_checklist_id": route["handoff_review_checklist_id"],
        "handoff_id": route["handoff_id"],
        "review_route_id": route["review_route_id"],
        "review_index_id": route["review_index_id"],
        "gap_queue_id": route["gap_queue_id"],
        "source_phase_row_id": route["source_phase_row_id"],
        "corpus_area": route["corpus_area"],
        "label_en": route["label_en"],
        "phase_name": route["phase_name"],
        "phase_status": route["phase_status"],
        "gap_type": route["gap_type"],
        "review_priority": route["review_priority"],
        "specialized_checklist_family": route["specialized_checklist_family"],
        "specialized_checklist_id": route["specialized_checklist_id"],
        "specialized_checklist_path": route["specialized_checklist_path"],
        "coverage_status": route["coverage_status"],
        "recommended_action": route["recommended_action"],
        "candidate_or_staging_boundary": route["candidate_or_staging_boundary"],
        "route_summary_path": CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY.as_posix(),
        "previous_route_summary_path": route["route_summary_path"],
        "outcome_handoff_checklist_path": route["outcome_handoff_checklist_path"],
        "outcome_handoff_scaffold_path": route["outcome_handoff_scaffold_path"],
        "outcome_route_pack_path": route["outcome_route_pack_path"],
        "outcome_scaffold_path": route["outcome_scaffold_path"],
        "outcome_update_target_path": route["outcome_update_target_path"],
        "checklist_update_target_path": route["checklist_update_target_path"],
        "handoff_review_checklist_path": route["handoff_review_checklist_path"],
        "handoff_scaffold_path": route["handoff_scaffold_path"],
        "previous_route_pack_path": route["previous_route_pack_path"],
        "review_index_path": route["review_index_path"],
        "route_files_to_open": route_files,
        "route_file_count": len(route_files),
        "required_review_steps": list(route.get("required_review_steps", [])),
        "required_precheck_steps": list(route.get("required_precheck_steps", [])),
        "reserved_outcome_fields": list(route.get("reserved_outcome_fields", [])),
        "assignment_status": ASSIGNMENT_STATUS,
        "handoff_readiness_status": HANDOFF_READINESS_STATUS,
        "handoff_review_status": route["handoff_review_status"],
        "handoff_status": route["handoff_status"],
        "route_status": route["route_status"],
        "review_outcome_status": route["review_outcome_status"],
        "evidence_collection_status": route["evidence_collection_status"],
        "human_review_status": route["human_review_status"],
        "rights_decision_status": route["rights_decision_status"],
        "source_promotion_status": route["source_promotion_status"],
        "corpus_import_status": route["corpus_import_status"],
        "decipherment_claim_status": route["decipherment_claim_status"],
        "identity_claim_status": route["identity_claim_status"],
        "component_claim_status": route["component_claim_status"],
        "evolution_claim_status": route["evolution_claim_status"],
        "phase_gap_outcome_reviewed": route["phase_gap_outcome_reviewed"],
        "specialized_checklist_outcome_reviewed": route["specialized_checklist_outcome_reviewed"],
        "reviewed_evidence_paths": route["reviewed_evidence_paths"],
        "reviewed_outcome_summary": route["reviewed_outcome_summary"],
        "reviewed_rights_decision": route["reviewed_rights_decision"],
        "reviewed_source_or_candidate_promotion": route["reviewed_source_or_candidate_promotion"],
        "reviewed_corpus_import": route["reviewed_corpus_import"],
        "reviewed_decipherment_claim": route["reviewed_decipherment_claim"],
        "required_followup_reviewed": route["required_followup_reviewed"],
        "human_reviewer_id": route["human_reviewer_id"],
        "human_review_date": route["human_review_date"],
        "human_review_notes": route["human_review_notes"],
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
    }


def wave_from_items(wave_index: int, phase_status: str, items: list[dict[str, object]]) -> dict[str, object]:
    route_files = unique_sorted([route_file for item in items for route_file in item["route_files_to_open"]])
    return {
        "assignment_wave_id": f"core-corpus-phase-gap-review-outcome-assignment-wave-{wave_index:03d}",
        "phase_status": phase_status,
        "priority_rank": str(wave_index),
        "assignment_item_count": len(items),
        "assignment_plan_item_ids": [str(item["assignment_plan_item_id"]) for item in items],
        "summary_route_ids": [str(item["summary_route_id"]) for item in items],
        "gap_queue_ids": [str(item["gap_queue_id"]) for item in items],
        "corpus_areas": unique_sorted([str(item["corpus_area"]) for item in items]),
        "specialized_checklist_families": unique_sorted(
            [str(item["specialized_checklist_family"]) for item in items]
        ),
        "review_priorities": unique_sorted([str(item["review_priority"]) for item in items]),
        "route_file_count": len(route_files),
        "route_files_to_open": route_files,
        "assignment_status": ASSIGNMENT_STATUS,
        "handoff_readiness_status": HANDOFF_READINESS_STATUS,
        "review_outcome_status": "not_started",
        "evidence_collection_status": "not_collected",
        "rights_decision_status": "no_rights_decision",
        "source_promotion_status": "not_promoted",
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
    routes = sorted(list(route_summary.get("routes", [])), key=route_sort_key)
    items = [assignment_item(index, route) for index, route in enumerate(routes, start=1)]
    waves = [
        wave_from_items(wave_index, phase_status, [item for item in items if item["phase_status"] == phase_status])
        for wave_index, phase_status in enumerate(PHASE_STATUS_ORDER, start=1)
        if any(item["phase_status"] == phase_status for item in items)
    ]
    corpus_area_workstreams = []
    for corpus_area in unique_sorted([str(item["corpus_area"]) for item in items]):
        area_items = [item for item in items if item["corpus_area"] == corpus_area]
        corpus_area_workstreams.append(
            {
                "corpus_area": corpus_area,
                "assignment_item_count": len(area_items),
                "assignment_plan_item_ids": [str(item["assignment_plan_item_id"]) for item in area_items],
                "summary_route_ids": [str(item["summary_route_id"]) for item in area_items],
                "phase_statuses": unique_sorted([str(item["phase_status"]) for item in area_items]),
                "specialized_checklist_families": unique_sorted(
                    [str(item["specialized_checklist_family"]) for item in area_items]
                ),
                "route_file_count": len(
                    unique_sorted([route_file for item in area_items for route_file in item["route_files_to_open"]])
                ),
            }
        )
    return {
        "assignment_plan_id": "core-corpus-phase-gap-review-outcome-assignment-plan-001",
        "updated_at": UPDATED_AT,
        "route_summary_path": CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY.as_posix(),
        "upstream_route_summary_id": route_summary.get("route_summary_id", ""),
        "assignment_item_count": len(items),
        "assignment_wave_count": len(waves),
        "corpus_area_workstream_count": len(corpus_area_workstreams),
        "corpus_area_count": len(corpus_area_workstreams),
        "specialized_checklist_family_count": len(
            {str(item["specialized_checklist_family"]) for item in items}
        ),
        "phase_status_counts": dict(sorted(Counter(item["phase_status"] for item in items).items())),
        "corpus_area_counts": dict(sorted(Counter(item["corpus_area"] for item in items).items())),
        "specialized_checklist_family_counts": dict(
            sorted(Counter(item["specialized_checklist_family"] for item in items).items())
        ),
        "assignment_status_counts": dict(sorted(Counter(item["assignment_status"] for item in items).items())),
        "handoff_readiness_status_counts": dict(
            sorted(Counter(item["handoff_readiness_status"] for item in items).items())
        ),
        "review_outcome_status_counts": dict(sorted(Counter(item["review_outcome_status"] for item in items).items())),
        "human_review_status_counts": dict(sorted(Counter(item["human_review_status"] for item in items).items())),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "assignment_waves": waves,
        "corpus_area_workstreams": corpus_area_workstreams,
        "assignment_items": items,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build core corpus phase gap outcome assignment plan.")
    parser.add_argument(
        "--route-summary",
        default=str(CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_assignment_plan(read_json(root / args.route_summary))
    write_json(root / args.output, data)
    print(
        f"core_corpus_phase_gap_review_outcome_assignment_items={data['assignment_item_count']} "
        f"assignment_waves={data['assignment_wave_count']} output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
