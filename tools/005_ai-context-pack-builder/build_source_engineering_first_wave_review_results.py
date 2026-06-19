#!/usr/bin/env python3
"""Capture first-wave source-engineering review metadata from existing records."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_REGISTER_DIR = Path("corpus/006_research-sources-and-bibliography/000_source-registers")
LARGE_SOURCE_REGISTER_DIR = Path("project_registry/006_large-source-register")

HANDOFF_SCAFFOLD = STAT_DIR / "118_ai-agent-source-engineering-review-wave-handoff-scaffold.json"
EVIDENCE_SNAPSHOT = STAT_DIR / "103_ai-agent-source-engineering-gap-evidence-snapshot.csv"
PIPELINE_AUDIT = STAT_DIR / "094_source-processing-pipeline-audit.csv"
SOURCE_INDEX = SOURCE_REGISTER_DIR / "001_all-sources-index.csv"
DOWNLOAD_MANIFEST = SOURCE_REGISTER_DIR / "003_source-download-manifest.csv"
DOWNLOAD_LOG = LARGE_SOURCE_REGISTER_DIR / "002_source-download-log.csv"
PACKAGE_MANIFEST = SOURCE_REGISTER_DIR / "009_source-package-file-manifest.csv"
METADATA_PROFILE = SOURCE_REGISTER_DIR / "010_downloaded-metadata-profile.csv"
FIELD_MAP_SCAFFOLD = STAT_DIR / "108_ai-agent-source-field-map-scaffold.csv"
FIELD_MAP_RESULT_SCAFFOLD = STAT_DIR / "110_ai-agent-source-field-map-review-result-scaffold.csv"
DEFAULT_OUTPUT = STAT_DIR / "119_ai-agent-source-engineering-first-wave-review-results.csv"

UPDATED_AT = "2026-06-19"
RESULT_STATUS = "metadata_captured_from_existing_records"
EVIDENCE_COLLECTION_STATUS = "existing_metadata_captured"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
COMPONENT_CLAIM_STATUS = "no_component_claim"
EVOLUTION_CLAIM_STATUS = "no_evolution_chain_claim"
HUMAN_REVIEW_STATUS = "metadata_reviewed_pending_human_decision"
RESEARCH_BOUNDARY = "source_engineering_first_wave_metadata-only_review_result_not_scholarship"
CAUTION = (
    "This row captures first-wave source-engineering metadata from existing "
    "local records only. It is not a new download, not checksum recalculation, "
    "not rights clearance, not source promotion, not corpus import, not an "
    "oracle-character identity claim, not a component assignment, not an "
    "evolution-chain assignment, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "first_wave_result_id",
    "handoff_item_id",
    "wave_id",
    "next_action_id",
    "source_engineering_gap_id",
    "evidence_snapshot_id",
    "source_id",
    "source_title",
    "provider",
    "source_url",
    "authority_tier",
    "source_register_status",
    "source_review_status",
    "action_lane",
    "gap_type",
    "priority_rank",
    "decision_field",
    "decision_value",
    "result_status",
    "evidence_collection_status",
    "human_review_status",
    "rights_status",
    "rights_decision_status",
    "risk_note",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "identity_claim_status",
    "component_claim_status",
    "evolution_claim_status",
    "download_manifest_ids",
    "download_manifest_artifact_kinds",
    "download_manifest_commit_policies",
    "download_log_ids",
    "download_log_status_counts",
    "download_log_http_status_counts",
    "download_log_file_size_bytes_total",
    "download_log_checksum_present_count",
    "download_log_risk_notes",
    "package_file_ids",
    "package_file_kinds",
    "package_file_commit_policies",
    "package_manifest_row_count",
    "metadata_profile_ids",
    "metadata_profile_metrics",
    "metadata_profile_metric_count",
    "metadata_profile_review_status_counts",
    "field_map_ids",
    "field_map_target_record_types",
    "field_map_review_status_counts",
    "field_map_scaffold_id",
    "field_map_review_status",
    "field_map_result_scaffold_id",
    "field_map_result_status",
    "pipeline_current_stage",
    "pipeline_observed_counts",
    "coverage_observed_counts",
    "evidence_snapshot_status",
    "required_next_checks",
    "remaining_blockers",
    "required_followup",
    "review_log_path",
    "result_record_path",
    "reviewed_evidence_paths",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def split_semicolon(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def count_semicolon(value: str) -> int:
    return len(split_semicolon(value))


def unique_in_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def by_field(rows: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    return {row[field]: row for row in rows if row.get(field)}


def rows_by_field(rows: list[dict[str, str]], field: str) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        result.setdefault(row.get(field, ""), []).append(row)
    return result


def decision_value(item: dict[str, Any], snapshot: dict[str, str]) -> str:
    lane = str(item["action_lane"])
    if lane == "access_boundary_followup":
        return "access_boundary_recorded_http_error_403"
    if lane == "checksum_and_download_status_review":
        return "no_checksum_recorded_for_http_error_403_no_recalculation"
    if lane == "metadata_profile_extraction_planning":
        return "metadata_profile_absent_existing_records_only"
    if lane == "source_field_map_planning":
        return "field_map_scaffold_exists_semantics_pending_human_review"
    if lane == "package_manifest_or_not_applicable_review":
        return "no_package_manifest_rows_found_decision_pending"
    if lane == "safe_derived_record_decision":
        return "metadata_profiles_available_promotion_decision_pending"
    raise ValueError(f"unsupported first-wave lane: {lane}")


def evidence_paths(lane: str) -> list[str]:
    paths = [
        HANDOFF_SCAFFOLD.as_posix(),
        EVIDENCE_SNAPSHOT.as_posix(),
        PIPELINE_AUDIT.as_posix(),
        SOURCE_INDEX.as_posix(),
        DOWNLOAD_MANIFEST.as_posix(),
        DOWNLOAD_LOG.as_posix(),
    ]
    if lane == "source_field_map_planning":
        paths.extend([FIELD_MAP_SCAFFOLD.as_posix(), FIELD_MAP_RESULT_SCAFFOLD.as_posix()])
    if lane in {"package_manifest_or_not_applicable_review", "metadata_profile_extraction_planning"}:
        paths.extend([PACKAGE_MANIFEST.as_posix(), METADATA_PROFILE.as_posix()])
    if lane == "safe_derived_record_decision":
        paths.extend([METADATA_PROFILE.as_posix()])
    return unique_in_order(paths)


def source_register_status(source_id: str, source_index_by_id: dict[str, dict[str, str]]) -> str:
    if source_id not in source_index_by_id:
        raise ValueError(f"missing source register row for {source_id}")
    return "source_register_row_found"


def matching_field_map_scaffold(
    item: dict[str, Any],
    field_scaffolds_by_action: dict[str, dict[str, str]],
    field_results_by_scaffold: dict[str, dict[str, str]],
) -> tuple[str, str, str, str, str]:
    if item["action_lane"] != "source_field_map_planning":
        return "", "", "", "", ""
    scaffold = field_scaffolds_by_action.get(str(item["next_action_id"]))
    if not scaffold:
        raise ValueError(f"missing field-map scaffold for {item['next_action_id']}")
    result = field_results_by_scaffold.get(scaffold["field_map_scaffold_id"], {})
    return (
        scaffold["field_map_scaffold_id"],
        scaffold["field_map_review_status"],
        result.get("field_map_result_scaffold_id", ""),
        result.get("field_map_result_status", ""),
        result.get("blockers", ""),
    )


def build_result_rows(root: Path) -> list[dict[str, str]]:
    handoff = read_json(root / HANDOFF_SCAFFOLD)
    snapshots = by_field(read_csv_rows(root / EVIDENCE_SNAPSHOT), "source_engineering_gap_id")
    pipeline_rows = by_field(read_csv_rows(root / PIPELINE_AUDIT), "source_id")
    source_index = by_field(read_csv_rows(root / SOURCE_INDEX), "source_id")
    package_rows = rows_by_field(read_csv_rows(root / PACKAGE_MANIFEST), "source_id")
    field_scaffolds_by_action = by_field(read_csv_rows(root / FIELD_MAP_SCAFFOLD), "next_action_id")
    field_results_by_scaffold = by_field(
        read_csv_rows(root / FIELD_MAP_RESULT_SCAFFOLD), "field_map_scaffold_id"
    )

    rows: list[dict[str, str]] = []
    for index, item in enumerate(handoff["handoff_items"], start=1):
        source_id = str(item["source_id"])
        gap_id = str(item["source_engineering_gap_id"])
        if gap_id not in snapshots:
            raise ValueError(f"missing evidence snapshot for {gap_id}")
        snapshot = snapshots[gap_id]
        pipeline = pipeline_rows.get(source_id, {})
        source = source_index.get(source_id, {})
        scaffold_id, scaffold_status, result_id, result_status, blockers = matching_field_map_scaffold(
            item, field_scaffolds_by_action, field_results_by_scaffold
        )
        package_file_ids = snapshot["package_file_ids"]
        package_row_count = count_semicolon(package_file_ids)
        if not package_row_count and package_rows.get(source_id):
            package_row_count = len(package_rows[source_id])
        metadata_metric_count = count_semicolon(snapshot["metadata_profile_ids"])
        lane = str(item["action_lane"])
        rows.append(
            {
                "first_wave_result_id": f"source-engineering-first-wave-review-result-{index:04d}",
                "handoff_item_id": str(item["handoff_item_id"]),
                "wave_id": str(item["wave_id"]),
                "next_action_id": str(item["next_action_id"]),
                "source_engineering_gap_id": gap_id,
                "evidence_snapshot_id": snapshot["evidence_snapshot_id"],
                "source_id": source_id,
                "source_title": snapshot["source_title"],
                "provider": snapshot["provider"],
                "source_url": snapshot["source_url"],
                "authority_tier": snapshot["authority_tier"],
                "source_register_status": source_register_status(source_id, source_index),
                "source_review_status": source.get("review_status", snapshot["source_review_status"]),
                "action_lane": lane,
                "gap_type": str(item["gap_type"]),
                "priority_rank": str(item["priority_rank"]),
                "decision_field": str(item["decision_field"]),
                "decision_value": decision_value(item, snapshot),
                "result_status": RESULT_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "human_review_status": HUMAN_REVIEW_STATUS,
                "rights_status": snapshot["rights_status"],
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "risk_note": snapshot["risk_note"],
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "corpus_import_status": CORPUS_IMPORT_STATUS,
                "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "component_claim_status": COMPONENT_CLAIM_STATUS,
                "evolution_claim_status": EVOLUTION_CLAIM_STATUS,
                "download_manifest_ids": snapshot["download_manifest_ids"],
                "download_manifest_artifact_kinds": snapshot["download_manifest_artifact_kinds"],
                "download_manifest_commit_policies": snapshot["download_manifest_commit_policies"],
                "download_log_ids": snapshot["download_log_ids"],
                "download_log_status_counts": snapshot["download_log_status_counts"],
                "download_log_http_status_counts": snapshot["download_log_http_status_counts"],
                "download_log_file_size_bytes_total": snapshot["download_log_file_size_bytes_total"],
                "download_log_checksum_present_count": snapshot["download_log_checksum_present_count"],
                "download_log_risk_notes": snapshot["download_log_risk_notes"],
                "package_file_ids": package_file_ids,
                "package_file_kinds": snapshot["package_file_kinds"],
                "package_file_commit_policies": snapshot["package_file_commit_policies"],
                "package_manifest_row_count": str(package_row_count),
                "metadata_profile_ids": snapshot["metadata_profile_ids"],
                "metadata_profile_metrics": snapshot["metadata_profile_metrics"],
                "metadata_profile_metric_count": str(metadata_metric_count),
                "metadata_profile_review_status_counts": snapshot["metadata_profile_review_status_counts"],
                "field_map_ids": snapshot["field_map_ids"],
                "field_map_target_record_types": snapshot["field_map_target_record_types"],
                "field_map_review_status_counts": snapshot["field_map_review_status_counts"],
                "field_map_scaffold_id": scaffold_id,
                "field_map_review_status": scaffold_status,
                "field_map_result_scaffold_id": result_id,
                "field_map_result_status": result_status,
                "pipeline_current_stage": pipeline.get("current_stage", snapshot["current_stage"]),
                "pipeline_observed_counts": snapshot["pipeline_observed_counts"],
                "coverage_observed_counts": snapshot["coverage_observed_counts"],
                "evidence_snapshot_status": snapshot["evidence_status"],
                "required_next_checks": snapshot["required_next_checks"],
                "remaining_blockers": blockers,
                "required_followup": ";".join(str(value) for value in item.get("required_followup", [])),
                "review_log_path": str(item["review_log_path"]),
                "result_record_path": str(item["result_record_path"]),
                "reviewed_evidence_paths": ";".join(evidence_paths(lane)),
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build first-wave source-engineering review results.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_result_rows(root)
    write_csv(root / args.output, rows)
    print(
        f"first_wave_result_count={len(rows)} "
        f"source_count={len({row['source_id'] for row in rows})} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
