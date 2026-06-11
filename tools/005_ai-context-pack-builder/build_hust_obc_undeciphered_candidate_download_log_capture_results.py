#!/usr/bin/env python3
"""Capture download-log metadata for HUST-OBC undeciphered candidates."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


EVIDENCE_CAPTURE_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "054_ai-agent-hust-obc-undeciphered-candidate-evidence-capture-scaffold.csv"
)
CAPTURE_REVIEW_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/"
    "055_ai-agent-hust-obc-undeciphered-candidate-evidence-capture-review-checklist.csv"
)
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "057_ai-agent-hust-obc-undeciphered-candidate-download-log-capture-results.csv"
)
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_download_log_capture_result_not_scholarship"
DOWNLOAD_LOG_ROW_STATUS = "reviewed_download_log_row_found"
DOWNLOAD_LOG_EVIDENCE_STATUS = "metadata_captured_from_reviewed_download_log"
EVIDENCE_COLLECTION_STATUS = "download_log_metadata_captured"
CHECKSUM_REVIEW_STATUS = "checksum_value_captured_no_recalculation"
SIZE_REVIEW_STATUS = "size_value_captured_no_new_file_review"
ACCESS_REVIEW_STATUS = "download_status_captured_no_new_access"
RIGHTS_DECISION_STATUS = "download_log_value_captured_no_new_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
DECIPHERMENT_CLAIM_STATUS = "no_claim"
COMPONENT_CLAIM_STATUS = "no_claim"
EVOLUTION_CHAIN_CLAIM_STATUS = "no_claim"
CAPTURE_STATUS = "reviewed_metadata_only"
CAUTION = (
    "This row captures download-log metadata for later undeciphered-candidate "
    "evidence review. It copies registered download URL, access status, file "
    "size, checksum, local archive path, and risk fields only; it is not a new "
    "download, not a checksum recalculation, not a file-size review, not a new "
    "rights decision, not source promotion, not an accepted oracle-character "
    "identity, not a formal obs-char assignment, not an accepted reading, not a "
    "component assignment, not an evolution-chain assignment, and not a "
    "decipherment conclusion."
)

OUTPUT_FIELDS = [
    "capture_result_id",
    "checklist_id",
    "capture_task_id",
    "route_result_id",
    "review_log_draft_id",
    "undeciphered_review_task_id",
    "context_pack_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
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
    "assignment_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
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


def _download_log_tasks(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    tasks = [row for row in rows if row.get("target_evidence_section") == "download_log"]
    tasks.sort(key=lambda row: row["capture_task_id"])
    return tasks


def _summary(parts: dict[str, str]) -> str:
    return ";".join(f"{key}={value}" for key, value in parts.items())


def _checklist_by_capture_task(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    download_rows = _download_log_tasks(rows)
    for row in download_rows:
        if row["checklist_status"] != "not_started":
            raise ValueError(f"unexpected checklist_status for {row['capture_task_id']}")
        if row["evidence_collection_status"] != "not_collected":
            raise ValueError(f"unexpected evidence_collection_status for {row['capture_task_id']}")
        if "open_download_log" not in row["required_review_checks"]:
            raise ValueError(f"missing download-log review check for {row['capture_task_id']}")
    return {row["capture_task_id"]: row for row in download_rows}


def _capture_row(
    index: int,
    task: dict[str, str],
    checklist_row: dict[str, str],
    download_row: dict[str, str],
) -> dict[str, str]:
    download_id = task["source_record_refs"]
    return {
        "capture_result_id": f"hust-obc-undeciphered-download-log-capture-result-{index:04d}",
        "checklist_id": checklist_row["checklist_id"],
        "capture_task_id": task["capture_task_id"],
        "route_result_id": task["route_result_id"],
        "review_log_draft_id": task["review_log_draft_id"],
        "undeciphered_review_task_id": task["undeciphered_review_task_id"],
        "context_pack_id": task["context_pack_id"],
        "unknown_candidate_id": task["unknown_candidate_id"],
        "primary_external_ref_id": task["primary_external_ref_id"],
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
        "assignment_status": ASSIGNMENT_STATUS,
        "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
        "component_claim_status": COMPONENT_CLAIM_STATUS,
        "evolution_chain_claim_status": EVOLUTION_CHAIN_CLAIM_STATUS,
        "capture_status": CAPTURE_STATUS,
        "captured_metadata_summary": _summary(
            {
                "route_result_id": task["route_result_id"],
                "capture_task_id": task["capture_task_id"],
                "checklist_id": checklist_row["checklist_id"],
                "download_id": download_id,
                "source_id": download_row["source_id"],
                "status": download_row["status"],
                "http_status": download_row["http_status"],
                "file_size_bytes": download_row["file_size_bytes"],
                "checksum_sha256_present": str(bool(download_row["checksum_sha256"])).lower(),
            }
        ),
        "required_next_checks": (
            "open_057_download_log_capture_result;cross_check_against_056_source_register;"
            "do_not_infer_rights_identity_assignment_or_decipherment_from_download_availability"
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_capture_results(
    capture_scaffold_rows: list[dict[str, str]],
    checklist_rows: list[dict[str, str]],
    download_log_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    download_by_id = {row["download_id"]: row for row in download_log_rows}
    checklist_by_task = _checklist_by_capture_task(checklist_rows)
    rows: list[dict[str, str]] = []
    for task in _download_log_tasks(capture_scaffold_rows):
        download_id = task["source_record_refs"]
        if download_id not in download_by_id:
            raise ValueError(f"missing download log row for {download_id}")
        if task["capture_task_id"] not in checklist_by_task:
            raise ValueError(f"missing checklist row for {task['capture_task_id']}")
        rows.append(
            _capture_row(
                len(rows) + 1,
                task,
                checklist_by_task[task["capture_task_id"]],
                download_by_id[download_id],
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
    parser.add_argument("--capture-scaffold", default=str(EVIDENCE_CAPTURE_SCAFFOLD))
    parser.add_argument("--capture-review-checklist", default=str(CAPTURE_REVIEW_CHECKLIST))
    parser.add_argument("--download-log", default=str(SOURCE_DOWNLOAD_LOG))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_capture_results(
        read_csv_rows(root / args.capture_scaffold),
        read_csv_rows(root / args.capture_review_checklist),
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
