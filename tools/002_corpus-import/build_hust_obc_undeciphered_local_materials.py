#!/usr/bin/env python3
"""Build object-local visual materials for all HUST-OBC undeciphered candidates."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import textwrap
import zipfile
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image, ImageStat
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required to profile HUST-OBC glyph images.") from exc


RAW_ZIP = Path("external_local_archive/source_packages/hust-obc/dl-hust-obc-figshare-raw.zip")
UNDECIPHERED_INDEX = Path(
    "corpus/001_oracle-characters/000_character-registers/003_undeciphered-oracle-characters-index.csv"
)
ASSET_SOURCE_INDEX = Path("project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv")
ASSET_RIGHTS_REVIEW_LOG = Path("project_registry/004_asset-source-and-rights-index/002_asset-rights-review-log.csv")
ASSET_ID_SOURCE_MAP = Path("project_registry/002_project-id-to-source-reference-map/003_asset-id-source-map.csv")
ASSET_IMAGE_TECHNICAL_PROFILE = Path(
    "project_registry/004_asset-source-and-rights-index/004_asset-image-technical-profile.csv"
)
ASSET_IMAGE_VISUAL_PROFILE = Path(
    "project_registry/004_asset-source-and-rights-index/005_asset-image-visual-profile.csv"
)

EXPECTED_RAW_SHA256 = "0d00a4de8dd9ce7b7495d7b26f3c80098ee9975b91615211dde02e569bf0ad9d"
FIGSHARE_SOURCE_URL = "https://ndownloader.figshare.com/files/48465988"
UPDATED_AT = "2026-06-20"
LUMA_THRESHOLD = 140
MAX_HUMAN_LINE_LENGTH = 80

RISK_NOTE = (
    "HUST-OBC glyph candidate image extracted from registered large source package for "
    "preparation-stage object-local visual review; rights signals conflict between "
    "Figshare package metadata and the Scientific Data article page."
)
BOUNDARY_CAUTION = (
    "Source-marked candidate image only; not an accepted glyph identity, not an "
    "accepted reading, not a component conclusion, and not a decipherment conclusion."
)


@dataclass(frozen=True)
class Candidate:
    project_id: str
    object_dir: Path
    packet_path: Path
    primary_external_ref_id: str
    source_id: str
    source_package_id: str
    download_id: str
    source_group: str
    source_group_label: str
    source_class_id: str
    source_class_path: str
    source_image_path: str
    source_image_count: str
    rights_status: str
    risk_note: str
    caution: str
    review_status: str


def filesystem_path(path: Path) -> str:
    resolved = path.resolve()
    if os.name == "nt":
        return "\\\\?\\" + str(resolved)
    return str(resolved)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(filesystem_path(path), "rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_size(path: Path) -> int:
    return os.stat(filesystem_path(path)).st_size


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        if not rows:
            raise ValueError(f"cannot infer fieldnames for empty CSV: {path}")
        fieldnames = list(rows[0])
    with open(filesystem_path(path), "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fieldnames} for row in rows])


def wrapped_bullet(text: str) -> str:
    return textwrap.fill(
        f"- {text}",
        width=MAX_HUMAN_LINE_LENGTH,
        subsequent_indent="  ",
        break_long_words=False,
        break_on_hyphens=False,
    )


def wrapped_check(text: str) -> str:
    return textwrap.fill(
        f"- [ ] {text}",
        width=MAX_HUMAN_LINE_LENGTH,
        subsequent_indent="  ",
        break_long_words=False,
        break_on_hyphens=False,
    )


def wrapped_paragraph(text: str) -> str:
    return textwrap.fill(
        text,
        width=MAX_HUMAN_LINE_LENGTH,
        break_long_words=False,
        break_on_hyphens=False,
    )


def upsert_rows(path: Path, key: str, new_rows: list[dict[str, str]]) -> None:
    rows = read_csv(path)
    fields = list(rows[0]) if rows else list(new_rows[0])
    by_key = {row[key]: row for row in rows}
    for row in new_rows:
        by_key[row[key]] = row
    write_csv(path, [by_key[row_key] for row_key in sorted(by_key)], fields)


def sanitize_token(value: str) -> str:
    return "".join(ch if ch.isascii() and (ch.isalnum() or ch in "-_") else "-" for ch in value).strip("-")


def find_zip_member(zip_file: zipfile.ZipFile, source_path: str) -> str:
    normalized = source_path.replace("\\", "/")
    names = zip_file.namelist()
    if normalized in names:
        return normalized
    matches = [name for name in names if name.replace("\\", "/").endswith(normalized)]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise FileNotFoundError(f"zip member not found: {source_path}")
    raise ValueError(f"ambiguous zip member for {source_path}: {matches[:3]}")


def next_asset_number(asset_rows: list[dict[str, str]]) -> int:
    numbers = [
        int(row["asset_id"].rsplit("-", 1)[1])
        for row in asset_rows
        if row.get("asset_id", "").startswith("asset-") and row["asset_id"].rsplit("-", 1)[1].isdigit()
    ]
    return max(numbers, default=0) + 1


def existing_asset_by_project(asset_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {
        row["related_project_ids"]: row
        for row in asset_rows
        if row.get("asset_type") == "glyph_candidate_image"
        and row.get("related_project_ids", "").startswith("obs-unk-")
    }


def load_candidates(root: Path) -> list[Candidate]:
    candidates: list[Candidate] = []
    for row in read_csv(root / UNDECIPHERED_INDEX):
        packet_path = root / row["materialized_candidate_packet_path"]
        object_dir = packet_path.parent
        candidates.append(
            Candidate(
                project_id=row["unknown_candidate_id"],
                object_dir=object_dir,
                packet_path=packet_path,
                primary_external_ref_id=row["primary_external_ref_id"],
                source_id=row["source_id"],
                source_package_id=row["source_package_id"],
                download_id=row["evidence_download_id"],
                source_group=row["source_group"],
                source_group_label=row["source_group_label"],
                source_class_id=row["source_class_id"],
                source_class_path=row["source_class_path"],
                source_image_path=row["first_source_image_path"],
                source_image_count=row["source_image_count"],
                rights_status=row["rights_status"],
                risk_note=row["risk_note"],
                caution=row["caution"],
                review_status=row["review_status"],
            )
        )
    return candidates


def image_info(path: Path) -> dict[str, str]:
    with Image.open(filesystem_path(path)) as image:
        dpi = image.info.get("dpi", ("", ""))
        icc = image.info.get("icc_profile", b"")
        return {
            "image_format": image.format or "",
            "pixel_width": str(image.width),
            "pixel_height": str(image.height),
            "color_mode": image.mode,
            "dpi_x": str(dpi[0]) if dpi and dpi[0] else "",
            "dpi_y": str(dpi[1]) if dpi and len(dpi) > 1 and dpi[1] else "",
            "icc_profile_bytes": str(len(icc) if icc else 0),
        }


def visual_profile(path: Path) -> dict[str, str]:
    with Image.open(filesystem_path(path)) as image:
        gray = image.convert("L")
        width, height = gray.size
        pixels = list(gray.getdata())
        foreground = [(index % width, index // width) for index, value in enumerate(pixels) if value < LUMA_THRESHOLD]
        mean_luma = ImageStat.Stat(gray).mean[0]
    if foreground:
        xs = [point[0] for point in foreground]
        ys = [point[1] for point in foreground]
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        bbox_width = x_max - x_min + 1
        bbox_height = y_max - y_min + 1
    else:
        x_min = y_min = x_max = y_max = bbox_width = bbox_height = 0
    pixel_count = width * height
    foreground_count = len(foreground)
    return {
        "pixel_width": str(width),
        "pixel_height": str(height),
        "foreground_bbox_x_min": str(x_min),
        "foreground_bbox_y_min": str(y_min),
        "foreground_bbox_x_max": str(x_max),
        "foreground_bbox_y_max": str(y_max),
        "foreground_bbox_width": str(bbox_width),
        "foreground_bbox_height": str(bbox_height),
        "foreground_pixel_count": str(foreground_count),
        "foreground_pixel_ratio": f"{foreground_count / pixel_count:.8f}" if pixel_count else "0.00000000",
        "mean_luma": f"{mean_luma:.4f}",
    }


def metadata_yaml(
    candidate: Candidate,
    asset_id: str,
    relative_asset_path: Path,
    raw_bytes: bytes,
    output_path: Path,
) -> str:
    info = image_info(output_path)
    return f"""asset_id: {asset_id}
