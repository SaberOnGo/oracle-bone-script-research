#!/usr/bin/env python3
"""Build source-level gap summaries from evidence presence rows."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/143_source-pipeline-phase-action-evidence-gap-summary.csv")
SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_PRESENCE_MATRIX = Path(
    "corpus/009_statistics-and-derived-features/142_source-pipeline-phase-action-evidence-presence-matrix.csv"
)
UPDATED_AT = "2026-06-19"
REVIEW_STATUS = "pending_human_review"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_evidence_gap_summary_not_scholarship"
CAUTION = (
    "This source pipeline phase action evidence gap summary only rolls up "
    "existing source-file presence and missing-row signals. It is not new "
    "evidence collection, not a reviewed outcome, not a rights decision, not "
    "source promotion, not a corpus import, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "evidence_gap_summary_id",
    "source_id",
    "source_type",
    "rights_status",
    "pipeline_gap_status",
    "review_lanes",
    "phase_names",
    "present_file_role_count",
    "missing_file_role_count",
    "not_applicable_file_role_count",
    "total_file_role_count",
    "total_matched_row_count",
    "present_file_roles",
    "missing_file_roles",
    "not_applicable_file_roles",
    "gap_status",
    "next_review_action",
    "evidence_presence_matrix_path",
    "evidence_presence_row_ids",
    "missing_evidence_presence_row_ids",
    "review_status",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "research_boundary",
    "caution",
    "updated_at",
]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def sorted_join(values: list[str]) -> str:
    return ";".join(sorted({value for value in values if value}))


def ordered_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return ";".join(seen)


def build_gap_summary_rows(evidence_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in evidence_rows:
        grouped[row["source_id"]].append(row)

    rows: list[dict[str, str]] = []
    for index, source_id in enumerate(sorted(grouped), start=1):
        source_rows = grouped[source_id]
        first = source_rows[0]
        present_rows = [row for row in source_rows if row["match_status"] == "present"]
        missing_rows = [row for row in source_rows if row["match_status"] == "missing_for_source"]
        not_applicable_rows = [
            row for row in source_rows if row["match_status"].startswith("not_applicable_")
        ]
        gap_status = "all_required_review_files_resolved" if not missing_rows else "has_missing_source_evidence_rows"
        rows.append(
            {
                "evidence_gap_summary_id": f"source-pipeline-phase-action-evidence-gap-summary-{index:03d}",
                "source_id": source_id,
                "source_type": first["source_type"],
                "rights_status": first["rights_status"],
                "pipeline_gap_status": first["pipeline_gap_status"],
                "review_lanes": first["review_lanes"],
                "phase_names": first["phase_names"],
                "present_file_role_count": str(len(present_rows)),
                "missing_file_role_count": str(len(missing_rows)),
                "not_applicable_file_role_count": str(len(not_applicable_rows)),
                "total_file_role_count": str(len(source_rows)),
                "total_matched_row_count": str(sum(int(row["matched_row_count"]) for row in source_rows)),
                "present_file_roles": sorted_join([row["file_role"] for row in present_rows]),
                "missing_file_roles": sorted_join([row["file_role"] for row in missing_rows]),
                "not_applicable_file_roles": sorted_join(
                    [row["file_role"] for row in not_applicable_rows]
                ),
                "gap_status": gap_status,
                "next_review_action": (
                    "open_matched_rows_and_retain_not_applicable_boundaries"
                    if not missing_rows
                    else "triage_missing_source_evidence_rows_before_review_outcome"
                ),
                "evidence_presence_matrix_path": SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_PRESENCE_MATRIX.as_posix(),
                "evidence_presence_row_ids": ordered_join([row["evidence_presence_row_id"] for row in source_rows]),
                "missing_evidence_presence_row_ids": ordered_join(
                    [row["evidence_presence_row_id"] for row in missing_rows]
                ),
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
    parser.add_argument("--evidence-presence", default=str(SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_PRESENCE_MATRIX))
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parents[2]
    rows = build_gap_summary_rows(read_csv_rows(root / args.evidence_presence))
    write_csv(root / args.csv_output, rows)
    print(f"source_pipeline_phase_action_evidence_gap_summary_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
