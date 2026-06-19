#!/usr/bin/env python3
"""Build a wave handoff scaffold for missing-evidence outcome review routes."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ASSIGNMENT_PLAN = (
    STAT_DIR / "160_source-pipeline-phase-action-missing-evidence-review-outcome-assignment-plan.json"
)
DEFAULT_OUTPUT = STAT_DIR / "161_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-scaffold.json"

UPDATED_AT = "2026-06-19"
HANDOFF_STATUS = "ready_for_outcome_review_not_started"
AUTOMATION_BOUNDARY = "wave_handoff_scaffold_only_no_missing_evidence_outcome_capture"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_scaffold_not_scholarship"
CAUTION = (
    "This source pipeline missing-evidence review outcome wave handoff scaffold "
    "is routing-only. It is not collected evidence, not a reviewed outcome, not "
    "a rights decision, not source promotion, not a corpus import, not an "
    "identity claim, not a component assignment, not an evolution-chain "
    "assignment, and not a decipherment conclusion."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def unique_sorted(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def status_counts(items: list[dict[str, object]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(item.get(field, "")) for item in items).items()))


def handoff_item(index: int, item: dict[str, object], wave_by_item_id: dict[str, dict[str, object]]) -> dict[str, object]:
    assignment_item_id = str(item["assignment_plan_item_id"])
    wave = wave_by_item_id[assignment_item_id]
    return {
        "handoff_item_id": f"source-pipeline-missing-evidence-review-outcome-handoff-{index:03d}",
        "handoff_wave_id": str(wave["assignment_wave_id"]).replace("assignment-wave", "handoff-wave"),
        "assignment_wave_id": wave["assignment_wave_id"],
        "assignment_plan_item_id": assignment_item_id,
        "summary_route_id": item["summary_route_id"],
        "outcome_handoff_checklist_id": item["outcome_handoff_checklist_id"],
        "handoff_id_from_157": item["handoff_id"],
        "route_id": item["route_id"],
        "missing_evidence_review_outcome_scaffold_id": item["missing_evidence_review_outcome_scaffold_id"],
        "source_id": item["source_id"],
        "source_type": item["source_type"],
        "rights_status": item["rights_status"],
        "pipeline_gap_status": item["pipeline_gap_status"],
        "missing_route_count": item["missing_route_count"],
        "missing_file_role_count": item["missing_file_role_count"],
        "missing_file_roles": list(item.get("missing_file_roles", [])),
        "priority_rank": item["priority_rank"],
        "priority_tags": list(item.get("priority_tags", [])),
        "required_review_steps": list(item.get("required_review_steps", [])),
        "required_precheck_steps": list(item.get("required_precheck_steps", [])),
        "required_review_actions": list(item.get("required_review_actions", [])),
        "assignment_plan_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ASSIGNMENT_PLAN.as_posix(),
        "route_summary_path": item["route_summary_path"],
        "handoff_scaffold_path": item["handoff_scaffold_path"],
        "route_pack_path": item["route_pack_path"],
        "outcome_scaffold_path": item["outcome_scaffold_path"],
        "outcome_update_target_path": item["outcome_update_target_path"],
        "previous_handoff_route_summary_path": item["previous_handoff_route_summary_path"],
        "review_checklist_path": item["review_checklist_path"],
        "result_scaffold_path": item["result_scaffold_path"],
        "result_update_target_path": item["result_update_target_path"],
        "review_draft_manifest_path": item["review_draft_manifest_path"],
        "draft_path": item["draft_path"],
        "source_summary_path": item["source_summary_path"],
        "source_gap_route_summary_path": item["source_gap_route_summary_path"],
        "route_files_to_open": list(item.get("route_files_to_open", [])),
        "route_file_count": item["route_file_count"],
        "reserved_outcome_fields": list(item.get("reserved_outcome_fields", [])),
        "handoff_status": HANDOFF_STATUS,
        "assignment_status": item["assignment_status"],
        "handoff_readiness_status": item["handoff_readiness_status"],
        "checklist_status": item["checklist_status"],
        "route_status": item["route_status"],
        "review_outcome_status": item["review_outcome_status"],
        "evidence_collection_status": item["evidence_collection_status"],
        "reviewed_evidence_paths": item["reviewed_evidence_paths"],
        "reviewed_outcome_summary": item["reviewed_outcome_summary"],
        "remaining_blockers_reviewed": item["remaining_blockers_reviewed"],
        "required_followup_reviewed": item["required_followup_reviewed"],
        "human_review_status": item["human_review_status"],
        "rights_decision_status": item["rights_decision_status"],
        "source_promotion_status": item["source_promotion_status"],
        "corpus_import_status": item["corpus_import_status"],
        "decipherment_claim_status": item["decipherment_claim_status"],
        "identity_claim_status": item["identity_claim_status"],
        "component_claim_status": item["component_claim_status"],
        "evolution_claim_status": item["evolution_claim_status"],
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
    }


def build_wave_handoff_scaffold(assignment_plan: dict[str, object]) -> dict[str, object]:
    waves = list(assignment_plan.get("assignment_waves", []))
    wave_by_item_id: dict[str, dict[str, object]] = {}
    handoff_waves = []
    for index, wave in enumerate(waves, start=1):
        item_ids = [str(item_id) for item_id in wave.get("assignment_plan_item_ids", [])]
        for item_id in item_ids:
            wave_by_item_id[item_id] = wave
        handoff_waves.append(
            {
                "handoff_wave_id": f"source-pipeline-missing-evidence-review-outcome-handoff-wave-{index:03d}",
                "assignment_wave_id": wave["assignment_wave_id"],
                "pipeline_gap_status": wave["pipeline_gap_status"],
                "priority_rank": wave["priority_rank"],
                "handoff_item_count": wave["assignment_item_count"],
                "assignment_plan_item_ids": item_ids,
                "summary_route_ids": list(wave.get("summary_route_ids", [])),
                "source_ids": list(wave.get("source_ids", [])),
                "route_files_to_open": list(wave.get("route_files_to_open", [])),
                "route_file_count": wave["route_file_count"],
                "handoff_status": HANDOFF_STATUS,
                "assignment_status": wave["assignment_status"],
                "handoff_readiness_status": wave["handoff_readiness_status"],
                "review_outcome_status": wave["review_outcome_status"],
                "evidence_collection_status": wave["evidence_collection_status"],
                "rights_decision_status": wave["rights_decision_status"],
                "source_promotion_status": wave["source_promotion_status"],
                "corpus_import_status": wave["corpus_import_status"],
                "decipherment_claim_status": wave["decipherment_claim_status"],
            }
        )

    assignment_items = list(assignment_plan.get("assignment_items", []))
    handoff_items = [
        handoff_item(index, item, wave_by_item_id)
        for index, item in enumerate(assignment_items, start=1)
    ]
    route_files = unique_sorted(
        [route_file for item in handoff_items for route_file in list(item["route_files_to_open"])]
    )
    return {
        "handoff_scaffold_id": "source-pipeline-missing-evidence-review-outcome-wave-handoff-scaffold-001",
        "updated_at": UPDATED_AT,
        "assignment_plan_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ASSIGNMENT_PLAN.as_posix(),
        "upstream_assignment_plan_id": assignment_plan.get("assignment_plan_id", ""),
        "handoff_item_count": len(handoff_items),
        "handoff_wave_count": len(handoff_waves),
        "source_count": len({item["source_id"] for item in handoff_items}),
        "route_file_reference_count": sum(int(item["route_file_count"]) for item in handoff_items),
        "unique_route_file_count": len(route_files),
        "pipeline_gap_status_counts": dict(sorted(Counter(item["pipeline_gap_status"] for item in handoff_items).items())),
        "handoff_status_counts": status_counts(handoff_items, "handoff_status"),
        "assignment_status_counts": status_counts(handoff_items, "assignment_status"),
        "review_outcome_status_counts": status_counts(handoff_items, "review_outcome_status"),
        "human_review_status_counts": status_counts(handoff_items, "human_review_status"),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "route_files_to_open": route_files,
        "handoff_waves": handoff_waves,
        "handoff_items": handoff_items,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build missing-evidence outcome wave handoff scaffold.")
    parser.add_argument("--assignment-plan", default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ASSIGNMENT_PLAN))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_wave_handoff_scaffold(read_json(root / args.assignment_plan))
    write_json(root / args.output, data)
    print(
        f"missing_evidence_outcome_handoff_items={data['handoff_item_count']} "
        f"handoff_waves={data['handoff_wave_count']} output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
