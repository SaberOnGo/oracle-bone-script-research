#!/usr/bin/env python3
"""Build graph edges for HUST-OBC candidate class/category metadata."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_VALIDATION_STAGING = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "005_hust-obc-validation-class-staging.csv"
)
DEFAULT_SOURCE_CATEGORY_STAGING = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "008_hust-obc-source-category-staging.csv"
)
DEFAULT_OUTPUT = Path("corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def build_edges(
    validation_rows: list[dict[str, str]],
    source_category_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    validation_by_candidate = {
        row["candidate_class_id"]: row
        for row in validation_rows
    }
    edges: list[dict[str, object]] = []

    for index, row in enumerate(source_category_rows, start=1):
        candidate_id = row["linked_candidate_class_id"]
        if candidate_id not in validation_by_candidate:
            raise ValueError(f"missing validation candidate for {candidate_id}")
        source_category_node_id = row["source_category_row_id"]
        edges.append(
            {
                "edge_id": f"edge-hust-obc-class-src-cat-{index:04d}",
                "source_node_id": candidate_id,
                "edge_type": "HAS_HUST_OBC_SOURCE_CATEGORY",
                "target_node_id": source_category_node_id,
                "confidence_level": "high",
                "source_ids": ["src-hust-obc"],
                "evidence_note": (
                    "Dataset metadata edge from HUST-OBC Validation_label.json; "
                    "not a formal oracle-character identity claim."
                ),
                "review_status": "reviewed",
            }
        )

    for index, row in enumerate(source_category_rows, start=1):
        label_node_id = f"hust-obc-ocr-label-{row['source_modern_label_codepoint'].lower().replace('+', '')}"
        edges.append(
            {
                "edge_id": f"edge-hust-obc-src-cat-label-{index:04d}",
                "source_node_id": row["source_category_row_id"],
                "edge_type": "HAS_HUST_OBC_OCR_LABEL_CANDIDATE",
                "target_node_id": label_node_id,
                "confidence_level": "high",
                "source_ids": ["src-hust-obc"],
                "evidence_note": (
                    "Dataset metadata edge from HUST-OBC ID_to_Chinese.json; "
                    "OCR label candidates are not accepted paleographic readings."
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
    parser.add_argument("--validation-staging", default=str(DEFAULT_VALIDATION_STAGING))
    parser.add_argument("--source-category-staging", default=str(DEFAULT_SOURCE_CATEGORY_STAGING))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    validation_rows = read_csv_rows(root / args.validation_staging)
    source_category_rows = read_csv_rows(root / args.source_category_staging)
    edges = build_edges(validation_rows, source_category_rows)
    write_jsonl(root / args.output, edges)

    print(f"wrote={len(edges)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
