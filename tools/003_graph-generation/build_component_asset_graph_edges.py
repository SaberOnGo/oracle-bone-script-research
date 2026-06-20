#!/usr/bin/env python3
"""Build graph edges from component candidates to local visual assets."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_ASSET_SOURCE_INDEX = Path(
    "project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv"
)
DEFAULT_OUTPUT = Path("corpus/008_relationship-graph/011_component-asset-graph-edges.jsonl")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_values(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def build_edges(asset_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    component_rows = [
        row
        for row in asset_rows
        if row.get("asset_type") == "obimd_component_candidate_image"
        and row.get("asset_id", "")
        and row.get("related_project_ids", "")
    ]
    edges: list[dict[str, object]] = []
    for index, row in enumerate(
        sorted(component_rows, key=lambda item: item["asset_id"]),
        start=1,
    ):
        related_project_ids = split_values(row["related_project_ids"])
        if len(related_project_ids) != 1:
            raise ValueError(f"component asset must link one project ID: {row['asset_id']}")
        source_ids = split_values(row.get("source_ids", ""))
        if not source_ids:
            raise ValueError(f"component asset missing source_ids: {row['asset_id']}")
        review_status = row.get("review_status", "") or "needs_human_visual_review"
        edges.append(
            {
                "edge_id": f"edge-component-asset-candidate-{index:05d}",
                "source_node_id": related_project_ids[0],
                "edge_type": "COMPONENT_CANDIDATE_HAS_LOCAL_IMAGE_ASSET",
                "target_node_id": row["asset_id"],
                "confidence_level": "high",
                "source_ids": source_ids,
                "evidence_note": (
                    "Local visual asset edge from the asset source registry; "
                    "the linked OBIMD subcharacter image is a preparation-stage "
                    "candidate asset and not a confirmed component form, component "
                    "assignment, oracle-character identity, or decipherment claim."
                ),
                "review_status": review_status,
                "asset_path": row.get("canonical_path", ""),
                "primary_external_ref_id": row.get("primary_external_ref_id", ""),
                "rights_status": row.get("rights_status", ""),
                "risk_note": row.get("risk_note", ""),
            }
        )
    return edges


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            file.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset-source-index", default=str(DEFAULT_ASSET_SOURCE_INDEX))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    asset_rows = read_csv_rows(root / args.asset_source_index)
    edges = build_edges(asset_rows)
    write_jsonl(root / args.output, edges)
    print(f"wrote={len(edges)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
