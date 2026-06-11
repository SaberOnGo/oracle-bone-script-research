#!/usr/bin/env python3
"""Build source/asset metadata evidence capture rows for HUST-OBC unknown candidates."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


NOTE_DRAFT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/"
    "063_ai-agent-hust-obc-undeciphered-candidate-evidence-collection-note-draft-manifest.csv"
)
TASK_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/"
    "062_ai-agent-hust-obc-undeciphered-candidate-evidence-collection-task-queue.csv"
)
SOURCE_REGISTER_CAPTURE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "056_ai-agent-hust-obc-undeciphered-candidate-source-register-capture-results.csv"
)
DOWNLOAD_LOG_CAPTURE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "057_ai-agent-hust-obc-undeciphered-candidate-download-log-capture-results.csv"
)
LARGE_SOURCE_REGISTER_CAPTURE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "058_ai-agent-hust-obc-undeciphered-candidate-large-source-register-capture-results.csv"
)
CANDIDATE_PACKET_CAPTURE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "059_ai-agent-hust-obc-undeciphered-candidate-packet-capture-results.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "064_ai-agent-hust-obc-undeciphered-candidate-source-metadata-evidence-capture-results.csv"
)
TARGET_SECTION = "source_references_and_asset_metadata"
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_source_metadata_evidence_capture_result_not_scholarship"
CAUTION = (
    "This row captures already reviewed source, download, large-source, and "
    "candidate-packet metadata for a later collection note. It is not a new "
    "download, not a raw file commit, not a checksum recalculation, not a new "
    "rights decision, not source promotion, not an accepted glyph identity, not "
    "a formal obs-char assignment, not an accepted reading, not a component "
    "assignment, not an evolution-chain assignment, and not a decipherment "
    "conclusion."
)

OUTPUT_FIELDS = [
    "source_metadata_evidence_capture_result_id",
    "evidence_collection_note_draft_id",
    "evidence_collection_task_id",
    "evidence_pack_scaffold_id",
    "readiness_check_id",
    "route_result_id",
    "review_log_draft_id",
    "undeciphered_review_task_id",
    "context_pack_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "target_evidence_section",
    "note_draft_path",
    "task_expected_output_path",
    "task_queue_source_path",
    "task_collection_scope",
    "route_hints",
    "route_files_to_open",
    "source_register_capture_result_id",
    "download_log_capture_result_id",
    "large_source_register_capture_result_id",
    "candidate_packet_capture_result_id",
    "source_id",
    "source_title",
    "source_provider",
    "source_authority_tier",
    "source_url",
    "source_scope",
    "source_rights_status",
    "source_risk_note",
    "source_review_status",
    "source_register_path",
    "download_id",
    "download_url",
    "downloaded_at",
    "download_status",
    "http_status",
    "download_file_size_bytes",
    "download_checksum_sha256",
    "local_archive_path",
    "download_risk_note",
    "download_log_path",
    "source_package_id",
    "large_source_title",
    "large_source_access_method",
    "large_source_storage_status",
    "large_source_storage_hint",
    "large_source_handling_strategy",
    "large_source_derived_record_paths",
    "large_source_rights_status",
    "large_source_risk_note",
    "large_source_register_path",
    "candidate_packet_path",
    "bucket_manifest_path",
    "undeciphered_index_path",
    "source_group",
    "source_group_label",
    "source_class_id",
    "source_class_path",
    "source_image_count",
    "first_source_image_path",
    "last_source_image_path",
    "filename_source_prefixes",
    "bucket_sequence",
    "source_reported_undeciphered_class_count",
    "zip_observed_undeciphered_class_count",
    "zip_observed_undeciphered_image_count",
    "candidate_materialization_status",
    "candidate_packet_review_status",
    "evidence_value_status",
    "evidence_collection_status",
    "note_update_status",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "assignment_status",
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


def _by_id(rows: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        key = row[field]
        if key in result:
            raise ValueError(f"duplicate {field}: {key}")
        result[key] = row
    return result


def _require_match(row: dict[str, str], other: dict[str, str], fields: list[str]) -> None:
    for field in fields:
        if row[field] != other[field]:
            raise ValueError(f"field mismatch for {field}: {row[field]} != {other[field]}")


def _assert_note_and_task_ready(note: dict[str, str], task: dict[str, str]) -> None:
    if note["target_evidence_section"] != TARGET_SECTION:
        raise ValueError(f"unexpected note target section: {note['target_evidence_section']}")
    if task["target_evidence_section"] != TARGET_SECTION:
        raise ValueError(f"unexpected task target section: {task['target_evidence_section']}")
    if note["note_status"] != "draft_not_collected":
        raise ValueError(f"note is not a draft-not-collected row: {note['evidence_collection_note_draft_id']}")
    if note["evidence_collection_status"] != "not_collected":
        raise ValueError(f"note already collected: {note['evidence_collection_note_draft_id']}")
    if task["task_status"] != "not_started":
        raise ValueError(f"task already started: {task['evidence_collection_task_id']}")
    if task["evidence_collection_status"] != "not_collected":
        raise ValueError(f"task already collected: {task['evidence_collection_task_id']}")


def _build_row(
    index: int,
    note: dict[str, str],
    task: dict[str, str],
    source: dict[str, str],
    download: dict[str, str],
    large_source: dict[str, str],
    candidate: dict[str, str],
) -> dict[str, str]:
    identity_fields = [
        "route_result_id",
        "review_log_draft_id",
        "undeciphered_review_task_id",
        "context_pack_id",
        "unknown_candidate_id",
        "primary_external_ref_id",
    ]
    _require_match(note, task, ["evidence_collection_task_id", *identity_fields])
    for capture_row in [source, download, large_source, candidate]:
        _require_match(note, capture_row, identity_fields)
    _assert_note_and_task_ready(note, task)

    return {
        "source_metadata_evidence_capture_result_id": (
            f"hust-obc-undeciphered-source-metadata-evidence-capture-result-{index:04d}"
        ),
        "evidence_collection_note_draft_id": note["evidence_collection_note_draft_id"],
        "evidence_collection_task_id": note["evidence_collection_task_id"],
        "evidence_pack_scaffold_id": note["evidence_pack_scaffold_id"],
        "readiness_check_id": note["readiness_check_id"],
        "route_result_id": note["route_result_id"],
        "review_log_draft_id": note["review_log_draft_id"],
        "undeciphered_review_task_id": note["undeciphered_review_task_id"],
        "context_pack_id": note["context_pack_id"],
        "unknown_candidate_id": note["unknown_candidate_id"],
        "primary_external_ref_id": note["primary_external_ref_id"],
        "target_evidence_section": note["target_evidence_section"],
        "note_draft_path": note["note_draft_path"],
        "task_expected_output_path": task["expected_output_path"],
        "task_queue_source_path": note["task_queue_source_path"],
        "task_collection_scope": task["collection_scope"],
        "route_hints": note["route_hints"],
        "route_files_to_open": note["route_files_to_open"],
        "source_register_capture_result_id": source["capture_result_id"],
        "download_log_capture_result_id": download["capture_result_id"],
        "large_source_register_capture_result_id": large_source["capture_result_id"],
        "candidate_packet_capture_result_id": candidate["capture_result_id"],
        "source_id": source["source_id"],
        "source_title": source["title_evidence_value"],
        "source_provider": source["provider_evidence_value"],
        "source_authority_tier": source["authority_tier_evidence_value"],
        "source_url": source["source_url_evidence_value"],
        "source_scope": source["scope_evidence_value"],
        "source_rights_status": source["rights_status_evidence_value"],
        "source_risk_note": source["risk_note_evidence_value"],
        "source_review_status": source["review_status_evidence_value"],
        "source_register_path": source["source_register_path"],
        "download_id": download["download_id"],
        "download_url": download["url_evidence_value"],
        "downloaded_at": download["downloaded_at_evidence_value"],
        "download_status": download["status_evidence_value"],
        "http_status": download["http_status_evidence_value"],
        "download_file_size_bytes": download["file_size_bytes_evidence_value"],
        "download_checksum_sha256": download["checksum_sha256_evidence_value"],
        "local_archive_path": download["local_temp_path_evidence_value"],
        "download_risk_note": download["risk_note_evidence_value"],
        "download_log_path": download["download_log_path"],
        "source_package_id": large_source["source_package_id"],
        "large_source_title": large_source["title_evidence_value"],
        "large_source_access_method": large_source["access_method_evidence_value"],
        "large_source_storage_status": large_source["storage_status_evidence_value"],
        "large_source_storage_hint": large_source["storage_hint_evidence_value"],
        "large_source_handling_strategy": large_source["handling_strategy_evidence_value"],
        "large_source_derived_record_paths": large_source["derived_record_paths_evidence_value"],
        "large_source_rights_status": large_source["rights_status_evidence_value"],
        "large_source_risk_note": large_source["risk_note_evidence_value"],
        "large_source_register_path": large_source["large_source_register_path"],
        "candidate_packet_path": candidate["candidate_packet_path"],
        "bucket_manifest_path": candidate["bucket_manifest_path"],
        "undeciphered_index_path": candidate["undeciphered_index_path"],
        "source_group": candidate["source_group_evidence_value"],
        "source_group_label": candidate["source_group_label_evidence_value"],
        "source_class_id": candidate["source_class_id_evidence_value"],
        "source_class_path": candidate["source_class_path_evidence_value"],
        "source_image_count": candidate["source_image_count_evidence_value"],
        "first_source_image_path": candidate["first_source_image_path_evidence_value"],
        "last_source_image_path": candidate["last_source_image_path_evidence_value"],
        "filename_source_prefixes": candidate["filename_source_prefixes_evidence_value"],
        "bucket_sequence": candidate["bucket_sequence_evidence_value"],
        "source_reported_undeciphered_class_count": candidate[
            "source_reported_undeciphered_class_count_evidence_value"
        ],
        "zip_observed_undeciphered_class_count": candidate[
            "zip_observed_undeciphered_class_count_evidence_value"
        ],
        "zip_observed_undeciphered_image_count": candidate[
            "zip_observed_undeciphered_image_count_evidence_value"
        ],
        "candidate_materialization_status": candidate["materialization_status_evidence_value"],
        "candidate_packet_review_status": candidate["packet_review_status_evidence_value"],
        "evidence_value_status": "metadata_evidence_captured",
        "evidence_collection_status": (
            "metadata_captured_from_reviewed_source_download_large_source_and_candidate_packet_rows"
        ),
        "note_update_status": "not_written_to_markdown_note",
        "rights_decision_status": "no_new_rights_decision",
        "source_promotion_status": "not_promoted",
        "identity_claim_status": "no_identity_claim",
        "assignment_status": "unknown_candidate_id_not_formal_obs_char_assignment",
        "decipherment_claim_status": "no_claim",
        "component_claim_status": "no_claim",
        "evolution_chain_claim_status": "no_claim",
        "research_boundary": RESEARCH_BOUNDARY,
        "required_next_checks": (
            "open_064_capture_result;update_063_source_metadata_note_after_human_review;"
            "cross_check_against_primary_catalog_or_inscription_context_before_identity_or_decipherment_claim"
        ),
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_source_metadata_evidence_capture_rows(
    note_rows: list[dict[str, str]],
    task_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    download_rows: list[dict[str, str]],
    large_source_rows: list[dict[str, str]],
    candidate_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    tasks_by_id = _by_id(task_rows, "evidence_collection_task_id")
    sources_by_id = _by_id(source_rows, "capture_result_id")
    downloads_by_id = _by_id(download_rows, "capture_result_id")
    large_sources_by_id = _by_id(large_source_rows, "capture_result_id")
    candidates_by_id = _by_id(candidate_rows, "capture_result_id")

    rows: list[dict[str, str]] = []
    target_notes = [row for row in note_rows if row["target_evidence_section"] == TARGET_SECTION]
    for note in sorted(target_notes, key=lambda row: row["evidence_collection_note_draft_id"]):
        task = tasks_by_id[note["evidence_collection_task_id"]]
        rows.append(
            _build_row(
                len(rows) + 1,
                note,
                task,
                sources_by_id[note["source_register_capture_result_id"]],
                downloads_by_id[note["download_log_capture_result_id"]],
                large_sources_by_id[note["large_source_register_capture_result_id"]],
                candidates_by_id[note["candidate_packet_capture_result_id"]],
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
    parser.add_argument("--note-draft-manifest", default=str(NOTE_DRAFT_MANIFEST))
    parser.add_argument("--task-queue", default=str(TASK_QUEUE))
    parser.add_argument("--source-register-capture-results", default=str(SOURCE_REGISTER_CAPTURE_RESULTS))
    parser.add_argument("--download-log-capture-results", default=str(DOWNLOAD_LOG_CAPTURE_RESULTS))
    parser.add_argument("--large-source-register-capture-results", default=str(LARGE_SOURCE_REGISTER_CAPTURE_RESULTS))
    parser.add_argument("--candidate-packet-capture-results", default=str(CANDIDATE_PACKET_CAPTURE_RESULTS))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_source_metadata_evidence_capture_rows(
        read_csv_rows(root / args.note_draft_manifest),
        read_csv_rows(root / args.task_queue),
        read_csv_rows(root / args.source_register_capture_results),
        read_csv_rows(root / args.download_log_capture_results),
        read_csv_rows(root / args.large_source_register_capture_results),
        read_csv_rows(root / args.candidate_packet_capture_results),
    )
    write_csv(root / args.output, rows)
    print(
        f"source_metadata_evidence_capture_result_count={len(rows)} "
        f"target_section={TARGET_SECTION} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
