#!/usr/bin/env python3
"""Build empty outcome scaffold rows for second-wave source-engineering review.

The scaffold is the human-fillable result surface after the 126 checklist has
been opened. It preserves route links and empty outcome fields only; it does
not collect evidence, decide rights, promote sources, import corpus rows, or
make identity, component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SECOND_WAVE_REVIEW_CHECKLIST = STAT_DIR / "126_ai-agent-source-engineering-second-wave-review-checklist.csv"
DEFAULT_OUTPUT = STAT_DIR / "127_ai-agent-source-engineering-second-wave-review-outcome-scaffold.csv"

UPDATED_AT = "2026-06-19"
REVIEW_OUTCOME_STATUS = "not_started"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
COMPONENT_CLAIM_STATUS = "no_component_claim"
EVOLUTION_CLAIM_STATUS = "no_evolution_chain_claim"
AUTOMATION_BOUNDARY = "human_gated_second_wave_source_engineering_outcome_capture"
RESEARCH_BOUNDARY = "source_engineering_second_wave_review_outcome_scaffold_not_scholarship"
RESERVED_OUTCOME_FIELDS = ";".join(
    [
        "access_outcome_reviewed",
        "checksum_outcome_reviewed",
        "manifest_decision_reviewed",
        "field_map_decision_reviewed",
        "metadata_profile_decision_reviewed",
        "safe_derived_record_decision_reviewed",
        "reviewed_evidence_paths",
        "reviewed_outcome_summary",
        "remaining_blockers_reviewed",
        "required_followup_reviewed",
        "human_reviewer_id",
        "human_review_date",
        "human_review_notes",
    ]
)
CAUTION = (
    "This second-wave source-engineering file is a human-gated outcome scaffold. "
    "It is not collected evidence, not a rights decision, not source promotion, "
    "not a corpus import, not an identity claim, not a component assignment, "
    "not an evolution-chain assignment, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "second_wave_review_outcome_scaffold_id",
    "second_wave_review_checklist_id",
    "second_wave_result_scaffold_id",
    "review_draft_id",
    "continuation_task_id",
    "source_status_id",
    "source_id",
    "source_action_lane",
    "source_first_wave_status",
    "priority_rank",
    "priority_tags",
    "required_result_action",
    "required_review_steps",
    "blocking_condition",
    "review_checklist_path",
    "outcome_update_target_path",
    "result_scaffold_path",
    "result_update_target_path",
    "source_review_draft_manifest_path",
    "source_checklist_path",
    "source_status_path",
    "draft_path",
    "route_files_to_open",
    "reserved_review_fields",
    "reserved_outcome_fields",
    "review_outcome_status",
    "evidence_collection_status",
    "reviewed_evidence_paths",
    "access_outcome_reviewed",
    "checksum_outcome_reviewed",
    "manifest_decision_reviewed",
    "field_map_decision_reviewed",
    "metadata_profile_decision_reviewed",
    "safe_derived_record_decision_reviewed",
    "reviewed_outcome_summary",
    "remaining_blockers_reviewed",
    "required_followup_reviewed",
    "human_reviewer_id",
    "human_review_date",
    "human_review_notes",
    "human_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "identity_claim_status",
    "component_claim_status",
    "evolution_claim_status",
    "automation_boundary",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def build_review_outcome_scaffold_rows(checklist_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(checklist_rows, start=1):
        rows.append(
            {
                "second_wave_review_outcome_scaffold_id": (
                    f"source-engineering-second-wave-review-outcome-scaffold-{index:04d}"
                ),
                "second_wave_review_checklist_id": row["second_wave_review_checklist_id"],
                "second_wave_result_scaffold_id": row["second_wave_result_scaffold_id"],
                "review_draft_id": row["review_draft_id"],
                "continuation_task_id": row["continuation_task_id"],
                "source_status_id": row["source_status_id"],
                "source_id": row["source_id"],
                "source_action_lane": row["source_action_lane"],
                "source_first_wave_status": row["source_first_wave_status"],
                "priority_rank": row["priority_rank"],
                "priority_tags": row["priority_tags"],
                "required_result_action": row["required_result_action"],
                "required_review_steps": row["required_review_steps"],
                "blocking_condition": row["blocking_condition"],
                "review_checklist_path": SECOND_WAVE_REVIEW_CHECKLIST.as_posix(),
                "outcome_update_target_path": DEFAULT_OUTPUT.as_posix(),
                "result_scaffold_path": row["result_scaffold_path"],
                "result_update_target_path": row["result_update_target_path"],
                "source_review_draft_manifest_path": row["source_review_draft_manifest_path"],
                "source_checklist_path": row["source_checklist_path"],
                "source_status_path": row["source_status_path"],
                "draft_path": row["draft_path"],
                "route_files_to_open": row["route_files_to_open"],
                "reserved_review_fields": row["reserved_review_fields"],
                "reserved_outcome_fields": RESERVED_OUTCOME_FIELDS,
                "review_outcome_status": REVIEW_OUTCOME_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "reviewed_evidence_paths": "",
                "access_outcome_reviewed": "",
                "checksum_outcome_reviewed": "",
                "manifest_decision_reviewed": "",
                "field_map_decision_reviewed": "",
                "metadata_profile_decision_reviewed": "",
                "safe_derived_record_decision_reviewed": "",
                "reviewed_outcome_summary": "",
                "remaining_blockers_reviewed": row["blocking_condition"],
                "required_followup_reviewed": "",
                "human_reviewer_id": "",
                "human_review_date": "",
                "human_review_notes": "",
                "human_review_status": HUMAN_REVIEW_STATUS,
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "corpus_import_status": CORPUS_IMPORT_STATUS,
                "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "component_claim_status": COMPONENT_CLAIM_STATUS,
                "evolution_claim_status": EVOLUTION_CLAIM_STATUS,
                "automation_boundary": AUTOMATION_BOUNDARY,
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
    parser = argparse.ArgumentParser(description="Build second-wave source-engineering review outcome scaffold.")
    parser.add_argument("--review-checklist", default=str(SECOND_WAVE_REVIEW_CHECKLIST))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_review_outcome_scaffold_rows(read_csv_rows(root / args.review_checklist))
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
