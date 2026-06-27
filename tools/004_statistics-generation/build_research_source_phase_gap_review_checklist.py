#!/usr/bin/env python3
"""Build a research-source phase gap review checklist.

This bridges core-corpus phase gaps to the existing source-pipeline assignment
checklist. It is a preprocessing navigation surface only.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


CORE_CORPUS_PHASE_GAP_ACTION_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/192_core-corpus-phase-gap-action-queue.csv"
)
SOURCE_PIPELINE_ASSIGNMENT_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/"
    "185_source-pipeline-missing-evidence-outcome-routes-assignment-checklist.csv"
)
OUTPUT_CSV = Path(
    "corpus/009_statistics-and-derived-features/193_research-source-phase-gap-review-checklist.csv"
)
UPDATED_AT = "2026-06-20"
CLAIM_BOUNDARY = "research_source_phase_gap_review_checklist_not_review_outcome_not_scholarship"
CAUTION = (
    "This research source phase gap review checklist only routes high-priority "
    "research-source preprocessing gaps to existing source-pipeline assignment "
    "groups. It does not collect evidence, record reviewed outcomes, decide "
    "rights, promote sources, import corpus records, or make decipherment claims."
)
REQUIRED_REVIEW_STEPS = (
    "open_193_research_source_phase_gap_review_checklist;"
    "open_192_core_corpus_phase_gap_action_queue;"
    "open_185_source_pipeline_assignment_checklist;"
    "confirm_assignment_groups_are_not_started;"
    "confirm_reviewed_evidence_paths_empty;"
    "confirm_no_rights_decision;"
    "confirm_no_source_promotion;"
    "confirm_no_corpus_import;"
    "confirm_no_decipherment_claim;"
    "do_not_collect_evidence_or_record_outcome_in_this_checklist"
)
REQUIRED_SOURCE_PROVENANCE_SLOTS = (
    "source_system;"
    "source_object;"
    "access_or_download_record;"
    "access_date;"
    "package_name;"
    "provider;"
    "file_name;"
    "file_size;"
    "checksum;"
    "package_manifest;"
    "rights_status;"
    "risk_note;"
    "public_commit_decision;"
    "field_map;"
    "extraction_note;"
    "derived_paths;"
    "review_status"
)
SOURCE_CONTEXT_FIELDS_TO_VERIFY = (
    "source_id;"
    "source_register_row;"
    "large_source_register_row;"
    "download_log_row;"
    "package_manifest_route;"
    "field_map_route;"
    "rights_status;"
    "risk_note;"
    "review_status"
)
CONCRETE_NEXT_CHECKS = (
    "Which source system, provider, catalog, book, paper, museum, or URL supplied this source?;"
    "Which access or download record, access date, package name, file size, and checksum locate it?;"
    "Which package manifest, field map, extraction note, and derived paths let a reviewer audit it?;"
    "Which rights status, risk note, and public-commit decision are visible beside it?;"
    "Which missing source, license, checksum, field, or review status remains?"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_values(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def unique_join(values: list[str]) -> str:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return ";".join(output)


def path_text(path: Path) -> str:
    return path.as_posix()


def build_checklist_rows(root: Path) -> list[dict[str, str]]:
    gap_rows = [
        row
        for row in read_csv_rows(root / CORE_CORPUS_PHASE_GAP_ACTION_QUEUE)
        if row["corpus_area"] == "research_sources_and_bibliography"
    ]
    assignment_rows = read_csv_rows(root / SOURCE_PIPELINE_ASSIGNMENT_CHECKLIST)

    assignment_ids = [row["assignment_checklist_id"] for row in assignment_rows]
    pipeline_gap_statuses = [row["pipeline_gap_status"] for row in assignment_rows]
    source_ids = [source_id for row in assignment_rows for source_id in split_values(row["source_ids"])]
    route_counts = [f'{row["assignment_checklist_id"]}:{row["route_count"]}' for row in assignment_rows]
    files_to_open = unique_join(
        [
            path_text(OUTPUT_CSV),
            path_text(CORE_CORPUS_PHASE_GAP_ACTION_QUEUE),
            path_text(SOURCE_PIPELINE_ASSIGNMENT_CHECKLIST),
        ]
        + [path for row in gap_rows for path in split_values(row["phase_evidence_paths"])]
    )

    rows: list[dict[str, str]] = []
    for gap_row in gap_rows:
        rows.append(
            {
                "review_checklist_id": f"research-source-phase-gap-review-{len(rows) + 1:03d}",
                "gap_queue_id": gap_row["gap_queue_id"],
                "source_phase_row_id": gap_row["source_phase_row_id"],
                "corpus_area": gap_row["corpus_area"],
                "phase_name": gap_row["phase_name"],
                "phase_status": gap_row["phase_status"],
                "gap_type": gap_row["gap_type"],
                "review_priority": gap_row["review_priority"],
                "review_status": "needs_human_review",
                "assignment_group_count": str(len(assignment_rows)),
                "assignment_source_count_total": str(len(set(source_ids))),
                "assignment_checklist_ids": ";".join(assignment_ids),
                "pipeline_gap_statuses": unique_join(pipeline_gap_statuses),
                "source_ids": ";".join(sorted(set(source_ids))),
                "assignment_route_counts": ";".join(route_counts),
                "assignment_checklist_path": path_text(SOURCE_PIPELINE_ASSIGNMENT_CHECKLIST),
                "files_to_open": files_to_open,
                "required_review_steps": REQUIRED_REVIEW_STEPS,
                "required_source_provenance_slots": REQUIRED_SOURCE_PROVENANCE_SLOTS,
                "source_context_fields_to_verify": SOURCE_CONTEXT_FIELDS_TO_VERIFY,
                "concrete_next_checks": CONCRETE_NEXT_CHECKS,
                "recommended_action": gap_row["recommended_action"],
                "candidate_or_staging_boundary": gap_row["candidate_or_staging_boundary"],
                "claim_boundary": CLAIM_BOUNDARY,
                "evidence_collection_status": "not_collected",
                "rights_decision_status": "no_rights_decision",
                "source_promotion_status": "not_promoted",
                "corpus_import_status": "not_imported",
                "decipherment_claim_status": "no_decipherment_claim",
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_checklist_rows(root)
    write_csv(root / args.csv_output, rows)
    print(f"research_source_phase_gap_review_checklist_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
