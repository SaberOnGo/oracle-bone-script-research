#!/usr/bin/env python3
"""Build a route pack for source-field-map review.

The pack connects the 108 scaffold, 109 checklist, and 110 empty result
scaffold. It is routing metadata only: no field-map semantics are approved, no
rights decision is made, no source is promoted, no corpus record is imported,
and no decipherment claim is made.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_FIELD_MAP = Path("corpus/006_research-sources-and-bibliography/000_source-registers/007_source-field-map.csv")
LANE_ROUTE_PACK = Path(
    "corpus/009_statistics-and-derived-features/107_ai-agent-source-engineering-lane-route-pack.json"
)
SOURCE_FIELD_MAP_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/108_ai-agent-source-field-map-scaffold.csv"
)
SOURCE_FIELD_MAP_REVIEW_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/109_ai-agent-source-field-map-review-checklist.csv"
)
SOURCE_FIELD_MAP_REVIEW_RESULT_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/110_ai-agent-source-field-map-review-result-scaffold.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/111_ai-agent-source-field-map-review-route-pack.json"
)

UPDATED_AT = "2026-06-19"
ROUTE_PACK_ID = "source-field-map-review-route-pack-001"
REVIEW_STATUS = "route_pack_pending_field_map_review"
RESEARCH_BOUNDARY = "source_field_map_review_route_pack_not_reviewed_mapping"
CAUTION = (
    "Source-field-map review route pack only; it does not approve field-map "
    "semantics, is not a corpus import, not source promotion, not a rights "
    "decision, and not an identity or decipherment claim."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_values(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def route_from_rows(
    scaffold_row: dict[str, str],
    checklist_row: dict[str, str],
    result_row: dict[str, str],
) -> dict[str, Any]:
    return {
        "field_map_scaffold_id": scaffold_row["field_map_scaffold_id"],
        "field_map_checklist_id": checklist_row["field_map_checklist_id"],
        "field_map_result_scaffold_id": result_row["field_map_result_scaffold_id"],
        "next_action_id": checklist_row["next_action_id"],
        "source_engineering_gap_id": checklist_row["source_engineering_gap_id"],
        "source_id": checklist_row["source_id"],
        "source_title": checklist_row["source_title"],
        "provider": checklist_row["provider"],
        "source_type": checklist_row["source_type"],
        "rights_status": checklist_row["rights_status"],
        "risk_note": checklist_row["risk_note"],
        "review_log_path": checklist_row["review_log_path"],
        "result_record_path": result_row["result_record_path"],
        "source_register_path": checklist_row["source_register_path"],
        "existing_field_map_path": checklist_row["existing_field_map_path"],
        "lane_route_pack_path": checklist_row["lane_route_pack_path"],
        "scaffold_path": checklist_row["scaffold_path"],
        "checklist_path": result_row["checklist_path"],
        "target_reviewed_field_map_path": result_row["target_reviewed_field_map_path"],
        "proposed_source_level": scaffold_row["proposed_source_level"],
        "proposed_source_field_or_unit": scaffold_row["proposed_source_field_or_unit"],
        "proposed_target_record_type": checklist_row["proposed_target_record_type"],
        "proposed_target_project_fields": checklist_row["proposed_target_project_fields"],
        "reviewed_source_level": result_row["reviewed_source_level"],
        "reviewed_source_field_or_unit": result_row["reviewed_source_field_or_unit"],
        "reviewed_source_meaning": result_row["reviewed_source_meaning"],
        "reviewed_target_record_type": result_row["reviewed_target_record_type"],
        "reviewed_target_project_fields": result_row["reviewed_target_project_fields"],
        "required_review_steps": split_values(checklist_row["required_review_steps"]),
        "blocking_condition": checklist_row["blocking_condition"],
        "reserved_review_fields": split_values(result_row["reserved_review_fields"]),
        "field_map_review_notes": result_row["field_map_review_notes"],
        "field_map_blockers": split_values(result_row["field_map_blockers"]),
        "required_followup": result_row["required_followup"],
        "checklist_status": checklist_row["checklist_status"],
        "field_map_result_status": result_row["field_map_result_status"],
        "field_map_review_status": result_row["field_map_review_status"],
        "human_review_status": result_row["human_review_status"],
        "rights_decision_status": result_row["rights_decision_status"],
        "source_promotion_status": result_row["source_promotion_status"],
        "corpus_import_status": result_row["corpus_import_status"],
        "decipherment_claim_status": result_row["decipherment_claim_status"],
    }


def build_route_pack(root: Path) -> dict[str, Any]:
    scaffold_rows = read_csv_rows(root / SOURCE_FIELD_MAP_SCAFFOLD)
    checklist_rows = read_csv_rows(root / SOURCE_FIELD_MAP_REVIEW_CHECKLIST)
    result_rows = read_csv_rows(root / SOURCE_FIELD_MAP_REVIEW_RESULT_SCAFFOLD)
    checklist_by_source = {row["source_id"]: row for row in checklist_rows}
    result_by_source = {row["source_id"]: row for row in result_rows}

    routes = [
        route_from_rows(
            scaffold_row,
            checklist_by_source[scaffold_row["source_id"]],
            result_by_source[scaffold_row["source_id"]],
        )
        for scaffold_row in scaffold_rows
    ]

    return {
        "route_pack_id": ROUTE_PACK_ID,
        "updated_at": UPDATED_AT,
        "source_paths": {
            "source_register": SOURCE_INDEX.as_posix(),
            "existing_field_map": SOURCE_FIELD_MAP.as_posix(),
            "lane_route_pack": LANE_ROUTE_PACK.as_posix(),
            "field_map_scaffold": SOURCE_FIELD_MAP_SCAFFOLD.as_posix(),
            "field_map_review_checklist": SOURCE_FIELD_MAP_REVIEW_CHECKLIST.as_posix(),
            "field_map_review_result_scaffold": SOURCE_FIELD_MAP_REVIEW_RESULT_SCAFFOLD.as_posix(),
        },
        "source_count": len({route["source_id"] for route in routes}),
        "route_count": len(routes),
        "review_status": REVIEW_STATUS,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "routes": routes,
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source-field-map review route pack.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_route_pack(root)
    write_json(root / args.output, data)
    print(f"routes={data['route_count']} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
