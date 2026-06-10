#!/usr/bin/env python3
"""Build metadata-only route availability rows for all codepoint review tasks."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


CODEPOINT_REVIEW_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/"
    "041_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-queue.csv"
)
SOURCE_INDEX = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "001_all-sources-index.csv"
)
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
OBIMD_MAIN_CHARACTER_STAGING = Path(
    "corpus/001_oracle-characters/000_character-registers/006_obimd-main-character-staging.csv"
)
EVOBC_EVOLUTION_CATEGORY_STAGING = Path(
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
    "001_evobc-evolution-category-staging.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "049_ai-agent-hust-obimd-evobc-codepoint-crosswalk-route-availability-snapshot.csv"
)
UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "codepoint_crosswalk_route_availability_snapshot_not_scholarship"
AVAILABILITY_STATUS = "ready_for_review_log_draft_materialization_metadata_only"
EVIDENCE_COLLECTION_STATUS = "availability_metadata_captured_not_evidence"
CAUTION = (
    "This row is a metadata-only route availability snapshot for a codepoint review task. "
    "It links local HUST candidate packets, matched OBIMD/EVOBC staging rows, source-register "
    "rows, and download-log rows for later human review; it is not source evidence by itself, "
    "not an oracle-character identity decision, not an accepted reading, not a component "
    "assignment, not an evolution-chain assignment, not a rights decision, not a source "
    "promotion, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "route_availability_id",
    "codepoint_review_task_id",
    "context_pack_id",
    "crosswalk_candidate_id",
    "suggested_oracle_character_id",
    "promotion_queue_id",
    "priority_rank",
    "priority_bucket",
    "cross_source_status",
    "matched_source_ids",
    "hust_primary_external_ref_id",
    "hust_label_codepoints",
    "hust_candidate_packet_id",
    "hust_candidate_packet_path",
    "hust_candidate_packet_exists",
    "hust_candidate_class_id",
    "hust_validation_class_id",
    "hust_source_category_id_padded",
    "hust_dataset_label_status",
    "hust_dataset_label_codepoints",
    "hust_packet_status",
    "hust_packet_review_status",
    "hust_packet_rights_status",
    "obimd_candidate_main_character_ids",
    "obimd_row_count",
    "obimd_source_uids",
    "obimd_codepoint_uplus_values",
    "obimd_review_statuses",
    "obimd_rights_statuses",
    "evobc_candidate_evolution_category_ids",
    "evobc_row_count",
    "evobc_source_category_ids",
    "evobc_source_character_codepoints_values",
    "evobc_image_reference_count_total",
    "evobc_has_oracle_bone_refs_any",
    "evobc_has_bronze_refs_any",
    "evobc_has_seal_refs_any",
    "evobc_review_statuses",
    "evobc_rights_statuses",
    "source_register_required_source_ids",
    "source_register_match_count",
    "source_register_rights_statuses",
    "source_register_review_statuses",
    "download_ids_required",
    "download_log_match_count",
    "download_total_file_size_bytes",
    "download_checksum_present_count",
    "download_access_statuses",
    "route_file_count",
    "missing_route_file_count",
    "route_file_review_status",
    "review_log_expected_path",
    "review_log_materialization_status",
    "availability_status",
    "evidence_collection_status",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
    "research_boundary",
    "required_next_checks",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _split_compact(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def _compact(values: list[str]) -> str:
    return ";".join(value for value in values if value)


def _unique(values: list[str]) -> list[str]:
    unique_values: list[str] = []
    for value in values:
        if value and value not in unique_values:
            unique_values.append(value)
    return unique_values


def _bool_any(rows: list[dict[str, str]], key: str) -> str:
    return str(any(row.get(key) == "true" for row in rows)).lower()


def _sum_int(rows: list[dict[str, str]], key: str) -> str:
    return str(sum(int(row.get(key, "0") or "0") for row in rows))


def _route_file_status(root: Path, route_files: list[str]) -> tuple[int, str]:
    missing_count = sum(1 for route_file in route_files if not (root / route_file).exists())
    status = "reviewed_route_files_exist" if missing_count == 0 else "route_files_missing"
    return missing_count, status


def _source_register_summary(
    source_ids: list[str],
    source_rows_by_id: dict[str, dict[str, str]],
) -> tuple[int, str, str]:
    matches = [source_rows_by_id[source_id] for source_id in source_ids if source_id in source_rows_by_id]
    rights_statuses = _compact([f"{row['source_id']}={row['rights_status']}" for row in matches])
    review_statuses = _compact([f"{row['source_id']}={row['review_status']}" for row in matches])
    return len(matches), rights_statuses, review_statuses


def _download_summary(
    download_ids: list[str],
    download_rows_by_id: dict[str, dict[str, str]],
) -> tuple[int, int, int, str]:
    matches = [
        download_rows_by_id[download_id]
        for download_id in download_ids
        if download_id in download_rows_by_id
    ]
    total_size = sum(int(row.get("file_size_bytes", "0") or "0") for row in matches)
    checksum_count = sum(1 for row in matches if row.get("checksum_sha256"))
    statuses = _compact(
        [
            f"{row['download_id']}={row['status']}:{row['http_status']}"
            for row in matches
        ]
    )
    return len(matches), total_size, checksum_count, statuses


def _download_ids(
    packet: dict[str, Any],
    obimd_rows: list[dict[str, str]],
    evobc_rows: list[dict[str, str]],
) -> list[str]:
    ids: list[str] = []
    for download_id in packet.get("evidence_download_ids", []):
        if isinstance(download_id, str):
            ids.append(download_id)
    ids.extend(row["evidence_download_id"] for row in obimd_rows)
    for row in evobc_rows:
        ids.append(row["evidence_download_id_key_value"])
        ids.append(row["evidence_download_id_list"])
    return _unique(ids)


def _matched_rows(
    ids: list[str],
    rows_by_id: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    return [rows_by_id[row_id] for row_id in ids if row_id in rows_by_id]


def _build_row(
    index: int,
    review_row: dict[str, str],
    packet: dict[str, Any],
    obimd_rows: list[dict[str, str]],
    evobc_rows: list[dict[str, str]],
    source_rows_by_id: dict[str, dict[str, str]],
    download_rows_by_id: dict[str, dict[str, str]],
    root: Path,
) -> dict[str, str]:
    source_candidate = packet["source_candidate"]
    dataset_label = packet["dataset_label"]
    if not isinstance(source_candidate, dict) or not isinstance(dataset_label, dict):
        raise TypeError("candidate packet source_candidate and dataset_label must be objects")
    source_ids = _split_compact(review_row["matched_source_ids"])
    source_match_count, source_rights, source_review = _source_register_summary(
        source_ids, source_rows_by_id
    )
    download_ids = _download_ids(packet, obimd_rows, evobc_rows)
    download_count, total_size, checksum_count, download_statuses = _download_summary(
        download_ids, download_rows_by_id
    )
    route_files = _split_compact(review_row["route_files_to_open"])
    missing_route_count, route_file_status = _route_file_status(root, route_files)
    review_log_status = (
        "draft_log_exists"
        if (root / review_row["expected_output_path"]).exists()
        else "draft_log_not_materialized"
    )
    return {
        "route_availability_id": f"codepoint-route-availability-{index:03d}",
        "codepoint_review_task_id": review_row["codepoint_review_task_id"],
        "context_pack_id": review_row["context_pack_id"],
        "crosswalk_candidate_id": review_row["crosswalk_candidate_id"],
        "suggested_oracle_character_id": review_row["suggested_oracle_character_id"],
        "promotion_queue_id": review_row["promotion_queue_id"],
        "priority_rank": review_row["priority_rank"],
        "priority_bucket": review_row["priority_bucket"],
        "cross_source_status": review_row["cross_source_status"],
        "matched_source_ids": review_row["matched_source_ids"],
        "hust_primary_external_ref_id": review_row["hust_primary_external_ref_id"],
        "hust_label_codepoints": review_row["hust_label_codepoints"],
        "hust_candidate_packet_id": str(packet["candidate_packet_id"]),
        "hust_candidate_packet_path": review_row["candidate_packet_path"],
        "hust_candidate_packet_exists": str((root / review_row["candidate_packet_path"]).exists()).lower(),
        "hust_candidate_class_id": str(source_candidate["candidate_class_id"]),
        "hust_validation_class_id": str(source_candidate["validation_class_id"]),
        "hust_source_category_id_padded": str(source_candidate["source_category_id_padded"]),
        "hust_dataset_label_status": str(dataset_label["status"]),
        "hust_dataset_label_codepoints": str(dataset_label["source_modern_label_codepoints"]),
        "hust_packet_status": str(packet["packet_status"]),
        "hust_packet_review_status": str(packet["review_status"]),
        "hust_packet_rights_status": str(packet["rights_status"]),
        "obimd_candidate_main_character_ids": review_row["obimd_candidate_main_character_ids"],
        "obimd_row_count": str(len(obimd_rows)),
        "obimd_source_uids": _compact([row["source_uid"] for row in obimd_rows]),
        "obimd_codepoint_uplus_values": _compact([row["codepoint_uplus"] for row in obimd_rows]),
        "obimd_review_statuses": _compact(
            [f"{row['candidate_main_character_id']}={row['review_status']}" for row in obimd_rows]
        ),
        "obimd_rights_statuses": _compact(
            [f"{row['candidate_main_character_id']}={row['rights_status']}" for row in obimd_rows]
        ),
        "evobc_candidate_evolution_category_ids": review_row[
            "evobc_candidate_evolution_category_ids"
        ],
        "evobc_row_count": str(len(evobc_rows)),
        "evobc_source_category_ids": _compact([row["source_category_id"] for row in evobc_rows]),
        "evobc_source_character_codepoints_values": _compact(
            [row["source_character_codepoints"] for row in evobc_rows]
        ),
        "evobc_image_reference_count_total": _sum_int(evobc_rows, "image_reference_count"),
        "evobc_has_oracle_bone_refs_any": _bool_any(evobc_rows, "has_oracle_bone_refs"),
        "evobc_has_bronze_refs_any": _bool_any(evobc_rows, "has_bronze_refs"),
        "evobc_has_seal_refs_any": _bool_any(evobc_rows, "has_seal_refs"),
        "evobc_review_statuses": _compact(
            [f"{row['candidate_evolution_category_id']}={row['review_status']}" for row in evobc_rows]
        ),
        "evobc_rights_statuses": _compact(
            [f"{row['candidate_evolution_category_id']}={row['rights_status']}" for row in evobc_rows]
        ),
        "source_register_required_source_ids": review_row["matched_source_ids"],
        "source_register_match_count": str(source_match_count),
        "source_register_rights_statuses": source_rights,
        "source_register_review_statuses": source_review,
        "download_ids_required": _compact(download_ids),
        "download_log_match_count": str(download_count),
        "download_total_file_size_bytes": str(total_size),
        "download_checksum_present_count": str(checksum_count),
        "download_access_statuses": download_statuses,
        "route_file_count": str(len(route_files)),
        "missing_route_file_count": str(missing_route_count),
        "route_file_review_status": route_file_status,
        "review_log_expected_path": review_row["expected_output_path"],
        "review_log_materialization_status": review_log_status,
        "availability_status": AVAILABILITY_STATUS,
        "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
        "rights_decision_status": "no_new_rights_decision",
        "source_promotion_status": "not_promoted",
        "identity_claim_status": "no_identity_claim",
        "decipherment_claim_status": "no_claim",
        "component_claim_status": "no_claim",
        "evolution_chain_claim_status": "no_claim",
        "research_boundary": RESEARCH_BOUNDARY,
        "required_next_checks": (
            "materialize_or_open_review_log_draft;verify_hust_candidate_packet;"
            "verify_matched_source_staging_rows;verify_source_register_and_download_log;"
            "compare_against_xiaoxuetang_obm_and_primary_inscription_context_before_any_identity_or_decipherment_claim"
        ),
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_availability_rows(
    review_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    download_rows: list[dict[str, str]],
    obimd_rows: list[dict[str, str]],
    evobc_rows: list[dict[str, str]],
    root: Path,
) -> list[dict[str, str]]:
    source_rows_by_id = {row["source_id"]: row for row in source_rows}
    download_rows_by_id = {row["download_id"]: row for row in download_rows}
    obimd_rows_by_id = {row["candidate_main_character_id"]: row for row in obimd_rows}
    evobc_rows_by_id = {row["candidate_evolution_category_id"]: row for row in evobc_rows}
    rows: list[dict[str, str]] = []
    for review_row in review_rows:
        packet = read_json(root / review_row["candidate_packet_path"])
        obimd_matches = _matched_rows(
            _split_compact(review_row["obimd_candidate_main_character_ids"]),
            obimd_rows_by_id,
        )
        evobc_matches = _matched_rows(
            _split_compact(review_row["evobc_candidate_evolution_category_ids"]),
            evobc_rows_by_id,
        )
        rows.append(
            _build_row(
                len(rows) + 1,
                review_row,
                packet,
                obimd_matches,
                evobc_matches,
                source_rows_by_id,
                download_rows_by_id,
                root,
            )
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-queue", default=str(CODEPOINT_REVIEW_QUEUE))
    parser.add_argument("--source-index", default=str(SOURCE_INDEX))
    parser.add_argument("--download-log", default=str(SOURCE_DOWNLOAD_LOG))
    parser.add_argument("--obimd-staging", default=str(OBIMD_MAIN_CHARACTER_STAGING))
    parser.add_argument("--evobc-staging", default=str(EVOBC_EVOLUTION_CATEGORY_STAGING))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_availability_rows(
        read_csv_rows(root / args.review_queue),
        read_csv_rows(root / args.source_index),
        read_csv_rows(root / args.download_log),
        read_csv_rows(root / args.obimd_staging),
        read_csv_rows(root / args.evobc_staging),
        root,
    )
    write_csv(root / args.output, rows)
    print(
        f"availability_row_count={len(rows)} "
        f"draft_exists_count={sum(row['review_log_materialization_status'] == 'draft_log_exists' for row in rows)} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