asset_type: glyph_candidate_image
local_file: {relative_asset_path.name}
canonical_path: {relative_asset_path.as_posix()}
file_size_bytes: {file_size(output_path)}
checksum_sha256: {sha256_file(output_path)}
image_format: {info["image_format"]}
pixel_width: {info["pixel_width"]}
pixel_height: {info["pixel_height"]}
color_mode: {info["color_mode"]}
related_project_ids:
  - {candidate.project_id}
related_external_ref_ids:
  - {candidate.primary_external_ref_id}
source_id: {candidate.source_id}
source_package_id: {candidate.source_package_id}
download_id: {candidate.download_id}
source_image_path: {candidate.source_image_path}
source_image_count_expected: {candidate.source_image_count}
raw_source_image_checksum_sha256: {sha256_bytes(raw_bytes)}
rights_status: {candidate.rights_status}
analysis_scope: local_review_image_derivative_only
risk_note: {RISK_NOTE}
review_status: needs_human_visual_review
research_boundary: candidate_image_not_scholarship
caution: {BOUNDARY_CAUTION}
updated_at: {UPDATED_AT}
"""


def visual_source_index(candidate: Candidate, asset_id: str, relative_asset_path: Path) -> list[dict[str, str]]:
    return [
        {
            "visual_source_index_id": f"{candidate.project_id}-visual-source-001",
            "project_id": candidate.project_id,
            "primary_external_ref_id": candidate.primary_external_ref_id,
            "source_id": candidate.source_id,
            "source_package_id": candidate.source_package_id,
            "download_id": candidate.download_id,
            "asset_id": asset_id,
            "visual_material_status": "committed_review_image_derivative",
            "committed_image_path": relative_asset_path.as_posix(),
            "source_image_reference_path": candidate.source_image_path,
            "source_image_sequence_in_candidate": "001",
            "source_image_count_expected": candidate.source_image_count,
            "registered_storage_hint": RAW_ZIP.as_posix(),
            "resolved_local_archive_path": RAW_ZIP.as_posix(),
            "local_archive_status": "registered_external_archive_available_outside_git",
            "rights_status": candidate.rights_status,
            "risk_note": RISK_NOTE,
            "review_status": "needs_human_visual_review",
            "research_boundary": "co_located_visual_source_index_not_scholarship",
            "caution": BOUNDARY_CAUTION,
            "updated_at": UPDATED_AT,
        }
    ]


def build_visual_source_rows(
    candidate: Candidate,
    asset_id: str,
    relative_asset_path: Path,
    visual_index_path: Path,
) -> list[dict[str, str]]:
    if visual_index_path.exists():
        rows = read_csv(visual_index_path)
        if rows and len(rows) > 1:
            for index, row in enumerate(rows, start=1):
                row["project_id"] = candidate.project_id
                row["primary_external_ref_id"] = candidate.primary_external_ref_id
                row["source_id"] = candidate.source_id
                row["source_package_id"] = row.get("source_package_id") or candidate.source_package_id
                row["download_id"] = row.get("download_id") or candidate.download_id
                row["asset_id"] = asset_id if index == 1 else row.get("asset_id", "")
                row["visual_material_status"] = (
                    "committed_review_image_derivative"
                    if index == 1
                    else row.get("visual_material_status", "source_image_reference_only_no_committed_glyph_image")
                )
                row["committed_image_path"] = relative_asset_path.as_posix() if index == 1 else ""
                row["source_image_sequence_in_candidate"] = (
                    row.get("source_image_sequence_in_candidate") or f"{index:03d}"
                )
                row["source_image_count_expected"] = row.get("source_image_count_expected") or candidate.source_image_count
                row["registered_storage_hint"] = row.get("registered_storage_hint") or RAW_ZIP.as_posix()
                row["resolved_local_archive_path"] = row.get("resolved_local_archive_path") or RAW_ZIP.as_posix()
                row["local_archive_status"] = "registered_external_archive_available_outside_git"
                row["rights_status"] = candidate.rights_status
                row["risk_note"] = row.get("risk_note") or RISK_NOTE
                row["review_status"] = "needs_human_visual_review"
                row["research_boundary"] = row.get("research_boundary") or "co_located_visual_source_index_not_scholarship"
                row["caution"] = row.get("caution") or BOUNDARY_CAUTION
                row["updated_at"] = UPDATED_AT
            return rows
    return visual_source_index(candidate, asset_id, relative_asset_path)


def readme_text(candidate: Candidate, asset_id: str, asset_name: str) -> str:
    return f"""# {candidate.project_id} Local Object Materials / {candidate.project_id} 本地对象资料

