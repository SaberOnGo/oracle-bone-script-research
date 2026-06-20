#!/usr/bin/env python3
"""Build a precheck checklist for core-corpus outcome handoffs.

The checklist gives later reviewers a per-handoff precheck surface before any
core-corpus phase gap outcome is recorded. It does not collect evidence, assign
owners, decide rights, promote sources or candidates, import corpus rows, or
make identity, component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_HANDOFF_SCAFFOLD = (
    STAT_DIR / "206_core-corpus-phase-gap-review-outcome-handoff-scaffold.json"
)
CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ROUTE_PACK = (
    STAT_DIR / "205_core-corpus-phase-gap-review-outcome-route-pack.json"
)
CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_SCAFFOLD = (
    STAT_DIR / "204_core-corpus-phase-gap-review-outcome-scaffold.csv"
)
DEFAULT_OUTPUT = STAT_DIR / "207_core-corpus-phase-gap-review-outcome-handoff-checklist.csv"

UPDATED_AT = "2026-06-20"
HANDOFF_REVIEW_STATUS = "precheck_not_started"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
COMPONENT_CLAIM_STATUS = "no_component_claim"
EVOLUTION_CLAIM_STATUS = "no_evolution_chain_claim"
AUTOMATION_BOUNDARY = "precheck_only_no_core_corpus_phase_gap_outcome_capture"
RESEARCH_BOUNDARY = "core_corpus_phase_gap_review_outcome_handoff_checklist_not_scholarship"
CAUTION = (
    "This core corpus phase gap review outcome handoff checklist is a precheck "
    "checklist only. It is not collected evidence, not a reviewed outcome, not "
    "a rights decision, not source or candidate promotion, not a corpus import, "
    "not an identity claim, not a component assignment, not an evolution-chain "
    "assignment, and not a decipherment conclusion."
)
REQUIRED_PRECHECK_STEPS = [
    "open_206_outcome_handoff_scaffold",
    "open_205_outcome_route_pack",
    "open_204_outcome_scaffold",
    "open_routed_specialized_checklist",
    "open_all_route_and_handoff_files",
    "verify_empty_reviewed_outcome_fields_before_review",
    "verify_no_rights_or_promotion_decision_recorded",
    "do_not_collect_evidence_or_record_outcome_in_checklist",
    "do_not_write_ai_hypothesis_as_scholarship",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def join_list(value: object) -> str:
    if isinstance(value, list):
        return ";".join(str(item) for item in value)
    return str(value)


def unique_paths(paths: list[object]) -> str:
    seen: list[str] = []
    for path in paths:
        text = str(path)
        if text and text not in seen:
            seen.append(text)
    return ";".join(seen)


def checklist_files_to_open(handoff: dict[str, object]) -> str:
    return unique_paths(
        [
            CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_HANDOFF_SCAFFOLD.as_posix(),
            CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ROUTE_PACK.as_posix(),
            CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_SCAFFOLD.as_posix(),
            handoff.get("outcome_scaffold_path", ""),
            handoff.get("route_summary_path", ""),
            handoff.get("handoff_review_checklist_path", ""),
            handoff.get("handoff_scaffold_path", ""),
            handoff.get("route_pack_path", ""),
            handoff.get("review_index_path", ""),
            handoff.get("specialized_checklist_path", ""),
            *list(handoff.get("route_files_to_open", [])),
            *list(handoff.get("handoff_files_to_open", [])),
        ]
    )


def row_from_handoff(index: int, handoff: dict[str, object]) -> dict[str, str]:
    return {
        "outcome_handoff_checklist_id": (
            f"core-corpus-phase-gap-review-outcome-handoff-checklist-{index:03d}"
        ),
        "outcome_handoff_id": str(handoff["outcome_handoff_id"]),
        "outcome_route_id": str(handoff["outcome_route_id"]),
        "core_corpus_phase_gap_review_outcome_scaffold_id": str(
            handoff["core_corpus_phase_gap_review_outcome_scaffold_id"]
        ),
        "summary_route_id": str(handoff["summary_route_id"]),
        "handoff_review_checklist_id": str(handoff["handoff_review_checklist_id"]),
        "handoff_id": str(handoff["handoff_id"]),
        "review_route_id": str(handoff["review_route_id"]),
        "review_index_id": str(handoff["review_index_id"]),
        "gap_queue_id": str(handoff["gap_queue_id"]),
        "source_phase_row_id": str(handoff["source_phase_row_id"]),
        "corpus_area": str(handoff["corpus_area"]),
        "label_en": str(handoff["label_en"]),
        "phase_name": str(handoff["phase_name"]),
        "phase_status": str(handoff["phase_status"]),
        "gap_type": str(handoff["gap_type"]),
        "review_priority": str(handoff["review_priority"]),
        "specialized_checklist_family": str(handoff["specialized_checklist_family"]),
        "specialized_checklist_id": str(handoff["specialized_checklist_id"]),
        "specialized_checklist_path": str(handoff["specialized_checklist_path"]),
        "coverage_status": str(handoff["coverage_status"]),
        "recommended_action": str(handoff["recommended_action"]),
        "candidate_or_staging_boundary": str(handoff["candidate_or_staging_boundary"]),
        "outcome_handoff_scaffold_path": CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_HANDOFF_SCAFFOLD.as_posix(),
        "outcome_route_pack_path": CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_ROUTE_PACK.as_posix(),
        "outcome_scaffold_path": CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_SCAFFOLD.as_posix(),
        "outcome_update_target_path": str(handoff["outcome_update_target_path"]),
        "checklist_update_target_path": DEFAULT_OUTPUT.as_posix(),
        "route_summary_path": str(handoff["route_summary_path"]),
        "handoff_review_checklist_path": str(handoff["handoff_review_checklist_path"]),
        "handoff_scaffold_path": str(handoff["handoff_scaffold_path"]),
        "previous_route_pack_path": str(handoff["route_pack_path"]),
        "review_index_path": str(handoff["review_index_path"]),
        "route_files_to_open": join_list(handoff["route_files_to_open"]),
        "handoff_files_to_open": join_list(handoff["handoff_files_to_open"]),
        "checklist_files_to_open": checklist_files_to_open(handoff),
        "required_review_steps": join_list(handoff["required_review_steps"]),
        "required_precheck_steps": ";".join(REQUIRED_PRECHECK_STEPS),
        "reserved_outcome_fields": join_list(handoff["reserved_outcome_fields"]),
        "handoff_review_status": HANDOFF_REVIEW_STATUS,
        "assignment_status": str(handoff["assignment_status"]),
        "handoff_status": str(handoff["handoff_status"]),
        "handoff_objective": str(handoff["handoff_objective"]),
        "route_status": str(handoff["route_status"]),
        "review_outcome_status": str(handoff["review_outcome_status"]),
        "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
        "human_review_status": HUMAN_REVIEW_STATUS,
        "rights_decision_status": RIGHTS_DECISION_STATUS,
        "source_promotion_status": SOURCE_PROMOTION_STATUS,
        "corpus_import_status": CORPUS_IMPORT_STATUS,
        "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
        "identity_claim_status": IDENTITY_CLAIM_STATUS,
        "component_claim_status": COMPONENT_CLAIM_STATUS,
        "evolution_claim_status": EVOLUTION_CLAIM_STATUS,
        "phase_gap_outcome_reviewed": "",
        "specialized_checklist_outcome_reviewed": "",
        "reviewed_evidence_paths": "",
        "reviewed_outcome_summary": "",
        "reviewed_rights_decision": "",
        "reviewed_source_or_candidate_promotion": "",
        "reviewed_corpus_import": "",
        "reviewed_decipherment_claim": "",
        "required_followup_reviewed": "",
        "human_reviewer_id": "",
        "human_review_date": "",
        "human_review_notes": "",
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_checklist_rows(handoff_scaffold: dict[str, object]) -> list[dict[str, str]]:
    return [
        row_from_handoff(index, handoff)
        for index, handoff in enumerate(handoff_scaffold.get("handoffs", []), start=1)
        if isinstance(handoff, dict)
    ]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build core corpus outcome handoff checklist.")
    parser.add_argument("--handoff-scaffold", default=str(CORE_CORPUS_PHASE_GAP_REVIEW_OUTCOME_HANDOFF_SCAFFOLD))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_checklist_rows(read_json(root / args.handoff_scaffold))
    write_csv(root / args.output, rows)
    print(f"core_corpus_phase_gap_review_outcome_handoff_checklist_rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
