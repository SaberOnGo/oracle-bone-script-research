#!/usr/bin/env python3
"""Build empty outcome scaffold rows for missing-evidence source review.

The scaffold is the human-fillable result surface after the 154 handoff route
summary has been opened. It preserves route links and empty outcome fields
only; it does not collect evidence, decide rights, promote sources, import
corpus rows, or make identity, component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_ROUTE_SUMMARY = (
    STAT_DIR / "154_source-pipeline-phase-action-missing-evidence-review-handoff-route-summary.json"
)
DEFAULT_OUTPUT = STAT_DIR / "155_source-pipeline-phase-action-missing-evidence-review-outcome-scaffold.csv"

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
AUTOMATION_BOUNDARY = "human_gated_missing_evidence_source_review_outcome_capture"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_missing_evidence_review_outcome_scaffold_not_scholarship"
RESERVED_OUTCOME_FIELDS = ";".join(
    [
        "source_metadata_outcome_reviewed",
        "access_boundary_outcome_reviewed",
        "download_or_access_outcome_reviewed",
        "large_source_register_outcome_reviewed",
        "field_map_outcome_reviewed",
        "package_manifest_outcome_reviewed",
        "safe_derived_record_outcome_reviewed",
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
    "This source pipeline missing-evidence file is a human-gated outcome scaffold. "
    "It is not collected evidence, not a rights decision, not source promotion, "
    "not a corpus import, not an identity claim, not a component assignment, not "
    "an evolution-chain assignment, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "missing_evidence_review_outcome_scaffold_id",
    "summary_route_id",
    "handoff_review_checklist_id",
    "handoff_id",
    "route_id",
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
    "required_precheck_steps",
    "required_review_actions",
    "blocking_condition",
    "route_summary_path",
    "outcome_update_target_path",
    "handoff_scaffold_path",
    "route_pack_path",
    "review_checklist_path",
    "result_scaffold_path",
    "result_update_target_path",
    "review_draft_manifest_path",
    "draft_path",
    "source_summary_path",
    "source_gap_route_summary_path",
    "route_ids",
    "missing_evidence_action_ids",
    "missing_evidence_result_scaffold_ids",
    "evidence_presence_row_ids",
    "files_to_open",
    "handoff_files_to_open",
    "reserved_outcome_fields",
    "review_outcome_status",
    "evidence_collection_status",
    "reviewed_evidence_paths",
    "source_metadata_outcome_reviewed",
    "access_boundary_outcome_reviewed",
    "download_or_access_outcome_reviewed",
    "large_source_register_outcome_reviewed",
    "field_map_outcome_reviewed",
    "package_manifest_outcome_reviewed",
    "safe_derived_record_outcome_reviewed",
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


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def join_semicolon(value: object) -> str:
    if isinstance(value, list):
        return ";".join(str(part) for part in value if str(part))
    return str(value) if value is not None else ""


def build_outcome_scaffold_rows(route_summary: dict[str, object]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, route in enumerate(route_summary.get("routes", []), start=1):
        route_row = route if isinstance(route, dict) else {}
        rows.append(
            {
                "missing_evidence_review_outcome_scaffold_id": (
                    f"source-pipeline-missing-evidence-review-outcome-scaffold-{index:03d}"
                ),
                "summary_route_id": str(route_row["summary_route_id"]),
                "handoff_review_checklist_id": str(route_row["handoff_review_checklist_id"]),
                "handoff_id": str(route_row["handoff_id"]),
                "route_id": str(route_row["route_id"]),
                "review_checklist_id": str(route_row["review_checklist_id"]),
                "result_scaffold_id": str(route_row["result_scaffold_id"]),
                "review_draft_id": str(route_row["review_draft_id"]),
                "source_summary_id": str(route_row["source_summary_id"]),
                "source_id": str(route_row["source_id"]),
                "source_type": str(route_row["source_type"]),
                "rights_status": str(route_row["rights_status"]),
                "pipeline_gap_status": str(route_row["pipeline_gap_status"]),
                "missing_route_count": str(route_row["missing_route_count"]),
                "missing_file_role_count": str(route_row["missing_file_role_count"]),
                "missing_file_roles": join_semicolon(route_row.get("missing_file_roles")),
                "priority_rank": str(route_row["priority_rank"]),
                "priority_tags": join_semicolon(route_row.get("priority_tags")),
                "required_review_steps": join_semicolon(route_row.get("required_review_steps")),
                "required_precheck_steps": join_semicolon(route_row.get("required_precheck_steps")),
                "required_review_actions": join_semicolon(route_row.get("required_review_actions")),
                "blocking_condition": str(route_row["blocking_condition"]),
                "route_summary_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_ROUTE_SUMMARY.as_posix(),
                "outcome_update_target_path": DEFAULT_OUTPUT.as_posix(),
                "handoff_scaffold_path": str(route_row["handoff_scaffold_path"]),
                "route_pack_path": str(route_row["route_pack_path"]),
                "review_checklist_path": str(route_row["review_checklist_path"]),
                "result_scaffold_path": str(route_row["result_scaffold_path"]),
                "result_update_target_path": str(route_row["result_update_target_path"]),
                "review_draft_manifest_path": str(route_row["review_draft_manifest_path"]),
                "draft_path": str(route_row["draft_path"]),
                "source_summary_path": str(route_row["source_summary_path"]),
                "source_gap_route_summary_path": str(route_row["route_summary_path"]),
                "route_ids": join_semicolon(route_row.get("route_ids")),
                "missing_evidence_action_ids": join_semicolon(route_row.get("missing_evidence_action_ids")),
                "missing_evidence_result_scaffold_ids": join_semicolon(
                    route_row.get("missing_evidence_result_scaffold_ids")
                ),
                "evidence_presence_row_ids": join_semicolon(route_row.get("evidence_presence_row_ids")),
                "files_to_open": join_semicolon(route_row.get("files_to_open")),
                "handoff_files_to_open": join_semicolon(route_row.get("handoff_files_to_open")),
                "reserved_outcome_fields": RESERVED_OUTCOME_FIELDS,
                "review_outcome_status": REVIEW_OUTCOME_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "reviewed_evidence_paths": "",
                "source_metadata_outcome_reviewed": "",
                "access_boundary_outcome_reviewed": "",
                "download_or_access_outcome_reviewed": "",
                "large_source_register_outcome_reviewed": "",
                "field_map_outcome_reviewed": "",
                "package_manifest_outcome_reviewed": "",
                "safe_derived_record_outcome_reviewed": "",
                "reviewed_outcome_summary": "",
                "remaining_blockers_reviewed": str(route_row["blocking_condition"]),
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
    parser = argparse.ArgumentParser(description="Build missing-evidence review outcome scaffold.")
    parser.add_argument(
        "--route-summary",
        default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_ROUTE_SUMMARY),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_outcome_scaffold_rows(read_json(root / args.route_summary))
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
