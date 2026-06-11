#!/usr/bin/env python3
"""Capture large-source-register metadata for HUST-OBC undeciphered candidates."""

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
LARGE_SOURCE_REGISTER = Path("project_registry/006_large-source-register/001_large-source-register.csv")
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "058_ai-agent-hust-obc-undeciphered-candidate-large-source-register-capture-results.csv"
)
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_large_source_register_capture_result_not_scholarship"
LARGE_SOURCE_ROW_STATUS = "reviewed_large_source_register_row_found"
LARGE_SOURCE_EVIDENCE_STATUS = "metadata_captured_from_reviewed_large_source_register"
EVIDENCE_COLLECTION_STATUS = "large_source_register_metadata_captured"
FILE_SIZE_REVIEW_STATUS = "registered_file_size_captured_no_new_file_review"
CHECKSUM_REVIEW_STATUS = "registered_checksum_captured_no_recalculation"
STORAGE_BOUNDARY_REVIEW_STATUS = "external_storage_boundary_captured_no_raw_commit"
RIGHTS_DECISION_STATUS = "large_source_register_value_captured_no_new_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
DECIPHERMENT_CLAIM_STATUS = "no_claim"
COMPONENT_CLAIM_STATUS = "no_claim"
EVOLUTION_CHAIN_CLAIM_STATUS = "no_claim"
CAPTURE_STATUS = "reviewed_metadata_only"
CAUTION = (
    "This row captures large-source-register metadata for later undeciphered-candidate "
    "evidence review. It copies registered raw-package size, checksum, storage hint, "
    "handling strategy, derived-record paths, rights status, risk note, and review "
    "status only; it is not a raw package commit, not a new checksum calculation, "
    "not a new file-size review, not a new rights decision, not source promotion, "
    "not an accepted oracle-character identity, not a formal obs-char assignment, "
    "not an accepted reading, not a component assignment, not an evolution-chain "
    "assignment, and not a decipherment conclusion."
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
    "source_package_id",
    "large_source_register_path",
    "large_source_row_status",
    "title_evidence_value",
    "provider_evidence_value",
    "source_url_evidence_value",
    "access_method_evidence_value",
    "downloaded_at_evidence_value",
    "file_size_bytes_evidence_value",
    "checksum_sha256_evidence_value",
    "storage_status_evidence_value",
    "storage_hint_evidence_value",
    "handling_strategy_evidence_value",
    "derived_record_paths_evidence_value",
    "rights_status_evidence_value",
    "risk_note_evidence_value",
    "review_status_evidence_value",
    "source_updated_at_evidence_value",
    "large_source_evidence_status",
    "evidence_collection_status",
    "file_size_review_status",
    "checksum_review_status",
    "storage_boundary_review_status",
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


def _large_source_tasks(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    tasks = [row for row in rows if row.get("target_evidence_section") == "large_source_register"]
    tasks.sort(key=lambda row: row["capture_task_id"])
    return tasks


def _summary(parts: dict[str, str]) -> str:
    return ";".join(f"{key}={value}" for key, value in parts.items())


def _checklist_by_capture_task(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    large_source_rows = _large_source_tasks(rows)
    for row in large_source_rows:
        if row["checklist_status"] != "not_started":
            raise ValueError(f"unexpected checklist_status for {row['capture_task_id']}")
        if row["evidence_collection_status"] != "not_collected":
            raise ValueError(f"unexpected evidence_collection_status for {row['capture_task_id']}")
        if "open_large_source_register" not in row["required_review_checks"]:
            raise ValueError(f"missing large-source review check for {row['capture_task_id']}")
    return {row["capture_task_id"]: row for row in large_source_rows}


def _capture_row(
    index: int,
    task: dict[str, str],
    checklist_row: dict[str, str],
    large_source_row: dict[str, str],
) -> dict[str, str]:
    source_package_id = task["source_record_refs"]
    return {
        "capture_result_id": f"hust-obc-undeciphered-large-source-capture-result-{index:04d}",
        "checklist_id": checklist_row["checklist_id"],
        "capture_task_id": task["capture_task_id"],
        "route_result_id": task["route_result_id"],
        "review_log_draft_id": task["review_log_draft_id"],
        "undeciphered_review_task_id": task["undeciphered_review_task_id"],
        "context_pack_id": task["context_pack_id"],
        "unknown_candidate_id": task["unknown_candidate_id"],
        "primary_external_ref_id": task["primary_external_ref_id"],
        "source_package_id": source_package_id,
        "large_source_register_path": task["source_route_path"],
        "large_source_row_status": LARGE_SOURCE_ROW_STATUS,
        "title_evidence_value": large_source_row["title"],
        "provider_evidence_value": large_source_row["provider"],
        "source_url_evidence_value": large_source_row["source_url"],
        "access_method_evidence_value": large_source_row["access_method"],
        "downloaded_at_evidence_value": large_source_row["downloaded_at"],
        "file_size_bytes_evidence_value": large_source_row["file_size_bytes"],
        "checksum_sha256_evidence_value": large_source_row["checksum_sha256"],
        "storage_status_evidence_value": large_source_row["storage_status"],
        "storage_hint_evidence_value": large_source_row["storage_hint"],
        "handling_strategy_evidence_value": large_source_row["handling_strategy"],
        "derived_record_paths_evidence_value": large_source_row["derived_record_paths"],
        "rights_status_evidence_value": large_source_row["rights_status"],
        "risk_note_evidence_value": large_source_row["risk_note"],
        "review_status_evidence_value": large_source_row["review_status"],
        "source_updated_at_evidence_value": large_source_row["updated_at"],
        "large_source_evidence_status": LARGE_SOURCE_EVIDENCE_STATUS,
        "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
        "file_size_review_status": FILE_SIZE_REVIEW_STATUS,
        "checksum_review_status": CHECKSUM_REVIEW_STATUS,
        "storage_boundary_review_status": STORAGE_BOUNDARY_REVIEW_STATUS,
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
                "source_package_id": source_package_id,
                "file_size_bytes": large_source_row["file_size_bytes"],
                "checksum_sha256_present": str(bool(large_source_row["checksum_sha256"])).lower(),
                "storage_status": large_source_row["storage_status"],
                "rights_status": large_source_row["rights_status"],
                "review_status": large_source_row["review_status"],
            }
        ),
        "required_next_checks": (
            "open_058_large_source_register_capture_result;cross_check_against_056_source_register_and_057_download_log;"
            "do_not_commit_raw_package_or_infer_rights_identity_assignment_or_decipherment"
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_capture_results(
    capture_scaffold_rows: list[dict[str, str]],
    checklist_rows: list[dict[str, str]],
    large_source_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    large_source_by_id = {row["source_package_id"]: row for row in large_source_rows}
    checklist_by_task = _checklist_by_capture_task(checklist_rows)
    rows: list[dict[str, str]] = []
    for task in _large_source_tasks(capture_scaffold_rows):
        source_package_id = task["source_record_refs"]
        if source_package_id not in large_source_by_id:
            raise ValueError(f"missing large source register row for {source_package_id}")
        if task["capture_task_id"] not in checklist_by_task:
            raise ValueError(f"missing checklist row for {task['capture_task_id']}")
        rows.append(
            _capture_row(
                len(rows) + 1,
                task,
                checklist_by_task[task["capture_task_id"]],
                large_source_by_id[source_package_id],
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
    parser.add_argument("--large-source-register", default=str(LARGE_SOURCE_REGISTER))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_capture_results(
        read_csv_rows(root / args.capture_scaffold),
        read_csv_rows(root / args.capture_review_checklist),
        read_csv_rows(root / args.large_source_register),
    )
    write_csv(root / args.output, rows)
    print(
        f"capture_result_count={len(rows)} "
        f"source_package_count={len({row['source_package_id'] for row in rows})} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
