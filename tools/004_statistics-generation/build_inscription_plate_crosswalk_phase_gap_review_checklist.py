#!/usr/bin/env python3
"""Build an inscription/plate crosswalk phase gap review checklist.

This bridges core-corpus inscription and plate/catalog crosswalk gaps to
existing Cambridge/Hopkins staging, review, source-map, and candidate-packet
routes. It is navigation only.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
INSCRIPTION_DIR = Path("corpus/002_oracle-bone-inscriptions")
INSCRIPTION_REGISTER_DIR = INSCRIPTION_DIR / "000_inscription-registers"
CORE_CORPUS_PHASE_GAP_ACTION_QUEUE = STAT_DIR / "192_core-corpus-phase-gap-action-queue.csv"
OUTPUT_CSV = STAT_DIR / "195_inscription-plate-crosswalk-phase-gap-review-checklist.csv"
CAMBRIDGE_HOPKINS_STAGING = INSCRIPTION_REGISTER_DIR / "002_cambridge-hopkins-crosswalk-staging.csv"
CAMBRIDGE_HOPKINS_CLASSIFIED_SUMMARY = (
    INSCRIPTION_REGISTER_DIR / "003_cambridge-hopkins-classified-summary.csv"
)
CAMBRIDGE_HOPKINS_REVIEW_QUEUE = (
    STAT_DIR / "098_ai-agent-cambridge-hopkins-inscription-crosswalk-review-queue.csv"
)
INSCRIPTION_ID_SOURCE_MAP = (
    Path("project_registry/002_project-id-to-source-reference-map")
    / "002_oracle-inscription-id-source-map.csv"
)
CAMBRIDGE_HOPKINS_GRAPH_EDGES = (
    Path("corpus/008_relationship-graph")
    / "008_cambridge-hopkins-inscription-crosswalk-graph-edges.jsonl"
)
UPDATED_AT = "2026-06-20"
CLAIM_BOUNDARY = "inscription_plate_crosswalk_phase_gap_review_checklist_not_review_outcome_not_scholarship"
CAUTION = (
    "This inscription plate crosswalk phase gap review checklist only routes "
    "Cambridge/Hopkins staging, catalog reference, plate-text, source-map, and "
    "candidate-packet records for later human review. It does not collect new "
    "evidence, decide rights, promote sources, import formal inscription records, "
    "confirm inscription identity, or make decipherment claims."
)
REQUIRED_REVIEW_STEPS = (
    "open_195_inscription_plate_crosswalk_phase_gap_review_checklist;"
    "open_192_core_corpus_phase_gap_action_queue;"
    "open_cambridge_hopkins_crosswalk_staging;"
    "open_cambridge_hopkins_crosswalk_review_queue;"
    "open_inscription_id_source_map;"
    "open_object_local_candidate_packets;"
    "open_plate_text_route_indexes;"
    "confirm_no_new_evidence_collection;"
    "confirm_no_rights_decision;"
    "confirm_no_source_promotion;"
    "confirm_no_formal_inscription_import;"
    "confirm_no_inscription_identity_claim;"
    "confirm_no_decipherment_claim"
)
REQUIRED_INSCRIPTION_DOSSIER_SLOTS = (
    "inscription_number;"
    "full_text_or_ocr;"
    "plate_number;"
    "catalog_source;"
    "page_number;"
    "heji_or_obm_route;"
    "collection_object;"
    "findspot;"
    "period;"
    "batch;"
    "related_glyph_routes;"
    "image_path;"
    "text_quality;"
    "missing_items;"
    "review_status"
)
SOURCE_CONTEXT_FIELDS_TO_VERIFY = (
    "source_id;"
    "source_register_row;"
    "catalog_reference;"
    "page_or_plate;"
    "rights_status;"
    "risk_note;"
    "review_status"
)
CONCRETE_NEXT_CHECKS = (
    "Which inscription number or catalog crosswalk row identifies this candidate?;"
    "Which full text or OCR route can be opened?;"
    "Which plate number, page number, Heji route, or OBM route locates it?;"
    "Which collection object, findspot, period, or batch is recorded?;"
    "Which related glyph routes and image paths must be checked?;"
    "What text quality, missing item, or review status remains?"
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


def count_files(root: Path, pattern: str) -> int:
    return sum(1 for path in root.glob(pattern) if path.is_file())


def build_checklist_rows(root: Path) -> list[dict[str, str]]:
    gap_rows = [
        row
        for row in read_csv_rows(root / CORE_CORPUS_PHASE_GAP_ACTION_QUEUE)
        if row["corpus_area"] == "inscriptions_and_plate_crosswalks"
    ]
    staging_rows = read_csv_rows(root / CAMBRIDGE_HOPKINS_STAGING)
    summary_rows = read_csv_rows(root / CAMBRIDGE_HOPKINS_CLASSIFIED_SUMMARY)
    review_queue_rows = read_csv_rows(root / CAMBRIDGE_HOPKINS_REVIEW_QUEUE)
    inscription_map_rows = read_csv_rows(root / INSCRIPTION_ID_SOURCE_MAP)
    candidate_map_rows = [
        row for row in inscription_map_rows if row["record_type"] == "inscription_crosswalk_candidate"
    ]
    source_ids = sorted(
        {source_id for row in candidate_map_rows for source_id in split_values(row["source_ids"])}
    )
    candidate_packet_count = count_files(
        root, "corpus/002_oracle-bone-inscriptions/**/01_candidate-inscription-crosswalk-packet.json"
    )
    plate_route_index_count = count_files(
        root, "corpus/002_oracle-bone-inscriptions/**/05_plate-text-route-index.csv"
    )
    plate_gallery_count = count_files(
        root, "corpus/002_oracle-bone-inscriptions/**/06_plate-text-gallery.md"
    )
    files_to_open = unique_join(
        [
            path_text(OUTPUT_CSV),
            path_text(CORE_CORPUS_PHASE_GAP_ACTION_QUEUE),
            path_text(CAMBRIDGE_HOPKINS_STAGING),
            path_text(CAMBRIDGE_HOPKINS_CLASSIFIED_SUMMARY),
            path_text(CAMBRIDGE_HOPKINS_REVIEW_QUEUE),
            path_text(INSCRIPTION_ID_SOURCE_MAP),
            path_text(CAMBRIDGE_HOPKINS_GRAPH_EDGES),
            path_text(INSCRIPTION_DIR),
        ]
        + [path for row in gap_rows for path in split_values(row["phase_evidence_paths"])]
    )

    rows: list[dict[str, str]] = []
    for gap_row in gap_rows:
        rows.append(
            {
                "review_checklist_id": f"inscription-plate-crosswalk-phase-gap-review-{len(rows) + 1:03d}",
                "gap_queue_id": gap_row["gap_queue_id"],
                "source_phase_row_id": gap_row["source_phase_row_id"],
                "corpus_area": gap_row["corpus_area"],
                "phase_name": gap_row["phase_name"],
                "phase_status": gap_row["phase_status"],
                "gap_type": gap_row["gap_type"],
                "review_priority": gap_row["review_priority"],
                "review_status": "needs_human_review",
                "cambridge_hopkins_crosswalk_staging_count": str(len(staging_rows)),
                "cambridge_hopkins_crosswalk_review_queue_count": str(len(review_queue_rows)),
                "inscription_source_map_count": str(len(candidate_map_rows)),
                "candidate_packet_count": str(candidate_packet_count),
                "plate_text_route_index_count": str(plate_route_index_count),
                "plate_text_gallery_count": str(plate_gallery_count),
                "classified_summary_count": str(len(summary_rows)),
                "source_ids": ";".join(source_ids),
                "files_to_open": files_to_open,
                "required_review_steps": REQUIRED_REVIEW_STEPS,
                "required_inscription_dossier_slots": REQUIRED_INSCRIPTION_DOSSIER_SLOTS,
                "source_context_fields_to_verify": SOURCE_CONTEXT_FIELDS_TO_VERIFY,
                "concrete_next_checks": CONCRETE_NEXT_CHECKS,
                "recommended_action": gap_row["recommended_action"],
                "candidate_or_staging_boundary": gap_row["candidate_or_staging_boundary"],
                "claim_boundary": CLAIM_BOUNDARY,
                "evidence_collection_status": "not_collected",
                "rights_decision_status": "no_rights_decision",
                "source_promotion_status": "not_promoted",
                "corpus_import_status": "not_imported",
                "inscription_identity_claim_status": "no_inscription_identity_claim",
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
    print(f"inscription_plate_crosswalk_phase_gap_review_checklist_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
