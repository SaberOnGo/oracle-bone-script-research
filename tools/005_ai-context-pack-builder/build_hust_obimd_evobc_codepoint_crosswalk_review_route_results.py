#!/usr/bin/env python3
"""Build metadata-only route results for first-priority codepoint review logs."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


CODEPOINT_REVIEW_LOG_DRAFT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/"
    "042_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-log-draft-manifest.csv"
)
SOURCE_INDEX = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv"
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
    "043_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-route-results.csv"
)
UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "codepoint_crosswalk_review_route_result_metadata_only_not_scholarship"
ROUTE_FILE_STATUS_OK = "reviewed_route_files_exist"
DRAFT_LOG_STATUS_OK = "draft_log_exists"
SOURCE_REGISTER_STATUS_OK = "reviewed_required_sources_registered"
DOWNLOAD_STATUS_OK = "reviewed_required_download_logs_registered"
EVIDENCE_COLLECTION_STATUS = "not_collected"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
PROMOTION_STATUS = "not_promoted"
CAUTION = (
    "This row is a metadata-only route result for later evidence collection. It records "
    "local candidate-packet, staging-row, source-register, and download-log availability; "
    "it is not source evidence by itself, not a confirmed oracle-character identity, not "
    "an accepted reading, not a component assignment, not an evolution-chain assignment, "
    "and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "route_result_id",
    "review_log_draft_id",
    "codepoint_review_task_id",
    "crosswalk_candidate_id",
    "suggested_oracle_character_id",
    "hust_primary_external_ref_id",
    "hust_label_codepoints",
    "hust_candidate_packet_id",
    "hust_candidate_packet_path",
    "hust_candidate_class_id",
    "hust_validation_class_id",
    "hust_source_category_id_padded",
    "hust_dataset_label_status",
    "hust_dataset_label_codepoints",
    "hust_dataset_label_component_count",
    "hust_packet_status",
    "hust_packet_review_status",
    "hust_packet_rights_status",
    "obimd_candidate_main_character_id",
    "obimd_source_uid",
    "obimd_codepoint_uplus",
    "obimd_transcription_count",
    "obimd_project_import_status",
    "obimd_review_status",
    "obimd_rights_status",
    "evobc_candidate_evolution_category_id",
    "evobc_source_category_id",
    "evobc_source_character_codepoints",
    "evobc_image_reference_count",
    "evobc_has_oracle_bone_refs",
    "evobc_has_bronze_refs",
    "evobc_has_seal_refs",
    "evobc_era_code_counts",
    "evobc_source_code_counts",
    "evobc_project_import_status",
    "evobc_review_status",
    "evobc_rights_status",
    "route_file_count",
    "missing_route_file_count",
    "route_file_review_status",
    "draft_log_status",
    "source_register_required_source_ids",
    "source_register_match_count",
    "source_register_rights_statuses",
    "source_register_review_statuses",
    "source_register_review_status",
    "download_ids_required",
    "download_log_match_count",
    "download_total_file_size_bytes",
    "download_checksum_present_count",
    "download_statuses",
    "download_log_review_status",
    "evidence_collection_status",
    "identity_claim_status",
    "promotion_status",
    "research_boundary",
    "review_note",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _split_compact(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def _one(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    matches = [row for row in rows if row.get(key) == value]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one row where {key}={value}, found {len(matches)}")
    return matches[0]


def _first_candidate_packet_path(route_files: list[str]) -> str:
    matches = [path for path in route_files if path.endswith("/01_candidate-character-packet.json")]
    if len(matches) != 1:
        raise ValueError(f"expected one HUST candidate packet route, found {len(matches)}")
    return matches[0]


def _route_file_status(root: Path, route_files: list[str]) -> tuple[int, str]:
    missing_count = sum(1 for route_file in route_files if not (root / route_file).exists())
    status = ROUTE_FILE_STATUS_OK if missing_count == 0 else "route_files_missing"
    return missing_count, status


def _source_register_summary(
    source_ids: list[str],
    source_rows_by_id: dict[str, dict[str, str]],
) -> tuple[int, str, str, str]:
    matches = [source_rows_by_id[source_id] for source_id in source_ids if source_id in source_rows_by_id]
    rights_statuses = ";".join(f"{row['source_id']}={row['rights_status']}" for row in matches)
    review_statuses = ";".join(f"{row['source_id']}={row['review_status']}" for row in matches)
    status = SOURCE_REGISTER_STATUS_OK if len(matches) == len(source_ids) else "missing_source_register_rows"
    return len(matches), rights_statuses, review_statuses, status


def _download_summary(
    download_ids: list[str],
    download_rows_by_id: dict[str, dict[str, str]],
) -> tuple[int, int, int, str, str]:
    matches = [download_rows_by_id[download_id] for download_id in download_ids if download_id in download_rows_by_id]
    total_size = sum(int(row["file_size_bytes"] or "0") for row in matches)
    checksum_count = sum(1 for row in matches if row.get("checksum_sha256"))
    statuses = ";".join(f"{row['download_id']}={row['status']}" for row in matches)
    status = DOWNLOAD_STATUS_OK if len(matches) == len(download_ids) else "missing_download_log_rows"
    return len(matches), total_size, checksum_count, statuses, status


def _download_ids(packet: dict[str, object], obimd_row: dict[str, str], evobc_row: dict[str, str]) -> list[str]:
    ids: list[str] = []
    for download_id in packet.get("evidence_download_ids", []):
        if isinstance(download_id, str):
            ids.append(download_id)
    ids.append(obimd_row["evidence_download_id"])
    ids.append(evobc_row["evidence_download_id_key_value"])
    ids.append(evobc_row["evidence_download_id_list"])
    unique_ids: list[str] = []
    for download_id in ids:
        if download_id and download_id not in unique_ids:
            unique_ids.append(download_id)
    return unique_ids


def _review_note(row: dict[str, str], route_file_count: int, download_count: int) -> str:
    return (
        f"Opened metadata routes for {row['crosswalk_candidate_id']}: {route_file_count} "
        f"local route files, 3 required source-register rows, and {download_count} required "
        "download-log rows are available for later evidence capture. This remains routing "
        "metadata only and does not promote codepoint matches into scholarship."
    )


def build_result_rows(
    draft_rows: list[dict[str, str]],
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
    for index, row in enumerate(draft_rows, start=1):
        route_files = _split_compact(row["route_files_to_open"])
        missing_route_count, route_file_status = _route_file_status(root, route_files)
        candidate_packet_path = _first_candidate_packet_path(route_files)
        packet = read_json(root / candidate_packet_path)
        source_candidate = packet["source_candidate"]
        dataset_label = packet["dataset_label"]
        if not isinstance(source_candidate, dict) or not isinstance(dataset_label, dict):
            raise TypeError("candidate packet source_candidate and dataset_label must be objects")
        obimd_id = row["obimd_candidate_main_character_ids"]
        evobc_id = row["evobc_candidate_evolution_category_ids"]
        obimd_row = obimd_rows_by_id[obimd_id]
        evobc_row = evobc_rows_by_id[evobc_id]
        source_ids = _split_compact(row["matched_source_ids"])
        (
            source_match_count,
            source_rights_statuses,
            source_review_statuses,
            source_review_status,
        ) = _source_register_summary(source_ids, source_rows_by_id)
        download_ids = _download_ids(packet, obimd_row, evobc_row)
        (
            download_match_count,
            download_total_size,
            download_checksum_count,
            download_statuses,
            download_review_status,
        ) = _download_summary(download_ids, download_rows_by_id)
        draft_log_status = DRAFT_LOG_STATUS_OK if (root / row["draft_path"]).exists() else "draft_log_missing"
        route_file_count = len(route_files)
        rows.append(
            {
                "route_result_id": f"codepoint-crosswalk-route-result-{index:03d}",
                "review_log_draft_id": row["review_log_draft_id"],
                "codepoint_review_task_id": row["codepoint_review_task_id"],
                "crosswalk_candidate_id": row["crosswalk_candidate_id"],
                "suggested_oracle_character_id": row["suggested_oracle_character_id"],
                "hust_primary_external_ref_id": row["hust_primary_external_ref_id"],
                "hust_label_codepoints": row["hust_label_codepoints"],
                "hust_candidate_packet_id": str(packet["candidate_packet_id"]),
                "hust_candidate_packet_path": candidate_packet_path,
                "hust_candidate_class_id": str(source_candidate["candidate_class_id"]),
                "hust_validation_class_id": str(source_candidate["validation_class_id"]),
                "hust_source_category_id_padded": str(source_candidate["source_category_id_padded"]),
                "hust_dataset_label_status": str(dataset_label["status"]),
                "hust_dataset_label_codepoints": str(dataset_label["source_modern_label_codepoints"]),
                "hust_dataset_label_component_count": str(dataset_label["label_component_count"]),
                "hust_packet_status": str(packet["packet_status"]),
                "hust_packet_review_status": str(packet["review_status"]),
                "hust_packet_rights_status": str(packet["rights_status"]),
                "obimd_candidate_main_character_id": obimd_id,
                "obimd_source_uid": obimd_row["source_uid"],
                "obimd_codepoint_uplus": obimd_row["codepoint_uplus"],
                "obimd_transcription_count": obimd_row["transcription_count"],
                "obimd_project_import_status": obimd_row["project_import_status"],
                "obimd_review_status": obimd_row["review_status"],
                "obimd_rights_status": obimd_row["rights_status"],
                "evobc_candidate_evolution_category_id": evobc_id,
                "evobc_source_category_id": evobc_row["source_category_id"],
                "evobc_source_character_codepoints": evobc_row["source_character_codepoints"],
                "evobc_image_reference_count": evobc_row["image_reference_count"],
                "evobc_has_oracle_bone_refs": evobc_row["has_oracle_bone_refs"],
                "evobc_has_bronze_refs": evobc_row["has_bronze_refs"],
                "evobc_has_seal_refs": evobc_row["has_seal_refs"],
                "evobc_era_code_counts": evobc_row["era_code_counts"],
                "evobc_source_code_counts": evobc_row["source_code_counts"],
                "evobc_project_import_status": evobc_row["project_import_status"],
                "evobc_review_status": evobc_row["review_status"],
                "evobc_rights_status": evobc_row["rights_status"],
                "route_file_count": str(route_file_count),
                "missing_route_file_count": str(missing_route_count),
                "route_file_review_status": route_file_status,
                "draft_log_status": draft_log_status,
                "source_register_required_source_ids": row["matched_source_ids"],
                "source_register_match_count": str(source_match_count),
                "source_register_rights_statuses": source_rights_statuses,
                "source_register_review_statuses": source_review_statuses,
                "source_register_review_status": source_review_status,
                "download_ids_required": ";".join(download_ids),
                "download_log_match_count": str(download_match_count),
                "download_total_file_size_bytes": str(download_total_size),
                "download_checksum_present_count": str(download_checksum_count),
                "download_statuses": download_statuses,
                "download_log_review_status": download_review_status,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "promotion_status": PROMOTION_STATUS,
                "research_boundary": RESEARCH_BOUNDARY,
                "review_note": _review_note(row, route_file_count, download_match_count),
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
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
    parser.add_argument("--draft-manifest", default=str(CODEPOINT_REVIEW_LOG_DRAFT_MANIFEST))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_result_rows(
        read_csv_rows(root / args.draft_manifest),
        read_csv_rows(root / SOURCE_INDEX),
        read_csv_rows(root / SOURCE_DOWNLOAD_LOG),
        read_csv_rows(root / OBIMD_MAIN_CHARACTER_STAGING),
        read_csv_rows(root / EVOBC_EVOLUTION_CATEGORY_STAGING),
        root,
    )
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
