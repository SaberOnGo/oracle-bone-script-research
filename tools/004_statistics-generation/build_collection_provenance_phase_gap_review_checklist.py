#!/usr/bin/env python3
"""Build a collection-provenance phase gap review checklist.

This bridges core-corpus collection provenance gaps to existing collection,
asset, object-map, and OBM access-boundary routes. It is navigation only.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CORE_CORPUS_PHASE_GAP_ACTION_QUEUE = STAT_DIR / "192_core-corpus-phase-gap-action-queue.csv"
OUTPUT_CSV = STAT_DIR / "194_collection-provenance-phase-gap-review-checklist.csv"
COLLECTION_STAGING = Path(
    "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/"
    "001_institutional-collection-provenance-staging.csv"
)
COLLECTION_REGISTERS_DIR = Path(
    "corpus/005_excavation-sites-periods-and-batches/000_collection-registers"
)
COLLECTION_OBJECT_ID_SOURCE_MAP = Path(
    "project_registry/002_project-id-to-source-reference-map/006_collection-object-id-source-map.csv"
)
ASSET_SOURCE_INDEX = Path("project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv")
ASSET_RIGHTS_REVIEW_LOG = Path(
    "project_registry/004_asset-source-and-rights-index/002_asset-rights-review-log.csv"
)
OBM_FOLLOWUP_REVIEW_QUEUE = STAT_DIR / "074_ai-agent-xxt-obm-access-boundary-followup-review-queue.csv"
UPDATED_AT = "2026-06-20"
CLAIM_BOUNDARY = "collection_provenance_phase_gap_review_checklist_not_review_outcome_not_scholarship"
CAUTION = (
    "This collection provenance phase gap review checklist only routes collection, "
    "object-map, asset-provenance, and access-boundary records for later review. "
    "It does not collect raw images, decide rights, promote sources, import corpus "
    "records, confirm collection-object identity, or make decipherment claims."
)
REQUIRED_REVIEW_STEPS = (
    "open_194_collection_provenance_phase_gap_review_checklist;"
    "open_192_core_corpus_phase_gap_action_queue;"
    "open_collection_provenance_staging;"
    "open_collection_object_id_source_map;"
    "open_asset_source_index_and_rights_log;"
    "open_obm_access_boundary_followup_queue;"
    "confirm_raw_unclear_images_stay_outside_git;"
    "confirm_no_rights_decision;"
    "confirm_no_source_promotion;"
    "confirm_no_corpus_import;"
    "confirm_no_collection_object_identity_claim;"
    "confirm_no_decipherment_claim"
)
REQUIRED_COLLECTION_PROVENANCE_SLOTS = (
    "collection_object_id;"
    "institution;"
    "museum_object_record;"
    "accession_or_catalog_number;"
    "findspot;"
    "excavation_site;"
    "period;"
    "batch_or_pit_context;"
    "source_system;"
    "source_register_row;"
    "asset_source_row;"
    "asset_rights_row;"
    "image_or_object_route;"
    "file_size;"
    "checksum;"
    "rights_status;"
    "risk_note;"
    "public_commit_decision;"
    "raw_package_storage;"
    "review_status"
)
SOURCE_CONTEXT_FIELDS_TO_VERIFY = (
    "collection_staging_row;"
    "collection_object_id_source_map_row;"
    "asset_source_index_row;"
    "asset_rights_review_log_row;"
    "large_source_register_row;"
    "download_or_access_record;"
    "source_id;"
    "rights_status;"
    "risk_note;"
    "review_status"
)
CONCRETE_NEXT_CHECKS = (
    "Which institution, object record, accession or catalog number, and source system "
    "identify this collection object?;"
    "Which findspot, excavation site, period, batch, or pit context remains missing?;"
    "Which asset source row, rights row, file size, checksum, and risk note limit public use?;"
    "Which object-local dossier or review sheet should be opened before comparing the image?;"
    "Which raw package or unclear image must stay outside regular Git until review?"
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


def build_checklist_rows(root: Path) -> list[dict[str, str]]:
    gap_rows = [
        row
        for row in read_csv_rows(root / CORE_CORPUS_PHASE_GAP_ACTION_QUEUE)
        if row["corpus_area"] == "collection_provenance_assets"
    ]
    collection_rows = read_csv_rows(root / COLLECTION_STAGING)
    object_map_rows = read_csv_rows(root / COLLECTION_OBJECT_ID_SOURCE_MAP)
    asset_rows = read_csv_rows(root / ASSET_SOURCE_INDEX)
    museum_asset_rows = [row for row in asset_rows if row["asset_type"] == "museum_object_image"]
    obm_followup_rows = read_csv_rows(root / OBM_FOLLOWUP_REVIEW_QUEUE)

    collection_source_ids = sorted({row["source_id"] for row in collection_rows if row["source_id"]})
    object_source_ids = sorted(
        {source_id for row in object_map_rows for source_id in split_values(row["source_ids"])}
    )
    museum_asset_source_ids = sorted(
        {source_id for row in museum_asset_rows for source_id in split_values(row["source_ids"])}
    )
    obm_source_ids = sorted({row["source_id"] for row in obm_followup_rows if row["source_id"]})
    files_to_open = unique_join(
        [
            path_text(OUTPUT_CSV),
            path_text(CORE_CORPUS_PHASE_GAP_ACTION_QUEUE),
            path_text(COLLECTION_STAGING),
            path_text(COLLECTION_REGISTERS_DIR),
            path_text(COLLECTION_OBJECT_ID_SOURCE_MAP),
            path_text(ASSET_SOURCE_INDEX),
            path_text(ASSET_RIGHTS_REVIEW_LOG),
            path_text(OBM_FOLLOWUP_REVIEW_QUEUE),
        ]
        + [path for row in gap_rows for path in split_values(row["phase_evidence_paths"])]
    )

    rows: list[dict[str, str]] = []
    for gap_row in gap_rows:
        rows.append(
            {
                "review_checklist_id": f"collection-provenance-phase-gap-review-{len(rows) + 1:03d}",
                "gap_queue_id": gap_row["gap_queue_id"],
                "source_phase_row_id": gap_row["source_phase_row_id"],
                "corpus_area": gap_row["corpus_area"],
                "phase_name": gap_row["phase_name"],
                "phase_status": gap_row["phase_status"],
                "gap_type": gap_row["gap_type"],
                "review_priority": gap_row["review_priority"],
                "review_status": "needs_human_review",
                "collection_staging_count": str(len(collection_rows)),
                "collection_object_map_count": str(len(object_map_rows)),
                "museum_object_asset_count": str(len(museum_asset_rows)),
                "obm_followup_route_count": str(len(obm_followup_rows)),
                "collection_source_ids": ";".join(collection_source_ids),
                "collection_object_source_ids": ";".join(object_source_ids),
                "museum_object_asset_source_ids": ";".join(museum_asset_source_ids),
                "obm_followup_source_ids": ";".join(obm_source_ids),
                "files_to_open": files_to_open,
                "required_review_steps": REQUIRED_REVIEW_STEPS,
                "required_collection_provenance_slots": REQUIRED_COLLECTION_PROVENANCE_SLOTS,
                "source_context_fields_to_verify": SOURCE_CONTEXT_FIELDS_TO_VERIFY,
                "concrete_next_checks": CONCRETE_NEXT_CHECKS,
                "recommended_action": gap_row["recommended_action"],
                "candidate_or_staging_boundary": gap_row["candidate_or_staging_boundary"],
                "claim_boundary": CLAIM_BOUNDARY,
                "evidence_collection_status": "not_collected",
                "rights_decision_status": "no_rights_decision",
                "source_promotion_status": "not_promoted",
                "corpus_import_status": "not_imported",
                "collection_object_identity_claim_status": "no_collection_object_identity_claim",
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
    print(f"collection_provenance_phase_gap_review_checklist_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
