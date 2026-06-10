#!/usr/bin/env python3
"""Build empty result scaffolds for graph-source evidence collection routes."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROUTE_PACK = Path(
    "corpus/009_statistics-and-derived-features/"
    "026_ai-agent-graph-source-evidence-collection-route-pack.json"
)
RESULT_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "027_ai-agent-graph-source-evidence-collection-result-scaffold.csv"
)
UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "evidence_collection_result_scaffold_not_scholarship"
OUTPUT_SCOPE = "graph_source_evidence_collection_result_scaffold_only"
CAUTION = (
    "This row is an empty graph-source evidence collection result scaffold only. "
    "All evidence sections remain not_collected until an agent opens the note draft "
    "and cited route files. Do not use it as collected evidence, a rights decision, "
    "a source promotion decision, a component or evolution-chain assignment, "
    "or a decipherment conclusion."
)

SECTION_ACTIONS = {
    "source_register": "collect_source_register_provenance_fields",
    "download_log": "collect_download_log_status_size_checksum_access_notes",
    "package_manifest": "collect_package_manifest_file_size_checksum_and_storage_boundary",
    "metadata_profile": "collect_metadata_profile_fields_and_extraction_scope",
    "graph_edges": "collect_graph_edge_source_status_and_claim_boundary",
    "staging_row": "collect_staging_row_field_map_and_review_status",
    "counter_source_lookup": "collect_counter_source_lookup_notes_without_identity_claim",
    "rights_risk_review": "collect_rights_risk_notes_without_rights_decision",
    "review_log": "collect_review_log_notes_without_promotion_decision",
}

OUTPUT_FIELDS = [
    "evidence_collection_result_id",
    "evidence_collection_note_draft_id",
    "evidence_collection_task_id",
    "context_pack_id",
    "source_id",
    "primary_review_record_id",
    "primary_external_ref_id",
    "source_record_id",
    "target_evidence_section",
    "required_collection_action",
    "note_draft_path",
    "route_pack_path",
    "manifest_path",
    "task_queue_source_path",
    "route_files_to_open",
    "counter_source_ids_to_check",
    "result_status",
    "note_draft_open_status",
    "route_files_open_status",
    "evidence_collection_status",
    "source_register_evidence_status",
    "download_log_evidence_status",
    "package_manifest_evidence_status",
    "metadata_profile_evidence_status",
    "graph_edge_evidence_status",
    "staging_row_evidence_status",
    "counter_source_lookup_status",
    "rights_risk_review_status",
    "review_log_status",
    "source_promotion_status",
    "decipherment_claim_status",
    "next_artifact_recommendation",
    "research_boundary",
    "output_scope",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _join_compact(values: object) -> str:
    if not isinstance(values, list):
        return ""
    return ";".join(str(value) for value in values if value)


def build_result_rows(route_pack: dict[str, object]) -> list[dict[str, str]]:
    context_pack_id = str(route_pack["context_pack_id"])
    note_routes = route_pack.get("note_routes", [])
    if not isinstance(note_routes, list):
        raise ValueError("route pack note_routes must be a list")

    rows: list[dict[str, str]] = []
    for index, route in enumerate(note_routes, start=1):
        if not isinstance(route, dict):
            raise ValueError("route pack note route must be an object")
        target_section = str(route["target_evidence_section"])
        rows.append(
            {
                "evidence_collection_result_id": f"graph-source-evidence-result-{index:03d}",
                "evidence_collection_note_draft_id": str(
                    route["evidence_collection_note_draft_id"]
                ),
                "evidence_collection_task_id": str(route["evidence_collection_task_id"]),
                "context_pack_id": context_pack_id,
                "source_id": str(route["source_id"]),
                "primary_review_record_id": str(route["primary_review_record_id"]),
                "primary_external_ref_id": str(route["primary_external_ref_id"]),
                "source_record_id": str(route["source_record_id"]),
                "target_evidence_section": target_section,
                "required_collection_action": SECTION_ACTIONS.get(
                    target_section, "collect_section_evidence_without_promotion"
                ),
                "note_draft_path": str(route["note_draft_path"]),
                "route_pack_path": ROUTE_PACK.as_posix(),
                "manifest_path": str(route["manifest_path"]),
                "task_queue_source_path": str(route["task_queue_source_path"]),
                "route_files_to_open": _join_compact(route.get("route_files_to_open", [])),
                "counter_source_ids_to_check": _join_compact(
                    route.get("counter_source_ids_to_check", [])
                ),
                "result_status": "not_started",
                "note_draft_open_status": "not_opened",
                "route_files_open_status": "not_opened",
                "evidence_collection_status": "not_collected",
                "source_register_evidence_status": "not_collected",
                "download_log_evidence_status": "not_collected",
                "package_manifest_evidence_status": "not_collected",
                "metadata_profile_evidence_status": "not_collected",
                "graph_edge_evidence_status": "not_collected",
                "staging_row_evidence_status": "not_collected",
                "counter_source_lookup_status": "not_collected",
                "rights_risk_review_status": "not_collected",
                "review_log_status": "not_collected",
                "source_promotion_status": "not_promoted",
                "decipherment_claim_status": "no_claim",
                "next_artifact_recommendation": "not_collected",
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
    parser.add_argument("--route-pack", default=str(ROUTE_PACK))
    parser.add_argument("--output", default=str(RESULT_SCAFFOLD))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_result_rows(read_json(root / args.route_pack))
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
