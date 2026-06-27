#!/usr/bin/env python3
"""Build a character-candidate phase gap review checklist.

This bridges high-priority core-corpus gaps for promoted-character candidates
and undeciphered-character candidates to the current HUST-OBC review surfaces.
It is a preprocessing navigation surface only.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CHAR_REGISTER_DIR = Path("corpus/001_oracle-characters/000_character-registers")
CORE_CORPUS_PHASE_GAP_ACTION_QUEUE = STAT_DIR / "192_core-corpus-phase-gap-action-queue.csv"
OUTPUT_CSV = STAT_DIR / "198_character-candidate-phase-gap-review-checklist.csv"
HUST_PROMOTION_QUEUE = CHAR_REGISTER_DIR / "009_hust-obc-obs-char-promotion-review-queue.csv"
HUST_PROMOTION_BUCKET_SUMMARY = CHAR_REGISTER_DIR / "010_hust-obc-promotion-bucket-review-summary.csv"
UNDECIPHERED_INDEX = CHAR_REGISTER_DIR / "003_undeciphered-oracle-characters-index.csv"
UNDECIPHERED_REVIEW_QUEUE = STAT_DIR / "051_ai-agent-hust-obc-undeciphered-candidate-review-queue.csv"
CANDIDATE_EVIDENCE_REQUEST_QUEUE = STAT_DIR / "005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv"
UNDECIPHERED_EVIDENCE_READINESS_CHECKLIST = (
    STAT_DIR / "060_ai-agent-hust-obc-undeciphered-candidate-evidence-readiness-checklist.csv"
)
CHARACTER_OBJECT_MATERIAL_COVERAGE_AUDIT = STAT_DIR / "186_character-object-material-coverage-audit.csv"
CHARACTER_OBJECT_MATERIAL_COVERAGE_SUMMARY = STAT_DIR / "187_character-object-material-coverage-summary.json"
UPDATED_AT = "2026-06-20"
TARGET_AREAS = {"oracle_characters", "undeciphered_oracle_character_candidates"}
CLAIM_BOUNDARY = "character_candidate_phase_gap_review_checklist_not_review_outcome_not_scholarship"
CAUTION = (
    "This character candidate phase gap review checklist only routes HUST-OBC "
    "oracle-character and undeciphered-character candidate phase gaps to existing "
    "promotion queues, candidate indexes, evidence-readiness rows, and "
    "object-local material audits. It does not collect evidence, decide rights, "
    "promote candidates, import formal character records, confirm character "
    "identity, or make decipherment claims."
)
REQUIRED_REVIEW_STEPS = (
    "open_198_character_candidate_phase_gap_review_checklist;"
    "open_192_core_corpus_phase_gap_action_queue;"
    "open_hust_obc_promotion_review_queue;"
    "open_hust_obc_candidate_evidence_request_queue;"
    "open_undeciphered_candidate_index;"
    "open_undeciphered_candidate_review_queue;"
    "open_undeciphered_evidence_readiness_checklist;"
    "open_character_object_material_coverage_audit;"
    "confirm_no_new_evidence_collection;"
    "confirm_no_rights_decision;"
    "confirm_no_candidate_promotion;"
    "confirm_no_formal_character_import;"
    "confirm_no_character_identity_claim;"
    "confirm_no_decipherment_claim"
)
REQUIRED_CHARACTER_DOSSIER_SLOTS = (
    "glyph_image;"
    "glyph_observation;"
    "variant_forms;"
    "near_forms;"
    "component_clues;"
    "inscription_occurrence;"
    "inscription_context;"
    "plate_route;"
    "catalog_number;"
    "heji_number;"
    "findspot;"
    "collection;"
    "period;"
    "group;"
    "source_evidence;"
    "decipherment_history;"
    "dispute_notes;"
    "later_script_routes;"
    "missing_items;"
    "next_sources_to_check"
)
SOURCE_CONTEXT_FIELDS_TO_VERIFY = (
    "source_id;"
    "source_row;"
    "external_reference;"
    "field_map;"
    "extraction_note;"
    "rights_status;"
    "risk_note;"
    "review_status"
)
CONCRETE_NEXT_CHECKS = (
    "Which glyph image and observation route can be opened?;"
    "Which variant, near-form, or component clue route must be compared?;"
    "Which inscription occurrence and context route supports this candidate?;"
    "Which plate, catalog number, Heji number, findspot, collection, period, or group route is present?;"
    "Which source row, field map, or extraction note supports this route?;"
    "Which decipherment-history or dispute route remains to be checked?;"
    "Which later-script route remains to be checked?;"
    "Which missing item or next source should be reviewed before promotion?"
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
        value = value.rstrip("/")
        if not value or value in seen:
            continue
        seen.add(value)
        output.append(value)
    return ";".join(output)


def path_text(path: Path) -> str:
    return path.as_posix()


def source_ids_from_rows(rows: list[dict[str, str]], *fields: str) -> str:
    source_ids: set[str] = set()
    for row in rows:
        for field in fields:
            source_ids.update(split_values(row.get(field, "")))
    return ";".join(sorted(source_ids))


def build_checklist_rows(root: Path) -> list[dict[str, str]]:
    gap_rows = [
        row
        for row in read_csv_rows(root / CORE_CORPUS_PHASE_GAP_ACTION_QUEUE)
        if row["corpus_area"] in TARGET_AREAS
    ]
    promotion_rows = read_csv_rows(root / HUST_PROMOTION_QUEUE)
    promotion_bucket_rows = read_csv_rows(root / HUST_PROMOTION_BUCKET_SUMMARY)
    undeciphered_rows = read_csv_rows(root / UNDECIPHERED_INDEX)
    undeciphered_review_rows = read_csv_rows(root / UNDECIPHERED_REVIEW_QUEUE)
    evidence_request_rows = read_csv_rows(root / CANDIDATE_EVIDENCE_REQUEST_QUEUE)
    undeciphered_readiness_rows = read_csv_rows(root / UNDECIPHERED_EVIDENCE_READINESS_CHECKLIST)
    character_material_rows = read_csv_rows(root / CHARACTER_OBJECT_MATERIAL_COVERAGE_AUDIT)
    source_ids = source_ids_from_rows(
        promotion_rows + undeciphered_rows + undeciphered_review_rows + undeciphered_readiness_rows,
        "source_id",
        "source_id_captured",
    )
    files_to_open = unique_join(
        [
            path_text(OUTPUT_CSV),
            path_text(CORE_CORPUS_PHASE_GAP_ACTION_QUEUE),
            path_text(HUST_PROMOTION_QUEUE),
            path_text(HUST_PROMOTION_BUCKET_SUMMARY),
            path_text(CANDIDATE_EVIDENCE_REQUEST_QUEUE),
            path_text(UNDECIPHERED_INDEX),
            path_text(UNDECIPHERED_REVIEW_QUEUE),
            path_text(UNDECIPHERED_EVIDENCE_READINESS_CHECKLIST),
            path_text(CHARACTER_OBJECT_MATERIAL_COVERAGE_AUDIT),
            path_text(CHARACTER_OBJECT_MATERIAL_COVERAGE_SUMMARY),
        ]
        + [path for row in gap_rows for path in split_values(row["phase_evidence_paths"])]
    )

    rows: list[dict[str, str]] = []
    for gap_row in gap_rows:
        rows.append(
            {
                "review_checklist_id": f"character-candidate-phase-gap-review-{len(rows) + 1:03d}",
                "gap_queue_id": gap_row["gap_queue_id"],
                "source_phase_row_id": gap_row["source_phase_row_id"],
                "corpus_area": gap_row["corpus_area"],
                "phase_name": gap_row["phase_name"],
                "phase_status": gap_row["phase_status"],
                "gap_type": gap_row["gap_type"],
                "review_priority": gap_row["review_priority"],
                "review_status": "needs_human_review",
                "hust_promotion_review_count": str(len(promotion_rows)),
                "hust_promotion_bucket_count": str(len(promotion_bucket_rows)),
                "candidate_evidence_request_count": str(len(evidence_request_rows)),
                "undeciphered_index_count": str(len(undeciphered_rows)),
                "undeciphered_review_queue_count": str(len(undeciphered_review_rows)),
                "undeciphered_evidence_readiness_count": str(len(undeciphered_readiness_rows)),
                "character_object_material_audit_count": str(len(character_material_rows)),
                "source_ids": source_ids,
                "files_to_open": files_to_open,
                "required_review_steps": REQUIRED_REVIEW_STEPS,
                "required_character_dossier_slots": REQUIRED_CHARACTER_DOSSIER_SLOTS,
                "source_context_fields_to_verify": SOURCE_CONTEXT_FIELDS_TO_VERIFY,
                "concrete_next_checks": CONCRETE_NEXT_CHECKS,
                "recommended_action": gap_row["recommended_action"],
                "candidate_or_staging_boundary": gap_row["candidate_or_staging_boundary"],
                "claim_boundary": CLAIM_BOUNDARY,
                "evidence_collection_status": "not_collected",
                "rights_decision_status": "no_rights_decision",
                "source_promotion_status": "not_promoted",
                "corpus_import_status": "not_imported",
                "character_identity_claim_status": "no_character_identity_claim",
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
    print(f"character_candidate_phase_gap_review_checklist_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
