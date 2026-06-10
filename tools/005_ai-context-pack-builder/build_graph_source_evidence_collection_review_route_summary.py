#!/usr/bin/env python3
"""Build a route summary for graph-source evidence collection review tasks."""

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
    "029_ai-agent-graph-source-evidence-collection-review-route-summary.json"
)
UPDATED_AT = "2026-06-10"
SOURCE_ORDER = ["src-hust-obc", "src-evobc", "src-obimd"]
SECTION_ORDER = [
    "source_register",
    "download_log",
    "package_manifest",
    "metadata_profile",
    "graph_edges",
    "staging_row",
    "counter_source_lookup",
    "rights_risk_review",
    "review_log",
]
STATUS = "draft_review_route_summary_not_collected"
RESEARCH_BOUNDARY = "evidence_collection_review_route_summary_not_scholarship"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _split_compact(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def _source_index(source_id: str) -> int:
    try:
        return SOURCE_ORDER.index(source_id)
    except ValueError:
        return len(SOURCE_ORDER)


def _section_index(section: str) -> int:
    try:
        return SECTION_ORDER.index(section)
    except ValueError:
        return len(SECTION_ORDER)


def _sorted_route_files(rows: list[dict[str, str]]) -> list[str]:
    return sorted(
        {
            route_file
            for row in rows
            for route_file in _split_compact(row.get("route_files_to_open", ""))
        }
    )


def _sorted_counter_sources(rows: list[dict[str, str]]) -> list[str]:
    return sorted(
        {
            source_id
            for row in rows
            for source_id in _split_compact(row.get("counter_source_ids_to_check", ""))
        }
    )


def build_route_summary(review_rows: list[dict[str, str]]) -> dict[str, object]:
    ordered_rows = sorted(
        review_rows,
        key=lambda row: (
            _source_index(row["source_id"]),
            _section_index(row["target_evidence_section"]),
            row["evidence_collection_review_task_id"],
        ),
    )

    source_counts = Counter(row["source_id"] for row in ordered_rows)
    section_counts = Counter(row["target_evidence_section"] for row in ordered_rows)
    priority_counts = Counter(row["priority_rank"] for row in ordered_rows)
    assignment_counts = Counter(row["assignment_status"] for row in ordered_rows)
    review_status_counts = Counter(row["review_status"] for row in ordered_rows)
    evidence_counts = Counter(row["evidence_collection_status"] for row in ordered_rows)
    promotion_counts = Counter(row["source_promotion_status"] for row in ordered_rows)
    decipherment_counts = Counter(row["decipherment_claim_status"] for row in ordered_rows)
    boundary_counts = Counter(row["research_boundary"] for row in ordered_rows)
    scope_counts = Counter(row["output_scope"] for row in ordered_rows)
    all_route_files = _sorted_route_files(ordered_rows)
    all_counter_sources = _sorted_counter_sources(ordered_rows)

    source_summaries = []
    for source_id in SOURCE_ORDER:
        rows = [row for row in ordered_rows if row["source_id"] == source_id]
        source_summaries.append(
            {
                "source_id": source_id,
                "review_task_count": len(rows),
                "target_evidence_sections": [row["target_evidence_section"] for row in rows],
                "review_task_ids": [
                    row["evidence_collection_review_task_id"] for row in rows
                ],
                "primary_review_record_ids": sorted(
                    {row["primary_review_record_id"] for row in rows}
                ),
                "primary_external_ref_ids": sorted(
                    {row["primary_external_ref_id"] for row in rows}
                ),
                "min_priority_rank": min((int(row["priority_rank"]) for row in rows), default=0),
                "max_priority_rank": max((int(row["priority_rank"]) for row in rows), default=0),
                "route_file_count": len(_sorted_route_files(rows)),
                "counter_source_count": len(_sorted_counter_sources(rows)),
                "route_files_to_open": _sorted_route_files(rows),
                "counter_source_ids_to_check": _sorted_counter_sources(rows),
                "result_update_targets": sorted(
                    {row["result_update_target_path"] for row in rows}
                ),
            }
        )

    section_summaries = []
    for section in SECTION_ORDER:
        rows = [row for row in ordered_rows if row["target_evidence_section"] == section]
        section_summaries.append(
            {
                "target_evidence_section": section,
                "review_task_count": len(rows),
                "source_ids": [row["source_id"] for row in rows],
                "priority_rank": rows[0]["priority_rank"] if rows else "",
                "required_collection_actions": sorted(
                    {row["required_collection_action"] for row in rows}
                ),
                "required_review_check_count": sum(
                    len(_split_compact(row["required_review_checks"])) for row in rows
                ),
                "route_file_count": len(_sorted_route_files(rows)),
                "counter_source_count": len(_sorted_counter_sources(rows)),
                "manifest_paths": sorted({row["manifest_path"] for row in rows}),
                "result_scaffold_paths": sorted(
                    {row["result_scaffold_path"] for row in rows}
                ),
            }
        )

    return {
        "context_pack_id": "ai-context-graph-source-evidence-collection-review-summary-001",
        "title": "Graph Source Evidence Collection Review Route Summary",
        "title_zh": "图谱来源证据收集复核路由摘要",
        "status": STATUS,
        "updated_at": UPDATED_AT,
        "generated_from": [
            REVIEW_QUEUE.as_posix(),
            RESULT_SCAFFOLD.as_posix(),
            ROUTE_PACK.as_posix(),
        ],
        "purpose": (
            "Summarize the 028 graph-source evidence collection review queue by "
            "source and target evidence section so AI Agents can choose the next "
            "review route before opening route files. This is a routing summary only."
        ),
        "purpose_zh": (
            "按来源和目标证据章节汇总 028 图谱来源证据收集复核队列，"
            "让 AI Agent 在打开 route files 前先选择下一条复核路由。"
            "本文件只是路由摘要。"
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "coverage": {
            "review_task_count": len(ordered_rows),
            "source_count": len(source_counts),
            "target_evidence_section_count": len(section_counts),
            "route_file_reference_count": sum(
                len(_split_compact(row.get("route_files_to_open", "")))
                for row in ordered_rows
            ),
            "unique_route_file_count": len(all_route_files),
            "counter_source_reference_count": sum(
                len(_split_compact(row.get("counter_source_ids_to_check", "")))
                for row in ordered_rows
            ),
            "unique_counter_source_count": len(all_counter_sources),
            "source_counts": {source_id: source_counts.get(source_id, 0) for source_id in SOURCE_ORDER},
            "section_counts": {
                section: section_counts.get(section, 0) for section in SECTION_ORDER
            },
            "priority_rank_counts": dict(sorted(priority_counts.items())),
            "assignment_status_counts": dict(sorted(assignment_counts.items())),
            "review_status_counts": dict(sorted(review_status_counts.items())),
            "evidence_collection_status_counts": dict(sorted(evidence_counts.items())),
            "source_promotion_status_counts": dict(sorted(promotion_counts.items())),
            "decipherment_claim_status_counts": dict(sorted(decipherment_counts.items())),
            "research_boundary_counts": dict(sorted(boundary_counts.items())),
            "output_scope_counts": dict(sorted(scope_counts.items())),
        },
        "route_file_summary": {
            "route_files_to_open": all_route_files,
            "counter_source_ids_to_check": all_counter_sources,
            "review_queue_path": REVIEW_QUEUE.as_posix(),
            "result_scaffold_path": RESULT_SCAFFOLD.as_posix(),
            "route_pack_path": ROUTE_PACK.as_posix(),
        },
        "source_summaries": source_summaries,
        "section_summaries": section_summaries,
        "agent_use_rules": [
            "Use this file only to choose an evidence-collection review route.",
            "Open the 028 queue row, 027 result scaffold row, 026 route pack, manifest, note draft, and route files before recording evidence.",
            "Do not treat this summary as collected evidence, a rights decision, a source promotion decision, a component or evolution-chain assignment, or a decipherment conclusion.",
            "Keep any new downloads or scratch analysis in ignored temporary directories until source, size, checksum, rights, and risk are recorded.",
        ],
        "agent_use_rules_zh": [
            "本文件只能用于选择证据收集复核路由。",
            "记录证据前，必须打开 028 队列行、027 结果骨架行、026 路由包、manifest、note draft 和 route files。",
            "不得把本摘要当作已收集证据、权利决定、来源提升决定、构件或演化链判定、释读结论。",
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
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    summary = build_route_summary(read_csv_rows(root / args.review_queue))
    write_json(root / args.output, summary)
    print(
        f"context_pack_id={summary['context_pack_id']} "
        f"review_task_count={summary['coverage']['review_task_count']} "
        f"source_count={summary['coverage']['source_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
