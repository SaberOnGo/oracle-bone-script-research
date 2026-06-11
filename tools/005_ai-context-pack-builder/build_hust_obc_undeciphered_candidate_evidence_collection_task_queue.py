#!/usr/bin/env python3
"""Build not-started evidence-collection tasks for HUST-OBC undeciphered candidates."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SCAFFOLD_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/"
    "061_ai-agent-hust-obc-undeciphered-candidate-evidence-pack-scaffold-manifest.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "062_ai-agent-hust-obc-undeciphered-candidate-evidence-collection-task-queue.csv"
)
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_candidate_evidence_collection_task_queue_not_scholarship"
OUTPUT_SCOPE = "route_to_future_source_marked_evidence_collection_only"
TASK_STATUS = "not_started"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "not_started"
FORMAL_SCHEMA_COMPATIBILITY_STATUS = "not_formal_obs_char_schema"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
NO_CLAIM = "no_claim"
CAUTION = (
    "This row is an evidence-collection task only for a HUST-OBC undeciphered "
    "candidate scaffold. It is not collected evidence, not an accepted glyph "
    "identity, not a formal obs-char assignment, not a reading, not a component "
    "or evolution-chain assignment, not a rights decision, not a source promotion, "
    "and not a decipherment conclusion."
)

SECTION_SCOPES = {
    "character_or_unknown_glyph_id": "verify_unknown_candidate_id_external_ref_and_local_candidate_packet",
    "source_references_and_asset_metadata": "collect_source_register_download_log_large_source_and_candidate_packet_metadata",
    "full_inscription_context": "find_and_collect_source_marked_inscription_or_catalog_context_when_available",
    "neighboring_characters": "collect_source_marked_neighboring_character_context_when_available",
    "component_breakdown_and_variant_notes": "collect_existing_source_marked_component_or_variant_notes_without_new_breakdown",
    "excavation_period_and_catalog_provenance": "collect_catalog_collection_excavation_period_and_provenance_metadata",
    "bronze_seal_or_modern_comparanda": "collect_existing_bronze_seal_or_modern_comparanda_sources_without_claiming_correspondence",
    "supporting_evidence": "collect_source_marked_supporting_evidence_after_primary_context_is_found",
    "opposing_evidence": "collect_source_marked_opposing_or_conflicting_evidence_after_primary_context_is_found",
    "open_questions_and_next_checks": "record_missing_sources_blockers_and_next_verification_steps",
    "review_log": "record_human_or_agent_review_notes_under_user_research_without_scholarship_promotion",
}

SECTION_ROUTE_HINTS = {
    "character_or_unknown_glyph_id": [
        "open_061_scaffold_row",
        "open_candidate_packet",
        "open_bucket_manifest",
    ],
    "source_references_and_asset_metadata": [
        "open_056_057_058_059_capture_rows",
        "open_candidate_packet",
        "open_bucket_manifest",
    ],
    "full_inscription_context": [
        "search_registered_catalog_sources_for_inscription_context",
        "open_candidate_packet_source_image_refs",
    ],
    "neighboring_characters": [
        "search_registered_catalog_sources_for_same_inscription_neighbors",
        "open_candidate_packet_source_image_refs",
    ],
    "component_breakdown_and_variant_notes": [
        "search_registered_component_and_variant_sources",
        "do_not_create_unsourced_component_split",
    ],
    "excavation_period_and_catalog_provenance": [
        "search_collection_catalog_and_large_source_register_routes",
        "separate_collection_catalog_and_excavation_provenance",
    ],
    "bronze_seal_or_modern_comparanda": [
        "search_registered_bronze_seal_modern_correspondence_sources",
        "do_not_claim_correspondence_without_source",
    ],
    "supporting_evidence": [
        "collect_only_after_primary_source_context_exists",
        "separate_dataset_label_from_evidence",
    ],
    "opposing_evidence": [
        "collect_conflicting_or_absent_evidence_when_found",
        "separate_dataset_label_from_evidence",
    ],
    "open_questions_and_next_checks": [
        "record_missing_sources",
        "record_required_cross_checks",
    ],
    "review_log": [
        "open_052_review_log_draft",
        "record_no_identity_or_decipherment_decision",
    ],
}

OUTPUT_FIELDS = [
    "evidence_collection_task_id",
    "evidence_pack_scaffold_id",
    "readiness_check_id",
    "route_result_id",
    "review_log_draft_id",
    "undeciphered_review_task_id",
    "context_pack_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "target_evidence_section",
    "collection_scope",
    "route_hints",
    "route_files_to_open",
    "candidate_packet_capture_result_id",
    "source_register_capture_result_id",
    "download_log_capture_result_id",
    "large_source_register_capture_result_id",
    "expected_output_path",
    "route_file_count",
    "prerequisite_status",
    "task_status",
    "evidence_collection_status",
    "human_review_status",
    "formal_schema_compatibility_status",
    "identity_claim_status",
    "assignment_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
    "rights_decision_status",
    "source_promotion_status",
    "research_boundary",
    "output_scope",
    "required_next_checks",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _split_compact(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def _section_slug(section: str) -> str:
    return section.replace("_", "-")


def _expected_output_path(task_id: str, unknown_candidate_id: str, external_ref_id: str, section: str) -> str:
    return (
        "doc/public/user_research/006_undeciphered-candidate-evidence-collection-tasks/"
        f"{unknown_candidate_id}_{external_ref_id}/{task_id}_{_section_slug(section)}_collection-note.md"
    )


def _route_files(row: dict[str, str], section: str) -> list[str]:
    base_files = [
        SCAFFOLD_MANIFEST.as_posix(),
        row["review_log_draft_path"],
        row["candidate_packet_path"],
        row["bucket_manifest_path"],
    ]
    capture_files = [
        "corpus/009_statistics-and-derived-features/056_ai-agent-hust-obc-undeciphered-candidate-source-register-capture-results.csv",
        "corpus/009_statistics-and-derived-features/057_ai-agent-hust-obc-undeciphered-candidate-download-log-capture-results.csv",
        "corpus/009_statistics-and-derived-features/058_ai-agent-hust-obc-undeciphered-candidate-large-source-register-capture-results.csv",
        "corpus/009_statistics-and-derived-features/059_ai-agent-hust-obc-undeciphered-candidate-packet-capture-results.csv",
        "corpus/009_statistics-and-derived-features/060_ai-agent-hust-obc-undeciphered-candidate-evidence-readiness-checklist.csv",
    ]
    source_registers = [
        "corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv",
        "project_registry/006_large-source-register/001_large-source-register.csv",
    ]
    if section in {"character_or_unknown_glyph_id", "review_log"}:
        return base_files
    if section == "source_references_and_asset_metadata":
        return base_files + capture_files + source_registers
    if section in {
        "full_inscription_context",
        "neighboring_characters",
        "excavation_period_and_catalog_provenance",
        "bronze_seal_or_modern_comparanda",
        "supporting_evidence",
        "opposing_evidence",
        "open_questions_and_next_checks",
    }:
        return base_files + source_registers
    if section == "component_breakdown_and_variant_notes":
        return base_files + [
            "corpus/003_graphemic-components/000_component-registers/001_all-components-index.csv",
            "corpus/008_relationship-graph/004_graph-edges.jsonl",
        ]
    raise ValueError(f"unsupported evidence section: {section}")


def _require_scaffold(row: dict[str, str]) -> None:
    required = {
        "metadata_capture_status": "ready_metadata_only",
        "evidence_pack_status": "empty_scaffold_not_started",
        "evidence_collection_status": "not_collected",
        "formal_schema_compatibility_status": "not_formal_obs_char_schema",
        "identity_claim_status": "no_identity_claim",
        "assignment_status": "unknown_candidate_id_not_formal_obs_char_assignment",
    }
    for field, expected in required.items():
        if row[field] != expected:
            raise ValueError(f"unexpected {field} for {row['evidence_pack_scaffold_id']}: {row[field]}")


def build_task_rows(scaffold_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for scaffold_row in scaffold_rows:
        _require_scaffold(scaffold_row)
        sections = _split_compact(scaffold_row["required_evidence_sections"])
        for section in sections:
            task_id = f"hust-obc-undeciphered-evidence-task-{len(rows) + 1:04d}"
            route_files = _route_files(scaffold_row, section)
            rows.append(
                {
                    "evidence_collection_task_id": task_id,
                    "evidence_pack_scaffold_id": scaffold_row["evidence_pack_scaffold_id"],
                    "readiness_check_id": scaffold_row["readiness_check_id"],
                    "route_result_id": scaffold_row["route_result_id"],
                    "review_log_draft_id": scaffold_row["review_log_draft_id"],
                    "undeciphered_review_task_id": scaffold_row["undeciphered_review_task_id"],
                    "context_pack_id": scaffold_row["context_pack_id"],
                    "unknown_candidate_id": scaffold_row["unknown_candidate_id"],
                    "primary_external_ref_id": scaffold_row["primary_external_ref_id"],
                    "target_evidence_section": section,
                    "collection_scope": SECTION_SCOPES[section],
                    "route_hints": ";".join(SECTION_ROUTE_HINTS[section]),
                    "route_files_to_open": ";".join(route_files),
                    "candidate_packet_capture_result_id": scaffold_row["candidate_packet_capture_result_id"],
                    "source_register_capture_result_id": scaffold_row["source_register_capture_result_id"],
                    "download_log_capture_result_id": scaffold_row["download_log_capture_result_id"],
                    "large_source_register_capture_result_id": scaffold_row["large_source_register_capture_result_id"],
                    "expected_output_path": _expected_output_path(
                        task_id,
                        scaffold_row["unknown_candidate_id"],
                        scaffold_row["primary_external_ref_id"],
                        section,
                    ),
                    "route_file_count": str(len(route_files)),
                    "prerequisite_status": "ready_from_061_scaffold_manifest",
                    "task_status": TASK_STATUS,
                    "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                    "human_review_status": HUMAN_REVIEW_STATUS,
                    "formal_schema_compatibility_status": FORMAL_SCHEMA_COMPATIBILITY_STATUS,
                    "identity_claim_status": IDENTITY_CLAIM_STATUS,
                    "assignment_status": ASSIGNMENT_STATUS,
                    "decipherment_claim_status": NO_CLAIM,
                    "component_claim_status": NO_CLAIM,
                    "evolution_chain_claim_status": NO_CLAIM,
                    "rights_decision_status": scaffold_row["rights_decision_status"],
                    "source_promotion_status": scaffold_row["source_promotion_status"],
                    "research_boundary": RESEARCH_BOUNDARY,
                    "output_scope": OUTPUT_SCOPE,
                    "required_next_checks": (
                        "open_062_task_row;open_061_scaffold_row;open_route_files;"
                        "record_source_marked_evidence_only_after_verification"
                    ),
                    "caution": CAUTION,
                    "updated_at": UPDATED_AT,
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scaffold-manifest", default=str(SCAFFOLD_MANIFEST))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_task_rows(read_csv_rows(root / args.scaffold_manifest))
    write_csv(root / args.output, rows)
    print(
        f"evidence_collection_task_count={len(rows)} "
        f"not_collected_count={sum(row['evidence_collection_status'] == EVIDENCE_COLLECTION_STATUS for row in rows)} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
