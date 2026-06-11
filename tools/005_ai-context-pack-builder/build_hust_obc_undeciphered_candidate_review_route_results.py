#!/usr/bin/env python3
"""Build metadata-only route results for top HUST-OBC undeciphered drafts."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REVIEW_LOG_DRAFT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/"
    "052_ai-agent-hust-obc-undeciphered-candidate-review-log-draft-manifest.csv"
)
SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
LARGE_SOURCE_REGISTER = Path("project_registry/006_large-source-register/001_large-source-register.csv")
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "053_ai-agent-hust-obc-undeciphered-candidate-review-route-results.csv"
)
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_candidate_review_route_result_metadata_only_not_scholarship"
ROUTE_FILE_STATUS_OK = "reviewed_route_files_exist"
DRAFT_LOG_STATUS_OK = "draft_log_exists"
SOURCE_REGISTER_STATUS_OK = "reviewed_source_registered"
LARGE_SOURCE_STATUS_OK = "reviewed_large_source_registered"
DOWNLOAD_LOG_STATUS_OK = "reviewed_download_log_registered"
EVIDENCE_COLLECTION_STATUS = "not_collected"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
PROMOTION_STATUS = "not_promoted"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CAUTION = (
    "This row is a metadata-only route result for later evidence collection. It records "
    "local draft-log, candidate-packet, source-register, large-source-register, and "
    "download-log availability; it is not source evidence by itself, not an accepted "
    "oracle-character identity, not a formal obs-char assignment, not a reading, not a "
    "component assignment, not an evolution-chain assignment, and not a decipherment "
    "conclusion."
)

OUTPUT_FIELDS = [
    "route_result_id",
    "review_log_draft_id",
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
    "packet_first_source_image_path",
    "packet_last_source_image_path",
    "packet_filename_source_prefixes",
    "bucket_directory",
    "bucket_manifest_path",
    "candidate_packet_path",
    "draft_path",
    "route_file_count",
    "missing_route_file_count",
    "route_file_review_status",
    "draft_log_status",
    "candidate_packet_status",
    "candidate_packet_review_status",
    "source_register_match_count",
    "source_register_provider",
    "source_register_authority_tier",
    "source_register_rights_status",
    "source_register_review_status",
    "source_register_route_status",
    "large_source_match_count",
    "large_source_file_size_bytes",
    "large_source_checksum_sha256",
    "large_source_storage_status",
    "large_source_rights_status",
    "large_source_review_status",
    "large_source_route_status",
    "download_log_match_count",
    "download_log_status",
    "download_log_http_status",
    "download_log_file_size_bytes",
    "download_log_checksum_sha256",
    "download_log_local_temp_path",
    "download_log_route_status",
    "rights_status",
    "risk_note",
    "evidence_collection_status",
    "identity_claim_status",
    "assignment_status",
    "promotion_status",
    "rights_decision_status",
    "source_promotion_status",
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


def _matches(rows: list[dict[str, str]], key: str, value: str) -> list[dict[str, str]]:
    return [row for row in rows if row.get(key) == value]


def _first_or_empty(rows: list[dict[str, str]]) -> dict[str, str]:
    return rows[0] if rows else {}


def _route_file_status(root: Path, route_files: list[str]) -> tuple[int, str]:
    missing_count = sum(1 for route_file in route_files if not (root / route_file).exists())
    status = ROUTE_FILE_STATUS_OK if missing_count == 0 else "route_files_missing"
    return missing_count, status


def _status_from_count(count: int, ok_status: str, missing_status: str) -> str:
    return ok_status if count > 0 else missing_status


def _review_note(row: dict[str, str], route_file_count: int, missing_route_count: int) -> str:
    return (
        f"Reviewed metadata routes for {row['unknown_candidate_id']}: {route_file_count} "
        f"local route files were listed and {missing_route_count} were missing. Source, "
        "large-source, download-log, and candidate-packet availability is recorded for "
        "later evidence capture only; no identity, assignment, reading, component, "
        "evolution-chain, or decipherment claim is made."
    )


def build_result_rows(
    draft_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    large_source_rows: list[dict[str, str]],
    download_rows: list[dict[str, str]],
    root: Path,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(draft_rows, start=1):
        route_files = _split_compact(row["route_files_to_open"])
        missing_route_count, route_file_status = _route_file_status(root, route_files)
        packet = read_json(root / row["candidate_packet_path"])
        source_matches = _matches(source_rows, "source_id", row["source_id"])
        source_row = _first_or_empty(source_matches)
        large_source_matches = _matches(large_source_rows, "source_package_id", row["source_package_id"])
        large_source_row = _first_or_empty(large_source_matches)
        download_matches = _matches(download_rows, "download_id", row["evidence_download_id"])
        download_row = _first_or_empty(download_matches)
        draft_log_status = DRAFT_LOG_STATUS_OK if (root / row["draft_path"]).exists() else "draft_log_missing"
        candidate_packet_status = (
            "candidate_packet_exists" if (root / row["candidate_packet_path"]).exists() else "candidate_packet_missing"
        )
        rows.append(
            {
                "route_result_id": f"hust-obc-undeciphered-route-result-{index:04d}",
                "review_log_draft_id": row["review_log_draft_id"],
                "undeciphered_review_task_id": row["undeciphered_review_task_id"],
                "context_pack_id": row["context_pack_id"],
                "unknown_candidate_id": row["unknown_candidate_id"],
                "primary_external_ref_id": row["primary_external_ref_id"],
                "source_id": row["source_id"],
                "source_package_id": row["source_package_id"],
                "evidence_download_id": row["evidence_download_id"],
                "priority_rank": row["priority_rank"],
                "priority_bucket": row["priority_bucket"],
                "source_group": row["source_group"],
                "source_group_label": row["source_group_label"],
                "source_class_id": row["source_class_id"],
                "source_class_path": row["source_class_path"],
                "source_image_count": row["source_image_count"],
                "packet_first_source_image_path": str(packet["first_source_image_path"]),
                "packet_last_source_image_path": str(packet["last_source_image_path"]),
                "packet_filename_source_prefixes": str(packet["filename_source_prefixes"]),
                "bucket_directory": row["bucket_directory"],
                "bucket_manifest_path": row["bucket_manifest_path"],
                "candidate_packet_path": row["candidate_packet_path"],
                "draft_path": row["draft_path"],
                "route_file_count": str(len(route_files)),
                "missing_route_file_count": str(missing_route_count),
                "route_file_review_status": route_file_status,
                "draft_log_status": draft_log_status,
                "candidate_packet_status": candidate_packet_status,
                "candidate_packet_review_status": str(packet["review_status"]),
                "source_register_match_count": str(len(source_matches)),
                "source_register_provider": source_row.get("provider", ""),
                "source_register_authority_tier": source_row.get("authority_tier", ""),
                "source_register_rights_status": source_row.get("rights_status", ""),
                "source_register_review_status": source_row.get("review_status", ""),
                "source_register_route_status": _status_from_count(
                    len(source_matches),
                    SOURCE_REGISTER_STATUS_OK,
                    "missing_source_register_row",
                ),
                "large_source_match_count": str(len(large_source_matches)),
                "large_source_file_size_bytes": large_source_row.get("file_size_bytes", ""),
                "large_source_checksum_sha256": large_source_row.get("checksum_sha256", ""),
                "large_source_storage_status": large_source_row.get("storage_status", ""),
                "large_source_rights_status": large_source_row.get("rights_status", ""),
                "large_source_review_status": large_source_row.get("review_status", ""),
                "large_source_route_status": _status_from_count(
                    len(large_source_matches),
                    LARGE_SOURCE_STATUS_OK,
                    "missing_large_source_register_row",
                ),
                "download_log_match_count": str(len(download_matches)),
                "download_log_status": download_row.get("status", ""),
                "download_log_http_status": download_row.get("http_status", ""),
                "download_log_file_size_bytes": download_row.get("file_size_bytes", ""),
                "download_log_checksum_sha256": download_row.get("checksum_sha256", ""),
                "download_log_local_temp_path": download_row.get("local_temp_path", ""),
                "download_log_route_status": _status_from_count(
                    len(download_matches),
                    DOWNLOAD_LOG_STATUS_OK,
                    "missing_download_log_row",
                ),
                "rights_status": row["rights_status"],
                "risk_note": row["risk_note"],
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "assignment_status": ASSIGNMENT_STATUS,
                "promotion_status": PROMOTION_STATUS,
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "research_boundary": RESEARCH_BOUNDARY,
                "review_note": _review_note(row, len(route_files), missing_route_count),
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
    parser.add_argument("--draft-manifest", default=str(REVIEW_LOG_DRAFT_MANIFEST))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_result_rows(
        read_csv_rows(root / args.draft_manifest),
        read_csv_rows(root / SOURCE_INDEX),
        read_csv_rows(root / LARGE_SOURCE_REGISTER),
        read_csv_rows(root / SOURCE_DOWNLOAD_LOG),
        root,
    )
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
