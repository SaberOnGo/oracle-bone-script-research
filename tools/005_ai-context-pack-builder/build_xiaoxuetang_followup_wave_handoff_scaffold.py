#!/usr/bin/env python3
"""Build a first-wave handoff scaffold for Xiaoxuetang follow-up review tasks."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


ASSIGNMENT_PLAN = Path(
    "corpus/009_statistics-and-derived-features/"
    "078_ai-agent-xiaoxuetang-followup-assignment-plan.json"
)
REVIEW_ROUTE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/"
    "077_ai-agent-xiaoxuetang-followup-review-route-summary.json"
)
ROUTE_PACK = Path(
    "corpus/009_statistics-and-derived-features/"
    "076_ai-agent-xiaoxuetang-followup-route-pack.json"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "079_ai-agent-xiaoxuetang-followup-wave-handoff-scaffold.json"
)
UPDATED_AT = "2026-06-11"
TARGET_WAVE_ID = "xxt-followup-assignment-wave-001"
TARGET_FAMILY_ID = "xxt_jgw_tls_access_boundary_followup"
STATUS = "draft_wave_handoff_scaffold_not_started"
RESEARCH_BOUNDARY = "xxt_followup_wave_handoff_scaffold_not_scholarship"
OUTPUT_SCOPE = "xiaoxuetang_followup_wave_handoff_scaffold_only"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _unique_sorted(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def _status_counts(items: list[dict[str, object]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(item.get(key, "")) for item in items).items()))


def _handoff_item(item: dict[str, object], wave: dict[str, object]) -> dict[str, object]:
    route_files = list(item.get("route_files_to_open", []))
    review_sections = list(item.get("required_review_sections", []))
    next_checks = list(item.get("required_next_checks", []))
    return {
        "handoff_item_id": str(item["assignment_plan_item_id"]).replace(
            "assignment", "handoff"
        ),
        "assignment_wave_id": wave["assignment_wave_id"],
        "assignment_plan_item_id": item["assignment_plan_item_id"],
        "followup_task_id": item["followup_task_id"],
        "followup_family_id": item["followup_family_id"],
        "followup_family_label": item["followup_family_label"],
        "priority_rank": item["priority_rank"],
        "priority_bucket": item["priority_bucket"],
        "followup_method": item["followup_method"],
        "route_source_id": item["route_source_id"],
        "target_source_id": item["target_source_id"],
        "unknown_candidate_id": item["unknown_candidate_id"],
        "primary_external_ref_id": item["primary_external_ref_id"],
        "targeted_download_id": item["targeted_download_id"],
        "targeted_url": item["targeted_url"],
        "artifact_kind": item["artifact_kind"],
        "review_log_draft_id": item["review_log_draft_id"],
        "review_log_draft_path": item["review_log_draft_path"],
        "source_queue_path": item["source_queue_path"],
        "assignment_status": item["assignment_status"],
        "handoff_status": "ready_for_xxt_jgw_followup_not_started",
        "handoff_readiness_status": item["handoff_readiness_status"],
        "official_access_boundary_status": item["official_access_boundary_status"],
        "required_review_sections": review_sections,
        "required_review_check_count": len(review_sections),
        "required_next_checks": next_checks,
        "required_next_check_count": len(next_checks),
        "route_files_to_open": route_files,
        "route_file_count": len(route_files),
        "route_file_review_status": item["route_file_review_status"],
        "evidence_collection_status": item["evidence_collection_status"],
        "human_review_status": item["human_review_status"],
        "formal_schema_compatibility_status": item[
            "formal_schema_compatibility_status"
        ],
        "rights_decision_status": "not_decided",
        "source_promotion_status": item["source_promotion_status"],
        "identity_claim_status": item["identity_claim_status"],
        "assignment_scope_status": item["assignment_scope_status"],
        "decipherment_claim_status": item["decipherment_claim_status"],
        "component_claim_status": item["component_claim_status"],
        "evolution_chain_claim_status": item["evolution_chain_claim_status"],
        "assignment_plan_path": ASSIGNMENT_PLAN.as_posix(),
        "review_route_summary_path": REVIEW_ROUTE_SUMMARY.as_posix(),
        "route_pack_path": ROUTE_PACK.as_posix(),
        "research_boundary": RESEARCH_BOUNDARY,
        "output_scope": OUTPUT_SCOPE,
        "followup_capture_status": "not_collected",
        "catalog_claim_status": "no_claim",
        "collection_match_status": "no_claim",
        "rights_status": item["rights_status"],
        "risk_note": item["risk_note"],
        "caution": (
            "This handoff row only opens the first Xiaoxuetang JGW follow-up wave for "
            "later manual-browser or institutional-export review. It is not collected "
            "evidence, not a rights decision, not a catalog or collection match, not a "
            "formal assignment, and not a decipherment conclusion."
        ),
    }


def build_wave_handoff_scaffold(assignment_plan: dict[str, object]) -> dict[str, object]:
    waves = list(assignment_plan.get("assignment_waves", []))
    target_waves = [
        wave
        for wave in waves
        if wave.get("assignment_wave_id") == TARGET_WAVE_ID
        and wave.get("followup_family_id") == TARGET_FAMILY_ID
    ]
    if len(target_waves) != 1:
        raise ValueError("expected exactly one first Xiaoxuetang JGW assignment wave")
    wave = target_waves[0]

    target_ids = set(wave.get("assignment_plan_item_ids", []))
    items = [
        item
        for item in list(assignment_plan.get("assignment_items", []))
        if item.get("assignment_plan_item_id") in target_ids
    ]
    items.sort(key=lambda item: int(item["priority_rank"]))
    if len(items) != len(target_ids):
        raise ValueError("assignment plan does not contain every first-wave item")

    handoff_items = [_handoff_item(item, wave) for item in items]
    unique_route_files = _unique_sorted(
        [
            route_file
            for item in handoff_items
            for route_file in item["route_files_to_open"]
        ]
    )
    unique_review_sections = _unique_sorted(
        [
            section
            for item in handoff_items
            for section in item["required_review_sections"]
        ]
    )
    unique_next_checks = _unique_sorted(
        [
            check
            for item in handoff_items
            for check in item["required_next_checks"]
        ]
    )

    return {
        "context_pack_id": "ai-context-xiaoxuetang-followup-wave-handoff-001",
        "title": "Xiaoxuetang Follow-up Wave Handoff Scaffold",
        "title_zh": "小学堂后续复核首波交接脚手架",
        "status": STATUS,
        "updated_at": UPDATED_AT,
        "generated_from": [
            ASSIGNMENT_PLAN.as_posix(),
            REVIEW_ROUTE_SUMMARY.as_posix(),
            ROUTE_PACK.as_posix(),
        ],
        "purpose": (
            "Open the first Xiaoxuetang follow-up assignment wave from the 078 plan for "
            "future JGW manual-browser or institutional-export review. This scaffold only "
            "lists handoff items and required files; it does not collect evidence, assign "
            "an owner, decide rights, confirm catalogs or collections, or make decipherment claims."
        ),
        "purpose_zh": (
            "从 078 计划中打开第一波小学堂后续复核任务，供后续 JGW 人工浏览器或机构导出复核使用。"
            "本脚手架只列出交接项和必开文件，不采集证据，不分派 owner，不做权利判断，"
            "不确认著录或馆藏，也不做释读判断。"
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "output_scope": OUTPUT_SCOPE,
        "upstream_context_pack_id": assignment_plan.get("context_pack_id", ""),
        "handoff_scope": {
            "assignment_wave_id": wave["assignment_wave_id"],
            "followup_family_id": wave["followup_family_id"],
            "followup_family_label": wave["followup_family_label"],
            "priority_rank": wave["priority_rank"],
            "assignment_plan_item_ids": wave["assignment_plan_item_ids"],
            "followup_task_ids": wave["followup_task_ids"],
            "target_source_ids": wave["target_source_ids"],
            "targeted_download_ids": wave["targeted_download_ids"],
            "handoff_status": "ready_for_xxt_jgw_followup_not_started",
            "assignment_status": wave["assignment_status"],
            "evidence_collection_status": wave["evidence_collection_status"],
            "source_promotion_status": wave["source_promotion_status"],
            "decipherment_claim_status": wave["decipherment_claim_status"],
        },
        "coverage": {
            "handoff_item_count": len(handoff_items),
            "assignment_wave_count": 1,
            "review_task_count": len(handoff_items),
            "followup_family_count": 1,
            "target_source_count": len({item["target_source_id"] for item in handoff_items}),
            "route_file_reference_count": sum(
                len(item["route_files_to_open"]) for item in handoff_items
            ),
            "unique_route_file_count": len(unique_route_files),
            "required_review_section_count": len(unique_review_sections),
            "required_next_check_count": len(unique_next_checks),
            "followup_family_counts": {
                TARGET_FAMILY_ID: len(handoff_items),
            },
            "target_source_counts": dict(
                sorted(Counter(str(item["target_source_id"]) for item in handoff_items).items())
            ),
            "handoff_status_counts": _status_counts(handoff_items, "handoff_status"),
            "assignment_status_counts": _status_counts(handoff_items, "assignment_status"),
            "evidence_collection_status_counts": _status_counts(
                handoff_items, "evidence_collection_status"
            ),
            "human_review_status_counts": _status_counts(
                handoff_items, "human_review_status"
            ),
            "catalog_claim_status_counts": _status_counts(
                handoff_items, "catalog_claim_status"
            ),
            "collection_match_status_counts": _status_counts(
                handoff_items, "collection_match_status"
            ),
            "rights_decision_status_counts": _status_counts(
                handoff_items, "rights_decision_status"
            ),
        },
        "route_files_to_open": unique_route_files,
        "required_review_sections": unique_review_sections,
        "required_next_checks": unique_next_checks,
        "handoff_items": handoff_items,
        "agent_use_rules": [
            "Use this handoff scaffold only to open the first Xiaoxuetang JGW follow-up wave.",
            "Open the 079 handoff row, 078 plan item, 077 review summary, 076 route pack, source queue row, review-log draft, and all route files before recording any evidence.",
            "Keep every row not_collected, not_decided, and no_claim until source-marked follow-up evidence is recorded elsewhere.",
            "Do not treat this scaffold as collected evidence, a rights decision, a catalog or collection match, a formal assignment, or a decipherment conclusion.",
        ],
        "agent_use_rules_zh": [
            "本交接脚手架只能用于打开第一波小学堂 JGW 后续复核路线。",
            "记录任何证据前，必须先打开 079 交接行、078 计划项、077 review summary、076 route pack、source queue 行、review-log 草稿和全部 route files。",
            "在带来源标记的后续复核证据于其他位置记录前，每行都必须保持 not_collected、not_decided 和 no_claim。",
            "不得把本脚手架当作已采集证据、权利结论、著录或馆藏匹配、正式分配或释读结论。",
        ],
    }


def write_json(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assignment-plan", default=str(ASSIGNMENT_PLAN))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    scaffold = build_wave_handoff_scaffold(read_json(root / args.assignment_plan))
    write_json(root / args.output, scaffold)
    print(
        f"context_pack_id={scaffold['context_pack_id']} "
        f"handoff_item_count={scaffold['coverage']['handoff_item_count']} "
        f"unique_route_file_count={scaffold['coverage']['unique_route_file_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
