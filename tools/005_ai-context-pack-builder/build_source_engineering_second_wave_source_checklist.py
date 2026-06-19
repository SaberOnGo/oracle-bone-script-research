#!/usr/bin/env python3
"""Build source-level continuation checklist from first-wave source status.

The checklist turns the 122 source status rollup into one human-gated
continuation task per source. It is metadata-only routing: it does not decide
rights, promote sources, import corpus records, or make identity, component,
evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_STATUS = STAT_DIR / "122_ai-agent-source-engineering-first-wave-source-status.csv"
DEFAULT_OUTPUT = STAT_DIR / "123_ai-agent-source-engineering-second-wave-source-checklist.csv"

UPDATED_AT = "2026-06-19"
ACTION_STATUS = "ready_for_human_source_engineering_review"
HUMAN_REVIEW_STATUS = "pending_human_review"
AUTOMATION_BOUNDARY = "human_gated_metadata_only_followup"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
COMPONENT_CLAIM_STATUS = "no_component_claim"
EVOLUTION_CLAIM_STATUS = "no_evolution_chain_claim"
RESEARCH_BOUNDARY = "source_engineering_second_wave_source_checklist_metadata-only_not_scholarship"
CAUTION = (
    "Second-wave source checklist only; this is metadata-only routing, not a "
    "new download, not checksum recalculation, not a rights decision, not "
    "source promotion, not a corpus import, not an identity claim, not a "
    "component assignment, not an evolution-chain assignment, and not a "
    "decipherment conclusion."
)

LANE_BY_STATUS = {
    "access_blocked_metadata_only_boundary_pending_human_decision": (
        "access_and_checksum_boundary_resolution",
        "open_access_and_checksum_records_then_record_human_boundary_decision",
    ),
    "downloaded_graph_derivative_metadata_profile_and_manifest_decisions_pending": (
        "metadata_profile_and_package_manifest_decision",
        "define_metadata_profile_scope_and_package_manifest_decision_before_import",
    ),
    "metadata_profile_available_field_map_semantics_pending": (
        "field_map_semantics_review",
        "review_field_map_semantics_and_rights_boundary_before_import",
    ),
    "metadata_profiles_available_safe_derived_decision_pending": (
        "safe_derived_record_decision",
        "decide_safe_derived_record_staging_or_review_queue_after_source_marked_review",
    ),
}

OUTPUT_FIELDS = [
    "continuation_task_id",
    "source_status_id",
    "source_id",
    "source_first_wave_status",
    "priority_rank",
    "source_action_lane",
    "source_level_objective",
    "blocker_summary",
    "next_recommended_action",
    "first_wave_result_ids",
    "followup_task_ids",
    "source_status_path",
    "result_record_paths",
    "reviewed_evidence_paths",
    "required_inputs",
    "expected_review_output_path",
    "action_status",
    "human_review_status",
    "automation_boundary",
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


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_action(row: dict[str, str]) -> tuple[str, str]:
    status = row["source_first_wave_status"]
    if status not in LANE_BY_STATUS:
        return (
            "source_status_followup_review",
            "open_source_status_rollup_and_determine_next_human_gated_source_engineering_action",
        )
    return LANE_BY_STATUS[status]


def expected_review_output_path(index: int, source_id: str, lane: str) -> str:
    return (
        "doc/public/user_research/009_source-engineering-gap-review-queues/"
        f"source-status-{index:04d}_{source_id}_{lane}_second-wave-review.md"
    )


def build_checklist_rows(source_status_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(source_status_rows, start=1):
        lane, objective_prefix = source_action(row)
        objective = ";".join(
            [
                objective_prefix,
                row["next_recommended_action"],
                "keep_metadata_only_boundary",
                "record_human_review_before_any_source_promotion_or_import",
            ]
        )
        rows.append(
            {
                "continuation_task_id": f"source-engineering-second-wave-source-checklist-{index:04d}",
                "source_status_id": row["source_status_id"],
                "source_id": row["source_id"],
                "source_first_wave_status": row["source_first_wave_status"],
                "priority_rank": str(index),
                "source_action_lane": lane,
                "source_level_objective": objective,
                "blocker_summary": row["remaining_blockers"],
                "next_recommended_action": row["next_recommended_action"],
                "first_wave_result_ids": row["first_wave_result_ids"],
                "followup_task_ids": row["followup_task_ids"],
                "source_status_path": SOURCE_STATUS.as_posix(),
                "result_record_paths": row["result_record_paths"],
                "reviewed_evidence_paths": row["reviewed_evidence_paths"],
                "required_inputs": ";".join(
                    [
                        SOURCE_STATUS.as_posix(),
                        row["result_record_paths"],
                        row["reviewed_evidence_paths"],
                    ]
                ),
                "expected_review_output_path": expected_review_output_path(index, row["source_id"], lane),
                "action_status": ACTION_STATUS,
                "human_review_status": HUMAN_REVIEW_STATUS,
                "automation_boundary": AUTOMATION_BOUNDARY,
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build second-wave source-level checklist.")
    parser.add_argument("--source-status", default=str(SOURCE_STATUS))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_checklist_rows(read_csv_rows(root / args.source_status))
    write_csv(root / args.output, rows)
    print(f"continuation_task_count={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
