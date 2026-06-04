#!/usr/bin/env python3
"""Build a review queue for promoting HUST-OBC candidates to obs-char records."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


DEFAULT_VALIDATION_STAGING = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "005_hust-obc-validation-class-staging.csv"
)
DEFAULT_LABEL_CROSSWALK = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "007_hust-obc-validation-label-crosswalk-staging.csv"
)
DEFAULT_SOURCE_CATEGORY_STAGING = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "008_hust-obc-source-category-staging.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "009_hust-obc-obs-char-promotion-review-queue.csv"
)

OUTPUT_FIELDS = [
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
    "reported_decipherment_scope",
    "suggested_decipherment_status",
    "assignment_status",
    "promotion_status",
    "required_next_review",
    "source_metadata_files",
    "rights_status",
    "caution",
    "review_status",
    "updated_at",
]

CAUTION = (
    "This row is a promotion-review queue item only. The suggested obs-char ID is not "
    "assigned until cross-source review confirms provenance, form identity, and "
    "decipherment status. HUST-OBC labels must not be treated as accepted readings."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def bucket_directory_for_index(index: int) -> str:
    bucket_number = ((index - 1) // 100) + 1
    bucket_start = ((index - 1) // 100) * 100 + 1
    bucket_end = bucket_start + 99
    return (
        f"{bucket_number:03d}_{bucket_start:06d}-{bucket_end:06d}"
        "_obs-char-bucket_oracle-characters"
    )


def build_rows(
    validation_rows: list[dict[str, str]],
    label_crosswalk_rows: list[dict[str, str]],
    source_category_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    label_by_candidate = {
        row["candidate_class_id"]: row
        for row in label_crosswalk_rows
    }
    source_categories_by_candidate: dict[str, list[dict[str, str]]] = {}
    for row in source_category_rows:
        source_categories_by_candidate.setdefault(row["linked_candidate_class_id"], []).append(row)

    output_rows: list[dict[str, str]] = []
    for index, validation_row in enumerate(validation_rows, start=1):
        candidate_id = validation_row["candidate_class_id"]
        try:
            label_row = label_by_candidate[candidate_id]
        except KeyError as error:
            raise ValueError(f"missing HUST label crosswalk for {candidate_id}") from error
        category_rows = source_categories_by_candidate.get(candidate_id, [])
        if not category_rows:
            raise ValueError(f"missing HUST source-category rows for {candidate_id}")
        category_rows = sorted(category_rows, key=lambda row: int(row["source_category_id"]))

        suggested_id = f"obs-char-{index:06d}"
        primary_external_ref_id = validation_row["primary_external_ref_id"]
        bucket_directory = bucket_directory_for_index(index)
        output_rows.append(
            {
                "promotion_queue_id": f"hust-obc-obs-char-promo-{index:06d}",
                "suggested_oracle_character_id": suggested_id,
                "suggested_bucket_directory": bucket_directory,
                "suggested_character_directory": (
                    f"{index:03d}_{suggested_id}_{primary_external_ref_id}_oracle-character"
                ),
                "candidate_class_id": candidate_id,
                "source_id": "src-hust-obc",
                "primary_external_ref_id": primary_external_ref_id,
                "source_category_id": validation_row["source_category_id"],
                "source_category_id_padded": label_row["source_category_id_padded"],
                "validation_class_id": validation_row["validation_class_id"],
                "candidate_label_crosswalk_id": label_row["candidate_label_crosswalk_id"],
                "source_modern_label_candidate": label_row["source_modern_label_candidate"],
                "source_modern_label_codepoints": label_row["source_modern_label_codepoints"],
                "label_component_count": label_row["label_component_count"],
                "has_multi_component_label": label_row["has_multi_component_label"],
                "source_category_member_count": str(len(category_rows)),
                "source_category_row_ids": ";".join(row["source_category_row_id"] for row in category_rows),
                "reported_decipherment_scope": validation_row["reported_decipherment_scope"],
                "suggested_decipherment_status": "unknown_until_cross_source_review",
                "assignment_status": "reserved_candidate_not_assigned",
                "promotion_status": "needs_cross_source_review",
                "required_next_review": (
                    "compare_xiaoxuetang_obm_obimd_evobc_and_primary_inscription_context"
                ),
                "source_metadata_files": "Validation_label.json;ID_to_Chinese.json",
                "rights_status": "source_marked_risk_noted",
                "caution": CAUTION,
                "review_status": "needs_review",
                "updated_at": "2026-06-04",
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
    parser.add_argument("--validation-staging", default=str(DEFAULT_VALIDATION_STAGING))
    parser.add_argument("--label-crosswalk", default=str(DEFAULT_LABEL_CROSSWALK))
    parser.add_argument("--source-category-staging", default=str(DEFAULT_SOURCE_CATEGORY_STAGING))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_rows(
        read_csv_rows(root / args.validation_staging),
        read_csv_rows(root / args.label_crosswalk),
        read_csv_rows(root / args.source_category_staging),
    )
    write_csv(root / args.output, rows)

    multi_count = sum(row["has_multi_component_label"] == "true" for row in rows)
    print(f"wrote={len(rows)} multi_component_labels={multi_count} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
