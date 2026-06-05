#!/usr/bin/env python3
"""Build one scaffold AI evidence-pack draft from the HUST-OBC request queue."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_REQUEST_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/"
    "005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv"
)
UPDATED_AT = "2026-06-05"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_request_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def find_request_row(
    rows: list[dict[str, str]],
    evidence_request_id: str,
) -> dict[str, str]:
    for row in rows:
        if row.get("evidence_request_id") == evidence_request_id:
            return row
    raise ValueError(f"request not found: {evidence_request_id}")


def _split_compact_list(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def _empty_evidence_section(note: str) -> dict[str, object]:
    return {
        "status": "not_collected",
        "items": [],
        "notes": note,
    }


def build_draft(
    row: dict[str, str],
    request_queue_path: Path = DEFAULT_REQUEST_QUEUE,
) -> dict[str, object]:
    request_id = row["evidence_request_id"]
    pack_id = request_id.replace("evidence-request", "evidence-pack")
    return {
        "evidence_pack_id": pack_id,
        "evidence_request_id": request_id,
        "status": "draft",
        "research_boundary": "draft_not_scholarship",
        "assignment_status": row["assignment_status"],
        "suggested_oracle_character_id": row["suggested_oracle_character_id"],
        "candidate_class_id": row["candidate_class_id"],
        "primary_external_ref_id": row["primary_external_ref_id"],
        "draft_source_queue_path": request_queue_path.as_posix(),
        "route_pack_id": row["route_pack_id"],
        "bucket_manifest_path": row["bucket_manifest_path"],
        "route_files": _split_compact_list(row["route_files"]),
        "source_route_requirement_ids": _split_compact_list(row["source_route_requirement_ids"]),
        "evidence_gap_types": _split_compact_list(row["evidence_gap_types"]),
        "character_or_unknown_glyph_id": _empty_evidence_section(
            "Reserved project ID and external candidate ID copied from the request queue; no formal character assignment."
        ),
        "source_references_and_asset_metadata": _empty_evidence_section(
            "Open cited source registers, route files, and asset metadata before adding evidence."
        ),
        "full_inscription_context": _empty_evidence_section(
            "Primary inscription text and same-piece context have not been collected."
        ),
        "neighboring_characters": _empty_evidence_section(
            "Neighboring characters and same-inscription co-text have not been collected."
        ),
        "component_breakdown_and_variant_notes": _empty_evidence_section(
            "Component split, variant chain, and glyph-form notes have not been collected."
        ),
        "excavation_period_and_catalog_provenance": _empty_evidence_section(
            "Excavation, period, collection, and catalog provenance have not been collected."
        ),
        "bronze_seal_or_modern_comparanda": _empty_evidence_section(
            "Bronze, seal, later script, and modern-form comparanda have not been collected."
        ),
        "supporting_evidence": _empty_evidence_section(
            "No supporting evidence has been accepted into this draft."
        ),
        "opposing_evidence": _empty_evidence_section(
            "No opposing evidence has been collected yet."
        ),
        "open_questions_and_next_checks": [
            {
                "status": "open",
                "note": "Collect source rows and image or inscription context before writing any hypothesis.",
            }
        ],
        "review_log": [
            {
                "status": "created_from_request_queue",
                "note": "Empty scaffold created for AI Agent evidence collection.",
            }
        ],
        "caution": (
            "This file is not a decipherment result, not a formal obs-char assignment, "
            "and not published scholarship. Treat it as a structured evidence-collection draft."
        ),
        "updated_at": UPDATED_AT,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--request-queue",
        default=str(DEFAULT_REQUEST_QUEUE),
        help="Path to the HUST-OBC evidence request queue CSV.",
    )
    parser.add_argument(
        "--request-id",
        required=True,
        help="Evidence request ID, for example hust-obc-evidence-request-000001.",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Optional output path. Defaults to the draft_output_path in the request queue.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the draft JSON without writing it.",
    )
    args = parser.parse_args(argv)

    root = repo_root()
    request_queue_path = Path(args.request_queue)
    rows = read_request_rows(root / request_queue_path)
    row = find_request_row(rows, args.request_id)
    draft = build_draft(row, request_queue_path)

    output_path = Path(args.output or row["draft_output_path"])
    if args.dry_run:
        print(json.dumps(draft, ensure_ascii=False, indent=2))
    else:
        write_json(root / output_path, draft)
        print(f"wrote={(root / output_path).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
