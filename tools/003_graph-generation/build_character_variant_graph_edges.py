#!/usr/bin/env python3
"""Build candidate character-variant routes from OBIMD hierarchy staging.

The OBIMD sub-character/main-character relation is dataset metadata.  This
builder preserves it as a review route and never promotes it to a paleographic
variant judgment or an oracle-character identity claim.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_STAGING = Path(
    "corpus/003_graphemic-components/000_component-registers/"
    "002_obimd-subcharacter-main-staging.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/008_relationship-graph/014_character-variant-graph-edges.jsonl"
)
SOURCE_ID = "src-obimd"
RELATION = "CHARACTER_HAS_VARIANT_CANDIDATE"
RISK_NOTE = (
    "OBIMD sub-character/main-character hierarchy is dataset metadata. "
    "It requires visual, source, and scholarly review before any formal "
    "variant or character identity record is created."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def build_edges(rows: list[dict[str, str]], staging_path: Path) -> list[dict[str, object]]:
    edges: list[dict[str, object]] = []
    seen: set[str] = set()
    for index, row in enumerate(rows, start=1):
        candidate_id = row.get("candidate_subcharacter_id", "")
        sub_ref = row.get("subcharacter_external_ref_id", "")
        main_ref = row.get("main_character_external_ref_id", "")
        main_uid = row.get("source_main_character_uid", "")
        if not candidate_id or not sub_ref or not main_ref or not main_uid:
            raise ValueError(f"incomplete OBIMD variant staging row: {row}")
        edge_id = f"edge-character-variant-obimd-{index:06d}"
        if edge_id in seen:
            raise ValueError(f"duplicate edge id: {edge_id}")
        seen.add(edge_id)
        edges.append(
            {
                "edge_id": edge_id,
                "source_node_id": f"obs-comp-cand-{index:06d}",
                "edge_type": RELATION,
                "target_node_id": main_ref,
                "confidence_level": "high",
                "source_ids": [SOURCE_ID],
                "evidence_note": (
                    "OBIMD sub-character/main-character hierarchy route only; "
                    "this is not a formal variant relation, not an oracle-character "
                    "identity claim, not an accepted reading, and not a decipherment conclusion."
                ),
                "review_status": "needs_cross_source_review",
                "candidate_relation": row.get("relation_type", "subcharacter_belongs_to_main_character"),
                "variant_candidate_id": row.get("obimd_subcharacter_candidate_id", "")
                or row.get("obimd_subcharacter_id", "")
                or sub_ref,
                "subcharacter_external_ref_id": sub_ref,
                "main_character_external_ref_id": main_ref,
                "source_subcharacter_uid": row.get("source_subcharacter_uid", ""),
                "source_main_character_uid": main_uid,
                "source_staging_path": staging_path.as_posix(),
                "rights_status": row.get("rights_status", "licensed_for_repository"),
                "risk_note": RISK_NOTE,
                "promotion_status": row.get("promotion_status", "dataset_candidate_not_promoted"),
                "review_scope": "human_visual_and_cross_source_variant_review_pending",
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
    parser.add_argument("--staging", default=str(DEFAULT_STAGING))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)
    root = repo_root()
    staging = Path(args.staging)
    if not staging.is_absolute():
        staging = root / staging
    output = Path(args.output)
    if not output.is_absolute():
        output = root / output
    rows = read_csv_rows(staging)
    edges = build_edges(rows, staging.relative_to(root))
    write_jsonl(output, edges)
    print(f"wrote={len(edges)} output={output.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