English:
This directory is the co-located working folder for one HUST-OBC undeciphered oracle-character candidate. Human-readable notes, the visual gallery, review sheet, source route, local image, and AI-readable packet stay together in this concrete object directory.

简体中文：
本目录是一个 HUST-OBC 未释甲骨字候选的同目录工作资料夹。人类可读说明、图像图库、复核表、来源路线、本地图像和 AI 可读候选包都放在同一具体对象目录内。

## Local Files / 本地文件

- AI-readable packet / AI 可读候选包: `01_undeciphered-candidate-packet.json`
- AI-readable visual/source index / AI 可读图像与来源索引: `02_visual-source-index.csv`
- Human-readable visual gallery / 人类可读图像图库: `04_visual-gallery.md`
- Human review sheet / 人工复核表: `05_human-review-sheet.md`
- Local review image / 本地复核图像: `03_visual-assets/{asset_name}`

## Object Summary / 对象摘要

- Project ID / 项目 ID: `{candidate.project_id}`
- Primary external reference / 首选外部参考: `{candidate.primary_external_ref_id}`
- Source group / 来源分组: `{candidate.source_group}` ({candidate.source_group_label})
- Source class path / 来源分类路径: `{candidate.source_class_path}`
- Source image path / 来源图像路径: `{candidate.source_image_path}`
- Asset ID / 资产 ID: `{asset_id}`

