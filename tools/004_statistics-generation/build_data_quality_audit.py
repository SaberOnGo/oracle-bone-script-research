#!/usr/bin/env python3
"""Build data-quality audit summaries for preprocessing records.

The audit checks engineering quality only: required fields, duplicate keys,
source-reference integrity, route-file availability, and candidate-boundary
status fields. It does not evaluate paleographic identity or decipherment.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from collections import Counter
from pathlib import Path
from typing import NamedTuple


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/092_data-quality-audit.csv")
OUTPUT_JSON = Path("corpus/009_statistics-and-derived-features/093_data-quality-summary.json")
UPDATED_AT = "2026-06-19"
CAUTION = (
    "Data-quality audit only; zero engineering issues here does not confirm "
    "oracle-character identity, readings, components, inscription context, "
    "or evolution/correspondence claims."
)

SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_DOWNLOAD_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/003_source-download-manifest.csv"
)
SOURCE_PACKAGE_FILE_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv"
)
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
LARGE_SOURCE_REGISTER = Path("project_registry/006_large-source-register/001_large-source-register.csv")
ASSET_SOURCE_INDEX = Path("project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv")
HUST_PROMOTION_QUEUE = Path("corpus/001_oracle-characters/000_character-registers/009_hust-obc-obs-char-promotion-review-queue.csv")
UNDECIPHERED_INDEX = Path("corpus/001_oracle-characters/000_character-registers/003_undeciphered-oracle-characters-index.csv")
OBIMD_MAIN_STAGING = Path("corpus/001_oracle-characters/000_character-registers/006_obimd-main-character-staging.csv")
HUST_CODEPOINT_CROSSWALK = Path("corpus/001_oracle-characters/000_character-registers/011_hust-obimd-evobc-codepoint-crosswalk-staging.csv")
CAMBRIDGE_HOPKINS_CROSSWALK_REVIEW_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/"
    "098_ai-agent-cambridge-hopkins-inscription-crosswalk-review-queue.csv"
)
SOURCE_ENGINEERING_GAP_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/099_ai-agent-source-engineering-gap-queue.csv"
)
SOURCE_ENGINEERING_EXECUTION_MATRIX = Path(
    "corpus/009_statistics-and-derived-features/100_ai-agent-source-engineering-execution-matrix.csv"
)
SOURCE_ENGINEERING_GAP_REVIEW_LOG_DRAFT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/"
    "102_ai-agent-source-engineering-gap-review-log-draft-manifest.csv"
)
SOURCE_ENGINEERING_GAP_EVIDENCE_SNAPSHOT = Path(
    "corpus/009_statistics-and-derived-features/"
    "103_ai-agent-source-engineering-gap-evidence-snapshot.csv"
)
SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/"
    "104_ai-agent-source-engineering-next-action-checklist.csv"
)
SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "105_ai-agent-source-engineering-next-action-result-scaffold.csv"
)
SOURCE_ENGINEERING_LANE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/"
    "106_ai-agent-source-engineering-lane-summary.csv"
)
SOURCE_FIELD_MAP_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "108_ai-agent-source-field-map-scaffold.csv"
)
SOURCE_FIELD_MAP_REVIEW_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/"
    "109_ai-agent-source-field-map-review-checklist.csv"
)
SOURCE_FIELD_MAP_REVIEW_RESULT_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "110_ai-agent-source-field-map-review-result-scaffold.csv"
)
REL_GRAPH_FILES = [
    Path("corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/008_cambridge-hopkins-inscription-crosswalk-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/009_character-asset-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/010_cross-source-id-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/011_component-asset-graph-edges.jsonl"),
]


class CsvDatasetSpec(NamedTuple):
    dataset_id: str
    dataset_type: str
    path: Path
    key_fields: tuple[str, ...]
    required_fields: tuple[str, ...]
    source_id_fields: tuple[str, ...] = ()
    download_id_fields: tuple[str, ...] = ()
    large_source_fields: tuple[str, ...] = ()
    path_fields: tuple[str, ...] = ()
    path_base: Path | None = None
    status_expectations: tuple[tuple[str, str], ...] = ()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def filesystem_path(path: Path) -> str:
    resolved = path.resolve()
    if os.name == "nt":
        return "\\\\?\\" + str(resolved)
    return str(resolved)


def path_exists(path: Path) -> bool:
    return os.path.exists(filesystem_path(path))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def compact_counter(counter: Counter[str]) -> str:
    return ";".join(f"{key}:{counter[key]}" for key in sorted(counter))


def count_missing_required_fields(rows: list[dict[str, str]], fields: tuple[str, ...]) -> int:
    return sum(1 for row in rows for field in fields if not row.get(field, "").strip())


def count_duplicate_keys(rows: list[dict[str, str]], fields: tuple[str, ...]) -> int:
    keys = Counter(tuple(row.get(field, "") for field in fields) for row in rows)
    return sum(count - 1 for count in keys.values() if count > 1)


def count_unknown_refs(rows: list[dict[str, str]], fields: tuple[str, ...], known_values: set[str]) -> int:
    unknown = 0
    for row in rows:
        for field in fields:
            values = [value for value in row.get(field, "").split(";") if value]
            for value in values:
                if value not in known_values:
                    unknown += 1
    return unknown


def count_missing_paths(
    root: Path,
    rows: list[dict[str, str]],
    fields: tuple[str, ...],
    path_base: Path | None = None,
) -> int:
    missing = 0
    base = root / path_base if path_base else root
    for row in rows:
        for field in fields:
            values = [value for value in row.get(field, "").split(";") if value]
            for value in values:
                if value.startswith("external_") or value.startswith("tmp/"):
                    continue
                if not path_exists(base / value):
                    missing += 1
    return missing


def count_status_violations(
    rows: list[dict[str, str]],
    expectations: tuple[tuple[str, str], ...],
) -> int:
    return sum(
        1
        for row in rows
        for field, expected in expectations
        if row.get(field, "") != expected
    )


def completeness_percent(rows: list[dict[str, str]], fields: tuple[str, ...]) -> str:
    denominator = len(rows) * len(fields)
    if denominator == 0:
        return "100.00"
    present = denominator - count_missing_required_fields(rows, fields)
    return f"{(present / denominator) * 100:.2f}"


def make_quality_row(
    quality_row_id: str,
    dataset_id: str,
    dataset_type: str,
    path: str,
    row_count: int,
    key_fields: tuple[str, ...],
    required_fields: tuple[str, ...],
    duplicate_key_count: int,
    missing_required_value_count: int,
    unknown_source_ref_count: int,
    unknown_download_ref_count: int,
    unknown_large_source_ref_count: int,
    missing_path_count: int,
    boundary_status_violation_count: int,
    status_counts: Counter[str],
) -> dict[str, str]:
    issue_count = (
        duplicate_key_count
        + missing_required_value_count
        + unknown_source_ref_count
        + unknown_download_ref_count
        + unknown_large_source_ref_count
        + missing_path_count
        + boundary_status_violation_count
    )
    return {
        "quality_row_id": quality_row_id,
        "dataset_id": dataset_id,
        "dataset_type": dataset_type,
        "path": path,
        "row_count": str(row_count),
        "key_fields": ";".join(key_fields),
        "required_fields": ";".join(required_fields),
        "duplicate_key_count": str(duplicate_key_count),
        "missing_required_value_count": str(missing_required_value_count),
        "unknown_source_ref_count": str(unknown_source_ref_count),
        "unknown_download_ref_count": str(unknown_download_ref_count),
        "unknown_large_source_ref_count": str(unknown_large_source_ref_count),
        "missing_path_count": str(missing_path_count),
        "boundary_status_violation_count": str(boundary_status_violation_count),
        "issue_count": str(issue_count),
        "completeness_percent": "",
        "status_counts": compact_counter(status_counts),
        "quality_status": "pass" if issue_count == 0 else "needs_review",
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def csv_quality_row(
    root: Path,
    spec: CsvDatasetSpec,
    source_ids: set[str],
    download_ids: set[str],
    large_source_ids: set[str],
    index: int,
) -> dict[str, str]:
    rows = read_csv_rows(root / spec.path)
    review_counter = Counter()
    for row in rows:
        for field in [
            "review_status",
            "draft_status",
            "evidence_collection_status",
            "human_review_status",
            "rights_decision_status",
            "source_promotion_status",
            "evidence_status",
            "corpus_import_status",
            "action_status",
            "safe_to_automate_status",
            "result_status",
            "decipherment_claim_status",
            "promotion_status",
            "assignment_status",
            "identity_claim_status",
            "field_map_review_status",
            "checklist_status",
            "field_map_result_status",
        ]:
            if field in row:
                review_counter[f"{field}={row.get(field, '')}"] += 1
    output = make_quality_row(
        quality_row_id=f"data-quality-{index:03d}",
        dataset_id=spec.dataset_id,
        dataset_type=spec.dataset_type,
        path=spec.path.as_posix(),
        row_count=len(rows),
        key_fields=spec.key_fields,
        required_fields=spec.required_fields,
        duplicate_key_count=count_duplicate_keys(rows, spec.key_fields),
        missing_required_value_count=count_missing_required_fields(rows, spec.required_fields),
        unknown_source_ref_count=count_unknown_refs(rows, spec.source_id_fields, source_ids),
        unknown_download_ref_count=count_unknown_refs(rows, spec.download_id_fields, download_ids),
        unknown_large_source_ref_count=count_unknown_refs(rows, spec.large_source_fields, large_source_ids),
        missing_path_count=count_missing_paths(root, rows, spec.path_fields, spec.path_base),
        boundary_status_violation_count=count_status_violations(rows, spec.status_expectations),
        status_counts=review_counter,
    )
    output["completeness_percent"] = completeness_percent(rows, spec.required_fields)
    return output


def graph_quality_row(root: Path, path: Path, source_ids: set[str], index: int) -> dict[str, str]:
    rows: list[dict[str, object]] = []
    parse_error_count = 0
    with (root / path).open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                parse_error_count += 1

    key_counter = Counter(str(row.get("edge_id", "")) for row in rows)
    duplicate_key_count = sum(count - 1 for count in key_counter.values() if count > 1)
    required_fields = (
        "edge_id",
        "source_node_id",
        "edge_type",
        "target_node_id",
        "confidence_level",
        "source_ids",
        "review_status",
    )
    missing_required = sum(
        1
        for row in rows
        for field in required_fields
        if not row.get(field)
    )
    unknown_source_refs = sum(
        1
        for row in rows
        for source_id in row.get("source_ids", [])
        if source_id not in source_ids
    )
    boundary_violations = sum(
        1
        for row in rows
        if row.get("review_status") != "reviewed" or row.get("confidence_level") != "high"
    )
    review_counter = Counter(
        f"review_status={row.get('review_status', '')};confidence_level={row.get('confidence_level', '')}"
        for row in rows
    )
    output = make_quality_row(
        quality_row_id=f"data-quality-{index:03d}",
        dataset_id=path.stem,
        dataset_type="relationship_graph_jsonl",
        path=path.as_posix(),
        row_count=len(rows),
        key_fields=("edge_id",),
        required_fields=required_fields,
        duplicate_key_count=duplicate_key_count,
        missing_required_value_count=missing_required + parse_error_count,
        unknown_source_ref_count=unknown_source_refs,
        unknown_download_ref_count=0,
        unknown_large_source_ref_count=0,
        missing_path_count=0,
        boundary_status_violation_count=boundary_violations,
        status_counts=review_counter,
    )
    output["completeness_percent"] = completeness_percent(
        [{field: str(row.get(field, "")) for field in required_fields} for row in rows],
        required_fields,
    )
    return output


def build_csv_specs() -> list[CsvDatasetSpec]:
    return [
        CsvDatasetSpec(
            dataset_id="source_index",
            dataset_type="source_registry",
            path=SOURCE_INDEX,
            key_fields=("source_id",),
            required_fields=(
                "source_id",
                "source_type",
                "title",
                "provider",
                "source_url",
                "rights_status",
                "risk_note",
                "review_status",
            ),
        ),
        CsvDatasetSpec(
            dataset_id="source_download_manifest",
            dataset_type="download_manifest",
            path=SOURCE_DOWNLOAD_MANIFEST,
            key_fields=("download_id",),
            required_fields=("download_id", "source_id", "url", "artifact_kind", "commit_policy", "max_bytes"),
            source_id_fields=("source_id",),
        ),
        CsvDatasetSpec(
            dataset_id="source_download_log",
            dataset_type="download_log",
            path=SOURCE_DOWNLOAD_LOG,
            key_fields=("download_id",),
            required_fields=("download_id", "source_id", "url", "downloaded_at", "status", "risk_note"),
            source_id_fields=("source_id",),
        ),
        CsvDatasetSpec(
            dataset_id="large_source_register",
            dataset_type="large_source_register",
            path=LARGE_SOURCE_REGISTER,
            key_fields=("source_package_id",),
            required_fields=(
                "source_package_id",
                "title",
                "provider",
                "source_url",
                "storage_status",
                "handling_strategy",
                "derived_record_paths",
                "rights_status",
                "risk_note",
                "review_status",
            ),
        ),
        CsvDatasetSpec(
            dataset_id="source_package_file_manifest",
            dataset_type="package_manifest",
            path=SOURCE_PACKAGE_FILE_MANIFEST,
            key_fields=("package_file_id",),
            required_fields=(
                "package_file_id",
                "source_package_id",
                "source_id",
                "file_name",
                "file_kind",
                "commit_policy",
                "handling_strategy",
                "rights_status",
                "review_status",
            ),
            source_id_fields=("source_id",),
            download_id_fields=("download_id",),
            large_source_fields=("source_package_id",),
        ),
        CsvDatasetSpec(
            dataset_id="asset_source_index",
            dataset_type="asset_registry",
            path=ASSET_SOURCE_INDEX,
            key_fields=("asset_id",),
            required_fields=(
                "asset_id",
                "asset_type",
                "canonical_path",
                "file_size_bytes",
                "primary_external_ref_id",
                "source_ids",
                "rights_status",
                "risk_note",
                "review_status",
            ),
            source_id_fields=("source_ids",),
            path_fields=("canonical_path",),
        ),
        CsvDatasetSpec(
            dataset_id="hust_obc_promotion_review_queue",
            dataset_type="candidate_character_queue",
            path=HUST_PROMOTION_QUEUE,
            key_fields=("promotion_queue_id",),
            required_fields=(
                "promotion_queue_id",
                "suggested_oracle_character_id",
                "suggested_character_directory",
                "candidate_class_id",
                "source_id",
                "primary_external_ref_id",
                "promotion_status",
                "required_next_review",
                "rights_status",
                "caution",
                "review_status",
            ),
            source_id_fields=("source_id",),
            path_fields=("suggested_bucket_directory",),
            path_base=Path("corpus/001_oracle-characters"),
            status_expectations=(
                ("assignment_status", "reserved_candidate_not_assigned"),
                ("promotion_status", "needs_cross_source_review"),
                ("review_status", "needs_review"),
            ),
        ),
        CsvDatasetSpec(
            dataset_id="hust_obc_undeciphered_candidate_index",
            dataset_type="undeciphered_candidate_index",
            path=UNDECIPHERED_INDEX,
            key_fields=("unknown_candidate_id",),
            required_fields=(
                "unknown_candidate_id",
                "source_id",
                "source_package_id",
                "evidence_download_id",
                "primary_external_ref_id",
                "source_image_count",
                "materialized_candidate_packet_path",
                "identity_claim_status",
                "promotion_status",
                "rights_status",
                "caution",
                "review_status",
            ),
            source_id_fields=("source_id",),
            download_id_fields=("evidence_download_id",),
            large_source_fields=("source_package_id",),
            path_fields=("materialized_candidate_packet_path",),
            status_expectations=(
                ("identity_claim_status", "no_identity_claim"),
                ("promotion_status", "not_promoted"),
                ("review_status", "reviewed_metadata_only"),
            ),
        ),
        CsvDatasetSpec(
            dataset_id="obimd_main_character_staging",
            dataset_type="component_glyph_staging",
            path=OBIMD_MAIN_STAGING,
            key_fields=("candidate_main_character_id",),
            required_fields=(
                "candidate_main_character_id",
                "source_id",
                "evidence_download_id",
                "source_uid",
                "primary_external_ref_id",
                "codepoint",
                "project_import_status",
                "rights_status",
                "caution",
                "review_status",
            ),
            source_id_fields=("source_id",),
            download_id_fields=("evidence_download_id",),
            status_expectations=(
                ("project_import_status", "dataset_candidate_not_promoted"),
                ("review_status", "reviewed_metadata_only"),
            ),
        ),
        CsvDatasetSpec(
            dataset_id="hust_obimd_evobc_codepoint_crosswalk",
            dataset_type="cross_source_candidate_crosswalk",
            path=HUST_CODEPOINT_CROSSWALK,
            key_fields=("crosswalk_candidate_id",),
            required_fields=(
                "crosswalk_candidate_id",
                "suggested_oracle_character_id",
                "promotion_queue_id",
                "hust_primary_external_ref_id",
                "matched_source_ids",
                "cross_source_status",
                "identity_claim_status",
                "promotion_status",
                "rights_status",
                "review_status",
                "route_files",
                "caution",
            ),
            source_id_fields=("matched_source_ids",),
            path_fields=("candidate_packet_path", "route_files"),
            status_expectations=(
                ("identity_claim_status", "no_identity_claim"),
                ("promotion_status", "not_promoted"),
                ("review_status", "needs_cross_source_review"),
            ),
        ),
        CsvDatasetSpec(
            dataset_id="cambridge_hopkins_inscription_crosswalk_review_queue",
            dataset_type="inscription_crosswalk_review_queue",
            path=CAMBRIDGE_HOPKINS_CROSSWALK_REVIEW_QUEUE,
            key_fields=("cambridge_hopkins_review_task_id",),
            required_fields=(
                "cambridge_hopkins_review_task_id",
                "candidate_inscription_crosswalk_id",
                "source_id",
                "evidence_download_id",
                "priority_rank",
                "priority_bucket",
                "yingguo_ref_id",
                "missing_reference_count",
                "required_next_checks",
                "route_files_to_open",
                "formal_inscription_assignment_status",
                "catalog_identity_claim_status",
                "image_evidence_status",
                "text_transcription_status",
                "collection_object_match_status",
                "task_status",
                "research_boundary",
                "rights_status",
                "review_status",
                "caution",
            ),
            source_id_fields=("source_id",),
            download_id_fields=("evidence_download_id",),
            path_fields=("route_files_to_open",),
            status_expectations=(
                ("formal_inscription_assignment_status", "not_assigned_formal_obi_id"),
                ("catalog_identity_claim_status", "not_confirmed_catalog_identity"),
                ("image_evidence_status", "not_collected"),
                ("text_transcription_status", "not_collected"),
                ("collection_object_match_status", "not_collected"),
                ("review_status", "needs_human_review"),
            ),
        ),
        CsvDatasetSpec(
            dataset_id="source_engineering_gap_queue",
            dataset_type="source_engineering_gap_queue",
            path=SOURCE_ENGINEERING_GAP_QUEUE,
            key_fields=("source_engineering_gap_id",),
            required_fields=(
                "source_engineering_gap_id",
                "source_id",
                "priority_rank",
                "gap_type",
                "current_stage",
                "rights_status",
                "observed_gap_evidence",
                "required_next_checks",
                "route_files_to_open",
                "expected_output_path",
                "commit_policy_boundary",
                "source_promotion_status",
                "research_boundary",
                "review_status",
                "caution",
            ),
            source_id_fields=("source_id",),
            path_fields=("route_files_to_open",),
            status_expectations=(
                ("commit_policy_boundary", "metadata_review_only_raw_or_temporary_material_stays_outside_regular_git"),
                ("source_promotion_status", "not_promoted"),
                ("review_status", "needs_source_engineering_review"),
            ),
        ),
        CsvDatasetSpec(
            dataset_id="source_engineering_execution_matrix",
            dataset_type="source_engineering_execution_matrix",
            path=SOURCE_ENGINEERING_EXECUTION_MATRIX,
            key_fields=("source_execution_id",),
            required_fields=(
                "source_execution_id",
                "source_id",
                "current_stage",
                "authority_tier",
                "rights_status",
                "gap_count",
                "highest_priority_rank",
                "safe_derivative_route_status",
                "source_promotion_status",
                "commit_policy_boundary",
                "research_boundary",
                "review_status",
                "caution",
            ),
            source_id_fields=("source_id",),
            path_fields=("route_files_to_open",),
            status_expectations=(
                ("source_promotion_status", "not_promoted"),
                ("commit_policy_boundary", "metadata_review_only_raw_or_temporary_material_stays_outside_regular_git"),
            ),
        ),
        CsvDatasetSpec(
            dataset_id="source_engineering_gap_review_log_draft_manifest",
            dataset_type="source_engineering_gap_review_log_draft_manifest",
            path=SOURCE_ENGINEERING_GAP_REVIEW_LOG_DRAFT_MANIFEST,
            key_fields=("review_log_draft_id",),
            required_fields=(
                "review_log_draft_id",
                "source_engineering_gap_id",
                "source_id",
                "gap_type",
                "priority_rank",
                "draft_path",
                "source_queue_path",
                "route_files_to_open",
                "observed_gap_evidence",
                "required_next_checks",
                "draft_status",
                "evidence_collection_status",
                "human_review_status",
                "rights_decision_status",
                "source_promotion_status",
                "commit_policy_boundary",
                "research_boundary",
                "caution",
            ),
            source_id_fields=("source_id",),
            path_fields=("draft_path", "source_queue_path", "route_files_to_open"),
            status_expectations=(
                ("draft_status", "draft_not_collected"),
                ("evidence_collection_status", "not_collected"),
                ("human_review_status", "pending_human_review"),
                ("rights_decision_status", "no_new_rights_decision"),
                ("source_promotion_status", "not_promoted"),
                ("commit_policy_boundary", "metadata_review_only_raw_or_temporary_material_stays_outside_regular_git"),
            ),
        ),
        CsvDatasetSpec(
            dataset_id="source_engineering_gap_evidence_snapshot",
            dataset_type="source_engineering_gap_evidence_snapshot",
            path=SOURCE_ENGINEERING_GAP_EVIDENCE_SNAPSHOT,
            key_fields=("evidence_snapshot_id",),
            required_fields=(
                "evidence_snapshot_id",
                "source_engineering_gap_id",
                "review_log_draft_id",
                "source_id",
                "gap_type",
                "priority_rank",
                "current_stage",
                "source_title",
                "provider",
                "source_url",
                "authority_tier",
                "rights_status",
                "risk_note",
                "source_review_status",
                "route_files_to_open",
                "route_file_missing_count",
                "draft_path",
                "required_next_checks",
                "evidence_status",
                "rights_decision_status",
                "source_promotion_status",
                "corpus_import_status",
                "research_boundary",
                "caution",
            ),
            source_id_fields=("source_id",),
            path_fields=("route_files_to_open", "draft_path"),
            status_expectations=(
                ("evidence_status", "metadata_only_existing_records_snapshot"),
                ("rights_decision_status", "no_new_rights_decision"),
                ("source_promotion_status", "not_promoted"),
                ("corpus_import_status", "not_imported"),
            ),
        ),
        CsvDatasetSpec(
            dataset_id="source_engineering_next_action_checklist",
            dataset_type="source_engineering_next_action_checklist",
            path=SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST,
            key_fields=("next_action_id",),
            required_fields=(
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
            ),
            source_id_fields=("source_id",),
            path_fields=("primary_input_path", "secondary_input_paths", "review_log_path"),
            status_expectations=(
                ("action_status", "ready_for_source_engineering_review"),
                ("human_review_status", "pending_human_review"),
                ("rights_decision_status", "no_new_rights_decision"),
                ("source_promotion_status", "not_promoted"),
                ("corpus_import_status", "not_imported"),
            ),
        ),
        CsvDatasetSpec(
            dataset_id="source_engineering_next_action_result_scaffold",
            dataset_type="source_engineering_next_action_result_scaffold",
            path=SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD,
            key_fields=("result_scaffold_id",),
            required_fields=(
                "result_scaffold_id",
                "next_action_id",
                "evidence_snapshot_id",
                "source_engineering_gap_id",
                "review_log_draft_id",
                "source_id",
                "gap_type",
                "priority_rank",
                "action_lane",
                "source_checklist_path",
                "source_review_log_path",
                "expected_result_path",
                "result_record_path",
                "result_status",
                "evidence_collection_status",
                "remaining_blockers",
                "required_followup",
                "human_review_status",
                "rights_decision_status",
                "source_promotion_status",
                "corpus_import_status",
                "decipherment_claim_status",
                "research_boundary",
                "caution",
            ),
            source_id_fields=("source_id",),
            path_fields=("source_checklist_path", "source_review_log_path"),
            status_expectations=(
                ("result_status", "not_started"),
                ("evidence_collection_status", "not_collected"),
                ("human_review_status", "pending_human_review"),
                ("rights_decision_status", "no_new_rights_decision"),
                ("source_promotion_status", "not_promoted"),
                ("corpus_import_status", "not_imported"),
                ("decipherment_claim_status", "no_decipherment_claim"),
            ),
        ),
        CsvDatasetSpec(
            dataset_id="source_engineering_lane_summary",
            dataset_type="source_engineering_lane_summary",
            path=SOURCE_ENGINEERING_LANE_SUMMARY,
            key_fields=("lane_summary_id",),
            required_fields=(
                "lane_summary_id",
                "action_lane",
                "action_count",
                "source_count",
                "priority_min",
                "priority_max",
                "gap_type_counts",
                "safe_to_automate_status_counts",
                "result_status_counts",
                "evidence_collection_status_counts",
                "human_review_status_counts",
                "rights_decision_status_counts",
                "source_promotion_status_counts",
                "corpus_import_status_counts",
                "decipherment_claim_status_counts",
                "source_ids",
                "next_action_ids",
                "result_scaffold_ids",
                "blocking_conditions",
                "checklist_path",
                "result_scaffold_path",
                "review_status",
                "research_boundary",
                "caution",
            ),
            source_id_fields=("source_ids",),
            path_fields=("checklist_path", "result_scaffold_path"),
            status_expectations=(
                ("review_status", "summary_only_pending_source_engineering_review"),
            ),
        ),
        CsvDatasetSpec(
            dataset_id="source_field_map_scaffold",
            dataset_type="source_field_map_scaffold",
            path=SOURCE_FIELD_MAP_SCAFFOLD,
            key_fields=("field_map_scaffold_id",),
            required_fields=(
                "field_map_scaffold_id",
                "next_action_id",
                "source_engineering_gap_id",
                "source_id",
                "source_title",
                "provider",
                "source_type",
                "source_url",
                "rights_status",
                "risk_note",
                "action_lane",
                "review_log_path",
                "result_record_path",
                "existing_field_map_count",
                "proposed_source_level",
                "proposed_source_field_or_unit",
                "proposed_source_meaning",
                "proposed_target_record_type",
                "proposed_target_project_fields",
                "field_map_review_status",
                "human_review_status",
                "rights_decision_status",
                "source_promotion_status",
                "corpus_import_status",
                "decipherment_claim_status",
                "research_boundary",
                "caution",
            ),
            source_id_fields=("source_id",),
            path_fields=("review_log_path",),
            status_expectations=(
                ("field_map_review_status", "pending_human_field_map_review"),
                ("human_review_status", "pending_human_review"),
                ("rights_decision_status", "no_new_rights_decision"),
                ("source_promotion_status", "not_promoted"),
                ("corpus_import_status", "not_imported"),
                ("decipherment_claim_status", "no_decipherment_claim"),
            ),
        ),
        CsvDatasetSpec(
            dataset_id="source_field_map_review_checklist",
            dataset_type="source_field_map_review_checklist",
            path=SOURCE_FIELD_MAP_REVIEW_CHECKLIST,
            key_fields=("field_map_checklist_id",),
            required_fields=(
                "field_map_checklist_id",
                "field_map_scaffold_id",
                "next_action_id",
                "source_engineering_gap_id",
                "source_id",
                "source_title",
                "provider",
                "source_type",
                "rights_status",
                "risk_note",
                "review_log_path",
                "result_record_path",
                "source_register_path",
                "existing_field_map_path",
                "lane_route_pack_path",
                "scaffold_path",
                "proposed_target_record_type",
                "proposed_target_project_fields",
                "required_review_steps",
                "blocking_condition",
                "checklist_status",
                "field_map_review_status",
                "human_review_status",
                "rights_decision_status",
                "source_promotion_status",
                "corpus_import_status",
                "decipherment_claim_status",
                "research_boundary",
                "caution",
            ),
            source_id_fields=("source_id",),
            path_fields=(
                "review_log_path",
                "source_register_path",
                "existing_field_map_path",
                "lane_route_pack_path",
                "scaffold_path",
            ),
            status_expectations=(
                ("checklist_status", "not_started"),
                ("field_map_review_status", "pending_human_field_map_review"),
                ("human_review_status", "pending_human_review"),
                ("rights_decision_status", "no_new_rights_decision"),
                ("source_promotion_status", "not_promoted"),
                ("corpus_import_status", "not_imported"),
                ("decipherment_claim_status", "no_decipherment_claim"),
            ),
        ),
        CsvDatasetSpec(
            dataset_id="source_field_map_review_result_scaffold",
            dataset_type="source_field_map_review_result_scaffold",
            path=SOURCE_FIELD_MAP_REVIEW_RESULT_SCAFFOLD,
            key_fields=("field_map_result_scaffold_id",),
            required_fields=(
                "field_map_result_scaffold_id",
                "field_map_checklist_id",
                "field_map_scaffold_id",
                "next_action_id",
                "source_engineering_gap_id",
                "source_id",
                "source_title",
                "provider",
                "source_type",
                "rights_status",
                "risk_note",
                "checklist_path",
                "scaffold_path",
                "review_log_path",
                "source_register_path",
                "target_reviewed_field_map_path",
                "result_record_path",
                "reserved_review_fields",
                "reviewed_source_level",
                "reviewed_source_field_or_unit",
                "reviewed_source_meaning",
                "reviewed_target_record_type",
                "reviewed_target_project_fields",
                "field_map_review_notes",
                "field_map_blockers",
                "required_followup",
                "field_map_result_status",
                "field_map_review_status",
                "human_review_status",
                "rights_decision_status",
                "source_promotion_status",
                "corpus_import_status",
                "decipherment_claim_status",
                "research_boundary",
                "caution",
            ),
            source_id_fields=("source_id",),
            path_fields=("checklist_path", "scaffold_path", "review_log_path", "source_register_path"),
            status_expectations=(
                ("field_map_result_status", "not_started"),
                ("field_map_review_status", "pending_human_field_map_review"),
                ("human_review_status", "pending_human_review"),
                ("rights_decision_status", "no_new_rights_decision"),
                ("source_promotion_status", "not_promoted"),
                ("corpus_import_status", "not_imported"),
                ("decipherment_claim_status", "no_decipherment_claim"),
            ),
        ),
    ]


def build_quality_rows(root: Path) -> list[dict[str, str]]:
    source_ids = {row["source_id"] for row in read_csv_rows(root / SOURCE_INDEX)}
    download_ids = {row["download_id"] for row in read_csv_rows(root / SOURCE_DOWNLOAD_LOG)}
    large_source_ids = {row["source_package_id"] for row in read_csv_rows(root / LARGE_SOURCE_REGISTER)}
    allowed_package_ids = set(large_source_ids)
    allowed_package_ids.update(f"light-src-{source_id.removeprefix('src-')}" for source_id in source_ids)

    rows: list[dict[str, str]] = []
    for index, spec in enumerate(build_csv_specs(), start=1):
        rows.append(csv_quality_row(root, spec, source_ids, download_ids, allowed_package_ids, index))
    offset = len(rows)
    for graph_index, graph_path in enumerate(REL_GRAPH_FILES, start=1):
        rows.append(graph_quality_row(root, graph_path, source_ids, offset + graph_index))
    return rows


def build_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    quality_status_counts = Counter(row["quality_status"] for row in rows)
    dataset_type_counts = Counter(row["dataset_type"] for row in rows)
    totals = Counter()
    for row in rows:
        for field in [
            "row_count",
            "duplicate_key_count",
            "missing_required_value_count",
            "unknown_source_ref_count",
            "unknown_download_ref_count",
            "unknown_large_source_ref_count",
            "missing_path_count",
            "boundary_status_violation_count",
            "issue_count",
        ]:
            totals[field] += int(row[field])
    return {
        "summary_id": "data-quality-summary-001",
        "updated_at": UPDATED_AT,
        "audit_csv_path": OUTPUT_CSV.as_posix(),
        "dataset_count": len(rows),
        "quality_status_counts": dict(sorted(quality_status_counts.items())),
        "dataset_type_counts": dict(sorted(dataset_type_counts.items())),
        "totals": dict(sorted(totals.items())),
        "completion_boundary": (
            "This summary verifies preprocessing data quality only. It does not "
            "promote candidate identities, readings, component assignments, "
            "inscription interpretations, or evolution/correspondence claims."
        ),
        "caution": CAUTION,
        "rows": rows,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    parser.add_argument("--json-output", default=str(OUTPUT_JSON))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_quality_rows(root)
    write_csv(root / args.csv_output, rows)
    write_json(root / args.json_output, build_summary(rows))
    print(f"data_quality_rows={len(rows)} csv={args.csv_output} json={args.json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
