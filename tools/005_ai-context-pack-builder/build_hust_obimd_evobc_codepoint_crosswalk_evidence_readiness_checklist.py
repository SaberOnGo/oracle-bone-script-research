#!/usr/bin/env python3
"""Build metadata-only evidence readiness rows for codepoint crosswalk candidates."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


CANDIDATE_PACKET_CAPTURE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "047_ai-agent-hust-obimd-evobc-codepoint-crosswalk-candidate-packet-capture-results.csv"
)
SOURCE_REGISTER_CAPTURE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "045_ai-agent-hust-obimd-evobc-codepoint-crosswalk-source-register-capture-results.csv"
)
DOWNLOAD_LOG_CAPTURE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "046_ai-agent-hust-obimd-evobc-codepoint-crosswalk-download-log-capture-results.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "048_ai-agent-hust-obimd-evobc-codepoint-crosswalk-evidence-readiness-checklist.csv"
)
UPDATED_AT = "2026-06-10"
SOURCE_ORDER = ["src-hust-obc", "src-obimd", "src-evobc"]
DOWNLOAD_ORDER = [
    "dl-hust-obc-validation-label",
    "dl-hust-obc-ocr-id-to-chinese",
    "dl-obimd-main-character-json",
    "dl-evobc-key-value-json",
    "dl-evobc-list-json",
]
RESEARCH_BOUNDARY = "codepoint_crosswalk_evidence_readiness_checklist_not_scholarship"
OVERALL_READINESS_STATUS = "ready_for_human_evidence_pack_review_metadata_only"
CHECKLIST_STATUS = "ready_for_human_review"
CAUTION = (
    "This row is a metadata-readiness checklist for later human evidence-pack review. "
    "It only confirms that 045 source-register metadata, 046 download-log metadata, "
    "and 047 candidate-packet metadata have been captured for the route; it is not "
    "source evidence by itself, not an oracle-character identity decision, not an "
    "accepted reading, not a component assignment, not an evolution-chain assignment, "
    "not a rights decision, not a source promotion, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "readiness_check_id",
    "route_result_id",
    "review_log_draft_id",
    "codepoint_review_task_id",
    "crosswalk_candidate_id",
    "suggested_oracle_character_id",
    "candidate_packet_capture_result_id",
    "source_register_capture_result_ids",
    "download_log_capture_result_ids",
    "candidate_packet_id",
    "source_ids_captured",
    "download_ids_captured",
    "route_cross_source_refs",
    "candidate_packet_capture_count",
    "source_register_capture_count",
    "download_log_capture_count",
    "captured_section_count",
    "required_section_count",
    "candidate_packet_evidence_status",
    "source_register_evidence_statuses",
    "download_log_evidence_statuses",
    "candidate_packet_capture_status",
    "source_register_capture_statuses",
    "download_log_capture_statuses",
    "candidate_packet_ready_status",
    "source_register_ready_status",
    "download_log_ready_status",
    "overall_readiness_status",
    "missing_required_sections",
    "blocking_issue_count",
    "source_register_rights_statuses",
    "download_log_access_statuses",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
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


def _compact(values: list[str]) -> str:
    return ";".join(value for value in values if value)


def _ordered_rows(rows: list[dict[str, str]], field: str, order: list[str]) -> list[dict[str, str]]:
    order_index = {value: index for index, value in enumerate(order)}
    return sorted(rows, key=lambda row: order_index.get(row.get(field, ""), len(order)))


def _group_by_route(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["route_result_id"]].append(row)
    return grouped


def _status_counts(rows: list[dict[str, str]], field: str) -> str:
    counts: dict[str, int] = {}
    for row in rows:
        value = row.get(field, "")
        counts[value] = counts.get(value, 0) + 1
    return ";".join(f"{value}={count}" for value, count in counts.items())


def _rights_statuses(source_rows: list[dict[str, str]]) -> str:
    return _compact(
        [
            f"{row['source_id']}={row['rights_status_evidence_value']}"
            for row in source_rows
        ]
    )


def _download_access_statuses(download_rows: list[dict[str, str]]) -> str:
    return _compact(
        [
            f"{row['download_id']}={row['status_evidence_value']}:{row['http_status_evidence_value']}"
            for row in download_rows
        ]
    )


def _captured_section_count(
    candidate_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    download_rows: list[dict[str, str]],
) -> int:
    return sum(
        [
            len(candidate_rows) == 1,
            len(source_rows) == len(SOURCE_ORDER),
            len(download_rows) == len(DOWNLOAD_ORDER),
        ]
    )


def _missing_sections(
    candidate_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    download_rows: list[dict[str, str]],
) -> str:
    missing = []
    if len(candidate_rows) != 1:
        missing.append("candidate_packet")
    if len(source_rows) != len(SOURCE_ORDER):
        missing.append("source_register")
    if len(download_rows) != len(DOWNLOAD_ORDER):
        missing.append("download_log")
    return "none" if not missing else _compact(missing)


def _build_row(
    index: int,
    candidate_row: dict[str, str],
    source_rows: list[dict[str, str]],
    download_rows: list[dict[str, str]],
) -> dict[str, str]:
    captured_sections = _captured_section_count([candidate_row], source_rows, download_rows)
    missing_sections = _missing_sections([candidate_row], source_rows, download_rows)
    return {
        "readiness_check_id": f"codepoint-evidence-readiness-{index:03d}",
        "route_result_id": candidate_row["route_result_id"],
        "review_log_draft_id": candidate_row["review_log_draft_id"],
        "codepoint_review_task_id": candidate_row["codepoint_review_task_id"],
        "crosswalk_candidate_id": candidate_row["crosswalk_candidate_id"],
        "suggested_oracle_character_id": candidate_row["suggested_oracle_character_id"],
        "candidate_packet_capture_result_id": candidate_row["capture_result_id"],
        "source_register_capture_result_ids": _compact(
            [row["capture_result_id"] for row in source_rows]
        ),
        "download_log_capture_result_ids": _compact(
            [row["capture_result_id"] for row in download_rows]
        ),
        "candidate_packet_id": candidate_row["candidate_packet_id_evidence_value"],
        "source_ids_captured": _compact([row["source_id"] for row in source_rows]),
        "download_ids_captured": _compact([row["download_id"] for row in download_rows]),
        "route_cross_source_refs": candidate_row["route_cross_source_refs_evidence_value"],
        "candidate_packet_capture_count": "1",
        "source_register_capture_count": str(len(source_rows)),
        "download_log_capture_count": str(len(download_rows)),
        "captured_section_count": str(captured_sections),
        "required_section_count": "3",
        "candidate_packet_evidence_status": candidate_row["candidate_packet_evidence_status"],
        "source_register_evidence_statuses": _status_counts(
            source_rows, "source_register_evidence_status"
        ),
        "download_log_evidence_statuses": _status_counts(
            download_rows, "download_log_evidence_status"
        ),
        "candidate_packet_capture_status": candidate_row["capture_status"],
        "source_register_capture_statuses": _status_counts(source_rows, "capture_status"),
        "download_log_capture_statuses": _status_counts(download_rows, "capture_status"),
        "candidate_packet_ready_status": "ready_metadata_only",
        "source_register_ready_status": "ready_metadata_only",
        "download_log_ready_status": "ready_metadata_only",
        "overall_readiness_status": OVERALL_READINESS_STATUS,
        "missing_required_sections": missing_sections,
        "blocking_issue_count": "0" if missing_sections == "none" else "1",
        "source_register_rights_statuses": _rights_statuses(source_rows),
        "download_log_access_statuses": _download_access_statuses(download_rows),
        "rights_decision_status": "no_new_rights_decision",
        "source_promotion_status": "not_promoted",
        "identity_claim_status": "no_identity_claim",
        "decipherment_claim_status": "no_claim",
        "component_claim_status": "no_claim",
        "evolution_chain_claim_status": "no_claim",
        "research_boundary": RESEARCH_BOUNDARY,
        "checklist_status": CHECKLIST_STATUS,
        "evidence_pack_action": "open_review_log_draft_then_attach_metadata_captures",
        "required_next_checks": (
            "open_review_log_draft;verify_candidate_packet_source_register_download_log_rows;"
            "compare_against_xiaoxuetang_obm_and_primary_inscription_context_before_any_identity_or_decipherment_claim"
        ),
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_readiness_rows(
    candidate_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    download_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_by_route = _group_by_route(source_rows)
    download_by_route = _group_by_route(download_rows)
    rows: list[dict[str, str]] = []
    for candidate_row in sorted(candidate_rows, key=lambda row: row["route_result_id"]):
        route_id = candidate_row["route_result_id"]
        route_source_rows = _ordered_rows(source_by_route.get(route_id, []), "source_id", SOURCE_ORDER)
        route_download_rows = _ordered_rows(
            download_by_route.get(route_id, []), "download_id", DOWNLOAD_ORDER
        )
        rows.append(_build_row(len(rows) + 1, candidate_row, route_source_rows, route_download_rows))
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
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_readiness_rows(
        read_csv_rows(root / args.candidate_packet_capture_results),
        read_csv_rows(root / args.source_register_capture_results),
        read_csv_rows(root / args.download_log_capture_results),
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
