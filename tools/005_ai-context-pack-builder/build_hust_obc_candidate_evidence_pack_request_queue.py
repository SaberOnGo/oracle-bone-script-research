#!/usr/bin/env python3
"""Build per-candidate AI evidence-pack requests for HUST-OBC review."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_PROMOTION_QUEUE = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "009_hust-obc-obs-char-promotion-review-queue.csv"
)
DEFAULT_ROUTE_PACK = Path(
    "corpus/009_statistics-and-derived-features/"
    "004_ai-agent-hust-obc-bucket-review-route-pack.json"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv"
)
UPDATED_AT = "2026-06-04"

REQUIRED_EVIDENCE_PACK_SECTIONS = [
    "character_or_unknown_glyph_id",
    "source_references_and_asset_metadata",
    "full_inscription_context",
    "neighboring_characters",
    "component_breakdown_and_variant_notes",
    "excavation_period_and_catalog_provenance",
    "bronze_seal_or_modern_comparanda",
    "supporting_evidence",
    "opposing_evidence",
    "open_questions_and_next_checks",
]

OUTPUT_FIELDS = [
    "evidence_request_id",
    "route_pack_id",
    "promotion_queue_id",
    "suggested_oracle_character_id",
    "candidate_class_id",
    "bucket_summary_id",
    "bucket_number",
    "bucket_manifest_path",
    "primary_external_ref_id",
    "source_category_id",
    "source_modern_label_codepoints",
    "has_multi_component_label",
    "source_category_member_count",
    "route_files",
    "source_route_requirement_ids",
    "evidence_gap_types",
    "required_evidence_pack_sections",
    "draft_output_path",
    "draft_status",
    "assignment_status",
    "promotion_status",
    "review_status",
    "caution",
    "updated_at",
]

CAUTION = (
    "This is an AI evidence-pack request only. It must not be treated as a "
    "decipherment result or formal obs-char assignment. Draft output belongs under "
    "doc/public/user_research/ until human review."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _bucket_number(bucket_directory: str) -> str:
    return bucket_directory.split("_", 1)[0]


def _draft_output_path(row: dict[str, str], bucket_number: str) -> str:
    bucket_short = row["suggested_bucket_directory"].replace(
        "_obs-char-bucket_oracle-characters",
        "_obs-char-bucket",
    )
    return (
        "doc/public/user_research/001_ai-agent-evidence-packs/hust-obc/"
        f"{bucket_short}/"
        f"{bucket_number}_{row['suggested_oracle_character_id']}_"
        f"{row['primary_external_ref_id']}_evidence-pack-draft.json"
    )


def build_request_rows(
    promotion_queue_rows: list[dict[str, str]],
    route_pack: dict[str, object],
) -> list[dict[str, str]]:
    route_pack_id = str(route_pack["context_pack_id"])
    route_by_bucket = {
        route["bucket_directory"]: route
        for route in route_pack["bucket_routes"]
        if isinstance(route, dict)
    }
    source_route_requirement_ids = ";".join(
        requirement["source_id"]
        for requirement in route_pack["source_route_requirements"]
        if isinstance(requirement, dict)
    )
    output_rows: list[dict[str, str]] = []
    for index, row in enumerate(promotion_queue_rows, start=1):
        bucket_directory = row["suggested_bucket_directory"]
        route = route_by_bucket[bucket_directory]
        bucket_number = _bucket_number(bucket_directory)
        output_rows.append(
            {
                "evidence_request_id": f"hust-obc-evidence-request-{index:06d}",
                "route_pack_id": route_pack_id,
                "promotion_queue_id": row["promotion_queue_id"],
                "suggested_oracle_character_id": row["suggested_oracle_character_id"],
                "candidate_class_id": row["candidate_class_id"],
                "bucket_summary_id": str(route["bucket_summary_id"]),
                "bucket_number": bucket_number,
                "bucket_manifest_path": str(route["manifest_path"]),
                "primary_external_ref_id": row["primary_external_ref_id"],
                "source_category_id": row["source_category_id"],
                "source_modern_label_codepoints": row["source_modern_label_codepoints"],
                "has_multi_component_label": row["has_multi_component_label"],
                "source_category_member_count": row["source_category_member_count"],
                "route_files": ";".join(str(path) for path in route["route_files"]),
                "source_route_requirement_ids": source_route_requirement_ids,
                "evidence_gap_types": ";".join(str(value) for value in route["evidence_gap_types"]),
                "required_evidence_pack_sections": ";".join(REQUIRED_EVIDENCE_PACK_SECTIONS),
                "draft_output_path": _draft_output_path(row, bucket_number),
                "draft_status": "not_started",
                "assignment_status": row["assignment_status"],
                "promotion_status": row["promotion_status"],
                "review_status": "needs_evidence_pack",
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return output_rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--promotion-queue", default=str(DEFAULT_PROMOTION_QUEUE))
    parser.add_argument("--route-pack", default=str(DEFAULT_ROUTE_PACK))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_request_rows(
        read_csv_rows(root / args.promotion_queue),
        read_json(root / args.route_pack),
    )
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
