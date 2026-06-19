#!/usr/bin/env python3
"""Build human review checklist rows for source-level missing evidence.

The checklist routes each 149 result scaffold row to the draft, source files,
and role-specific checks that must be opened before a human records any
outcome. It does not collect evidence, decide rights, promote sources, import
corpus rows, or make identity, component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_RESULT_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "149_source-pipeline-phase-action-missing-evidence-result-scaffold.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "150_source-pipeline-phase-action-missing-evidence-review-checklist.csv"
)

UPDATED_AT = "2026-06-19"
ASSIGNMENT_STATUS = "unassigned"
REVIEW_STATUS = "needs_missing_evidence_source_review"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
COMPONENT_CLAIM_STATUS = "no_component_claim"
EVOLUTION_CLAIM_STATUS = "no_evolution_chain_claim"
AUTOMATION_BOUNDARY = "human_gated_source_pipeline_missing_evidence_review"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_missing_evidence_review_checklist_not_scholarship"
CAUTION = (
    "This source pipeline missing-evidence checklist is a human-gated review "
    "route only. It is not collected evidence, not a reviewed outcome, not a "
    "rights decision, not source promotion, not a corpus import, not an "
    "identity claim, not a component assignment, not an evolution-chain "
    "assignment, and not a decipherment conclusion."
)

COMMON_REVIEW_STEPS = [
    "open_missing_evidence_result_scaffold",
    "open_missing_evidence_review_draft",
    "open_source_summary",
    "open_route_summary",
    "open_all_files_to_open",
    "verify_rights_status_and_risk_note",
    "record_only_reviewed_source_metadata_outcomes",
    "leave_unchecked_roles_empty",
    "do_not_import_or_promote_until_reviewed",
    "do_not_write_ai_hypothesis_as_scholarship",
]
ROLE_REVIEW_STEPS = {
    "downloaded_metadata_profile": "verify_downloaded_metadata_profile_or_not_applicable_boundary",
    "large_source_register": "verify_large_source_register_applicability",
    "source_field_map": "verify_source_field_map_or_create_reviewed_row",
    "source_package_file_manifest": "verify_package_manifest_or_not_applicable_boundary",
}

OUTPUT_FIELDS = [
    "review_checklist_id",
    "result_scaffold_id",
    "review_draft_id",
    "source_summary_id",
    "source_id",
    "source_type",
    "rights_status",
    "pipeline_gap_status",
    "missing_route_count",
    "missing_file_role_count",
    "missing_file_roles",
    "priority_rank",
    "priority_tags",
    "required_review_steps",
    "blocking_condition",
    "result_scaffold_path",
    "result_update_target_path",
    "review_draft_manifest_path",
    "draft_path",
    "source_summary_path",
    "route_summary_path",
    "route_ids",
    "missing_evidence_action_ids",
    "missing_evidence_result_scaffold_ids",
    "evidence_presence_row_ids",
    "files_to_open",
    "required_review_actions",
    "assignment_status",
    "review_status",
    "evidence_collection_status",
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


def split_semicolon(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def required_review_steps(row: dict[str, str]) -> str:
    steps = list(COMMON_REVIEW_STEPS)
    for role in split_semicolon(row["missing_file_roles"]):
        step = ROLE_REVIEW_STEPS.get(role)
        if step:
            steps.append(step)
    return ";".join(dict.fromkeys(steps))


def priority_tags(row: dict[str, str]) -> str:
    tags = [
        f"source:{row['source_id']}",
        f"gap_status:{row['pipeline_gap_status']}",
        "missing_evidence_review",
    ]
    tags.extend(f"role:{role}" for role in split_semicolon(row["missing_file_roles"]))
    return ";".join(tags)


def build_review_checklist_rows(scaffold_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(scaffold_rows, start=1):
        rows.append(
            {
                "review_checklist_id": f"source-pipeline-missing-evidence-review-checklist-{index:03d}",
                "result_scaffold_id": row["result_scaffold_id"],
                "review_draft_id": row["review_draft_id"],
                "source_summary_id": row["source_summary_id"],
                "source_id": row["source_id"],
                "source_type": row["source_type"],
                "rights_status": row["rights_status"],
                "pipeline_gap_status": row["pipeline_gap_status"],
                "missing_route_count": row["missing_route_count"],
                "missing_file_role_count": row["missing_file_role_count"],
                "missing_file_roles": row["missing_file_roles"],
                "priority_rank": str(index),
                "priority_tags": priority_tags(row),
                "required_review_steps": required_review_steps(row),
                "blocking_condition": "open_all_routed_files_before_recording_missing_evidence_outcomes",
                "result_scaffold_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_RESULT_SCAFFOLD.as_posix(),
                "result_update_target_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_RESULT_SCAFFOLD.as_posix(),
                "review_draft_manifest_path": row["review_draft_manifest_path"],
                "draft_path": row["draft_path"],
                "source_summary_path": row["source_summary_path"],
                "route_summary_path": row["route_summary_path"],
                "route_ids": row["route_ids"],
                "missing_evidence_action_ids": row["missing_evidence_action_ids"],
                "missing_evidence_result_scaffold_ids": row["missing_evidence_result_scaffold_ids"],
                "evidence_presence_row_ids": row["evidence_presence_row_ids"],
                "files_to_open": row["files_to_open"],
                "required_review_actions": row["required_review_actions"],
                "assignment_status": ASSIGNMENT_STATUS,
                "review_status": REVIEW_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
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
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source pipeline missing-evidence review checklist.")
    parser.add_argument("--result-scaffold", default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_RESULT_SCAFFOLD))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_review_checklist_rows(read_csv_rows(root / args.result_scaffold))
    write_csv(root / args.output, rows)
    print(f"missing_evidence_review_checklist_rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
