#!/usr/bin/env python3
"""Build empty result scaffold rows for source-field-map review.

The output pairs with the 109 checklist and reserves fields for a future human
review pass. It does not approve field semantics or append reviewed field-map
rows.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_FIELD_MAP = Path("corpus/006_research-sources-and-bibliography/000_source-registers/007_source-field-map.csv")
SOURCE_FIELD_MAP_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/108_ai-agent-source-field-map-scaffold.csv"
)
SOURCE_FIELD_MAP_REVIEW_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/109_ai-agent-source-field-map-review-checklist.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/110_ai-agent-source-field-map-review-result-scaffold.csv"
)

UPDATED_AT = "2026-06-19"
FIELD_MAP_RESULT_STATUS = "not_started"
FIELD_MAP_REVIEW_STATUS = "pending_human_field_map_review"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
RESEARCH_BOUNDARY = "source_field_map_review_result_scaffold_not_reviewed_mapping"
PENDING_REVIEW = "pending_human_review"
RESERVED_REVIEW_FIELDS = ";".join(
    [
        "reviewed_source_level",
        "reviewed_source_field_or_unit",
        "reviewed_source_meaning",
        "reviewed_target_record_type",
        "reviewed_target_project_fields",
        "field_map_review_notes",
        "field_map_blockers",
        "required_followup",
    ]
)
CAUTION = (
    "This result scaffold does not approve field-map semantics. It is not a "
    "corpus import, not source promotion, not a rights decision, and not an "
    "identity or decipherment claim."
)

OUTPUT_FIELDS = [
    "field_map_result_scaffold_id",
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
    "checklist_path",
    "scaffold_path",
    "review_log_path",
    "source_register_path",
    "target_reviewed_field_map_path",
    "result_record_path",
    "reserved_review_fields",
    "reviewed_source_level",
    "reviewed_source_field_or_unit",
    "reviewed_source_meaning",
    "reviewed_target_record_type",
    "reviewed_target_project_fields",
    "field_map_review_notes",
    "field_map_blockers",
    "required_followup",
    "field_map_result_status",
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


def build_result_scaffold_rows(root: Path) -> list[dict[str, str]]:
    checklist_rows = read_csv_rows(root / SOURCE_FIELD_MAP_REVIEW_CHECKLIST)
    rows: list[dict[str, str]] = []
    for index, checklist in enumerate(checklist_rows, start=1):
        rows.append(
            {
                "field_map_result_scaffold_id": f"source-field-map-review-result-scaffold-{index:03d}",
                "field_map_checklist_id": checklist["field_map_checklist_id"],
                "field_map_scaffold_id": checklist["field_map_scaffold_id"],
                "next_action_id": checklist["next_action_id"],
                "source_engineering_gap_id": checklist["source_engineering_gap_id"],
                "source_id": checklist["source_id"],
                "source_title": checklist["source_title"],
                "provider": checklist["provider"],
                "source_type": checklist["source_type"],
                "rights_status": checklist["rights_status"],
                "risk_note": checklist["risk_note"],
                "checklist_path": SOURCE_FIELD_MAP_REVIEW_CHECKLIST.as_posix(),
                "scaffold_path": SOURCE_FIELD_MAP_SCAFFOLD.as_posix(),
                "review_log_path": checklist["review_log_path"],
                "source_register_path": SOURCE_INDEX.as_posix(),
                "target_reviewed_field_map_path": SOURCE_FIELD_MAP.as_posix(),
                "result_record_path": checklist["result_record_path"],
                "reserved_review_fields": RESERVED_REVIEW_FIELDS,
                "reviewed_source_level": PENDING_REVIEW,
                "reviewed_source_field_or_unit": PENDING_REVIEW,
                "reviewed_source_meaning": PENDING_REVIEW,
                "reviewed_target_record_type": checklist["proposed_target_record_type"],
                "reviewed_target_project_fields": PENDING_REVIEW,
                "field_map_review_notes": PENDING_REVIEW,
                "field_map_blockers": "field_map_semantics_not_reviewed",
                "required_followup": "human_field_map_review_required_before_import",
                "field_map_result_status": FIELD_MAP_RESULT_STATUS,
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
    parser = argparse.ArgumentParser(description="Build source-field-map review result scaffold rows.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_result_scaffold_rows(root)
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
