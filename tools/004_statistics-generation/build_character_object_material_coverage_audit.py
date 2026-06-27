#!/usr/bin/env python3
"""Audit object-local human/AI material coverage for character directories."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/186_character-object-material-coverage-audit.csv")
OUTPUT_JSON = Path("corpus/009_statistics-and-derived-features/187_character-object-material-coverage-summary.json")
CHARACTER_ROOT = Path("corpus/001_oracle-characters")
UPDATED_AT = "2026-06-20"
RESEARCH_BOUNDARY = (
    "object_local_material_coverage_audit_not_scholarship; not an identity "
    "claim, not a component conclusion, not an evolution conclusion, not an "
    "accepted reading, and not a decipherment conclusion"
)

PROJECT_ID_PATTERN = re.compile(r"(obs-(?:char|unk)-\d{6})")

FIELDNAMES = [
    "coverage_audit_id",
    "project_id",
    "project_id_type",
    "object_sequence",
    "object_dir",
    "bucket_dir",
    "primary_external_ref_id",
    "ai_packet_path",
    "human_readme_path",
    "ai_visual_source_index_path",
    "human_visual_gallery_path",
    "local_visual_asset_count",
    "local_visual_metadata_count",
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


def read_packet(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def project_id_from_dir(path: Path) -> str:
    match = PROJECT_ID_PATTERN.search(path.name)
    if not match:
        raise ValueError(f"cannot parse project ID from object directory: {path}")
    return match.group(1)


def project_id_type(project_id: str) -> str:
    return "obs-char" if project_id.startswith("obs-char-") else "obs-unk"


def object_sequence(project_id: str) -> str:
    return project_id.rsplit("-", 1)[-1]


def bundle_status(has_readme: bool, has_visual_index: bool, has_gallery: bool, asset_count: int) -> str:
    if has_readme and has_visual_index and has_gallery and asset_count > 0:
        return "object_local_bundle_with_review_image"
    if has_readme and has_visual_index and has_gallery:
        return "object_local_bundle_no_image_yet"
    if has_readme or has_visual_index or has_gallery:
        return "partial_object_local_bundle"
    return "missing_human_object_materials"


def next_step(status: str) -> str:
    return {
        "object_local_bundle_with_review_image": "human_visual_review_and_source_cross_check",
        "object_local_bundle_no_image_yet": "extract_or_register_review_safe_visual_material_when_source_allows",
        "partial_object_local_bundle": "complete_object_local_readme_gallery_and_visual_index",
        "missing_human_object_materials": "generate_object_local_human_readme_gallery_and_ai_visual_index",
    }[status]


def local_image_count(asset_dir: Path) -> int:
    if not asset_dir.exists():
        return 0
    return sum(
        1
        for path in asset_dir.iterdir()
        if path.name.lower().endswith((".jpg", ".jpeg", ".png"))
    )


def build_audit_rows(root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    character_root = root / CHARACTER_ROOT
    packet_paths = sorted(
        [
            *character_root.glob("*/*/01_candidate-character-packet.json"),
            *character_root.glob("*/*/01_undeciphered-candidate-packet.json"),
        ]
    )
    for index, packet_path in enumerate(packet_paths, start=1):
        object_dir = packet_path.parent
        bucket_dir = object_dir.parent
        project_id = project_id_from_dir(object_dir)
        packet = read_packet(packet_path)
        readme_path = object_dir / "README.md"
        visual_index_path = object_dir / "02_visual-source-index.csv"
        gallery_path = object_dir / "04_visual-gallery.md"
        asset_dir = object_dir / "03_visual-assets"
        asset_count = local_image_count(asset_dir)
        metadata_count = len(list(asset_dir.glob("*.yaml"))) if asset_dir.exists() else 0
        parallel_human = (object_dir / "human-readable").exists() or (bucket_dir / "human-readable").exists()
        status = bundle_status(
            readme_path.exists(),
            visual_index_path.exists(),
            gallery_path.exists(),
            asset_count,
        )
        rows.append(
            {
                "coverage_audit_id": f"char-object-material-coverage-{index:05d}",
                "project_id": project_id,
                "project_id_type": project_id_type(project_id),
                "object_sequence": object_sequence(project_id),
                "object_dir": relative(object_dir, root),
                "bucket_dir": relative(bucket_dir, root),
                "primary_external_ref_id": packet.get("primary_external_ref_id", ""),
                "ai_packet_path": relative(packet_path, root),
                "human_readme_path": relative(readme_path, root) if readme_path.exists() else "",
                "ai_visual_source_index_path": relative(visual_index_path, root) if visual_index_path.exists() else "",
                "human_visual_gallery_path": relative(gallery_path, root) if gallery_path.exists() else "",
                "local_visual_asset_count": str(asset_count),
                "local_visual_metadata_count": str(metadata_count),
                "parallel_human_directory_present": str(parallel_human).lower(),
                "material_bundle_status": status,
                "next_material_engineering_step": next_step(status),
                "rights_status": packet.get("rights_status", ""),
                "review_status": packet.get("review_status", ""),
                "research_boundary": RESEARCH_BOUNDARY,
                "decipherment_claim_status": "no_claim",
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def build_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    status_counts = Counter(row["material_bundle_status"] for row in rows)
    project_id_type_counts = Counter(row["project_id_type"] for row in rows)
    return {
        "object_directory_count": len(rows),
        "project_id_type_counts": dict(sorted(project_id_type_counts.items())),
        "human_readme_count": sum(1 for row in rows if row["human_readme_path"]),
        "human_visual_gallery_count": sum(1 for row in rows if row["human_visual_gallery_path"]),
        "ai_packet_count": sum(1 for row in rows if row["ai_packet_path"]),
        "ai_visual_source_index_count": sum(1 for row in rows if row["ai_visual_source_index_path"]),
        "local_visual_asset_object_count": sum(1 for row in rows if int(row["local_visual_asset_count"]) > 0),
        "complete_object_local_bundle_count": (
            status_counts["object_local_bundle_with_review_image"]
            + status_counts["object_local_bundle_no_image_yet"]
        ),
        "missing_human_entry_count": status_counts["missing_human_object_materials"],
        "material_bundle_status_counts": dict(sorted(status_counts.items())),
        "parallel_human_directory_count": sum(
            1 for row in rows if row["parallel_human_directory_present"] == "true"
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "completion_boundary": (
            "Coverage audit only; it identifies object-local material gaps and does "
            "not start formal decipherment research or promote candidate records."
        ),
        "updated_at": UPDATED_AT,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
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
    rows = build_audit_rows(args.root)
    write_csv(args.root / OUTPUT_CSV, rows)
    write_json(args.root / OUTPUT_JSON, build_summary(rows))
    print(f"character_object_material_coverage_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
