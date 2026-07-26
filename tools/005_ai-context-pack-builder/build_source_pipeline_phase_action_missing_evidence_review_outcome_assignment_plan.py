#!/usr/bin/env python3
"""Build an assignment plan for missing-evidence outcome review routes.

The plan groups the 159 route-summary rows into planned review waves. It does
not assign reviewers, collect evidence, record outcomes, decide rights, promote
sources, import corpus rows, or make identity, component, evolution, or
decipherment claims.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY = (
    STAT_DIR / "159_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-route-summary.json"
)
DEFAULT_OUTPUT = STAT_DIR / "160_source-pipeline-phase-action-missing-evidence-review-outcome-assignment-plan.json"

UPDATED_AT = "2026-06-19"
GAP_ORDER = [
    "needs_download_or_access_review",
    "needs_access_boundary_review",
    "needs_field_map_review",
    "needs_package_manifest_review",
    "needs_safe_derived_record_review",
    "ready_for_source_engineering_review",
]
ASSIGNMENT_STATUS = "planned_not_assigned"
HANDOFF_READINESS_STATUS = "planned_for_outcome_review_handoff"
AUTOMATION_BOUNDARY = "assignment_plan_only_no_missing_evidence_outcome_capture"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_missing_evidence_review_outcome_assignment_plan_not_scholarship"
CAUTION = (
    "This source pipeline missing-evidence review outcome assignment plan is "
    "routing-only. It is not collected evidence, not a reviewed outcome, not a "
    "rights decision, not source promotion, not a corpus import, not an identity "
    "claim, not a component assignment, not an evolution-chain assignment, and "
    "not a decipherment conclusion."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def unique_sorted(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def gap_index(route: dict[str, object]) -> tuple[int, int, str]:
    gap_status = str(route.get("pipeline_gap_status", ""))
    try:
        gap_rank = GAP_ORDER.index(gap_status)
    except ValueError:
        gap_rank = len(GAP_ORDER)
    try:
        priority_rank = int(str(route.get("priority_rank", "999999")))
    except ValueError:
        priority_rank = 999999
    return gap_rank, priority_rank, str(route.get("source_id", ""))


def assignment_item(index: int, route: dict[str, object]) -> dict[str, object]:
    route_files = list(route.get("outcome_handoff_files_to_open", []))
    return {
        "assignment_plan_item_id": f"source-pipeline-missing-evidence-review-outcome-assignment-{index:03d}",
        "summary_route_id": route["summary_route_id"],
        "outcome_handoff_checklist_id": route["outcome_handoff_checklist_id"],
        "handoff_id": route["handoff_id"],
        "route_id": route["route_id"],
        "missing_evidence_review_outcome_scaffold_id": route["missing_evidence_review_outcome_scaffold_id"],
        "source_id": route["source_id"],
        "source_type": route["source_type"],
        "rights_status": route["rights_status"],
        "pipeline_gap_status": route["pipeline_gap_status"],
        "missing_route_count": route["missing_route_count"],
        "missing_file_role_count": route["missing_file_role_count"],
        "missing_file_roles": list(route.get("missing_file_roles", [])),
        "priority_rank": route["priority_rank"],
        "priority_tags": list(route.get("priority_tags", [])),
        "required_review_steps": list(route.get("required_review_steps", [])),
        "required_precheck_steps": list(route.get("required_precheck_steps", [])),
        "required_review_actions": list(route.get("required_review_actions", [])),
        "route_summary_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY.as_posix(),
        "handoff_scaffold_path": route["handoff_scaffold_path"],
        "route_pack_path": route["route_pack_path"],
        "outcome_scaffold_path": route["outcome_scaffold_path"],
        "outcome_update_target_path": route["outcome_update_target_path"],
        "previous_handoff_route_summary_path": route["route_summary_path"],
        "review_checklist_path": route["review_checklist_path"],
        "result_scaffold_path": route["result_scaffold_path"],
        "result_update_target_path": route["result_update_target_path"],
        "review_draft_manifest_path": route["review_draft_manifest_path"],
        "draft_path": route["draft_path"],
        "source_summary_path": route["source_summary_path"],
        "source_gap_route_summary_path": route["source_gap_route_summary_path"],
        "route_files_to_open": route_files,
        "route_file_count": len(route_files),
        "reserved_outcome_fields": list(route.get("reserved_outcome_fields", [])),
        "assignment_status": ASSIGNMENT_STATUS,
        "handoff_readiness_status": HANDOFF_READINESS_STATUS,
        "checklist_status": route["checklist_status"],
        "handoff_status": route["handoff_status"],
        "route_status": route["route_status"],
        "review_outcome_status": route["review_outcome_status"],
        "evidence_collection_status": route["evidence_collection_status"],
        "reviewed_evidence_paths": route["reviewed_evidence_paths"],
        "reviewed_outcome_summary": route["reviewed_outcome_summary"],
        "remaining_blockers_reviewed": route["remaining_blockers_reviewed"],
        "required_followup_reviewed": route["required_followup_reviewed"],
        "human_review_status": route["human_review_status"],
        "rights_decision_status": route["rights_decision_status"],
        "source_promotion_status": route["source_promotion_status"],
        "corpus_import_status": route["corpus_import_status"],
        "decipherment_claim_status": route["decipherment_claim_status"],
        "identity_claim_status": route["identity_claim_status"],
        "component_claim_status": route["component_claim_status"],
        "evolution_claim_status": route["evolution_claim_status"],
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
    }


def build_assignment_plan(route_summary: dict[str, object]) -> dict[str, object]:
    routes = sorted(list(route_summary.get("routes", [])), key=gap_index)
    items = [assignment_item(index, route) for index, route in enumerate(routes, start=1)]
    waves: list[dict[str, object]] = []
    for wave_index, gap_status in enumerate(GAP_ORDER, start=1):
        wave_items = [item for item in items if item["pipeline_gap_status"] == gap_status]
        if not wave_items:
            continue
        route_files = unique_sorted(
            [route_file for item in wave_items for route_file in item["route_files_to_open"]]
        )
        waves.append(
            {
                "assignment_wave_id": f"source-pipeline-missing-evidence-review-outcome-assignment-wave-{wave_index:03d}",
                "pipeline_gap_status": gap_status,
                "priority_rank": str(wave_index),
                "assignment_item_count": len(wave_items),
                "assignment_plan_item_ids": [str(item["assignment_plan_item_id"]) for item in wave_items],
                "summary_route_ids": [str(item["summary_route_id"]) for item in wave_items],
                "source_ids": [str(item["source_id"]) for item in wave_items],
                "route_file_count": len(route_files),
                "route_files_to_open": route_files,
                "assignment_status": ASSIGNMENT_STATUS,
                "handoff_readiness_status": HANDOFF_READINESS_STATUS,
                "review_outcome_status": "not_started",
                "evidence_collection_status": "not_collected",
                "rights_decision_status": "no_new_rights_decision",
                "source_promotion_status": "not_promoted",
                "corpus_import_status": "not_imported",
                "decipherment_claim_status": "no_decipherment_claim",
            }
        )

    source_workstreams = []
    for source_id in unique_sorted([str(item["source_id"]) for item in items]):
        source_items = [item for item in items if item["source_id"] == source_id]
        source_workstreams.append(
            {
                "source_id": source_id,
                "assignment_item_count": len(source_items),
                "assignment_plan_item_ids": [str(item["assignment_plan_item_id"]) for item in source_items],
                "summary_route_ids": [str(item["summary_route_id"]) for item in source_items],
                "pipeline_gap_statuses": unique_sorted([str(item["pipeline_gap_status"]) for item in source_items]),
                "route_file_count": len(
                    unique_sorted([route_file for item in source_items for route_file in item["route_files_to_open"]])
                ),
            }
        )

    return {
        "assignment_plan_id": "source-pipeline-missing-evidence-review-outcome-assignment-plan-001",
        "updated_at": UPDATED_AT,
        "route_summary_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY.as_posix(),
        "upstream_route_summary_id": route_summary.get("route_summary_id", ""),
        "assignment_item_count": len(items),
        "assignment_wave_count": len(waves),
        "source_workstream_count": len(source_workstreams),
        "source_count": len(source_workstreams),
        "pipeline_gap_status_counts": dict(sorted(Counter(item["pipeline_gap_status"] for item in items).items())),
        "assignment_status_counts": dict(sorted(Counter(item["assignment_status"] for item in items).items())),
        "handoff_readiness_status_counts": dict(sorted(Counter(item["handoff_readiness_status"] for item in items).items())),
        "review_outcome_status_counts": dict(sorted(Counter(item["review_outcome_status"] for item in items).items())),
        "human_review_status_counts": dict(sorted(Counter(item["human_review_status"] for item in items).items())),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "assignment_waves": waves,
        "source_workstreams": source_workstreams,
        "assignment_items": items,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source pipeline missing-evidence outcome assignment plan.")
    parser.add_argument(
        "--route-summary",
        default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_assignment_plan(read_json(root / args.route_summary))
    write_json(root / args.output, data)
    print(
        f"missing_evidence_outcome_assignment_items={data['assignment_item_count']} "
        f"assignment_waves={data['assignment_wave_count']} output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
