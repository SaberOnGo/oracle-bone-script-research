#!/usr/bin/env python3
"""Build an assignment plan for Xiaoxuetang follow-up review routes."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


ROUTE_PACK = Path(
    "corpus/009_statistics-and-derived-features/"
    "076_ai-agent-xiaoxuetang-followup-route-pack.json"
)
REVIEW_ROUTE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/"
    "077_ai-agent-xiaoxuetang-followup-review-route-summary.json"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "078_ai-agent-xiaoxuetang-followup-assignment-plan.json"
)
UPDATED_AT = "2026-06-11"
FAMILY_ORDER = [
    "xxt_jgw_tls_access_boundary_followup",
    "xxt_obm_access_boundary_followup",
]
STATUS = "draft_assignment_plan_not_started"
RESEARCH_BOUNDARY = "xxt_followup_assignment_plan_not_scholarship"
OUTPUT_SCOPE = "xiaoxuetang_followup_assignment_plan_only"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _family_index(family_id: str) -> int:
    try:
        return FAMILY_ORDER.index(family_id)
    except ValueError:
        return len(FAMILY_ORDER)


def _unique_sorted(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def _assignment_item(index: int, row: dict[str, object]) -> dict[str, object]:
    route_files = list(row.get("route_files_to_open", []))
    review_sections = list(row.get("required_review_sections", []))
    next_checks = list(row.get("required_next_checks", []))
    return {
        "assignment_plan_item_id": f"xxt-followup-assignment-{index:03d}",
        "followup_task_id": row["followup_task_id"],
        "followup_family_id": row["followup_family_id"],
        "followup_family_label": row["followup_family_label"],
        "review_log_draft_id": row["review_log_draft_id"],
        "review_log_draft_path": row["review_log_draft_path"],
        "source_queue_path": row["source_queue_path"],
        "priority_rank": row["priority_rank"],
        "priority_bucket": row["priority_bucket"],
        "followup_method": row["followup_method"],
        "route_source_id": row["route_source_id"],
        "target_source_id": row["target_source_id"],
        "unknown_candidate_id": row["unknown_candidate_id"],
        "primary_external_ref_id": row["primary_external_ref_id"],
        "target_evidence_section": row["target_evidence_section"],
        "targeted_download_id": row["targeted_download_id"],
        "targeted_url": row["targeted_url"],
        "artifact_kind": row["artifact_kind"],
        "official_access_boundary_status": row["official_access_boundary_status"],
        "staging_row_count": row["staging_row_count"],
        "route_files_to_open": route_files,
        "route_file_count": len(route_files),
        "required_review_sections": review_sections,
        "required_review_check_count": len(review_sections),
        "required_next_checks": next_checks,
        "required_next_check_count": len(next_checks),
        "assignment_status": "planned_not_assigned",
        "handoff_readiness_status": "planned_for_followup_handoff",
        "route_file_review_status": row["route_file_review_status"],
        "evidence_collection_status": row["evidence_collection_status"],
        "human_review_status": row["human_review_status"],
        "formal_schema_compatibility_status": row[
            "formal_schema_compatibility_status"
        ],
        "rights_decision_status": row["rights_decision_status"],
        "source_promotion_status": row["source_promotion_status"],
        "identity_claim_status": row["identity_claim_status"],
        "assignment_scope_status": row["assignment_status"],
        "decipherment_claim_status": row["decipherment_claim_status"],
        "component_claim_status": row["component_claim_status"],
        "evolution_chain_claim_status": row["evolution_chain_claim_status"],
        "research_boundary": RESEARCH_BOUNDARY,
        "output_scope": OUTPUT_SCOPE,
        "rights_status": row["rights_status"],
        "risk_note": row["risk_note"],
        "caution": (
            "This assignment-plan item only schedules a Xiaoxuetang follow-up route for "
            "later manual-browser or institutional-export work. It is not collected "
            "evidence, not a rights decision, not a catalog or collection match, not a "
            "formal assignment, and not a decipherment conclusion."
        ),
    }


def build_assignment_plan(
    route_pack: dict[str, object],
    review_summary: dict[str, object],
) -> dict[str, object]:
    route_rows = list(route_pack.get("followup_routes", []))
    route_rows.sort(
        key=lambda row: (
            _family_index(str(row["followup_family_id"])),
            int(row["priority_rank"]),
            str(row["followup_task_id"]),
        )
    )
    assignment_items = [
        _assignment_item(index, row) for index, row in enumerate(route_rows, start=1)
    ]

    assignment_waves = []
    for wave_index, family_id in enumerate(FAMILY_ORDER, start=1):
        items = [
            item for item in assignment_items if item["followup_family_id"] == family_id
        ]
        if not items:
            continue
        route_files = _unique_sorted(
            [
                route_file
                for item in items
                for route_file in item["route_files_to_open"]
            ]
        )
        assignment_waves.append(
            {
                "assignment_wave_id": f"xxt-followup-assignment-wave-{wave_index:03d}",
                "followup_family_id": family_id,
                "followup_family_label": items[0]["followup_family_label"],
                "priority_rank": str(wave_index),
                "assignment_item_count": len(items),
                "assignment_plan_item_ids": [
                    str(item["assignment_plan_item_id"]) for item in items
                ],
                "followup_task_ids": [str(item["followup_task_id"]) for item in items],
                "target_source_ids": [str(item["target_source_id"]) for item in items],
                "targeted_download_ids": [
                    str(item["targeted_download_id"]) for item in items
                ],
                "route_file_count": len(route_files),
                "route_files_to_open": route_files,
                "assignment_status": "planned_not_assigned",
                "handoff_readiness_status": "planned_for_followup_handoff",
                "evidence_collection_status": "followup_review_not_started",
                "source_promotion_status": "not_promoted",
                "decipherment_claim_status": "no_claim",
            }
        )

    target_source_workstreams = []
    target_source_ids = _unique_sorted(
        [str(item["target_source_id"]) for item in assignment_items]
    )
    for target_source_id in target_source_ids:
        items = [
            item for item in assignment_items if item["target_source_id"] == target_source_id
        ]
        target_source_workstreams.append(
            {
                "target_source_id": target_source_id,
                "assignment_item_count": len(items),
                "assignment_plan_item_ids": [
                    str(item["assignment_plan_item_id"]) for item in items
                ],
                "followup_task_ids": [str(item["followup_task_id"]) for item in items],
                "followup_family_ids": sorted(
                    {str(item["followup_family_id"]) for item in items}
                ),
                "artifact_kinds": sorted({str(item["artifact_kind"]) for item in items}),
                "min_priority_rank": min(int(item["priority_rank"]) for item in items),
                "max_priority_rank": max(int(item["priority_rank"]) for item in items),
                "route_file_count": len(
                    _unique_sorted(
                        [
                            route_file
                            for item in items
                            for route_file in item["route_files_to_open"]
                        ]
                    )
                ),
            }
        )

    family_counts = Counter(str(item["followup_family_id"]) for item in assignment_items)
    target_source_counts = Counter(str(item["target_source_id"]) for item in assignment_items)
    artifact_kind_counts = Counter(str(item["artifact_kind"]) for item in assignment_items)
    assignment_counts = Counter(str(item["assignment_status"]) for item in assignment_items)
    readiness_counts = Counter(str(item["handoff_readiness_status"]) for item in assignment_items)
    evidence_counts = Counter(str(item["evidence_collection_status"]) for item in assignment_items)
    review_counts = Counter(str(item["human_review_status"]) for item in assignment_items)
    access_counts = Counter(
        str(item["official_access_boundary_status"]) for item in assignment_items
    )
    unique_route_files = _unique_sorted(
        [
            route_file
            for item in assignment_items
            for route_file in item["route_files_to_open"]
        ]
    )
    unique_review_sections = _unique_sorted(
        [
            section
            for item in assignment_items
            for section in item["required_review_sections"]
        ]
    )
    unique_next_checks = _unique_sorted(
        [
            check
            for item in assignment_items
            for check in item["required_next_checks"]
        ]
    )

    return {
        "context_pack_id": "ai-context-xiaoxuetang-followup-assignment-plan-001",
        "title": "Xiaoxuetang Follow-up Assignment Plan",
        "title_zh": "小学堂后续复核分派计划",
        "status": STATUS,
        "updated_at": UPDATED_AT,
        "generated_from": [
            ROUTE_PACK.as_posix(),
            REVIEW_ROUTE_SUMMARY.as_posix(),
        ],
        "purpose": (
            "Plan the next Xiaoxuetang follow-up review waves from the combined 076 route "
            "pack and 077 review summary. This plan only orders routing work for later "
            "manual-browser or institutional-export follow-up; it does not assign an owner, "
            "collect evidence, decide rights, confirm catalogs or collections, or make "
            "decipherment claims."
        ),
        "purpose_zh": (
            "依据 076 统一 route pack 和 077 review summary 规划下一步小学堂后续复核 wave。"
            "本计划只给后续人工浏览器或机构导出跟进排顺序，不分派 owner，不采集证据，"
            "不做权利结论，不确认著录或馆藏，也不做释读判断。"
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "output_scope": OUTPUT_SCOPE,
        "upstream_context_pack_id": review_summary.get("context_pack_id", ""),
        "coverage": {
            "assignment_item_count": len(assignment_items),
            "review_task_count": len(assignment_items),
            "assignment_wave_count": len(assignment_waves),
            "target_source_workstream_count": len(target_source_workstreams),
            "followup_family_count": len(family_counts),
            "target_source_count": len(target_source_counts),
            "artifact_kind_count": len(artifact_kind_counts),
            "route_file_reference_count": sum(
                len(item["route_files_to_open"]) for item in assignment_items
            ),
            "unique_route_file_count": len(unique_route_files),
            "required_review_section_count": len(unique_review_sections),
            "required_next_check_count": len(unique_next_checks),
            "staging_row_count_total": sum(int(item["staging_row_count"]) for item in assignment_items),
            "followup_family_counts": {
                family_id: family_counts.get(family_id, 0) for family_id in FAMILY_ORDER
            },
            "target_source_counts": dict(sorted(target_source_counts.items())),
            "artifact_kind_counts": dict(sorted(artifact_kind_counts.items())),
            "assignment_status_counts": dict(sorted(assignment_counts.items())),
            "handoff_readiness_status_counts": dict(sorted(readiness_counts.items())),
            "evidence_collection_status_counts": dict(sorted(evidence_counts.items())),
            "human_review_status_counts": dict(sorted(review_counts.items())),
            "official_access_boundary_status_counts": dict(sorted(access_counts.items())),
        },
        "assignment_waves": assignment_waves,
        "target_source_workstreams": target_source_workstreams,
        "assignment_items": assignment_items,
        "agent_use_rules": [
            "Use this assignment plan only to choose the next planned Xiaoxuetang follow-up route.",
            "Open the 078 plan item, 077 review summary, 076 route pack, source queue row, review-log draft, and all route files before recording any evidence.",
            "Keep each item planned_not_assigned until an owner explicitly records assignment outside this generated plan.",
            "Do not treat this plan as collected evidence, a rights decision, a catalog or collection match, a formal assignment, or a decipherment conclusion.",
        ],
        "agent_use_rules_zh": [
            "本分派计划只能用于选择下一条小学堂后续复核路线。",
            "记录任何证据前，必须先打开 078 计划项、077 review summary、076 route pack、source queue 行、review-log 草稿和全部 route files。",
            "在有人于本生成计划之外明确登记分派前，每个项目都必须保持 planned_not_assigned。",
            "不得把本计划当作已采集证据、权利结论、著录或馆藏匹配、正式分配或释读结论。",
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
    parser.add_argument("--route-pack", default=str(ROUTE_PACK))
    parser.add_argument("--review-summary", default=str(REVIEW_ROUTE_SUMMARY))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    plan = build_assignment_plan(
        read_json(root / args.route_pack),
        read_json(root / args.review_summary),
    )
    write_json(root / args.output, plan)
    print(
        f"context_pack_id={plan['context_pack_id']} "
        f"assignment_item_count={plan['coverage']['assignment_item_count']} "
        f"assignment_wave_count={plan['coverage']['assignment_wave_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
