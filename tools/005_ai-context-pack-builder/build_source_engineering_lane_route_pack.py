#!/usr/bin/env python3
"""Build a route pack for source-engineering review lanes.

The pack connects the 106 lane summary back to the 104 checklist and 105 empty
result scaffold so later reviewers can open the right files for each lane. It
is routing metadata only: no evidence is collected, no rights decision is made,
no source is promoted, and no corpus or decipherment claim is imported.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/104_ai-agent-source-engineering-next-action-checklist.csv"
)
SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/105_ai-agent-source-engineering-next-action-result-scaffold.csv"
)
SOURCE_ENGINEERING_LANE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/106_ai-agent-source-engineering-lane-summary.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/107_ai-agent-source-engineering-lane-route-pack.json"
)

UPDATED_AT = "2026-06-19"
ROUTE_PACK_ID = "source-engineering-lane-route-pack-001"
REVIEW_STATUS = "route_pack_pending_source_engineering_review"
RESEARCH_BOUNDARY = "source_engineering_lane_route_pack_not_scholarship"
CAUTION = (
    "Source-engineering lane route pack only; it does not collect evidence, "
    "decide rights, promote sources, import corpus records, confirm identity, "
    "or make decipherment claims."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_values(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def task_from_rows(checklist_row: dict[str, str], result_row: dict[str, str]) -> dict[str, Any]:
    return {
        "next_action_id": checklist_row["next_action_id"],
        "result_scaffold_id": result_row["result_scaffold_id"],
        "source_engineering_gap_id": checklist_row["source_engineering_gap_id"],
        "evidence_snapshot_id": checklist_row["evidence_snapshot_id"],
        "review_log_draft_id": checklist_row["review_log_draft_id"],
        "source_id": checklist_row["source_id"],
        "gap_type": checklist_row["gap_type"],
        "priority_rank": int(checklist_row["priority_rank"]),
        "automation_scope": checklist_row["automation_scope"],
        "human_gate": checklist_row["human_gate"],
        "primary_input_path": checklist_row["primary_input_path"],
        "secondary_input_paths": split_values(checklist_row["secondary_input_paths"]),
        "review_log_path": checklist_row["review_log_path"],
        "expected_result_path": checklist_row["expected_result_path"],
        "result_record_path": result_row["result_record_path"],
        "checklist_items": split_values(checklist_row["checklist_items"]),
        "blocking_condition": checklist_row["blocking_condition"],
        "safe_to_automate_status": checklist_row["safe_to_automate_status"],
        "action_status": checklist_row["action_status"],
        "result_status": result_row["result_status"],
        "evidence_collection_status": result_row["evidence_collection_status"],
        "human_review_status": result_row["human_review_status"],
        "rights_decision_status": result_row["rights_decision_status"],
        "source_promotion_status": result_row["source_promotion_status"],
        "corpus_import_status": result_row["corpus_import_status"],
        "decipherment_claim_status": result_row["decipherment_claim_status"],
    }


def build_route_pack(root: Path) -> dict[str, Any]:
    lane_rows = read_csv_rows(root / SOURCE_ENGINEERING_LANE_SUMMARY)
    checklist_rows = read_csv_rows(root / SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST)
    result_rows = read_csv_rows(root / SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD)
    results_by_action = {row["next_action_id"]: row for row in result_rows}

    lanes: list[dict[str, Any]] = []
    for lane_row in lane_rows:
        action_lane = lane_row["action_lane"]
        lane_checklist_rows = [row for row in checklist_rows if row["action_lane"] == action_lane]
        tasks = [
            task_from_rows(checklist_row, results_by_action[checklist_row["next_action_id"]])
            for checklist_row in lane_checklist_rows
        ]
        lanes.append(
            {
                "lane_summary_id": lane_row["lane_summary_id"],
                "action_lane": action_lane,
                "action_count": int(lane_row["action_count"]),
                "source_count": int(lane_row["source_count"]),
                "priority_min": int(lane_row["priority_min"]),
                "priority_max": int(lane_row["priority_max"]),
                "gap_type_counts": lane_row["gap_type_counts"],
                "safe_to_automate_status_counts": lane_row["safe_to_automate_status_counts"],
                "result_status_counts": lane_row["result_status_counts"],
                "evidence_collection_status_counts": lane_row["evidence_collection_status_counts"],
                "human_review_status_counts": lane_row["human_review_status_counts"],
                "rights_decision_status_counts": lane_row["rights_decision_status_counts"],
                "source_promotion_status_counts": lane_row["source_promotion_status_counts"],
                "corpus_import_status_counts": lane_row["corpus_import_status_counts"],
                "decipherment_claim_status_counts": lane_row["decipherment_claim_status_counts"],
                "source_ids": split_values(lane_row["source_ids"]),
                "checklist_path": lane_row["checklist_path"],
                "result_scaffold_path": lane_row["result_scaffold_path"],
                "blocking_conditions": split_values(lane_row["blocking_conditions"]),
                "tasks": tasks,
            }
        )

    return {
        "route_pack_id": ROUTE_PACK_ID,
        "updated_at": UPDATED_AT,
        "source_paths": {
            "next_action_checklist": SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST.as_posix(),
            "next_action_result_scaffold": SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD.as_posix(),
            "lane_summary": SOURCE_ENGINEERING_LANE_SUMMARY.as_posix(),
        },
        "lane_count": len(lanes),
        "action_count": len(checklist_rows),
        "result_scaffold_count": len(result_rows),
        "review_status": REVIEW_STATUS,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "lanes": lanes,
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source-engineering lane route pack.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_route_pack(root)
    write_json(root / args.output, data)
    print(
        f"lanes={data['lane_count']} actions={data['action_count']} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
