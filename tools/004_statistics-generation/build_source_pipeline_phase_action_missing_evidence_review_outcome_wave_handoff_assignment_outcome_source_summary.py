#!/usr/bin/env python3
"""Build a source-level summary for missing-evidence assignment outcome routes."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_ROUTE_SUMMARY = (
    STAT_DIR / "167_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-route-summary.json"
)
OUTPUT_CSV = (
    STAT_DIR / "168_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-summary.csv"
)

UPDATED_AT = "2026-06-19"
NEXT_REVIEW_ACTION = "open_assignment_outcome_routes_for_source_then_record_human_gated_source_outcomes"
SOURCE_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
RESEARCH_BOUNDARY = (
    "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_summary_not_scholarship"
)
CAUTION = (
    "This source pipeline missing-evidence assignment outcome source summary is routing-only. "
    "It is not collected evidence, not a reviewed outcome, not a rights decision, "
    "not source promotion, not a corpus import, not an identity claim, not a component "
    "assignment, not an evolution-chain assignment, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "assignment_outcome_source_summary_id",
    "source_id",
    "source_type",
    "rights_status",
    "pipeline_gap_status",
    "assignment_outcome_route_count",
    "handoff_wave_ids",
    "assignment_wave_ids",
    "assignment_plan_item_ids",
    "assignment_review_checklist_ids",
    "assignment_outcome_scaffold_ids",
    "assignment_outcome_route_ids",
    "missing_file_role_count",
    "missing_file_roles",
    "priority_tags",
    "required_review_steps",
    "assignment_files_to_open",
    "draft_paths",
    "assignment_outcome_route_summary_path",
    "next_review_action",
    "source_review_status",
    "assignment_review_status_counts",
    "review_outcome_status_counts",
    "evidence_collection_status_counts",
    "human_review_status_counts",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "reviewed_evidence_paths",
    "reviewed_outcome_summary",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_route_summary(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def route_values(route: dict[str, object], field: str) -> list[str]:
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
        missing_file_roles: list[str] = []
        priority_tags: list[str] = []
        required_review_steps: list[str] = []
        assignment_files_to_open: list[str] = []
        draft_paths: list[str] = []
        for route in routes:
            missing_file_roles.extend(route_values(route, "missing_file_roles"))
            priority_tags.extend(route_values(route, "priority_tags"))
            required_review_steps.extend(route_values(route, "required_review_steps"))
            assignment_files_to_open.extend(route_values(route, "assignment_files_to_open"))
            draft_paths.append(str(route.get("draft_path", "")))

        rows.append(
            {
                "assignment_outcome_source_summary_id": (
                    "source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-summary-"
                    f"{index:03d}"
                ),
                "source_id": source_id,
                "source_type": str(first["source_type"]),
                "rights_status": str(first["rights_status"]),
                "pipeline_gap_status": str(first["pipeline_gap_status"]),
                "assignment_outcome_route_count": str(len(routes)),
                "handoff_wave_ids": unique_join([str(route["handoff_wave_id"]) for route in routes]),
                "assignment_wave_ids": unique_join([str(route["assignment_wave_id"]) for route in routes]),
                "assignment_plan_item_ids": unique_join([str(route["assignment_plan_item_id"]) for route in routes]),
                "assignment_review_checklist_ids": unique_join(
                    [str(route["assignment_review_checklist_id"]) for route in routes]
                ),
                "assignment_outcome_scaffold_ids": unique_join(
                    [str(route["assignment_outcome_scaffold_id"]) for route in routes]
                ),
                "assignment_outcome_route_ids": unique_join([str(route["summary_route_id"]) for route in routes]),
                "missing_file_role_count": str(len(set(missing_file_roles))),
                "missing_file_roles": sorted_unique_join(missing_file_roles),
                "priority_tags": sorted_unique_join(priority_tags),
                "required_review_steps": sorted_unique_join(required_review_steps),
                "assignment_files_to_open": unique_join(assignment_files_to_open),
                "draft_paths": unique_join(draft_paths),
                "assignment_outcome_route_summary_path": (
                    SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_ROUTE_SUMMARY.as_posix()
                ),
                "next_review_action": NEXT_REVIEW_ACTION,
                "source_review_status": SOURCE_REVIEW_STATUS,
                "assignment_review_status_counts": count_join(
                    [str(route["assignment_review_status"]) for route in routes]
                ),
                "review_outcome_status_counts": count_join([str(route["review_outcome_status"]) for route in routes]),
                "evidence_collection_status_counts": count_join(
                    [str(route["evidence_collection_status"]) for route in routes]
                ),
                "human_review_status_counts": count_join([str(route["human_review_status"]) for route in routes]),
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "corpus_import_status": CORPUS_IMPORT_STATUS,
                "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
                "reviewed_evidence_paths": "",
                "reviewed_outcome_summary": "",
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
    parser = argparse.ArgumentParser(description="Build missing-evidence assignment outcome source summary.")
    parser.add_argument(
        "--route-summary",
        default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_ROUTE_SUMMARY),
    )
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_source_summary_rows(read_route_summary(root / args.route_summary))
    write_csv(root / args.csv_output, rows)
    print(f"missing_evidence_assignment_outcome_source_summary_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