## Boundary / 边界

English:
This is a preparation-stage candidate packet and image entrance. It is not an accepted character record, not an accepted reading, not a component conclusion, and not a decipherment conclusion.

简体中文：
这是准备阶段的候选资料包和图像入口。它不是正式甲骨单字记录，不是已确认释读，不是构件结论，也不是破译结论。
"""


def gallery_text(candidate: Candidate, asset_id: str, asset_name: str, metadata_name: str) -> str:
    return f"""# {candidate.project_id} Visual Gallery / {candidate.project_id} 图像资料页

English:
This human-readable gallery stays inside the same concrete candidate directory as the AI-readable packet and visual/source index.

简体中文：
本图像资料页与 AI 可读候选包、图像与来源索引放在同一个具体候选目录内。

- Visual/source index / 图像与来源索引: `02_visual-source-index.csv`

## Review Image / 复核图像

![{candidate.project_id} glyph candidate](03_visual-assets/{asset_name})

- Asset ID / 资产 ID: `{asset_id}`
- Local image / 本地图像: `03_visual-assets/{asset_name}`
- Local metadata / 本地 metadata: `03_visual-assets/{metadata_name}`
- Source image path / 来源图像路径: `{candidate.source_image_path}`
- Source package / 来源包: `{candidate.source_package_id}`
- Download ID / 下载 ID: `{candidate.download_id}`
- Rights status / 权利状态: `{candidate.rights_status}`
- Risk note / 风险提示: {RISK_NOTE}

