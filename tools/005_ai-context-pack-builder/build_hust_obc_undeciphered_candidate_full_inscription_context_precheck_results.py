#!/usr/bin/env python3
"""Precheck inscription-context routes for HUST-OBC unknown candidates."""

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
SOURCE_METADATA_CAPTURE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "064_ai-agent-hust-obc-undeciphered-candidate-source-metadata-evidence-capture-results.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "066_ai-agent-hust-obc-undeciphered-candidate-full-inscription-context-precheck-results.csv"
)
TARGET_SECTION = "full_inscription_context"
UPDATED_AT = "2026-06-11"
NEXT_REGISTERED_SOURCE_ROUTES = "src-xiaoxuetang-jiaguwen;src-xiaoxuetang-obm;src-hust-obc"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_full_inscription_context_precheck_not_scholarship"
CAUTION = (
    "This row is a route precheck for full inscription context only. It records "
    "that the current candidate packet has dataset source-image paths but no "
    "primary catalog number, inscription transcription, Heji crosswalk, old "
    "catalog number, collection number, or excavation context captured yet. It "
    "is not proof of full inscription context, not an accepted glyph identity, "
    "not a formal obs-char assignment, not an accepted reading, not a component "
    "or evolution-chain assignment, not a rights decision, not source promotion, "
    "and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "full_inscription_context_precheck_result_id",
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
    "source_id",
    "source_package_id",
    "download_id",
    "candidate_packet_capture_result_id",
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
    "source_image_reference_status",
    "candidate_packet_context_status",
    "primary_catalog_context_status",
    "heji_crosswalk_status",
    "old_catalog_context_status",
    "collection_context_status",
    "excavation_context_status",
    "transcription_context_status",
    "inscription_context_evidence_status",
    "route_precheck_status",
    "next_registered_source_routes",
    "next_source_search_scope",
    "source_reported_undeciphered_class_count",
    "zip_observed_undeciphered_class_count",
    "zip_observed_undeciphered_image_count",
    "candidate_materialization_status",
    "candidate_packet_review_status",
    "source_rights_status",
    "large_source_rights_status",
    "large_source_risk_note",
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


def _assert_route_ready(note: dict[str, str], task: dict[str, str]) -> None:
    if note["target_evidence_section"] != TARGET_SECTION:
        raise ValueError(f"unexpected note target section: {note['target_evidence_section']}")
    if task["target_evidence_section"] != TARGET_SECTION:
        raise ValueError(f"unexpected task target section: {task['target_evidence_section']}")
    if note["note_status"] != "draft_not_collected":
        raise ValueError(f"note is not draft-not-collected: {note['evidence_collection_note_draft_id']}")
    if task["task_status"] != "not_started":
        raise ValueError(f"task already started: {task['evidence_collection_task_id']}")


def _build_row(
    index: int,
    note: dict[str, str],
    task: dict[str, str],
    source_metadata: dict[str, str],
) -> dict[str, str]:
    identity_fields = [
        "evidence_pack_scaffold_id",
        "readiness_check_id",
        "route_result_id",
        "review_log_draft_id",
        "undeciphered_review_task_id",
        "context_pack_id",
        "unknown_candidate_id",
        "primary_external_ref_id",
    ]
    _require_match(note, task, ["evidence_collection_task_id", *identity_fields])
    _require_match(note, source_metadata, identity_fields)
    _assert_route_ready(note, task)

    return {
        "full_inscription_context_precheck_result_id": (
            f"hust-obc-undeciphered-full-inscription-context-precheck-{index:04d}"
        ),
        "source_metadata_evidence_capture_result_id": source_metadata[
            "source_metadata_evidence_capture_result_id"
        ],
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
        "source_id": source_metadata["source_id"],
        "source_package_id": source_metadata["source_package_id"],
        "download_id": source_metadata["download_id"],
        "candidate_packet_capture_result_id": source_metadata["candidate_packet_capture_result_id"],
        "candidate_packet_path": source_metadata["candidate_packet_path"],
        "bucket_manifest_path": source_metadata["bucket_manifest_path"],
        "undeciphered_index_path": source_metadata["undeciphered_index_path"],
        "source_group": source_metadata["source_group"],
        "source_group_label": source_metadata["source_group_label"],
        "source_class_id": source_metadata["source_class_id"],
        "source_class_path": source_metadata["source_class_path"],
        "source_image_count": source_metadata["source_image_count"],
        "first_source_image_path": source_metadata["first_source_image_path"],
        "last_source_image_path": source_metadata["last_source_image_path"],
        "filename_source_prefixes": source_metadata["filename_source_prefixes"],
        "source_image_reference_status": "available_as_hust_obc_dataset_file_paths_only",
        "candidate_packet_context_status": "source_image_refs_only_no_primary_inscription_context",
        "primary_catalog_context_status": "not_found_in_current_candidate_packet_metadata",
        "heji_crosswalk_status": "not_collected",
        "old_catalog_context_status": "not_collected",
        "collection_context_status": "not_collected",
        "excavation_context_status": "not_collected",
        "transcription_context_status": "not_collected",
        "inscription_context_evidence_status": "not_collected_route_precheck_only",
        "route_precheck_status": "ready_for_registered_catalog_context_search",
        "next_registered_source_routes": NEXT_REGISTERED_SOURCE_ROUTES,
        "next_source_search_scope": (
            "search Xiaoxuetang oracle-character database, Xiaoxuetang OBM material-source table, "
            "and reviewed HUST-OBC source-image paths for primary catalog, Heji, old catalog, "
            "collection, excavation, and transcription context before any identity or decipherment claim"
        ),
        "source_reported_undeciphered_class_count": source_metadata[
            "source_reported_undeciphered_class_count"
        ],
        "zip_observed_undeciphered_class_count": source_metadata[
            "zip_observed_undeciphered_class_count"
        ],
        "zip_observed_undeciphered_image_count": source_metadata[
            "zip_observed_undeciphered_image_count"
        ],
        "candidate_materialization_status": source_metadata["candidate_materialization_status"],
        "candidate_packet_review_status": source_metadata["candidate_packet_review_status"],
        "source_rights_status": source_metadata["source_rights_status"],
        "large_source_rights_status": source_metadata["large_source_rights_status"],
        "large_source_risk_note": source_metadata["large_source_risk_note"],
        "evidence_value_status": "route_precheck_recorded_no_inscription_context_collected",
        "evidence_collection_status": "full_inscription_context_not_collected",
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
            "open_066_precheck_result;open_candidate_packet_source_image_refs;"
            "search_registered_catalog_routes_before_claiming_full_inscription_context;"
            "do_not_promote_dataset_candidate_to_formal_obs_char_or_decipherment"
        ),
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_full_inscription_context_precheck_rows(
    note_rows: list[dict[str, str]],
    task_rows: list[dict[str, str]],
    source_metadata_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    tasks_by_id = _by_id(task_rows, "evidence_collection_task_id")
    source_metadata_by_candidate = _by_id(source_metadata_rows, "unknown_candidate_id")

    rows: list[dict[str, str]] = []
    target_notes = [row for row in note_rows if row["target_evidence_section"] == TARGET_SECTION]
    for note in sorted(target_notes, key=lambda row: row["evidence_collection_note_draft_id"]):
        rows.append(
            _build_row(
                len(rows) + 1,
                note,
                tasks_by_id[note["evidence_collection_task_id"]],
                source_metadata_by_candidate[note["unknown_candidate_id"]],
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
    parser.add_argument("--source-metadata-capture-results", default=str(SOURCE_METADATA_CAPTURE_RESULTS))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_full_inscription_context_precheck_rows(
        read_csv_rows(root / args.note_draft_manifest),
        read_csv_rows(root / args.task_queue),
        read_csv_rows(root / args.source_metadata_capture_results),
    )
    write_csv(root / args.output, rows)
    print(
        f"full_inscription_context_precheck_result_count={len(rows)} "
        f"target_section={TARGET_SECTION} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
