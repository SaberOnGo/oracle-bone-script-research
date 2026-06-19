#!/usr/bin/env python3
"""Build review checklist rows for second-wave source-engineering scaffolds.

The checklist tells a future human reviewer which 125 scaffold row, draft, and
route files to open before recording any source-engineering outcome. It does
not collect evidence, decide rights, promote sources, import corpus rows, or
make identity, component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SECOND_WAVE_RESULT_SCAFFOLD = STAT_DIR / "125_ai-agent-source-engineering-second-wave-result-scaffold.csv"
DEFAULT_OUTPUT = STAT_DIR / "126_ai-agent-source-engineering-second-wave-review-checklist.csv"

UPDATED_AT = "2026-06-19"
ASSIGNMENT_STATUS = "unassigned"
REVIEW_STATUS = "needs_second_wave_source_review"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
COMPONENT_CLAIM_STATUS = "no_component_claim"
EVOLUTION_CLAIM_STATUS = "no_evolution_chain_claim"
AUTOMATION_BOUNDARY = "human_gated_second_wave_source_engineering_review"
RESEARCH_BOUNDARY = "source_engineering_second_wave_review_checklist_not_scholarship"
CAUTION = (
    "This second-wave source-engineering checklist is a human-gated review "
    "route only. It is not collected evidence, not a rights decision, not "
    "source promotion, not a corpus import, not an identity claim, not a "
    "component assignment, not an evolution-chain assignment, and not a "
    "decipherment conclusion."
)

COMMON_REVIEW_STEPS = [
    "open_second_wave_result_scaffold",
    "open_second_wave_review_draft",
    "open_source_status_rollup",
    "open_cited_route_files",
    "verify_rights_and_risk_boundaries",
    "record_only_reviewed_metadata_outcomes",
    "do_not_import_or_promote_until_reviewed",
    "do_not_write_ai_hypothesis_as_scholarship",
]

REQUIRED_REVIEW_STEPS_BY_LANE = {
    "access_and_checksum_boundary_resolution": [
        *COMMON_REVIEW_STEPS,
        "verify_access_and_checksum_boundary",
        "keep_download_failure_and_rights_decision_separate",
    ],
    "metadata_profile_and_package_manifest_decision": [
        *COMMON_REVIEW_STEPS,
        "verify_metadata_profile_scope",
        "verify_package_manifest_or_not_applicable_boundary",
    ],
    "field_map_semantics_review": [
        *COMMON_REVIEW_STEPS,
        "verify_field_map_semantics_before_import",
        "keep_field_map_review_separate_from_corpus_import",
    ],
    "safe_derived_record_decision": [
        *COMMON_REVIEW_STEPS,
        "verify_safe_derived_record_boundary",
        "keep_source_promotion_pending_until_human_review",
    ],
}

OUTPUT_FIELDS = [
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
    "result_scaffold_path",
    "result_update_target_path",
    "source_review_draft_manifest_path",
    "source_checklist_path",
    "source_status_path",
    "draft_path",
    "route_files_to_open",
    "reserved_review_fields",
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


def priority_tags(row: dict[str, str]) -> str:
    tags = [f"source:{row['source_id']}", f"lane:{row['source_action_lane']}", "second_wave"]
    if row["source_action_lane"] in {
        "access_and_checksum_boundary_resolution",
        "metadata_profile_and_package_manifest_decision",
    }:
        tags.append("provenance_first")
    if row["source_action_lane"] == "field_map_semantics_review":
        tags.append("field_map_boundary")
    if row["source_action_lane"] == "safe_derived_record_decision":
        tags.append("promotion_boundary")
    return ";".join(tags)


def build_review_checklist_rows(scaffold_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(scaffold_rows, start=1):
        lane = row["source_action_lane"]
        rows.append(
            {
                "second_wave_review_checklist_id": f"source-engineering-second-wave-review-checklist-{index:04d}",
                "second_wave_result_scaffold_id": row["second_wave_result_scaffold_id"],
                "review_draft_id": row["review_draft_id"],
                "continuation_task_id": row["continuation_task_id"],
                "source_status_id": row["source_status_id"],
                "source_id": row["source_id"],
                "source_action_lane": lane,
                "source_first_wave_status": row["source_first_wave_status"],
                "priority_rank": str(index),
                "priority_tags": priority_tags(row),
                "required_result_action": row["required_result_action"],
                "required_review_steps": ";".join(
                    REQUIRED_REVIEW_STEPS_BY_LANE.get(lane, COMMON_REVIEW_STEPS)
                ),
                "blocking_condition": row["remaining_blockers"],
                "result_scaffold_path": SECOND_WAVE_RESULT_SCAFFOLD.as_posix(),
                "result_update_target_path": SECOND_WAVE_RESULT_SCAFFOLD.as_posix(),
                "source_review_draft_manifest_path": row["source_review_draft_manifest_path"],
                "source_checklist_path": row["source_checklist_path"],
                "source_status_path": row["source_status_path"],
                "draft_path": row["draft_path"],
                "route_files_to_open": row["route_files_to_open"],
                "reserved_review_fields": row["reserved_review_fields"],
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
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build second-wave source-engineering review checklist.")
    parser.add_argument("--result-scaffold", default=str(SECOND_WAVE_RESULT_SCAFFOLD))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_review_checklist_rows(read_csv_rows(root / args.result_scaffold))
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
