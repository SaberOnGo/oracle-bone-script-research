#!/usr/bin/env python3
"""Build empty outcome scaffold rows for core-corpus phase gap review.

The scaffold is the human-fillable result surface after the 203 handoff route
summary has been opened. It preserves route links and empty outcome fields
only; it does not collect evidence, decide rights, promote sources or
candidates, import corpus rows, or make identity, component, evolution, or
decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CORE_CORPUS_PHASE_GAP_REVIEW_HANDOFF_ROUTE_SUMMARY = (
    STAT_DIR / "203_core-corpus-phase-gap-review-handoff-route-summary.json"
)
DEFAULT_OUTPUT = STAT_DIR / "204_core-corpus-phase-gap-review-outcome-scaffold.csv"

UPDATED_AT = "2026-06-20"
REVIEW_OUTCOME_STATUS = "not_started"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
COMPONENT_CLAIM_STATUS = "no_component_claim"
EVOLUTION_CLAIM_STATUS = "no_evolution_chain_claim"
AUTOMATION_BOUNDARY = "human_gated_core_corpus_phase_gap_review_outcome_capture"
RESEARCH_BOUNDARY = "core_corpus_phase_gap_review_outcome_scaffold_not_scholarship"
RESERVED_OUTCOME_FIELDS = ";".join(
    [
        "phase_gap_outcome_reviewed",
        "specialized_checklist_outcome_reviewed",
        "reviewed_evidence_paths",
        "reviewed_outcome_summary",
        "reviewed_rights_decision",
        "reviewed_source_or_candidate_promotion",
        "reviewed_corpus_import",
        "reviewed_decipherment_claim",
        "remaining_blockers_reviewed",
        "required_followup_reviewed",
        "human_reviewer_id",
        "human_review_date",
        "human_review_notes",
    ]
)
CAUTION = (
    "This core corpus phase gap review file is a human-gated outcome scaffold. "
    "It is not collected evidence, not a rights decision, not source or "
    "candidate promotion, not a corpus import, not an identity claim, not a "
    "component assignment, not an evolution-chain assignment, and not a "
    "decipherment conclusion."
)

OUTPUT_FIELDS = [
    "core_corpus_phase_gap_review_outcome_scaffold_id",
    "summary_route_id",
    "handoff_review_checklist_id",
    "handoff_id",
    "route_id",
    "review_index_id",
    "gap_queue_id",
    "source_phase_row_id",
    "corpus_area",
    "label_en",
    "phase_name",
    "phase_status",
    "gap_type",
    "review_priority",
    "specialized_checklist_family",
    "specialized_checklist_id",
    "specialized_checklist_path",
    "coverage_status",
    "recommended_action",
    "candidate_or_staging_boundary",
    "route_summary_path",
    "outcome_update_target_path",
    "handoff_review_checklist_path",
    "handoff_scaffold_path",
    "route_pack_path",
    "review_index_path",
    "route_files_to_open",
    "handoff_files_to_open",
    "required_review_steps",
    "required_precheck_steps",
    "reserved_outcome_fields",
    "review_outcome_status",
    "evidence_collection_status",
    "phase_gap_outcome_reviewed",
    "specialized_checklist_outcome_reviewed",
    "reviewed_evidence_paths",
    "reviewed_outcome_summary",
    "reviewed_rights_decision",
    "reviewed_source_or_candidate_promotion",
    "reviewed_corpus_import",
    "reviewed_decipherment_claim",
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
                "core_corpus_phase_gap_review_outcome_scaffold_id": (
                    f"core-corpus-phase-gap-review-outcome-scaffold-{index:03d}"
                ),
                "summary_route_id": str(route_row["summary_route_id"]),
                "handoff_review_checklist_id": str(route_row["handoff_review_checklist_id"]),
                "handoff_id": str(route_row["handoff_id"]),
                "route_id": str(route_row["route_id"]),
                "review_index_id": str(route_row["review_index_id"]),
                "gap_queue_id": str(route_row["gap_queue_id"]),
                "source_phase_row_id": str(route_row["source_phase_row_id"]),
                "corpus_area": str(route_row["corpus_area"]),
                "label_en": str(route_row["label_en"]),
                "phase_name": str(route_row["phase_name"]),
                "phase_status": str(route_row["phase_status"]),
                "gap_type": str(route_row["gap_type"]),
                "review_priority": str(route_row["review_priority"]),
                "specialized_checklist_family": str(route_row["specialized_checklist_family"]),
                "specialized_checklist_id": str(route_row["specialized_checklist_id"]),
                "specialized_checklist_path": str(route_row["specialized_checklist_path"]),
                "coverage_status": str(route_row["coverage_status"]),
                "recommended_action": str(route_row["recommended_action"]),
                "candidate_or_staging_boundary": str(route_row["candidate_or_staging_boundary"]),
                "route_summary_path": CORE_CORPUS_PHASE_GAP_REVIEW_HANDOFF_ROUTE_SUMMARY.as_posix(),
                "outcome_update_target_path": DEFAULT_OUTPUT.as_posix(),
                "handoff_review_checklist_path": str(route_row["handoff_review_checklist_path"]),
                "handoff_scaffold_path": str(route_row["handoff_scaffold_path"]),
                "route_pack_path": str(route_row["route_pack_path"]),
                "review_index_path": str(route_row["review_index_path"]),
                "route_files_to_open": join_semicolon(route_row.get("route_files_to_open")),
                "handoff_files_to_open": join_semicolon(route_row.get("handoff_files_to_open")),
                "required_review_steps": join_semicolon(route_row.get("required_review_steps")),
                "required_precheck_steps": join_semicolon(route_row.get("required_precheck_steps")),
                "reserved_outcome_fields": RESERVED_OUTCOME_FIELDS,
                "review_outcome_status": REVIEW_OUTCOME_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "phase_gap_outcome_reviewed": "",
                "specialized_checklist_outcome_reviewed": "",
                "reviewed_evidence_paths": "",
                "reviewed_outcome_summary": "",
                "reviewed_rights_decision": "",
                "reviewed_source_or_candidate_promotion": "",
                "reviewed_corpus_import": "",
                "reviewed_decipherment_claim": "",
                "remaining_blockers_reviewed": "open_all_routed_files_before_recording_core_corpus_phase_gap_outcomes",
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
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the core corpus phase gap review outcome scaffold.")
    parser.add_argument("--route-summary", default=str(CORE_CORPUS_PHASE_GAP_REVIEW_HANDOFF_ROUTE_SUMMARY))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_outcome_scaffold_rows(read_json(root / args.route_summary))
    write_csv(root / args.output, rows)
    print(f"core_corpus_phase_gap_review_outcome_scaffold_rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
