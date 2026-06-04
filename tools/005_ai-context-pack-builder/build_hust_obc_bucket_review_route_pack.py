#!/usr/bin/env python3
"""Build an AI Agent route pack for HUST-OBC bucket review batches."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_BUCKET_SUMMARY = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "010_hust-obc-promotion-bucket-review-summary.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "004_ai-agent-hust-obc-bucket-review-route-pack.json"
)
UPDATED_AT = "2026-06-04"

HUST_GRAPH_EDGES = "corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl"
OBIMD_GRAPH_EDGES = "corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl"
EVOBC_GRAPH_EDGES = "corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl"
SOURCE_INDEX = "corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv"

SOURCE_ROUTE_REQUIREMENTS = [
    {
        "source_id": "src-hust-obc",
        "role": "starting_candidate_metadata",
        "required_lookup": "Open the bucket manifest and HUST-OBC graph edges for candidate/category/label metadata.",
        "required_lookup_zh": "打开 bucket manifest 和 HUST-OBC 图谱边，核对 candidate、category、label metadata。",
    },
    {
        "source_id": "src-xiaoxuetang-jiaguwen",
        "role": "character_head_and_glyph_form_cross_check",
        "required_lookup": "Cross-check whether the candidate aligns with Xiaoxuetang oracle character heads and glyph forms.",
        "required_lookup_zh": "交叉核对候选是否能对应小學堂甲骨文字头与字形。",
    },
    {
        "source_id": "src-xiaoxuetang-obm",
        "role": "catalog_and_heji_source_cross_check",
        "required_lookup": "Check catalog abbreviations, Heji references, and source notes before promoting any ID.",
        "required_lookup_zh": "正式提升前核对著录简称、合集引用和来源说明。",
    },
    {
        "source_id": "src-obimd",
        "role": "component_and_glyph_variant_cross_check",
        "required_lookup": "Compare OBIMD component and glyph metadata for possible form-family links.",
        "required_lookup_zh": "比较 OBIMD 构件与 glyph metadata，寻找可能的字形族关联。",
    },
    {
        "source_id": "src-evobc",
        "role": "evolution_correspondence_cross_check",
        "required_lookup": "Use EVOBC only as evolution-category metadata; do not treat it as accepted decipherment evidence.",
        "required_lookup_zh": "EVOBC 仅作为演化 category metadata 使用，不得当作已接受释读证据。",
    },
    {
        "source_id": "src-ihp-oracle-rubbings",
        "role": "primary_rubbing_or_inscription_context_lookup",
        "required_lookup": "Find primary rubbing or inscription context before any character-level hypothesis.",
        "required_lookup_zh": "提出单字假说前，先查找原拓或卜辞上下文。",
    },
]

EVIDENCE_GAP_TYPES = [
    "source_provenance",
    "primary_inscription_context",
    "neighboring_characters",
    "component_breakdown",
    "variant_chain",
    "bronze_seal_modern_correspondence",
    "cooccurrence_distribution",
    "supporting_evidence",
    "opposing_evidence",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _int_value(row: dict[str, str], field: str) -> int:
    value = row.get(field, "")
    return int(value) if value.isdigit() else 0


def build_route_pack(summary_rows: list[dict[str, str]]) -> dict[str, object]:
    bucket_routes = []
    for row in summary_rows:
        bucket_routes.append(
            {
                "bucket_summary_id": row["bucket_summary_id"],
                "bucket_number": row["bucket_number"],
                "bucket_directory": row["bucket_directory"],
                "manifest_path": row["manifest_path"],
                "suggested_oracle_character_id_range": [
                    row["suggested_oracle_character_id_start"],
                    row["suggested_oracle_character_id_end"],
                ],
                "promotion_queue_id_range": [
                    row["promotion_queue_id_start"],
                    row["promotion_queue_id_end"],
                ],
                "candidate_class_id_range": [
                    row["candidate_class_id_start"],
                    row["candidate_class_id_end"],
                ],
                "candidate_count": _int_value(row, "row_count"),
                "multi_component_label_count": _int_value(row, "multi_component_label_count"),
                "source_category_row_count": _int_value(row, "source_category_row_count"),
                "assignment_status": row["assignment_status_set"],
                "review_status": row["review_status_set"],
                "required_next_review": row["required_next_review"],
                "route_files": [
                    row["manifest_path"],
                    HUST_GRAPH_EDGES,
                    OBIMD_GRAPH_EDGES,
                    EVOBC_GRAPH_EDGES,
                    SOURCE_INDEX,
                ],
                "evidence_gap_types": EVIDENCE_GAP_TYPES,
                "agent_batch_steps": [
                    "Open the bucket manifest rows before reasoning.",
                    "Trace each HUST-OBC candidate to source category and OCR label graph edges.",
                    "Cross-check against Xiaoxuetang, OBM, OBIMD, EVOBC, and primary inscription context.",
                    "Write only draft evidence packs under doc/public/user_research/ until human review.",
                ],
                "agent_batch_steps_zh": [
                    "推理前先打开 bucket manifest 行。",
                    "把每个 HUST-OBC candidate 追溯到 source category 和 OCR label 图谱边。",
                    "交叉核对小學堂、OBM、OBIMD、EVOBC 和原始卜辞上下文。",
                    "人工复核前，只能把证据包草稿写入 doc/public/user_research/。",
                ],
            }
        )

    return {
        "context_pack_id": "ai-context-hust-obc-bucket-review-001",
        "title": "HUST-OBC Bucket Review Route Pack",
        "title_zh": "HUST-OBC 分桶复核路由包",
        "status": "reviewed_metadata_only",
        "updated_at": UPDATED_AT,
        "generated_from": [DEFAULT_BUCKET_SUMMARY.as_posix()],
        "purpose": (
            "Route AI Agents from 16 HUST-OBC promotion-review buckets to the specific "
            "manifests, graph files, source checks, and evidence gaps needed before any "
            "draft hypothesis. This pack does not contain decipherment claims."
        ),
        "purpose_zh": (
            "把 AI Agent 从 16 个 HUST-OBC 提升复核 bucket 路由到具体 manifest、图谱文件、"
            "来源核验和证据缺口；生成任何草稿假说前必须先完成这些检索。本包不包含释读结论。"
        ),
        "coverage": {
            "bucket_count": len(bucket_routes),
            "candidate_count": sum(route["candidate_count"] for route in bucket_routes),
            "multi_component_label_count": sum(
                route["multi_component_label_count"] for route in bucket_routes
            ),
            "source_category_row_count": sum(
                route["source_category_row_count"] for route in bucket_routes
            ),
            "route_file_count_per_bucket": 5,
            "source_route_requirement_count": len(SOURCE_ROUTE_REQUIREMENTS),
            "evidence_gap_type_count": len(EVIDENCE_GAP_TYPES),
        },
        "source_route_requirements": SOURCE_ROUTE_REQUIREMENTS,
        "bucket_routes": bucket_routes,
        "agent_use_rules": [
            "Use this pack only for routing HUST-OBC bucket review work.",
            "Open the bucket manifest and cited graph/source files before making any claim.",
            "Treat suggested obs-char IDs as reserved candidates, not assigned project characters.",
            "Draft hypotheses and evidence packs belong under doc/public/user_research/ until reviewed.",
        ],
        "agent_use_rules_zh": [
            "本包只用于路由 HUST-OBC 分桶复核工作。",
            "提出任何判断前，必须打开 bucket manifest 以及被引用的图谱和来源文件。",
            "建议 obs-char ID 只是保留候选，不是已分配的本项目甲骨单字。",
            "假说草稿和证据包在复核前只能放在 doc/public/user_research/。",
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
    parser.add_argument("--bucket-summary", default=str(DEFAULT_BUCKET_SUMMARY))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    route_pack = build_route_pack(read_csv_rows(root / args.bucket_summary))
    write_json(root / args.output, route_pack)
    print(
        f"context_pack_id={route_pack['context_pack_id']} "
        f"bucket_count={route_pack['coverage']['bucket_count']} "
        f"candidate_count={route_pack['coverage']['candidate_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
