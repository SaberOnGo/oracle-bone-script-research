#!/usr/bin/env python3
"""Build a routing summary from the combined Xiaoxuetang capture-results route pack."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


ROUTE_PACK = Path(
    "corpus/009_statistics-and-derived-features/"
    "086_ai-agent-xiaoxuetang-followup-capture-route-pack.json"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "087_ai-agent-xiaoxuetang-followup-capture-review-route-summary.json"
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
    route_rows = list(route_pack["capture_routes"])
    route_rows.sort(
        key=lambda row: (
            _family_index(str(row["followup_family_id"])),
            int(row["capture_priority_rank"]),
            str(row["followup_task_id"]),
        )
    )

    family_counts = Counter(str(row["followup_family_id"]) for row in route_rows)
    target_source_counts = Counter(str(row["target_source_id"]) for row in route_rows)
    artifact_kind_counts = Counter(str(row["artifact_kind"]) for row in route_rows)
    capture_status_counts = Counter(str(row["capture_status"]) for row in route_rows)
    human_review_status_counts = Counter(str(row["human_review_status"]) for row in route_rows)
    rights_status_counts = Counter(str(row["rights_status"]) for row in route_rows)
    access_boundary_counts = Counter(str(row["official_access_boundary_status"]) for row in route_rows)

    family_summaries = []
    for family_id in FAMILY_ORDER:
        rows = [row for row in route_rows if row["followup_family_id"] == family_id]
        if not rows:
            continue
        route_status_counter = Counter()
        for row in rows:
            for key, value in dict(row["route_status_snapshot"]).items():
                route_status_counter[f"{key}={value}"] += 1
        family_summaries.append(
            {
                "followup_family_id": family_id,
                "followup_family_label": rows[0]["followup_family_label"],
                "capture_result_count": len(rows),
                "target_source_ids": sorted({str(row["target_source_id"]) for row in rows}),
                "targeted_download_ids": [str(row["targeted_download_id"]) for row in rows],
                "capture_result_ids": [str(row["capture_result_id"]) for row in rows],
                "artifact_kinds": sorted({str(row["artifact_kind"]) for row in rows}),
                "official_access_boundary_statuses": sorted({str(row["official_access_boundary_status"]) for row in rows}),
                "route_file_count": len({route_file for row in rows for route_file in row["route_files_to_open"]}),
                "required_review_sections": sorted({section for row in rows for section in row["required_review_sections"]}),
                "route_status_counts": dict(sorted(route_status_counter.items())),
            }
        )

    target_source_summaries = []
    for target_source_id in sorted(target_source_counts):
        rows = [row for row in route_rows if row["target_source_id"] == target_source_id]
        target_source_summaries.append(
            {
                "target_source_id": target_source_id,
                "capture_result_count": len(rows),
                "followup_family_ids": sorted({str(row["followup_family_id"]) for row in rows}),
                "targeted_download_ids": [str(row["targeted_download_id"]) for row in rows],
                "capture_result_ids": [str(row["capture_result_id"]) for row in rows],
            }
        )

    return {
        "context_pack_id": "ai-context-xiaoxuetang-followup-capture-review-summary-001",
        "title": "Xiaoxuetang Follow-up Capture Review Route Summary",
        "title_zh": "小学堂 follow-up capture review route summary",
        "status": "draft_capture_review_route_summary_reviewed_metadata_only",
        "updated_at": UPDATED_AT,
        "generated_from": [ROUTE_PACK.as_posix()],
        "purpose": (
            "Summarize the combined Xiaoxuetang capture-results route pack so later AI Agents can quickly choose whether the next reviewed metadata-only route is a JGW character-page capture result or an OBM access-boundary capture result before opening route files."
        ),
        "purpose_zh": "汇总统一的小学堂 capture-results route pack，让后续 AI Agent 在打开 route files 前，先快速判断下一条 reviewed metadata-only 路线属于 JGW 字页 capture result 还是 OBM access-boundary capture result。",
        "research_boundary": "xxt_followup_capture_review_route_summary_not_scholarship",
        "coverage": {
            "capture_result_count": len(route_rows),
            "followup_family_count": len(family_counts),
            "target_source_count": len(target_source_counts),
            "route_file_reference_count": sum(len(row["route_files_to_open"]) for row in route_rows),
            "followup_family_counts": {family_id: family_counts.get(family_id, 0) for family_id in FAMILY_ORDER},
            "target_source_counts": dict(sorted(target_source_counts.items())),
            "artifact_kind_counts": dict(sorted(artifact_kind_counts.items())),
            "capture_status_counts": dict(sorted(capture_status_counts.items())),
            "human_review_status_counts": dict(sorted(human_review_status_counts.items())),
            "rights_status_counts": dict(sorted(rights_status_counts.items())),
            "official_access_boundary_status_counts": dict(sorted(access_boundary_counts.items())),
        },
        "route_pack_path": ROUTE_PACK.as_posix(),
        "family_summaries": family_summaries,
        "target_source_summaries": target_source_summaries,
        "agent_use_rules": [
            "Use this file only to choose the next Xiaoxuetang capture-result review route.",
            "Open the capture-route row and all route files before recording any new evidence or manual follow-up outcome.",
            "Do not treat this summary as source evidence, a rights decision, a catalog confirmation, a collection/object match, a formal assignment, or a decipherment conclusion.",
        ],
        "agent_use_rules_zh": [
            "本文档只能用于选择下一条小学堂 capture-result 复核路线。",
            "记录任何新证据或人工 follow-up 结果前，必须先打开 capture-route 行和全部 route files。",
            "不得把本摘要当作来源证据、权利结论、著录确认、馆藏/对象匹配、正式分配或释读结论。",
        ],
    }


def write_json(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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
        f"capture_result_count={summary['coverage']['capture_result_count']} "
        f"followup_family_count={summary['coverage']['followup_family_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
