#!/usr/bin/env python3
"""Build a precheck checklist for core-corpus phase gap handoffs.

The checklist turns the 201 handoff scaffold into per-handoff CSV rows for
later human review. It does not collect evidence, record reviewed outcomes,
decide rights, promote sources or candidates, import corpus rows, or make
decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CORE_CORPUS_PHASE_GAP_REVIEW_HANDOFF_SCAFFOLD = (
    STAT_DIR / "201_core-corpus-phase-gap-review-handoff-scaffold.json"
)
DEFAULT_OUTPUT = STAT_DIR / "202_core-corpus-phase-gap-review-handoff-checklist.csv"
UPDATED_AT = "2026-06-20"
CHECKLIST_STATUS = "not_started"
AUTOMATION_BOUNDARY = "handoff_precheck_only_no_core_corpus_phase_gap_outcome_capture"
RESEARCH_BOUNDARY = "core_corpus_phase_gap_review_handoff_checklist_not_scholarship"
CAUTION = (
    "This core corpus phase gap review handoff checklist is a precheck surface "
    "only. It is not collected evidence, not a reviewed outcome, not a rights "
    "decision, not source or candidate promotion, not a corpus import, and not "
    "a decipherment conclusion."
)
REQUIRED_PRECHECK_STEPS = [
    "verify_handoff_row_against_201",
    "open_201_handoff_scaffold",
    "open_200_route_pack",
    "open_199_review_index",
    "open_specialized_review_checklist_row",
    "open_all_handoff_files_before_review",
    "verify_empty_reviewed_outcome_fields_before_review",
    "do_not_collect_evidence_or_record_outcome_in_checklist",
    "keep_source_candidate_promotion_and_corpus_import_blocked",
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


def unique_list(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def checklist_files_to_open(handoff: dict[str, object]) -> str:
    paths = unique_list(
        [
            CORE_CORPUS_PHASE_GAP_REVIEW_HANDOFF_SCAFFOLD.as_posix(),
            str(handoff["route_pack_path"]),
            str(handoff["review_index_path"]),
            str(handoff["specialized_checklist_path"]),
            *[str(path) for path in handoff.get("handoff_files_to_open", [])],
        ]
    )
    return ";".join(paths)


def row_from_handoff(index: int, handoff: dict[str, object]) -> dict[str, str]:
    return {
        "handoff_review_checklist_id": f"core-corpus-phase-gap-review-handoff-checklist-{index:03d}",
        "handoff_id": str(handoff["handoff_id"]),
        "route_id": str(handoff["route_id"]),
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
        "handoff_scaffold_path": CORE_CORPUS_PHASE_GAP_REVIEW_HANDOFF_SCAFFOLD.as_posix(),
        "route_pack_path": str(handoff["route_pack_path"]),
        "review_index_path": str(handoff["review_index_path"]),
        "route_files_to_open": join_list(handoff["route_files_to_open"]),
        "handoff_files_to_open": checklist_files_to_open(handoff),
        "required_review_steps": join_list(handoff["required_review_steps"]),
        "required_precheck_steps": ";".join(REQUIRED_PRECHECK_STEPS),
        "checklist_status": CHECKLIST_STATUS,
        "handoff_status": str(handoff["handoff_status"]),
        "route_status": str(handoff["route_status"]),
        "review_status": str(handoff["review_status"]),
        "human_review_status": str(handoff["human_review_status"]),
        "index_status": str(handoff["index_status"]),
        "evidence_collection_status": str(handoff["evidence_collection_status"]),
        "rights_decision_status": str(handoff["rights_decision_status"]),
        "source_promotion_status": str(handoff["source_promotion_status"]),
        "corpus_import_status": str(handoff["corpus_import_status"]),
        "decipherment_claim_status": str(handoff["decipherment_claim_status"]),
        "reviewed_evidence_paths": str(handoff["reviewed_evidence_paths"]),
        "reviewed_outcome_summary": str(handoff["reviewed_outcome_summary"]),
        "reviewed_rights_decision": str(handoff["reviewed_rights_decision"]),
        "reviewed_source_or_candidate_promotion": str(handoff["reviewed_source_or_candidate_promotion"]),
        "reviewed_corpus_import": str(handoff["reviewed_corpus_import"]),
        "reviewed_decipherment_claim": str(handoff["reviewed_decipherment_claim"]),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_checklist_rows(handoff_scaffold: dict[str, object]) -> list[dict[str, str]]:
    return [
        row_from_handoff(index, handoff)
        for index, handoff in enumerate(handoff_scaffold.get("handoffs", []), start=1)
    ]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the core corpus phase gap review handoff checklist.")
    parser.add_argument("--handoff-scaffold", default=str(CORE_CORPUS_PHASE_GAP_REVIEW_HANDOFF_SCAFFOLD))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_checklist_rows(read_json(root / args.handoff_scaffold))
    write_csv(root / args.output, rows)
    print(f"core_corpus_phase_gap_review_handoff_checklist_rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
