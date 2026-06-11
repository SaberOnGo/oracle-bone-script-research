#!/usr/bin/env python3
"""Capture candidate-packet metadata for HUST-OBC undeciphered candidates."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


EVIDENCE_CAPTURE_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "054_ai-agent-hust-obc-undeciphered-candidate-evidence-capture-scaffold.csv"
)
CAPTURE_REVIEW_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/"
    "055_ai-agent-hust-obc-undeciphered-candidate-evidence-capture-review-checklist.csv"
)
UNDECIPHERED_INDEX = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "003_undeciphered-oracle-characters-index.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "059_ai-agent-hust-obc-undeciphered-candidate-packet-capture-results.csv"
)
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_candidate_packet_capture_result_not_scholarship"
CANDIDATE_PACKET_ROW_STATUS = "reviewed_candidate_packet_found"
BUCKET_MANIFEST_ROW_STATUS = "reviewed_bucket_manifest_row_found"
UNDECIPHERED_INDEX_ROW_STATUS = "reviewed_undeciphered_index_row_found"
CANDIDATE_PACKET_EVIDENCE_STATUS = "metadata_captured_from_reviewed_candidate_packet"
EVIDENCE_COLLECTION_STATUS = "candidate_packet_metadata_captured"
RIGHTS_DECISION_STATUS = "candidate_packet_value_captured_no_new_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
DECIPHERMENT_CLAIM_STATUS = "no_claim"
COMPONENT_CLAIM_STATUS = "no_claim"
EVOLUTION_CHAIN_CLAIM_STATUS = "no_claim"
CAPTURE_STATUS = "reviewed_metadata_only"
CAUTION = (
    "This row captures HUST-OBC undeciphered candidate-packet metadata for later "
    "evidence review. It copies dataset candidate IDs, source class paths, image "
    "counts, first and last source-image paths, rights status, and risk notes only; "
    "it is not an accepted oracle-character identity, not a formal obs-char "
    "assignment, not an accepted reading, not a component assignment, not an "
    "evolution-chain assignment, not source promotion, not a new rights decision, "
    "and not a decipherment conclusion."
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
    "candidate_packet_path",
    "bucket_manifest_path",
    "undeciphered_index_path",
    "candidate_packet_row_status",
    "bucket_manifest_row_status",
    "undeciphered_index_row_status",
    "record_type_evidence_value",
    "source_id_evidence_value",
    "source_package_id_evidence_value",
    "evidence_download_id_evidence_value",
    "source_group_evidence_value",
    "source_group_label_evidence_value",
    "source_class_id_evidence_value",
    "source_class_path_evidence_value",
    "source_image_count_evidence_value",
    "first_source_image_path_evidence_value",
    "last_source_image_path_evidence_value",
    "filename_source_prefixes_evidence_value",
    "bucket_sequence_evidence_value",
    "bucket_manifest_review_status_evidence_value",
    "source_reported_undeciphered_class_count_evidence_value",
    "zip_observed_undeciphered_class_count_evidence_value",
    "zip_observed_undeciphered_image_count_evidence_value",
    "materialization_status_evidence_value",
    "decipherment_status_evidence_value",
    "identity_claim_status_evidence_value",
    "assignment_status_evidence_value",
    "promotion_status_evidence_value",
    "rights_status_evidence_value",
    "risk_note_evidence_value",
    "packet_review_status_evidence_value",
    "packet_updated_at_evidence_value",
    "candidate_packet_evidence_status",
    "evidence_collection_status",
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


def read_json_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object in {path}")
    return data


def _candidate_packet_tasks(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    tasks = [row for row in rows if row.get("target_evidence_section") == "candidate_packet"]
    tasks.sort(key=lambda row: row["capture_task_id"])
    return tasks


def _summary(parts: dict[str, str]) -> str:
    return ";".join(f"{key}={value}" for key, value in parts.items())


def _checklist_by_capture_task(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    packet_rows = _candidate_packet_tasks(rows)
    for row in packet_rows:
        if row["checklist_status"] != "not_started":
            raise ValueError(f"unexpected checklist_status for {row['capture_task_id']}")
        if row["evidence_collection_status"] != "not_collected":
            raise ValueError(f"unexpected evidence_collection_status for {row['capture_task_id']}")
        if "open_candidate_packet" not in row["required_review_checks"]:
            raise ValueError(f"missing candidate-packet review check for {row['capture_task_id']}")
    return {row["capture_task_id"]: row for row in packet_rows}


def _candidate_refs(task: dict[str, str]) -> dict[str, str]:
    parts = task["source_record_refs"].split(";")
    if len(parts) != 4:
        raise ValueError(f"unexpected candidate refs for {task['capture_task_id']}")
    return {
        "unknown_candidate_id": parts[0],
        "primary_external_ref_id": parts[1],
        "source_class_id": parts[2],
        "source_class_path": parts[3],
    }


def _bucket_manifest_path(packet_path: Path) -> Path:
    return packet_path.parents[1] / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"


def _bucket_row_by_candidate(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["unknown_candidate_id"]: row for row in rows}


def _index_row_by_candidate(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["unknown_candidate_id"]: row for row in rows}


def _packet_value(packet: dict[str, Any], field: str) -> str:
    value = packet.get(field, "")
    return str(value)


def _validate_candidate_sources(
    task: dict[str, str],
    packet: dict[str, Any],
    bucket_row: dict[str, str],
    index_row: dict[str, str],
) -> None:
    refs = _candidate_refs(task)
    checks = {
        "unknown_candidate_id": refs["unknown_candidate_id"],
        "primary_external_ref_id": refs["primary_external_ref_id"],
        "source_class_id": refs["source_class_id"],
        "source_class_path": refs["source_class_path"],
    }
    for field, expected in checks.items():
        if _packet_value(packet, field) != expected:
            raise ValueError(f"packet {field} mismatch for {task['capture_task_id']}")
        if index_row[field] != expected:
            raise ValueError(f"undeciphered index {field} mismatch for {task['capture_task_id']}")
    for field in ["unknown_candidate_id", "primary_external_ref_id", "source_class_id"]:
        if bucket_row[field] != checks[field]:
            raise ValueError(f"bucket manifest {field} mismatch for {task['capture_task_id']}")
    if bucket_row["packet_path"] != task["source_route_path"]:
        raise ValueError(f"bucket manifest packet_path mismatch for {task['capture_task_id']}")
    if index_row["materialized_candidate_packet_path"] != task["source_route_path"]:
        raise ValueError(f"undeciphered index packet path mismatch for {task['capture_task_id']}")
    if bucket_row["source_image_count"] != _packet_value(packet, "source_image_count"):
        raise ValueError(f"bucket manifest image count mismatch for {task['capture_task_id']}")
    if index_row["source_image_count"] != _packet_value(packet, "source_image_count"):
        raise ValueError(f"undeciphered index image count mismatch for {task['capture_task_id']}")


def _capture_row(
    index: int,
    task: dict[str, str],
    checklist_row: dict[str, str],
    packet: dict[str, Any],
    bucket_manifest_path: Path,
    bucket_row: dict[str, str],
    index_row: dict[str, str],
) -> dict[str, str]:
    return {
        "capture_result_id": f"hust-obc-undeciphered-candidate-packet-capture-result-{index:04d}",
        "checklist_id": checklist_row["checklist_id"],
        "capture_task_id": task["capture_task_id"],
        "route_result_id": task["route_result_id"],
        "review_log_draft_id": task["review_log_draft_id"],
        "undeciphered_review_task_id": task["undeciphered_review_task_id"],
        "context_pack_id": task["context_pack_id"],
        "unknown_candidate_id": task["unknown_candidate_id"],
        "primary_external_ref_id": task["primary_external_ref_id"],
        "candidate_packet_path": task["source_route_path"],
        "bucket_manifest_path": bucket_manifest_path.as_posix(),
        "undeciphered_index_path": UNDECIPHERED_INDEX.as_posix(),
        "candidate_packet_row_status": CANDIDATE_PACKET_ROW_STATUS,
        "bucket_manifest_row_status": BUCKET_MANIFEST_ROW_STATUS,
        "undeciphered_index_row_status": UNDECIPHERED_INDEX_ROW_STATUS,
        "record_type_evidence_value": _packet_value(packet, "record_type"),
        "source_id_evidence_value": _packet_value(packet, "source_id"),
        "source_package_id_evidence_value": _packet_value(packet, "source_package_id"),
        "evidence_download_id_evidence_value": _packet_value(packet, "evidence_download_id"),
        "source_group_evidence_value": _packet_value(packet, "source_group"),
        "source_group_label_evidence_value": _packet_value(packet, "source_group_label"),
        "source_class_id_evidence_value": _packet_value(packet, "source_class_id"),
        "source_class_path_evidence_value": _packet_value(packet, "source_class_path"),
        "source_image_count_evidence_value": _packet_value(packet, "source_image_count"),
        "first_source_image_path_evidence_value": _packet_value(packet, "first_source_image_path"),
        "last_source_image_path_evidence_value": _packet_value(packet, "last_source_image_path"),
        "filename_source_prefixes_evidence_value": _packet_value(packet, "filename_source_prefixes"),
        "bucket_sequence_evidence_value": bucket_row["bucket_sequence"],
        "bucket_manifest_review_status_evidence_value": bucket_row["review_status"],
        "source_reported_undeciphered_class_count_evidence_value": index_row[
            "source_reported_undeciphered_class_count"
        ],
        "zip_observed_undeciphered_class_count_evidence_value": index_row[
            "zip_observed_undeciphered_class_count"
        ],
        "zip_observed_undeciphered_image_count_evidence_value": index_row[
            "zip_observed_undeciphered_image_count"
        ],
        "materialization_status_evidence_value": index_row["materialization_status"],
        "decipherment_status_evidence_value": _packet_value(packet, "decipherment_status"),
        "identity_claim_status_evidence_value": _packet_value(packet, "identity_claim_status"),
        "assignment_status_evidence_value": _packet_value(packet, "assignment_status"),
        "promotion_status_evidence_value": _packet_value(packet, "promotion_status"),
        "rights_status_evidence_value": _packet_value(packet, "rights_status"),
        "risk_note_evidence_value": _packet_value(packet, "risk_note"),
        "packet_review_status_evidence_value": _packet_value(packet, "review_status"),
        "packet_updated_at_evidence_value": _packet_value(packet, "updated_at"),
        "candidate_packet_evidence_status": CANDIDATE_PACKET_EVIDENCE_STATUS,
        "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
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
                "unknown_candidate_id": task["unknown_candidate_id"],
                "source_class_path": _packet_value(packet, "source_class_path"),
                "source_image_count": _packet_value(packet, "source_image_count"),
                "packet_review_status": _packet_value(packet, "review_status"),
                "index_materialization_status": index_row["materialization_status"],
            }
        ),
        "required_next_checks": (
            "open_059_candidate_packet_capture_result;cross_check_against_056_057_058;"
            "do_not_promote_dataset_candidate_to_formal_obs_char_or_decipherment"
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_capture_results(
    capture_scaffold_rows: list[dict[str, str]],
    checklist_rows: list[dict[str, str]],
    undeciphered_index_rows: list[dict[str, str]],
    root: Path | None = None,
) -> list[dict[str, str]]:
    root = repo_root() if root is None else root
    checklist_by_task = _checklist_by_capture_task(checklist_rows)
    index_by_candidate = _index_row_by_candidate(undeciphered_index_rows)
    bucket_manifest_cache: dict[Path, dict[str, dict[str, str]]] = {}
    rows: list[dict[str, str]] = []
    for task in _candidate_packet_tasks(capture_scaffold_rows):
        packet_path = Path(task["source_route_path"])
        absolute_packet_path = root / packet_path
        bucket_manifest_path = _bucket_manifest_path(packet_path)
        if bucket_manifest_path not in bucket_manifest_cache:
            bucket_manifest_cache[bucket_manifest_path] = _bucket_row_by_candidate(
                read_csv_rows(root / bucket_manifest_path)
            )
        bucket_rows = bucket_manifest_cache[bucket_manifest_path]
        candidate_id = task["unknown_candidate_id"]
        if task["capture_task_id"] not in checklist_by_task:
            raise ValueError(f"missing checklist row for {task['capture_task_id']}")
        if candidate_id not in bucket_rows:
            raise ValueError(f"missing bucket manifest row for {candidate_id}")
        if candidate_id not in index_by_candidate:
            raise ValueError(f"missing undeciphered index row for {candidate_id}")
        packet = read_json_object(absolute_packet_path)
        bucket_row = bucket_rows[candidate_id]
        index_row = index_by_candidate[candidate_id]
        _validate_candidate_sources(task, packet, bucket_row, index_row)
        rows.append(
            _capture_row(
                len(rows) + 1,
                task,
                checklist_by_task[task["capture_task_id"]],
                packet,
                bucket_manifest_path,
                bucket_row,
                index_row,
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
    parser.add_argument("--undeciphered-index", default=str(UNDECIPHERED_INDEX))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_capture_results(
        read_csv_rows(root / args.capture_scaffold),
        read_csv_rows(root / args.capture_review_checklist),
        read_csv_rows(root / args.undeciphered_index),
        root=root,
    )
    write_csv(root / args.output, rows)
    print(
        f"capture_result_count={len(rows)} "
        f"candidate_count={len({row['unknown_candidate_id'] for row in rows})} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
