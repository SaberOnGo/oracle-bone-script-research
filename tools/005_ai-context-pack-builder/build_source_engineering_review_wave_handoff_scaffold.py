#!/usr/bin/env python3
"""Build a first-wave handoff scaffold for source-engineering review routes."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
REVIEW_ROUTE_SUMMARY = STAT_DIR / "117_ai-agent-source-engineering-review-route-summary.json"
DEFAULT_OUTPUT = STAT_DIR / "118_ai-agent-source-engineering-review-wave-handoff-scaffold.json"

CONTEXT_PACK_ID = "ai-context-source-engineering-review-wave-handoff-001"
UPDATED_AT = "2026-06-19"
STATUS = "draft_source_engineering_review_wave_handoff_not_started"
RESEARCH_BOUNDARY = "source_engineering_review_wave_handoff_not_review_result"
OUTPUT_SCOPE = "source_engineering_review_wave_handoff_scaffold_only"
WAVE_ID = "source-engineering-review-wave-001"
HANDOFF_STATUS = "ready_for_source_engineering_review_not_started"
CAUTION = (
    "Source-engineering review wave handoff scaffold only; it does not record "
    "reviewed outcomes, is not collected evidence, not a corpus import, not "
    "source promotion, not a rights decision, and not an identity or "
    "decipherment claim."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def route_value(route: dict[str, Any], field: str) -> Any:
    if field == "result_status":
        return route.get("result_status") or route.get("field_map_result_status", "")
    if field == "evidence_collection_status":
        return route.get("evidence_collection_status") or "not_collected"
    return route.get(field, "")


def unique_sorted(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def unique_in_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def status_counts(items: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(item.get(field, "")) for item in items).items()))


def load_first_route(root: Path, lane: dict[str, Any]) -> dict[str, Any]:
    route_pack_path = Path(str(lane["route_pack_path"]))
    route_pack = read_json(root / route_pack_path)
    routes = list(route_pack.get("routes", []))
    return routes[0] if routes else {}


def route_files_for_item(summary_path: Path, lane: dict[str, Any], route: dict[str, Any]) -> list[str]:
    paths = [
        summary_path.as_posix(),
        str(lane.get("route_pack_path", "")),
        str(route.get("source_checklist_path", "")),
        str(route.get("lane_route_pack_path", "")),
        str(route.get("primary_input_path", "")),
        str(route.get("review_log_path", "")),
        str(route.get("result_record_path", "")),
    ]
    paths.extend(str(path) for path in list(route.get("secondary_input_paths", [])))
    for optional_field in [
        "source_register_path",
        "download_manifest_path",
        "download_log_path",
        "download_status_codebook_path",
        "downloaded_metadata_profile_path",
        "source_processing_pipeline_audit_path",
        "source_coverage_summary_path",
        "existing_field_map_path",
        "scaffold_path",
        "checklist_path",
        "target_reviewed_field_map_path",
        "package_manifest_path",
        "large_source_register_path",
    ]:
        paths.append(str(route.get(optional_field, "")))
    return unique_in_order(paths)


def handoff_item(root: Path, summary_path: Path, lane: dict[str, Any], wave_index: int) -> dict[str, Any]:
    route = load_first_route(root, lane)
    if not route:
        return {
            "handoff_item_id": f"source-engineering-review-wave-handoff-{wave_index:04d}",
            "wave_id": WAVE_ID,
            "action_lane": lane["action_lane"],
            "route_pack_id": lane["route_pack_id"],
            "route_pack_path": lane["route_pack_path"],
            "decision_field": str(lane["decision_field"]),
            "decision_value": "",
            "next_action_id": "",
            "result_scaffold_id": "",
            "source_engineering_gap_id": "",
            "source_id": "",
            "gap_type": "",
            "priority_rank": int(lane.get("priority_min", 0) or 0),
            "automation_scope": "no_current_routes_for_lane",
            "human_gate": "",
            "handoff_status": "no_current_routes_after_pipeline_refresh",
            "action_status": "no_current_source_engineering_route",
            "result_status": "not_applicable_no_current_route",
            "evidence_collection_status": "not_applicable_no_current_route",
            "human_review_status": "not_applicable_no_current_route",
            "rights_decision_status": "no_new_rights_decision",
            "source_promotion_status": "not_promoted",
            "corpus_import_status": "not_imported",
            "decipherment_claim_status": "no_decipherment_claim",
            "blocking_condition": "",
            "safe_to_automate_status": "no_current_route_to_automate",
            "review_log_path": "",
            "result_record_path": "",
            "required_followup": [],
            "required_followup_count": 0,
            "checklist_items": [],
            "checklist_item_count": 0,
            "route_files_to_open": unique_in_order([summary_path.as_posix(), str(lane.get("route_pack_path", ""))]),
            "route_file_count": 2,
            "review_route_summary_path": summary_path.as_posix(),
            "research_boundary": RESEARCH_BOUNDARY,
            "output_scope": OUTPUT_SCOPE,
            "caution": CAUTION,
        }
    decision_field = str(lane["decision_field"])
    required_followup = route.get("required_followup", route.get("required_review_steps", []))
    if isinstance(required_followup, str):
        required_followup = [required_followup]
    checklist_items = route.get("checklist_items", route.get("required_review_steps", []))
    if isinstance(checklist_items, str):
        checklist_items = [checklist_items]
    route_files = route_files_for_item(summary_path, lane, route)
    return {
        "handoff_item_id": f"source-engineering-review-wave-handoff-{wave_index:04d}",
        "wave_id": WAVE_ID,
        "action_lane": lane["action_lane"],
        "route_pack_id": lane["route_pack_id"],
        "route_pack_path": lane["route_pack_path"],
        "decision_field": decision_field,
        "decision_value": str(route.get(decision_field, "")),
        "next_action_id": route.get("next_action_id", ""),
        "result_scaffold_id": route.get("result_scaffold_id", route.get("field_map_result_scaffold_id", "")),
        "source_engineering_gap_id": route.get("source_engineering_gap_id", ""),
        "source_id": route.get("source_id", ""),
        "gap_type": route.get("gap_type", ""),
        "priority_rank": int(route.get("priority_rank", lane.get("priority_min", 0)) or 0),
        "automation_scope": route.get("automation_scope", ""),
        "human_gate": route.get("human_gate", ""),
        "handoff_status": HANDOFF_STATUS,
        "action_status": route.get("action_status", "ready_for_source_engineering_review"),
        "result_status": route_value(route, "result_status"),
        "evidence_collection_status": route_value(route, "evidence_collection_status"),
        "human_review_status": route.get("human_review_status", ""),
        "rights_decision_status": route.get("rights_decision_status", ""),
        "source_promotion_status": route.get("source_promotion_status", ""),
        "corpus_import_status": route.get("corpus_import_status", ""),
        "decipherment_claim_status": route.get("decipherment_claim_status", ""),
        "blocking_condition": route.get("blocking_condition", ""),
        "safe_to_automate_status": route.get("safe_to_automate_status", ""),
        "review_log_path": route.get("review_log_path", ""),
        "result_record_path": route.get("result_record_path", ""),
        "required_followup": list(required_followup),
        "required_followup_count": len(required_followup),
        "checklist_items": list(checklist_items),
        "checklist_item_count": len(checklist_items),
        "route_files_to_open": route_files,
        "route_file_count": len(route_files),
        "review_route_summary_path": summary_path.as_posix(),
        "research_boundary": RESEARCH_BOUNDARY,
        "output_scope": OUTPUT_SCOPE,
        "caution": CAUTION,
    }


def build_wave_handoff_scaffold(root: Path, summary: dict[str, Any]) -> dict[str, Any]:
    lanes = list(summary.get("lanes", []))
    handoff_items = [
        handoff_item(root, REVIEW_ROUTE_SUMMARY, lane, index)
        for index, lane in enumerate(lanes, start=1)
    ]
    selected_items = [
        item
        for item in handoff_items
        if item.get("handoff_status") != "no_current_routes_after_pipeline_refresh"
    ]
    no_route_lanes = [
        str(item["action_lane"])
        for item in handoff_items
        if item.get("handoff_status") == "no_current_routes_after_pipeline_refresh"
    ]
    route_files = unique_in_order(
        [
            route_file
            for item in handoff_items
            for route_file in list(item["route_files_to_open"])
        ]
    )
    return {
        "context_pack_id": CONTEXT_PACK_ID,
        "title": "Source Engineering Review Wave Handoff Scaffold",
        "title_zh": "来源工程复核首波交接脚手架",
        "status": STATUS,
        "updated_at": UPDATED_AT,
        "generated_from": [
            REVIEW_ROUTE_SUMMARY.as_posix(),
            *[str(lane.get("route_pack_path", "")) for lane in lanes],
        ],
        "purpose": (
            "Open the first pending route from each source-engineering review lane "
            "so later reviewers can record actual outcomes in the planned result "
            "records. This scaffold lists route files only."
        ),
        "purpose_zh": (
            "从每个来源工程复核 lane 打开第一条待处理路线，供后续复核者把实际结果写入已规划的结果记录。"
            "本脚手架只列出必开的 route files。"
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "output_scope": OUTPUT_SCOPE,
        "upstream_summary_id": summary.get("summary_id", ""),
        "handoff_scope": {
            "wave_id": WAVE_ID,
            "source_summary_path": REVIEW_ROUTE_SUMMARY.as_posix(),
            "route_selection_rule": "first_not_started_route_per_action_lane",
            "handoff_status": HANDOFF_STATUS,
            "action_lane_count": len(lanes),
            "total_upstream_route_count": summary.get("total_route_count", 0),
            "selected_route_count": len(selected_items),
            "no_current_route_lane_count": len(no_route_lanes),
            "no_current_route_lanes": no_route_lanes,
            "remaining_route_count_after_wave": int(summary.get("total_route_count", 0)) - len(selected_items),
            "review_status": "wave_handoff_pending_source_engineering_review",
            "evidence_collection_status": "not_collected",
            "rights_decision_status": "no_new_rights_decision",
            "source_promotion_status": "not_promoted",
            "corpus_import_status": "not_imported",
            "decipherment_claim_status": "no_decipherment_claim",
        },
        "coverage": {
            "handoff_item_count": len(handoff_items),
            "action_lane_count": len({item["action_lane"] for item in handoff_items}),
            "source_count": len({item["source_id"] for item in handoff_items}),
            "review_log_count": len({item["review_log_path"] for item in handoff_items}),
            "result_record_count": len({item["result_record_path"] for item in handoff_items}),
            "route_file_reference_count": sum(int(item["route_file_count"]) for item in handoff_items),
            "unique_route_file_count": len(route_files),
            "decision_filled_count": sum(1 for item in handoff_items if item["decision_value"]),
            "result_started_count": sum(1 for item in handoff_items if item["result_status"] != "not_started"),
            "action_lane_counts": status_counts(handoff_items, "action_lane"),
            "handoff_status_counts": status_counts(handoff_items, "handoff_status"),
            "result_status_counts": status_counts(handoff_items, "result_status"),
            "evidence_collection_status_counts": status_counts(handoff_items, "evidence_collection_status"),
            "human_review_status_counts": status_counts(handoff_items, "human_review_status"),
            "rights_decision_status_counts": status_counts(handoff_items, "rights_decision_status"),
            "source_promotion_status_counts": status_counts(handoff_items, "source_promotion_status"),
            "corpus_import_status_counts": status_counts(handoff_items, "corpus_import_status"),
            "decipherment_claim_status_counts": status_counts(handoff_items, "decipherment_claim_status"),
        },
        "route_files_to_open": route_files,
        "handoff_items": handoff_items,
        "agent_use_rules": [
            "Use this scaffold only to open the first source-engineering review wave.",
            "Open the 118 handoff item, 117 summary, lane route pack, review log, result record path, and every route file before recording a reviewed outcome.",
            "This scaffold is not collected evidence, not a rights decision, not source promotion, not corpus import, and not an identity or decipherment claim.",
            "Record actual reviewed outcomes in the cited result record path or the 105 result scaffold, not in this routing-only file.",
            "Keep any new downloads, OCR, unpacking, or checksum recalculation in ignored temporary directories until source, size, checksum, rights, and risk are recorded.",
        ],
        "agent_use_rules_zh": [
            "本脚手架只能用于打开第一波来源工程复核路线。",
            "记录复核结果前，必须打开 118 handoff item、117 summary、lane route pack、review log、result record path 和全部 route files。",
            "本脚手架不是已采集证据、不是权利判断、不是来源提升、不是语料导入，也不是身份或释读结论。",
            "实际复核结果应写入引用的 result record path 或 105 result scaffold，不写入这个仅用于路由的文件。",
            "任何新下载、OCR、解包或 checksum 复算，在记录来源、大小、checksum、权利和风险前，都必须留在已忽略临时目录。",
        ],
        "caution": CAUTION,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source-engineering review wave handoff scaffold.")
    parser.add_argument("--summary", default=str(REVIEW_ROUTE_SUMMARY))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    summary = read_json(root / args.summary)
    data = build_wave_handoff_scaffold(root, summary)
    write_json(root / args.output, data)
    print(
        f"context_pack_id={data['context_pack_id']} "
        f"handoff_item_count={data['coverage']['handoff_item_count']} "
        f"unique_route_file_count={data['coverage']['unique_route_file_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
