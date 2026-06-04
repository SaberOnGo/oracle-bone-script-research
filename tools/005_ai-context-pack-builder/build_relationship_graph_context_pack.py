#!/usr/bin/env python3
"""Build a compact AI Agent context pack for relationship graph coverage."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_EDGE_TYPE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/"
    "001_relationship-graph-edge-type-summary.csv"
)
DEFAULT_NODE_DEGREE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/"
    "002_relationship-graph-node-degree-summary.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "003_ai-agent-relationship-graph-context-pack.json"
)
UPDATED_AT = "2026-06-04"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def source_label(source_id: str) -> str:
    labels = {
        "src-hust-obc": "HUST-OBC dataset metadata",
        "src-obimd": "OBIMD component and glyph metadata",
        "src-evobc": "EVOBC evolution category metadata",
    }
    return labels.get(source_id, source_id)


def build_context_pack(
    edge_summary_rows: list[dict[str, str]],
    node_degree_rows: list[dict[str, str]],
    top_node_limit: int = 20,
) -> dict[str, object]:
    total_edge_count = sum(int(row["edge_count"]) for row in edge_summary_rows)
    source_summaries: dict[str, dict[str, object]] = {}
    graph_files = sorted({row["graph_file"] for row in edge_summary_rows})
    for row in edge_summary_rows:
        source_id = row["source_id"]
        source_summary = source_summaries.setdefault(
            source_id,
            {
                "source_id": source_id,
                "label": source_label(source_id),
                "edge_count": 0,
                "edge_types": [],
                "graph_files": set(),
            },
        )
        source_summary["edge_count"] = int(source_summary["edge_count"]) + int(row["edge_count"])
        source_summary["edge_types"].append(
            {
                "edge_type": row["edge_type"],
                "edge_count": int(row["edge_count"]),
                "unique_source_node_count": int(row["unique_source_node_count"]),
                "unique_target_node_count": int(row["unique_target_node_count"]),
            }
        )
        source_summary["graph_files"].add(row["graph_file"])

    normalized_sources: list[dict[str, object]] = []
    for source_id in sorted(source_summaries):
        source_summary = source_summaries[source_id]
        normalized_sources.append(
            {
                "source_id": source_summary["source_id"],
                "label": source_summary["label"],
                "edge_count": source_summary["edge_count"],
                "graph_files": sorted(source_summary["graph_files"]),
                "edge_types": sorted(
                    source_summary["edge_types"],
                    key=lambda item: item["edge_type"],
                ),
            }
        )

    top_nodes = [
        {
            "node_id": row["node_id"],
            "total_degree": int(row["total_degree"]),
            "out_degree": int(row["out_degree"]),
            "in_degree": int(row["in_degree"]),
            "outgoing_edge_type_counts": row["outgoing_edge_type_counts"],
            "incoming_edge_type_counts": row["incoming_edge_type_counts"],
            "source_ids": row["source_ids"],
            "graph_files": row["graph_files"],
        }
        for row in node_degree_rows[:top_node_limit]
    ]

    return {
        "context_pack_id": "ai-context-relationship-graph-001",
        "title": "Relationship Graph Coverage Context Pack",
        "title_zh": "关系图谱覆盖范围上下文包",
        "status": "reviewed_metadata_only",
        "updated_at": UPDATED_AT,
        "generated_from": [
            DEFAULT_EDGE_TYPE_SUMMARY.as_posix(),
            DEFAULT_NODE_DEGREE_SUMMARY.as_posix(),
        ],
        "purpose": (
            "Entry-point context for AI Agents before deeper graph or source lookup; "
            "supports evidence-first retrieval and does not contain decipherment claims."
        ),
        "purpose_zh": (
            "供 AI Agent 深入检索图谱或来源表前使用的入口上下文；"
            "支持先证据后推理，不包含释读结论。"
        ),
        "coverage": {
            "graph_file_count": len(graph_files),
            "graph_files": graph_files,
            "source_count": len(normalized_sources),
            "edge_type_count": len(edge_summary_rows),
            "total_edge_count": total_edge_count,
            "node_count": len(node_degree_rows),
            "top_node_limit": top_node_limit,
        },
        "source_summaries": normalized_sources,
        "top_degree_nodes": top_nodes,
        "agent_use_rules": [
            "Use this pack only as a routing and coverage summary.",
            "Open the cited CSV/JSONL source rows before making any research claim.",
            "Treat HUST-OBC, OBIMD, and EVOBC rows as dataset metadata until cross-source review.",
            "Do not present OCR labels, component links, glyph code points, or evolution category links as accepted readings.",
        ],
        "agent_use_rules_zh": [
            "本上下文包只作为检索路由和覆盖范围摘要使用。",
            "提出任何研究判断前，必须打开被引用的 CSV/JSONL 来源行。",
            "HUST-OBC、OBIMD 和 EVOBC 记录在跨来源复核前都只是数据集元数据。",
            "不得把 OCR 标签、构件链接、glyph codepoint 或演化 category 关系写成已接受释读。",
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
    parser.add_argument("--edge-type-summary", default=str(DEFAULT_EDGE_TYPE_SUMMARY))
    parser.add_argument("--node-degree-summary", default=str(DEFAULT_NODE_DEGREE_SUMMARY))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--top-node-limit", type=int, default=20)
    args = parser.parse_args(argv)

    root = repo_root()
    edge_summary_rows = read_csv_rows(root / args.edge_type_summary)
    node_degree_rows = read_csv_rows(root / args.node_degree_summary)
    context_pack = build_context_pack(edge_summary_rows, node_degree_rows, args.top_node_limit)
    write_json(root / args.output, context_pack)
    print(
        f"context_pack_id={context_pack['context_pack_id']} "
        f"total_edge_count={context_pack['coverage']['total_edge_count']} "
        f"node_count={context_pack['coverage']['node_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
