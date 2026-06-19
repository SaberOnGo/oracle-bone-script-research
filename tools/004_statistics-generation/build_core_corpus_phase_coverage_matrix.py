#!/usr/bin/env python3
"""Build a core-corpus preprocessing phase coverage matrix.

The matrix translates existing audits into the phase vocabulary used by the
project goal: discovered, downloaded, registered, unpacked, extracted, cleaned,
structured, linked, verified, and pending human review. It is a navigation and
gap surface only, not a scholarly result.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/135_core-corpus-phase-coverage-matrix.csv")
PREPROCESSING_STATUS_AUDIT = Path("corpus/009_statistics-and-derived-features/090_preprocessing-status-audit.csv")
CORE_CORPUS_READINESS_MATRIX = Path("corpus/009_statistics-and-derived-features/096_core-corpus-readiness-matrix.csv")
SOURCE_PIPELINE_EVIDENCE_LEDGER = Path(
    "corpus/009_statistics-and-derived-features/134_ai-agent-source-pipeline-evidence-ledger.csv"
)
SOURCE_PIPELINE_PHASE_COVERAGE_MATRIX = Path(
    "corpus/009_statistics-and-derived-features/136_source-pipeline-phase-coverage-matrix.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/137_source-pipeline-phase-action-queue.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_RESULT_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/138_source-pipeline-phase-action-result-scaffold.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_ROUTE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/139_source-pipeline-phase-action-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_SOURCE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/140_source-pipeline-phase-action-source-summary.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_FILE_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/141_source-pipeline-phase-action-file-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_PRESENCE_MATRIX = Path(
    "corpus/009_statistics-and-derived-features/142_source-pipeline-phase-action-evidence-presence-matrix.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_GAP_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/143_source-pipeline-phase-action-evidence-gap-summary.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ACTION_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/144_source-pipeline-phase-action-missing-evidence-action-queue.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_RESULT_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/145_source-pipeline-phase-action-missing-evidence-result-scaffold.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ROUTE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/146_source-pipeline-phase-action-missing-evidence-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_SOURCE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/147_source-pipeline-phase-action-missing-evidence-source-summary.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_DRAFT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/148_source-pipeline-phase-action-missing-evidence-review-draft-manifest.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_RESULT_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/149_source-pipeline-phase-action-missing-evidence-result-scaffold.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/150_source-pipeline-phase-action-missing-evidence-review-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_ROUTE_PACK = Path(
    "corpus/009_statistics-and-derived-features/151_source-pipeline-phase-action-missing-evidence-review-route-pack.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/152_source-pipeline-phase-action-missing-evidence-review-handoff-scaffold.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/153_source-pipeline-phase-action-missing-evidence-review-handoff-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_ROUTE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/154_source-pipeline-phase-action-missing-evidence-review-handoff-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/155_source-pipeline-phase-action-missing-evidence-review-outcome-scaffold.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ROUTE_PACK = Path(
    "corpus/009_statistics-and-derived-features/156_source-pipeline-phase-action-missing-evidence-review-outcome-route-pack.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/157_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-scaffold.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/158_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/159_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ASSIGNMENT_PLAN = Path(
    "corpus/009_statistics-and-derived-features/160_source-pipeline-phase-action-missing-evidence-review-outcome-assignment-plan.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/161_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-scaffold.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/162_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ROUTE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/163_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_PLAN = Path(
    "corpus/009_statistics-and-derived-features/164_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-plan.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/165_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/166_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-scaffold.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_ROUTE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/167_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/168_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-summary.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/169_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_ROUTE_PACK = Path(
    "corpus/009_statistics-and-derived-features/170_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-route-pack.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/171_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-scaffold.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/172_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_ROUTE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/173_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/174_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-scaffold.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_ROUTE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/175_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/176_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST_ROUTE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/177_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST_OUTCOME_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/178_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-scaffold.csv"
)
UPDATED_AT = "2026-06-19"
CLAIM_BOUNDARY = "core_corpus_phase_coverage_not_review_outcome_not_scholarship"
CAUTION = (
    "Core corpus preprocessing phase coverage only; statuses summarize existing engineering "
    "evidence and do not decide rights, import corpus records, promote candidates, or make "
    "decipherment claims."
)

PHASES = [
    "discovered",
    "downloaded",
    "registered",
    "unpacked",
    "extracted",
    "cleaned",
    "structured",
    "linked",
    "verified",
    "pending_human_review",
]

AREA_TO_AUDIT_TYPE = {
    "oracle_characters": "oracle_character_candidates",
    "undeciphered_oracle_character_candidates": "undeciphered_character_candidates",
    "cross_source_codepoint_routes": "oracle_character_candidates",
    "graphemic_components": "components_and_glyph_links",
    "evolution_correspondences": "evolution_correspondence_candidates",
    "inscriptions_and_plate_crosswalks": "inscription_and_collection_staging",
    "collection_provenance_assets": "inscription_and_collection_staging",
    "research_sources_and_bibliography": "source_registry",
    "relationship_graph_and_statistics": "relationship_graph",
    "published_research_notes": "review_queues",
}

BOUNDARY_BY_AREA = {
    "oracle_characters": "candidate_not_promoted",
    "undeciphered_oracle_character_candidates": "candidate_not_promoted",
    "cross_source_codepoint_routes": "candidate_crosswalk_not_identity_claim",
    "graphemic_components": "candidate_component_graph_not_formal_component",
    "evolution_correspondences": "candidate_evolution_graph_not_formal_correspondence",
    "inscriptions_and_plate_crosswalks": "staging_crosswalk_not_formal_inscription",
    "collection_provenance_assets": "metadata_or_reviewed_asset_not_raw_import",
    "research_sources_and_bibliography": "source_metadata_not_rights_decision",
    "relationship_graph_and_statistics": "candidate_graph_edges_not_semantic_promotion",
    "published_research_notes": "draft_or_bibliography_review_queue",
}

PHASE_OVERRIDES = {
    "oracle_characters": {
        "downloaded": "present",
        "registered": "present",
        "unpacked": "present",
        "extracted": "present",
        "cleaned": "present",
        "structured": "present",
        "linked": "present",
        "verified": "missing",
        "pending_human_review": "present",
    },
    "undeciphered_oracle_character_candidates": {
        "downloaded": "present",
        "registered": "present",
        "unpacked": "present",
        "extracted": "present",
        "cleaned": "present",
        "structured": "present",
        "linked": "missing",
        "verified": "missing",
        "pending_human_review": "present",
    },
    "cross_source_codepoint_routes": {
        "downloaded": "present",
        "registered": "present",
        "unpacked": "present",
        "extracted": "present",
        "cleaned": "present",
        "structured": "present",
        "linked": "present",
        "verified": "missing",
        "pending_human_review": "present",
    },
    "graphemic_components": {
        "downloaded": "present",
        "registered": "present",
        "unpacked": "present",
        "extracted": "present",
        "cleaned": "present",
        "structured": "present",
        "linked": "present",
        "verified": "missing",
        "pending_human_review": "present",
    },
    "evolution_correspondences": {
        "downloaded": "present",
        "registered": "present",
        "unpacked": "present",
        "extracted": "present",
        "cleaned": "present",
        "structured": "present",
        "linked": "present",
        "verified": "missing",
        "pending_human_review": "present",
    },
    "inscriptions_and_plate_crosswalks": {
        "downloaded": "mixed_or_partial",
        "registered": "present",
        "unpacked": "present",
        "extracted": "present",
        "cleaned": "present",
        "structured": "present",
        "linked": "present",
        "verified": "missing",
        "pending_human_review": "present",
    },
    "collection_provenance_assets": {
        "downloaded": "mixed_or_partial",
        "registered": "present",
        "unpacked": "present",
        "extracted": "present",
        "cleaned": "present",
        "structured": "present",
        "linked": "missing",
        "verified": "mixed_or_partial",
        "pending_human_review": "present",
    },
    "research_sources_and_bibliography": {
        "downloaded": "mixed_or_partial",
        "registered": "present",
        "unpacked": "mixed_or_partial",
        "extracted": "mixed_or_partial",
        "cleaned": "mixed_or_partial",
        "structured": "present",
        "linked": "present",
        "verified": "mixed_or_partial",
        "pending_human_review": "present",
    },
    "relationship_graph_and_statistics": {
        "downloaded": "not_applicable",
        "registered": "present",
        "unpacked": "not_applicable",
        "extracted": "present",
        "cleaned": "present",
        "structured": "present",
        "linked": "present",
        "verified": "present",
        "pending_human_review": "present",
    },
    "published_research_notes": {
        "downloaded": "not_applicable",
        "registered": "present",
        "unpacked": "not_applicable",
        "extracted": "mixed_or_partial",
        "cleaned": "mixed_or_partial",
        "structured": "present",
        "linked": "mixed_or_partial",
        "verified": "missing",
        "pending_human_review": "present",
    },
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def count_csv(root: Path, path: Path) -> int:
    return len(read_csv_rows(root / path))


def phase_status(area: str, phase: str, audit_stage: str, readiness: dict[str, str]) -> str:
    if phase == "discovered":
        return "present" if int(readiness["formal_record_count"]) + int(readiness["staging_record_count"]) + int(
            readiness["candidate_record_count"]
        ) + int(readiness["graph_edge_count"]) else "missing"
    override = PHASE_OVERRIDES.get(area, {}).get(phase)
    if override:
        return override
    if audit_stage == phase:
        return "present"
    return "missing"


def phase_evidence_paths(area: str, readiness: dict[str, str], audit: dict[str, str]) -> str:
    paths = [readiness["primary_entry_path"], readiness["review_queue_path"], audit["next_entry_path"]]
    if area == "research_sources_and_bibliography":
        paths.append(SOURCE_PIPELINE_EVIDENCE_LEDGER.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_COVERAGE_MATRIX.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_QUEUE.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_RESULT_SCAFFOLD.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_ROUTE_SUMMARY.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_SOURCE_SUMMARY.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_FILE_CHECKLIST.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_PRESENCE_MATRIX.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_GAP_SUMMARY.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ACTION_QUEUE.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_RESULT_SCAFFOLD.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ROUTE_SUMMARY.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_SOURCE_SUMMARY.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_DRAFT_MANIFEST.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_RESULT_SCAFFOLD.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_CHECKLIST.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_ROUTE_PACK.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_SCAFFOLD.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_CHECKLIST.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_ROUTE_SUMMARY.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_SCAFFOLD.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ROUTE_PACK.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_SCAFFOLD.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_CHECKLIST.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ASSIGNMENT_PLAN.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_SCAFFOLD.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_CHECKLIST.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ROUTE_SUMMARY.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_PLAN.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_CHECKLIST.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SCAFFOLD.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_ROUTE_SUMMARY.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_SUMMARY.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_CHECKLIST.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_ROUTE_PACK.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_SCAFFOLD.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_CHECKLIST.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_ROUTE_SUMMARY.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_SCAFFOLD.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_ROUTE_SUMMARY.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST_ROUTE_SUMMARY.as_posix())
        paths.append(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST_OUTCOME_SCAFFOLD.as_posix())
    unique_paths = []
    for path in paths:
        if path and path not in unique_paths:
            unique_paths.append(path)
    return ";".join(unique_paths)


def build_phase_rows(root: Path) -> list[dict[str, str]]:
    audit_rows = read_csv_rows(root / PREPROCESSING_STATUS_AUDIT)
    readiness_rows = read_csv_rows(root / CORE_CORPUS_READINESS_MATRIX)
    source_pipeline_evidence_rows = count_csv(root, SOURCE_PIPELINE_EVIDENCE_LEDGER)
    source_pipeline_phase_rows = count_csv(root, SOURCE_PIPELINE_PHASE_COVERAGE_MATRIX)
    source_pipeline_action_rows = count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_QUEUE)
    source_pipeline_action_result_rows = count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_RESULT_SCAFFOLD)
    source_pipeline_action_route_summary_files = 1 if (root / SOURCE_PIPELINE_PHASE_ACTION_ROUTE_SUMMARY).exists() else 0
    source_pipeline_action_source_summary_rows = count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_SOURCE_SUMMARY)
    source_pipeline_action_file_checklist_rows = count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_FILE_CHECKLIST)
    source_pipeline_action_evidence_presence_rows = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_PRESENCE_MATRIX
    )
    source_pipeline_action_evidence_gap_summary_rows = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_GAP_SUMMARY
    )
    source_pipeline_action_missing_evidence_action_queue_rows = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ACTION_QUEUE
    )
    source_pipeline_action_missing_evidence_result_scaffold_rows = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_RESULT_SCAFFOLD
    )
    source_pipeline_action_missing_evidence_route_summary_files = (
        1 if (root / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ROUTE_SUMMARY).exists() else 0
    )
    source_pipeline_action_missing_evidence_source_summary_rows = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_SOURCE_SUMMARY
    )
    source_pipeline_action_missing_evidence_review_draft_rows = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_DRAFT_MANIFEST
    )
    source_pipeline_action_missing_evidence_review_result_scaffold_rows = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_RESULT_SCAFFOLD
    )
    source_pipeline_action_missing_evidence_review_checklist_rows = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_CHECKLIST
    )
    source_pipeline_action_missing_evidence_review_route_pack_files = (
        1 if (root / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_ROUTE_PACK).exists() else 0
    )
    source_pipeline_action_missing_evidence_review_handoff_scaffold_files = (
        1 if (root / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_SCAFFOLD).exists() else 0
    )
    source_pipeline_action_missing_evidence_review_handoff_checklist_rows = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_CHECKLIST
    )
    source_pipeline_action_missing_evidence_review_handoff_route_summary_files = (
        1 if (root / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_ROUTE_SUMMARY).exists() else 0
    )
    source_pipeline_action_missing_evidence_review_outcome_scaffold_rows = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_SCAFFOLD
    )
    source_pipeline_action_missing_evidence_review_outcome_route_pack_files = (
        1 if (root / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ROUTE_PACK).exists() else 0
    )
    source_pipeline_action_missing_evidence_review_outcome_handoff_scaffold_files = (
        1 if (root / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_SCAFFOLD).exists() else 0
    )
    source_pipeline_action_missing_evidence_review_outcome_handoff_checklist_rows = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_CHECKLIST
    )
    source_pipeline_action_missing_evidence_review_outcome_handoff_route_summary_files = (
        1 if (root / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY).exists() else 0
    )
    source_pipeline_action_missing_evidence_review_outcome_assignment_plan_files = (
        1 if (root / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ASSIGNMENT_PLAN).exists() else 0
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_scaffold_files = (
        1 if (root / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_SCAFFOLD).exists() else 0
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_checklist_rows = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_CHECKLIST
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_route_summary_files = (
        1 if (root / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ROUTE_SUMMARY).exists() else 0
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_plan_files = (
        1 if (root / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_PLAN).exists() else 0
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_checklist_rows = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_CHECKLIST
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_scaffold_rows = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SCAFFOLD
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_route_summary_files = (
        1 if (root / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_ROUTE_SUMMARY).exists() else 0
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_summary_rows = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_SUMMARY
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_checklist_rows = count_csv(
        root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_CHECKLIST
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_route_pack_files = (
        1
        if (
            root
            / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_ROUTE_PACK
        ).exists()
        else 0
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_scaffold_files = (
        1
        if (
            root
            / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_SCAFFOLD
        ).exists()
        else 0
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_checklist_rows = count_csv(
        root,
        SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_CHECKLIST,
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_route_summary_files = (
        1
        if (
            root
            / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_ROUTE_SUMMARY
        ).exists()
        else 0
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_outcome_scaffold_rows = count_csv(
        root,
        SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_SCAFFOLD,
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_outcome_route_summary_files = (
        1
        if (
            root
            / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_ROUTE_SUMMARY
        ).exists()
        else 0
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_outcome_checklist_rows = count_csv(
        root,
        SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST,
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_outcome_checklist_route_summary_files = (
        1
        if (
            root
            / SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST_ROUTE_SUMMARY
        ).exists()
        else 0
    )
    source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_outcome_checklist_outcome_scaffold_rows = count_csv(
        root,
        SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_CHECKLIST_OUTCOME_SCAFFOLD,
    )
    audit_by_type = {row["area_type"]: row for row in audit_rows}

    rows: list[dict[str, str]] = []
    for index, readiness in enumerate(readiness_rows, start=1):
        area = readiness["corpus_area"]
        audit = audit_by_type[AREA_TO_AUDIT_TYPE[area]]
        phase_values = {
            f"{phase}_status": phase_status(area, phase, audit["current_stage"], readiness) for phase in PHASES
        }
        rows.append(
            {
                "phase_row_id": f"core-corpus-phase-{index:03d}",
                "corpus_area": area,
                "label_en": readiness["label_en"],
                "preprocessing_audit_area_type": audit["area_type"],
                "preprocessing_current_stage": audit["current_stage"],
                "readiness_stage": readiness["readiness_stage"],
                "review_priority": readiness["review_priority"],
                **phase_values,
                "formal_record_count": readiness["formal_record_count"],
                "staging_record_count": readiness["staging_record_count"],
                "candidate_record_count": readiness["candidate_record_count"],
                "graph_edge_count": readiness["graph_edge_count"],
                "review_queue_count": readiness["review_queue_count"],
                "source_pipeline_evidence_rows": str(
                    source_pipeline_evidence_rows
                    + source_pipeline_phase_rows
                    + source_pipeline_action_rows
                    + source_pipeline_action_result_rows
                    + source_pipeline_action_route_summary_files
                    + source_pipeline_action_source_summary_rows
                    + source_pipeline_action_file_checklist_rows
                    + source_pipeline_action_evidence_presence_rows
                    + source_pipeline_action_evidence_gap_summary_rows
                    + source_pipeline_action_missing_evidence_action_queue_rows
                    + source_pipeline_action_missing_evidence_result_scaffold_rows
                    + source_pipeline_action_missing_evidence_route_summary_files
                    + source_pipeline_action_missing_evidence_source_summary_rows
                    + source_pipeline_action_missing_evidence_review_draft_rows
                    + source_pipeline_action_missing_evidence_review_result_scaffold_rows
                    + source_pipeline_action_missing_evidence_review_checklist_rows
                    + source_pipeline_action_missing_evidence_review_route_pack_files
                    + source_pipeline_action_missing_evidence_review_handoff_scaffold_files
                    + source_pipeline_action_missing_evidence_review_handoff_checklist_rows
                    + source_pipeline_action_missing_evidence_review_handoff_route_summary_files
                    + source_pipeline_action_missing_evidence_review_outcome_scaffold_rows
                    + source_pipeline_action_missing_evidence_review_outcome_route_pack_files
                    + source_pipeline_action_missing_evidence_review_outcome_handoff_scaffold_files
                    + source_pipeline_action_missing_evidence_review_outcome_handoff_checklist_rows
                    + source_pipeline_action_missing_evidence_review_outcome_handoff_route_summary_files
                    + source_pipeline_action_missing_evidence_review_outcome_assignment_plan_files
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_scaffold_files
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_checklist_rows
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_route_summary_files
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_plan_files
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_checklist_rows
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_scaffold_rows
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_route_summary_files
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_summary_rows
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_checklist_rows
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_route_pack_files
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_scaffold_files
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_checklist_rows
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_route_summary_files
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_outcome_scaffold_rows
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_outcome_route_summary_files
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_outcome_checklist_rows
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_outcome_checklist_route_summary_files
                    + source_pipeline_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_outcome_checklist_outcome_scaffold_rows
                    if area == "research_sources_and_bibliography"
                    else 0
                ),
                "phase_evidence_paths": phase_evidence_paths(area, readiness, audit),
                "next_action": f"open_phase_evidence_then_{readiness['next_action']}",
                "candidate_or_staging_boundary": BOUNDARY_BY_AREA[area],
                "research_boundary_status": BOUNDARY_BY_AREA[area],
                "claim_boundary": CLAIM_BOUNDARY,
                "rights_decision_status": "no_new_rights_decision",
                "source_promotion_status": "not_promoted",
                "corpus_import_status": "not_imported",
                "decipherment_claim_status": "no_decipherment_claim",
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_phase_rows(root)
    write_csv(root / args.csv_output, rows)
    print(f"core_corpus_phase_coverage_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
