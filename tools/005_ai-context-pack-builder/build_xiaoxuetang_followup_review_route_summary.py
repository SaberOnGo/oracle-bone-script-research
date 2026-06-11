#!/usr/bin/env python3
"""Build a review-route summary from the combined Xiaoxuetang follow-up route pack."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


ROUTE_PACK = Path(
    "corpus/009_statistics-and-derived-features/"
    "076_ai-agent-xiaoxuetang-followup-route-pack.json"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "077_ai-agent-xiaoxuetang-followup-review-route-summary.json"
)
UPDATED_AT = "2026-06-11"
FAMILY_ORDER = [
    "xxt_jgw_tls_access_boundary_followup",
    "xxt_obm_access_boundary_followup",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _family_index(family_id: str) -> int:
    try:
        return FAMILY_ORDER.index(family_id)
    except ValueError:
        return len(FAMILY_ORDER)


def build_review_summary(route_pack: dict[str, object]) -> dict[str, object]:
    route_rows = list(route_pack["followup_routes"])
    route_rows.sort(
        key=lambda row: (
            _family_index(str(row["followup_family_id"])),
            int(row["priority_rank"]),
            str(row["followup_task_id"]),
        )
    )

    family_counts = Counter(str(row["followup_family_id"]) for row in route_rows)
    target_source_counts = Counter(str(row["target_source_id"]) for row in route_rows)
    method_counts = Counter(str(row["followup_method"]) for row in route_rows)
    artifact_kind_counts = Counter(str(row["artifact_kind"]) for row in route_rows)
    access_status_counts = Counter(
        str(row["official_access_boundary_status"]) for row in route_rows
    )
    evidence_counts = Counter(
        str(row["evidence_collection_status"]) for row in route_rows
    )
    human_counts = Counter(str(row["human_review_status"]) for row in route_rows)
    rights_counts = Counter(str(row["rights_status"]) for row in route_rows)
    route_file_review_counts = Counter(
        str(row["route_file_review_status"]) for row in route_rows
    )

    family_summaries = []
    for family_id in FAMILY_ORDER:
        rows = [row for row in route_rows if row["followup_family_id"] == family_id]
        if not rows:
            continue
        family_summaries.append(
            {
                "followup_family_id": family_id,
                "followup_family_label": rows[0]["followup_family_label"],
                "review_task_count": len(rows),
                "target_source_ids": sorted({str(row["target_source_id"]) for row in rows}),
                "targeted_download_ids": [str(row["targeted_download_id"]) for row in rows],
                "artifact_kinds": sorted({str(row["artifact_kind"]) for row in rows}),
                "official_access_boundary_statuses": sorted(
                    {str(row["official_access_boundary_status"]) for row in rows}
                ),
                "route_file_count": len(
                    {
                        route_file
                        for row in rows
                        for route_file in row["route_files_to_open"]
                    }
                ),
                "required_review_sections": sorted(
                    {
                        section
                        for row in rows
                        for section in row["required_review_sections"]
                    }
                ),
                "review_log_draft_paths": [
                    str(row["review_log_draft_path"]) for row in rows
                ],
            }
        )

    target_source_summaries = []
    for target_source_id in sorted(target_source_counts):
        rows = [row for row in route_rows if row["target_source_id"] == target_source_id]
        target_source_summaries.append(
            {
                "target_source_id": target_source_id,
                "review_task_count": len(rows),
                "followup_family_ids": sorted(
                    {str(row["followup_family_id"]) for row in rows}
                ),
                "targeted_download_ids": [str(row["targeted_download_id"]) for row in rows],
                "review_log_draft_paths": [
                    str(row["review_log_draft_path"]) for row in rows
                ],
            }
        )

    return {
        "context_pack_id": "ai-context-xiaoxuetang-followup-review-summary-001",
        "title": "Xiaoxuetang Follow-up Review Route Summary",
        "title_zh": "小学堂后续复核路由摘要",
        "status": "draft_review_route_summary_not_collected",
        "updated_at": UPDATED_AT,
        "generated_from": [ROUTE_PACK.as_posix()],
        "purpose": (
            "Summarize the combined Xiaoxuetang follow-up route pack so later AI Agents "
            "can quickly choose whether the next route is a JGW character-page TLS/access "
            "boundary task or an OBM access-restricted-page task before opening route files."
        ),
        "purpose_zh": (
            "汇总合并后的小学堂后续复核路由包，让后续 AI Agent 在打开 route files 之前，"
            "先快速判断下一条路线属于甲骨文字页 TLS/访问边界任务还是《甲骨文合集材料来源表》"
            "访问受限页面任务。"
        ),
        "research_boundary": "xxt_followup_review_route_summary_not_scholarship",
        "coverage": {
            "review_task_count": len(route_rows),
            "followup_family_count": len(family_counts),
            "target_source_count": len(target_source_counts),
            "route_file_reference_count": sum(
                len(row["route_files_to_open"]) for row in route_rows
            ),
            "staging_row_count_total": sum(int(row["staging_row_count"]) for row in route_rows),
            "followup_family_counts": {
                family_id: family_counts.get(family_id, 0) for family_id in FAMILY_ORDER
            },
            "target_source_counts": dict(sorted(target_source_counts.items())),
            "followup_method_counts": dict(sorted(method_counts.items())),
            "artifact_kind_counts": dict(sorted(artifact_kind_counts.items())),
            "official_access_boundary_status_counts": dict(
                sorted(access_status_counts.items())
            ),
            "evidence_collection_status_counts": dict(sorted(evidence_counts.items())),
            "human_review_status_counts": dict(sorted(human_counts.items())),
            "rights_status_counts": dict(sorted(rights_counts.items())),
            "route_file_review_status_counts": dict(
                sorted(route_file_review_counts.items())
            ),
        },
        "route_pack_path": ROUTE_PACK.as_posix(),
        "family_summaries": family_summaries,
        "target_source_summaries": target_source_summaries,
        "agent_use_rules": [
            "Use this file only to choose the next Xiaoxuetang follow-up review route.",
            "Open the route-pack row, review-log draft, and all route files before recording any evidence.",
            "Do not treat this summary as source evidence, a rights decision, a catalog match, a collection/object match, a formal assignment, or a decipherment conclusion.",
        ],
        "agent_use_rules_zh": [
            "本文件只能用于选择下一条小学堂后续复核路线。",
            "记录任何证据前，必须先打开 route-pack 对应行、review-log 草稿和全部 route files。",
            "不得把本摘要当作来源证据、权利结论、著录匹配、馆藏/对象匹配、正式分配或释读结论。",
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
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    route_pack = json.loads((root / args.route_pack).read_text(encoding="utf-8"))
    summary = build_review_summary(route_pack)
    write_json(root / args.output, summary)
    print(
        f"context_pack_id={summary['context_pack_id']} "
        f"review_task_count={summary['coverage']['review_task_count']} "
        f"followup_family_count={summary['coverage']['followup_family_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
