#!/usr/bin/env python3
"""Capture download-log rows for codepoint crosswalk evidence tasks."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


EVIDENCE_CAPTURE_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "044_ai-agent-hust-obimd-evobc-codepoint-crosswalk-evidence-capture-scaffold.csv"
)
SOURCE_DOWNLOAD_LOG = Path(
    "project_registry/006_large-source-register/002_source-download-log.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "046_ai-agent-hust-obimd-evobc-codepoint-crosswalk-download-log-capture-results.csv"
)
UPDATED_AT = "2026-06-10"
DOWNLOAD_ORDER = [
    "dl-hust-obc-validation-label",
    "dl-hust-obc-ocr-id-to-chinese",
    "dl-obimd-main-character-json",
    "dl-evobc-key-value-json",
    "dl-evobc-list-json",
]
RESEARCH_BOUNDARY = "codepoint_crosswalk_download_log_capture_result_not_scholarship"
DOWNLOAD_LOG_ROW_STATUS = "reviewed_download_log_row_found"
DOWNLOAD_LOG_EVIDENCE_STATUS = "metadata_captured_from_reviewed_download_log"
EVIDENCE_COLLECTION_STATUS = "download_log_metadata_captured"
CHECKSUM_REVIEW_STATUS = "checksum_value_captured_no_recalculation"
SIZE_REVIEW_STATUS = "size_value_captured_no_new_file_review"
ACCESS_REVIEW_STATUS = "download_status_captured_no_new_access"
RIGHTS_DECISION_STATUS = "download_log_value_captured_no_new_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
DECIPHERMENT_CLAIM_STATUS = "no_claim"
CAPTURE_STATUS = "reviewed_metadata_only"
CAUTION = (
    "This row captures download-log metadata for later evidence review. It copies "
    "registered download URL, access status, file size, checksum, local tmp path, "
    "and risk fields only; it is not a new download, not a checksum recalculation, "
    "not a file-size review, not a new rights decision, not a source promotion, "
    "not an oracle-character identity decision, not an accepted reading, not a "
    "component assignment, not an evolution-chain assignment, and not a decipherment "
    "conclusion."
)

OUTPUT_FIELDS = [
    "capture_result_id",
    "capture_task_id",
    "route_result_id",
    "review_log_draft_id",
    "codepoint_review_task_id",
    "crosswalk_candidate_id",
    "suggested_oracle_character_id",
    "download_id",
    "download_log_path",
    "download_log_row_status",
    "source_id_evidence_value",
    "url_evidence_value",
    "downloaded_at_evidence_value",
    "status_evidence_value",
    "http_status_evidence_value",
    "file_size_bytes_evidence_value",
    "checksum_sha256_evidence_value",
    "local_temp_path_evidence_value",
    "risk_note_evidence_value",
    "download_log_evidence_status",
    "evidence_collection_status",
    "checksum_review_status",
    "size_review_status",
    "access_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "decipherment_claim_status",
    "capture_status",
    "captured_metadata_summary",
    "required_next_checks",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _split_compact(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def _download_sort_key(download_id: str) -> int:
    try:
        return DOWNLOAD_ORDER.index(download_id)
    except ValueError:
        return len(DOWNLOAD_ORDER)


def _download_log_tasks(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    tasks = [row for row in rows if row.get("target_evidence_section") == "download_log"]
    tasks.sort(key=lambda row: row["capture_task_id"])
    return tasks


def _summary(parts: dict[str, str]) -> str:
    return ";".join(f"{key}={value}" for key, value in parts.items())


def _capture_row(
    index: int,
    task: dict[str, str],
    download_id: str,
    download_row: dict[str, str],
) -> dict[str, str]:
    return {
        "capture_result_id": f"codepoint-download-log-capture-result-{index:03d}",
        "capture_task_id": task["capture_task_id"],
        "route_result_id": task["route_result_id"],
        "review_log_draft_id": task["review_log_draft_id"],
        "codepoint_review_task_id": task["codepoint_review_task_id"],
        "crosswalk_candidate_id": task["crosswalk_candidate_id"],
        "suggested_oracle_character_id": task["suggested_oracle_character_id"],
        "download_id": download_id,
        "download_log_path": task["source_route_path"],
        "download_log_row_status": DOWNLOAD_LOG_ROW_STATUS,
        "source_id_evidence_value": download_row["source_id"],
        "url_evidence_value": download_row["url"],
        "downloaded_at_evidence_value": download_row["downloaded_at"],
        "status_evidence_value": download_row["status"],
        "http_status_evidence_value": download_row["http_status"],
        "file_size_bytes_evidence_value": download_row["file_size_bytes"],
        "checksum_sha256_evidence_value": download_row["checksum_sha256"],
        "local_temp_path_evidence_value": download_row["local_temp_path"],
        "risk_note_evidence_value": download_row["risk_note"],
        "download_log_evidence_status": DOWNLOAD_LOG_EVIDENCE_STATUS,
        "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
        "checksum_review_status": CHECKSUM_REVIEW_STATUS,
        "size_review_status": SIZE_REVIEW_STATUS,
        "access_review_status": ACCESS_REVIEW_STATUS,
        "rights_decision_status": RIGHTS_DECISION_STATUS,
        "source_promotion_status": SOURCE_PROMOTION_STATUS,
        "identity_claim_status": IDENTITY_CLAIM_STATUS,
        "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
        "capture_status": CAPTURE_STATUS,
        "captured_metadata_summary": _summary(
            {
                "route_result_id": task["route_result_id"],
                "capture_task_id": task["capture_task_id"],
                "download_id": download_id,
                "source_id": download_row["source_id"],
                "status": download_row["status"],
                "http_status": download_row["http_status"],
                "file_size_bytes": download_row["file_size_bytes"],
                "checksum_sha256_present": str(bool(download_row["checksum_sha256"])).lower(),
                "local_temp_path": download_row["local_temp_path"],
            }
        ),
        "required_next_checks": (
            "open_download_log_row;verify_url_status_size_checksum_and_tmp_path;"
            "cross_check_against_source_register_before_asset_or_evidence_promotion"
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_capture_results(
    capture_scaffold_rows: list[dict[str, str]],
    download_log_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    download_by_id = {row["download_id"]: row for row in download_log_rows}
    rows: list[dict[str, str]] = []
    for task in _download_log_tasks(capture_scaffold_rows):
        download_ids = sorted(_split_compact(task["source_record_refs"]), key=_download_sort_key)
        for download_id in download_ids:
            if download_id not in download_by_id:
                raise ValueError(f"missing download log row for {download_id}")
            rows.append(_capture_row(len(rows) + 1, task, download_id, download_by_id[download_id]))
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture-scaffold", default=str(EVIDENCE_CAPTURE_SCAFFOLD))
    parser.add_argument("--download-log", default=str(SOURCE_DOWNLOAD_LOG))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_capture_results(
        read_csv_rows(root / args.capture_scaffold),
        read_csv_rows(root / args.download_log),
    )
    write_csv(root / args.output, rows)
    print(
        f"capture_result_count={len(rows)} "
        f"download_count={len({row['download_id'] for row in rows})} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
