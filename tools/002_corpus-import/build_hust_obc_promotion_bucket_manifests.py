#!/usr/bin/env python3
"""Build bucket-level review manifests from the HUST-OBC promotion queue."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


DEFAULT_INPUT = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "009_hust-obc-obs-char-promotion-review-queue.csv"
)
DEFAULT_OUTPUT_ROOT = Path("corpus/001_oracle-characters")
BUCKET_MANIFEST_FILENAME = "000_hust-obc-promotion-bucket-manifest.csv"

OUTPUT_FIELDS = [
    "bucket_manifest_row_id",
    "promotion_queue_id",
    "suggested_oracle_character_id",
    "suggested_bucket_directory",
    "suggested_character_directory",
    "candidate_class_id",
    "source_id",
    "primary_external_ref_id",
    "source_category_id",
    "source_category_id_padded",
    "validation_class_id",
    "candidate_label_crosswalk_id",
    "source_modern_label_candidate",
    "source_modern_label_codepoints",
    "label_component_count",
    "has_multi_component_label",
    "source_category_member_count",
    "source_category_row_ids",
    "suggested_decipherment_status",
    "assignment_status",
    "promotion_status",
    "required_next_review",
    "rights_status",
    "caution",
    "review_status",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def build_bucket_manifests(queue_rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    manifests: dict[str, list[dict[str, str]]] = {}
    for row in queue_rows:
        bucket_directory = row["suggested_bucket_directory"]
        bucket_rows = manifests.setdefault(bucket_directory, [])
        bucket_row_index = len(bucket_rows) + 1
        bucket_number = bucket_directory.split("_", 1)[0]
        output_row = {
            field: row.get(field, "")
            for field in OUTPUT_FIELDS
            if field != "bucket_manifest_row_id"
        }
        output_row["bucket_manifest_row_id"] = (
            f"hust-obc-bucket-{bucket_number}-row-{bucket_row_index:03d}"
        )
        bucket_rows.append(output_row)
    return manifests


def write_bucket_manifests(output_root: Path, manifests: dict[str, list[dict[str, str]]]) -> None:
    for bucket_directory, rows in sorted(manifests.items()):
        output_path = output_root / bucket_directory / BUCKET_MANIFEST_FILENAME
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS)
            writer.writeheader()
            writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    args = parser.parse_args(argv)

    root = repo_root()
    manifests = build_bucket_manifests(read_csv_rows(root / args.input))
    write_bucket_manifests(root / args.output_root, manifests)

    row_count = sum(len(rows) for rows in manifests.values())
    print(
        "wrote_bucket_manifests="
        f"{len(manifests)} rows={row_count} output_root={(root / args.output_root).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
