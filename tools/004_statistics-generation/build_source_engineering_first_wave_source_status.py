#!/usr/bin/env python3
"""Build source-level status rollup for first-wave source engineering.

This aggregates the metadata-only 119 review results and 121 follow-up queue
by source. It is a preprocessing status surface only: it does not download
new material, decide rights, promote sources, import corpus rows, or make
identity, component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
FIRST_WAVE_REVIEW_RESULTS = STAT_DIR / "119_ai-agent-source-engineering-first-wave-review-results.csv"
FIRST_WAVE_FOLLOWUP_QUEUE = STAT_DIR / "121_ai-agent-source-engineering-first-wave-followup-queue.csv"
DEFAULT_OUTPUT = STAT_DIR / "122_ai-agent-source-engineering-first-wave-source-status.csv"

UPDATED_AT = "2026-06-19"
FOLLOWUP_STATUS = "pending_human_review"
AUTOMATION_BOUNDARY = "human_gated_metadata_only_followup"
RESEARCH_BOUNDARY = "source_engineering_first_wave_source_status_metadata-only_not_scholarship"
CAUTION = (
    "First-wave source status rollup only; this is metadata-only, not a new "
    "download, not a checksum recalculation, not a rights decision, not source "
    "promotion, not a corpus import, not an identity claim, not a component "
    "assignment, not an evolution-chain assignment, and not a decipherment "
    "conclusion."
)

OUTPUT_FIELDS = [
    "source_status_id",
    "source_id",
    "first_wave_result_ids",
    "first_wave_result_count",
    "followup_task_ids",
    "followup_task_count",
    "action_lanes",
    "followup_action_types",
    "decision_values",
    "result_record_paths",
    "reviewed_evidence_paths",
    "pipeline_current_stages",
    "source_first_wave_status",
    "remaining_blockers",
    "next_recommended_action",
    "download_log_ids",
    "download_log_status_counts",
    "download_log_http_status_counts",
    "download_log_checksum_present_count_total",
    "metadata_profile_ids",
    "metadata_profile_metric_count_total",
    "package_manifest_row_count_total",
    "field_map_scaffold_ids",
    "rights_statuses",
    "followup_status",
    "automation_boundary",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "identity_claim_status",
    "component_claim_status",
    "evolution_claim_status",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def split_values(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def join_unique(values: list[str]) -> str:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        for part in split_values(value):
            if part not in seen:
                output.append(part)
                seen.add(part)
    return ";".join(output)


def int_value(value: str) -> int:
    return int(value) if value.isdigit() else 0


def merge_count_strings(values: list[str]) -> str:
    counter: Counter[str] = Counter()
    for value in values:
        for part in split_values(value):
            if ":" not in part:
                continue
            key, raw_count = part.rsplit(":", 1)
            counter[key] = max(counter[key], int_value(raw_count))
    return ";".join(f"{key}:{counter[key]}" for key in sorted(counter))


def first_non_empty_status(values: list[str], fallback: str) -> str:
    return join_unique(values) or fallback


def field_map_scaffold_ids(rows: list[dict[str, str]]) -> str:
    values: list[str] = []
    for row in rows:
        values.append(row.get("field_map_scaffold_ids", ""))
        values.append(row.get("field_map_scaffold_id", ""))
    return join_unique(values)


def classify_source(action_types: set[str]) -> tuple[str, str, str]:
    if {"manual_access_boundary_review", "checksum_absence_boundary_review"} <= action_types:
        return (
            "access_blocked_metadata_only_boundary_pending_human_decision",
            "manual_access_boundary_review_required;checksum_absence_review_required;no_source_content_import",
            "resolve_access_boundary_before_download_or_content_import",
        )
    if {"metadata_profile_extraction_plan_review", "package_manifest_decision_review"} <= action_types:
        return (
            "downloaded_graph_derivative_metadata_profile_and_manifest_decisions_pending",
            "metadata_profile_metrics_not_extracted;package_manifest_decision_pending;linked_assets_rights_not_reviewed",
            "define_metadata_profile_and_manifest_decision_before_import",
        )
    if "field_map_semantics_review" in action_types:
        return (
            "metadata_profile_available_field_map_semantics_pending",
            "field_map_semantics_not_reviewed;rights_boundary_per_field_pending",
            "review_field_map_semantics_against_metadata_profile_before_import",
        )
    if "safe_derived_record_decision_review" in action_types:
        return (
            "metadata_profiles_available_safe_derived_decision_pending",
            "safe_derived_record_decision_pending;source_marked_review_required_before_promotion",
            "decide_safe_derived_record_staging_or_review_queue",
        )
    return (
        "first_wave_metadata_captured_followup_pending",
        "human_followup_review_pending",
        "open_first_wave_result_records_before_any_source_promotion",
    )


def build_source_status_rows(
    review_rows: list[dict[str, str]], followup_rows: list[dict[str, str]]
) -> list[dict[str, str]]:
    followups_by_result = {row["first_wave_result_id"]: row for row in followup_rows}
    source_order = list(dict.fromkeys(row["source_id"] for row in review_rows))

    output_rows: list[dict[str, str]] = []
    for index, source_id in enumerate(source_order, start=1):
        source_review_rows = [row for row in review_rows if row["source_id"] == source_id]
        source_followups = [
            followups_by_result[row["first_wave_result_id"]]
            for row in source_review_rows
            if row["first_wave_result_id"] in followups_by_result
        ]
        action_types = {row["followup_action_type"] for row in source_followups}
        status, blockers, next_action = classify_source(action_types)
        output_rows.append(
            {
                "source_status_id": f"source-engineering-first-wave-source-status-{index:04d}",
                "source_id": source_id,
                "first_wave_result_ids": join_unique([row["first_wave_result_id"] for row in source_review_rows]),
                "first_wave_result_count": str(len(source_review_rows)),
                "followup_task_ids": join_unique([row["followup_task_id"] for row in source_followups]),
                "followup_task_count": str(len(source_followups)),
                "action_lanes": join_unique([row["action_lane"] for row in source_review_rows]),
                "followup_action_types": join_unique([row["followup_action_type"] for row in source_followups]),
                "decision_values": join_unique([row["decision_value"] for row in source_review_rows]),
                "result_record_paths": join_unique([row["result_record_path"] for row in source_review_rows]),
                "reviewed_evidence_paths": join_unique(
                    [row["reviewed_evidence_paths"] for row in source_review_rows]
                ),
                "pipeline_current_stages": join_unique([row.get("pipeline_current_stage", "") for row in source_review_rows]),
                "source_first_wave_status": status,
                "remaining_blockers": blockers,
                "next_recommended_action": next_action,
                "download_log_ids": join_unique([row["download_log_ids"] for row in source_review_rows]),
                "download_log_status_counts": merge_count_strings(
                    [row["download_log_status_counts"] for row in source_review_rows]
                ),
                "download_log_http_status_counts": merge_count_strings(
                    [row["download_log_http_status_counts"] for row in source_review_rows]
                ),
                "download_log_checksum_present_count_total": str(
                    max(int_value(row["download_log_checksum_present_count"]) for row in source_review_rows)
                ),
                "metadata_profile_ids": join_unique([row["metadata_profile_ids"] for row in source_review_rows]),
                "metadata_profile_metric_count_total": str(
                    max(int_value(row["metadata_profile_metric_count"]) for row in source_review_rows)
                ),
                "package_manifest_row_count_total": str(
                    max(int_value(row["package_manifest_row_count"]) for row in source_review_rows)
                ),
                "field_map_scaffold_ids": field_map_scaffold_ids(source_review_rows),
                "rights_statuses": join_unique([row.get("rights_status", "") for row in source_review_rows]),
                "followup_status": first_non_empty_status(
                    [row["followup_status"] for row in source_followups], FOLLOWUP_STATUS
                ),
                "automation_boundary": first_non_empty_status(
                    [row["automation_boundary"] for row in source_followups], AUTOMATION_BOUNDARY
                ),
                "rights_decision_status": join_unique([row["rights_decision_status"] for row in source_review_rows]),
                "source_promotion_status": join_unique([row["source_promotion_status"] for row in source_review_rows]),
                "corpus_import_status": join_unique([row["corpus_import_status"] for row in source_review_rows]),
                "decipherment_claim_status": join_unique(
                    [row["decipherment_claim_status"] for row in source_review_rows]
                ),
                "identity_claim_status": join_unique([row["identity_claim_status"] for row in source_review_rows]),
                "component_claim_status": join_unique([row["component_claim_status"] for row in source_review_rows]),
                "evolution_claim_status": join_unique([row["evolution_claim_status"] for row in source_review_rows]),
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return output_rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build first-wave source-engineering source status rollup.")
    parser.add_argument("--results", default=str(FIRST_WAVE_REVIEW_RESULTS))
    parser.add_argument("--followup", default=str(FIRST_WAVE_FOLLOWUP_QUEUE))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_source_status_rows(
        read_csv_rows(root / args.results),
        read_csv_rows(root / args.followup),
    )
    write_csv(root / args.output, rows)
    print(f"source_status_count={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
