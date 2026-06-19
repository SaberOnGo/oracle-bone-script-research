#!/usr/bin/env python3
"""Build next-action checklist rows for source-engineering gaps.

The checklist turns the metadata-only 103 evidence snapshot into explicit
preprocessing actions. It does not perform the actions, download source
material, decide rights, promote sources, import corpus rows, or make
scholarly claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_ENGINEERING_GAP_EVIDENCE_SNAPSHOT = Path(
    "corpus/009_statistics-and-derived-features/103_ai-agent-source-engineering-gap-evidence-snapshot.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/104_ai-agent-source-engineering-next-action-checklist.csv"
)

UPDATED_AT = "2026-06-19"
ACTION_STATUS = "ready_for_source_engineering_review"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
RESEARCH_BOUNDARY = "source_engineering_next_action_checklist_not_scholarship"
CAUTION = (
    "This checklist only schedules source-engineering preprocessing review. It "
    "does not execute downloads, recalculate checksums, clear rights, promote "
    "sources, import corpus records, confirm oracle-character identity, or make "
    "decipherment conclusions."
)

OUTPUT_FIELDS = [
    "next_action_id",
    "evidence_snapshot_id",
    "source_engineering_gap_id",
    "review_log_draft_id",
    "source_id",
    "gap_type",
    "priority_rank",
    "action_lane",
    "automation_scope",
    "human_gate",
    "primary_input_path",
    "secondary_input_paths",
    "review_log_path",
    "expected_result_path",
    "checklist_items",
    "blocking_condition",
    "safe_to_automate_status",
    "action_status",
    "human_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "research_boundary",
    "caution",
    "updated_at",
]


LANE_RULES = {
    "access_boundary_or_error_followup": {
        "action_lane": "access_boundary_followup",
        "automation_scope": "route_metadata_only_manual_access_may_be_needed",
        "human_gate": "manual_browser_or_institutional_export_required_before_any_content_claim",
        "checklist_items": (
            "open_download_log;open_status_codebook;record_access_outcome;"
            "separate_http_tls_access_boundary_from_source_content"
        ),
        "blocking_condition": "no_content_import_until_access_or_metadata_only_boundary_is_reviewed",
        "safe_to_automate_status": "metadata_routing_safe_content_capture_blocked",
    },
    "checksum_or_failed_download_status_review_needed": {
        "action_lane": "checksum_and_download_status_review",
        "automation_scope": "existing_download_log_metadata_only",
        "human_gate": "human_confirms_failed_or_restricted_download_rows_before_package_promotion",
        "checklist_items": (
            "open_download_log;verify_status_and_size_fields;confirm_checksum_absence_or_presence;"
            "record_retry_or_no-retry_decision"
        ),
        "blocking_condition": "no_source_package_or_derivative_promotion_without_reviewed_download_status",
        "safe_to_automate_status": "metadata_audit_safe_checksum_recalculation_blocked",
    },
    "metadata_profile_extraction_needed": {
        "action_lane": "metadata_profile_extraction_planning",
        "automation_scope": "profile_extraction_can_be_scripted_from_reviewed_local_or_registered_rows",
        "human_gate": "human_reviews_profile_scope_before_using_raw_or_access_restricted_content",
        "checklist_items": (
            "open_source_register;open_download_log;open_existing_metadata_profiles;"
            "define_profile_metrics;record_extraction_boundary"
        ),
        "blocking_condition": "no_profile_from_raw_or_restricted_material_until_source_route_is_reviewed",
        "safe_to_automate_status": "scriptable_after_route_review",
    },
    "source_field_map_needed": {
        "action_lane": "source_field_map_planning",
        "automation_scope": "field_map_schema_design_only",
        "human_gate": "human_confirms_target_record_type_and_source_field_meaning",
        "checklist_items": (
            "open_source_register;open_existing_field_map;identify_target_record_type;"
            "draft_field_mapping;mark_unknown_fields_pending_review"
        ),
        "blocking_condition": "no_import_until_field_semantics_are_reviewed",
        "safe_to_automate_status": "schema_scaffold_safe_semantic_mapping_requires_review",
    },
    "package_file_manifest_or_not_applicable_decision_needed": {
        "action_lane": "package_manifest_or_not_applicable_review",
        "automation_scope": "manifest_gap_review_only",
        "human_gate": "human_decides_package_manifest_needed_not_applicable_or_local_only",
        "checklist_items": (
            "open_large_source_register;open_package_manifest;open_download_manifest;"
            "record_manifest_needed_or_not_applicable;keep_raw_package_outside_regular_git"
        ),
        "blocking_condition": "no_raw_package_commit_without_manifest_or_explicit_not_applicable_decision",
        "safe_to_automate_status": "metadata_review_safe_manifest_decision_requires_human",
    },
    "safe_derived_record_decision_needed": {
        "action_lane": "safe_derived_record_decision",
        "automation_scope": "derived_record_route_planning_only",
        "human_gate": "human_confirms_safe_derivative_kind_rights_and_source_trail_before_promotion",
        "checklist_items": (
            "open_pipeline_audit;open_coverage_summary;open_source_register;"
            "identify_candidate_derived_record;record_rights_risk_and_review_status"
        ),
        "blocking_condition": "no_derived_record_promotion_without_source_marked_reviewed_boundary",
        "safe_to_automate_status": "planning_safe_derivative_promotion_blocked",
    },
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_paths(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def expected_result_path(row: dict[str, str]) -> str:
    safe_gap_id = row["source_engineering_gap_id"].replace("source-engineering-gap-", "")
    return (
        "doc/public/user_research/009_source-engineering-gap-review-queues/"
        f"{safe_gap_id}_{row['source_id']}_{row['gap_type']}_next-action-result.md"
    )


def build_checklist_rows(root: Path) -> list[dict[str, str]]:
    snapshot_rows = read_csv_rows(root / SOURCE_ENGINEERING_GAP_EVIDENCE_SNAPSHOT)
    output_rows: list[dict[str, str]] = []
    for index, row in enumerate(snapshot_rows, start=1):
        rule = LANE_RULES[row["gap_type"]]
        route_files = split_paths(row["route_files_to_open"])
        output_rows.append(
            {
                "next_action_id": f"source-engineering-next-action-{index:04d}",
                "evidence_snapshot_id": row["evidence_snapshot_id"],
                "source_engineering_gap_id": row["source_engineering_gap_id"],
                "review_log_draft_id": row["review_log_draft_id"],
                "source_id": row["source_id"],
                "gap_type": row["gap_type"],
                "priority_rank": row["priority_rank"],
                "action_lane": rule["action_lane"],
                "automation_scope": rule["automation_scope"],
                "human_gate": rule["human_gate"],
                "primary_input_path": SOURCE_ENGINEERING_GAP_EVIDENCE_SNAPSHOT.as_posix(),
                "secondary_input_paths": ";".join(route_files),
                "review_log_path": row["draft_path"],
                "expected_result_path": expected_result_path(row),
                "checklist_items": rule["checklist_items"],
                "blocking_condition": rule["blocking_condition"],
                "safe_to_automate_status": rule["safe_to_automate_status"],
                "action_status": ACTION_STATUS,
                "human_review_status": HUMAN_REVIEW_STATUS,
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "corpus_import_status": CORPUS_IMPORT_STATUS,
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return output_rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source-engineering next-action checklist.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_checklist_rows(root)
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
