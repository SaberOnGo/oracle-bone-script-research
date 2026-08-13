#!/usr/bin/env python3
"""Build explicit candidate routes for EVOBC later-era co-membership."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_CATEGORY_STAGING = Path(
    "corpus/004_bronze-seal-modern-correspondences/"
    "000_evolution-registers/001_evobc-evolution-category-staging.csv"
)
DEFAULT_CODEBOOK_STAGING = Path(
    "corpus/004_bronze-seal-modern-correspondences/"
    "000_evolution-registers/002_evobc-era-source-codebook-staging.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/008_relationship-graph/"
    "017_evobc-evolution-correspondence-candidate-graph-edges.jsonl"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def parse_compact_counts(value: str) -> dict[int, int]:
    counts: dict[int, int] = {}
    for part in value.split(";"):
        if part:
            code, raw_count = part.rsplit(":", 1)
            counts[int(code)] = int(raw_count)
    return counts


def build_edges(
    category_rows: list[dict[str, str]],
    codebook_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    codebook_by_value = {
        int(row["code_value"]): row
        for row in codebook_rows
        if row.get("code_type") == "era"
    }
    edges: list[dict[str, object]] = []
    for row in category_rows:
        era_counts = parse_compact_counts(row.get("era_code_counts", ""))
        later_codes = [code for code in era_counts if code > 0]
        if 0 not in era_counts or not later_codes:
            continue
        category_id = row.get("source_category_id", "")
        if not category_id.isdigit():
            raise ValueError(f"non-numeric EVOBC category id: {category_id}")
        for later_code in later_codes:
            codebook = codebook_by_value.get(later_code)
            if codebook is None:
                raise ValueError(f"missing later-era codebook row: {later_code}")
            edges.append(
                {
                    "edge_id": (
                        f"edge-evobc-correspondence-candidate-"
                        f"{int(category_id):05d}-{later_code:02d}"
                    ),
                    "source_node_id": row["candidate_evolution_category_id"],
                    "edge_type": (
                        "EVOBC_CATEGORY_HAS_LATER_ERA_CORRESPONDENCE_CANDIDATE"
                    ),
                    "target_node_id": codebook["codebook_row_id"],
                    "confidence_level": "unknown",
                    "confidence_semantics": "hypothesis_probability_not_estimated",
                    "route_integrity_confidence": "high",
                    "source_ids": ["src-evobc"],
                    "review_status": "needs_cross_source_review",
                    "candidate_route_status": "dataset_candidate_not_promoted",
                    "candidate_correspondence_status": (
                        "candidate_evolution_correspondence_route"
                    ),
                    "identity_claim_status": "no_identity_claim",
                    "rights_status": row.get(
                        "rights_status", "source_marked_risk_noted"
                    ),
                    "source_category_id": category_id,
                    "source_character_label": row.get("source_character_label", ""),
                    "oracle_bone_era_code": 0,
                    "later_era_code": later_code,
                    "later_era_label": codebook.get("label_en", ""),
                    "category_image_reference_count": int(
                        row.get("image_reference_count", "0") or 0
                    ),
                    "later_era_image_reference_count": int(
                        codebook.get("image_reference_count", "0") or 0
                    ),
                    "route_files": [
                        DEFAULT_CATEGORY_STAGING.as_posix(),
                        DEFAULT_CODEBOOK_STAGING.as_posix(),
                        "corpus/004_bronze-seal-modern-correspondences/"
                        "018_src-evobc_source-object/10_source-evidence-dossier.md",
                    ],
                    "missing_evidence": [
                        "original image member and checksum for this category",
                        "catalog and period locator for both era forms",
                        "independent paleographic comparison",
                        "inscription context and opposing classification",
                    ],
                    "evidence_note": (
                        "EVOBC metadata places an Oracle Bone Characters code and "
                        "a later-era code in one dataset category. This is a "
                        "candidate co-membership route, not a confirmed later-form "
                        "correspondence and not a decipherment conclusion."
                    ),
                }
            )
    if not edges:
        raise ValueError("no EVOBC correspondence candidate edges were built")
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
    edges = build_edges(
        read_csv_rows(root / args.category_staging),
        read_csv_rows(root / args.codebook_staging),
    )
    write_jsonl(root / args.output, edges)
    print(f"wrote={len(edges)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
