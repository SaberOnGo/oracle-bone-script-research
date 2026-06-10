#!/usr/bin/env python3
"""Build evidence-capture scaffolds from codepoint crosswalk route results."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROUTE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "043_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-route-results.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "044_ai-agent-hust-obimd-evobc-codepoint-crosswalk-evidence-capture-scaffold.csv"
)
SOURCE_REGISTER_PATH = (
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "001_all-sources-index.csv"
)
SOURCE_DOWNLOAD_LOG_PATH = "project_registry/006_large-source-register/002_source-download-log.csv"
UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "codepoint_crosswalk_evidence_capture_scaffold_not_scholarship"
EVIDENCE_COLLECTION_STATUS = "not_collected"
CAPTURE_STATUS = "not_started"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
PROMOTION_STATUS = "not_promoted"
CAUTION = (
    "This row is an evidence-capture scaffold derived from metadata-only route "
    "results. It identifies which local route record to open next, but it is not "
    "collected source evidence, not a confirmed oracle-character identity, not an "
    "accepted reading, not a component assignment, not an evolution-chain assignment, "
    "and not a decipherment conclusion."
)

SECTION_ORDER = ["candidate_packet", "source_register", "download_log"]

OUTPUT_FIELDS = [
    "capture_task_id",
    "route_result_id",
    "review_log_draft_id",
    "codepoint_review_task_id",
    "crosswalk_candidate_id",
    "suggested_oracle_character_id",
    "target_evidence_section",
    "source_route_path",
    "source_record_refs",
    "capturable_field_names",
    "captured_metadata_summary",
    "required_review_actions",
    "evidence_collection_status",
    "capture_status",
    "identity_claim_status",
    "promotion_status",
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
        "capture_task_id": f"codepoint-evidence-capture-{index:03d}",
        "route_result_id": row["route_result_id"],
        "review_log_draft_id": row["review_log_draft_id"],
        "codepoint_review_task_id": row["codepoint_review_task_id"],
        "crosswalk_candidate_id": row["crosswalk_candidate_id"],
        "suggested_oracle_character_id": row["suggested_oracle_character_id"],
        "target_evidence_section": target_section,
        "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
        "capture_status": CAPTURE_STATUS,
        "identity_claim_status": IDENTITY_CLAIM_STATUS,
        "promotion_status": PROMOTION_STATUS,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def _candidate_packet_row(row: dict[str, str], index: int) -> dict[str, str]:
    output = _base(row, index, "candidate_packet")
    output.update(
        {
            "source_route_path": row["hust_candidate_packet_path"],
            "source_record_refs": ";".join(
                [
                    row["hust_candidate_packet_id"],
                    row["hust_candidate_class_id"],
                    row["hust_validation_class_id"],
                    row["obimd_candidate_main_character_id"],
                    row["evobc_candidate_evolution_category_id"],
                ]
            ),
            "capturable_field_names": ";".join(
                [
                    "hust_candidate_packet_id",
                    "hust_candidate_class_id",
                    "hust_validation_class_id",
                    "hust_source_category_id_padded",
                    "hust_dataset_label_status",
                    "hust_dataset_label_codepoints",
                    "hust_packet_status",
                    "hust_packet_review_status",
                    "hust_packet_rights_status",
                    "obimd_candidate_main_character_id",
                    "obimd_codepoint_uplus",
                    "evobc_candidate_evolution_category_id",
                    "evobc_source_character_codepoints",
                    "evobc_image_reference_count",
                ]
            ),
            "captured_metadata_summary": _summary(
                {
                    "route_result_id": row["route_result_id"],
                    "hust_candidate_packet_id": row["hust_candidate_packet_id"],
                    "hust_packet_status": row["hust_packet_status"],
                    "hust_packet_review_status": row["hust_packet_review_status"],
                    "hust_packet_rights_status": row["hust_packet_rights_status"],
                    "obimd_candidate_main_character_id": row[
                        "obimd_candidate_main_character_id"
                    ],
                    "obimd_codepoint_uplus": row["obimd_codepoint_uplus"],
                    "evobc_candidate_evolution_category_id": row[
                        "evobc_candidate_evolution_category_id"
                    ],
                    "evobc_source_character_codepoints": row[
                        "evobc_source_character_codepoints"
                    ],
                    "evobc_image_reference_count": row["evobc_image_reference_count"],
                }
            ),
            "required_review_actions": (
                "open_hust_candidate_packet;verify_hust_obimd_evobc_staging_refs;"
                "record_metadata_only_no_identity_or_decipherment_claim"
            ),
        }
    )
    return output


def _source_register_row(row: dict[str, str], index: int) -> dict[str, str]:
    output = _base(row, index, "source_register")
    output.update(
        {
            "source_route_path": SOURCE_REGISTER_PATH,
            "source_record_refs": row["source_register_required_source_ids"],
            "capturable_field_names": ";".join(
                [
                    "source_register_required_source_ids",
                    "source_register_match_count",
                    "source_register_rights_statuses",
                    "source_register_review_statuses",
                    "source_register_review_status",
                ]
            ),
            "captured_metadata_summary": _summary(
                {
                    "route_result_id": row["route_result_id"],
                    "source_register_required_source_ids": row[
                        "source_register_required_source_ids"
                    ],
                    "source_register_match_count": row["source_register_match_count"],
                    "source_register_rights_statuses": row[
                        "source_register_rights_statuses"
                    ],
                    "source_register_review_statuses": row[
                        "source_register_review_statuses"
                    ],
                    "source_register_review_status": row["source_register_review_status"],
                }
            ),
            "required_review_actions": (
                "open_source_register;verify_required_source_rows;"
                "record_rights_status_and_risk_note_before_evidence_capture"
            ),
        }
    )
    return output


def _download_log_row(row: dict[str, str], index: int) -> dict[str, str]:
    output = _base(row, index, "download_log")
    output.update(
        {
            "source_route_path": SOURCE_DOWNLOAD_LOG_PATH,
            "source_record_refs": row["download_ids_required"],
            "capturable_field_names": ";".join(
                [
                    "download_ids_required",
                    "download_log_match_count",
                    "download_total_file_size_bytes",
                    "download_checksum_present_count",
                    "download_statuses",
                    "download_log_review_status",
                ]
            ),
            "captured_metadata_summary": _summary(
                {
                    "route_result_id": row["route_result_id"],
                    "download_ids_required": row["download_ids_required"],
                    "download_log_match_count": row["download_log_match_count"],
                    "download_total_file_size_bytes": row[
                        "download_total_file_size_bytes"
                    ],
                    "download_checksum_present_count": row[
                        "download_checksum_present_count"
                    ],
                    "download_statuses": row["download_statuses"],
                    "download_log_review_status": row["download_log_review_status"],
                }
            ),
            "required_review_actions": (
                "open_download_log;verify_download_ids_size_checksum_and_status;"
                "do_not_infer_rights_or_identity_from_download_availability"
            ),
        }
    )
    return output


def build_capture_rows(route_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    builders = {
        "candidate_packet": _candidate_packet_row,
        "source_register": _source_register_row,
        "download_log": _download_log_row,
    }
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
        "sections=candidate_packet;source_register;download_log "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
