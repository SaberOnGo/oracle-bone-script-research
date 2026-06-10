#!/usr/bin/env python3
"""Build a review queue for graph-source evidence collection result scaffolds."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


RESULT_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "027_ai-agent-graph-source-evidence-collection-result-scaffold.csv"
)
REVIEW_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/"
    "028_ai-agent-graph-source-evidence-collection-review-queue.csv"
)
UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "evidence_collection_review_queue_not_scholarship"
OUTPUT_SCOPE = "graph_source_evidence_collection_review_queue_only"
CAUTION = (
    "This row is an AI Agent evidence-collection review queue item only. "
    "Open the result scaffold row, note draft, route pack, manifest, and route files "
    "before recording any evidence. Do not use this queue as collected evidence, "
    "a rights decision, a source promotion decision, a component or evolution-chain "
    "assignment, or a decipherment conclusion."
)

SECTION_PRIORITY = {
    "source_register": 1,
    "download_log": 2,
    "package_manifest": 3,
    "metadata_profile": 4,
    "rights_risk_review": 5,
    "graph_edges": 6,
    "staging_row": 7,
    "counter_source_lookup": 8,
    "review_log": 9,
}

SECTION_REVIEW_CHECKS = {
    "source_register": [
        "open_source_register_row_before_copying_provenance",
        "record_source_id_external_ref_and_review_status_only",
    ],
    "download_log": [
        "open_download_log_before_recording_access_or_checksum_status",
        "do_not_infer_rights_from_download_success",
    ],
    "package_manifest": [
        "open_package_manifest_before_recording_file_size_or_checksum",
        "keep_raw_package_storage_boundary_explicit",
    ],
    "metadata_profile": [
        "open_metadata_profile_before_recording_metric_or_field_counts",
        "keep_metadata_extraction_separate_from_source_promotion",
    ],
    "graph_edges": [
        "open_graph_edge_files_before_recording_edge_evidence",
        "do_not_promote_edges_to_component_or_evolution_assignments",
    ],
    "staging_row": [
        "open_candidate_or_staging_rows_before_recording_dataset_fields",
        "keep_dataset_labels_as_candidates",
    ],
    "counter_source_lookup": [
        "open_counter_source_rows_before_recording_cross_source_notes",
        "do_not_claim_identity_match_from_lookup_queue",
    ],
    "rights_risk_review": [
        "open_rights_and_risk_route_files_before_recording_status",
        "do_not_turn_review_queue_into_rights_decision",
    ],
    "review_log": [
        "open_prior_review_logs_before_recording_human_or_agent_review_notes",
        "do_not_promote_review_notes_without_source_marked_evidence",
    ],
}

OUTPUT_FIELDS = [
    "evidence_collection_review_task_id",
    "evidence_collection_result_id",
    "evidence_collection_note_draft_id",
    "evidence_collection_task_id",
    "context_pack_id",
    "source_id",
    "primary_review_record_id",
    "primary_external_ref_id",
    "source_record_id",
    "target_evidence_section",
    "priority_rank",
    "priority_tags",
    "required_collection_action",
    "required_review_checks",
    "result_scaffold_path",
    "note_draft_path",
    "route_pack_path",
    "manifest_path",
    "task_queue_source_path",
    "route_files_to_open",
    "counter_source_ids_to_check",
    "result_update_target_path",
    "assignment_status",
    "review_status",
    "evidence_collection_status",
    "source_promotion_status",
    "decipherment_claim_status",
    "research_boundary",
    "output_scope",
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


def _join_unique(values: list[str]) -> str:
    unique_values: list[str] = []
    for value in values:
        if value and value not in unique_values:
            unique_values.append(value)
    return ";".join(unique_values)


def _priority_rank(section: str) -> int:
    return SECTION_PRIORITY.get(section, len(SECTION_PRIORITY) + 1)


def _priority_tags(section: str, source_id: str) -> list[str]:
    tags = [f"section:{section}", f"source:{source_id}"]
    if section in {"source_register", "download_log", "package_manifest", "metadata_profile"}:
        tags.append("provenance_first")
    if section == "rights_risk_review":
        tags.append("rights_boundary")
    if section in {"graph_edges", "staging_row", "counter_source_lookup"}:
        tags.append("cross_source_candidate_check")
    if section == "review_log":
        tags.append("review_trace")
    return tags


def _required_review_checks(section: str) -> list[str]:
    checks = SECTION_REVIEW_CHECKS.get(section, ["open_route_files_before_recording_notes"])
    return checks + [
        "keep_result_row_not_collected_until_evidence_is_source_marked",
        "do_not_write_ai_hypothesis_as_scholarship",
    ]


def build_review_rows(result_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, result in enumerate(result_rows, start=1):
        section = result["target_evidence_section"]
        source_id = result["source_id"]
        route_files = _join_unique(
            [
                result["route_pack_path"],
                result["manifest_path"],
                result["task_queue_source_path"],
                result["note_draft_path"],
                *_split_compact(result["route_files_to_open"]),
            ]
        )
        rows.append(
            {
                "evidence_collection_review_task_id": f"graph-source-evidence-review-{index:03d}",
                "evidence_collection_result_id": result["evidence_collection_result_id"],
                "evidence_collection_note_draft_id": result["evidence_collection_note_draft_id"],
                "evidence_collection_task_id": result["evidence_collection_task_id"],
                "context_pack_id": result["context_pack_id"],
                "source_id": source_id,
                "primary_review_record_id": result["primary_review_record_id"],
                "primary_external_ref_id": result["primary_external_ref_id"],
                "source_record_id": result["source_record_id"],
                "target_evidence_section": section,
                "priority_rank": str(_priority_rank(section)),
                "priority_tags": ";".join(_priority_tags(section, source_id)),
                "required_collection_action": result["required_collection_action"],
                "required_review_checks": ";".join(_required_review_checks(section)),
                "result_scaffold_path": RESULT_SCAFFOLD.as_posix(),
                "note_draft_path": result["note_draft_path"],
                "route_pack_path": result["route_pack_path"],
                "manifest_path": result["manifest_path"],
                "task_queue_source_path": result["task_queue_source_path"],
                "route_files_to_open": route_files,
                "counter_source_ids_to_check": result["counter_source_ids_to_check"],
                "result_update_target_path": RESULT_SCAFFOLD.as_posix(),
                "assignment_status": "unassigned",
                "review_status": "needs_evidence_collection_review",
                "evidence_collection_status": result["evidence_collection_status"],
                "source_promotion_status": result["source_promotion_status"],
                "decipherment_claim_status": result["decipherment_claim_status"],
                "research_boundary": RESEARCH_BOUNDARY,
                "output_scope": OUTPUT_SCOPE,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result-scaffold", default=str(RESULT_SCAFFOLD))
    parser.add_argument("--output", default=str(REVIEW_QUEUE))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_review_rows(read_csv_rows(root / args.result_scaffold))
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
