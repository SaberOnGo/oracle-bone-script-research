#!/usr/bin/env python3
"""Build empty evidence-capture scaffolds from HUST-OBC undeciphered routes."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROUTE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "053_ai-agent-hust-obc-undeciphered-candidate-review-route-results.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "054_ai-agent-hust-obc-undeciphered-candidate-evidence-capture-scaffold.csv"
)
SOURCE_REGISTER_PATH = "corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv"
LARGE_SOURCE_REGISTER_PATH = "project_registry/006_large-source-register/001_large-source-register.csv"
SOURCE_DOWNLOAD_LOG_PATH = "project_registry/006_large-source-register/002_source-download-log.csv"
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_candidate_evidence_capture_scaffold_not_scholarship"
EVIDENCE_COLLECTION_STATUS = "not_collected"
CAPTURE_STATUS = "empty_scaffold_not_started"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
PROMOTION_STATUS = "not_promoted"
RIGHTS_DECISION_STATUS = "not_decided"
SOURCE_PROMOTION_STATUS = "not_promoted"
DECIPHERMENT_CLAIM_STATUS = "no_claim"
CAUTION = (
    "This row is an empty evidence-capture scaffold derived from metadata-only route "
    "results. Fill evidence-value fields only after opening the cited source-marked route "
    "files. Do not use this row as collected evidence, an accepted oracle-character "
    "identity, a formal obs-char assignment, a reading, a component assignment, an "
    "evolution-chain assignment, source promotion, a rights decision, or a decipherment "
    "conclusion."
)

SECTION_ORDER = ["candidate_packet", "source_register", "large_source_register", "download_log"]

OUTPUT_FIELDS = [
    "capture_task_id",
    "route_result_id",
    "review_log_draft_id",
    "undeciphered_review_task_id",
    "context_pack_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "target_evidence_section",
    "source_route_path",
    "source_record_refs",
    "route_metadata_summary",
    "capturable_field_names",
    "captured_evidence_value",
    "captured_evidence_source_id",
    "captured_evidence_source_path",
    "captured_evidence_note",
    "required_review_actions",
    "evidence_collection_status",
    "capture_status",
    "identity_claim_status",
    "assignment_status",
    "promotion_status",
    "rights_decision_status",
    "source_promotion_status",
    "decipherment_claim_status",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _summary(parts: dict[str, str]) -> str:
    return ";".join(f"{key}={value}" for key, value in parts.items())


def _base(row: dict[str, str], index: int, target_section: str) -> dict[str, str]:
    return {
        "capture_task_id": f"hust-obc-undeciphered-evidence-capture-{index:04d}",
        "route_result_id": row["route_result_id"],
        "review_log_draft_id": row["review_log_draft_id"],
        "undeciphered_review_task_id": row["undeciphered_review_task_id"],
        "context_pack_id": row["context_pack_id"],
        "unknown_candidate_id": row["unknown_candidate_id"],
        "primary_external_ref_id": row["primary_external_ref_id"],
        "target_evidence_section": target_section,
        "captured_evidence_value": "",
        "captured_evidence_source_id": "",
        "captured_evidence_source_path": "",
        "captured_evidence_note": "",
        "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
        "capture_status": CAPTURE_STATUS,
        "identity_claim_status": IDENTITY_CLAIM_STATUS,
        "assignment_status": ASSIGNMENT_STATUS,
        "promotion_status": PROMOTION_STATUS,
        "rights_decision_status": RIGHTS_DECISION_STATUS,
        "source_promotion_status": SOURCE_PROMOTION_STATUS,
        "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def _candidate_packet_row(row: dict[str, str], index: int) -> dict[str, str]:
    output = _base(row, index, "candidate_packet")
    output.update(
        {
            "source_route_path": row["candidate_packet_path"],
            "source_record_refs": ";".join(
                [
                    row["unknown_candidate_id"],
                    row["primary_external_ref_id"],
                    row["source_class_id"],
                    row["source_class_path"],
                ]
            ),
            "route_metadata_summary": _summary(
                {
                    "source_image_count": row["source_image_count"],
                    "packet_first_source_image_path": row["packet_first_source_image_path"],
                    "packet_last_source_image_path": row["packet_last_source_image_path"],
                    "candidate_packet_review_status": row["candidate_packet_review_status"],
                }
            ),
            "capturable_field_names": ";".join(
                [
                    "source_group",
                    "source_group_label",
                    "source_class_id",
                    "source_class_path",
                    "source_image_count",
                    "packet_first_source_image_path",
                    "packet_last_source_image_path",
                    "packet_filename_source_prefixes",
                    "candidate_packet_review_status",
                ]
            ),
            "required_review_actions": (
                "open_candidate_packet;copy_source_marked_packet_fields_only;"
                "leave_identity_assignment_reading_component_evolution_and_decipherment_blank"
            ),
        }
    )
    return output


def _source_register_row(row: dict[str, str], index: int) -> dict[str, str]:
    output = _base(row, index, "source_register")
    output.update(
        {
            "source_route_path": SOURCE_REGISTER_PATH,
            "source_record_refs": row["source_id"],
            "route_metadata_summary": _summary(
                {
                    "source_register_provider": row["source_register_provider"],
                    "source_register_authority_tier": row["source_register_authority_tier"],
                    "source_register_rights_status": row["source_register_rights_status"],
                    "source_register_review_status": row["source_register_review_status"],
                }
            ),
            "capturable_field_names": ";".join(
                [
                    "source_id",
                    "source_register_provider",
                    "source_register_authority_tier",
                    "source_register_rights_status",
                    "source_register_review_status",
                    "risk_note",
                ]
            ),
            "required_review_actions": (
                "open_source_register;verify_source_id_provider_authority_rights_and_risk;"
                "do_not_decide_new_rights_or_promote_source"
            ),
        }
    )
    return output


def _large_source_register_row(row: dict[str, str], index: int) -> dict[str, str]:
    output = _base(row, index, "large_source_register")
    output.update(
        {
            "source_route_path": LARGE_SOURCE_REGISTER_PATH,
            "source_record_refs": row["source_package_id"],
            "route_metadata_summary": _summary(
                {
                    "large_source_file_size_bytes": row["large_source_file_size_bytes"],
                    "large_source_checksum_sha256": row["large_source_checksum_sha256"],
                    "large_source_storage_status": row["large_source_storage_status"],
                    "large_source_review_status": row["large_source_review_status"],
                }
            ),
            "capturable_field_names": ";".join(
                [
                    "source_package_id",
                    "large_source_file_size_bytes",
                    "large_source_checksum_sha256",
                    "large_source_storage_status",
                    "large_source_rights_status",
                    "large_source_review_status",
                ]
            ),
            "required_review_actions": (
                "open_large_source_register;verify_raw_package_size_checksum_storage_and_rights;"
                "do_not_commit_raw_package_or_treat_availability_as_evidence"
            ),
        }
    )
    return output


def _download_log_row(row: dict[str, str], index: int) -> dict[str, str]:
    output = _base(row, index, "download_log")
    output.update(
        {
            "source_route_path": SOURCE_DOWNLOAD_LOG_PATH,
            "source_record_refs": row["evidence_download_id"],
            "route_metadata_summary": _summary(
                {
                    "download_log_status": row["download_log_status"],
                    "download_log_http_status": row["download_log_http_status"],
                    "download_log_file_size_bytes": row["download_log_file_size_bytes"],
                    "download_log_checksum_sha256": row["download_log_checksum_sha256"],
                }
            ),
            "capturable_field_names": ";".join(
                [
                    "evidence_download_id",
                    "download_log_status",
                    "download_log_http_status",
                    "download_log_file_size_bytes",
                    "download_log_checksum_sha256",
                    "download_log_local_temp_path",
                ]
            ),
            "required_review_actions": (
                "open_download_log;verify_download_id_status_size_checksum_and_temp_path;"
                "do_not_infer_rights_identity_or_decipherment_from_download_availability"
            ),
        }
    )
    return output


def build_capture_rows(route_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    builders = {
        "candidate_packet": _candidate_packet_row,
        "source_register": _source_register_row,
        "large_source_register": _large_source_register_row,
        "download_log": _download_log_row,
    }
    rows: list[dict[str, str]] = []
    for route_row in route_rows:
        for target_section in SECTION_ORDER:
            rows.append(builders[target_section](route_row, len(rows) + 1))
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--route-results", default=str(ROUTE_RESULTS))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_capture_rows(read_csv_rows(root / args.route_results))
    write_csv(root / args.output, rows)
    print(
        f"capture_task_count={len(rows)} "
        "sections=candidate_packet;source_register;large_source_register;download_log "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
