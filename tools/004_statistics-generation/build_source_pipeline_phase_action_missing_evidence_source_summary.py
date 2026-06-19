#!/usr/bin/env python3
"""Build a source-level summary for missing source-evidence routes."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


OUTPUT_CSV = Path(
    "corpus/009_statistics-and-derived-features/"
    "147_source-pipeline-phase-action-missing-evidence-source-summary.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ROUTE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/"
    "146_source-pipeline-phase-action-missing-evidence-route-summary.json"
)
UPDATED_AT = "2026-06-19"
SOURCE_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_missing_evidence_source_summary_not_scholarship"
NEXT_REVIEW_ACTION = "open_missing_evidence_routes_for_source_and_record_human_gated_outcomes"
CAUTION = (
    "This source pipeline missing-evidence source summary is routing-only. It is "
    "not collected evidence, not a reviewed outcome, not a rights decision, not "
    "source promotion, not a corpus import, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "missing_evidence_source_summary_id",
    "source_id",
    "source_type",
    "rights_status",
    "pipeline_gap_status",
    "review_lanes",
    "phase_names",
    "missing_route_count",
    "missing_file_role_count",
    "missing_file_roles",
    "action_priority_counts",
    "route_ids",
    "missing_evidence_action_ids",
    "missing_evidence_result_scaffold_ids",
    "evidence_presence_row_ids",
    "files_to_open",
    "route_summary_path",
    "next_review_action",
    "source_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "reviewed_evidence_paths",
    "reviewed_outcome_summary",
    "remaining_blockers_reviewed",
    "required_followup_reviewed",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_route_summary(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def route_list_values(route: dict[str, object], field: str) -> list[str]:
    value = route.get(field, "")
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    return [part for part in str(value).split(";") if part]


def unique_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return ";".join(seen)


def sorted_unique_join(values: list[str]) -> str:
    return ";".join(sorted({value for value in values if value}))


def count_join(values: list[str]) -> str:
    return ";".join(f"{key}:{count}" for key, count in sorted(Counter(values).items()) if key)


def build_source_summary_rows(route_summary: dict[str, object]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for route in route_summary.get("routes", []):
        if isinstance(route, dict):
            grouped[str(route["source_id"])].append(route)

    rows: list[dict[str, str]] = []
    for index, source_id in enumerate(sorted(grouped), start=1):
        routes = grouped[source_id]
        first = routes[0]
        missing_file_roles = [str(route["missing_file_role"]) for route in routes]
        review_lanes: list[str] = []
        phase_names: list[str] = []
        files_to_open: list[str] = []
        for route in routes:
            review_lanes.extend(route_list_values(route, "review_lanes"))
            phase_names.extend(route_list_values(route, "phase_names"))
            files_to_open.append(str(route.get("file_to_open", "")))

        rows.append(
            {
                "missing_evidence_source_summary_id": (
                    f"source-pipeline-phase-action-missing-evidence-source-summary-{index:03d}"
                ),
                "source_id": source_id,
                "source_type": str(first["source_type"]),
                "rights_status": str(first["rights_status"]),
                "pipeline_gap_status": str(first["pipeline_gap_status"]),
                "review_lanes": sorted_unique_join(review_lanes),
                "phase_names": sorted_unique_join(phase_names),
                "missing_route_count": str(len(routes)),
                "missing_file_role_count": str(len(set(missing_file_roles))),
                "missing_file_roles": sorted_unique_join(missing_file_roles),
                "action_priority_counts": count_join([str(route["action_priority"]) for route in routes]),
                "route_ids": unique_join([str(route["route_id"]) for route in routes]),
                "missing_evidence_action_ids": unique_join(
                    [str(route["missing_evidence_action_id"]) for route in routes]
                ),
                "missing_evidence_result_scaffold_ids": unique_join(
                    [str(route["missing_evidence_result_scaffold_id"]) for route in routes]
                ),
                "evidence_presence_row_ids": unique_join([str(route["evidence_presence_row_id"]) for route in routes]),
                "files_to_open": unique_join(files_to_open),
                "route_summary_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ROUTE_SUMMARY.as_posix(),
                "next_review_action": NEXT_REVIEW_ACTION,
                "source_review_status": SOURCE_REVIEW_STATUS,
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "corpus_import_status": CORPUS_IMPORT_STATUS,
                "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
                "reviewed_evidence_paths": "",
                "reviewed_outcome_summary": "",
                "remaining_blockers_reviewed": unique_join(
                    [str(route.get("remaining_blockers_reviewed", "")) for route in routes]
                ),
                "required_followup_reviewed": "",
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
    parser.add_argument("--route-summary", default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ROUTE_SUMMARY))
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_source_summary_rows(read_route_summary(root / args.route_summary))
    write_csv(root / args.csv_output, rows)
    print(f"source_pipeline_phase_action_missing_evidence_source_summary_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
