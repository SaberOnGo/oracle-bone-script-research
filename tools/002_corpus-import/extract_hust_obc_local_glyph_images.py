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
ASSET_SOURCE_INDEX = Path("project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv")
ASSET_RIGHTS_REVIEW_LOG = Path("project_registry/004_asset-source-and-rights-index/002_asset-rights-review-log.csv")
ASSET_ID_SOURCE_MAP = Path("project_registry/002_project-id-to-source-reference-map/003_asset-id-source-map.csv")
ASSET_IMAGE_TECHNICAL_PROFILE = Path(
    "project_registry/004_asset-source-and-rights-index/004_asset-image-technical-profile.csv"
)
EXPECTED_RAW_SHA256 = "0d00a4de8dd9ce7b7495d7b26f3c80098ee9975b91615211dde02e569bf0ad9d"
UPDATED_AT = "2026-06-20"
FIGSHARE_SOURCE_URL = "https://ndownloader.figshare.com/files/48465988"
HUST_RISK_NOTE = (
    "HUST-OBC image derivative extracted from registered large source package for local "
    "preparation-stage visual review; rights signals conflict between Figshare and article "
    "page and this is not decipherment evidence."
)
HUST_RIGHTS_EVIDENCE = (
    "HUST-OBC raw package is registered as large-src-000001 with checksum "
    f"{EXPECTED_RAW_SHA256}; Figshare package metadata reports CC BY 4.0 while the "
    "Scientific Data article page uses CC BY-NC-ND 4.0."
)
UNDECIPHERED_TARGETS = {
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
OBS_CHAR_IMAGE_LIMIT = 700
OBS_CHAR_ASSET_ID_START = 6


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


def upsert_rows(path: Path, key: str, new_rows: list[dict[str, str]]) -> None:
    rows = read_csv_rows(path)
    fields = list(rows[0]) if rows else list(new_rows[0])
    by_key = {row[key]: row for row in rows}
    for row in new_rows:
        by_key[row[key]] = row
    ordered_keys = sorted(by_key)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows([{field: by_key[row_key].get(field, "") for field in fields} for row_key in ordered_keys])


def first_reference_rows(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    selected: dict[str, dict[str, str]] = {}
    for row in rows:
        project_id = row.get("unknown_candidate_id", "")
        if project_id in UNDECIPHERED_TARGETS and project_id not in selected:
            selected[project_id] = row
    return selected


def project_id_from_object_dir(path: Path) -> str:
    for part in path.name.split("_"):
        if part.startswith("obs-char-") or part.startswith("obs-unk-"):
            return part
    raise ValueError(f"Cannot find project ID in object directory name: {path}")


def discover_obs_char_targets(root: Path) -> dict[str, dict[str, Path | str]]:
    targets: dict[str, dict[str, Path | str]] = {}
    object_root = root / "corpus/001_oracle-characters"
    for packet_path in sorted(
        object_root.glob("*_obs-char-bucket_oracle-characters/*/01_candidate-character-packet.json")
    ):
        object_dir = packet_path.parent
        project_id = project_id_from_object_dir(object_dir)
        number = int(project_id.rsplit("-", 1)[1])
        if number > OBS_CHAR_IMAGE_LIMIT:
            continue
        packet = json_load(packet_path)
        external_ref = packet["primary_external_ref_id"]
        asset_id = f"asset-{OBS_CHAR_ASSET_ID_START + number - 1:06d}"
        targets[project_id] = {
            "asset_id": asset_id,
            "object_dir": object_dir.relative_to(root),
            "asset_filename": f"001_{asset_id}_{external_ref}_glyph.png",
            "primary_external_ref_id": external_ref,
            "source_category_id": packet["source_candidate"]["source_category_id"],
        }
    expected = {f"obs-char-{index:06d}" for index in range(1, OBS_CHAR_IMAGE_LIMIT + 1)}
    missing = sorted(expected - set(targets))
    if missing:
        raise FileNotFoundError(f"missing obs-char target packets: {missing}")
    return {project_id: targets[project_id] for project_id in sorted(targets)}


def json_load(path: Path) -> dict:
    import json

    return json.loads(path.read_text(encoding="utf-8"))


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


def first_deciphered_member(zip_file: zipfile.ZipFile, source_category_id: str) -> str:
    prefix = f"HUST-OBC/deciphered/{source_category_id}/"
    candidates = [
        name
        for name in zip_file.namelist()
        if name.startswith(prefix)
        and not name.endswith("/")
        and Path(name).suffix.lower() in {".png", ".jpg", ".jpeg"}
    ]
    if not candidates:
        raise FileNotFoundError(f"no deciphered images found for {source_category_id}")
    glyph_candidates = sorted(name for name in candidates if Path(name).name.startswith("G_"))
    return (glyph_candidates or sorted(candidates))[0]


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


def source_row_for_obs_char(target: dict[str, Path | str], member_name: str) -> dict[str, str]:
    return {
        "primary_external_ref_id": str(target["primary_external_ref_id"]),
        "source_id": "src-hust-obc",
        "source_package_id": "large-src-000001",
        "download_id": "dl-hust-obc-figshare-raw",
        "source_image_path": member_name,
        "source_image_sequence_in_candidate": "001",
        "source_image_count_expected": "not_counted_for_deciphered_category_yet",
    }


def asset_source_rows(outputs: dict[str, dict[str, Path | str]]) -> list[dict[str, str]]:
    rows = []
    for project_id, output in outputs.items():
        rows.append(
            {
                "asset_id": str(output["asset_id"]),
                "asset_type": "glyph_candidate_image",
                "canonical_path": Path(output["asset_path"]).as_posix(),
                "file_size_bytes": str(Path(output["asset_path_abs"]).stat().st_size),
                "related_project_ids": project_id,
                "primary_external_ref_id": str(output["primary_external_ref_id"]),
                "source_ids": "src-hust-obc",
                "source_url": FIGSHARE_SOURCE_URL,
                "rights_status": "source_marked_risk_noted",
                "risk_note": HUST_RISK_NOTE,
                "review_status": "needs_human_visual_review",
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def asset_rights_rows(outputs: dict[str, dict[str, Path | str]]) -> list[dict[str, str]]:
    rows = []
    for output in outputs.values():
        asset_number = str(output["asset_id"]).rsplit("-", 1)[1]
        rows.append(
            {
                "review_id": f"asset-rights-review-{asset_number}",
                "asset_id": str(output["asset_id"]),
                "reviewer": "codex-agent",
                "previous_rights_status": "unreviewed",
                "reviewed_rights_status": "source_marked_risk_noted",
                "rights_evidence": HUST_RIGHTS_EVIDENCE,
                "review_date": UPDATED_AT,
                "risk_note": (
                    "Small glyph candidate derivative committed for preparation-stage local visual "
                    "review with visible risk note; not an accepted reading, component conclusion, "
                    "or decipherment conclusion."
                ),
            }
        )
    return rows


def asset_map_rows(outputs: dict[str, dict[str, Path | str]]) -> list[dict[str, str]]:
    rows = []
    for project_id, output in outputs.items():
        rows.append(
            {
                "project_id": str(output["asset_id"]),
                "project_id_type": "glyph_candidate_image",
                "preferred_path": Path(output["asset_path"]).as_posix(),
                "primary_external_ref_id": str(output["primary_external_ref_id"]),
                "external_ref_ids": f"{output['primary_external_ref_id']};large-src-000001;dl-hust-obc-figshare-raw",
                "source_ids": "src-hust-obc",
                "rights_status": "source_marked_risk_noted",
                "review_status": "needs_human_visual_review",
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def technical_profile_rows(outputs: dict[str, dict[str, Path | str]]) -> list[dict[str, str]]:
    rows = []
    for output in outputs.values():
        asset_id = str(output["asset_id"])
        asset_path_abs = Path(output["asset_path_abs"])
        image_info = image_metadata(asset_path_abs)
        rows.append(
            {
                "profile_id": f"asset-image-profile-{asset_id.rsplit('-', 1)[1]}",
                "asset_id": asset_id,
                "asset_path": Path(output["asset_path"]).as_posix(),
                "image_format": image_info["image_format"],
                "pixel_width": image_info["pixel_width"],
                "pixel_height": image_info["pixel_height"],
                "color_mode": image_info["color_mode"],
                "dpi_x": "",
                "dpi_y": "",
                "icc_profile_bytes": "0",
                "file_size_bytes": str(asset_path_abs.stat().st_size),
                "checksum_sha256": sha256_file(asset_path_abs),
                "analysis_tool": "Pillow",
                "analysis_scope": "image_technical_metadata_only",
                "caution": (
                    "Technical profile records file properties only; it is not glyph "
                    "segmentation or paleographic interpretation."
                ),
                "review_status": "needs_human_visual_review",
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def extract_outputs(root: Path) -> dict[str, dict[str, Path | str]]:
    raw_zip_path = root / RAW_ZIP
    if not raw_zip_path.exists():
        raise FileNotFoundError(f"missing HUST-OBC raw zip: {RAW_ZIP}")
    actual_sha256 = sha256_file(raw_zip_path)
    if actual_sha256 != EXPECTED_RAW_SHA256:
        raise ValueError(f"HUST-OBC raw zip checksum mismatch: {actual_sha256}")

    source_rows = read_csv_rows(root / IMAGE_REFERENCE_RESULTS)
    selected_rows = first_reference_rows(source_rows)
    if set(selected_rows) != set(UNDECIPHERED_TARGETS):
        missing = sorted(set(UNDECIPHERED_TARGETS) - set(selected_rows))
        raise ValueError(f"missing selected source image rows: {missing}")

    outputs: dict[str, dict[str, Path | str]] = {}
    targets = {**UNDECIPHERED_TARGETS, **discover_obs_char_targets(root)}
    with zipfile.ZipFile(raw_zip_path) as zip_file:
        for project_id, target in targets.items():
            if project_id in selected_rows:
                source_row = selected_rows[project_id]
                member_name = find_zip_member(zip_file, source_row["source_image_path"])
            else:
                member_name = first_deciphered_member(zip_file, str(target["source_category_id"]))
                source_row = source_row_for_obs_char(target, member_name)
            object_dir = root / target["object_dir"]
            asset_dir = object_dir / "03_visual-assets"
            asset_dir.mkdir(parents=True, exist_ok=True)
            asset_path = asset_dir / target["asset_filename"]
            metadata_path = asset_path.with_suffix(".yaml")
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
            update_visual_index(object_dir / "02_visual-source-index.csv", asset_path.relative_to(root), source_row)
            outputs[project_id] = {
                "asset_id": target["asset_id"],
                "asset_path": asset_path,
                "asset_path_abs": asset_path,
                "metadata_path": metadata_path,
                "source_image_path": source_row["source_image_path"],
                "zip_member": member_name,
                "primary_external_ref_id": source_row["primary_external_ref_id"],
            }
    obs_char_outputs = {
        project_id: output for project_id, output in outputs.items() if project_id.startswith("obs-char-")
    }
    if obs_char_outputs:
        upsert_rows(root / ASSET_SOURCE_INDEX, "asset_id", asset_source_rows(obs_char_outputs))
        upsert_rows(root / ASSET_RIGHTS_REVIEW_LOG, "asset_id", asset_rights_rows(obs_char_outputs))
        upsert_rows(root / ASSET_ID_SOURCE_MAP, "project_id", asset_map_rows(obs_char_outputs))
        upsert_rows(root / ASSET_IMAGE_TECHNICAL_PROFILE, "asset_id", technical_profile_rows(obs_char_outputs))
    return outputs


def update_visual_index(path: Path, relative_asset_path: Path, source_row: dict[str, str]) -> None:
    rows = read_csv_rows(path)
    if not rows:
        raise ValueError(f"empty visual source index: {path}")
    for row in rows:
        row["local_archive_status"] = "registered_external_archive_available_outside_git"
        if not row.get("source_package_id"):
            row["source_package_id"] = "large-src-000001"
        if not row.get("download_id") or row.get("download_id") == "dl-hust-obc-validation-label;dl-hust-obc-ocr-id-to-chinese":
            row["download_id"] = "dl-hust-obc-figshare-raw"
        if not row.get("registered_storage_hint"):
            row["registered_storage_hint"] = RAW_ZIP.as_posix()
        if not row.get("resolved_local_archive_path"):
            row["resolved_local_archive_path"] = str(RAW_ZIP)
        if not row.get("risk_note"):
            row["risk_note"] = HUST_RISK_NOTE
        if not row.get("source_image_reference_path"):
            row["source_image_reference_path"] = source_row["source_image_path"]
        if not row.get("source_image_sequence_in_candidate"):
            row["source_image_sequence_in_candidate"] = source_row["source_image_sequence_in_candidate"]
        if not row.get("source_image_count_expected"):
            row["source_image_count_expected"] = source_row["source_image_count_expected"]
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
