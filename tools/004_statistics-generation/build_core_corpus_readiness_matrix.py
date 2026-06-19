#!/usr/bin/env python3
"""Build readiness and manual-review matrix for core corpus areas.

The matrix is a preprocessing navigation aid. It records formal records,
staging/candidate records, graph derivatives, review queues, and next entry
points for each core corpus area without making scholarly claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/096_core-corpus-readiness-matrix.csv")
OUTPUT_JSON = Path("corpus/009_statistics-and-derived-features/097_manual-review-backlog-summary.json")
CAMBRIDGE_HOPKINS_REVIEW_QUEUE = (
    "corpus/009_statistics-and-derived-features/"
    "098_ai-agent-cambridge-hopkins-inscription-crosswalk-review-queue.csv"
)
SOURCE_ENGINEERING_GAP_QUEUE = (
    "corpus/009_statistics-and-derived-features/"
    "099_ai-agent-source-engineering-gap-queue.csv"
)
SOURCE_ENGINEERING_EXECUTION_MATRIX = (
    "corpus/009_statistics-and-derived-features/"
    "100_ai-agent-source-engineering-execution-matrix.csv"
)
SOURCE_ENGINEERING_GAP_REVIEW_LOG_DRAFT_MANIFEST = (
    "corpus/009_statistics-and-derived-features/"
    "102_ai-agent-source-engineering-gap-review-log-draft-manifest.csv"
)
SOURCE_ENGINEERING_GAP_EVIDENCE_SNAPSHOT = (
    "corpus/009_statistics-and-derived-features/"
    "103_ai-agent-source-engineering-gap-evidence-snapshot.csv"
)
SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST = (
    "corpus/009_statistics-and-derived-features/"
    "104_ai-agent-source-engineering-next-action-checklist.csv"
)
SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "105_ai-agent-source-engineering-next-action-result-scaffold.csv"
)
SOURCE_ENGINEERING_LANE_ROUTE_PACK = (
    "corpus/009_statistics-and-derived-features/"
    "107_ai-agent-source-engineering-lane-route-pack.json"
)
SOURCE_FIELD_MAP_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "108_ai-agent-source-field-map-scaffold.csv"
)
SOURCE_FIELD_MAP_REVIEW_CHECKLIST = (
    "corpus/009_statistics-and-derived-features/"
    "109_ai-agent-source-field-map-review-checklist.csv"
)
SOURCE_FIELD_MAP_REVIEW_RESULT_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "110_ai-agent-source-field-map-review-result-scaffold.csv"
)
SOURCE_FIELD_MAP_REVIEW_ROUTE_PACK = (
    "corpus/009_statistics-and-derived-features/"
    "111_ai-agent-source-field-map-review-route-pack.json"
)
SOURCE_PACKAGE_MANIFEST_REVIEW_ROUTE_PACK = (
    "corpus/009_statistics-and-derived-features/"
    "112_ai-agent-source-package-manifest-review-route-pack.json"
)
SOURCE_ACCESS_BOUNDARY_REVIEW_ROUTE_PACK = (
    "corpus/009_statistics-and-derived-features/"
    "113_ai-agent-source-access-boundary-review-route-pack.json"
)
SOURCE_CHECKSUM_REVIEW_ROUTE_PACK = (
    "corpus/009_statistics-and-derived-features/"
    "114_ai-agent-source-checksum-review-route-pack.json"
)
SOURCE_METADATA_PROFILE_REVIEW_ROUTE_PACK = (
    "corpus/009_statistics-and-derived-features/"
    "115_ai-agent-source-metadata-profile-review-route-pack.json"
)
SOURCE_SAFE_DERIVED_RECORD_REVIEW_ROUTE_PACK = (
    "corpus/009_statistics-and-derived-features/"
    "116_ai-agent-source-safe-derived-record-review-route-pack.json"
)
SOURCE_ENGINEERING_REVIEW_ROUTE_SUMMARY = (
    "corpus/009_statistics-and-derived-features/"
    "117_ai-agent-source-engineering-review-route-summary.json"
)
SOURCE_ENGINEERING_REVIEW_WAVE_HANDOFF_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "118_ai-agent-source-engineering-review-wave-handoff-scaffold.json"
)
SOURCE_ENGINEERING_FIRST_WAVE_REVIEW_RESULTS = (
    "corpus/009_statistics-and-derived-features/"
    "119_ai-agent-source-engineering-first-wave-review-results.csv"
)
SOURCE_ENGINEERING_FIRST_WAVE_RESULT_RECORD_MANIFEST = (
    "corpus/009_statistics-and-derived-features/"
    "120_ai-agent-source-engineering-first-wave-result-record-manifest.csv"
)
SOURCE_ENGINEERING_FIRST_WAVE_FOLLOWUP_QUEUE = (
    "corpus/009_statistics-and-derived-features/"
    "121_ai-agent-source-engineering-first-wave-followup-queue.csv"
)
SOURCE_ENGINEERING_FIRST_WAVE_SOURCE_STATUS = (
    "corpus/009_statistics-and-derived-features/"
    "122_ai-agent-source-engineering-first-wave-source-status.csv"
)
SOURCE_ENGINEERING_SECOND_WAVE_SOURCE_CHECKLIST = (
    "corpus/009_statistics-and-derived-features/"
    "123_ai-agent-source-engineering-second-wave-source-checklist.csv"
)
SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_DRAFT_MANIFEST = (
    "corpus/009_statistics-and-derived-features/"
    "124_ai-agent-source-engineering-second-wave-review-draft-manifest.csv"
)
SOURCE_ENGINEERING_SECOND_WAVE_RESULT_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "125_ai-agent-source-engineering-second-wave-result-scaffold.csv"
)
SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_CHECKLIST = (
    "corpus/009_statistics-and-derived-features/"
    "126_ai-agent-source-engineering-second-wave-review-checklist.csv"
)
SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_OUTCOME_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "127_ai-agent-source-engineering-second-wave-review-outcome-scaffold.csv"
)
SOURCE_ENGINEERING_SECOND_WAVE_OUTCOME_ROUTE_PACK = (
    "corpus/009_statistics-and-derived-features/"
    "128_ai-agent-source-engineering-second-wave-outcome-route-pack.json"
)
SOURCE_ENGINEERING_SECOND_WAVE_OUTCOME_HANDOFF_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "129_ai-agent-source-engineering-second-wave-outcome-handoff-scaffold.json"
)
SOURCE_ENGINEERING_SECOND_WAVE_HANDOFF_REVIEW_CHECKLIST = (
    "corpus/009_statistics-and-derived-features/"
    "130_ai-agent-source-engineering-second-wave-handoff-review-checklist.csv"
)
SOURCE_ENGINEERING_SECOND_WAVE_HANDOFF_ROUTE_SUMMARY = (
    "corpus/009_statistics-and-derived-features/"
    "131_ai-agent-source-engineering-second-wave-handoff-route-summary.json"
)
SOURCE_PIPELINE_GAP_MATRIX = (
    "corpus/009_statistics-and-derived-features/"
    "132_ai-agent-source-pipeline-gap-matrix.csv"
)
SOURCE_PIPELINE_GAP_REVIEW_CHECKLIST = (
    "corpus/009_statistics-and-derived-features/"
    "133_ai-agent-source-pipeline-gap-review-checklist.csv"
)
SOURCE_PIPELINE_EVIDENCE_LEDGER = (
    "corpus/009_statistics-and-derived-features/"
    "134_ai-agent-source-pipeline-evidence-ledger.csv"
)
CORE_CORPUS_PHASE_COVERAGE_MATRIX = (
    "corpus/009_statistics-and-derived-features/"
    "135_core-corpus-phase-coverage-matrix.csv"
)
SOURCE_PIPELINE_PHASE_COVERAGE_MATRIX = (
    "corpus/009_statistics-and-derived-features/"
    "136_source-pipeline-phase-coverage-matrix.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_QUEUE = (
    "corpus/009_statistics-and-derived-features/"
    "137_source-pipeline-phase-action-queue.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_RESULT_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "138_source-pipeline-phase-action-result-scaffold.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_ROUTE_SUMMARY = (
    "corpus/009_statistics-and-derived-features/"
    "139_source-pipeline-phase-action-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_SOURCE_SUMMARY = (
    "corpus/009_statistics-and-derived-features/"
    "140_source-pipeline-phase-action-source-summary.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_FILE_CHECKLIST = (
    "corpus/009_statistics-and-derived-features/"
    "141_source-pipeline-phase-action-file-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_PRESENCE_MATRIX = (
    "corpus/009_statistics-and-derived-features/"
    "142_source-pipeline-phase-action-evidence-presence-matrix.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_GAP_SUMMARY = (
    "corpus/009_statistics-and-derived-features/"
    "143_source-pipeline-phase-action-evidence-gap-summary.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ACTION_QUEUE = (
    "corpus/009_statistics-and-derived-features/"
    "144_source-pipeline-phase-action-missing-evidence-action-queue.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_RESULT_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "145_source-pipeline-phase-action-missing-evidence-result-scaffold.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ROUTE_SUMMARY = (
    "corpus/009_statistics-and-derived-features/"
    "146_source-pipeline-phase-action-missing-evidence-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_SOURCE_SUMMARY = (
    "corpus/009_statistics-and-derived-features/"
    "147_source-pipeline-phase-action-missing-evidence-source-summary.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_DRAFT_MANIFEST = (
    "corpus/009_statistics-and-derived-features/"
    "148_source-pipeline-phase-action-missing-evidence-review-draft-manifest.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_RESULT_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "149_source-pipeline-phase-action-missing-evidence-result-scaffold.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_CHECKLIST = (
    "corpus/009_statistics-and-derived-features/"
    "150_source-pipeline-phase-action-missing-evidence-review-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_ROUTE_PACK = (
    "corpus/009_statistics-and-derived-features/"
    "151_source-pipeline-phase-action-missing-evidence-review-route-pack.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "152_source-pipeline-phase-action-missing-evidence-review-handoff-scaffold.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_CHECKLIST = (
    "corpus/009_statistics-and-derived-features/"
    "153_source-pipeline-phase-action-missing-evidence-review-handoff-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_ROUTE_SUMMARY = (
    "corpus/009_statistics-and-derived-features/"
    "154_source-pipeline-phase-action-missing-evidence-review-handoff-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "155_source-pipeline-phase-action-missing-evidence-review-outcome-scaffold.csv"
)
UPDATED_AT = "2026-06-19"
CAUTION = (
    "Core corpus readiness only; candidate, staging, graph, and review-queue "
    "counts do not confirm readings, identities, components, inscriptions, "
    "or evolution/correspondence claims."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(root: Path, path: str) -> list[dict[str, str]]:
    with (root / path).open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def count_csv(root: Path, path: str) -> int:
    return len(read_csv_rows(root, path))


def count_files(root: Path, pattern: str) -> int:
    return sum(1 for _ in root.glob(pattern))


def count_existing_file(root: Path, path: str) -> int:
    return 1 if (root / path).exists() else 0


def count_jsonl(root: Path, path: str) -> int:
    count = 0
    with (root / path).open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                count += 1
    return count


def count_statistics_outputs(root: Path) -> int:
    excluded = {OUTPUT_CSV.name, OUTPUT_JSON.name}
    stats_dir = root / "corpus/009_statistics-and-derived-features"
    return sum(1 for path in stats_dir.glob("*.csv") if path.name not in excluded) + sum(
        1 for path in stats_dir.glob("*.json") if path.name not in excluded
    )


def readiness_stage(
    formal_count: int,
    staging_count: int,
    candidate_count: int,
    graph_edge_count: int,
    review_queue_count: int,
    quality_status: str,
) -> str:
    if review_queue_count:
        return "ready_for_human_review"
    if graph_edge_count:
        return "linked_candidate_derivatives"
    if formal_count and quality_status == "pass":
        return "verified_formal_records"
    if staging_count or candidate_count:
        return "structured_staging"
    return "registered_empty_or_scaffold"


def review_priority(review_queue_count: int, formal_count: int, staging_count: int, graph_edge_count: int) -> str:
    if review_queue_count >= 1000:
        return "high_batch_review"
    if review_queue_count > 0:
        return "targeted_review"
    if graph_edge_count > 0 and formal_count == 0:
        return "graph_derivative_boundary_review"
    if staging_count > 0 and formal_count == 0:
        return "staging_promotion_policy_review"
    return "monitor"


def make_row(
    area_id: str,
    corpus_area: str,
    label_en: str,
    label_zh: str,
    formal_count: int,
    staging_count: int,
    candidate_count: int,
    graph_edge_count: int,
    review_queue_count: int,
    manual_review_backlog_count: int,
    primary_entry_path: str,
    review_queue_path: str,
    next_action: str,
    quality_status: str = "pass",
) -> dict[str, str]:
    stage = readiness_stage(
        formal_count,
        staging_count,
        candidate_count,
        graph_edge_count,
        review_queue_count,
        quality_status,
    )
    return {
        "readiness_row_id": area_id,
        "corpus_area": corpus_area,
        "label_en": label_en,
        "label_zh": label_zh,
        "formal_record_count": str(formal_count),
        "staging_record_count": str(staging_count),
        "candidate_record_count": str(candidate_count),
        "graph_edge_count": str(graph_edge_count),
        "review_queue_count": str(review_queue_count),
        "manual_review_backlog_count": str(manual_review_backlog_count),
        "readiness_stage": stage,
        "review_priority": review_priority(review_queue_count, formal_count, staging_count, graph_edge_count),
        "primary_entry_path": primary_entry_path,
        "review_queue_path": review_queue_path,
        "next_action": next_action,
        "quality_status": quality_status,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_readiness_rows(root: Path) -> list[dict[str, str]]:
    hust_candidate_graph_edges = count_jsonl(
        root, "corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl"
    )
    obimd_graph_edges = count_jsonl(root, "corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl")
    evobc_graph_edges = count_jsonl(root, "corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl")
    cambridge_hopkins_graph_edges = count_jsonl(
        root, "corpus/008_relationship-graph/008_cambridge-hopkins-inscription-crosswalk-graph-edges.jsonl"
    )
    graph_edge_total = (
        hust_candidate_graph_edges
        + obimd_graph_edges
        + evobc_graph_edges
        + cambridge_hopkins_graph_edges
    )

    collection_staging_count = sum(
        count_csv(root, path)
        for path in [
            "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/001_institutional-collection-provenance-staging.csv",
            "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/002_ihp-museum-oracle-bone-object-staging.csv",
            "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/003_smithsonian-nmaa-oracle-bone-object-staging.csv",
            "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/004_penn-museum-oracle-bone-object-staging.csv",
            "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/005_metmuseum-oracle-bone-object-staging.csv",
        ]
    )
    source_staging_count = sum(
        count_csv(root, path)
        for path in [
            "corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv",
            "corpus/006_research-sources-and-bibliography/000_source-registers/003_source-download-manifest.csv",
            "corpus/006_research-sources-and-bibliography/000_source-registers/007_source-field-map.csv",
            "corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv",
            "corpus/006_research-sources-and-bibliography/000_source-registers/010_downloaded-metadata-profile.csv",
        ]
    )
    research_note_count = count_files(root, "research/**/*.md")
    cambridge_hopkins_review_queue_count = count_csv(root, CAMBRIDGE_HOPKINS_REVIEW_QUEUE)
    source_engineering_gap_queue_count = count_csv(root, SOURCE_ENGINEERING_GAP_QUEUE)
    source_engineering_execution_matrix_count = count_csv(root, SOURCE_ENGINEERING_EXECUTION_MATRIX)
    source_engineering_gap_review_log_draft_count = count_csv(
        root, SOURCE_ENGINEERING_GAP_REVIEW_LOG_DRAFT_MANIFEST
    )
    source_engineering_gap_evidence_snapshot_count = count_csv(
        root, SOURCE_ENGINEERING_GAP_EVIDENCE_SNAPSHOT
    )
    source_engineering_next_action_checklist_count = count_csv(
        root, SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST
    )
    source_engineering_next_action_result_scaffold_count = count_csv(
        root, SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD
    )
    source_field_map_scaffold_count = count_csv(root, SOURCE_FIELD_MAP_SCAFFOLD)
    source_field_map_review_checklist_count = count_csv(root, SOURCE_FIELD_MAP_REVIEW_CHECKLIST)
    source_field_map_review_result_scaffold_count = count_csv(root, SOURCE_FIELD_MAP_REVIEW_RESULT_SCAFFOLD)
    source_field_map_review_route_pack_count = count_existing_file(root, SOURCE_FIELD_MAP_REVIEW_ROUTE_PACK)
    source_package_manifest_review_route_pack_count = count_existing_file(
        root, SOURCE_PACKAGE_MANIFEST_REVIEW_ROUTE_PACK
    )
    source_access_boundary_review_route_pack_count = count_existing_file(
        root, SOURCE_ACCESS_BOUNDARY_REVIEW_ROUTE_PACK
    )
    source_checksum_review_route_pack_count = count_existing_file(root, SOURCE_CHECKSUM_REVIEW_ROUTE_PACK)
    source_metadata_profile_review_route_pack_count = count_existing_file(
        root, SOURCE_METADATA_PROFILE_REVIEW_ROUTE_PACK
    )
    source_safe_derived_record_review_route_pack_count = count_existing_file(
        root, SOURCE_SAFE_DERIVED_RECORD_REVIEW_ROUTE_PACK
    )
    source_engineering_review_route_summary_count = count_existing_file(
        root, SOURCE_ENGINEERING_REVIEW_ROUTE_SUMMARY
    )
    source_engineering_review_wave_handoff_scaffold_count = count_existing_file(
        root, SOURCE_ENGINEERING_REVIEW_WAVE_HANDOFF_SCAFFOLD
    )
    source_engineering_first_wave_review_result_count = count_csv(
        root, SOURCE_ENGINEERING_FIRST_WAVE_REVIEW_RESULTS
    )
    source_engineering_first_wave_result_record_manifest_count = count_csv(
        root, SOURCE_ENGINEERING_FIRST_WAVE_RESULT_RECORD_MANIFEST
    )
    source_engineering_first_wave_followup_queue_count = count_csv(
        root, SOURCE_ENGINEERING_FIRST_WAVE_FOLLOWUP_QUEUE
    )
    source_engineering_first_wave_source_status_count = count_csv(
        root, SOURCE_ENGINEERING_FIRST_WAVE_SOURCE_STATUS
    )
    source_engineering_second_wave_source_checklist_count = count_csv(
        root, SOURCE_ENGINEERING_SECOND_WAVE_SOURCE_CHECKLIST
    )
    source_engineering_second_wave_review_draft_manifest_count = count_csv(
        root, SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_DRAFT_MANIFEST
    )
    source_engineering_second_wave_result_scaffold_count = count_csv(
        root, SOURCE_ENGINEERING_SECOND_WAVE_RESULT_SCAFFOLD
    )
    source_engineering_second_wave_review_checklist_count = count_csv(
        root, SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_CHECKLIST
    )
    source_engineering_second_wave_review_outcome_scaffold_count = count_csv(
        root, SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_OUTCOME_SCAFFOLD
    )
    source_engineering_second_wave_outcome_route_pack_count = count_existing_file(
        root, SOURCE_ENGINEERING_SECOND_WAVE_OUTCOME_ROUTE_PACK
    )
    source_engineering_second_wave_outcome_handoff_scaffold_count = count_existing_file(
        root, SOURCE_ENGINEERING_SECOND_WAVE_OUTCOME_HANDOFF_SCAFFOLD
    )
    source_engineering_second_wave_handoff_review_checklist_count = count_csv(
        root, SOURCE_ENGINEERING_SECOND_WAVE_HANDOFF_REVIEW_CHECKLIST
    )
    source_engineering_second_wave_handoff_route_summary_count = count_existing_file(
        root, SOURCE_ENGINEERING_SECOND_WAVE_HANDOFF_ROUTE_SUMMARY
    )
    source_pipeline_gap_matrix_count = count_csv(root, SOURCE_PIPELINE_GAP_MATRIX)
    source_pipeline_gap_review_checklist_count = count_csv(root, SOURCE_PIPELINE_GAP_REVIEW_CHECKLIST)
    source_pipeline_evidence_ledger_count = count_csv(root, SOURCE_PIPELINE_EVIDENCE_LEDGER)
    core_corpus_phase_coverage_count = count_csv(root, CORE_CORPUS_PHASE_COVERAGE_MATRIX)
    source_pipeline_phase_coverage_count = count_csv(root, SOURCE_PIPELINE_PHASE_COVERAGE_MATRIX)
    source_pipeline_phase_action_queue_count = count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_QUEUE)
    source_pipeline_phase_action_result_scaffold_count = count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_RESULT_SCAFFOLD)
    source_pipeline_phase_action_route_summary_count = count_existing_file(
        root, SOURCE_PIPELINE_PHASE_ACTION_ROUTE_SUMMARY
    )
    source_pipeline_phase_action_source_summary_count = count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_SOURCE_SUMMARY)
    source_pipeline_phase_action_file_checklist_count = count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_FILE_CHECKLIST)
    source_pipeline_phase_action_evidence_presence_count = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_PRESENCE_MATRIX
    )
    source_pipeline_phase_action_evidence_gap_summary_count = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_GAP_SUMMARY
    )
    source_pipeline_phase_action_missing_evidence_action_queue_count = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ACTION_QUEUE
    )
    source_pipeline_phase_action_missing_evidence_result_scaffold_count = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_RESULT_SCAFFOLD
    )
    source_pipeline_phase_action_missing_evidence_route_summary_count = count_existing_file(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ROUTE_SUMMARY
    )
    source_pipeline_phase_action_missing_evidence_source_summary_count = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_SOURCE_SUMMARY
    )
    source_pipeline_phase_action_missing_evidence_review_draft_manifest_count = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_DRAFT_MANIFEST
    )
    source_pipeline_phase_action_missing_evidence_review_result_scaffold_count = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_RESULT_SCAFFOLD
    )
    source_pipeline_phase_action_missing_evidence_review_checklist_count = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_CHECKLIST
    )
    source_pipeline_phase_action_missing_evidence_review_route_pack_count = count_existing_file(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_ROUTE_PACK
    )
    source_pipeline_phase_action_missing_evidence_review_handoff_scaffold_count = count_existing_file(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_SCAFFOLD
    )
    source_pipeline_phase_action_missing_evidence_review_handoff_checklist_count = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_CHECKLIST
    )
    source_pipeline_phase_action_missing_evidence_review_handoff_route_summary_count = count_existing_file(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_ROUTE_SUMMARY
    )
    source_pipeline_phase_action_missing_evidence_review_outcome_scaffold_count = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_SCAFFOLD
    )

    rows = [
        make_row(
            "core-ready-001",
            "oracle_characters",
            "Deciphered-class oracle character candidates",
            "已释类别甲骨单字候选",
            count_csv(root, "corpus/001_oracle-characters/000_character-registers/001_all-oracle-characters-index.csv"),
            count_csv(root, "corpus/001_oracle-characters/000_character-registers/005_hust-obc-validation-class-staging.csv")
            + count_csv(root, "corpus/001_oracle-characters/000_character-registers/007_hust-obc-validation-label-crosswalk-staging.csv")
            + count_csv(root, "corpus/001_oracle-characters/000_character-registers/008_hust-obc-source-category-staging.csv"),
            count_csv(root, "corpus/001_oracle-characters/000_character-registers/009_hust-obc-obs-char-promotion-review-queue.csv"),
            hust_candidate_graph_edges,
            count_csv(root, "corpus/001_oracle-characters/000_character-registers/009_hust-obc-obs-char-promotion-review-queue.csv"),
            count_csv(root, "corpus/001_oracle-characters/000_character-registers/009_hust-obc-obs-char-promotion-review-queue.csv"),
            "corpus/001_oracle-characters/000_character-registers/009_hust-obc-obs-char-promotion-review-queue.csv",
            "corpus/009_statistics-and-derived-features/005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv",
            "batch_review_reserved_obs_char_candidates_before_any_formal_character_assignment",
        ),
        make_row(
            "core-ready-002",
            "undeciphered_oracle_character_candidates",
            "Undeciphered oracle character candidates",
            "未释甲骨字候选",
            0,
            count_csv(root, "corpus/001_oracle-characters/000_character-registers/003_undeciphered-oracle-characters-index.csv"),
            count_files(root, "corpus/001_oracle-characters/**/01_undeciphered-candidate-packet.json"),
            0,
            count_csv(root, "corpus/009_statistics-and-derived-features/051_ai-agent-hust-obc-undeciphered-candidate-review-queue.csv"),
            count_csv(root, "corpus/009_statistics-and-derived-features/051_ai-agent-hust-obc-undeciphered-candidate-review-queue.csv"),
            "corpus/001_oracle-characters/000_character-registers/003_undeciphered-oracle-characters-index.csv",
            "corpus/009_statistics-and-derived-features/051_ai-agent-hust-obc-undeciphered-candidate-review-queue.csv",
            "collect_source_marked_evidence_for_priority_undeciphered_candidates_keep_no_identity_claim",
        ),
        make_row(
            "core-ready-003",
            "cross_source_codepoint_routes",
            "HUST/OBIMD/EVOBC codepoint lookup routes",
            "HUST/OBIMD/EVOBC 码位检索路线",
            0,
            count_csv(root, "corpus/001_oracle-characters/000_character-registers/011_hust-obimd-evobc-codepoint-crosswalk-staging.csv"),
            count_csv(root, "corpus/009_statistics-and-derived-features/041_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-queue.csv"),
            0,
            count_csv(root, "corpus/009_statistics-and-derived-features/041_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-queue.csv"),
            count_csv(root, "corpus/009_statistics-and-derived-features/041_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-queue.csv"),
            "corpus/001_oracle-characters/000_character-registers/011_hust-obimd-evobc-codepoint-crosswalk-staging.csv",
            "corpus/009_statistics-and-derived-features/041_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-queue.csv",
            "review_lookup_routes_as_evidence_paths_not_identity_or_reading_claims",
        ),
        make_row(
            "core-ready-004",
            "graphemic_components",
            "OBIMD component and glyph-codepoint candidates",
            "OBIMD 构件与字形码位候选",
            count_csv(root, "corpus/003_graphemic-components/000_component-registers/001_all-components-index.csv"),
            count_csv(root, "corpus/003_graphemic-components/000_component-registers/002_obimd-subcharacter-main-staging.csv")
            + count_csv(root, "corpus/003_graphemic-components/000_component-registers/003_obimd-subcharacter-glyph-staging.csv"),
            0,
            obimd_graph_edges,
            count_files(root, "doc/public/user_research/002_cross-source-review-queues/obimd/*.md"),
            count_files(root, "doc/public/user_research/002_cross-source-review-queues/obimd/*.md"),
            "corpus/003_graphemic-components/000_component-registers/002_obimd-subcharacter-main-staging.csv",
            "doc/public/user_research/002_cross-source-review-queues/obimd/",
            "review_obimd_component_routes_without_promoting_formal_component_ids",
        ),
        make_row(
            "core-ready-005",
            "evolution_correspondences",
            "EVOBC evolution/correspondence candidates",
            "EVOBC 字形演化/对应候选",
            0,
            count_csv(root, "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/001_evobc-evolution-category-staging.csv")
            + count_csv(root, "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/002_evobc-era-source-codebook-staging.csv"),
            0,
            evobc_graph_edges,
            count_files(root, "doc/public/user_research/002_cross-source-review-queues/evobc/*.md"),
            count_files(root, "doc/public/user_research/002_cross-source-review-queues/evobc/*.md"),
            "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/001_evobc-evolution-category-staging.csv",
            "doc/public/user_research/002_cross-source-review-queues/evobc/",
            "review_evolution_routes_as_dataset_links_not_formal_evolution_chains",
        ),
        make_row(
            "core-ready-006",
            "inscriptions_and_plate_crosswalks",
            "Inscription and plate/catalog crosswalk staging",
            "卜辞与图版/著录交叉暂存",
            count_csv(root, "corpus/002_oracle-bone-inscriptions/000_inscription-registers/001_all-inscriptions-index.csv"),
            count_csv(root, "corpus/002_oracle-bone-inscriptions/000_inscription-registers/002_cambridge-hopkins-crosswalk-staging.csv")
            + count_csv(root, "corpus/002_oracle-bone-inscriptions/000_inscription-registers/003_cambridge-hopkins-classified-summary.csv"),
            0,
            cambridge_hopkins_graph_edges,
            cambridge_hopkins_review_queue_count,
            cambridge_hopkins_review_queue_count,
            "corpus/002_oracle-bone-inscriptions/000_inscription-registers/002_cambridge-hopkins-crosswalk-staging.csv",
            CAMBRIDGE_HOPKINS_REVIEW_QUEUE,
            "expand_inscription_records_from_reviewed_catalog_crosswalks_and_access_boundary_routes",
        ),
        make_row(
            "core-ready-007",
            "collection_provenance_assets",
            "Collection provenance and public-domain object assets",
            "馆藏出处与公版对象资产",
            count_files(root, "corpus/005_excavation-sites-periods-and-batches/001_public-domain-object-image-assets/*.jpg"),
            collection_staging_count,
            0,
            0,
            count_csv(root, "corpus/009_statistics-and-derived-features/074_ai-agent-xxt-obm-access-boundary-followup-review-queue.csv"),
            count_csv(root, "corpus/009_statistics-and-derived-features/074_ai-agent-xxt-obm-access-boundary-followup-review-queue.csv"),
            "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/001_institutional-collection-provenance-staging.csv",
            "corpus/009_statistics-and-derived-features/074_ai-agent-xxt-obm-access-boundary-followup-review-queue.csv",
            "review_collection_metadata_and_keep_unclear_raw_images_outside_git",
        ),
        make_row(
            "core-ready-008",
            "research_sources_and_bibliography",
            "Research source and bibliography infrastructure",
            "研究来源与书目基础设施",
            count_csv(root, "corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv"),
            source_staging_count,
            0,
            0,
            count_csv(root, "corpus/009_statistics-and-derived-features/009_ai-agent-source-route-review-queue.csv")
            + source_engineering_gap_queue_count
            + source_engineering_execution_matrix_count
            + source_engineering_gap_review_log_draft_count
            + source_engineering_gap_evidence_snapshot_count
            + source_engineering_next_action_checklist_count
            + source_engineering_next_action_result_scaffold_count
            + source_field_map_scaffold_count
            + source_field_map_review_checklist_count
            + source_field_map_review_result_scaffold_count
            + source_field_map_review_route_pack_count
            + source_package_manifest_review_route_pack_count
            + source_access_boundary_review_route_pack_count
            + source_checksum_review_route_pack_count
            + source_metadata_profile_review_route_pack_count
            + source_safe_derived_record_review_route_pack_count
            + source_engineering_review_route_summary_count
            + source_engineering_review_wave_handoff_scaffold_count
            + source_engineering_first_wave_review_result_count
            + source_engineering_first_wave_result_record_manifest_count
            + source_engineering_first_wave_followup_queue_count
            + source_engineering_first_wave_source_status_count
            + source_engineering_second_wave_source_checklist_count
            + source_engineering_second_wave_review_draft_manifest_count
            + source_engineering_second_wave_result_scaffold_count
            + source_engineering_second_wave_review_checklist_count
            + source_engineering_second_wave_review_outcome_scaffold_count
            + source_engineering_second_wave_outcome_route_pack_count
            + source_engineering_second_wave_outcome_handoff_scaffold_count
            + source_engineering_second_wave_handoff_review_checklist_count
            + source_engineering_second_wave_handoff_route_summary_count
            + source_pipeline_gap_matrix_count
            + source_pipeline_gap_review_checklist_count
            + source_pipeline_evidence_ledger_count
            + core_corpus_phase_coverage_count
            + source_pipeline_phase_coverage_count
            + source_pipeline_phase_action_queue_count
            + source_pipeline_phase_action_result_scaffold_count
            + source_pipeline_phase_action_route_summary_count
            + source_pipeline_phase_action_source_summary_count
            + source_pipeline_phase_action_file_checklist_count
            + source_pipeline_phase_action_evidence_presence_count
            + source_pipeline_phase_action_evidence_gap_summary_count
            + source_pipeline_phase_action_missing_evidence_action_queue_count
            + source_pipeline_phase_action_missing_evidence_result_scaffold_count
            + source_pipeline_phase_action_missing_evidence_route_summary_count
            + source_pipeline_phase_action_missing_evidence_source_summary_count
            + source_pipeline_phase_action_missing_evidence_review_draft_manifest_count
            + source_pipeline_phase_action_missing_evidence_review_result_scaffold_count
            + source_pipeline_phase_action_missing_evidence_review_checklist_count
            + source_pipeline_phase_action_missing_evidence_review_route_pack_count
            + source_pipeline_phase_action_missing_evidence_review_handoff_scaffold_count
            + source_pipeline_phase_action_missing_evidence_review_handoff_checklist_count
            + source_pipeline_phase_action_missing_evidence_review_handoff_route_summary_count,
            count_csv(root, "corpus/009_statistics-and-derived-features/009_ai-agent-source-route-review-queue.csv")
            + source_engineering_gap_queue_count
            + source_engineering_execution_matrix_count
            + source_engineering_gap_review_log_draft_count
            + source_engineering_gap_evidence_snapshot_count
            + source_engineering_next_action_checklist_count
            + source_engineering_next_action_result_scaffold_count
            + source_field_map_scaffold_count
            + source_field_map_review_checklist_count
            + source_field_map_review_result_scaffold_count
            + source_field_map_review_route_pack_count
            + source_package_manifest_review_route_pack_count
            + source_access_boundary_review_route_pack_count
            + source_checksum_review_route_pack_count
            + source_metadata_profile_review_route_pack_count
            + source_safe_derived_record_review_route_pack_count
            + source_engineering_review_route_summary_count
            + source_engineering_review_wave_handoff_scaffold_count
            + source_engineering_first_wave_review_result_count
            + source_engineering_first_wave_result_record_manifest_count
            + source_engineering_first_wave_followup_queue_count
            + source_engineering_first_wave_source_status_count
            + source_engineering_second_wave_source_checklist_count
            + source_engineering_second_wave_review_draft_manifest_count
            + source_engineering_second_wave_result_scaffold_count
            + source_engineering_second_wave_review_checklist_count
            + source_engineering_second_wave_review_outcome_scaffold_count
            + source_engineering_second_wave_outcome_route_pack_count
            + source_engineering_second_wave_outcome_handoff_scaffold_count
            + source_engineering_second_wave_handoff_review_checklist_count
            + source_engineering_second_wave_handoff_route_summary_count
            + source_pipeline_gap_matrix_count
            + source_pipeline_gap_review_checklist_count
            + source_pipeline_evidence_ledger_count
            + core_corpus_phase_coverage_count
            + source_pipeline_phase_coverage_count
            + source_pipeline_phase_action_queue_count
            + source_pipeline_phase_action_result_scaffold_count
            + source_pipeline_phase_action_route_summary_count
            + source_pipeline_phase_action_source_summary_count
            + source_pipeline_phase_action_file_checklist_count
            + source_pipeline_phase_action_evidence_presence_count
            + source_pipeline_phase_action_evidence_gap_summary_count
            + source_pipeline_phase_action_missing_evidence_action_queue_count
            + source_pipeline_phase_action_missing_evidence_result_scaffold_count
            + source_pipeline_phase_action_missing_evidence_route_summary_count
            + source_pipeline_phase_action_missing_evidence_source_summary_count
            + source_pipeline_phase_action_missing_evidence_review_draft_manifest_count
            + source_pipeline_phase_action_missing_evidence_review_result_scaffold_count
            + source_pipeline_phase_action_missing_evidence_review_checklist_count
            + source_pipeline_phase_action_missing_evidence_review_route_pack_count
            + source_pipeline_phase_action_missing_evidence_review_handoff_scaffold_count
            + source_pipeline_phase_action_missing_evidence_review_handoff_checklist_count
            + source_pipeline_phase_action_missing_evidence_review_handoff_route_summary_count
            + source_pipeline_phase_action_missing_evidence_review_outcome_scaffold_count,
            "corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv",
            SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_SCAFFOLD,
            "open_source_pipeline_phase_action_missing_evidence_review_outcome_scaffold_then_record_human_gated_source_outcomes",
        ),
        make_row(
            "core-ready-009",
            "relationship_graph_and_statistics",
            "Relationship graph and derived statistics",
            "关系图与派生统计",
            count_csv(root, "corpus/009_statistics-and-derived-features/001_relationship-graph-edge-type-summary.csv")
            + count_csv(root, "corpus/009_statistics-and-derived-features/002_relationship-graph-node-degree-summary.csv"),
            count_statistics_outputs(root),
            0,
            graph_edge_total,
            count_csv(root, "corpus/009_statistics-and-derived-features/012_ai-agent-graph-source-cross-review-queue.csv"),
            count_csv(root, "corpus/009_statistics-and-derived-features/012_ai-agent-graph-source-cross-review-queue.csv"),
            "corpus/008_relationship-graph/",
            "corpus/009_statistics-and-derived-features/012_ai-agent-graph-source-cross-review-queue.csv",
            "review_graph_edges_as_candidate_routing_edges_before_any_semantic_promotion",
        ),
        make_row(
            "core-ready-010",
            "published_research_notes",
            "Published-scholarship and bibliography note scaffolds",
            "已发表研究与书目笔记骨架",
            research_note_count,
            count_files(root, "research/**/*.md"),
            0,
            0,
            count_files(root, "doc/public/user_research/**/*.md"),
            count_files(root, "doc/public/user_research/**/*.md"),
            "research/",
            "doc/public/user_research/",
            "rewrite_only_reviewed_source_marked_drafts_into_research_notes",
        ),
    ]
    return rows


def build_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    stage_counts = Counter(row["readiness_stage"] for row in rows)
    priority_counts = Counter(row["review_priority"] for row in rows)
    totals = Counter()
    for row in rows:
        for field in [
            "formal_record_count",
            "staging_record_count",
            "candidate_record_count",
            "graph_edge_count",
            "review_queue_count",
            "manual_review_backlog_count",
        ]:
            totals[field] += int(row[field])
    return {
        "summary_id": "manual-review-backlog-summary-001",
        "updated_at": UPDATED_AT,
        "matrix_csv_path": OUTPUT_CSV.as_posix(),
        "core_area_count": len(rows),
        "readiness_stage_counts": dict(sorted(stage_counts.items())),
        "review_priority_counts": dict(sorted(priority_counts.items())),
        "totals": dict(sorted(totals.items())),
        "completion_boundary": (
            "This summary is a preprocessing readiness and manual-review backlog "
            "index. It does not start formal decipherment research or confirm "
            "candidate scholarship."
        ),
        "totals_note": (
            "Totals are row-sums across readiness areas and may include shared "
            "derivatives exposed through both corpus-specific rows and the graph/statistics row."
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
    rows = build_readiness_rows(root)
    write_csv(root / args.csv_output, rows)
    write_json(root / args.json_output, build_summary(rows))
    print(f"core_readiness_rows={len(rows)} csv={args.csv_output} json={args.json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
