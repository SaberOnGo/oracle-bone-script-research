#!/usr/bin/env python3
"""Build a review checklist for second-wave outcome handoffs.

The checklist gives later reviewers a per-handoff precheck surface before any
source-engineering outcome is recorded. It does not collect evidence, assign
owners, decide rights, promote sources, import corpus rows, or make identity,
component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SECOND_WAVE_OUTCOME_HANDOFF_SCAFFOLD = (
    STAT_DIR / "129_ai-agent-source-engineering-second-wave-outcome-handoff-scaffold.json"
)
DEFAULT_OUTPUT = STAT_DIR / "130_ai-agent-source-engineering-second-wave-handoff-review-checklist.csv"

UPDATED_AT = "2026-06-19"
CHECKLIST_STATUS = "not_started"
AUTOMATION_BOUNDARY = "handoff_precheck_only_no_outcome_capture"
RESEARCH_BOUNDARY = "source_engineering_second_wave_handoff_review_checklist_not_scholarship"
CAUTION = (
    "This second-wave source-engineering handoff review checklist is a precheck "
    "surface only. It is not collected evidence, not a rights decision, not "
    "source promotion, not a corpus import, not an identity claim, not a "
    "component assignment, not an evolution-chain assignment, and not a "
    "decipherment conclusion."
)
REQUIRED_PRECHECK_STEPS = [
    "verify_handoff_row_against_129",
    "open_128_route_pack",
    "open_127_outcome_scaffold",
    "open_all_route_files_before_review",
    "verify_rights_and_risk_boundaries",
    "verify_empty_outcome_fields_before_review",
    "do_not_collect_evidence_or_record_outcome_in_checklist",
    "keep_source_promotion_and_corpus_import_blocked",
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


def row_from_handoff(index: int, handoff: dict[str, object]) -> dict[str, str]:
    return {
        "handoff_review_checklist_id": f"source-engineering-second-wave-handoff-review-checklist-{index:04d}",
        "handoff_id": str(handoff["handoff_id"]),
        "route_id": str(handoff["route_id"]),
        "second_wave_review_outcome_scaffold_id": str(handoff["second_wave_review_outcome_scaffold_id"]),
        "second_wave_review_checklist_id": str(handoff["second_wave_review_checklist_id"]),
        "second_wave_result_scaffold_id": str(handoff["second_wave_result_scaffold_id"]),
        "review_draft_id": str(handoff["review_draft_id"]),
        "continuation_task_id": str(handoff["continuation_task_id"]),
        "source_status_id": str(handoff["source_status_id"]),
        "source_id": str(handoff["source_id"]),
        "source_action_lane": str(handoff["source_action_lane"]),
        "source_first_wave_status": str(handoff["source_first_wave_status"]),
        "priority_rank": str(handoff["priority_rank"]),
        "priority_tags": join_list(handoff["priority_tags"]),
        "required_result_action": str(handoff["required_result_action"]),
        "required_review_steps": join_list(handoff["required_review_steps"]),
        "required_precheck_steps": ";".join(REQUIRED_PRECHECK_STEPS),
        "blocking_condition": str(handoff["blocking_condition"]),
        "handoff_scaffold_path": SECOND_WAVE_OUTCOME_HANDOFF_SCAFFOLD.as_posix(),
        "route_pack_path": str(handoff["route_pack_path"]),
        "outcome_scaffold_path": str(handoff["outcome_scaffold_path"]),
        "review_checklist_path": str(handoff["review_checklist_path"]),
        "result_scaffold_path": str(handoff["result_scaffold_path"]),
        "source_review_draft_manifest_path": str(handoff["source_review_draft_manifest_path"]),
        "source_checklist_path": str(handoff["source_checklist_path"]),
        "source_status_path": str(handoff["source_status_path"]),
        "draft_path": str(handoff["draft_path"]),
        "route_files_to_open": join_list(handoff["route_files_to_open"]),
        "reserved_review_fields": join_list(handoff["reserved_review_fields"]),
        "reserved_outcome_fields": join_list(handoff["reserved_outcome_fields"]),
        "checklist_status": CHECKLIST_STATUS,
        "assignment_status": str(handoff["assignment_status"]),
        "handoff_status": str(handoff["handoff_status"]),
        "route_status": str(handoff["route_status"]),
        "review_outcome_status": str(handoff["review_outcome_status"]),
        "evidence_collection_status": str(handoff["evidence_collection_status"]),
        "reviewed_evidence_paths": str(handoff["reviewed_evidence_paths"]),
        "reviewed_outcome_summary": str(handoff["reviewed_outcome_summary"]),
        "human_review_status": str(handoff["human_review_status"]),
        "rights_decision_status": str(handoff["rights_decision_status"]),
        "source_promotion_status": str(handoff["source_promotion_status"]),
        "corpus_import_status": str(handoff["corpus_import_status"]),
        "decipherment_claim_status": str(handoff["decipherment_claim_status"]),
        "identity_claim_status": str(handoff["identity_claim_status"]),
        "component_claim_status": str(handoff["component_claim_status"]),
        "evolution_claim_status": str(handoff["evolution_claim_status"]),
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
    parser = argparse.ArgumentParser(description="Build second-wave handoff review checklist.")
    parser.add_argument("--handoff-scaffold", default=str(SECOND_WAVE_OUTCOME_HANDOFF_SCAFFOLD))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_checklist_rows(read_json(root / args.handoff_scaffold))
    write_csv(root / args.output, rows)
    print(f"handoff_review_checklist_rows={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
