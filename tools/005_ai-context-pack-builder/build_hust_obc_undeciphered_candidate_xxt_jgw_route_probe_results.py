#!/usr/bin/env python3
"""Build metadata-only Xiaoxuetang JGW route-probe results for HUST-OBC undeciphered candidates."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


NOTE_UPDATE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "070_ai-agent-hust-obc-undeciphered-candidate-source-image-reference-note-update-results.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "071_ai-agent-hust-obc-undeciphered-candidate-xxt-jgw-route-probe-results.csv"
)
UPDATED_AT = "2026-06-11"
TARGET_SOURCE_ID = "src-xiaoxuetang-jiaguwen"
OFFICIAL_ROUTE_KIND = "xiaoxuetang_jgw_character_detail_page"
AUTOMATED_FETCH_CLIENT_MATRIX = "python_urllib_openssl;curl_schannel"
AUTOMATED_FETCH_STATUS = "failed_tls_handshake_no_html_captured"
OFFICIAL_ACCESS_BOUNDARY_STATUS = (
    "direct_official_character_page_not_collected_due_tls_or_access_boundary"
)
TOKEN_ORIGIN_STATUS = "derived_from_hust_filename_search_hint_only"
EVIDENCE_COLLECTION_STATUS = "route_probe_only_no_official_character_html_collected"
HUMAN_REVIEW_STATUS = "not_started"
FORMAL_SCHEMA_COMPATIBILITY_STATUS = "not_formal_obs_char_schema"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
NO_CLAIM = "no_claim"
RESEARCH_BOUNDARY = "hust_obc_xxt_jgw_route_probe_not_scholarship"
REQUIRED_NEXT_CHECKS = (
    "open_070_note_update_result;review_registered_xxt_download_log_rows;"
    "use_manual_browser_or_institutional_export_before_any_catalog_claim"
)
CAUTION = (
    "This result records an official Xiaoxuetang route probe only. The kaiOrder token is "
    "derived from HUST-OBC filename number tokens and remains a search hint, not catalog "
    "confirmation, not a Heji crosswalk, not a collection match, not a formal obs-char "
    "assignment, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "route_probe_result_id",
    "note_update_result_id",
    "source_image_reference_extraction_summary_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "source_id",
    "target_source_id",
    "targeted_download_id",
    "targeted_url",
    "candidate_filename_number_probe_token",
    "token_origin_status",
    "official_route_kind",
    "automated_fetch_client_matrix",
    "automated_fetch_status",
    "official_access_boundary_status",
    "primary_catalog_context_status",
    "heji_crosswalk_status",
    "old_catalog_context_status",
    "collection_context_status",
    "excavation_context_status",
    "transcription_context_status",
    "catalog_context_status",
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
    "required_next_checks",
    "risk_note",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def first_probe_token(value: str) -> str:
    tokens = [item.strip() for item in value.split(";") if item.strip()]
    if not tokens:
        raise ValueError("missing filename catalog candidate number tokens")
    return tokens[0]


def build_download_id(token: str) -> str:
    return f"dl-xxt-jgw-kaiorder-{int(token):04d}"


def build_target_url(token: str) -> str:
    return f"https://xiaoxue.iis.sinica.edu.tw/jiaguwen?kaiOrder={int(token)}"


def build_route_probe_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        token = first_probe_token(row["filename_catalog_candidate_number_tokens"])
        results.append(
            {
                "route_probe_result_id": f"hust-obc-xxt-jgw-route-probe-{index:04d}",
                "note_update_result_id": row["note_update_result_id"],
                "source_image_reference_extraction_summary_id": row[
                    "source_image_reference_extraction_summary_id"
                ],
                "unknown_candidate_id": row["unknown_candidate_id"],
                "primary_external_ref_id": row["primary_external_ref_id"],
                "source_id": row["source_id"],
                "target_source_id": TARGET_SOURCE_ID,
                "targeted_download_id": build_download_id(token),
                "targeted_url": build_target_url(token),
                "candidate_filename_number_probe_token": token,
                "token_origin_status": TOKEN_ORIGIN_STATUS,
                "official_route_kind": OFFICIAL_ROUTE_KIND,
                "automated_fetch_client_matrix": AUTOMATED_FETCH_CLIENT_MATRIX,
                "automated_fetch_status": AUTOMATED_FETCH_STATUS,
                "official_access_boundary_status": OFFICIAL_ACCESS_BOUNDARY_STATUS,
                "primary_catalog_context_status": "not_collected_route_probe_only",
                "heji_crosswalk_status": "not_collected_route_probe_only",
                "old_catalog_context_status": "not_collected_route_probe_only",
                "collection_context_status": "not_collected_route_probe_only",
                "excavation_context_status": "not_collected_route_probe_only",
                "transcription_context_status": "not_collected_route_probe_only",
                "catalog_context_status": "not_collected_route_probe_only",
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
                "required_next_checks": REQUIRED_NEXT_CHECKS,
                "risk_note": (
                    "Official Xiaoxuetang route was targeted from a HUST filename token, but "
                    "local Python urllib/OpenSSL and curl schannel clients both failed before "
                    "HTML capture. Treat as access-boundary evidence only until a manual browser "
                    "or institutional export path is reviewed."
                ),
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return results


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build metadata-only Xiaoxuetang JGW route-probe results for "
            "HUST-OBC undeciphered candidates."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=NOTE_UPDATE_RESULTS,
        help="CSV of 070 note-update results.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output CSV path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = repo_root()
    rows = read_csv_rows(root / args.input)
    output_rows = build_route_probe_rows(rows)
    write_csv(root / args.output, output_rows)


if __name__ == "__main__":
    main()