## Research Boundary / 研究边界

English:
The image shown here is source-marked preparation material for human visual review. It is not an accepted glyph identity, not an accepted reading, not a component conclusion, and not a decipherment conclusion.

简体中文：
本页图像是带来源标记的准备阶段材料，用于人工视觉复核。它不是已确认字形身份，不是已确认释读，不是构件结论，也不是破译结论。
"""


def review_sheet_text(candidate: Candidate, asset_id: str) -> str:
    english_scope = wrapped_paragraph(
        "Review only whether the local image, packet, and source-route "
        "metadata match the registered HUST-OBC source package. Do not record "
        "a reading, identity confirmation, component conclusion, or "
        "decipherment conclusion here."
    )
    chinese_scope = "\n".join(
        [
            "这里只复核本地图像、候选包和来源路线 metadata 是否对应已登记的",
            "HUST-OBC 来源包。不要在此记录释读、身份确认、构件结论或破译结论。",
        ]
    )
    checklist = "\n".join(
        [
            wrapped_check("Source image path checked against `02_visual-source-index.csv`"),
            wrapped_check("Local review image opens and is readable"),
            wrapped_check(f"Asset registry row checked: `{asset_id}`"),
            wrapped_check("Rights and risk note reviewed"),
            wrapped_check("No formal reading or identity claim added"),
        ]
    )
    concrete_questions = "\n".join(
        [
            wrapped_bullet("Which HUST-OBC source image should be checked first?"),
            wrapped_bullet(
                "Which glyph, codepoint, or later-script route is only a "
                "candidate clue?"
            ),
            wrapped_bullet(
                "Which inscription, plate, collection, findspot, or period "
                "context is still missing?"
            ),
            wrapped_bullet(
                "Which rights status or source-package risk must be rechecked "
                "before reuse?"
            ),
            wrapped_bullet(
                "What evidence is still missing before any formal reading or "
                "identity judgment?"
            ),
            "",
            "- 应先核对哪一张 HUST-OBC 来源图像？",
            "- 哪些字形、codepoint 或后世字形路线只是候选线索？",
            "- 还缺哪些卜辞、图版、馆藏、出土地或时期上下文？",
            "- 复用前还要复核哪些权利状态或来源包风险？",
            "- 正式释读或身份判断前还缺哪些证据？",
        ]
    )
    return f"""# {candidate.project_id} Human Review Sheet / {candidate.project_id} 人工复核表

## Review Scope / 复核范围

English:
{english_scope}

简体中文：
{chinese_scope}

## Checklist / 清单

{checklist}

## Concrete Questions To Check / 具体待查问题

{concrete_questions}

## Status / 状态

