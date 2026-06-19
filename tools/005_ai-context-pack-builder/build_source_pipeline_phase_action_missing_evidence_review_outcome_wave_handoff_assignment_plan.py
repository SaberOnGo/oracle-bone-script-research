#!/usr/bin/env python3
"""Build an assignment plan for missing-evidence outcome wave handoff routes."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ROUTE_SUMMARY = (
    STAT_DIR / "163_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-route-summary.json"
)
DEFAULT_OUTPUT = STAT_DIR / "164_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-plan.json"

UPDATED_AT = "2026-06-19"
ASSIGNMENT_STATUS = "planned_not_assigned"
AUTOMATION_BOUNDARY = "wave_handoff_assignment_plan_only_no_missing_evidence_outcome_capture"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_plan_not_scholarship"
CAUTION = (
    "This source pipeline missing-evidence review outcome wave handoff assignment "
    "plan is routing-only. It is not collected evidence, not a reviewed outcome, "
    "not a rights decision, not source promotion, not a corpus import, not an "
    "identity claim, not a component assignment, not an evolution-chain assignment, "
    "and not a decipherment conclusion."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def unique_in_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def assignment_item(index: int, route: dict[str, object]) -> dict[str, object]:
    route_files = list(route.get("wave_handoff_files_to_open", []))
    return {
        "assignment_plan_item_id": f"source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-{index:03d}",
        "summary_route_id": route["summary_route_id"],
        "wave_handoff_checklist_id": route["wave_handoff_checklist_id"],
        "handoff_item_id": route["handoff_item_id"],
        "handoff_wave_id": route["handoff_wave_id"],
        "assignment_wave_id": route["assignment_wave_id"],
        "assignment_plan_item_id_from_160": route["assignment_plan_item_id"],
        "outcome_handoff_checklist_id": route["outcome_handoff_checklist_id"],
        "handoff_id_from_157": route["handoff_id_from_157"],
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
        "route_summary_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ROUTE_SUMMARY.as_posix(),
        "wave_handoff_checklist_path": route["wave_handoff_checklist_path"],
        "handoff_scaffold_path": route["handoff_scaffold_path"],
        "assignment_plan_path": route["assignment_plan_path"],
        "previous_route_summary_path": route["route_summary_path"],
        "previous_handoff_route_summary_path": route["previous_handoff_route_summary_path"],
        "previous_handoff_scaffold_path": route["previous_handoff_scaffold_path"],
        "route_pack_path": route["route_pack_path"],
        "outcome_scaffold_path": route["outcome_scaffold_path"],
        "outcome_update_target_path": route["outcome_update_target_path"],
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
        "handoff_status": route["handoff_status"],
        "handoff_readiness_status": route["handoff_readiness_status"],
        "checklist_status": route["checklist_status"],
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
    routes = list(route_summary.get("routes", []))
    items = [assignment_item(index, route) for index, route in enumerate(routes, start=1)]
    wave_ids = unique_in_order([str(item["handoff_wave_id"]) for item in items])
    waves = []
    for index, wave_id in enumerate(wave_ids, start=1):
        wave_items = [item for item in items if item["handoff_wave_id"] == wave_id]
        route_files = unique_in_order([path for item in wave_items for path in item["route_files_to_open"]])
        waves.append(
            {
                "assignment_wave_id": f"source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-wave-{index:03d}",
                "handoff_wave_id": wave_id,
                "pipeline_gap_status": str(wave_items[0]["pipeline_gap_status"]),
                "priority_rank": str(index),
                "assignment_item_count": len(wave_items),
                "assignment_plan_item_ids": [str(item["assignment_plan_item_id"]) for item in wave_items],
                "summary_route_ids": [str(item["summary_route_id"]) for item in wave_items],
                "source_ids": [str(item["source_id"]) for item in wave_items],
                "route_file_count": len(route_files),
                "route_files_to_open": route_files,
                "assignment_status": ASSIGNMENT_STATUS,
                "review_outcome_status": "not_started",
                "evidence_collection_status": "not_collected",
                "rights_decision_status": "no_new_rights_decision",
                "source_promotion_status": "not_promoted",
                "corpus_import_status": "not_imported",
                "decipherment_claim_status": "no_decipherment_claim",
            }
        )
    return {
        "assignment_plan_id": "source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-plan-001",
        "updated_at": UPDATED_AT,
        "route_summary_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ROUTE_SUMMARY.as_posix(),
        "upstream_route_summary_id": route_summary.get("route_summary_id", ""),
        "assignment_item_count": len(items),
        "assignment_wave_count": len(waves),
        "source_count": len({item["source_id"] for item in items}),
        "pipeline_gap_status_counts": dict(sorted(Counter(item["pipeline_gap_status"] for item in items).items())),
        "assignment_status_counts": dict(sorted(Counter(item["assignment_status"] for item in items).items())),
        "review_outcome_status_counts": dict(sorted(Counter(item["review_outcome_status"] for item in items).items())),
        "human_review_status_counts": dict(sorted(Counter(item["human_review_status"] for item in items).items())),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "assignment_waves": waves,
        "assignment_items": items,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build missing-evidence outcome wave handoff assignment plan.")
    parser.add_argument("--route-summary", default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ROUTE_SUMMARY))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_assignment_plan(read_json(root / args.route_summary))
    write_json(root / args.output, data)
    print(
        f"missing_evidence_outcome_wave_handoff_assignment_items={data['assignment_item_count']} "
        f"assignment_waves={data['assignment_wave_count']} output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
