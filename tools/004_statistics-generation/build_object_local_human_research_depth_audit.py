#!/usr/bin/env python3
"""Audit human-research depth slots for object-local corpus dossiers.

This audit groups the object-local material coverage rows by corpus area and
records which human dossier slots a reviewer must inspect before any formal
research claim. It is a navigation and gatekeeping artifact, not scholarship.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


COVERAGE_AUDIT = Path("corpus/009_statistics-and-derived-features/188_object-local-material-coverage-audit.csv")
OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/220_object-local-human-research-depth-audit.csv")
OUTPUT_JSON = Path("corpus/009_statistics-and-derived-features/221_object-local-human-research-depth-summary.json")
UPDATED_AT = "2026-06-30"
DEPTH_REVIEW_STATUS = "needs_human_research_depth_review"
HUMAN_FIRST_BOUNDARY = (
    "human dossier first; structured support files only route reviewers back "
    "to object-local evidence"
)
CLAIM_BOUNDARY = (
    "object_local_human_research_depth_audit_not_scholarship;"
    "no_identity_claim;no_component_claim;no_evolution_claim;no_decipherment_claim"
)


AREA_REQUIREMENTS: dict[str, dict[str, tuple[str, ...]]] = {
    "oracle_character_candidates": {
        "human_files": (
            "README.md",
            "04_visual-gallery.md",
            "05_human-research-dossier.md",
            "06_human-review-sheet.md",
            "08_character-context-evidence-dossier.md",
            "10_archaeology-paleography-review.md",
            "12_human-research-readiness-review.md",
        ),
        "slots": (
            "glyph_image",
            "glyph_observation",
            "variant_forms",
            "near_forms",
            "component_clues",
            "inscription_occurrence",
            "inscription_context",
            "plate_catalog_number",
            "heji_or_collection_number",
            "findspot_collection_period_group",
            "source_evidence",
            "decipherment_history",
            "dispute_record",
            "later_script_routes",
            "opened_glyph_image_observation",
            "formal_character_research_blockers",
            "source_manifest_checksum_field_map",
            "missing_items",
            "next_sources_to_check",
        ),
        "questions": (
            "Which concrete source, plate, or inscription should a human open next?",
            "Which observation is still candidate, disputed, missing, or pending review?",
            "Which visual route supports the dossier without replacing it?",
            "Which opened image row supports the first glyph observation?",
            "Which bibliography records reading history, proposer, or dispute?",
            "Which manifest, checksum, field map, rights note, and risk note apply?",
        ),
    },
    "inscription_crosswalk_candidates": {
        "human_files": (
            "README.md",
            "04_human-review-sheet.md",
            "06_plate-text-gallery.md",
            "07_human-inscription-dossier.md",
            "09_inscription-plate-evidence-dossier.md",
            "11_inscription-review-fact-matrix.md",
            "13_text-ocr-quality-review.md",
            "15_inscription-context-review.md",
            "17_human-research-readiness-review.md",
        ),
        "slots": (
            "inscription_number",
            "ocr_or_full_text",
            "plate_number",
            "catalog_source",
            "page_number",
            "heji_or_collection_number",
            "library_or_collection",
            "findspot",
            "period_group_batch",
            "linked_glyphs",
            "image_path",
            "text_quality",
            "bibliography_disputes",
            "source_trail",
            "formal_research_blockers",
            "source_manifest_checksum_field_map",
            "linked_glyph_candidate_boundary",
            "missing_items",
            "review_status",
        ),
        "questions": (
            "Which plate, catalog page, or OCR text must be opened first?",
            "Which linked glyph remains a candidate route rather than a confirmed reading?",
            "Which text-quality issue blocks use in a formal inscription record?",
            "Which manifest, checksum, field map, rights note, and risk note apply?",
            "Which bibliography, proposer, reading history, or dispute trail is missing?",
            "Which issue blocks formal obi assignment and corpus import?",
        ),
    },
    "graphemic_component_candidates": {
        "human_files": (
            "README.md",
            "07_component-visual-gallery.md",
            "08_human-visual-review-sheet.md",
            "10_component-visual-route-gallery.md",
            "11_human-component-dossier.md",
            "13_component-context-evidence-dossier.md",
            "15_component-review-fact-matrix.md",
            "16_component-research-readiness-review.md",
        ),
        "slots": (
            "component_candidate_id",
            "glyph_image_route",
            "host_character",
            "visual_evidence",
            "component_boundary",
            "near_shape",
            "context_evidence",
            "source_codepoint_route",
            "missing_items",
            "review_status",
        ),
        "questions": (
            "Which host character and image route should be reviewed first?",
            "Which component boundary remains only a candidate observation?",
            "Which near-shape comparison needs a human visual check?",
        ),
    },
    "evolution_correspondence_candidates": {
        "human_files": (
            "README.md",
            "04_human-review-sheet.md",
            "06_image-reference-route-gallery.md",
            "07_human-evolution-dossier.md",
            "09_cross-period-review-dossier.md",
            "11_evolution-review-fact-matrix.md",
            "12_modern-label-caution-review.md",
            "14_human-research-readiness-review.md",
        ),
        "slots": (
            "evolution_candidate_id",
            "oracle_source_route",
            "bronze_seal_modern_route",
            "era_source_code",
            "correspondence_category",
            "image_reference_route",
            "cross_period_comparison",
            "dispute_record",
            "later_script_identity_boundary",
            "formal_correspondence_research_blockers",
            "source_manifest_checksum_field_map",
            "missing_items",
            "review_status",
        ),
        "questions": (
            "Which era-specific source code and image route must be opened?",
            "Which correspondence is only a route, not an accepted evolution chain?",
            "Which cross-period comparison remains missing or disputed?",
            "Which opened oracle, bronze, seal, or modern image supports review?",
            "Which manifest, checksum, field map, rights note, and risk note apply?",
            "Which issue blocks formal correspondence research?",
        ),
    },
    "codepoint_crosswalk_candidates": {
        "human_files": (
            "README.md",
            "04_human-codepoint-crosswalk-review-sheet.md",
            "05_codepoint-crosswalk-route-gallery.md",
            "06_human-codepoint-crosswalk-dossier.md",
            "08_codepoint-crosswalk-fact-matrix.md",
            "10_cross-source-conflict-review.md",
            "12_modern-label-boundary-review.md",
        ),
        "slots": (
            "source_codepoint",
            "source_system",
            "matched_project_character_route",
            "glyph_image_route",
            "cross_source_id",
            "conflict_or_ambiguity",
            "modern_label_boundary",
            "unicode_codepoint_route",
            "dataset_label_boundary",
            "visible_glyph_evidence",
            "bibliography_or_proposer",
            "missing_items",
            "review_status",
        ),
        "questions": (
            "Which source codepoint route needs direct human comparison?",
            "Which cross-source match remains ambiguous or conflicting?",
            "Which project object should be opened before using the crosswalk?",
            "Which modern label is only lookup metadata?",
        ),
    },
    "collection_object_candidates": {
        "human_files": (
            "README.md",
            "04_visual-gallery.md",
            "05_human-review-sheet.md",
            "06_human-collection-dossier.md",
            "08_collection-provenance-evidence-dossier.md",
            "10_collection-provenance-fact-matrix.md",
            "12_archaeological-context-review.md",
            "14_human-research-readiness-review.md",
        ),
        "slots": (
            "institution",
            "museum_object_record",
            "accession_or_catalog_number",
            "image_or_object_route",
            "findspot",
            "excavation_site",
            "period",
            "batch_or_pit_context",
            "plate_or_publication_route",
            "inscription_route",
            "oracle_character_route",
            "rights_status",
            "risk_note",
            "scholarship_dispute_route",
            "raw_asset_boundary",
            "missing_items",
            "review_status",
        ),
        "questions": (
            "Which institution and accession record must be opened first?",
            "Which findspot, period, or batch field still needs source review?",
            "Which plate, inscription, or character route remains candidate only?",
            "Which raw image or unclear asset must remain outside regular Git?",
            "Which bibliography, proposer, disagreement, or citation trail is missing?",
        ),
    },
    "research_source_objects": {
        "human_files": (
            "README.md",
            "06_human-source-review-sheet.md",
            "07_material-access-index.md",
            "08_source-processing-status.md",
            "10_source-evidence-dossier.md",
            "12_source-provenance-fact-matrix.md",
            "14_source-to-dossier-transfer-review.md",
            "16_source-literature-scope-review.md",
            "18_source-access-integrity-review.md",
        ),
        "slots": (
            "source_identity",
            "access_or_download_record",
            "checksum",
            "file_size",
            "rights_status",
            "risk_note",
            "package_manifest",
            "field_map",
            "metadata_profile",
            "derived_paths",
            "exceptions",
            "large_source_exception_or_storage",
            "access_integrity_review",
            "public_commit_decision",
            "review_status",
        ),
        "questions": (
            "Which access, checksum, manifest, or field map is still missing?",
            "Which safe derived record can be opened instead of a raw package?",
            "Which rights or risk note blocks public promotion?",
            "Which access-integrity row blocks source use?",
        ),
    },
    "research_topic_candidates": {
        "human_files": (
            "README.md",
            "05_human-topic-review-sheet.md",
            "06_human-topic-dossier.md",
            "08_topic-literature-context-dossier.md",
            "10_topic-citation-dispute-review-dossier.md",
            "12_topic-research-use-boundary-review.md",
        ),
        "slots": (
            "bibliographic_identity",
            "topic_scope",
            "citation_relation",
            "evidence_level",
            "reading_process_status",
            "proposer",
            "different_opinions",
            "dispute_record",
            "linked_inscription_routes",
            "research_use_boundary",
            "promotion_blockers",
            "accepted_claim_boundary",
            "missing_items",
            "review_status",
        ),
        "questions": (
            "Which bibliography or database note should be opened first?",
            "Which citation relation or disagreement remains only a review route?",
            "Which linked inscription route needs human checking before promotion?",
            "Which topic, grammar, reading, or dating claim remains blocked?",
        ),
    },
}


FIELDNAMES = [
    "depth_audit_id",
    "corpus_area",
    "object_count",
    "human_entry_object_count",
    "ai_entry_object_count",
    "complete_bundle_object_count",
    "representative_human_files_to_open",
    "required_human_slots",
    "concrete_depth_questions",
    "coverage_source_file",
    "human_first_boundary",
    "depth_review_status",
    "claim_boundary",
    "updated_at",
]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def representative_files(root: Path, object_dir: str, file_names: tuple[str, ...]) -> str:
    base = root / object_dir
    paths = [relative(base / name, root) for name in file_names if (base / name).exists()]
    return ";".join(paths)


def build_rows(root: Path, coverage_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows_by_area: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in coverage_rows:
        rows_by_area[row["corpus_area"]].append(row)

    rows: list[dict[str, str]] = []
    for area in sorted(AREA_REQUIREMENTS):
        area_rows = rows_by_area[area]
        first_object_dir = area_rows[0]["object_dir"] if area_rows else ""
        requirements = AREA_REQUIREMENTS[area]
        complete_count = sum(
            1
            for row in area_rows
            if not row["missing_human_files"] and not row["missing_ai_files"]
        )
        rows.append(
            {
                "depth_audit_id": f"object-local-human-depth-{len(rows) + 1:03d}",
                "corpus_area": area,
                "object_count": str(len(area_rows)),
                "human_entry_object_count": str(sum(1 for row in area_rows if not row["missing_human_files"])),
                "ai_entry_object_count": str(sum(1 for row in area_rows if not row["missing_ai_files"])),
                "complete_bundle_object_count": str(complete_count),
                "representative_human_files_to_open": representative_files(
                    root, first_object_dir, requirements["human_files"]
                ),
                "required_human_slots": ";".join(requirements["slots"]),
                "concrete_depth_questions": ";".join(requirements["questions"]),
                "coverage_source_file": COVERAGE_AUDIT.as_posix(),
                "human_first_boundary": HUMAN_FIRST_BOUNDARY,
                "depth_review_status": DEPTH_REVIEW_STATUS,
                "claim_boundary": CLAIM_BOUNDARY,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def build_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    status_counts = Counter(row["depth_review_status"] for row in rows)
    return {
        "area_count": len(rows),
        "object_directory_count": sum(int(row["object_count"]) for row in rows),
        "human_entry_object_count": sum(int(row["human_entry_object_count"]) for row in rows),
        "ai_entry_object_count": sum(int(row["ai_entry_object_count"]) for row in rows),
        "complete_bundle_object_count": sum(int(row["complete_bundle_object_count"]) for row in rows),
        "partial_or_missing_bundle_count": sum(
            int(row["object_count"]) - int(row["complete_bundle_object_count"])
            for row in rows
        ),
        "parallel_human_directory_count": 0,
        "depth_review_status_counts": dict(sorted(status_counts.items())),
        "human_first_boundary": HUMAN_FIRST_BOUNDARY,
        "claim_boundary": CLAIM_BOUNDARY,
        "completion_boundary": (
            "Depth audit only; it routes humans to object-local dossiers and "
            "does not complete formal research, source promotion, or decipherment."
        ),
        "updated_at": UPDATED_AT,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data: dict[str, object]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    coverage_rows = read_csv_rows(root / COVERAGE_AUDIT)
    rows = build_rows(root, coverage_rows)
    write_csv(root / OUTPUT_CSV, rows)
    write_json(root / OUTPUT_JSON, build_summary(rows))
    print(f"object_local_human_research_depth_area_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
