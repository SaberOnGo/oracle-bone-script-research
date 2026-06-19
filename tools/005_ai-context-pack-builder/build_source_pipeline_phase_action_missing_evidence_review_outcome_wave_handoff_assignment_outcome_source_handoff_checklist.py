#!/usr/bin/env python3
"""Build source handoff precheck checklist rows from the 171 handoff scaffold."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_SCAFFOLD = (
    STAT_DIR
    / "171_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-scaffold.json"
)
DEFAULT_OUTPUT = (
    STAT_DIR
    / "172_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-checklist.csv"
)

UPDATED_AT = "2026-06-19"
CHECKLIST_STATUS = "not_started"
AUTOMATION_BOUNDARY = "assignment_outcome_source_handoff_precheck_only_no_evidence_capture"
RESEARCH_BOUNDARY = (
    "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_checklist_not_scholarship"
)
CAUTION = (
    "This source pipeline missing-evidence assignment outcome source handoff checklist is a "
    "precheck surface only. It has not collected evidence, is not a reviewed outcome, "
    "not a rights decision, not source promotion, not a corpus import, not an identity "
    "claim, not a component assignment, not an evolution-chain assignment, and not a "
    "decipherment conclusion."
)

REQUIRED_SOURCE_HANDOFF_CHECK_STEPS = [
    "verify_source_handoff_against_171",
    "open_171_source_handoff_scaffold",
    "open_170_source_route_pack",
    "open_169_source_checklist",
    "open_168_source_summary",
    "open_all_routed_source_files_before_review",
    "verify_rights_status_and_risk_note",
    "verify_empty_reviewed_evidence_and_outcome_fields",
    "do_not_collect_evidence_or_record_outcome_in_checklist",
    "keep_source_promotion_and_corpus_import_blocked",
    "do_not_write_ai_hypothesis_as_scholarship",
]

OUTPUT_FIELDS = [
    "source_handoff_checklist_id",
    "source_handoff_id",
    "source_route_id",
    "assignment_outcome_source_checklist_id",
    "assignment_outcome_source_summary_id",
    "source_id",
    "source_type",
    "rights_status",
    "pipeline_gap_status",
    "assignment_outcome_route_count",
    "handoff_wave_ids",
    "assignment_wave_ids",
    "assignment_plan_item_ids",
    "assignment_review_checklist_ids",
    "assignment_outcome_scaffold_ids",
    "assignment_outcome_route_ids",
    "missing_file_role_count",
    "missing_file_roles",
    "priority_tags",
    "required_source_review_steps",
    "required_source_handoff_check_steps",
    "blocking_condition",
    "source_handoff_scaffold_path",
    "source_route_pack_path",
    "source_checklist_path",
    "source_summary_path",
    "assignment_outcome_route_summary_path",
    "source_files_to_open",
    "source_handoff_files_to_open",
    "draft_paths",
    "source_review_status",
    "checklist_status",
    "assignment_status",
    "handoff_status",
    "handoff_objective",
    "route_status",
    "assignment_review_status_counts",
    "review_outcome_status_counts",
    "evidence_collection_status_counts",
    "human_review_status_counts",
    "evidence_collection_status",
    "human_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "identity_claim_status",
    "component_claim_status",
    "evolution_claim_status",
    "reviewed_evidence_paths",
    "reviewed_outcome_summary",
    "automation_boundary",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def join_list(value: object) -> str:
    if isinstance(value, list):
        return ";".join(str(item) for item in value if item)
    return str(value) if value is not None else ""


def unique_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return ";".join(seen)


def source_handoff_files_to_open(handoff: dict[str, object]) -> str:
    files: list[str] = [
        SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_SCAFFOLD.as_posix(),
        str(handoff.get("source_route_pack_path", "")),
        str(handoff.get("source_checklist_path", "")),
        str(handoff.get("source_summary_path", "")),
        str(handoff.get("assignment_outcome_route_summary_path", "")),
    ]
    for field in ("source_files_to_open", "draft_paths"):
        values = handoff.get(field, [])
        if isinstance(values, list):
            files.extend(str(value) for value in values if value)
    return unique_join(files)


def row_from_source_handoff(index: int, handoff: dict[str, object]) -> dict[str, str]:
    return {
        "source_handoff_checklist_id": (
            "source-pipeline-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-checklist-"
            f"{index:03d}"
        ),
        "source_handoff_id": join_list(handoff.get("source_handoff_id")),
        "source_route_id": join_list(handoff.get("source_route_id")),
        "assignment_outcome_source_checklist_id": join_list(handoff.get("assignment_outcome_source_checklist_id")),
        "assignment_outcome_source_summary_id": join_list(handoff.get("assignment_outcome_source_summary_id")),
        "source_id": join_list(handoff.get("source_id")),
        "source_type": join_list(handoff.get("source_type")),
        "rights_status": join_list(handoff.get("rights_status")),
        "pipeline_gap_status": join_list(handoff.get("pipeline_gap_status")),
        "assignment_outcome_route_count": join_list(handoff.get("assignment_outcome_route_count")),
        "handoff_wave_ids": join_list(handoff.get("handoff_wave_ids")),
        "assignment_wave_ids": join_list(handoff.get("assignment_wave_ids")),
        "assignment_plan_item_ids": join_list(handoff.get("assignment_plan_item_ids")),
        "assignment_review_checklist_ids": join_list(handoff.get("assignment_review_checklist_ids")),
        "assignment_outcome_scaffold_ids": join_list(handoff.get("assignment_outcome_scaffold_ids")),
        "assignment_outcome_route_ids": join_list(handoff.get("assignment_outcome_route_ids")),
        "missing_file_role_count": join_list(handoff.get("missing_file_role_count")),
        "missing_file_roles": join_list(handoff.get("missing_file_roles")),
        "priority_tags": join_list(handoff.get("priority_tags")),
        "required_source_review_steps": join_list(handoff.get("required_source_review_steps")),
        "required_source_handoff_check_steps": ";".join(REQUIRED_SOURCE_HANDOFF_CHECK_STEPS),
        "blocking_condition": join_list(handoff.get("blocking_condition")),
        "source_handoff_scaffold_path": (
            SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_SCAFFOLD.as_posix()
        ),
        "source_route_pack_path": join_list(handoff.get("source_route_pack_path")),
        "source_checklist_path": join_list(handoff.get("source_checklist_path")),
        "source_summary_path": join_list(handoff.get("source_summary_path")),
        "assignment_outcome_route_summary_path": join_list(handoff.get("assignment_outcome_route_summary_path")),
        "source_files_to_open": join_list(handoff.get("source_files_to_open")),
        "source_handoff_files_to_open": source_handoff_files_to_open(handoff),
        "draft_paths": join_list(handoff.get("draft_paths")),
        "source_review_status": join_list(handoff.get("source_review_status")),
        "checklist_status": CHECKLIST_STATUS,
        "assignment_status": join_list(handoff.get("assignment_status")),
        "handoff_status": join_list(handoff.get("handoff_status")),
        "handoff_objective": join_list(handoff.get("handoff_objective")),
        "route_status": join_list(handoff.get("route_status")),
        "assignment_review_status_counts": join_list(handoff.get("assignment_review_status_counts")),
        "review_outcome_status_counts": join_list(handoff.get("review_outcome_status_counts")),
        "evidence_collection_status_counts": join_list(handoff.get("evidence_collection_status_counts")),
        "human_review_status_counts": join_list(handoff.get("human_review_status_counts")),
        "evidence_collection_status": join_list(handoff.get("evidence_collection_status")),
        "human_review_status": join_list(handoff.get("human_review_status")),
        "rights_decision_status": join_list(handoff.get("rights_decision_status")),
        "source_promotion_status": join_list(handoff.get("source_promotion_status")),
        "corpus_import_status": join_list(handoff.get("corpus_import_status")),
        "decipherment_claim_status": join_list(handoff.get("decipherment_claim_status")),
        "identity_claim_status": join_list(handoff.get("identity_claim_status")),
        "component_claim_status": join_list(handoff.get("component_claim_status")),
        "evolution_claim_status": join_list(handoff.get("evolution_claim_status")),
        "reviewed_evidence_paths": "",
        "reviewed_outcome_summary": "",
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_source_handoff_checklist_rows(scaffold: dict[str, object]) -> list[dict[str, str]]:
    handoffs = scaffold.get("handoffs", [])
    if not isinstance(handoffs, list):
        return []
    return [
        row_from_source_handoff(index, handoff)
        for index, handoff in enumerate(handoffs, start=1)
        if isinstance(handoff, dict)
    ]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build assignment outcome source handoff checklist.")
    parser.add_argument(
        "--source-handoff-scaffold",
        default=str(
            SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_SCAFFOLD
        ),
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_source_handoff_checklist_rows(read_json(root / args.source_handoff_scaffold))
    write_csv(root / args.output, rows)
    print(f"assignment_outcome_source_handoff_checklist_rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
