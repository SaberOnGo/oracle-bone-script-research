#!/usr/bin/env python3
"""Build HUST-OBC source-category staging rows from validation labels."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_VALIDATION_STAGING = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "005_hust-obc-validation-class-staging.csv"
)
DEFAULT_ID_TO_CHINESE = Path("tmp/source_downloads/dl-hust-obc-ocr-id-to-chinese.json")
DEFAULT_OUTPUT = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "008_hust-obc-source-category-staging.csv"
)

OUTPUT_FIELDS = [
    "source_category_row_id",
    "source_id",
    "evidence_download_id_validation",
    "evidence_download_id_id_to_chinese",
    "source_category_id",
    "source_category_id_padded",
    "source_modern_label_candidate",
    "source_modern_label_codepoint",
    "validation_class_id",
    "linked_candidate_class_id",
    "linked_label_crosswalk_id",
    "is_part_of_multi_category_class",
    "source_metadata_files",
    "project_import_status",
    "rights_status",
    "caution",
    "review_status",
    "updated_at",
]

CAUTION = (
    "HUST-OBC source-category labels are dataset metadata for candidate lookup; do not "
    "treat them as accepted oracle-character readings or formal project character IDs "
    "without cross-source review."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def build_rows(validation_rows: list[dict[str, str]], id_to_chinese: dict[str, str]) -> list[dict[str, str]]:
    category_rows: dict[str, dict[str, str]] = {}
    for class_index, row in enumerate(validation_rows, start=1):
        category_ids = row["source_category_id"].split("_")
        is_multi = len(category_ids) > 1
        for category_id in category_ids:
            padded_id = category_id.zfill(5)
            try:
                label = id_to_chinese[padded_id]
            except KeyError as error:
                raise ValueError(f"missing HUST OCR ID_to_Chinese mapping for {padded_id}") from error
            if len(label) != 1:
                raise ValueError(f"HUST source category {category_id} mapped to non-single label: {label!r}")
            if category_id in category_rows:
                raise ValueError(f"duplicate HUST source category ID: {category_id}")
            category_rows[category_id] = {
                "source_category_row_id": f"hust-obc-src-cat-{int(category_id):04d}",
                "source_id": "src-hust-obc",
                "evidence_download_id_validation": "dl-hust-obc-validation-label",
                "evidence_download_id_id_to_chinese": "dl-hust-obc-ocr-id-to-chinese",
                "source_category_id": category_id,
                "source_category_id_padded": padded_id,
                "source_modern_label_candidate": label,
                "source_modern_label_codepoint": f"U+{ord(label):04X}",
                "validation_class_id": row["validation_class_id"],
                "linked_candidate_class_id": row["candidate_class_id"],
                "linked_label_crosswalk_id": f"hust-obc-label-xwalk-{class_index:04d}",
                "is_part_of_multi_category_class": str(is_multi).lower(),
                "source_metadata_files": "Validation_label.json;ID_to_Chinese.json",
                "project_import_status": "dataset_source_category_not_promoted",
                "rights_status": "source_marked_risk_noted",
                "caution": CAUTION,
                "review_status": "reviewed_metadata_only",
                "updated_at": "2026-06-04",
            }
    return [
        category_rows[category_id]
        for category_id in sorted(category_rows, key=lambda value: int(value))
    ]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation-staging", default=str(DEFAULT_VALIDATION_STAGING))
    parser.add_argument("--id-to-chinese", default=str(DEFAULT_ID_TO_CHINESE))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    validation_rows = read_csv_rows(root / args.validation_staging)
    id_to_chinese = json.loads((root / args.id_to_chinese).read_text(encoding="utf-8"))
    output_rows = build_rows(validation_rows, id_to_chinese)
    write_csv(root / args.output, output_rows)

    multi_count = sum(row["is_part_of_multi_category_class"] == "true" for row in output_rows)
    print(
        f"wrote={len(output_rows)} multi_category_members={multi_count} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
