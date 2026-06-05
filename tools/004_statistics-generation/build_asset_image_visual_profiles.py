#!/usr/bin/env python3
"""Build deterministic visual profiles for committed image assets."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - exercised only when Pillow is absent.
    raise SystemExit("Pillow is required to build image visual profiles.") from exc


ASSET_SOURCE_INDEX = Path("project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv")
DEFAULT_OUTPUT = Path("project_registry/004_asset-source-and-rights-index/005_asset-image-visual-profile.csv")
LUMA_THRESHOLD = 140
UPDATED_AT = "2026-06-05"
ANALYSIS_METHOD = "pillow_luma_threshold_bbox_v1"
ANALYSIS_SCOPE = "visual_preprocessing_metadata_only"
CAUTION = (
    "Algorithmic foreground candidate only; not glyph segmentation, component "
    "analysis, or paleographic interpretation."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def build_visual_profile(asset_row: dict[str, str], root: Path, index: int) -> dict[str, str]:
    asset_path = root / asset_row["canonical_path"]
    with Image.open(asset_path) as image:
        luma = image.convert("L")
        width, height = luma.size
        pixels = luma.tobytes()

    foreground_indices = [idx for idx, value in enumerate(pixels) if value < LUMA_THRESHOLD]
    foreground_count = len(foreground_indices)
    total_pixels = width * height
    mean_luma = sum(pixels) / total_pixels

    if foreground_indices:
        xs = [idx % width for idx in foreground_indices]
        ys = [idx // width for idx in foreground_indices]
        x_min = min(xs)
        x_max = max(xs)
        y_min = min(ys)
        y_max = max(ys)
        bbox_width = x_max - x_min + 1
        bbox_height = y_max - y_min + 1
    else:
        x_min = x_max = y_min = y_max = bbox_width = bbox_height = 0

    return {
        "visual_profile_id": f"asset-visual-profile-{index:06d}",
        "asset_id": asset_row["asset_id"],
        "asset_path": asset_row["canonical_path"],
        "analysis_tool": "Pillow",
        "analysis_method": ANALYSIS_METHOD,
        "luma_threshold": str(LUMA_THRESHOLD),
        "pixel_width": str(width),
        "pixel_height": str(height),
        "foreground_bbox_x_min": str(x_min),
        "foreground_bbox_y_min": str(y_min),
        "foreground_bbox_x_max": str(x_max),
        "foreground_bbox_y_max": str(y_max),
        "foreground_bbox_width": str(bbox_width),
        "foreground_bbox_height": str(bbox_height),
        "foreground_pixel_count": str(foreground_count),
        "foreground_pixel_ratio": f"{foreground_count / total_pixels:.8f}",
        "mean_luma": f"{mean_luma:.4f}",
        "analysis_scope": ANALYSIS_SCOPE,
        "caution": CAUTION,
        "review_status": "reviewed_algorithmic_metadata",
        "updated_at": UPDATED_AT,
    }


def build_visual_profiles(asset_rows: list[dict[str, str]], root: Path) -> list[dict[str, str]]:
    image_rows = [
        row
        for row in asset_rows
        if row.get("asset_type") == "museum_object_image" and row.get("canonical_path")
    ]
    return [
        build_visual_profile(asset_row, root, index)
        for index, asset_row in enumerate(image_rows, start=1)
    ]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows to write: {path}")
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    asset_rows = read_csv_rows(root / ASSET_SOURCE_INDEX)
    visual_rows = build_visual_profiles(asset_rows, root)
    write_csv(root / args.output, visual_rows)
    print(f"visual_profile_rows={len(visual_rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
