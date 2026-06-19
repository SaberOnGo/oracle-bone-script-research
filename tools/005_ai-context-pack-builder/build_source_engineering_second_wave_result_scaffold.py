#!/usr/bin/env python3
"""Build empty result scaffold rows for second-wave source-engineering review.

The scaffold reserves a stable place for future human reviewers to record
source-level outcomes after opening the 124 draft manifest and cited route
files. It does not collect evidence, decide rights, promote sources, import
corpus rows, or make identity, component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SECOND_WAVE_REVIEW_DRAFT_MANIFEST = (
    STAT_DIR / "124_ai-agent-source-engineering-second-wave-review-draft-manifest.csv"
)
DEFAULT_OUTPUT = STAT_DIR / "125_ai-agent-source-engineering-second-wave-result-scaffold.csv"

UPDATED_AT = "2026-06-19"
RESULT_STATUS = "not_started"
DRAFT_OPEN_STATUS = "not_opened"
ROUTE_FILES_OPEN_STATUS = "not_opened"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
COMPONENT_CLAIM_STATUS = "no_component_claim"
EVOLUTION_CLAIM_STATUS = "no_evolution_chain_claim"
RESEARCH_BOUNDARY = "source_engineering_second_wave_result_scaffold_not_scholarship"
RESERVED_REVIEW_FIELDS = ";".join(
    [
        "access_outcome",
        "checksum_outcome",
        "manifest_decision",
        "field_map_decision",
        "metadata_profile_decision",
        "safe_derived_record_decision",
        "reviewed_evidence_paths",
        "remaining_blockers",
        "required_followup",
        "human_review_notes",
    ]
)
CAUTION = (
    "This second-wave source-engineering result scaffold is empty. It is not "
    "collected evidence, not a rights decision, not source promotion, not a "
    "corpus import, not an identity claim, not a component assignment, not an "
    "evolution-chain assignment, and not a decipherment conclusion."
)

REQUIRED_ACTIONS = {
    "access_and_checksum_boundary_resolution": "record_access_and_checksum_boundary_outcomes_after_human_review",
    "metadata_profile_and_package_manifest_decision": (
        "record_metadata_profile_scope_and_package_manifest_decision_after_human_review"
    ),
    "field_map_semantics_review": "record_field_map_semantics_review_after_human_review",
    "safe_derived_record_decision": "record_safe_derived_record_decision_after_human_review",
}

OUTPUT_FIELDS = [
    "second_wave_result_scaffold_id",
    "review_draft_id",
    "continuation_task_id",
    "source_status_id",
    "source_id",
    "source_action_lane",
    "source_first_wave_status",
    "required_result_action",
    "source_review_draft_manifest_path",
    "source_checklist_path",
    "source_status_path",
    "draft_path",
    "route_files_to_open",
    "result_record_paths",
    "source_level_objective",
    "reserved_review_fields",
    "result_status",
    "draft_open_status",
    "route_files_open_status",
    "evidence_collection_status",
    "reviewed_evidence_paths",
    "access_outcome",
    "checksum_outcome",
    "manifest_decision",
    "field_map_decision",
    "metadata_profile_decision",
    "safe_derived_record_decision",
    "remaining_blockers",
    "required_followup",
    "human_review_notes",
    "human_review_status",
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


def join_route_files(row: dict[str, str]) -> str:
    values = [
        row["draft_path"],
        row["source_checklist_path"],
        row["source_status_path"],
    ]
    values.extend(part for part in row["required_inputs"].split(";") if part)
    return ";".join(dict.fromkeys(values))


def build_result_scaffold_rows(manifest_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(manifest_rows, start=1):
        rows.append(
            {
                "second_wave_result_scaffold_id": f"source-engineering-second-wave-result-scaffold-{index:04d}",
                "review_draft_id": row["review_draft_id"],
                "continuation_task_id": row["continuation_task_id"],
                "source_status_id": row["source_status_id"],
                "source_id": row["source_id"],
                "source_action_lane": row["source_action_lane"],
                "source_first_wave_status": row["source_first_wave_status"],
                "required_result_action": REQUIRED_ACTIONS.get(
                    row["source_action_lane"], "record_second_wave_source_review_outcome_after_human_review"
                ),
                "source_review_draft_manifest_path": SECOND_WAVE_REVIEW_DRAFT_MANIFEST.as_posix(),
                "source_checklist_path": row["source_checklist_path"],
                "source_status_path": row["source_status_path"],
                "draft_path": row["draft_path"],
                "route_files_to_open": join_route_files(row),
                "result_record_paths": row["result_record_paths"],
                "source_level_objective": row["source_level_objective"],
                "reserved_review_fields": RESERVED_REVIEW_FIELDS,
                "result_status": RESULT_STATUS,
                "draft_open_status": DRAFT_OPEN_STATUS,
                "route_files_open_status": ROUTE_FILES_OPEN_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "reviewed_evidence_paths": "",
                "access_outcome": "",
                "checksum_outcome": "",
                "manifest_decision": "",
                "field_map_decision": "",
                "metadata_profile_decision": "",
                "safe_derived_record_decision": "",
                "remaining_blockers": row["blocker_summary"],
                "required_followup": "open_draft_and_route_files_before_recording_reviewed_outcomes",
                "human_review_notes": "",
                "human_review_status": HUMAN_REVIEW_STATUS,
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
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build second-wave source-engineering result scaffold.")
    parser.add_argument("--manifest", default=str(SECOND_WAVE_REVIEW_DRAFT_MANIFEST))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_result_scaffold_rows(read_csv_rows(root / args.manifest))
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
