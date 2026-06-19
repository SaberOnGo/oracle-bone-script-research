#!/usr/bin/env python3
"""Build graph edges for Cambridge/Hopkins inscription crosswalk metadata."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


DEFAULT_CROSSWALK_STAGING = Path(
    "corpus/002_oracle-bone-inscriptions/000_inscription-registers/"
    "002_cambridge-hopkins-crosswalk-staging.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/008_relationship-graph/"
    "008_cambridge-hopkins-inscription-crosswalk-graph-edges.jsonl"
)
DEFAULT_INSCRIPTION_MAP = Path(
    "project_registry/002_project-id-to-source-reference-map/"
    "002_oracle-inscription-id-source-map.csv"
)
SOURCE_ID = "src-cambridge-hopkins"
EVIDENCE_NOTE = (
    "Metadata edge from Cambridge/Hopkins finding-list crosswalk staging; "
    "not a formal obi-* inscription record, object identification, or textual reading."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def safe_token(value: str) -> str:
    token = re.sub(r"[^0-9A-Za-z]+", "-", value.strip()).strip("-").lower()
    return token or "unassigned"


def has_external_ref(value: str) -> bool:
    stripped = value.strip()
    return bool(stripped) and set(stripped) != {"*"}


def group_node_id(group_number: str) -> str:
    stripped = group_number.strip()
    if stripped.isdigit():
        return f"cam-hopkins-group-{int(stripped):02d}"
    return f"cam-hopkins-group-{safe_token(stripped)}"


def crosswalk_project_id_map(inscription_map_rows: list[dict[str, str]]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for row in inscription_map_rows:
        if row.get("record_type") != "inscription_crosswalk_candidate":
            continue
        project_id = row.get("project_id", "")
        for external_ref in row.get("all_external_ref_ids", "").split(";"):
            if external_ref.startswith("cam-hopkins-crosswalk-"):
                mapping[external_ref] = project_id
    return mapping


def make_edge(edge_id: str, source_node_id: str, edge_type: str, target_node_id: str) -> dict[str, object]:
    return {
        "edge_id": edge_id,
        "source_node_id": source_node_id,
        "edge_type": edge_type,
        "target_node_id": target_node_id,
        "confidence_level": "high",
        "source_ids": [SOURCE_ID],
        "evidence_note": EVIDENCE_NOTE,
        "review_status": "reviewed",
    }


def build_edges(
    crosswalk_rows: list[dict[str, str]],
    crosswalk_to_project_id: dict[str, str] | None = None,
) -> list[dict[str, object]]:
    edges: list[dict[str, object]] = []
    crosswalk_to_project_id = crosswalk_to_project_id or {}
    external_ref_specs = [
        ("yingguo_ref_id", "HAS_CAMBRIDGE_HOPKINS_YINGGUO_REF", "cam-hopkins-yingguo"),
        ("cul_ref_id", "HAS_CAMBRIDGE_HOPKINS_CUL_REF", "cam-hopkins-cul"),
        ("chalfant_ref_id", "HAS_CAMBRIDGE_HOPKINS_CHALFANT_REF", "cam-hopkins-chalfant"),
        ("heji_ref_id", "HAS_CAMBRIDGE_HOPKINS_HEJI_REF", "cam-hopkins-heji"),
    ]
    for index, row in enumerate(crosswalk_rows, start=1):
        crosswalk_id = row["candidate_inscription_crosswalk_id"]
        source_node_id = crosswalk_to_project_id.get(crosswalk_id, crosswalk_id)
        group_number = row.get("group_number", "")
        period_label = row.get("period_label", "")
        download_id = row.get("evidence_download_id", "")
        edges.extend(
            [
                make_edge(
                    f"edge-cam-hopkins-crosswalk-source-{index:04d}",
                    source_node_id,
                    "HAS_CAMBRIDGE_HOPKINS_SOURCE",
                    row.get("source_id", SOURCE_ID),
                ),
                make_edge(
                    f"edge-cam-hopkins-crosswalk-download-{index:04d}",
                    source_node_id,
                    "HAS_CAMBRIDGE_HOPKINS_DOWNLOAD_RECORD",
                    download_id,
                ),
                make_edge(
                    f"edge-cam-hopkins-crosswalk-period-{index:04d}",
                    source_node_id,
                    "HAS_CAMBRIDGE_HOPKINS_PERIOD_LABEL",
                    f"cam-hopkins-period-{safe_token(period_label)}",
                ),
                make_edge(
                    f"edge-cam-hopkins-crosswalk-group-{index:04d}",
                    source_node_id,
                    "HAS_CAMBRIDGE_HOPKINS_CLASSIFICATION_GROUP",
                    group_node_id(group_number),
                ),
            ]
        )
        for field_name, edge_type, target_prefix in external_ref_specs:
            external_ref = row.get(field_name, "")
            if not has_external_ref(external_ref):
                continue
            edges.append(
                make_edge(
                    f"edge-cam-hopkins-crosswalk-{safe_token(field_name)}-{index:04d}",
                    source_node_id,
                    edge_type,
                    f"{target_prefix}-{safe_token(external_ref)}",
                )
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
    parser.add_argument("--crosswalk-staging", default=str(DEFAULT_CROSSWALK_STAGING))
    parser.add_argument("--inscription-map", default=str(DEFAULT_INSCRIPTION_MAP))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    crosswalk_rows = read_csv_rows(root / args.crosswalk_staging)
    inscription_map_rows = read_csv_rows(root / args.inscription_map)
    edges = build_edges(crosswalk_rows, crosswalk_project_id_map(inscription_map_rows))
    write_jsonl(root / args.output, edges)
    print(f"wrote={len(edges)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
