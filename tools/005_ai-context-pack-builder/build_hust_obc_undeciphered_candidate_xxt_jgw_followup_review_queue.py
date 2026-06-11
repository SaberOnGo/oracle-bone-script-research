#!/usr/bin/env python3
"""Build metadata-only Xiaoxuetang follow-up review queue rows from route-probe results."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


NOTE_UPDATE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "070_ai-agent-hust-obc-undeciphered-candidate-source-image-reference-note-update-results.csv"
)
ROUTE_PROBE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "071_ai-agent-hust-obc-undeciphered-candidate-xxt-jgw-route-probe-results.csv"
)
SOURCE_INDEX = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "001_all-sources-index.csv"
)
SOURCE_DOWNLOAD_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "003_source-download-manifest.csv"
)
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "072_ai-agent-hust-obc-undeciphered-candidate-xxt-jgw-followup-review-queue.csv"
)
UPDATED_AT = "2026-06-11"
FOLLOWUP_METHOD = "manual_browser_or_institutional_export_required"
PRIORITY_BUCKET = "xxt_jgw_tls_access_boundary_followup"
RESEARCH_BOUNDARY = "hust_obc_xxt_jgw_followup_review_queue_not_scholarship"
EVIDENCE_COLLECTION_STATUS = "followup_review_not_started"
HUMAN_REVIEW_STATUS = "not_started"
FORMAL_SCHEMA_COMPATIBILITY_STATUS = "not_formal_obs_char_schema"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
NO_CLAIM = "no_claim"
REQUIRED_NEXT_CHECKS = (
    "open_071_route_probe_result;open_070_note_update_result;open_full_inscription_context_note_draft;"
    "verify_registered_xxt_source_and_download_rows;use_manual_browser_or_institutional_export_before_any_catalog_claim;"
    "record_no_identity_assignment_or_decipherment_claim"
)
CAUTION = (
    "This queue row is a metadata-only follow-up route for an official Xiaoxuetang page probe. "
    "It tracks source-marked route files, registered download rows, and the need for manual or "
    "institutional access follow-up; it is not catalog confirmation, not a Heji crosswalk, not "
    "a collection match, not a formal obs-char assignment, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "xxt_followup_review_task_id",
    "priority_rank",
    "priority_bucket",
    "followup_method",
    "route_probe_result_id",
    "note_update_result_id",
    "source_image_reference_extraction_summary_id",
    "context_pack_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "target_evidence_section",
    "note_draft_path",
    "source_id",
    "target_source_id",
    "targeted_download_id",
    "targeted_url",
    "candidate_filename_number_probe_token",
    "source_class_path",
    "source_image_count_expected",
    "source_image_count_extracted",
    "official_route_kind",
    "automated_fetch_client_matrix",
    "automated_fetch_status",
    "official_access_boundary_status",
    "source_register_match_count",
    "source_register_rights_statuses",
    "source_register_review_statuses",
    "download_manifest_match_count",
    "download_manifest_artifact_kinds",
    "download_manifest_commit_policies",
    "download_log_match_count",
    "download_log_access_statuses",
    "route_file_count",
    "missing_route_file_count",
    "route_file_review_status",
    "expected_output_path",
    "route_files_to_open",
    "required_review_sections",
    "required_next_checks",
    "evidence_collection_status",
    "human_review_status",
    "formal_schema_compatibility_status",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "assignment_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
    "research_boundary",
    "rights_status",
    "risk_note",
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


def _compact(values: list[str]) -> str:
    return ";".join(value for value in values if value)


def _expected_output_path(index: int, route_row: dict[str, str]) -> str:
    return (
        "doc/public/user_research/007_xxt-jgw-route-probe-review-queues/"
        "001_tls-access-boundary/"
        f"{index:04d}_{route_row['unknown_candidate_id']}_{route_row['targeted_download_id']}_review-log.md"
    )


def _route_files(note_row: dict[str, str]) -> list[str]:
    return [
        NOTE_UPDATE_RESULTS.as_posix(),
        ROUTE_PROBE_RESULTS.as_posix(),
        note_row["note_draft_path"],
        SOURCE_INDEX.as_posix(),
        SOURCE_DOWNLOAD_MANIFEST.as_posix(),
        SOURCE_DOWNLOAD_LOG.as_posix(),
    ]


def _route_file_status(root: Path, route_files: list[str]) -> tuple[int, str]:
    missing_count = sum(1 for route_file in route_files if not (root / route_file).exists())
    status = "reviewed_route_files_exist" if missing_count == 0 else "route_files_missing"
    return missing_count, status


def _by_key(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows}


def build_followup_review_rows(
    note_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    manifest_rows: list[dict[str, str]],
    download_rows: list[dict[str, str]],
    root: Path,
) -> list[dict[str, str]]:
    note_by_id = _by_key(note_rows, "note_update_result_id")
    source_by_id = _by_key(source_rows, "source_id")
    manifest_by_id = _by_key(manifest_rows, "download_id")
    download_by_id = _by_key(download_rows, "download_id")

    sorted_route_rows = sorted(
        route_rows,
        key=lambda row: (-int(row["source_image_count_expected"]) if row.get("source_image_count_expected") else 0, row["route_probe_result_id"]),
    )

    results: list[dict[str, str]] = []
    for index, route_row in enumerate(sorted_route_rows, start=1):
        note_row = note_by_id[route_row["note_update_result_id"]]
        source_match = source_by_id.get(route_row["target_source_id"])
        manifest_match = manifest_by_id.get(route_row["targeted_download_id"])
        download_match = download_by_id.get(route_row["targeted_download_id"])
        route_files = _route_files(note_row)
        missing_route_file_count, route_file_review_status = _route_file_status(root, route_files)
        results.append(
            {
                "xxt_followup_review_task_id": f"hust-obc-xxt-followup-review-{index:04d}",
                "priority_rank": str(index),
                "priority_bucket": PRIORITY_BUCKET,
                "followup_method": FOLLOWUP_METHOD,
                "route_probe_result_id": route_row["route_probe_result_id"],
                "note_update_result_id": route_row["note_update_result_id"],
                "source_image_reference_extraction_summary_id": route_row[
                    "source_image_reference_extraction_summary_id"
                ],
                "context_pack_id": note_row["context_pack_id"],
                "unknown_candidate_id": route_row["unknown_candidate_id"],
                "primary_external_ref_id": route_row["primary_external_ref_id"],
                "target_evidence_section": note_row["target_evidence_section"],
                "note_draft_path": note_row["note_draft_path"],
                "source_id": route_row["source_id"],
                "target_source_id": route_row["target_source_id"],
                "targeted_download_id": route_row["targeted_download_id"],
                "targeted_url": route_row["targeted_url"],
                "candidate_filename_number_probe_token": route_row[
                    "candidate_filename_number_probe_token"
                ],
                "source_class_path": note_row["source_class_path"],
                "source_image_count_expected": note_row["source_image_count_expected"],
                "source_image_count_extracted": note_row["source_image_count_extracted"],
                "official_route_kind": route_row["official_route_kind"],
                "automated_fetch_client_matrix": route_row["automated_fetch_client_matrix"],
                "automated_fetch_status": route_row["automated_fetch_status"],
                "official_access_boundary_status": route_row["official_access_boundary_status"],
                "source_register_match_count": "1" if source_match else "0",
                "source_register_rights_statuses": (
                    f"{route_row['target_source_id']}={source_match['rights_status']}"
                    if source_match
                    else ""
                ),
                "source_register_review_statuses": (
                    f"{route_row['target_source_id']}={source_match['review_status']}"
                    if source_match
                    else ""
                ),
                "download_manifest_match_count": "1" if manifest_match else "0",
                "download_manifest_artifact_kinds": (
                    f"{route_row['targeted_download_id']}={manifest_match['artifact_kind']}"
                    if manifest_match
                    else ""
                ),
                "download_manifest_commit_policies": (
                    f"{route_row['targeted_download_id']}={manifest_match['commit_policy']}"
                    if manifest_match
                    else ""
                ),
                "download_log_match_count": "1" if download_match else "0",
                "download_log_access_statuses": (
                    f"{route_row['targeted_download_id']}={download_match['status']}:{download_match['http_status']}"
                    if download_match
                    else ""
                ),
                "route_file_count": str(len(route_files)),
                "missing_route_file_count": str(missing_route_file_count),
                "route_file_review_status": route_file_review_status,
                "expected_output_path": _expected_output_path(index, route_row),
                "route_files_to_open": _compact(route_files),
                "required_review_sections": (
                    "route_probe_result;note_update_result;full_inscription_context_note;"
                    "source_register_row;source_download_manifest_row;download_log_row;"
                    "official_access_boundary;review_log"
                ),
                "required_next_checks": REQUIRED_NEXT_CHECKS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "human_review_status": HUMAN_REVIEW_STATUS,
                "formal_schema_compatibility_status": FORMAL_SCHEMA_COMPATIBILITY_STATUS,
                "rights_decision_status": "no_new_rights_decision",
                "source_promotion_status": "not_promoted",
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "assignment_status": ASSIGNMENT_STATUS,
                "decipherment_claim_status": NO_CLAIM,
                "component_claim_status": NO_CLAIM,
                "evolution_chain_claim_status": NO_CLAIM,
                "research_boundary": RESEARCH_BOUNDARY,
                "rights_status": note_row["source_rights_status"],
                "risk_note": route_row["risk_note"],
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return results


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--notes", default=str(NOTE_UPDATE_RESULTS))
    parser.add_argument("--routes", default=str(ROUTE_PROBE_RESULTS))
    parser.add_argument("--source-index", default=str(SOURCE_INDEX))
    parser.add_argument("--download-manifest", default=str(SOURCE_DOWNLOAD_MANIFEST))
    parser.add_argument("--download-log", default=str(SOURCE_DOWNLOAD_LOG))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = repo_root()
    rows = build_followup_review_rows(
        read_csv_rows(root / args.notes),
        read_csv_rows(root / args.routes),
        read_csv_rows(root / args.source_index),
        read_csv_rows(root / args.download_manifest),
        read_csv_rows(root / args.download_log),
        root,
    )
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
