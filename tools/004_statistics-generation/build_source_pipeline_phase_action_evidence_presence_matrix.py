#!/usr/bin/env python3
"""Build source-file evidence presence rows for pipeline action file checks."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/142_source-pipeline-phase-action-evidence-presence-matrix.csv")
SOURCE_PIPELINE_PHASE_ACTION_FILE_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/141_source-pipeline-phase-action-file-checklist.csv"
)
SOURCE_PACKAGE_FILE_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv"
)
UPDATED_AT = "2026-06-19"
REVIEW_STATUS = "pending_human_review"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_evidence_presence_matrix_not_scholarship"
CAUTION = (
    "This source pipeline phase action evidence presence matrix records whether "
    "existing review files contain source-matched rows. It is not new evidence "
    "collection, not a reviewed outcome, not a rights decision, not source "
    "promotion, not a corpus import, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "evidence_presence_row_id",
    "file_check_id",
    "source_id",
    "source_type",
    "rights_status",
    "pipeline_gap_status",
    "review_lanes",
    "phase_names",
    "file_role",
    "file_to_open",
    "join_strategy",
    "matched_row_count",
    "match_status",
    "matched_ids",
    "next_review_action",
    "file_checklist_path",
    "source_summary_path",
    "route_ids",
    "result_scaffold_ids",
    "action_ids",
    "review_status",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "research_boundary",
    "caution",
    "updated_at",
]

IDENTIFIER_FIELDS = [
    "source_id",
    "download_id",
    "map_id",
    "package_file_id",
    "profile_id",
    "pipeline_row_id",
    "gap_matrix_row_id",
    "source_route_task_id",
    "source_package_id",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def package_ids_by_source(root: Path) -> dict[str, set[str]]:
    rows = read_csv_rows(root / SOURCE_PACKAGE_FILE_MANIFEST)
    package_ids: dict[str, set[str]] = {}
    for row in rows:
        package_ids.setdefault(row["source_id"], set()).add(row["source_package_id"])
    return package_ids


def row_identifier(row: dict[str, str]) -> str:
    for field in IDENTIFIER_FIELDS:
        value = row.get(field, "")
        if value:
            return value
    return ""


def match_rows(root: Path, checklist_row: dict[str, str], source_package_ids: dict[str, set[str]]) -> tuple[str, list[str]]:
    source_id = checklist_row["source_id"]
    file_path = checklist_row["file_to_open"]
    file_rows = read_csv_rows(root / file_path)
    if not file_rows:
        return "empty_file", []

    if checklist_row["file_role"] == "large_source_register":
        package_ids = source_package_ids.get(source_id, set())
        matched = [row for row in file_rows if row.get("source_package_id", "") in package_ids]
        return "source_package_id_via_package_manifest", [row_identifier(row) for row in matched]

    if "source_id" in file_rows[0]:
        matched = [row for row in file_rows if row.get("source_id", "") == source_id]
        return "source_id", [row_identifier(row) for row in matched]

    return "no_source_join_field", []


def role_presence_counts(rows: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for row in rows:
        counts.setdefault(row["file_role"], Counter())
        counts[row["file_role"]][row["match_status"]] += 1
    return {role: dict(counter) for role, counter in counts.items()}


def build_evidence_presence_rows(root: Path, checklist_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    source_package_ids = package_ids_by_source(root)
    rows: list[dict[str, str]] = []
    for checklist_row in checklist_rows:
        join_strategy, matched_ids = match_rows(root, checklist_row, source_package_ids)
        match_status = "present" if matched_ids else "missing_for_source"
        rows.append(
            {
                "evidence_presence_row_id": f"source-pipeline-phase-action-evidence-presence-{len(rows) + 1:03d}",
                "file_check_id": checklist_row["file_check_id"],
                "source_id": checklist_row["source_id"],
                "source_type": checklist_row["source_type"],
                "rights_status": checklist_row["rights_status"],
                "pipeline_gap_status": checklist_row["pipeline_gap_status"],
                "review_lanes": checklist_row["review_lanes"],
                "phase_names": checklist_row["phase_names"],
                "file_role": checklist_row["file_role"],
                "file_to_open": checklist_row["file_to_open"],
                "join_strategy": join_strategy,
                "matched_row_count": str(len(matched_ids)),
                "match_status": match_status,
                "matched_ids": ";".join(matched_ids),
                "next_review_action": (
                    "open_matched_rows_and_record_human_review_outcome"
                    if matched_ids
                    else "record_missing_source_row_or_not_applicable_after_review"
                ),
                "file_checklist_path": SOURCE_PIPELINE_PHASE_ACTION_FILE_CHECKLIST.as_posix(),
                "source_summary_path": checklist_row["source_summary_path"],
                "route_ids": checklist_row["route_ids"],
                "result_scaffold_ids": checklist_row["result_scaffold_ids"],
                "action_ids": checklist_row["action_ids"],
                "review_status": REVIEW_STATUS,
                "rights_decision_status": "no_new_rights_decision",
                "source_promotion_status": "not_promoted",
                "corpus_import_status": "not_imported",
                "decipherment_claim_status": "no_decipherment_claim",
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--file-checklist", default=str(SOURCE_PIPELINE_PHASE_ACTION_FILE_CHECKLIST))
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_evidence_presence_rows(root, read_csv_rows(root / args.file_checklist))
    write_csv(root / args.csv_output, rows)
    print(f"source_pipeline_phase_action_evidence_presence_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
