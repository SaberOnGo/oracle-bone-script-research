#!/usr/bin/env python3
"""Build an assignment plan for graph-source evidence collection review tasks."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


REVIEW_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/"
    "028_ai-agent-graph-source-evidence-collection-review-queue.csv"
)
REVIEW_ROUTE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/"
    "029_ai-agent-graph-source-evidence-collection-review-route-summary.json"
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
    "030_ai-agent-graph-source-evidence-collection-assignment-plan.json"
)
UPDATED_AT = "2026-06-10"
SOURCE_ORDER = ["src-hust-obc", "src-evobc", "src-obimd"]
PRIORITY_SECTION_ORDER = [
    "source_register",
    "download_log",
    "package_manifest",
    "metadata_profile",
    "rights_risk_review",
    "graph_edges",
    "staging_row",
    "counter_source_lookup",
    "review_log",
]
STATUS = "draft_assignment_plan_not_started"
RESEARCH_BOUNDARY = "evidence_collection_assignment_plan_not_scholarship"
OUTPUT_SCOPE = "graph_source_evidence_collection_assignment_plan_only"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _split_compact(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def _source_index(source_id: str) -> int:
    try:
        return SOURCE_ORDER.index(source_id)
    except ValueError:
        return len(SOURCE_ORDER)


def _priority_index(row: dict[str, str]) -> tuple[int, int]:
    try:
        priority_rank = int(row["priority_rank"])
    except (KeyError, ValueError):
        priority_rank = len(PRIORITY_SECTION_ORDER) + 1
    return priority_rank, _source_index(row.get("source_id", ""))


def _unique_sorted(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def _all_route_files(rows: list[dict[str, str]]) -> list[str]:
    return _unique_sorted(
        [
            route_file
            for row in rows
            for route_file in _split_compact(row.get("route_files_to_open", ""))
        ]
    )


def _all_counter_sources(rows: list[dict[str, str]]) -> list[str]:
    return _unique_sorted(
        [
            source_id
            for row in rows
            for source_id in _split_compact(row.get("counter_source_ids_to_check", ""))
        ]
    )


def _assignment_item(index: int, row: dict[str, str]) -> dict[str, object]:
    route_files = _split_compact(row["route_files_to_open"])
    counter_sources = _split_compact(row["counter_source_ids_to_check"])
    return {
        "assignment_plan_item_id": f"graph-source-evidence-assignment-{index:03d}",
        "evidence_collection_review_task_id": row["evidence_collection_review_task_id"],
        "evidence_collection_result_id": row["evidence_collection_result_id"],
        "evidence_collection_task_id": row["evidence_collection_task_id"],
        "source_id": row["source_id"],
        "primary_review_record_id": row["primary_review_record_id"],
        "primary_external_ref_id": row["primary_external_ref_id"],
        "source_record_id": row["source_record_id"],
        "target_evidence_section": row["target_evidence_section"],
        "priority_rank": row["priority_rank"],
        "assignment_status": "planned_not_assigned",
        "review_status": row["review_status"],
        "evidence_collection_status": row["evidence_collection_status"],
        "source_promotion_status": row["source_promotion_status"],
        "decipherment_claim_status": row["decipherment_claim_status"],
        "required_collection_action": row["required_collection_action"],
        "required_review_checks": _split_compact(row["required_review_checks"]),
        "result_scaffold_path": row["result_scaffold_path"],
        "result_update_target_path": row["result_update_target_path"],
        "note_draft_path": row["note_draft_path"],
        "route_pack_path": row["route_pack_path"],
        "manifest_path": row["manifest_path"],
        "task_queue_source_path": row["task_queue_source_path"],
        "route_files_to_open": route_files,
        "route_file_count": len(route_files),
        "counter_source_ids_to_check": counter_sources,
        "counter_source_count": len(counter_sources),
        "research_boundary": row["research_boundary"],
        "output_scope": row["output_scope"],
        "caution": row["caution"],
    }


def build_assignment_plan(
    review_rows: list[dict[str, str]],
    review_summary: dict[str, object],
) -> dict[str, object]:
    ordered_rows = sorted(review_rows, key=_priority_index)
    assignment_items = [
        _assignment_item(index, row)
        for index, row in enumerate(ordered_rows, start=1)
    ]

    items_by_section = {
        section: [
            item
            for item in assignment_items
            if item["target_evidence_section"] == section
        ]
        for section in PRIORITY_SECTION_ORDER
    }
    assignment_waves = []
    for wave_index, section in enumerate(PRIORITY_SECTION_ORDER, start=1):
        items = sorted(
            items_by_section[section],
            key=lambda item: _source_index(str(item["source_id"])),
        )
        route_files = _unique_sorted(
            [
                route_file
                for item in items
                for route_file in item["route_files_to_open"]
            ]
        )
        assignment_waves.append(
            {
                "assignment_wave_id": f"graph-source-evidence-assignment-wave-{wave_index:03d}",
                "target_evidence_section": section,
                "priority_rank": str(wave_index),
                "assignment_item_count": len(items),
                "source_ids": [str(item["source_id"]) for item in items],
                "assignment_plan_item_ids": [
                    str(item["assignment_plan_item_id"]) for item in items
                ],
                "review_task_ids": [
                    str(item["evidence_collection_review_task_id"]) for item in items
                ],
                "route_file_count": len(route_files),
                "route_files_to_open": route_files,
                "assignment_status": "planned_not_assigned",
                "evidence_collection_status": "not_collected",
                "source_promotion_status": "not_promoted",
                "decipherment_claim_status": "no_claim",
            }
        )

    source_workstreams = []
    for source_id in SOURCE_ORDER:
        items = [
            item for item in assignment_items if item["source_id"] == source_id
        ]
        source_workstreams.append(
            {
                "source_id": source_id,
                "assignment_item_count": len(items),
                "assignment_plan_item_ids": [
                    str(item["assignment_plan_item_id"]) for item in items
                ],
                "review_task_ids": [
                    str(item["evidence_collection_review_task_id"]) for item in items
                ],
                "target_evidence_sections": [
                    str(item["target_evidence_section"]) for item in items
                ],
                "min_priority_rank": min((int(item["priority_rank"]) for item in items), default=0),
                "max_priority_rank": max((int(item["priority_rank"]) for item in items), default=0),
                "route_file_count": len(
                    _unique_sorted(
                        [
                            route_file
                            for item in items
                            for route_file in item["route_files_to_open"]
                        ]
                    )
                ),
                "counter_source_count": len(
                    _unique_sorted(
                        [
                            source
                            for item in items
                            for source in item["counter_source_ids_to_check"]
                        ]
                    )
                ),
            }
        )

    assignment_counts = Counter(str(item["assignment_status"]) for item in assignment_items)
    review_counts = Counter(str(item["review_status"]) for item in assignment_items)
    evidence_counts = Counter(str(item["evidence_collection_status"]) for item in assignment_items)
    promotion_counts = Counter(str(item["source_promotion_status"]) for item in assignment_items)
    decipherment_counts = Counter(str(item["decipherment_claim_status"]) for item in assignment_items)
    source_counts = Counter(str(item["source_id"]) for item in assignment_items)
    section_counts = Counter(str(item["target_evidence_section"]) for item in assignment_items)
    route_file_reference_count = sum(
        len(item["route_files_to_open"]) for item in assignment_items
    )
    counter_source_reference_count = sum(
        len(item["counter_source_ids_to_check"]) for item in assignment_items
    )
    unique_route_files = _unique_sorted(
        [
            route_file
            for item in assignment_items
            for route_file in item["route_files_to_open"]
        ]
    )
    unique_counter_sources = _unique_sorted(
        [
            source_id
            for item in assignment_items
            for source_id in item["counter_source_ids_to_check"]
        ]
    )

    return {
        "context_pack_id": "ai-context-graph-source-evidence-collection-assignment-plan-001",
        "title": "Graph Source Evidence Collection Assignment Plan",
        "title_zh": "图谱来源证据收集复核任务分配计划",
        "status": STATUS,
        "updated_at": UPDATED_AT,
        "generated_from": [
            REVIEW_ROUTE_SUMMARY.as_posix(),
            REVIEW_QUEUE.as_posix(),
            RESULT_SCAFFOLD.as_posix(),
            ROUTE_PACK.as_posix(),
        ],
        "purpose": (
            "Plan review-task assignment waves from the 029 route summary and 028 "
            "review queue. This pack only orders unassigned, not-collected review "
            "routes; it does not assign people, collect evidence, decide rights, "
            "promote sources, or make decipherment claims."
        ),
        "purpose_zh": (
            "依据 029 路由摘要和 028 复核队列规划复核任务分配 wave。"
            "本包只排序未分配、未收集的复核路由；不分配具体人员，"
            "不收集证据，不决定权利，不提升来源，也不提出释读声明。"
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "output_scope": OUTPUT_SCOPE,
        "upstream_context_pack_id": review_summary.get("context_pack_id", ""),
        "coverage": {
            "review_task_count": len(assignment_items),
            "assignment_item_count": len(assignment_items),
            "assignment_wave_count": len(assignment_waves),
            "source_workstream_count": len(source_workstreams),
            "source_count": len(source_counts),
            "target_evidence_section_count": len(section_counts),
            "route_file_reference_count": route_file_reference_count,
            "unique_route_file_count": len(unique_route_files),
            "counter_source_reference_count": counter_source_reference_count,
            "unique_counter_source_count": len(unique_counter_sources),
            "source_counts": {
                source_id: source_counts.get(source_id, 0)
                for source_id in SOURCE_ORDER
            },
            "section_counts": {
                section: section_counts.get(section, 0)
                for section in PRIORITY_SECTION_ORDER
            },
            "assignment_status_counts": dict(sorted(assignment_counts.items())),
            "review_status_counts": dict(sorted(review_counts.items())),
            "evidence_collection_status_counts": dict(sorted(evidence_counts.items())),
            "source_promotion_status_counts": dict(sorted(promotion_counts.items())),
            "decipherment_claim_status_counts": dict(sorted(decipherment_counts.items())),
        },
        "assignment_waves": assignment_waves,
        "source_workstreams": source_workstreams,
        "assignment_items": assignment_items,
        "agent_use_rules": [
            "Use this assignment plan only to choose the next planned review route; it does not assign a human or agent owner.",
            "Open the 030 plan item, 029 route summary, 028 queue row, 027 result scaffold row, 026 route pack, note draft, manifest, and all route files before recording evidence.",
            "Keep each item planned_not_assigned until an owner explicitly records assignment outside this generated plan.",
            "Do not treat this plan as collected evidence, a rights decision, a source promotion decision, a component or evolution-chain assignment, or a decipherment conclusion.",
            "Keep any new downloads or scratch analysis in ignored temporary directories until source, size, checksum, rights, and risk are recorded.",
        ],
        "agent_use_rules_zh": [
            "本分配计划只能用于选择下一条计划中的复核路由；它不分配具体人工或 agent owner。",
            "记录证据前，必须打开 030 计划项、029 路由摘要、028 队列行、027 结果骨架行、026 路由包、note draft、manifest 和全部 route files。",
            "在有人明确于本生成计划之外登记分配前，每项都必须保持 planned_not_assigned。",
            "不得把本计划当作已收集证据、权利决定、来源提升决定、构件或演化链判定、释读结论。",
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
    parser.add_argument("--review-queue", default=str(REVIEW_QUEUE))
    parser.add_argument("--review-summary", default=str(REVIEW_ROUTE_SUMMARY))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    plan = build_assignment_plan(
        read_csv_rows(root / args.review_queue),
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
