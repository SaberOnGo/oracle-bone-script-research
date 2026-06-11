#!/usr/bin/env python3
"""Build metadata-only Xiaoxuetang JGW follow-up capture results."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


CAPTURE_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "080_ai-agent-xiaoxuetang-followup-jgw-capture-scaffold.csv"
)
NOTE_UPDATE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "070_ai-agent-hust-obc-undeciphered-candidate-source-image-reference-note-update-results.csv"
)
ROUTE_PROBE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "071_ai-agent-hust-obc-undeciphered-candidate-xxt-jgw-route-probe-results.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "082_ai-agent-xiaoxuetang-followup-jgw-capture-results.csv"
)
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "xxt_followup_jgw_capture_results_not_scholarship"
OUTPUT_SCOPE = "xiaoxuetang_followup_jgw_capture_results_only"
CAUTION = (
    "This row records only what the current Xiaoxuetang JGW route evidence proves: "
    "a TLS/access-boundary failure, filename-token-derived route targeting, and the "
    "current absence of catalog, Heji, collection, and full inscription-context evidence. "
    "It is not catalog confirmation, not a Heji crosswalk, not a collection match, not "
    "a formal assignment, and not a decipherment conclusion."
)

FIELDNAMES = [
    "capture_result_id",
    "capture_row_id",
    "followup_task_id",
    "route_probe_result_id",
    "note_update_result_id",
    "source_image_reference_extraction_summary_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "targeted_download_id",
    "targeted_url",
    "official_access_boundary_status",
    "source_register_row_check_status",
    "download_manifest_row_check_status",
    "download_log_row_check_status",
    "full_inscription_context_note_check_status",
    "route_probe_result_check_status",
    "manual_followup_route_status",
    "catalog_availability_status",
    "catalog_availability_evidence_value",
    "heji_crosswalk_availability_status",
    "heji_crosswalk_evidence_value",
    "collection_match_availability_status",
    "collection_match_evidence_value",
    "inscription_context_availability_status",
    "inscription_context_evidence_value",
    "capture_status",
    "human_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "assignment_scope_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
    "route_files_to_open",
    "required_review_sections",
    "required_next_checks",
    "research_boundary",
    "output_scope",
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


def _by_id(rows: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        key = row[field]
        if key in result:
            raise ValueError(f"duplicate {field}: {key}")
        result[key] = row
    return result


def _require_match(left: dict[str, str], right: dict[str, str], fields: list[str]) -> None:
    for field in fields:
        if left[field] != right[field]:
            raise ValueError(f"field mismatch for {field}: {left[field]} != {right[field]}")


def _build_row(
    index: int,
    capture: dict[str, str],
    note_update: dict[str, str],
    route_probe: dict[str, str],
) -> dict[str, str]:
    _require_match(
        capture,
        note_update,
        ["unknown_candidate_id", "primary_external_ref_id"],
    )
    _require_match(
        capture,
        route_probe,
        [
            "unknown_candidate_id",
            "primary_external_ref_id",
            "targeted_download_id",
            "targeted_url",
        ],
    )

    return {
        "capture_result_id": f"xxt-jgw-followup-capture-result-{index:03d}",
        "capture_row_id": capture["capture_row_id"],
        "followup_task_id": capture["followup_task_id"],
        "route_probe_result_id": route_probe["route_probe_result_id"],
        "note_update_result_id": note_update["note_update_result_id"],
        "source_image_reference_extraction_summary_id": note_update[
            "source_image_reference_extraction_summary_id"
        ],
        "unknown_candidate_id": capture["unknown_candidate_id"],
        "primary_external_ref_id": capture["primary_external_ref_id"],
        "targeted_download_id": capture["targeted_download_id"],
        "targeted_url": capture["targeted_url"],
        "official_access_boundary_status": route_probe["official_access_boundary_status"],
        "source_register_row_check_status": "registered_route_file_listed_not_reopened",
        "download_manifest_row_check_status": "registered_route_file_listed_not_reopened",
        "download_log_row_check_status": "registered_route_file_listed_not_reopened",
        "full_inscription_context_note_check_status": "reviewed_note_update_result_row",
        "route_probe_result_check_status": "reviewed_route_probe_result_row",
        "manual_followup_route_status": "manual_browser_or_institutional_export_required_after_tls_access_boundary",
        "catalog_availability_status": "not_available_from_current_route_evidence",
        "catalog_availability_evidence_value": note_update["catalog_context_status"],
        "heji_crosswalk_availability_status": "not_available_from_current_route_evidence",
        "heji_crosswalk_evidence_value": route_probe["heji_crosswalk_status"],
        "collection_match_availability_status": "not_available_from_current_route_evidence",
        "collection_match_evidence_value": route_probe["collection_context_status"],
        "inscription_context_availability_status": "not_available_from_current_route_evidence",
        "inscription_context_evidence_value": note_update[
            "inscription_context_evidence_status"
        ],
        "capture_status": "reviewed_metadata_only_current_route_boundary_recorded",
        "human_review_status": "reviewed_metadata_only",
        "rights_decision_status": "no_new_rights_decision",
        "source_promotion_status": "not_promoted",
        "identity_claim_status": "no_identity_claim",
        "assignment_scope_status": capture["assignment_scope_status"],
        "decipherment_claim_status": "no_claim",
        "component_claim_status": "no_claim",
        "evolution_chain_claim_status": "no_claim",
        "route_files_to_open": capture["route_files_to_open"],
        "required_review_sections": capture["required_review_sections"],
        "required_next_checks": (
            "open_082_capture_result;use_manual_browser_or_institutional_export_before_any_catalog_claim;"
            "keep_filename_tokens_as_search_hints_only;do_not_write_identity_or_decipherment_claim"
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "output_scope": OUTPUT_SCOPE,
        "rights_status": capture["rights_status"],
        "risk_note": capture["risk_note"],
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_capture_results(
    capture_rows: list[dict[str, str]],
    note_update_rows: list[dict[str, str]],
    route_probe_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    note_update_by_candidate = _by_id(note_update_rows, "unknown_candidate_id")
    route_probe_by_candidate = _by_id(route_probe_rows, "unknown_candidate_id")

    rows: list[dict[str, str]] = []
    for capture in sorted(capture_rows, key=lambda row: row["capture_row_id"]):
        candidate_id = capture["unknown_candidate_id"]
        rows.append(
            _build_row(
                len(rows) + 1,
                capture,
                note_update_by_candidate[candidate_id],
                route_probe_by_candidate[candidate_id],
            )
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture-scaffold", default=str(CAPTURE_SCAFFOLD))
    parser.add_argument("--note-update-results", default=str(NOTE_UPDATE_RESULTS))
    parser.add_argument("--route-probe-results", default=str(ROUTE_PROBE_RESULTS))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_capture_results(
        read_csv_rows(root / args.capture_scaffold),
        read_csv_rows(root / args.note_update_results),
        read_csv_rows(root / args.route_probe_results),
    )
    write_csv(root / args.output, rows)
    print(
        f"capture_result_count={len(rows)} "
        f"candidate_count={len({row['unknown_candidate_id'] for row in rows})} "
        "capture_status=reviewed_metadata_only_current_route_boundary_recorded"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
