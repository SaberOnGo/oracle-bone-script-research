#!/usr/bin/env python3
"""Build a route summary for missing source-evidence result scaffolds."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


OUTPUT_JSON = Path(
    "corpus/009_statistics-and-derived-features/146_source-pipeline-phase-action-missing-evidence-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_RESULT_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/145_source-pipeline-phase-action-missing-evidence-result-scaffold.csv"
)
UPDATED_AT = "2026-06-19"
ROUTE_STATUS = "not_started"
AUTOMATION_BOUNDARY = "routing_only_no_missing_evidence_outcome_capture"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_missing_evidence_route_summary_not_scholarship"
CAUTION = (
    "This source pipeline missing-evidence route summary is routing-only. It is "
    "not collected evidence, not a reviewed outcome, not a rights decision, not "
    "source promotion, not a corpus import, and not a decipherment conclusion."
)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_semicolon(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def route_from_row(index: int, row: dict[str, str]) -> dict[str, object]:
    return {
        "route_id": f"source-pipeline-phase-action-missing-evidence-route-{index:03d}",
        "action_result_scaffold_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_RESULT_SCAFFOLD.as_posix(),
        "missing_evidence_result_scaffold_id": row["missing_evidence_result_scaffold_id"],
        "missing_evidence_action_id": row["missing_evidence_action_id"],
        "evidence_presence_row_id": row["evidence_presence_row_id"],
        "source_id": row["source_id"],
        "source_type": row["source_type"],
        "rights_status": row["rights_status"],
        "pipeline_gap_status": row["pipeline_gap_status"],
        "review_lanes": split_semicolon(row["review_lanes"]),
        "phase_names": split_semicolon(row["phase_names"]),
        "missing_file_role": row["missing_file_role"],
        "file_to_open": row["file_to_open"],
        "join_strategy": row["join_strategy"],
        "missing_reason": row["missing_reason"],
        "action_type": row["action_type"],
        "action_priority": row["action_priority"],
        "action_queue_path": row["action_queue_path"],
        "evidence_presence_matrix_path": row["evidence_presence_matrix_path"],
        "file_checklist_path": row["file_checklist_path"],
        "source_summary_path": row["source_summary_path"],
        "source_gap_summary_path": row["source_gap_summary_path"],
        "route_ids": split_semicolon(row["route_ids"]),
        "result_scaffold_ids": split_semicolon(row["result_scaffold_ids"]),
        "action_ids": split_semicolon(row["action_ids"]),
        "reserved_outcome_fields": split_semicolon(row["reserved_outcome_fields"]),
        "route_status": ROUTE_STATUS,
        "result_status": row["result_status"],
        "evidence_collection_status": row["evidence_collection_status"],
        "reviewed_evidence_paths": row["reviewed_evidence_paths"],
        "reviewed_outcome_summary": row["reviewed_outcome_summary"],
        "remaining_blockers_reviewed": row["remaining_blockers_reviewed"],
        "required_followup_reviewed": row["required_followup_reviewed"],
        "human_review_status": row["human_review_status"],
        "rights_decision_status": row["rights_decision_status"],
        "source_promotion_status": row["source_promotion_status"],
        "corpus_import_status": row["corpus_import_status"],
        "decipherment_claim_status": row["decipherment_claim_status"],
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
    }


def build_route_summary(scaffold_rows: list[dict[str, str]]) -> dict[str, object]:
    routes = [route_from_row(index, row) for index, row in enumerate(scaffold_rows, start=1)]
    return {
        "route_summary_id": "source-pipeline-phase-action-missing-evidence-route-summary-001",
        "updated_at": UPDATED_AT,
        "action_result_scaffold_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_RESULT_SCAFFOLD.as_posix(),
        "route_count": len(routes),
        "source_count": len({route["source_id"] for route in routes}),
        "source_counts": dict(sorted(Counter(route["source_id"] for route in routes).items())),
        "missing_file_role_counts": dict(sorted(Counter(route["missing_file_role"] for route in routes).items())),
        "action_priority_counts": dict(sorted(Counter(route["action_priority"] for route in routes).items())),
        "result_status_counts": dict(sorted(Counter(route["result_status"] for route in routes).items())),
        "route_status_counts": dict(sorted(Counter(route["route_status"] for route in routes).items())),
        "evidence_collection_status_counts": dict(
            sorted(Counter(route["evidence_collection_status"] for route in routes).items())
        ),
        "human_review_status_counts": dict(sorted(Counter(route["human_review_status"] for route in routes).items())),
        "rights_decision_status_counts": dict(
            sorted(Counter(route["rights_decision_status"] for route in routes).items())
        ),
        "source_promotion_status_counts": dict(
            sorted(Counter(route["source_promotion_status"] for route in routes).items())
        ),
        "corpus_import_status_counts": dict(sorted(Counter(route["corpus_import_status"] for route in routes).items())),
        "decipherment_claim_status_counts": dict(
            sorted(Counter(route["decipherment_claim_status"] for route in routes).items())
        ),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "routes": routes,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scaffold", default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_RESULT_SCAFFOLD))
    parser.add_argument("--json-output", default=str(OUTPUT_JSON))
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parents[2]
    data = build_route_summary(read_csv_rows(root / args.scaffold))
    write_json(root / args.json_output, data)
    print(f"source_pipeline_phase_action_missing_evidence_routes={data['route_count']} json={args.json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
