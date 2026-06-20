#!/usr/bin/env python3
"""Build a core-corpus preprocessing phase gap action queue.

This expands missing and mixed phase statuses from the core corpus phase matrix
into reviewable routing rows. It is a preprocessing navigation surface only.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


CORE_CORPUS_PHASE_COVERAGE_MATRIX = Path(
    "corpus/009_statistics-and-derived-features/135_core-corpus-phase-coverage-matrix.csv"
)
OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/192_core-corpus-phase-gap-action-queue.csv")
UPDATED_AT = "2026-06-20"
CLAIM_BOUNDARY = "core_corpus_phase_gap_action_queue_not_review_outcome_not_scholarship"
CAUTION = (
    "Core corpus phase gap action queue only; rows route missing or mixed preprocessing "
    "phases for review and do not decide rights, import corpus records, promote "
    "candidates, or make decipherment claims."
)

PHASES = [
    "discovered",
    "downloaded",
    "registered",
    "unpacked",
    "extracted",
    "cleaned",
    "structured",
    "linked",
    "verified",
    "pending_human_review",
]
GAP_STATUSES = {"missing", "mixed_or_partial"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def phase_priority(status: str) -> str:
    if status == "missing":
        return "fill_missing_phase"
    return "complete_partial_phase"


def build_gap_rows(root: Path) -> list[dict[str, str]]:
    phase_rows = read_csv_rows(root / CORE_CORPUS_PHASE_COVERAGE_MATRIX)
    rows: list[dict[str, str]] = []
    for phase_row in phase_rows:
        for phase_name in PHASES:
            phase_status = phase_row[f"{phase_name}_status"]
            if phase_status not in GAP_STATUSES:
                continue
            rows.append(
                {
                    "gap_queue_id": f"core-corpus-phase-gap-{len(rows) + 1:03d}",
                    "source_phase_row_id": phase_row["phase_row_id"],
                    "corpus_area": phase_row["corpus_area"],
                    "label_en": phase_row["label_en"],
                    "phase_name": phase_name,
                    "phase_status": phase_status,
                    "gap_type": phase_priority(phase_status),
                    "review_priority": phase_row["review_priority"],
                    "review_status": "needs_human_review",
                    "phase_evidence_paths": phase_row["phase_evidence_paths"],
                    "recommended_action": phase_row["next_action"],
                    "candidate_or_staging_boundary": phase_row["candidate_or_staging_boundary"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "rights_decision_status": "no_new_rights_decision",
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
    rows = build_gap_rows(root)
    write_csv(root / args.csv_output, rows)
    print(f"core_corpus_phase_gap_action_queue_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
