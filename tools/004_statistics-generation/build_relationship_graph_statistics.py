#!/usr/bin/env python3
"""Build statistics from relationship graph edge JSONL files."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


GRAPH_EDGE_FILES = [
    Path("corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl"),
]
DEFAULT_EDGE_TYPE_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "001_relationship-graph-edge-type-summary.csv"
)
DEFAULT_NODE_DEGREE_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "002_relationship-graph-node-degree-summary.csv"
)
UPDATED_AT = "2026-06-04"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_jsonl_edges(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if stripped:
                rows.append(json.loads(stripped))
    return rows


def compact_counter(counter: Counter[str]) -> str:
    return ";".join(f"{key}:{counter[key]}" for key in sorted(counter))


def compact_set(values: set[str]) -> str:
    return ";".join(sorted(values))


def build_edge_type_summary(graph_files: list[Path], root: Path) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str, str], dict[str, object]] = {}
    for graph_file in graph_files:
        rows = read_jsonl_edges(root / graph_file)
        for edge in rows:
            for source_id in edge.get("source_ids", []):
                key = (graph_file.as_posix(), str(source_id), str(edge["edge_type"]))
                group = grouped.setdefault(
                    key,
                    {
                        "edge_count": 0,
                        "source_node_ids": set(),
                        "target_node_ids": set(),
                        "review_statuses": Counter(),
                        "confidence_levels": Counter(),
                    },
                )
                group["edge_count"] = int(group["edge_count"]) + 1
                group["source_node_ids"].add(str(edge["source_node_id"]))
                group["target_node_ids"].add(str(edge["target_node_id"]))
                group["review_statuses"][str(edge["review_status"])] += 1
                group["confidence_levels"][str(edge["confidence_level"])] += 1

    output_rows: list[dict[str, str]] = []
    for index, (key, group) in enumerate(sorted(grouped.items()), start=1):
        graph_file, source_id, edge_type = key
        output_rows.append(
            {
                "summary_row_id": f"graph-edge-type-summary-{index:03d}",
                "graph_file": graph_file,
                "source_id": source_id,
                "edge_type": edge_type,
                "edge_count": str(group["edge_count"]),
                "unique_source_node_count": str(len(group["source_node_ids"])),
                "unique_target_node_count": str(len(group["target_node_ids"])),
                "review_status_counts": compact_counter(group["review_statuses"]),
                "confidence_level_counts": compact_counter(group["confidence_levels"]),
                "generated_from": "relationship_graph_jsonl",
                "updated_at": UPDATED_AT,
            }
        )
    return output_rows


def build_node_degree_summary(graph_files: list[Path], root: Path) -> list[dict[str, str]]:
    node_stats: dict[str, dict[str, object]] = defaultdict(
        lambda: {
            "out_degree": 0,
            "in_degree": 0,
            "outgoing_edge_types": Counter(),
            "incoming_edge_types": Counter(),
            "source_ids": set(),
            "graph_files": set(),
            "review_statuses": Counter(),
        }
    )
    for graph_file in graph_files:
        rows = read_jsonl_edges(root / graph_file)
        graph_file_text = graph_file.as_posix()
        for edge in rows:
            source_node_id = str(edge["source_node_id"])
            target_node_id = str(edge["target_node_id"])
            edge_type = str(edge["edge_type"])
            review_status = str(edge["review_status"])
            edge_source_ids = {str(source_id) for source_id in edge.get("source_ids", [])}

            source_stats = node_stats[source_node_id]
            source_stats["out_degree"] = int(source_stats["out_degree"]) + 1
            source_stats["outgoing_edge_types"][edge_type] += 1
            source_stats["source_ids"].update(edge_source_ids)
            source_stats["graph_files"].add(graph_file_text)
            source_stats["review_statuses"][review_status] += 1

            target_stats = node_stats[target_node_id]
            target_stats["in_degree"] = int(target_stats["in_degree"]) + 1
            target_stats["incoming_edge_types"][edge_type] += 1
            target_stats["source_ids"].update(edge_source_ids)
            target_stats["graph_files"].add(graph_file_text)
            target_stats["review_statuses"][review_status] += 1

    sorted_items = sorted(
        node_stats.items(),
        key=lambda item: (
            -(int(item[1]["out_degree"]) + int(item[1]["in_degree"])),
            item[0],
        ),
    )
    output_rows: list[dict[str, str]] = []
    for index, (node_id, stats) in enumerate(sorted_items, start=1):
        out_degree = int(stats["out_degree"])
        in_degree = int(stats["in_degree"])
        output_rows.append(
            {
                "node_degree_row_id": f"graph-node-degree-{index:06d}",
                "node_id": node_id,
                "total_degree": str(out_degree + in_degree),
                "out_degree": str(out_degree),
                "in_degree": str(in_degree),
                "outgoing_edge_type_counts": compact_counter(stats["outgoing_edge_types"]),
                "incoming_edge_type_counts": compact_counter(stats["incoming_edge_types"]),
                "source_ids": compact_set(stats["source_ids"]),
                "graph_files": compact_set(stats["graph_files"]),
                "review_status_counts": compact_counter(stats["review_statuses"]),
                "generated_from": "relationship_graph_jsonl",
                "updated_at": UPDATED_AT,
            }
        )
    return output_rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows to write: {path}")
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--edge-type-output", default=str(DEFAULT_EDGE_TYPE_OUTPUT))
    parser.add_argument("--node-degree-output", default=str(DEFAULT_NODE_DEGREE_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    edge_type_rows = build_edge_type_summary(GRAPH_EDGE_FILES, root)
    node_degree_rows = build_node_degree_summary(GRAPH_EDGE_FILES, root)
    write_csv(root / args.edge_type_output, edge_type_rows)
    write_csv(root / args.node_degree_output, node_degree_rows)
    print(
        f"edge_type_rows={len(edge_type_rows)} "
        f"node_degree_rows={len(node_degree_rows)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
