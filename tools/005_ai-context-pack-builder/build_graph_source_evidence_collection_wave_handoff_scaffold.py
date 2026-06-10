#!/usr/bin/env python3
"""Build a first-wave handoff scaffold for graph-source evidence collection."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


ASSIGNMENT_PLAN = Path(
    "corpus/009_statistics-and-derived-features/"
    "030_ai-agent-graph-source-evidence-collection-assignment-plan.json"
)
REVIEW_ROUTE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/"
    "029_ai-agent-graph-source-evidence-collection-review-route-summary.json"
)
REVIEW_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/"
    "028_ai-agent-graph-source-evidence-collection-review-queue.csv"
)
RESULT_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "027_ai-agent-graph-source-evidence-collection-result-scaffold.csv"
)
ROUTE_PACK = Path(
    "corpus/009_statistics-and-derived-features/"
    "026_ai-agent-graph-source-evidence-collection-route-pack.json"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "031_ai-agent-graph-source-evidence-collection-wave-handoff-scaffold.json"
)
UPDATED_AT = "2026-06-10"
SOURCE_ORDER = ["src-hust-obc", "src-evobc", "src-obimd"]
STATUS = "draft_wave_handoff_scaffold_not_started"
RESEARCH_BOUNDARY = "evidence_collection_wave_handoff_scaffold_not_scholarship"
OUTPUT_SCOPE = "graph_source_evidence_collection_wave_handoff_scaffold_only"
TARGET_WAVE_ID = "graph-source-evidence-assignment-wave-001"
TARGET_EVIDENCE_SECTION = "source_register"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _source_index(source_id: str) -> int:
    try:
        return SOURCE_ORDER.index(source_id)
    except ValueError:
        return len(SOURCE_ORDER)


def _unique_sorted(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def _status_counts(items: list[dict[str, object]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(item.get(key, "")) for item in items).items()))


def _handoff_item(item: dict[str, object], wave: dict[str, object]) -> dict[str, object]:
    route_files = list(item.get("route_files_to_open", []))
    counter_sources = list(item.get("counter_source_ids_to_check", []))
    required_checks = list(item.get("required_review_checks", []))
    return {
        "handoff_item_id": str(item["assignment_plan_item_id"]).replace(
            "assignment", "handoff"
        ),
        "assignment_wave_id": wave["assignment_wave_id"],
        "assignment_plan_item_id": item["assignment_plan_item_id"],
        "assignment_status": item["assignment_status"],
        "evidence_collection_review_task_id": item["evidence_collection_review_task_id"],
        "evidence_collection_result_id": item["evidence_collection_result_id"],
        "evidence_collection_task_id": item["evidence_collection_task_id"],
        "source_id": item["source_id"],
        "primary_review_record_id": item["primary_review_record_id"],
        "primary_external_ref_id": item["primary_external_ref_id"],
        "source_record_id": item["source_record_id"],
        "target_evidence_section": item["target_evidence_section"],
        "priority_rank": item["priority_rank"],
        "handoff_status": "ready_for_source_register_evidence_collection_not_started",
        "review_status": item["review_status"],
        "evidence_collection_status": item["evidence_collection_status"],
        "source_promotion_status": item["source_promotion_status"],
        "decipherment_claim_status": item["decipherment_claim_status"],
        "required_collection_action": item["required_collection_action"],
        "required_review_checks": required_checks,
        "required_review_check_count": len(required_checks),
        "result_scaffold_path": item["result_scaffold_path"],
        "result_update_target_path": item["result_update_target_path"],
        "note_draft_path": item["note_draft_path"],
        "route_pack_path": item["route_pack_path"],
        "manifest_path": item["manifest_path"],
        "task_queue_source_path": item["task_queue_source_path"],
        "assignment_plan_path": ASSIGNMENT_PLAN.as_posix(),
        "review_route_summary_path": REVIEW_ROUTE_SUMMARY.as_posix(),
        "review_queue_path": REVIEW_QUEUE.as_posix(),
        "route_files_to_open": route_files,
        "route_file_count": len(route_files),
        "counter_source_ids_to_check": counter_sources,
        "counter_source_count": len(counter_sources),
        "research_boundary": RESEARCH_BOUNDARY,
        "output_scope": OUTPUT_SCOPE,
        "evidence_pack_write_status": "not_started",
        "rights_decision_status": "not_decided",
        "source_register_evidence_status": "not_collected",
        "source_promotion_review_status": "not_ready",
        "caution": (
            "This handoff row only opens the first assignment wave for later "
            "source-register evidence collection. It is not collected evidence, "
            "a rights decision, a source promotion decision, a component or "
            "evolution-chain assignment, or a decipherment conclusion."
        ),
    }


def build_wave_handoff_scaffold(
    assignment_plan: dict[str, object],
) -> dict[str, object]:
    waves = list(assignment_plan.get("assignment_waves", []))
    target_waves = [
        wave
        for wave in waves
        if wave.get("assignment_wave_id") == TARGET_WAVE_ID
        and wave.get("target_evidence_section") == TARGET_EVIDENCE_SECTION
    ]
    if len(target_waves) != 1:
        raise ValueError("expected exactly one source_register assignment wave")
    wave = target_waves[0]

    target_ids = set(wave.get("assignment_plan_item_ids", []))
    items = [
        item
        for item in list(assignment_plan.get("assignment_items", []))
        if item.get("assignment_plan_item_id") in target_ids
    ]
    items.sort(key=lambda item: _source_index(str(item.get("source_id", ""))))
    if len(items) != len(target_ids):
        raise ValueError("assignment plan does not contain every first-wave item")

    handoff_items = [_handoff_item(item, wave) for item in items]
    route_file_reference_count = sum(
        int(item["route_file_count"]) for item in handoff_items
    )
    counter_source_reference_count = sum(
        int(item["counter_source_count"]) for item in handoff_items
    )
    required_review_check_reference_count = sum(
        int(item["required_review_check_count"]) for item in handoff_items
    )
    unique_route_files = _unique_sorted(
        [
            route_file
            for item in handoff_items
            for route_file in list(item["route_files_to_open"])
        ]
    )
    unique_counter_sources = _unique_sorted(
        [
            source_id
            for item in handoff_items
            for source_id in list(item["counter_source_ids_to_check"])
        ]
    )
    unique_required_checks = _unique_sorted(
        [
            check
            for item in handoff_items
            for check in list(item["required_review_checks"])
        ]
    )

    return {
        "context_pack_id": "ai-context-graph-source-evidence-collection-wave-handoff-001",
        "title": "Graph Source Evidence Collection Wave Handoff Scaffold",
        "title_zh": "图谱来源证据收集首波交接脚手架",
        "status": STATUS,
        "updated_at": UPDATED_AT,
        "generated_from": [
            ASSIGNMENT_PLAN.as_posix(),
            REVIEW_ROUTE_SUMMARY.as_posix(),
            REVIEW_QUEUE.as_posix(),
            RESULT_SCAFFOLD.as_posix(),
            ROUTE_PACK.as_posix(),
        ],
        "purpose": (
            "Open the first source-register assignment wave from the 030 plan for "
            "future evidence collection. This scaffold only lists the handoff "
            "items and files that must be opened; it does not collect evidence, "
            "assign an owner, decide rights, promote sources, or make decipherment claims."
        ),
        "purpose_zh": (
            "从 030 计划打开第一波 source_register 分配任务，供后续证据收集使用。"
            "本脚手架只列出必须打开的交接项和文件；不收集证据，不分配 owner，"
            "不决定权利，不提升来源，也不提出释读声明。"
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "output_scope": OUTPUT_SCOPE,
        "upstream_context_pack_id": assignment_plan.get("context_pack_id", ""),
        "handoff_scope": {
            "assignment_wave_id": wave["assignment_wave_id"],
            "target_evidence_section": wave["target_evidence_section"],
            "priority_rank": wave["priority_rank"],
            "source_ids": wave["source_ids"],
            "assignment_plan_item_ids": wave["assignment_plan_item_ids"],
            "review_task_ids": wave["review_task_ids"],
            "handoff_status": "ready_for_source_register_evidence_collection_not_started",
            "assignment_status": wave["assignment_status"],
            "evidence_collection_status": wave["evidence_collection_status"],
            "source_promotion_status": wave["source_promotion_status"],
            "decipherment_claim_status": wave["decipherment_claim_status"],
        },
        "coverage": {
            "handoff_item_count": len(handoff_items),
            "assignment_wave_count": 1,
            "assignment_item_count": len(handoff_items),
            "review_task_count": len(handoff_items),
            "source_count": len({item["source_id"] for item in handoff_items}),
            "target_evidence_section_count": 1,
            "route_file_reference_count": route_file_reference_count,
            "unique_route_file_count": len(unique_route_files),
            "counter_source_reference_count": counter_source_reference_count,
            "unique_counter_source_count": len(unique_counter_sources),
            "required_review_check_reference_count": required_review_check_reference_count,
            "unique_required_review_check_count": len(unique_required_checks),
            "source_counts": dict(
                sorted(Counter(str(item["source_id"]) for item in handoff_items).items())
            ),
            "section_counts": dict(
                sorted(
                    Counter(
                        str(item["target_evidence_section"])
                        for item in handoff_items
                    ).items()
                )
            ),
            "handoff_status_counts": _status_counts(handoff_items, "handoff_status"),
            "assignment_status_counts": _status_counts(handoff_items, "assignment_status"),
            "review_status_counts": _status_counts(handoff_items, "review_status"),
            "evidence_collection_status_counts": _status_counts(
                handoff_items, "evidence_collection_status"
            ),
            "source_promotion_status_counts": _status_counts(
                handoff_items, "source_promotion_status"
            ),
            "decipherment_claim_status_counts": _status_counts(
                handoff_items, "decipherment_claim_status"
            ),
            "rights_decision_status_counts": _status_counts(
                handoff_items, "rights_decision_status"
            ),
            "source_register_evidence_status_counts": _status_counts(
                handoff_items, "source_register_evidence_status"
            ),
        },
        "route_files_to_open": unique_route_files,
        "counter_source_ids_to_check": unique_counter_sources,
        "required_review_checks": unique_required_checks,
        "handoff_items": handoff_items,
        "agent_use_rules": [
            "Use this handoff scaffold only to open the first source_register evidence-collection wave.",
            "Open the 031 handoff row, 030 plan item, 029 route summary, 028 queue row, 027 result scaffold row, 026 route pack, note draft, manifest, and all route files before recording evidence.",
            "Keep every row not_collected, not_promoted, not_decided, and no_claim until source-marked evidence is recorded elsewhere.",
            "Do not treat this scaffold as collected evidence, a rights decision, a source promotion decision, a component or evolution-chain assignment, or a decipherment conclusion.",
            "Keep any new downloads or scratch analysis in ignored temporary directories until source, size, checksum, rights, and risk are recorded.",
        ],
        "agent_use_rules_zh": [
            "本交接脚手架只能用于打开第一波 source_register 证据收集任务。",
            "记录证据前，必须打开 031 交接行、030 计划项、029 路由摘要、028 队列行、027 结果骨架行、026 路由包、note draft、manifest 和全部 route files。",
            "在带来源标记的证据于其他位置记录前，每行都必须保持 not_collected、not_promoted、not_decided 和 no_claim。",
            "不得把本脚手架当作已收集证据、权利决定、来源提升决定、构件或演化链判定、释读结论。",
            "新增下载或临时分析在记录来源、大小、checksum、权利和风险前必须留在已忽略临时目录。",
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
