#!/usr/bin/env python3
"""Build empty result scaffolds for source-engineering next actions.

The scaffold gives later reviewers a stable place to record action outcomes
from the 104 checklist. It intentionally starts empty and non-decisional: no
evidence is collected, no rights decision is made, no source is promoted, and
no corpus or decipherment claim is imported.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/104_ai-agent-source-engineering-next-action-checklist.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/105_ai-agent-source-engineering-next-action-result-scaffold.csv"
)

UPDATED_AT = "2026-06-19"
RESULT_STATUS = "not_started"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
RESEARCH_BOUNDARY = "source_engineering_next_action_result_scaffold_not_scholarship"
CAUTION = (
    "This scaffold does not record completed evidence. It is not a rights "
    "decision, not source promotion, not a corpus import, not an "
    "oracle-character identity claim, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "result_scaffold_id",
    "next_action_id",
    "evidence_snapshot_id",
    "source_engineering_gap_id",
    "review_log_draft_id",
    "source_id",
    "gap_type",
    "priority_rank",
    "action_lane",
    "source_checklist_path",
    "source_review_log_path",
    "expected_result_path",
    "result_record_path",
    "result_status",
    "evidence_collection_status",
    "reviewed_evidence_paths",
    "access_outcome",
    "checksum_outcome",
    "manifest_decision",
    "field_map_decision",
    "metadata_profile_decision",
    "safe_derived_record_decision",
    "remaining_blockers",
    "required_followup",
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
    checklist_rows = read_csv_rows(root / SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST)
    output_rows: list[dict[str, str]] = []
    for index, row in enumerate(checklist_rows, start=1):
        output_rows.append(
            {
                "result_scaffold_id": f"source-engineering-next-action-result-scaffold-{index:04d}",
                "next_action_id": row["next_action_id"],
                "evidence_snapshot_id": row["evidence_snapshot_id"],
                "source_engineering_gap_id": row["source_engineering_gap_id"],
                "review_log_draft_id": row["review_log_draft_id"],
                "source_id": row["source_id"],
                "gap_type": row["gap_type"],
                "priority_rank": row["priority_rank"],
                "action_lane": row["action_lane"],
                "source_checklist_path": SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST.as_posix(),
                "source_review_log_path": row["review_log_path"],
                "expected_result_path": row["expected_result_path"],
                "result_record_path": row["expected_result_path"],
                "result_status": RESULT_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "reviewed_evidence_paths": "",
                "access_outcome": "",
                "checksum_outcome": "",
                "manifest_decision": "",
                "field_map_decision": "",
                "metadata_profile_decision": "",
                "safe_derived_record_decision": "",
                "remaining_blockers": row["blocking_condition"],
                "required_followup": row["checklist_items"],
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
    return output_rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source-engineering next-action result scaffold.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_result_scaffold_rows(root)
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
