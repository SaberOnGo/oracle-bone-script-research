#!/usr/bin/env python3
"""Build a metadata-only review queue for HUST-OBC undeciphered candidates."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


CONTEXT_PACK = Path(
    "corpus/009_statistics-and-derived-features/"
    "050_ai-agent-hust-obc-undeciphered-candidate-context-pack.json"
)
UNDECIPHERED_INDEX = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "003_undeciphered-oracle-characters-index.csv"
)
SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
LARGE_SOURCE_REGISTER = Path("project_registry/006_large-source-register/001_large-source-register.csv")
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "051_ai-agent-hust-obc-undeciphered-candidate-review-queue.csv"
)
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_candidate_review_queue_metadata_only_not_scholarship"
TASK_STATUS = "needs_metadata_route_review"
EVIDENCE_COLLECTION_STATUS = "not_collected"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CAUTION = (
    "This row is an undeciphered-candidate metadata review task only. It routes the "
    "reviewer to source-marked HUST-OBC metadata and local candidate packets; it is not "
    "an accepted oracle-character identity, not a formal obs-char assignment, not a "
    "reading, not a component assignment, not an evolution-chain assignment, and not a "
    "decipherment conclusion."
)

OUTPUT_FIELDS = [
    "undeciphered_review_task_id",
    "context_pack_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "source_id",
    "source_package_id",
    "evidence_download_id",
    "priority_rank",
    "priority_bucket",
    "source_group",
    "source_group_label",
    "source_class_id",
    "source_class_path",
    "source_image_count",
    "bucket_directory",
    "bucket_manifest_path",
    "candidate_packet_path",
    "required_evidence_sections",
    "required_next_checks",
    "route_files_to_open",
    "expected_output_path",
    "decipherment_status",
    "identity_claim_status",
    "assignment_status",
    "promotion_status",
    "evidence_collection_status",
    "rights_decision_status",
    "source_promotion_status",
    "task_status",
    "research_boundary",
    "rights_status",
    "risk_note",
    "caution",
    "updated_at",
]

REQUIRED_EVIDENCE_SECTIONS = [
    "undeciphered_index_row",
    "bucket_manifest_row",
    "candidate_packet",
    "source_register_row",
    "large_source_register_row",
    "download_log_row",
    "rights_risk_boundary",
    "review_log",
]

COMMON_NEXT_CHECKS = [
    "open_undeciphered_index_row",
    "open_bucket_manifest_row",
    "open_candidate_packet",
    "verify_source_register_and_large_source_register",
    "verify_download_log_checksum_size_and_risk_note",
    "record_no_identity_assignment_or_decipherment_claim",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _image_count(row: dict[str, str]) -> int:
    return int(row["source_image_count"])


def _priority(row: dict[str, str]) -> tuple[int, str]:
    count = _image_count(row)
    if count >= 50:
        return (1, "image_count_050_plus")
    if count >= 20:
        return (2, "image_count_020_049")
    if count >= 10:
        return (3, "image_count_010_019")
    if count >= 2:
        return (4, "image_count_002_009")
    return (5, "image_count_001")


def _bucket_directory(row: dict[str, str]) -> str:
    parts = row["materialized_candidate_packet_path"].split("/")
    if len(parts) < 3:
        raise ValueError(f"cannot parse bucket directory from {row['materialized_candidate_packet_path']}")
    return parts[2]


def _bucket_manifest_path(bucket_directory: str) -> str:
    return (
        "corpus/001_oracle-characters/"
        f"{bucket_directory}/000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
    )


def _expected_output_path(index: int, row: dict[str, str]) -> str:
    priority_rank, priority_bucket = _priority(row)
    return (
        "doc/public/user_research/005_undeciphered-candidate-review-queues/"
        f"{priority_rank:03d}_{priority_bucket}/"
        f"{index:04d}_{row['unknown_candidate_id']}_{row['primary_external_ref_id']}_review-log.md"
    )


def _route_files(row: dict[str, str]) -> list[str]:
    bucket_directory = _bucket_directory(row)
    files = [
        CONTEXT_PACK.as_posix(),
        UNDECIPHERED_INDEX.as_posix(),
        _bucket_manifest_path(bucket_directory),
        row["materialized_candidate_packet_path"],
        SOURCE_INDEX.as_posix(),
        LARGE_SOURCE_REGISTER.as_posix(),
        SOURCE_DOWNLOAD_LOG.as_posix(),
    ]
    unique_files: list[str] = []
    for file_path in files:
        if file_path not in unique_files:
            unique_files.append(file_path)
    return unique_files


def build_review_rows(
    context_pack: dict[str, object],
    undeciphered_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    context_pack_id = str(context_pack["context_pack_id"])
    sorted_rows = sorted(
        undeciphered_rows,
        key=lambda row: (
            _priority(row)[0],
            -_image_count(row),
            row["source_group"],
            row["unknown_candidate_id"],
        ),
    )

    output_rows: list[dict[str, str]] = []
    for index, row in enumerate(sorted_rows, start=1):
        priority_rank, priority_bucket = _priority(row)
        bucket_directory = _bucket_directory(row)
        output_rows.append(
            {
                "undeciphered_review_task_id": f"hust-obc-undeciphered-review-{index:04d}",
                "context_pack_id": context_pack_id,
                "unknown_candidate_id": row["unknown_candidate_id"],
                "primary_external_ref_id": row["primary_external_ref_id"],
                "source_id": row["source_id"],
                "source_package_id": row["source_package_id"],
                "evidence_download_id": row["evidence_download_id"],
                "priority_rank": str(priority_rank),
                "priority_bucket": priority_bucket,
                "source_group": row["source_group"],
                "source_group_label": row["source_group_label"],
                "source_class_id": row["source_class_id"],
                "source_class_path": row["source_class_path"],
                "source_image_count": row["source_image_count"],
                "bucket_directory": bucket_directory,
                "bucket_manifest_path": _bucket_manifest_path(bucket_directory),
                "candidate_packet_path": row["materialized_candidate_packet_path"],
                "required_evidence_sections": ";".join(REQUIRED_EVIDENCE_SECTIONS),
                "required_next_checks": ";".join(COMMON_NEXT_CHECKS),
                "route_files_to_open": ";".join(_route_files(row)),
                "expected_output_path": _expected_output_path(index, row),
                "decipherment_status": row["decipherment_status"],
                "identity_claim_status": row["identity_claim_status"],
                "assignment_status": row["assignment_status"],
                "promotion_status": row["promotion_status"],
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "task_status": TASK_STATUS,
                "research_boundary": RESEARCH_BOUNDARY,
                "rights_status": row["rights_status"],
                "risk_note": row["risk_note"],
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return output_rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--context-pack", default=str(CONTEXT_PACK))
    parser.add_argument("--undeciphered-index", default=str(UNDECIPHERED_INDEX))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_review_rows(
        read_json(root / args.context_pack),
        read_csv_rows(root / args.undeciphered_index),
    )
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
