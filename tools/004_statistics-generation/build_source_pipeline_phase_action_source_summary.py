#!/usr/bin/env python3
"""Build a source-level summary for source pipeline phase action routes."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/140_source-pipeline-phase-action-source-summary.csv")
SOURCE_PIPELINE_PHASE_ACTION_ROUTE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/139_source-pipeline-phase-action-route-summary.json"
)
UPDATED_AT = "2026-06-19"
ROUTE_STATUS = "not_started"
RESULT_STATUS = "not_started"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_source_summary_not_scholarship"
CAUTION = (
    "This source pipeline phase action source summary is routing-only. It is not "
    "collected evidence, not a reviewed outcome, not a rights decision, not "
    "source promotion, not a corpus import, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "source_summary_id",
    "source_id",
    "source_type",
    "rights_status",
    "pipeline_gap_status",
    "review_lanes",
    "phase_names",
    "route_count",
    "downloaded_count_max",
    "checksum_present_count_max",
    "package_manifest_count_max",
    "metadata_profile_count_max",
    "candidate_queue_count_total",
    "cross_source_crosswalk_match_count_total",
    "graph_edge_count_total",
    "route_ids",
    "result_scaffold_ids",
    "action_ids",
    "phase_row_ids",
    "action_types",
    "action_priorities",
    "route_files_to_open",
    "phase_evidence_paths",
    "source_route_summary_path",
    "action_result_scaffold_path",
    "route_status",
    "result_status",
    "evidence_collection_status",
    "reviewed_evidence_paths",
    "reviewed_outcome_summary",
    "remaining_blockers_reviewed",
    "required_followup_reviewed",
    "human_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_route_summary(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def split_semicolon(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def unique_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return ";".join(seen)


def sorted_unique_join(values: list[str]) -> str:
    return ";".join(sorted({value for value in values if value}))


def int_value(value: object) -> int:
    text = str(value)
    return int(text) if text else 0


def route_values(route: dict[str, object], field: str) -> list[str]:
    value = route.get(field, "")
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    return split_semicolon(str(value))


def build_source_summary_rows(route_summary: dict[str, object]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for route in route_summary.get("routes", []):
        if isinstance(route, dict):
            grouped[str(route["source_id"])].append(route)

    rows: list[dict[str, str]] = []
    for index, source_id in enumerate(sorted(grouped), start=1):
        routes = grouped[source_id]
        first = routes[0]
        route_files: list[str] = []
        phase_paths: list[str] = []
        for route in routes:
            route_files.extend(route_values(route, "route_files_to_open"))
            phase_paths.extend(route_values(route, "phase_evidence_paths"))

        rows.append(
            {
                "source_summary_id": f"source-pipeline-phase-action-source-summary-{index:03d}",
                "source_id": source_id,
                "source_type": str(first["source_type"]),
                "rights_status": str(first["rights_status"]),
                "pipeline_gap_status": str(first["pipeline_gap_status"]),
                "review_lanes": sorted_unique_join([str(route["review_lane"]) for route in routes]),
                "phase_names": sorted_unique_join([str(route["phase_name"]) for route in routes]),
                "route_count": str(len(routes)),
                "downloaded_count_max": str(max(int_value(route.get("downloaded_count", "0")) for route in routes)),
                "checksum_present_count_max": str(
                    max(int_value(route.get("checksum_present_count", "0")) for route in routes)
                ),
                "package_manifest_count_max": str(
                    max(int_value(route.get("package_manifest_count", "0")) for route in routes)
                ),
                "metadata_profile_count_max": str(
                    max(int_value(route.get("metadata_profile_count", "0")) for route in routes)
                ),
                "candidate_queue_count_total": str(
                    sum(int_value(route.get("candidate_queue_count", "0")) for route in routes)
                ),
                "cross_source_crosswalk_match_count_total": str(
                    sum(int_value(route.get("cross_source_crosswalk_match_count", "0")) for route in routes)
                ),
                "graph_edge_count_total": str(sum(int_value(route.get("graph_edge_count", "0")) for route in routes)),
                "route_ids": unique_join([str(route["route_id"]) for route in routes]),
                "result_scaffold_ids": unique_join([str(route["result_scaffold_id"]) for route in routes]),
                "action_ids": unique_join([str(route["action_id"]) for route in routes]),
                "phase_row_ids": unique_join([str(route["phase_row_id"]) for route in routes]),
                "action_types": sorted_unique_join([str(route["action_type"]) for route in routes]),
                "action_priorities": sorted_unique_join([str(route["action_priority"]) for route in routes]),
                "route_files_to_open": unique_join(route_files),
                "phase_evidence_paths": unique_join(phase_paths),
                "source_route_summary_path": SOURCE_PIPELINE_PHASE_ACTION_ROUTE_SUMMARY.as_posix(),
                "action_result_scaffold_path": str(first["action_result_scaffold_path"]),
                "route_status": ROUTE_STATUS,
                "result_status": RESULT_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "reviewed_evidence_paths": "",
                "reviewed_outcome_summary": "",
                "remaining_blockers_reviewed": unique_join(
                    [str(route.get("remaining_blockers_reviewed", "")) for route in routes]
                ),
                "required_followup_reviewed": "",
                "human_review_status": HUMAN_REVIEW_STATUS,
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "corpus_import_status": CORPUS_IMPORT_STATUS,
                "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--route-summary", default=str(SOURCE_PIPELINE_PHASE_ACTION_ROUTE_SUMMARY))
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_source_summary_rows(read_route_summary(root / args.route_summary))
    write_csv(root / args.csv_output, rows)
    print(f"source_pipeline_phase_action_source_summary_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
