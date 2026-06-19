#!/usr/bin/env python3
"""Build source-level result scaffold rows for missing-evidence review drafts.

The scaffold is a human-fillable outcome surface after the 148 Markdown drafts
are opened. It preserves source routing and empty reviewed-result fields only;
it does not collect evidence, decide rights, promote sources, import corpus
rows, or make identity, component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_DRAFT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/"
    "148_source-pipeline-phase-action-missing-evidence-review-draft-manifest.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "149_source-pipeline-phase-action-missing-evidence-result-scaffold.csv"
)

UPDATED_AT = "2026-06-19"
RESULT_STATUS = "not_started"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
COMPONENT_CLAIM_STATUS = "no_component_claim"
EVOLUTION_CLAIM_STATUS = "no_evolution_chain_claim"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_missing_evidence_result_scaffold_not_scholarship"
CAUTION = (
    "This source pipeline missing-evidence result scaffold is human-fillable "
    "and empty. It is not collected evidence, not a reviewed outcome, not a "
    "rights decision, not source promotion, not a corpus import, not an "
    "identity claim, not a component assignment, not an evolution-chain "
    "assignment, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
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
    "draft_path",
    "review_draft_manifest_path",
    "source_summary_path",
    "route_summary_path",
    "route_ids",
    "missing_evidence_action_ids",
    "missing_evidence_result_scaffold_ids",
    "evidence_presence_row_ids",
    "files_to_open",
    "required_review_actions",
    "result_status",
    "evidence_collection_status",
    "human_review_status",
    "missing_role_applicability_reviewed",
    "target_source_file_action_reviewed",
    "large_source_register_action_reviewed",
    "metadata_profile_action_reviewed",
    "field_map_action_reviewed",
    "package_manifest_action_reviewed",
    "reviewed_evidence_paths",
    "reviewed_outcome_summary",
    "remaining_blockers_reviewed",
    "required_followup_reviewed",
    "reviewer_notes",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "identity_claim_status",
    "component_claim_status",
    "evolution_claim_status",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def build_result_scaffold_rows(manifest_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(manifest_rows, start=1):
        rows.append(
            {
                "result_scaffold_id": f"source-pipeline-missing-evidence-result-scaffold-{index:03d}",
                "review_draft_id": row["review_draft_id"],
                "source_summary_id": row["source_summary_id"],
                "source_id": row["source_id"],
                "source_type": row["source_type"],
                "rights_status": row["rights_status"],
                "pipeline_gap_status": row["pipeline_gap_status"],
                "missing_route_count": row["missing_route_count"],
                "missing_file_role_count": row["missing_file_role_count"],
                "missing_file_roles": row["missing_file_roles"],
                "draft_path": row["draft_path"],
                "review_draft_manifest_path": (
                    SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_DRAFT_MANIFEST.as_posix()
                ),
                "source_summary_path": row["source_summary_path"],
                "route_summary_path": row["route_summary_path"],
                "route_ids": row["route_ids"],
                "missing_evidence_action_ids": row["missing_evidence_action_ids"],
                "missing_evidence_result_scaffold_ids": row["missing_evidence_result_scaffold_ids"],
                "evidence_presence_row_ids": row["evidence_presence_row_ids"],
                "files_to_open": row["files_to_open"],
                "required_review_actions": row["required_review_actions"],
                "result_status": RESULT_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "human_review_status": HUMAN_REVIEW_STATUS,
                "missing_role_applicability_reviewed": "",
                "target_source_file_action_reviewed": "",
                "large_source_register_action_reviewed": "",
                "metadata_profile_action_reviewed": "",
                "field_map_action_reviewed": "",
                "package_manifest_action_reviewed": "",
                "reviewed_evidence_paths": "",
                "reviewed_outcome_summary": "",
                "remaining_blockers_reviewed": "",
                "required_followup_reviewed": "",
                "reviewer_notes": "",
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "corpus_import_status": CORPUS_IMPORT_STATUS,
                "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "component_claim_status": COMPONENT_CLAIM_STATUS,
                "evolution_claim_status": EVOLUTION_CLAIM_STATUS,
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
    parser = argparse.ArgumentParser(description="Build missing-evidence review result scaffold.")
    parser.add_argument("--manifest", default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_DRAFT_MANIFEST))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_result_scaffold_rows(read_csv_rows(root / args.manifest))
    write_csv(root / args.output, rows)
    print(f"missing_evidence_review_result_scaffold_rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
