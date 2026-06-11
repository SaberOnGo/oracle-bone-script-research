#!/usr/bin/env python3
"""Build metadata-only capture results for Xiaoxuetang OBM access-boundary routes."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


CAPTURE_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "083_ai-agent-xxt-obm-access-boundary-capture-scaffold.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "085_ai-agent-xxt-obm-access-boundary-capture-results.csv"
)
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "xxt_obm_access_boundary_capture_results_not_scholarship"
OUTPUT_SCOPE = "xxt_obm_access_boundary_capture_results_only"
CAUTION = (
    "This row records only what the current Xiaoxuetang OBM access-boundary route evidence proves: "
    "an access-restricted HTML boundary, the current availability or absence of registered access-profile "
    "and staged-abbreviation metadata, and the continued need for manual browser or institutional export follow-up. "
    "It is not a source-table import, not an old-catalog confirmation, not a holding or collection match, "
    "not a formal assignment, and not a decipherment conclusion."
)

FIELDNAMES = [
    "capture_result_id",
    "capture_row_id",
    "review_log_draft_id",
    "followup_task_id",
    "source_id",
    "targeted_download_id",
    "targeted_url",
    "artifact_kind",
    "official_access_boundary_status",
    "route_file_review_status",
    "manual_followup_route_status",
    "access_profile_availability_status",
    "access_profile_evidence_value",
    "staging_availability_status",
    "staging_evidence_value",
    "capture_status",
    "human_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "assignment_status",
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


def _int(value: str) -> int:
    return int(value) if value else 0


def _build_row(index: int, capture: dict[str, str]) -> dict[str, str]:
    profile_match_count = _int(capture["profile_match_count"])
    staging_row_count = _int(capture["staging_row_count"])

    access_profile_status = (
        "available_from_current_route_evidence"
        if profile_match_count > 0
        else "not_available_from_current_route_evidence"
    )
    staging_status = (
        "available_from_current_route_evidence"
        if staging_row_count > 0
        else "not_available_from_current_route_evidence"
    )

    return {
        "capture_result_id": f"xxt-obm-access-capture-result-{index:03d}",
        "capture_row_id": capture["capture_row_id"],
        "review_log_draft_id": capture["review_log_draft_id"],
        "followup_task_id": capture["followup_task_id"],
        "source_id": capture["source_id"],
        "targeted_download_id": capture["targeted_download_id"],
        "targeted_url": capture["targeted_url"],
        "artifact_kind": capture["artifact_kind"],
        "official_access_boundary_status": capture["official_access_boundary_status"],
        "route_file_review_status": capture["route_file_review_status"],
        "manual_followup_route_status": "manual_browser_or_institutional_export_required_after_access_restricted_html",
        "access_profile_availability_status": access_profile_status,
        "access_profile_evidence_value": (
            capture["profile_normalized_values"]
            if profile_match_count > 0
            else "no_profile_rows_linked_from_current_route_evidence"
        ),
        "staging_availability_status": staging_status,
        "staging_evidence_value": (
            capture["staging_row_kind_counts"]
            if staging_row_count > 0
            else "no_staging_rows_linked_from_current_route_evidence"
        ),
        "capture_status": "reviewed_metadata_only_current_access_boundary_recorded",
        "human_review_status": "reviewed_metadata_only",
        "rights_decision_status": "no_new_rights_decision",
        "source_promotion_status": "not_promoted",
        "identity_claim_status": "no_identity_claim",
        "assignment_status": capture["assignment_status"],
        "decipherment_claim_status": "no_claim",
        "component_claim_status": "no_claim",
        "evolution_chain_claim_status": "no_claim",
        "route_files_to_open": capture["route_files_to_open"],
        "required_review_sections": capture["required_review_sections"],
        "required_next_checks": (
            "open_085_capture_result;use_manual_browser_or_institutional_export_before_any_source_table_claim;"
            "keep_access_boundary_and_staging_routes_separate;do_not_write_old_catalog_holding_assignment_or_decipherment_claim"
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "output_scope": OUTPUT_SCOPE,
        "rights_status": capture["rights_status"],
        "risk_note": capture["risk_note"],
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_capture_results(capture_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        _build_row(index, row)
        for index, row in enumerate(sorted(capture_rows, key=lambda item: item["capture_row_id"]), start=1)
    ]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture-scaffold", default=str(CAPTURE_SCAFFOLD))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_capture_results(read_csv_rows(root / args.capture_scaffold))
    write_csv(root / args.output, rows)
    print(
        f"capture_result_count={len(rows)} "
        f"targeted_download_count={len({row['targeted_download_id'] for row in rows})} "
        "capture_status=reviewed_metadata_only_current_access_boundary_recorded"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