- Review status / 复核状态: `needs_human_visual_review`
- Promotion status / 提升状态: `not_promoted`
- Identity claim status / 身份结论状态: `no_identity_claim`
- Decipherment claim status / 释读结论状态: `no_claim`
"""


def asset_source_row(candidate: Candidate, asset_id: str, relative_asset_path: Path, output_path: Path) -> dict[str, str]:
    return {
        "asset_id": asset_id,
        "asset_type": "glyph_candidate_image",
        "canonical_path": relative_asset_path.as_posix(),
        "file_size_bytes": str(file_size(output_path)),
        "related_project_ids": candidate.project_id,
        "primary_external_ref_id": candidate.primary_external_ref_id,
        "source_ids": candidate.source_id,
        "source_url": FIGSHARE_SOURCE_URL,
        "rights_status": candidate.rights_status,
        "risk_note": RISK_NOTE,
        "review_status": "needs_human_visual_review",
        "updated_at": UPDATED_AT,
    }


def rights_row(asset_id: str) -> dict[str, str]:
    number = asset_id.rsplit("-", 1)[1]
    return {
        "review_id": f"asset-rights-review-{number}",
        "asset_id": asset_id,
        "reviewer": "codex-agent",
        "rights_status_before": "unreviewed",
        "rights_status_after": "source_marked_risk_noted",
        "evidence": (
            "HUST-OBC raw package is registered as large-src-000001; Figshare package "
            "metadata reports CC BY 4.0 while the Scientific Data article page uses "
            "CC BY-NC-ND 4.0."
        ),
        "reviewed_at": UPDATED_AT,
        "notes": "Preparation-stage local review image only; not decipherment evidence.",
    }


def asset_map_row(candidate: Candidate, asset_id: str, relative_asset_path: Path) -> dict[str, str]:
    return {
        "project_id": asset_id,
        "record_type": "glyph_candidate_image",
        "canonical_path": relative_asset_path.as_posix(),
        "primary_external_ref_id": candidate.primary_external_ref_id,
        "all_external_ref_ids": f"{candidate.primary_external_ref_id};large-src-000001;{candidate.download_id}",
        "source_ids": candidate.source_id,
        "rights_status": candidate.rights_status,
        "review_status": "needs_human_visual_review",
        "updated_at": UPDATED_AT,
    }


def technical_profile_row(asset_id: str, relative_asset_path: Path, output_path: Path) -> dict[str, str]:
    info = image_info(output_path)
    number = asset_id.rsplit("-", 1)[1]
    return {
        "profile_id": f"asset-image-profile-{number}",
        "asset_id": asset_id,
        "asset_path": relative_asset_path.as_posix(),
        "image_format": info["image_format"],
        "pixel_width": info["pixel_width"],
        "pixel_height": info["pixel_height"],
        "color_mode": info["color_mode"],
        "dpi_x": info["dpi_x"],
        "dpi_y": info["dpi_y"],
        "icc_profile_bytes": info["icc_profile_bytes"],
        "file_size_bytes": str(file_size(output_path)),
        "checksum_sha256": sha256_file(output_path),
        "analysis_tool": "Pillow",
        "analysis_scope": "image_technical_metadata_only",
        "caution": "Technical profile records file properties only; it is not glyph segmentation or paleographic interpretation.",
        "review_status": "needs_human_visual_review",
        "updated_at": UPDATED_AT,
    }


def visual_profile_row(asset_id: str, relative_asset_path: Path, output_path: Path) -> dict[str, str]:
    profile = visual_profile(output_path)
    number = asset_id.rsplit("-", 1)[1]
    return {
        "visual_profile_id": f"asset-visual-profile-{number}",
        "asset_id": asset_id,
        "asset_path": relative_asset_path.as_posix(),
        "analysis_tool": "Pillow",
        "analysis_method": "pillow_luma_threshold_bbox_v1",
        "luma_threshold": str(LUMA_THRESHOLD),
        **profile,
        "analysis_scope": "visual_preprocessing_metadata_only",
        "caution": "Algorithmic foreground candidate only; not glyph segmentation, component analysis, or paleographic interpretation.",
        "review_status": "needs_human_visual_review",
        "updated_at": UPDATED_AT,
    }


def build_materials(root: Path) -> dict[str, int]:
    root = root.resolve()
    raw_zip = root / RAW_ZIP
    if sha256_file(raw_zip) != EXPECTED_RAW_SHA256:
        raise ValueError(f"HUST-OBC raw zip checksum mismatch: {raw_zip}")

    candidates = load_candidates(root)
    asset_rows = read_csv(root / ASSET_SOURCE_INDEX)
    existing_assets = existing_asset_by_project(asset_rows)
    next_number = next_asset_number(asset_rows)

    new_asset_rows: list[dict[str, str]] = []
    new_rights_rows: list[dict[str, str]] = []
    new_map_rows: list[dict[str, str]] = []
    new_technical_rows: list[dict[str, str]] = []
    new_visual_rows: list[dict[str, str]] = []
    reused_asset_count = 0

    with zipfile.ZipFile(raw_zip) as zip_file:
        for candidate in candidates:
            existing = existing_assets.get(candidate.project_id)
            if existing:
                asset_id = existing["asset_id"]
                relative_asset_path = Path(existing["canonical_path"])
                output_path = root / relative_asset_path
                reused_asset_count += 1
            else:
                asset_id = f"asset-{next_number:06d}"
                next_number += 1
                safe_ref = sanitize_token(candidate.primary_external_ref_id)
                asset_dir = candidate.object_dir / "03_visual-assets"
                asset_dir.mkdir(parents=True, exist_ok=True)
                relative_asset_path = (asset_dir / f"001_{asset_id}_{safe_ref}_glyph.jpg").relative_to(root)
                output_path = root / relative_asset_path
                raw_bytes = zip_file.read(find_zip_member(zip_file, candidate.source_image_path))
                with open(filesystem_path(output_path), "wb") as file:
                    file.write(raw_bytes)
                new_asset_rows.append(asset_source_row(candidate, asset_id, relative_asset_path, output_path))
                new_rights_rows.append(rights_row(asset_id))
                new_map_rows.append(asset_map_row(candidate, asset_id, relative_asset_path))
                new_technical_rows.append(technical_profile_row(asset_id, relative_asset_path, output_path))
                new_visual_rows.append(visual_profile_row(asset_id, relative_asset_path, output_path))

            with open(filesystem_path(output_path), "rb") as file:
                output_bytes = file.read()
            metadata_path = output_path.with_suffix(".yaml")
            with open(filesystem_path(metadata_path), "w", encoding="utf-8", newline="\n") as file:
                file.write(metadata_yaml(candidate, asset_id, relative_asset_path, output_bytes, output_path))
            visual_index_path = candidate.object_dir / "02_visual-source-index.csv"
            write_csv(
                visual_index_path,
                build_visual_source_rows(candidate, asset_id, relative_asset_path, visual_index_path),
            )
            asset_name = relative_asset_path.name
            metadata_name = metadata_path.name
            with open(filesystem_path(candidate.object_dir / "README.md"), "w", encoding="utf-8", newline="\n") as file:
                file.write(readme_text(candidate, asset_id, asset_name))
            with open(
                filesystem_path(candidate.object_dir / "04_visual-gallery.md"),
                "w",
                encoding="utf-8",
                newline="\n",
            ) as file:
                file.write(gallery_text(candidate, asset_id, asset_name, metadata_name))
            with open(
                filesystem_path(candidate.object_dir / "05_human-review-sheet.md"),
                "w",
                encoding="utf-8",
                newline="\n",
            ) as file:
                file.write(review_sheet_text(candidate, asset_id))

    if new_asset_rows:
        upsert_rows(root / ASSET_SOURCE_INDEX, "asset_id", new_asset_rows)
        upsert_rows(root / ASSET_RIGHTS_REVIEW_LOG, "asset_id", new_rights_rows)
        upsert_rows(root / ASSET_ID_SOURCE_MAP, "project_id", new_map_rows)
        upsert_rows(root / ASSET_IMAGE_TECHNICAL_PROFILE, "asset_id", new_technical_rows)
        upsert_rows(root / ASSET_IMAGE_VISUAL_PROFILE, "asset_id", new_visual_rows)

    return {
        "candidate_count": len(candidates),
        "new_asset_count": len(new_asset_rows),
        "reused_asset_count": reused_asset_count,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    args = parser.parse_args()
    result = build_materials(args.root)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
