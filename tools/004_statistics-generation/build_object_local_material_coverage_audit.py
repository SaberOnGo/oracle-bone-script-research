#!/usr/bin/env python3
"""Audit object-local human/AI material coverage across core corpus objects."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/188_object-local-material-coverage-audit.csv")
OUTPUT_JSON = Path("corpus/009_statistics-and-derived-features/189_object-local-material-coverage-summary.json")
UPDATED_AT = "2026-06-20"
RESEARCH_BOUNDARY = (
    "object_local_material_coverage_audit_not_scholarship; routes, images, "
    "candidate packets, and review sheets are preprocessing infrastructure, "
    "not identity, component, inscription, evolution, reading, or decipherment conclusions"
)


class ObjectSpec:
    def __init__(
        self,
        corpus_area: str,
        root: Path,
        packet_glob: str,
        required_human_files: tuple[str, ...],
        required_ai_files: tuple[str, ...],
        asset_dirs: tuple[str, ...],
        route_files: tuple[str, ...] = (),
    ) -> None:
        self.corpus_area = corpus_area
        self.root = root
        self.packet_glob = packet_glob
        self.required_human_files = required_human_files
        self.required_ai_files = required_ai_files
        self.asset_dirs = asset_dirs
        self.route_files = route_files


PROJECT_ID_PATTERN = re.compile(
    r"(obs-(?:char|unk|comp-cand|evo-cand|insc-cw-cand|topic-cand|xwalk-cand)-\d{6}|coll-obj-cand-\d{5}|src-[a-z0-9-]+)"
)
SOURCE_ID_PATTERN = re.compile(r"^src-[a-z0-9-]+$")
CHARACTER_MATERIAL_OBSERVATION_IDS = {
    f"obs-char-{index:06d}" for index in range(1, 681)
}


OBJECT_SPECS = [
    ObjectSpec(
        "oracle_character_candidates",
        Path("corpus/001_oracle-characters"),
        "*/*/01_candidate-character-packet.json",
        (
            "README.md",
            "04_visual-gallery.md",
            "05_human-research-dossier.md",
            "06_human-review-sheet.md",
            "08_character-context-evidence-dossier.md",
            "10_archaeology-paleography-review.md",
            "12_human-research-readiness-review.md",
        ),
        (
            "01_*packet.json",
            "02_visual-source-index.csv",
            "07_research-dossier-index.json",
            "09_character-context-evidence-index.json",
            "11_archaeology-paleography-index.json",
            "13_human-research-readiness-index.json",
        ),
        ("03_visual-assets",),
        (
            "04_visual-gallery.md",
            "08_character-context-evidence-dossier.md",
            "10_archaeology-paleography-review.md",
            "12_human-research-readiness-review.md",
        ),
    ),
    ObjectSpec(
        "oracle_character_candidates",
        Path("corpus/001_oracle-characters"),
        "*/*/01_undeciphered-candidate-packet.json",
        (
            "README.md",
            "04_visual-gallery.md",
            "05_human-research-dossier.md",
            "06_human-review-sheet.md",
            "08_character-context-evidence-dossier.md",
            "10_archaeology-paleography-review.md",
            "12_human-research-readiness-review.md",
        ),
        (
            "01_*packet.json",
            "02_visual-source-index.csv",
            "07_research-dossier-index.json",
            "09_character-context-evidence-index.json",
            "11_archaeology-paleography-index.json",
            "13_human-research-readiness-index.json",
        ),
        ("03_visual-assets",),
        (
            "04_visual-gallery.md",
            "08_character-context-evidence-dossier.md",
            "10_archaeology-paleography-review.md",
            "12_human-research-readiness-review.md",
        ),
    ),
    ObjectSpec(
        "graphemic_component_candidates",
        Path("corpus/003_graphemic-components"),
        "*/*/01_candidate-component-packet.json",
        (
            "README.md",
            "04_glyph-codepoint-gallery.md",
            "07_component-visual-gallery.md",
            "08_human-visual-review-sheet.md",
            "10_component-visual-route-gallery.md",
            "11_human-component-dossier.md",
            "13_component-context-evidence-dossier.md",
            "15_component-review-fact-matrix.md",
            "16_component-research-readiness-review.md",
        ),
        (
            "01_candidate-component-packet.json",
            "02_component-source-index.csv",
            "03_glyph-codepoint-index.csv",
            "06_component-visual-index.csv",
            "09_component-visual-route-index.csv",
            "12_component-dossier-index.json",
            "14_component-context-evidence-index.json",
            "17_component-research-readiness-index.json",
        ),
        ("05_component-visual-assets",),
        (
            "09_component-visual-route-index.csv",
            "10_component-visual-route-gallery.md",
            "13_component-context-evidence-dossier.md",
            "16_component-research-readiness-review.md",
        ),
    ),
    ObjectSpec(
        "evolution_correspondence_candidates",
        Path("corpus/004_bronze-seal-modern-correspondences"),
        "*/*/01_candidate-evolution-packet.json",
        (
            "README.md",
            "04_human-review-sheet.md",
            "06_image-reference-route-gallery.md",
            "07_human-evolution-dossier.md",
            "09_cross-period-review-dossier.md",
            "11_evolution-review-fact-matrix.md",
            "12_modern-label-caution-review.md",
            "14_human-research-readiness-review.md",
        ),
        (
            "01_candidate-evolution-packet.json",
            "02_evolution-source-index.csv",
            "03_era-source-code-index.csv",
            "05_image-reference-route-index.csv",
            "08_evolution-dossier-index.json",
            "10_cross-period-review-index.json",
            "13_modern-label-caution-index.json",
            "15_human-research-readiness-index.json",
        ),
        (),
        (
            "05_image-reference-route-index.csv",
            "06_image-reference-route-gallery.md",
            "12_modern-label-caution-review.md",
            "14_human-research-readiness-review.md",
        ),
    ),
    ObjectSpec(
        "inscription_crosswalk_candidates",
        Path("corpus/002_oracle-bone-inscriptions"),
        "*/*/01_candidate-inscription-crosswalk-packet.json",
        (
            "README.md",
            "04_human-review-sheet.md",
            "06_plate-text-gallery.md",
            "07_human-inscription-dossier.md",
            "09_inscription-plate-evidence-dossier.md",
            "11_inscription-review-fact-matrix.md",
            "13_text-ocr-quality-review.md",
            "15_inscription-context-review.md",
            "17_human-research-readiness-review.md",
            "19_preformal-research-start-check.md",
        ),
        (
            "01_candidate-inscription-crosswalk-packet.json",
            "02_crosswalk-source-index.csv",
            "03_catalog-reference-index.csv",
            "05_plate-text-route-index.csv",
            "08_inscription-dossier-index.json",
            "10_inscription-plate-evidence-index.json",
            "12_inscription-review-fact-matrix-index.json",
            "14_text-ocr-quality-index.json",
            "16_inscription-context-index.json",
            "18_human-research-readiness-index.json",
            "20_preformal-research-start-index.json",
        ),
        (),
        (
            "05_plate-text-route-index.csv",
            "06_plate-text-gallery.md",
            "15_inscription-context-review.md",
            "17_human-research-readiness-review.md",
            "19_preformal-research-start-check.md",
        ),
    ),
    ObjectSpec(
        "codepoint_crosswalk_candidates",
        Path("corpus/001_oracle-characters"),
        "*/*/01_codepoint-crosswalk-packet.json",
        (
            "README.md",
            "04_human-codepoint-crosswalk-review-sheet.md",
            "05_codepoint-crosswalk-route-gallery.md",
            "06_human-codepoint-crosswalk-dossier.md",
            "08_codepoint-crosswalk-fact-matrix.md",
            "10_cross-source-conflict-review.md",
            "12_modern-label-boundary-review.md",
            "14_codepoint-research-readiness-review.md",
        ),
        (
            "01_codepoint-crosswalk-packet.json",
            "02_codepoint-crosswalk-source-index.csv",
            "03_codepoint-crosswalk-route-index.csv",
            "07_codepoint-crosswalk-dossier-index.json",
            "09_codepoint-crosswalk-fact-matrix-index.json",
            "11_cross-source-conflict-index.json",
            "13_modern-label-boundary-index.json",
            "15_codepoint-research-readiness-index.json",
        ),
        (),
        (
            "03_codepoint-crosswalk-route-index.csv",
            "05_codepoint-crosswalk-route-gallery.md",
            "14_codepoint-research-readiness-review.md",
        ),
    ),
    ObjectSpec(
        "collection_object_candidates",
        Path("corpus/005_excavation-sites-periods-and-batches/002_collection-object-candidates"),
        "*/01_collection-object-packet.json",
        (
            "README.md",
            "04_visual-gallery.md",
            "05_human-review-sheet.md",
            "06_human-collection-dossier.md",
            "08_collection-provenance-evidence-dossier.md",
            "10_collection-provenance-fact-matrix.md",
            "12_archaeological-context-review.md",
            "14_human-research-readiness-review.md",
            "16_preformal-research-start-check.md",
        ),
        (
            "01_collection-object-packet.json",
            "02_collection-source-index.csv",
            "03_visual-asset-index.csv",
            "07_collection-dossier-index.json",
            "09_collection-provenance-evidence-index.json",
            "11_collection-provenance-fact-matrix-index.json",
            "13_archaeological-context-index.json",
            "15_human-research-readiness-index.json",
            "17_preformal-research-start-index.json",
        ),
        (),
        (
            "03_visual-asset-index.csv",
            "04_visual-gallery.md",
            "12_archaeological-context-review.md",
            "14_human-research-readiness-review.md",
            "16_preformal-research-start-check.md",
        ),
    ),
    ObjectSpec(
        "research_source_objects",
        Path("corpus/006_research-sources-and-bibliography/001_source-objects"),
        "*/01_source-packet.json",
        (
            "README.md",
            "06_human-source-review-sheet.md",
            "07_material-access-index.md",
            "08_source-processing-status.md",
            "10_source-evidence-dossier.md",
            "12_source-provenance-fact-matrix.md",
            "14_source-to-dossier-transfer-review.md",
            "16_source-literature-scope-review.md",
            "18_source-access-integrity-review.md",
            "20_source-presearch-readiness-review.md",
        ),
        (
            "01_source-packet.json",
            "02_download-route-index.csv",
            "03_package-route-index.csv",
            "04_field-map-route-index.csv",
            "05_metadata-profile-route-index.csv",
            "09_source-processing-status-index.json",
            "11_source-evidence-dossier-index.json",
            "13_source-provenance-fact-matrix-index.json",
            "15_source-to-dossier-transfer-index.json",
            "17_source-literature-scope-index.json",
            "19_source-access-integrity-index.json",
            "21_source-presearch-readiness-index.json",
        ),
        (),
        (
            "02_download-route-index.csv",
            "03_package-route-index.csv",
            "04_field-map-route-index.csv",
            "05_metadata-profile-route-index.csv",
            "20_source-presearch-readiness-review.md",
        ),
    ),
    ObjectSpec(
        "research_topic_candidates",
        Path("corpus/007_research-topics-and-grammar/001_topic-candidates"),
        "*/01_topic-candidate-packet.json",
        (
            "README.md",
            "05_human-topic-review-sheet.md",
            "06_human-topic-dossier.md",
            "08_topic-literature-context-dossier.md",
            "10_topic-citation-dispute-review-dossier.md",
            "12_topic-research-use-boundary-review.md",
            "14_topic-research-readiness-review.md",
        ),
        (
            "01_topic-candidate-packet.json",
            "02_topic-source-index.csv",
            "03_period-count-index.csv",
            "04_inscription-crosswalk-route-index.csv",
            "07_topic-dossier-index.json",
            "09_topic-literature-context-index.json",
            "11_topic-citation-dispute-review-index.json",
            "13_topic-research-use-boundary-index.json",
            "15_topic-research-readiness-index.json",
        ),
        (),
        (
            "04_inscription-crosswalk-route-index.csv",
            "08_topic-literature-context-dossier.md",
            "10_topic-citation-dispute-review-dossier.md",
            "12_topic-research-use-boundary-review.md",
            "14_topic-research-readiness-review.md",
        ),
    ),
]

FIELDNAMES = [
    "coverage_audit_id",
    "corpus_area",
    "project_id",
    "source_ids",
    "record_type",
    "object_dir",
    "packet_path",
    "human_file_count",
    "ai_file_count",
    "missing_human_files",
    "missing_ai_files",
    "local_visual_asset_count",
    "local_visual_metadata_count",
    "route_file_count",
    "parallel_human_directory_present",
    "material_bundle_status",
    "next_material_engineering_step",
    "rights_status",
    "review_status",
    "research_boundary",
    "decipherment_claim_status",
    "updated_at",
]


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def read_packet(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def project_id_for_packet(packet: dict[str, object], object_dir: Path) -> str:
    for key in (
        "project_id",
        "unknown_candidate_id",
        "suggested_oracle_character_id",
        "candidate_component_id",
        "candidate_evolution_id",
        "candidate_collection_object_id",
        "topic_candidate_id",
        "source_id",
    ):
        value = str(packet.get(key, ""))
        if value:
            return value
    match = PROJECT_ID_PATTERN.search(object_dir.name)
    return match.group(1) if match else ""


def source_ids_for_packet(packet: dict[str, object]) -> list[str]:
    source_ids: set[str] = set()
    collect_source_ids(packet, source_ids)
    return sorted(source_ids)


def collect_source_ids(value: object, source_ids: set[str]) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in {"source_id", "source_ids"}:
                collect_source_ids(nested, source_ids)
            elif isinstance(nested, (dict, list)):
                collect_source_ids(nested, source_ids)
        return
    if isinstance(value, list):
        for item in value:
            collect_source_ids(item, source_ids)
        return
    if isinstance(value, str):
        for item in split_source_ids(value):
            if SOURCE_ID_PATTERN.match(item):
                source_ids.add(item)


def split_source_ids(value: str) -> list[str]:
    return [item for item in value.replace(",", ";").split(";") if item]


def match_one(object_dir: Path, pattern: str) -> bool:
    return any(object_dir.glob(pattern))


def count_images(asset_dirs: list[Path]) -> int:
    count = 0
    for asset_dir in asset_dirs:
        if not asset_dir.exists():
            continue
        for path in asset_dir.iterdir():
            if path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                continue
            if path.is_file():
                count += 1
            else:
                resolved = path.resolve()
                if resolved.drive:
                    count += int(Path("\\\\?\\" + str(resolved)).is_file())
    return count


def count_metadata(asset_dirs: list[Path]) -> int:
    count = 0
    for asset_dir in asset_dirs:
        if not asset_dir.exists():
            continue
        count += sum(1 for path in asset_dir.iterdir() if path.suffix.lower() in {".yaml", ".yml", ".json", ".csv"})
    return count


def bundle_status(missing_human: list[str], missing_ai: list[str], asset_count: int, route_count: int) -> str:
    if missing_human or missing_ai:
        return "partial_or_missing_object_local_bundle"
    if asset_count > 0:
        return "object_local_bundle_with_review_image"
    if route_count > 0:
        return "object_local_bundle_with_evidence_routes"
    return "object_local_bundle_metadata_only"


def next_step(status: str) -> str:
    return {
        "object_local_bundle_with_review_image": "human_visual_review_and_source_cross_check",
        "object_local_bundle_with_evidence_routes": "follow_object_local_routes_to_collect_rights_reviewed_images_or_text",
        "object_local_bundle_metadata_only": "add_object_local_route_gallery_or_review_safe_visual_material_when_source_allows",
        "partial_or_missing_object_local_bundle": "complete_object_local_human_and_ai_material_bundle",
    }[status]


def build_rows(root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for spec in OBJECT_SPECS:
        packet_paths = sorted((root / spec.root).glob(spec.packet_glob))
        for packet_path in packet_paths:
            object_dir = packet_path.parent
            packet = read_packet(packet_path)
            project_id = project_id_for_packet(packet, object_dir)
            required_human_files = spec.required_human_files
            route_files = spec.route_files
            if spec.corpus_area == "oracle_character_candidates" and project_id in CHARACTER_MATERIAL_OBSERVATION_IDS:
                required_human_files = required_human_files + (
                    "14_material-visual-observation.md",
                )
                route_files = route_files + (
                    "14_material-visual-observation.md",
                )
            if spec.corpus_area == "graphemic_component_candidates" and project_id in {
                f"obs-comp-cand-{index:06d}" for index in range(1, 11)
            }:
                required_human_files = required_human_files + (
                    "18_material-visual-observation.md",
                )
                route_files = route_files + (
                    "18_material-visual-observation.md",
                )
            missing_human = [
                name
                for name in required_human_files
                if not (object_dir / name).exists()
            ]
            missing_ai = [name for name in spec.required_ai_files if not match_one(object_dir, name)]
            asset_dirs = [object_dir / name for name in spec.asset_dirs]
            asset_count = count_images(asset_dirs)
            metadata_count = count_metadata(asset_dirs)
            route_count = sum(1 for name in route_files if (object_dir / name).exists())
            status = bundle_status(missing_human, missing_ai, asset_count, route_count)
            parallel_human = (object_dir / "human-readable").exists() or (object_dir.parent / "human-readable").exists()
            rows.append(
                {
                    "coverage_audit_id": f"object-local-material-coverage-{len(rows) + 1:05d}",
                    "corpus_area": spec.corpus_area,
                    "project_id": project_id,
                    "source_ids": ";".join(source_ids_for_packet(packet)),
                    "record_type": str(packet.get("record_type", "")),
                    "object_dir": relative(object_dir, root),
                    "packet_path": relative(packet_path, root),
                    "human_file_count": str(len(required_human_files) - len(missing_human)),
                    "ai_file_count": str(len(spec.required_ai_files) - len(missing_ai)),
                    "missing_human_files": ";".join(missing_human),
                    "missing_ai_files": ";".join(missing_ai),
                    "local_visual_asset_count": str(asset_count),
                    "local_visual_metadata_count": str(metadata_count),
                    "route_file_count": str(route_count),
                    "parallel_human_directory_present": str(parallel_human).lower(),
                    "material_bundle_status": status,
                    "next_material_engineering_step": next_step(status),
                    "rights_status": str(packet.get("rights_status", "")),
                    "review_status": str(packet.get("review_status", "")),
                    "research_boundary": RESEARCH_BOUNDARY,
                    "decipherment_claim_status": "no_claim",
                    "updated_at": UPDATED_AT,
                }
            )
    return rows


def build_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    area_counts = Counter(row["corpus_area"] for row in rows)
    status_counts = Counter(row["material_bundle_status"] for row in rows)
    return {
        "object_directory_count": len(rows),
        "corpus_area_counts": dict(sorted(area_counts.items())),
        "material_bundle_status_counts": dict(sorted(status_counts.items())),
        "human_entry_object_count": sum(1 for row in rows if not row["missing_human_files"]),
        "ai_entry_object_count": sum(1 for row in rows if not row["missing_ai_files"]),
        "local_visual_asset_object_count": sum(1 for row in rows if int(row["local_visual_asset_count"]) > 0),
        "route_gallery_or_route_index_object_count": sum(1 for row in rows if int(row["route_file_count"]) > 0),
        "partial_or_missing_bundle_count": status_counts["partial_or_missing_object_local_bundle"],
        "parallel_human_directory_count": sum(1 for row in rows if row["parallel_human_directory_present"] == "true"),
        "research_boundary": RESEARCH_BOUNDARY,
        "completion_boundary": (
            "Coverage audit only; it identifies object-local material and route gaps "
            "without promoting candidate records or starting formal decipherment research."
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
    rows = build_rows(root)
    write_csv(root / OUTPUT_CSV, rows)
    write_json(root / OUTPUT_JSON, build_summary(rows))
    print(f"object_local_material_coverage_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
