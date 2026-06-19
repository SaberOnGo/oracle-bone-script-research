#!/usr/bin/env python3
"""Build candidate cross-source lookup-route graph edges from codepoint staging."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_CROSSWALK = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "011_hust-obimd-evobc-codepoint-crosswalk-staging.csv"
)
DEFAULT_OUTPUT = Path("corpus/008_relationship-graph/010_cross-source-id-graph-edges.jsonl")

EDGE_SPECS = [
    (
        "hust",
        "hust_primary_external_ref_id",
        "CHARACTER_HAS_HUST_OBC_CODEPOINT_LOOKUP_ROUTE",
    ),
    (
        "obimd",
        "obimd_candidate_main_character_ids",
        "CHARACTER_HAS_OBIMD_CODEPOINT_LOOKUP_ROUTE",
    ),
    (
        "evobc",
        "evobc_candidate_evolution_category_ids",
        "CHARACTER_HAS_EVOBC_CODEPOINT_LOOKUP_ROUTE",
    ),
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_values(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def build_edges(crosswalk_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    edges: list[dict[str, object]] = []
    for row in crosswalk_rows:
        source_node_id = row.get("suggested_oracle_character_id", "")
        if not source_node_id:
            raise ValueError(f"crosswalk row missing suggested_oracle_character_id: {row}")
        source_ids = split_values(row.get("matched_source_ids", ""))
        if not source_ids:
            raise ValueError(f"crosswalk row missing matched_source_ids: {row.get('crosswalk_candidate_id', '')}")
        for source_key, target_field, edge_type in EDGE_SPECS:
            for target_index, target_node_id in enumerate(split_values(row.get(target_field, "")), start=1):
                edges.append(
                    {
                        "edge_id": (
                            "edge-cross-source-id-"
                            f"{row['crosswalk_candidate_id']}-{source_key}-{target_index:03d}"
                        ),
                        "source_node_id": source_node_id,
                        "edge_type": edge_type,
                        "target_node_id": target_node_id,
                        "confidence_level": "high",
                        "source_ids": source_ids,
                        "evidence_note": (
                            "Codepoint lookup-route edge from HUST/OBIMD/EVOBC crosswalk staging; "
                            "exact dataset-label codepoint matches are not confirmed oracle-character "
                            "identity, not accepted readings, not component assignments, not "
                            "evolution-chain assignments, and not decipherment conclusions."
                        ),
                        "review_status": row.get("review_status", "") or "needs_cross_source_review",
                        "crosswalk_candidate_id": row.get("crosswalk_candidate_id", ""),
                        "cross_source_status": row.get("cross_source_status", ""),
                        "identity_claim_status": row.get("identity_claim_status", ""),
                        "promotion_status": row.get("promotion_status", ""),
                        "rights_status": row.get("rights_status", ""),
                        "hust_label_codepoints": row.get("hust_label_codepoints", ""),
                        "route_files": split_values(row.get("route_files", "")),
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
    parser.add_argument("--crosswalk", default=str(DEFAULT_CROSSWALK))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_edges(read_csv_rows(root / args.crosswalk))
    write_jsonl(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
