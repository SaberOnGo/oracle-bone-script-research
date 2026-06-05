#!/usr/bin/env python3
"""Build an AI Agent context pack for committed public-domain image assets."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ASSET_SOURCE_INDEX = Path("project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv")
ASSET_RIGHTS_REVIEW_LOG = Path("project_registry/004_asset-source-and-rights-index/002_asset-rights-review-log.csv")
ASSET_IMAGE_TECHNICAL_PROFILE = Path(
    "project_registry/004_asset-source-and-rights-index/004_asset-image-technical-profile.csv"
)
ASSET_IMAGE_VISUAL_PROFILE = Path(
    "project_registry/004_asset-source-and-rights-index/005_asset-image-visual-profile.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "006_ai-agent-public-domain-asset-context-pack.json"
)
UPDATED_AT = "2026-06-05"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def rows_by_asset_id(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["asset_id"]: row for row in rows if row.get("asset_id")}


def int_or_none(value: str) -> int | None:
    if value == "":
        return None
    return int(value)


def float_or_none(value: str) -> float | None:
    if value == "":
        return None
    return float(value)


def build_asset_entry(
    asset_row: dict[str, str],
    rights_row: dict[str, str],
    technical_row: dict[str, str],
    visual_row: dict[str, str],
) -> dict[str, object]:
    return {
        "asset_id": asset_row["asset_id"],
        "asset_type": asset_row["asset_type"],
        "canonical_path": asset_row["canonical_path"],
        "primary_external_ref_id": asset_row["primary_external_ref_id"],
        "source_ids": asset_row["source_ids"].split(";"),
        "source_url": asset_row["source_url"],
        "rights_status": asset_row["rights_status"],
        "risk_note": asset_row["risk_note"],
        "rights_review": {
            "review_id": rights_row["review_id"],
            "reviewer": rights_row["reviewer"],
            "rights_status_before": rights_row["rights_status_before"],
            "rights_status_after": rights_row["rights_status_after"],
            "evidence": rights_row["evidence"],
            "reviewed_at": rights_row["reviewed_at"],
            "notes": rights_row["notes"],
        },
        "technical_profile": {
            "image_format": technical_row["image_format"],
            "pixel_width": int(technical_row["pixel_width"]),
            "pixel_height": int(technical_row["pixel_height"]),
            "color_mode": technical_row["color_mode"],
            "dpi_x": int_or_none(technical_row["dpi_x"]),
            "dpi_y": int_or_none(technical_row["dpi_y"]),
            "icc_profile_bytes": int(technical_row["icc_profile_bytes"]),
            "file_size_bytes": int(technical_row["file_size_bytes"]),
            "checksum_sha256": technical_row["checksum_sha256"],
            "analysis_scope": technical_row["analysis_scope"],
        },
        "visual_profile": {
            "analysis_method": visual_row["analysis_method"],
            "luma_threshold": int(visual_row["luma_threshold"]),
            "foreground_bbox": {
                "x_min": int(visual_row["foreground_bbox_x_min"]),
                "y_min": int(visual_row["foreground_bbox_y_min"]),
                "x_max": int(visual_row["foreground_bbox_x_max"]),
                "y_max": int(visual_row["foreground_bbox_y_max"]),
                "width": int(visual_row["foreground_bbox_width"]),
                "height": int(visual_row["foreground_bbox_height"]),
            },
            "foreground_pixel_count": int(visual_row["foreground_pixel_count"]),
            "foreground_pixel_ratio": float_or_none(visual_row["foreground_pixel_ratio"]),
            "mean_luma": float_or_none(visual_row["mean_luma"]),
            "analysis_scope": visual_row["analysis_scope"],
            "caution": visual_row["caution"],
        },
    }


def build_context_pack(
    asset_rows: list[dict[str, str]],
    rights_rows: list[dict[str, str]],
    technical_rows: list[dict[str, str]],
    visual_rows: list[dict[str, str]],
) -> dict[str, object]:
    rights_by_id = rows_by_asset_id(rights_rows)
    technical_by_id = rows_by_asset_id(technical_rows)
    visual_by_id = rows_by_asset_id(visual_rows)

    eligible_assets = [
        row
        for row in asset_rows
        if row.get("asset_type") == "museum_object_image"
        and row.get("rights_status") == "public_domain_verified"
    ]
    asset_entries = [
        build_asset_entry(
            asset_row,
            rights_by_id[asset_row["asset_id"]],
            technical_by_id[asset_row["asset_id"]],
            visual_by_id[asset_row["asset_id"]],
        )
        for asset_row in sorted(eligible_assets, key=lambda row: row["asset_id"])
    ]
    source_ids = sorted({source_id for asset in asset_entries for source_id in asset["source_ids"]})
    return {
        "context_pack_id": "ai-context-public-domain-assets-001",
        "title": "Public-Domain Image Asset Context Pack",
        "title_zh": "公共领域图像资产上下文包",
        "status": "reviewed_metadata_only",
        "updated_at": UPDATED_AT,
        "generated_from": [
            ASSET_SOURCE_INDEX.as_posix(),
            ASSET_RIGHTS_REVIEW_LOG.as_posix(),
            ASSET_IMAGE_TECHNICAL_PROFILE.as_posix(),
            ASSET_IMAGE_VISUAL_PROFILE.as_posix(),
        ],
        "purpose": (
            "Entry-point context for AI Agents that need committed public-domain "
            "image assets, source provenance, rights review, and safe visual "
            "preprocessing metadata before opening the image files."
        ),
        "purpose_zh": (
            "供 AI Agent 在打开图像文件前快速了解已提交公共领域图像资产、"
            "来源追溯、权利复核和安全视觉预处理 metadata 的入口上下文。"
        ),
        "coverage": {
            "asset_count": len(asset_entries),
            "source_count": len(source_ids),
            "source_ids": source_ids,
            "rights_statuses": sorted({asset["rights_status"] for asset in asset_entries}),
            "analysis_scopes": sorted(
                {
                    asset["technical_profile"]["analysis_scope"]
                    for asset in asset_entries
                }
                | {asset["visual_profile"]["analysis_scope"] for asset in asset_entries}
            ),
        },
        "assets": asset_entries,
        "agent_use_rules": [
            "Use this pack as an image-asset routing summary, not as a decipherment result.",
            "Open the cited asset index, rights log, technical profile, and visual profile rows before making any research claim.",
            "Treat luma-threshold regions as preprocessing metadata only; they are not glyph segmentation or component analysis.",
            "Retain The Met object-page and API provenance when reusing or discussing the images.",
        ],
        "agent_use_rules_zh": [
            "本上下文包只作为图像资产检索路由摘要使用，不是释读结果。",
            "提出任何研究判断前，必须打开被引用的资产索引、权利日志、技术画像和视觉画像记录行。",
            "亮度阈值区域只是预处理 metadata，不是字形切分或构件分析。",
            "复用或讨论图像时必须保留 The Met 对象页和 API 来源追溯。",
        ],
    }


def write_json(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    context_pack = build_context_pack(
        read_csv_rows(root / ASSET_SOURCE_INDEX),
        read_csv_rows(root / ASSET_RIGHTS_REVIEW_LOG),
        read_csv_rows(root / ASSET_IMAGE_TECHNICAL_PROFILE),
        read_csv_rows(root / ASSET_IMAGE_VISUAL_PROFILE),
    )
    write_json(root / args.output, context_pack)
    print(
        f"context_pack_id={context_pack['context_pack_id']} "
        f"asset_count={context_pack['coverage']['asset_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
