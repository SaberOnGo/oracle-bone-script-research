#!/usr/bin/env python3
"""Build a published-research-note phase gap review checklist.

This routes published-scholarship note gaps to the current research and
user/AI draft areas. It is a preprocessing boundary surface only.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


CORE_CORPUS_PHASE_GAP_ACTION_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/192_core-corpus-phase-gap-action-queue.csv"
)
SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
OUTPUT_CSV = Path(
    "corpus/009_statistics-and-derived-features/197_published-research-note-phase-gap-review-checklist.csv"
)
RESEARCH_DIR = Path("research")
USER_RESEARCH_DIR = Path("doc/public/user_research")
SOURCE_REGISTER_DIR = Path("corpus/006_research-sources-and-bibliography")
PUBLISHED_SCHOLARSHIP_REVIEW_GUIDE = Path(
    "research/001_published-scholarship-index/002_published-scholarship-review-guide.md"
)
UPDATED_AT = "2026-06-20"
CLAIM_BOUNDARY = "published_research_note_phase_gap_review_checklist_not_review_outcome_not_scholarship"
CAUTION = (
    "This published research note phase gap review checklist only routes "
    "published-scholarship and bibliography note preprocessing gaps to current "
    "research, source-register, and user/AI draft review surfaces. It does not "
    "collect evidence, promote drafts into research, import corpus records, or "
    "make decipherment claims."
)
REQUIRED_REVIEW_STEPS = (
    "open_197_published_research_note_phase_gap_review_checklist;"
    "open_192_core_corpus_phase_gap_action_queue;"
    "open_published_scholarship_review_guide;"
    "open_research_directory;"
    "open_doc_public_user_research_directory;"
    "open_source_register_index;"
    "confirm_published_scholarship_source_marking;"
    "confirm_user_ai_drafts_remain_under_doc_public_user_research;"
    "confirm_no_draft_promotion_to_research_without_human_review;"
    "confirm_no_corpus_import;"
    "confirm_no_decipherment_claim"
)
REQUIRED_CONTENT_SLOTS = (
    "bibliographic_identity;"
    "source_trail;"
    "scope;"
    "evidence_level;"
    "citation_relation;"
    "reading_process_status;"
    "proposer_and_disagreement;"
    "dispute_record;"
    "review_status"
)
SOURCE_TRAIL_FIELDS_TO_VERIFY = (
    "source_object_id;"
    "source_register_row;"
    "access_or_download_route;"
    "checksum;"
    "file_size;"
    "manifest;"
    "derived_path;"
    "rights_status;"
    "risk_note;"
    "review_status"
)
CONCRETE_NEXT_CHECKS = (
    "Which source object and register row prove this bibliography item?;"
    "Which page, plate, URL, catalog number, or object record locates it?;"
    "Which checksum, file size, manifest, or field map supports the route?;"
    "Which corpus object can this source actually support?;"
    "What evidence level is justified by the opened source?;"
    "Who is the proposer, and where is the proposal recorded?;"
    "Which disagreement or dispute is documented, and where?;"
    "Which user or AI draft must stay outside research until reviewed?;"
    "What exact source must be opened before any note can be promoted?"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def path_text(path: Path) -> str:
    return path.as_posix()


def count_files(root: Path, relative_dir: Path) -> int:
    return sum(1 for path in (root / relative_dir).rglob("*") if path.is_file())


def route_paths(root: Path, relative_dir: Path, patterns: tuple[str, ...]) -> str:
    paths: list[str] = []
    for pattern in patterns:
        paths.extend(path.relative_to(root).as_posix() for path in sorted((root / relative_dir).rglob(pattern)))
    return ";".join(paths)


def build_checklist_rows(root: Path) -> list[dict[str, str]]:
    gap_rows = [
        row
        for row in read_csv_rows(root / CORE_CORPUS_PHASE_GAP_ACTION_QUEUE)
        if row["corpus_area"] == "published_research_notes"
    ]
    source_rows = read_csv_rows(root / SOURCE_INDEX)
    research_note_route_paths = route_paths(
        root,
        RESEARCH_DIR,
        ("README.md", PUBLISHED_SCHOLARSHIP_REVIEW_GUIDE.name),
    )
    draft_review_route_paths = route_paths(root, USER_RESEARCH_DIR, ("README.md", "*.md"))
    files_to_open = ";".join(
        [
            path_text(OUTPUT_CSV),
            path_text(CORE_CORPUS_PHASE_GAP_ACTION_QUEUE),
            path_text(SOURCE_INDEX),
            "research/",
            "doc/public/user_research/",
            path_text(PUBLISHED_SCHOLARSHIP_REVIEW_GUIDE),
            research_note_route_paths,
            "doc/public/user_research/README.md",
        ]
    )

    rows: list[dict[str, str]] = []
    for gap_row in gap_rows:
        rows.append(
            {
                "review_checklist_id": f"published-research-note-phase-gap-review-{len(rows) + 1:03d}",
                "gap_queue_id": gap_row["gap_queue_id"],
                "source_phase_row_id": gap_row["source_phase_row_id"],
                "corpus_area": gap_row["corpus_area"],
                "phase_name": gap_row["phase_name"],
                "phase_status": gap_row["phase_status"],
                "gap_type": gap_row["gap_type"],
                "review_priority": gap_row["review_priority"],
                "review_status": "needs_human_review",
                "research_note_file_count": str(count_files(root, RESEARCH_DIR)),
                "user_research_review_file_count": str(count_files(root, USER_RESEARCH_DIR)),
                "source_register_file_count": str(count_files(root, SOURCE_REGISTER_DIR)),
                "source_index_row_count": str(len(source_rows)),
                "research_note_route_paths": research_note_route_paths,
                "draft_review_route_paths": draft_review_route_paths,
                "source_index_path": path_text(SOURCE_INDEX),
                "files_to_open": files_to_open,
                "required_review_steps": REQUIRED_REVIEW_STEPS,
                "required_content_slots": REQUIRED_CONTENT_SLOTS,
                "source_trail_fields_to_verify": SOURCE_TRAIL_FIELDS_TO_VERIFY,
                "concrete_next_checks": CONCRETE_NEXT_CHECKS,
                "recommended_action": gap_row["recommended_action"],
                "candidate_or_staging_boundary": gap_row["candidate_or_staging_boundary"],
                "claim_boundary": CLAIM_BOUNDARY,
                "evidence_collection_status": "not_collected",
                "rights_decision_status": "no_rights_decision",
                "source_promotion_status": "not_promoted",
                "corpus_import_status": "not_imported",
                "scholarship_note_promotion_status": "not_promoted_to_research",
                "draft_boundary_status": "user_ai_drafts_stay_in_doc_public_user_research",
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
    print(f"published_research_note_phase_gap_review_checklist_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
