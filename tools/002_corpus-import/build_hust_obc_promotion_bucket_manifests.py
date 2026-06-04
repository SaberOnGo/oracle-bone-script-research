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
DEFAULT_SUMMARY_OUTPUT = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "010_hust-obc-promotion-bucket-review-summary.csv"
)
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

SUMMARY_FIELDS = [
    "bucket_summary_id",
    "bucket_number",
    "bucket_directory",
    "manifest_path",
    "suggested_oracle_character_id_start",
    "suggested_oracle_character_id_end",
    "promotion_queue_id_start",
    "promotion_queue_id_end",
    "candidate_class_id_start",
    "candidate_class_id_end",
    "row_count",
    "single_component_label_count",
    "multi_component_label_count",
    "multi_source_category_candidate_count",
    "source_category_row_count",
    "source_id_set",
    "assignment_status_set",
    "promotion_status_set",
    "suggested_decipherment_status_set",
    "rights_status_set",
    "review_status_set",
    "required_next_review",
    "ai_agent_batch_action",
    "caution",
    "updated_at",
]

SUMMARY_CAUTION = (
    "Bucket summary is derived from reserved-only HUST-OBC promotion manifests. "
    "The listed obs-char range is not assigned until cross-source review confirms "
    "provenance, form identity, and decipherment status."
)

AI_AGENT_BATCH_ACTION = (
    "review_manifest_rows_against_xiaoxuetang_obm_obimd_evobc_and_primary_inscription_context"
)


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


def _joined_unique_values(rows: list[dict[str, str]], field: str) -> str:
    return ";".join(sorted({row.get(field, "") for row in rows if row.get(field, "")}))


def build_bucket_summary_rows(
    manifests: dict[str, list[dict[str, str]]],
    output_root: Path,
) -> list[dict[str, str]]:
    summary_rows: list[dict[str, str]] = []
    for bucket_directory, rows in sorted(manifests.items()):
        if not rows:
            continue
        bucket_number = int(bucket_directory.split("_", 1)[0])
        source_category_row_count = sum(
            int(row["source_category_member_count"])
            for row in rows
            if row.get("source_category_member_count", "").isdigit()
        )
        multi_source_category_candidate_count = sum(
            1
            for row in rows
            if row.get("source_category_member_count", "").isdigit()
            and int(row["source_category_member_count"]) > 1
        )
        summary_rows.append(
            {
                "bucket_summary_id": f"hust-obc-bucket-summary-{bucket_number:03d}",
                "bucket_number": f"{bucket_number:03d}",
                "bucket_directory": bucket_directory,
                "manifest_path": str(
                    output_root / bucket_directory / BUCKET_MANIFEST_FILENAME
                ).replace("\\", "/"),
                "suggested_oracle_character_id_start": rows[0]["suggested_oracle_character_id"],
                "suggested_oracle_character_id_end": rows[-1]["suggested_oracle_character_id"],
                "promotion_queue_id_start": rows[0]["promotion_queue_id"],
                "promotion_queue_id_end": rows[-1]["promotion_queue_id"],
                "candidate_class_id_start": rows[0]["candidate_class_id"],
                "candidate_class_id_end": rows[-1]["candidate_class_id"],
                "row_count": str(len(rows)),
                "single_component_label_count": str(
                    sum(1 for row in rows if row.get("has_multi_component_label") == "false")
                ),
                "multi_component_label_count": str(
                    sum(1 for row in rows if row.get("has_multi_component_label") == "true")
                ),
                "multi_source_category_candidate_count": str(
                    multi_source_category_candidate_count
                ),
                "source_category_row_count": str(source_category_row_count),
                "source_id_set": _joined_unique_values(rows, "source_id"),
                "assignment_status_set": _joined_unique_values(rows, "assignment_status"),
                "promotion_status_set": _joined_unique_values(rows, "promotion_status"),
                "suggested_decipherment_status_set": _joined_unique_values(
                    rows, "suggested_decipherment_status"
                ),
                "rights_status_set": _joined_unique_values(rows, "rights_status"),
                "review_status_set": _joined_unique_values(rows, "review_status"),
                "required_next_review": _joined_unique_values(rows, "required_next_review"),
                "ai_agent_batch_action": AI_AGENT_BATCH_ACTION,
                "caution": SUMMARY_CAUTION,
                "updated_at": _joined_unique_values(rows, "updated_at"),
            }
        )
    return summary_rows


def write_bucket_summary(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=SUMMARY_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--summary-output", default=str(DEFAULT_SUMMARY_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    manifests = build_bucket_manifests(read_csv_rows(root / args.input))
    write_bucket_manifests(root / args.output_root, manifests)
    summary_rows = build_bucket_summary_rows(manifests, Path(args.output_root))
    write_bucket_summary(root / args.summary_output, summary_rows)

    row_count = sum(len(rows) for rows in manifests.values())
    print(
        "wrote_bucket_manifests="
        f"{len(manifests)} rows={row_count} "
        f"summary_rows={len(summary_rows)} output_root={(root / args.output_root).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
