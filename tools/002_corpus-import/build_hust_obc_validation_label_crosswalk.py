#!/usr/bin/env python3
"""Build HUST-OBC validation-label to OCR-label crosswalk staging."""

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
    "007_hust-obc-validation-label-crosswalk-staging.csv"
)

OUTPUT_FIELDS = [
    "candidate_label_crosswalk_id",
    "candidate_class_id",
    "source_id",
    "evidence_download_id_validation",
    "evidence_download_id_id_to_chinese",
    "source_category_id",
    "source_category_id_padded",
    "validation_class_id",
    "source_modern_label_candidate",
    "source_modern_label_codepoints",
    "label_component_count",
    "has_multi_component_label",
    "source_metadata_files",
    "project_import_status",
    "rights_status",
    "caution",
    "review_status",
    "updated_at",
]

CAUTION = (
    "HUST-OBC OCR labels are dataset metadata for candidate lookup; do not treat "
    "them as accepted oracle-character readings without cross-source review."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def codepoint_sequence(value: str) -> str:
    return ";".join(f"U+{ord(character):04X}" for character in value)


def build_rows(validation_rows: list[dict[str, str]], id_to_chinese: dict[str, str]) -> list[dict[str, str]]:
    output_rows: list[dict[str, str]] = []
    for index, row in enumerate(validation_rows, start=1):
        source_ids = row["source_category_id"].split("_")
        padded_ids = [source_id.zfill(5) for source_id in source_ids]
        labels = []
        for padded_id in padded_ids:
            try:
                labels.append(id_to_chinese[padded_id])
            except KeyError as error:
                raise ValueError(f"missing HUST OCR ID_to_Chinese mapping for {padded_id}") from error
        label = "".join(labels)
        output_rows.append(
            {
                "candidate_label_crosswalk_id": f"hust-obc-label-xwalk-{index:04d}",
                "candidate_class_id": row["candidate_class_id"],
                "source_id": "src-hust-obc",
                "evidence_download_id_validation": "dl-hust-obc-validation-label",
                "evidence_download_id_id_to_chinese": "dl-hust-obc-ocr-id-to-chinese",
                "source_category_id": row["source_category_id"],
                "source_category_id_padded": ";".join(padded_ids),
                "validation_class_id": row["validation_class_id"],
                "source_modern_label_candidate": label,
                "source_modern_label_codepoints": codepoint_sequence(label),
                "label_component_count": str(len(labels)),
                "has_multi_component_label": str(len(labels) > 1).lower(),
                "source_metadata_files": "Validation_label.json;ID_to_Chinese.json",
                "project_import_status": "dataset_label_candidate_not_promoted",
                "rights_status": "source_marked_risk_noted",
                "caution": CAUTION,
                "review_status": "reviewed_metadata_only",
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
    parser.add_argument("--id-to-chinese", default=str(DEFAULT_ID_TO_CHINESE))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    validation_rows = read_csv_rows(root / args.validation_staging)
    id_to_chinese = json.loads((root / args.id_to_chinese).read_text(encoding="utf-8"))
    output_rows = build_rows(validation_rows, id_to_chinese)
    write_csv(root / args.output, output_rows)

    multi_count = sum(row["has_multi_component_label"] == "true" for row in output_rows)
    print(
        f"wrote={len(output_rows)} multi_component={multi_count} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
