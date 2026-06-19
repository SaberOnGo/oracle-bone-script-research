#!/usr/bin/env python3
"""Extract selected HUST-OBC glyph candidate images into object directories."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import zipfile
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required to extract local glyph images.") from exc


RAW_ZIP = Path("external_local_archive/source_packages/hust-obc/dl-hust-obc-figshare-raw.zip")
IMAGE_REFERENCE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "068_ai-agent-hust-obc-undeciphered-candidate-source-image-reference-extraction-results.csv"
)
EXPECTED_RAW_SHA256 = "0d00a4de8dd9ce7b7495d7b26f3c80098ee9975b91615211dde02e569bf0ad9d"
UPDATED_AT = "2026-06-19"
TARGETS = {
    "obs-unk-005708": {
        "asset_id": "asset-000004",
        "object_dir": Path(
            "corpus/001_oracle-characters/"
            "074_undeciphered-005701-005800_obs-unk-bucket_oracle-character-candidates/"
            "008_obs-unk-005708_hust-obc-und-X-005708_oracle-character-candidate"
        ),
        "asset_filename": "001_asset-000004_hust-X-005708_glyph.png",
    },
    "obs-unk-006294": {
        "asset_id": "asset-000005",
        "object_dir": Path(
            "corpus/001_oracle-characters/"
            "079_undeciphered-006201-006300_obs-unk-bucket_oracle-character-candidates/"
            "094_obs-unk-006294_hust-obc-und-X-006294_oracle-character-candidate"
        ),
        "asset_filename": "001_asset-000005_hust-X-006294_glyph.png",
    },
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def filesystem_path(path: Path) -> str:
    resolved = path.resolve()
    if os.name == "nt":
        return "\\\\?\\" + str(resolved)
    return str(resolved)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"no rows to write: {path}")
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def first_reference_rows(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    selected: dict[str, dict[str, str]] = {}
    for row in rows:
        project_id = row.get("unknown_candidate_id", "")
        if project_id in TARGETS and project_id not in selected:
            selected[project_id] = row
    return selected


def find_zip_member(zip_file: zipfile.ZipFile, source_path: str) -> str:
    normalized = source_path.replace("\\", "/")
    names = zip_file.namelist()
    if normalized in names:
        return normalized
    suffix_matches = [name for name in names if name.replace("\\", "/").endswith(normalized)]
    if len(suffix_matches) == 1:
        return suffix_matches[0]
    if not suffix_matches:
        raise FileNotFoundError(f"zip member not found for source path: {source_path}")
    raise ValueError(f"ambiguous zip members for source path: {source_path}")


def image_metadata(image_path: Path) -> dict[str, str]:
    with Image.open(filesystem_path(image_path)) as image:
        return {
            "image_format": image.format or "",
            "pixel_width": str(image.width),
            "pixel_height": str(image.height),
            "color_mode": image.mode,
        }


def metadata_yaml(
    project_id: str,
    asset_id: str,
    asset_path: Path,
    source_row: dict[str, str],
    raw_bytes: bytes,
    output_bytes: bytes,
) -> str:
    image_info = image_metadata(asset_path)
    relative_asset_path = asset_path.as_posix()
    return f"""asset_id: {asset_id}
asset_type: glyph_candidate_image
local_file: {asset_path.name}
canonical_path: {relative_asset_path}
file_size_bytes: {len(output_bytes)}
checksum_sha256: {sha256_bytes(output_bytes)}
image_format: {image_info["image_format"]}
pixel_width: {image_info["pixel_width"]}
pixel_height: {image_info["pixel_height"]}
color_mode: {image_info["color_mode"]}
related_project_ids:
  - {project_id}
related_external_ref_ids:
  - {source_row["primary_external_ref_id"]}
source_id: {source_row["source_id"]}
source_package_id: {source_row["source_package_id"]}
download_id: {source_row["download_id"]}
source_image_path: {source_row["source_image_path"]}
source_image_sequence_in_candidate: {source_row["source_image_sequence_in_candidate"]}
source_image_count_expected: {source_row["source_image_count_expected"]}
raw_source_image_checksum_sha256: {sha256_bytes(raw_bytes)}
rights_status: source_marked_risk_noted
analysis_scope: local_review_image_derivative_only
risk_note: HUST-OBC rights are source-marked with conflicting Figshare and article license signals; this small derivative is committed for preparation-stage review with provenance and risk note.
review_status: needs_human_visual_review
research_boundary: candidate_image_not_scholarship
caution: Source-marked local review image only; not an accepted glyph identity, not an accepted reading, and not a decipherment conclusion.
updated_at: {UPDATED_AT}
"""


def extract_outputs(root: Path) -> dict[str, dict[str, Path | str]]:
    raw_zip_path = root / RAW_ZIP
    if not raw_zip_path.exists():
        raise FileNotFoundError(f"missing HUST-OBC raw zip: {RAW_ZIP}")
    actual_sha256 = sha256_file(raw_zip_path)
    if actual_sha256 != EXPECTED_RAW_SHA256:
        raise ValueError(f"HUST-OBC raw zip checksum mismatch: {actual_sha256}")

    source_rows = read_csv_rows(root / IMAGE_REFERENCE_RESULTS)
    selected_rows = first_reference_rows(source_rows)
    if set(selected_rows) != set(TARGETS):
        missing = sorted(set(TARGETS) - set(selected_rows))
        raise ValueError(f"missing selected source image rows: {missing}")

    outputs: dict[str, dict[str, Path | str]] = {}
    with zipfile.ZipFile(raw_zip_path) as zip_file:
        for project_id, target in TARGETS.items():
            source_row = selected_rows[project_id]
            object_dir = root / target["object_dir"]
            asset_dir = object_dir / "03_visual-assets"
            asset_dir.mkdir(parents=True, exist_ok=True)
            asset_path = asset_dir / target["asset_filename"]
            metadata_path = asset_path.with_suffix(".yaml")
            member_name = find_zip_member(zip_file, source_row["source_image_path"])
            raw_bytes = zip_file.read(member_name)
            with Image.open(io.BytesIO(raw_bytes)) as image:
                image.save(filesystem_path(asset_path), format="PNG")
            with open(filesystem_path(asset_path), "rb") as file:
                output_bytes = file.read()
            metadata_text = metadata_yaml(
                project_id,
                target["asset_id"],
                asset_path.relative_to(root),
                source_row,
                raw_bytes,
                output_bytes,
            )
            with open(filesystem_path(metadata_path), "w", encoding="utf-8", newline="\n") as file:
                file.write(metadata_text)
            update_visual_index(object_dir / "02_visual-source-index.csv", asset_path.relative_to(root))
            outputs[project_id] = {
                "asset_path": asset_path,
                "metadata_path": metadata_path,
                "source_image_path": source_row["source_image_path"],
                "zip_member": member_name,
            }
    return outputs


def update_visual_index(path: Path, relative_asset_path: Path) -> None:
    rows = read_csv_rows(path)
    if not rows:
        raise ValueError(f"empty visual source index: {path}")
    for row in rows:
        row["local_archive_status"] = "registered_external_archive_available_outside_git"
    rows[0]["committed_image_path"] = relative_asset_path.as_posix()
    rows[0]["visual_material_status"] = "committed_review_image_derivative"
    rows[0]["review_status"] = "needs_human_visual_review"
    write_csv(path, rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    args = parser.parse_args()
    outputs = extract_outputs(args.root)
    for project_id, output in outputs.items():
        print(f"{project_id}: {output['asset_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
