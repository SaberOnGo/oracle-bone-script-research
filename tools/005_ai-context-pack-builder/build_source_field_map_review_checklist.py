#!/usr/bin/env python3
"""Build review checklist rows for pending source-field-map scaffolds.

The checklist routes each 108 scaffold row to the files and questions a human
reviewer must inspect before any field-map semantics can be promoted.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_FIELD_MAP = Path("corpus/006_research-sources-and-bibliography/000_source-registers/007_source-field-map.csv")
LANE_ROUTE_PACK = Path(
    "corpus/009_statistics-and-derived-features/107_ai-agent-source-engineering-lane-route-pack.json"
)
SOURCE_FIELD_MAP_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/108_ai-agent-source-field-map-scaffold.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/109_ai-agent-source-field-map-review-checklist.csv"
)

UPDATED_AT = "2026-06-19"
CHECKLIST_STATUS = "not_started"
FIELD_MAP_REVIEW_STATUS = "pending_human_field_map_review"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
RESEARCH_BOUNDARY = "source_field_map_review_checklist_not_reviewed_mapping"
REQUIRED_REVIEW_STEPS = ";".join(
    [
        "open_scaffold_row",
        "open_source_register",
        "open_existing_field_map",
        "open_lane_route_pack",
        "open_review_log",
        "verify_rights_and_risk_note",
        "identify_source_field_or_unit",
        "identify_target_record_type",
        "record_unknown_fields_pending_review",
        "do_not_import_until_reviewed",
    ]
)
BLOCKING_CONDITION = "no_field_map_import_until_semantics_and_rights_are_reviewed"
CAUTION = (
    "This checklist does not approve field-map semantics. It is not a corpus "
    "import, not source promotion, not a rights decision, and not an identity "
    "or decipherment claim."
)

OUTPUT_FIELDS = [
    "field_map_checklist_id",
    "field_map_scaffold_id",
    "next_action_id",
    "source_engineering_gap_id",
    "source_id",
    "source_title",
    "provider",
    "source_type",
    "rights_status",
    "risk_note",
    "review_log_path",
    "result_record_path",
    "source_register_path",
    "existing_field_map_path",
    "lane_route_pack_path",
    "scaffold_path",
    "proposed_target_record_type",
    "proposed_target_project_fields",
    "required_review_steps",
    "blocking_condition",
    "checklist_status",
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


def build_review_checklist_rows(root: Path) -> list[dict[str, str]]:
    scaffold_rows = read_csv_rows(root / SOURCE_FIELD_MAP_SCAFFOLD)
    rows: list[dict[str, str]] = []
    for index, scaffold in enumerate(scaffold_rows, start=1):
        rows.append(
            {
                "field_map_checklist_id": f"source-field-map-review-checklist-{index:03d}",
                "field_map_scaffold_id": scaffold["field_map_scaffold_id"],
                "next_action_id": scaffold["next_action_id"],
                "source_engineering_gap_id": scaffold["source_engineering_gap_id"],
                "source_id": scaffold["source_id"],
                "source_title": scaffold["source_title"],
                "provider": scaffold["provider"],
                "source_type": scaffold["source_type"],
                "rights_status": scaffold["rights_status"],
                "risk_note": scaffold["risk_note"],
                "review_log_path": scaffold["review_log_path"],
                "result_record_path": scaffold["result_record_path"],
                "source_register_path": SOURCE_INDEX.as_posix(),
                "existing_field_map_path": SOURCE_FIELD_MAP.as_posix(),
                "lane_route_pack_path": LANE_ROUTE_PACK.as_posix(),
                "scaffold_path": SOURCE_FIELD_MAP_SCAFFOLD.as_posix(),
                "proposed_target_record_type": scaffold["proposed_target_record_type"],
                "proposed_target_project_fields": scaffold["proposed_target_project_fields"],
                "required_review_steps": REQUIRED_REVIEW_STEPS,
                "blocking_condition": BLOCKING_CONDITION,
                "checklist_status": CHECKLIST_STATUS,
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
    parser = argparse.ArgumentParser(description="Build source-field-map review checklist rows.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_review_checklist_rows(root)
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
