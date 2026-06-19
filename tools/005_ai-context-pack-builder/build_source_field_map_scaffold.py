#!/usr/bin/env python3
"""Build pending source-field-map scaffold rows.

The scaffold targets the source_field_map_planning lane from the 107 route
pack. It gives later reviewers a structured place to draft field semantics
without appending reviewed rows to the formal 007 source-field-map table.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


SOURCE_ENGINEERING_LANE_ROUTE_PACK = Path(
    "corpus/009_statistics-and-derived-features/107_ai-agent-source-engineering-lane-route-pack.json"
)
SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_FIELD_MAP = Path("corpus/006_research-sources-and-bibliography/000_source-registers/007_source-field-map.csv")
DEFAULT_OUTPUT = Path("corpus/009_statistics-and-derived-features/108_ai-agent-source-field-map-scaffold.csv")

UPDATED_AT = "2026-06-19"
FIELD_MAP_REVIEW_STATUS = "pending_human_field_map_review"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
RESEARCH_BOUNDARY = "source_field_map_scaffold_not_reviewed_mapping"
CAUTION = (
    "This scaffold does not add reviewed field-map rows. It is not a corpus "
    "import, not source promotion, not a rights decision, and not an identity "
    "or decipherment claim."
)

OUTPUT_FIELDS = [
    "field_map_scaffold_id",
    "next_action_id",
    "source_engineering_gap_id",
    "source_id",
    "source_title",
    "provider",
    "source_type",
    "source_url",
    "rights_status",
    "risk_note",
    "action_lane",
    "review_log_path",
    "result_record_path",
    "existing_field_map_count",
    "proposed_source_level",
    "proposed_source_field_or_unit",
    "proposed_source_meaning",
    "proposed_target_record_type",
    "proposed_target_project_fields",
    "field_map_review_status",
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def target_record_type_for_source(source: dict[str, str]) -> str:
    source_type = source.get("source_type", "")
    if source_type == "museum_collection":
        return "collection_provenance;oracle_inscription;asset_metadata"
    if source_type == "open_research_dataset":
        return "ai_benchmark_dataset;asset_metadata"
    if source_type == "project_repository":
        return "source_record;dataset_index"
    return "source_record;oracle_character;oracle_inscription;asset_metadata"


def build_scaffold_rows(root: Path) -> list[dict[str, str]]:
    route_pack = json.loads((root / SOURCE_ENGINEERING_LANE_ROUTE_PACK).read_text(encoding="utf-8"))
    source_rows = {row["source_id"]: row for row in read_csv_rows(root / SOURCE_INDEX)}
    existing_field_map_counts = Counter(row["source_id"] for row in read_csv_rows(root / SOURCE_FIELD_MAP))

    field_map_tasks = [
        task
        for lane in route_pack["lanes"]
        if lane["action_lane"] == "source_field_map_planning"
        for task in lane["tasks"]
    ]

    rows: list[dict[str, str]] = []
    for index, task in enumerate(field_map_tasks, start=1):
        source = source_rows[task["source_id"]]
        rows.append(
            {
                "field_map_scaffold_id": f"source-field-map-scaffold-{index:03d}",
                "next_action_id": task["next_action_id"],
                "source_engineering_gap_id": task["source_engineering_gap_id"],
                "source_id": task["source_id"],
                "source_title": source["title"],
                "provider": source["provider"],
                "source_type": source["source_type"],
                "source_url": source["source_url"],
                "rights_status": source["rights_status"],
                "risk_note": source["risk_note"],
                "action_lane": "source_field_map_planning",
                "review_log_path": task["review_log_path"],
                "result_record_path": task["result_record_path"],
                "existing_field_map_count": str(existing_field_map_counts[task["source_id"]]),
                "proposed_source_level": "source_level_unreviewed",
                "proposed_source_field_or_unit": "field_semantics_unreviewed",
                "proposed_source_meaning": "pending_human_review",
                "proposed_target_record_type": target_record_type_for_source(source),
                "proposed_target_project_fields": "pending_human_review",
                "field_map_review_status": FIELD_MAP_REVIEW_STATUS,
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
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build pending source-field-map scaffold rows.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_scaffold_rows(root)
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
