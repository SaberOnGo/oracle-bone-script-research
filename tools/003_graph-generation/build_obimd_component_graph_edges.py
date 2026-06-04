#!/usr/bin/env python3
"""Build graph edges for OBIMD component and glyph metadata."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_MAIN_STAGING = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "006_obimd-main-character-staging.csv"
)
DEFAULT_SUBCHARACTER_MAIN_STAGING = Path(
    "corpus/003_graphemic-components/000_component-registers/"
    "002_obimd-subcharacter-main-staging.csv"
)
DEFAULT_SUBCHARACTER_GLYPH_STAGING = Path(
    "corpus/003_graphemic-components/000_component-registers/"
    "003_obimd-subcharacter-glyph-staging.csv"
)
DEFAULT_OUTPUT = Path("corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def glyph_codepoint_node_id(codepoints: str) -> str:
    compact = codepoints.lower().replace("+", "").replace(";", "-")
    return f"obimd-glyph-codepoint-{compact}"


def build_edges(
    main_rows: list[dict[str, str]],
    subcharacter_main_rows: list[dict[str, str]],
    subcharacter_glyph_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    _ = main_rows
    subcandidate_by_uid = {
        row["source_subcharacter_uid"]: row["candidate_subcharacter_id"]
        for row in subcharacter_main_rows
    }
    edges: list[dict[str, object]] = []

    for index, row in enumerate(subcharacter_main_rows, start=1):
        sub_uid = row["source_subcharacter_uid"]
        main_uid = row["source_main_character_uid"]
        if sub_uid not in subcandidate_by_uid:
            raise ValueError(f"missing OBIMD subcharacter candidate for {sub_uid}")
        if not main_uid:
            raise ValueError("missing OBIMD main UID")
        edges.append(
            {
                "edge_id": f"edge-obimd-sub-main-{index:06d}",
                "source_node_id": subcandidate_by_uid[sub_uid],
                "edge_type": "OBIMD_SUBCHARACTER_OF_MAIN_CHARACTER",
                "target_node_id": row["main_character_external_ref_id"],
                "confidence_level": "high",
                "source_ids": ["src-obimd"],
                "evidence_note": (
                    "Dataset metadata edge from OBIMD Sub-character to Main-character Mapping.xlsx; "
                    "not a formal component analysis or oracle-character identity claim."
                ),
                "review_status": "reviewed",
            }
        )

    for index, row in enumerate(subcharacter_glyph_rows, start=1):
        sub_uid = row["source_subcharacter_uid"]
        if sub_uid not in subcandidate_by_uid:
            raise ValueError(f"missing OBIMD subcharacter candidate for glyph link {sub_uid}")
        edges.append(
            {
                "edge_id": f"edge-obimd-sub-glyph-{index:06d}",
                "source_node_id": subcandidate_by_uid[sub_uid],
                "edge_type": "OBIMD_SUBCHARACTER_HAS_GLYPH_CODEPOINT",
                "target_node_id": glyph_codepoint_node_id(row["glyph_codepoint_uplus"]),
                "confidence_level": "high",
                "source_ids": ["src-obimd"],
                "evidence_note": (
                    "Dataset metadata edge from OBIMD Sub-character to Glyph Code Point Mapping.xlsx; "
                    "glyph code points may include private-use code points and are not formal image assets."
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
    parser.add_argument("--main-staging", default=str(DEFAULT_MAIN_STAGING))
    parser.add_argument("--subcharacter-main-staging", default=str(DEFAULT_SUBCHARACTER_MAIN_STAGING))
    parser.add_argument("--subcharacter-glyph-staging", default=str(DEFAULT_SUBCHARACTER_GLYPH_STAGING))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    main_rows = read_csv_rows(root / args.main_staging)
    subcharacter_main_rows = read_csv_rows(root / args.subcharacter_main_staging)
    subcharacter_glyph_rows = read_csv_rows(root / args.subcharacter_glyph_staging)
    edges = build_edges(main_rows, subcharacter_main_rows, subcharacter_glyph_rows)
    write_jsonl(root / args.output, edges)

    print(f"wrote={len(edges)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
