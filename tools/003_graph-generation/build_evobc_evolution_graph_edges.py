#!/usr/bin/env python3
"""Build graph edges for EVOBC evolution category metadata."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_CATEGORY_STAGING = Path(
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
    "001_evobc-evolution-category-staging.csv"
)
DEFAULT_CODEBOOK_STAGING = Path(
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
    "002_evobc-era-source-codebook-staging.csv"
)
DEFAULT_OUTPUT = Path("corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def parse_compact_counts(value: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    if not value:
        return counts
    for part in value.split(";"):
        if not part:
            continue
        key, raw_count = part.rsplit(":", 1)
        counts[key] = int(raw_count)
    return counts


def build_edges(
    category_rows: list[dict[str, str]],
    codebook_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    codebook_by_type_value = {
        (row["code_type"], row["code_value"]): row
        for row in codebook_rows
    }
    edges: list[dict[str, object]] = []

    for row in category_rows:
        category_node_id = row["candidate_evolution_category_id"]
        category_id = int(row["source_category_id"])
        category_image_count = row["image_reference_count"]
        era_counts = parse_compact_counts(row["era_code_counts"])
        source_counts = parse_compact_counts(row["source_code_counts"])

        for era_code, image_count in era_counts.items():
            codebook_row = codebook_by_type_value.get(("era", era_code))
            if codebook_row is None:
                raise ValueError(f"missing EVOBC era codebook row for {era_code}")
            edges.append(
                {
                    "edge_id": f"edge-evobc-cat-era-{category_id:05d}-{int(era_code):02d}",
                    "source_node_id": category_node_id,
                    "edge_type": "EVOBC_CATEGORY_HAS_ERA_CODE",
                    "target_node_id": codebook_row["codebook_row_id"],
                    "confidence_level": "high",
                    "source_ids": ["src-evobc"],
                    "evidence_note": (
                        "Dataset metadata edge from EVOBC category era_code_counts; "
                        f"category_image_reference_count={category_image_count}; "
                        f"edge_image_reference_count={image_count}; "
                        "not an accepted paleographic correspondence."
                    ),
                    "review_status": "reviewed",
                }
            )

        for source_code, image_count in source_counts.items():
            codebook_row = codebook_by_type_value.get(("source", source_code))
            if codebook_row is None:
                raise ValueError(f"missing EVOBC source codebook row for {source_code}")
            edges.append(
                {
                    "edge_id": f"edge-evobc-cat-source-{category_id:05d}-{int(source_code):02d}",
                    "source_node_id": category_node_id,
                    "edge_type": "EVOBC_CATEGORY_HAS_SOURCE_CODE",
                    "target_node_id": codebook_row["codebook_row_id"],
                    "confidence_level": "high",
                    "source_ids": ["src-evobc"],
                    "evidence_note": (
                        "Dataset metadata edge from EVOBC category source_code_counts; "
                        f"category_image_reference_count={category_image_count}; "
                        f"edge_image_reference_count={image_count}; "
                        "source-code labels are dataset tokens, not authoritative source names."
                    ),
                    "review_status": "reviewed",
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
    parser.add_argument("--category-staging", default=str(DEFAULT_CATEGORY_STAGING))
    parser.add_argument("--codebook-staging", default=str(DEFAULT_CODEBOOK_STAGING))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    category_rows = read_csv_rows(root / args.category_staging)
    codebook_rows = read_csv_rows(root / args.codebook_staging)
    edges = build_edges(category_rows, codebook_rows)
    write_jsonl(root / args.output, edges)

    print(f"wrote={len(edges)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
