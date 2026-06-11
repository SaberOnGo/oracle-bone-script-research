#!/usr/bin/env python3
"""Build metadata-only evidence readiness rows for HUST-OBC undeciphered candidates."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


CANDIDATE_PACKET_CAPTURE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "059_ai-agent-hust-obc-undeciphered-candidate-packet-capture-results.csv"
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
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "060_ai-agent-hust-obc-undeciphered-candidate-evidence-readiness-checklist.csv"
)
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_candidate_evidence_readiness_checklist_not_scholarship"
OVERALL_READINESS_STATUS = "ready_for_human_evidence_pack_review_metadata_only"
CHECKLIST_STATUS = "ready_for_human_review"
CAUTION = (
    "This row is a metadata-readiness checklist for later human evidence-pack review. "
    "It only confirms that 056 source-register metadata, 057 download-log metadata, "
    "058 large-source-register metadata, and 059 candidate-packet metadata have been "
    "captured for the HUST-OBC undeciphered-candidate route; it is not source evidence "
    "by itself, not an accepted oracle-character identity, not a formal obs-char "
    "assignment, not an accepted reading, not a component assignment, not an "
    "evolution-chain assignment, not a rights decision, not a source promotion, and "
    "not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "readiness_check_id",
    "route_result_id",
    "review_log_draft_id",
    "undeciphered_review_task_id",
    "context_pack_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "candidate_packet_capture_result_id",
    "source_register_capture_result_id",
    "download_log_capture_result_id",
    "large_source_register_capture_result_id",
    "candidate_packet_path",
    "bucket_manifest_path",
    "source_id_captured",
    "source_package_id_captured",
    "download_id_captured",
    "source_class_path_captured",
    "source_image_count_captured",
    "source_reported_undeciphered_class_count",
    "zip_observed_undeciphered_class_count",
    "zip_observed_undeciphered_image_count",
    "candidate_packet_capture_count",
    "source_register_capture_count",
    "download_log_capture_count",
    "large_source_register_capture_count",
    "captured_section_count",
    "required_section_count",
    "candidate_packet_evidence_status",
    "source_register_evidence_status",
    "download_log_evidence_status",
    "large_source_register_evidence_status",
    "candidate_packet_capture_status",
    "source_register_capture_status",
    "download_log_capture_status",
    "large_source_register_capture_status",
    "candidate_packet_ready_status",
    "source_register_ready_status",
    "download_log_ready_status",
    "large_source_register_ready_status",
    "overall_readiness_status",
    "missing_required_sections",
    "blocking_issue_count",
    "rights_statuses_captured",
    "download_access_status",
    "large_source_storage_status",
    "large_source_file_size_bytes",
    "large_source_checksum_sha256_present",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "assignment_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
    "research_boundary",
    "checklist_status",
    "evidence_pack_action",
    "required_next_checks",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _group_by_route(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["route_result_id"]].append(row)
    return grouped


def _one(rows_by_route: dict[str, list[dict[str, str]]], route_id: str, section: str) -> dict[str, str] | None:
    rows = rows_by_route.get(route_id, [])
    if len(rows) > 1:
        raise ValueError(f"multiple {section} rows for {route_id}")
    return rows[0] if rows else None


def _present(row: dict[str, str] | None) -> bool:
    return row is not None


def _status(row: dict[str, str] | None, field: str) -> str:
    return row[field] if row else "missing"


def _missing_sections(
    candidate_row: dict[str, str] | None,
    source_row: dict[str, str] | None,
    download_row: dict[str, str] | None,
    large_source_row: dict[str, str] | None,
) -> str:
    missing = []
    if candidate_row is None:
        missing.append("candidate_packet")
    if source_row is None:
        missing.append("source_register")
    if download_row is None:
        missing.append("download_log")
    if large_source_row is None:
        missing.append("large_source_register")
    return "none" if not missing else ";".join(missing)


def _rights_statuses(
    candidate_row: dict[str, str],
    source_row: dict[str, str] | None,
    large_source_row: dict[str, str] | None,
) -> str:
    values = [
        f"candidate_packet={candidate_row['rights_status_evidence_value']}",
    ]
    if source_row is not None:
        values.append(f"source_register={source_row['rights_status_evidence_value']}")
    if large_source_row is not None:
        values.append(f"large_source_register={large_source_row['rights_status_evidence_value']}")
    return ";".join(values)


def _checksum_present(row: dict[str, str] | None) -> str:
    if row is None:
        return "false"
    return str(bool(row["checksum_sha256_evidence_value"])).lower()


def _build_row(
    index: int,
    candidate_row: dict[str, str],
    source_row: dict[str, str] | None,
    download_row: dict[str, str] | None,
    large_source_row: dict[str, str] | None,
) -> dict[str, str]:
    missing_sections = _missing_sections(candidate_row, source_row, download_row, large_source_row)
    captured_section_count = sum(
        [
            _present(candidate_row),
            _present(source_row),
            _present(download_row),
            _present(large_source_row),
        ]
    )
    return {
        "readiness_check_id": f"hust-obc-undeciphered-evidence-readiness-{index:04d}",
        "route_result_id": candidate_row["route_result_id"],
        "review_log_draft_id": candidate_row["review_log_draft_id"],
        "undeciphered_review_task_id": candidate_row["undeciphered_review_task_id"],
        "context_pack_id": candidate_row["context_pack_id"],
        "unknown_candidate_id": candidate_row["unknown_candidate_id"],
        "primary_external_ref_id": candidate_row["primary_external_ref_id"],
        "candidate_packet_capture_result_id": candidate_row["capture_result_id"],
        "source_register_capture_result_id": source_row["capture_result_id"] if source_row else "",
        "download_log_capture_result_id": download_row["capture_result_id"] if download_row else "",
        "large_source_register_capture_result_id": large_source_row["capture_result_id"] if large_source_row else "",
        "candidate_packet_path": candidate_row["candidate_packet_path"],
        "bucket_manifest_path": candidate_row["bucket_manifest_path"],
        "source_id_captured": candidate_row["source_id_evidence_value"],
        "source_package_id_captured": candidate_row["source_package_id_evidence_value"],
        "download_id_captured": candidate_row["evidence_download_id_evidence_value"],
        "source_class_path_captured": candidate_row["source_class_path_evidence_value"],
        "source_image_count_captured": candidate_row["source_image_count_evidence_value"],
        "source_reported_undeciphered_class_count": candidate_row[
            "source_reported_undeciphered_class_count_evidence_value"
        ],
        "zip_observed_undeciphered_class_count": candidate_row[
            "zip_observed_undeciphered_class_count_evidence_value"
        ],
        "zip_observed_undeciphered_image_count": candidate_row[
            "zip_observed_undeciphered_image_count_evidence_value"
        ],
        "candidate_packet_capture_count": "1",
        "source_register_capture_count": "1" if source_row else "0",
        "download_log_capture_count": "1" if download_row else "0",
        "large_source_register_capture_count": "1" if large_source_row else "0",
        "captured_section_count": str(captured_section_count),
        "required_section_count": "4",
        "candidate_packet_evidence_status": candidate_row["candidate_packet_evidence_status"],
        "source_register_evidence_status": _status(source_row, "source_register_evidence_status"),
        "download_log_evidence_status": _status(download_row, "download_log_evidence_status"),
        "large_source_register_evidence_status": _status(large_source_row, "large_source_evidence_status"),
        "candidate_packet_capture_status": candidate_row["capture_status"],
        "source_register_capture_status": _status(source_row, "capture_status"),
        "download_log_capture_status": _status(download_row, "capture_status"),
        "large_source_register_capture_status": _status(large_source_row, "capture_status"),
        "candidate_packet_ready_status": "ready_metadata_only",
        "source_register_ready_status": "ready_metadata_only" if source_row else "missing",
        "download_log_ready_status": "ready_metadata_only" if download_row else "missing",
        "large_source_register_ready_status": "ready_metadata_only" if large_source_row else "missing",
        "overall_readiness_status": (
            OVERALL_READINESS_STATUS if missing_sections == "none" else "blocked_missing_metadata_capture"
        ),
        "missing_required_sections": missing_sections,
        "blocking_issue_count": "0" if missing_sections == "none" else "1",
        "rights_statuses_captured": _rights_statuses(candidate_row, source_row, large_source_row),
        "download_access_status": (
            f"{download_row['download_id']}={download_row['status_evidence_value']}:"
            f"{download_row['http_status_evidence_value']}"
            if download_row
            else "missing"
        ),
        "large_source_storage_status": _status(large_source_row, "storage_status_evidence_value"),
        "large_source_file_size_bytes": _status(large_source_row, "file_size_bytes_evidence_value"),
        "large_source_checksum_sha256_present": _checksum_present(large_source_row),
        "rights_decision_status": "no_new_rights_decision",
        "source_promotion_status": "not_promoted",
        "identity_claim_status": "no_identity_claim",
        "assignment_status": "unknown_candidate_id_not_formal_obs_char_assignment",
        "decipherment_claim_status": "no_claim",
        "component_claim_status": "no_claim",
        "evolution_chain_claim_status": "no_claim",
        "research_boundary": RESEARCH_BOUNDARY,
        "checklist_status": CHECKLIST_STATUS if missing_sections == "none" else "needs_missing_metadata_capture",
        "evidence_pack_action": "open_review_log_draft_then_attach_056_057_058_059_metadata_captures",
        "required_next_checks": (
            "open_060_readiness_row;open_review_log_draft;verify_056_057_058_059_capture_rows;"
            "cross_check_against_xiaoxuetang_obm_heji_or_primary_inscription_context_before_any_identity_or_decipherment_claim"
        ),
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_readiness_rows(
    candidate_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    download_rows: list[dict[str, str]],
    large_source_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_by_route = _group_by_route(source_rows)
    download_by_route = _group_by_route(download_rows)
    large_source_by_route = _group_by_route(large_source_rows)
    rows: list[dict[str, str]] = []
    for candidate_row in sorted(candidate_rows, key=lambda row: row["route_result_id"]):
        route_id = candidate_row["route_result_id"]
        rows.append(
            _build_row(
                len(rows) + 1,
                candidate_row,
                _one(source_by_route, route_id, "source-register"),
                _one(download_by_route, route_id, "download-log"),
                _one(large_source_by_route, route_id, "large-source-register"),
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
    parser.add_argument("--candidate-packet-capture-results", default=str(CANDIDATE_PACKET_CAPTURE_RESULTS))
    parser.add_argument("--source-register-capture-results", default=str(SOURCE_REGISTER_CAPTURE_RESULTS))
    parser.add_argument("--download-log-capture-results", default=str(DOWNLOAD_LOG_CAPTURE_RESULTS))
    parser.add_argument("--large-source-register-capture-results", default=str(LARGE_SOURCE_REGISTER_CAPTURE_RESULTS))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_readiness_rows(
        read_csv_rows(root / args.candidate_packet_capture_results),
        read_csv_rows(root / args.source_register_capture_results),
        read_csv_rows(root / args.download_log_capture_results),
        read_csv_rows(root / args.large_source_register_capture_results),
    )
    write_csv(root / args.output, rows)
    print(
        f"readiness_check_count={len(rows)} "
        f"ready_count={sum(row['overall_readiness_status'] == OVERALL_READINESS_STATUS for row in rows)} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
