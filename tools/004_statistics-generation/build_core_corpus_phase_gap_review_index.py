#!/usr/bin/env python3
"""Build a core-corpus phase gap review index.

This joins the 192 core-corpus phase gap action queue to the specialized
193-198 review checklists. It is a preprocessing navigation surface only.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CORE_CORPUS_PHASE_GAP_ACTION_QUEUE = STAT_DIR / "192_core-corpus-phase-gap-action-queue.csv"
OUTPUT_CSV = STAT_DIR / "199_core-corpus-phase-gap-review-index.csv"
UPDATED_AT = "2026-06-20"
CLAIM_BOUNDARY = "core_corpus_phase_gap_review_index_not_review_outcome_not_scholarship"
CAUTION = (
    "This core corpus phase gap review index only routes each 192 core-corpus "
    "phase gap row to its specialized 193-198 review checklist entry. It does "
    "not collect evidence, record reviewed outcomes, decide rights, promote "
    "sources or candidates, import formal corpus records, or make decipherment "
    "claims."
)
REQUIRED_REVIEW_STEPS = (
    "open_199_core_corpus_phase_gap_review_index;"
    "open_192_core_corpus_phase_gap_action_queue;"
    "open_specialized_review_checklist_row;"
    "confirm_specialized_row_matches_gap_queue_id;"
    "confirm_no_evidence_collection;"
    "confirm_no_rights_decision;"
    "confirm_no_source_or_candidate_promotion;"
    "confirm_no_corpus_import;"
    "confirm_no_decipherment_claim"
)

CHECKLIST_SOURCES = [
    (
        "character_candidate_phase_gap_review",
        STAT_DIR / "198_character-candidate-phase-gap-review-checklist.csv",
    ),
    (
        "shape_component_evolution_verification_gap_review",
        STAT_DIR / "196_shape-component-evolution-verification-gap-review-checklist.csv",
    ),
    (
        "inscription_plate_crosswalk_phase_gap_review",
        STAT_DIR / "195_inscription-plate-crosswalk-phase-gap-review-checklist.csv",
    ),
    (
        "collection_provenance_phase_gap_review",
        STAT_DIR / "194_collection-provenance-phase-gap-review-checklist.csv",
    ),
    (
        "research_source_phase_gap_review",
        STAT_DIR / "193_research-source-phase-gap-review-checklist.csv",
    ),
    (
        "published_research_note_phase_gap_review",
        STAT_DIR / "197_published-research-note-phase-gap-review-checklist.csv",
    ),
]


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
        value = value.rstrip("/")
        if not value or value in seen:
            continue
        seen.add(value)
        output.append(value)
    return ";".join(output)


def path_text(path: Path) -> str:
    return path.as_posix()


def specialized_rows_by_gap(root: Path) -> dict[str, tuple[str, Path, dict[str, str]]]:
    by_gap: dict[str, tuple[str, Path, dict[str, str]]] = {}
    for family, path in CHECKLIST_SOURCES:
        for row in read_csv_rows(root / path):
            gap_id = row["gap_queue_id"]
            if gap_id in by_gap:
                previous_family = by_gap[gap_id][0]
                raise ValueError(f"duplicate specialized checklist row for {gap_id}: {previous_family};{family}")
            by_gap[gap_id] = (family, path, row)
    return by_gap


def build_index_rows(root: Path) -> list[dict[str, str]]:
    gap_rows = read_csv_rows(root / CORE_CORPUS_PHASE_GAP_ACTION_QUEUE)
    checklist_rows = specialized_rows_by_gap(root)
    rows: list[dict[str, str]] = []

    for gap_row in gap_rows:
        gap_id = gap_row["gap_queue_id"]
        if gap_id not in checklist_rows:
            raise ValueError(f"missing specialized checklist row for {gap_id}")
        family, checklist_path, checklist_row = checklist_rows[gap_id]
        files_to_open = unique_join(
            [
                path_text(OUTPUT_CSV),
                path_text(CORE_CORPUS_PHASE_GAP_ACTION_QUEUE),
                path_text(checklist_path),
            ]
            + split_values(gap_row.get("phase_evidence_paths", ""))
            + split_values(checklist_row.get("files_to_open", ""))
        )
        rows.append(
            {
                "review_index_id": f"core-corpus-phase-gap-review-index-{len(rows) + 1:03d}",
                "gap_queue_id": gap_id,
                "source_phase_row_id": gap_row["source_phase_row_id"],
                "corpus_area": gap_row["corpus_area"],
                "label_en": gap_row["label_en"],
                "phase_name": gap_row["phase_name"],
                "phase_status": gap_row["phase_status"],
                "gap_type": gap_row["gap_type"],
                "review_priority": gap_row["review_priority"],
                "specialized_checklist_family": family,
                "specialized_checklist_id": checklist_row["review_checklist_id"],
                "specialized_checklist_path": path_text(checklist_path),
                "specialized_checklist_row_status": checklist_row["review_status"],
                "coverage_status": "covered_by_specialized_review_checklist",
                "files_to_open": files_to_open,
                "required_review_steps": REQUIRED_REVIEW_STEPS,
                "recommended_action": gap_row["recommended_action"],
                "candidate_or_staging_boundary": gap_row["candidate_or_staging_boundary"],
                "claim_boundary": CLAIM_BOUNDARY,
                "review_status": "needs_human_review",
                "index_status": "route_index_only",
                "evidence_collection_status": "not_collected",
                "rights_decision_status": "no_rights_decision",
                "source_promotion_status": "not_promoted",
                "corpus_import_status": "not_imported",
                "decipherment_claim_status": "no_decipherment_claim",
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )

    extra_gap_ids = sorted(set(checklist_rows) - {row["gap_queue_id"] for row in gap_rows})
    if extra_gap_ids:
        raise ValueError(f"specialized checklist rows have no 192 gap row: {';'.join(extra_gap_ids)}")
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
    rows = build_index_rows(root)
    write_csv(root / args.csv_output, rows)
    print(f"core_corpus_phase_gap_review_index_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
