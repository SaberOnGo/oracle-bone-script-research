#!/usr/bin/env python3
"""Build candidate character packets for every HUST-OBC obs-char bucket."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


PROMOTION_QUEUE = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "009_hust-obc-obs-char-promotion-review-queue.csv"
)
CORPUS_ROOT = Path("corpus/001_oracle-characters")
CANDIDATE_PACKET_MANIFEST_FILENAME = "001_hust-obc-candidate-packet-manifest.csv"
PROMOTION_BUCKET_MANIFEST_FILENAME = "000_hust-obc-promotion-bucket-manifest.csv"
UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "candidate_packet_not_accepted_character_record_not_scholarship"
DATASET_LABEL_STATUS = "dataset_label_candidate_not_accepted_reading"
PACKET_STATUS = "candidate_packet_created_from_source_marked_staging"
REVIEW_STATUS = "needs_cross_source_review"

MANIFEST_FIELDS = [
    "candidate_packet_id",
    "suggested_oracle_character_id",
    "candidate_packet_path",
    "source_id",
    "primary_external_ref_id",
    "source_label_candidate",
    "source_label_codepoints",
    "label_component_count",
    "has_multi_component_label",
    "source_category_member_count",
    "promotion_queue_id",
    "candidate_class_id",
    "source_category_row_ids",
    "assignment_status",
    "promotion_status",
    "decipherment_status",
    "dataset_label_status",
    "rights_status",
    "review_status",
    "research_boundary",
    "caution",
    "updated_at",
]

CAUTION = (
    "Candidate packet only. This is not an accepted oracle character record, not an "
    "accepted reading, not a source promotion, and not a decipherment conclusion. "
    "The HUST-OBC label is dataset metadata for lookup until cross-source review."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _bucket_path(row: dict[str, str]) -> Path:
    return CORPUS_ROOT / row["suggested_bucket_directory"]


def _packet_relative_path(row: dict[str, str]) -> Path:
    return _bucket_path(row) / row["suggested_character_directory"] / "01_candidate-character-packet.json"


def _bucket_manifest_relative_path(bucket_directory: str) -> Path:
    return CORPUS_ROOT / bucket_directory / CANDIDATE_PACKET_MANIFEST_FILENAME


def _route_files_for(row: dict[str, str]) -> list[str]:
    bucket_path = _bucket_path(row)
    return [
        PROMOTION_QUEUE.as_posix(),
        f"{bucket_path.as_posix()}/{PROMOTION_BUCKET_MANIFEST_FILENAME}",
        (
            "corpus/001_oracle-characters/000_character-registers/"
            "005_hust-obc-validation-class-staging.csv"
        ),
        (
            "corpus/001_oracle-characters/000_character-registers/"
            "007_hust-obc-validation-label-crosswalk-staging.csv"
        ),
        (
            "corpus/001_oracle-characters/000_character-registers/"
            "008_hust-obc-source-category-staging.csv"
        ),
        "project_registry/006_large-source-register/002_source-download-log.csv",
        "corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv",
        f"corpus/001_oracle-characters/{row['suggested_bucket_directory']}",
    ]


def _packet_payload(index: int, row: dict[str, str]) -> dict[str, object]:
    return {
        "candidate_packet_id": f"hust-obc-candidate-packet-{index:06d}",
        "record_type": "oracle_character_candidate_packet",
        "suggested_oracle_character_id": row["suggested_oracle_character_id"],
        "preferred_directory_name": row["suggested_character_directory"],
        "primary_external_ref_id": row["primary_external_ref_id"],
        "source_id": row["source_id"],
        "source_candidate": {
            "promotion_queue_id": row["promotion_queue_id"],
            "candidate_class_id": row["candidate_class_id"],
            "validation_class_id": row["validation_class_id"],
            "source_category_id": row["source_category_id"],
            "source_category_id_padded": row["source_category_id_padded"],
            "candidate_label_crosswalk_id": row["candidate_label_crosswalk_id"],
            "source_category_row_ids": [
                value for value in row["source_category_row_ids"].split(";") if value
            ],
        },
        "dataset_label": {
            "status": DATASET_LABEL_STATUS,
            "source_modern_label_candidate": row["source_modern_label_candidate"],
            "source_modern_label_codepoints": row["source_modern_label_codepoints"],
            "label_component_count": row["label_component_count"],
            "has_multi_component_label": row["has_multi_component_label"],
            "source_category_member_count": row["source_category_member_count"],
        },
        "decipherment_status": "unknown_until_cross_source_review",
        "assignment_status": row["assignment_status"],
        "promotion_status": row["promotion_status"],
        "packet_status": PACKET_STATUS,
        "required_next_review": row["required_next_review"],
        "external_references": [
            {
                "external_ref_id": row["primary_external_ref_id"],
                "source_id": row["source_id"],
                "id_type": "hust_obc_source_category",
                "external_value": row["source_category_id"],
                "note": "Dataset category reference only; not an accepted oracle-character reading.",
            },
            {
                "external_ref_id": row["candidate_class_id"],
                "source_id": row["source_id"],
                "id_type": "hust_obc_validation_class_candidate",
                "external_value": row["validation_class_id"],
                "note": "Validation class candidate used for routing cross-source review.",
            },
        ],
        "evidence_download_ids": [
            "dl-hust-obc-validation-label",
            "dl-hust-obc-ocr-id-to-chinese",
        ],
        "source_metadata_files": [
            value for value in row["source_metadata_files"].split(";") if value
        ],
        "route_files": _route_files_for(row),
        "rights_status": row["rights_status"],
        "review_status": REVIEW_STATUS,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def _manifest_row(index: int, row: dict[str, str]) -> dict[str, str]:
    return {
        "candidate_packet_id": f"hust-obc-candidate-packet-{index:06d}",
        "suggested_oracle_character_id": row["suggested_oracle_character_id"],
        "candidate_packet_path": _packet_relative_path(row).as_posix(),
        "source_id": row["source_id"],
        "primary_external_ref_id": row["primary_external_ref_id"],
        "source_label_candidate": row["source_modern_label_candidate"],
        "source_label_codepoints": row["source_modern_label_codepoints"],
        "label_component_count": row["label_component_count"],
        "has_multi_component_label": row["has_multi_component_label"],
        "source_category_member_count": row["source_category_member_count"],
        "promotion_queue_id": row["promotion_queue_id"],
        "candidate_class_id": row["candidate_class_id"],
        "source_category_row_ids": row["source_category_row_ids"],
        "assignment_status": row["assignment_status"],
        "promotion_status": row["promotion_status"],
        "decipherment_status": "unknown_until_cross_source_review",
        "dataset_label_status": DATASET_LABEL_STATUS,
        "rights_status": row["rights_status"],
        "review_status": REVIEW_STATUS,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_candidate_packets(
    promotion_rows: list[dict[str, str]],
) -> tuple[dict[Path, list[tuple[Path, dict[str, object]]]], dict[Path, list[dict[str, str]]]]:
    packets_by_manifest: dict[Path, list[tuple[Path, dict[str, object]]]] = defaultdict(list)
    manifest_rows_by_manifest: dict[Path, list[dict[str, str]]] = defaultdict(list)
    for index, row in enumerate(promotion_rows, start=1):
        if not row.get("suggested_bucket_directory"):
            raise ValueError(f"missing bucket directory for row {index}")
        manifest_path = _bucket_manifest_relative_path(row["suggested_bucket_directory"])
        packets_by_manifest[manifest_path].append((_packet_relative_path(row), _packet_payload(index, row)))
        manifest_rows_by_manifest[manifest_path].append(_manifest_row(index, row))
    return dict(packets_by_manifest), dict(manifest_rows_by_manifest)


def write_outputs(
    root: Path,
    packets_by_manifest: dict[Path, list[tuple[Path, dict[str, object]]]],
    manifest_rows_by_manifest: dict[Path, list[dict[str, str]]],
) -> None:
    for packets in packets_by_manifest.values():
        for relative_path, payload in packets:
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
    for manifest_path, manifest_rows in sorted(manifest_rows_by_manifest.items()):
        path = root / manifest_path
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=MANIFEST_FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(manifest_rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--promotion-queue", default=str(PROMOTION_QUEUE))
    args = parser.parse_args(argv)

    root = repo_root()
    packets_by_manifest, manifest_rows_by_manifest = build_candidate_packets(
        read_csv_rows(root / args.promotion_queue)
    )
    write_outputs(root, packets_by_manifest, manifest_rows_by_manifest)
    print(
        f"candidate_packet_count={sum(len(packets) for packets in packets_by_manifest.values())} "
        f"manifest_count={len(manifest_rows_by_manifest)} "
        f"bucket_count={len(manifest_rows_by_manifest)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
