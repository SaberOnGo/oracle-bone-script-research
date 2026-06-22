#!/usr/bin/env python3
"""Build object-local materials for collection/museum object candidates."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import textwrap
from pathlib import Path


COLLECTION_ROOT = Path("corpus/005_excavation-sites-periods-and-batches")
REGISTER_ROOT = COLLECTION_ROOT / "000_collection-registers"
OBJECT_ROOT = COLLECTION_ROOT / "002_collection-object-candidates"
OBJECT_ID_MAP = Path(
    "project_registry/002_project-id-to-source-reference-map/"
    "006_collection-object-id-source-map.csv"
)
ASSET_SOURCE_INDEX = Path(
    "project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv"
)
ASSET_TECHNICAL_PROFILE = Path(
    "project_registry/004_asset-source-and-rights-index/004_asset-image-technical-profile.csv"
)
ASSET_VISUAL_PROFILE = Path(
    "project_registry/004_asset-source-and-rights-index/005_asset-image-visual-profile.csv"
)

UPDATED_AT = "2026-06-20"
RECORD_TYPE = "collection_object_candidate"
REVIEW_STATUS = "needs_human_collection_object_review"
RESEARCH_BOUNDARY = "collection_object_candidate_not_inscription_identity_not_decipherment"
CAUTION = (
    "This collection object directory is a preprocessing research entrance only. "
    "Object metadata, catalog labels, image links, and public-domain asset previews "
    "must not be treated as inscription identity, transcription, formal reading, "
    "component analysis, or decipherment conclusions."
)
MAX_HUMAN_LINE_LENGTH = 80

STAGING_SPECS = [
    (
        REGISTER_ROOT / "002_ihp-museum-oracle-bone-object-staging.csv",
        "ihp",
        "ihp-item",
    ),
    (
        REGISTER_ROOT / "003_smithsonian-nmaa-oracle-bone-object-staging.csv",
        "smithsonian",
        "si-nmaa",
    ),
    (
        REGISTER_ROOT / "004_penn-museum-oracle-bone-object-staging.csv",
        "penn",
        "penn-obj",
    ),
    (
        REGISTER_ROOT / "005_metmuseum-oracle-bone-object-staging.csv",
        "met",
        "met-obj",
    ),
]

MAP_FIELDS = [
    "project_id",
    "record_type",
    "canonical_path",
    "primary_external_ref_id",
    "all_external_ref_ids",
    "source_ids",
    "rights_status",
    "review_status",
    "updated_at",
]

SOURCE_INDEX_FIELDS = [
    "source_index_id",
    "project_id",
    "candidate_collection_object_id",
    "source_id",
    "evidence_download_id",
    "source_file_path",
    "source_row_id",
    "object_page_url",
    "source_collection_item_id",
    "rights_status",
    "project_import_status",
    "review_status",
    "research_boundary",
    "caution",
    "updated_at",
]

VISUAL_INDEX_FIELDS = [
    "visual_index_id",
    "project_id",
    "candidate_collection_object_id",
    "visual_entry_type",
    "asset_id",
    "asset_path",
    "thumbnail_url",
    "source_image_url",
    "rights_status",
    "download_or_commit_status",
    "technical_profile_status",
    "visual_profile_status",
    "review_status",
    "caution",
    "updated_at",
]

MANIFEST_FIELDS = [
    "project_id",
    "candidate_collection_object_id",
    "candidate_directory",
    "packet_path",
    "source_index_path",
    "visual_index_path",
    "gallery_path",
    "human_review_sheet_path",
    "human_collection_dossier_path",
    "collection_dossier_index_path",
    "source_id",
    "rights_status",
    "visual_entry_status",
    "review_status",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def safe_token(value: str) -> str:
    token = re.sub(r"[^0-9A-Za-z]+", "-", value.strip()).strip("-").lower()
    return token or "extid-unassigned"


def primary_external_ref(row: dict[str, str], external_prefix: str) -> str:
    return f"{external_prefix}-{safe_token(row.get('source_collection_item_id', ''))}"


def project_id(index: int) -> str:
    return f"coll-obj-cand-{index:05d}"


def object_dir(index: int, row: dict[str, str], external_prefix: str) -> Path:
    return OBJECT_ROOT / (
        f"{index:03d}_{project_id(index)}_"
        f"{primary_external_ref(row, external_prefix)}_collection-object-candidate"
    )


def load_object_rows(root: Path) -> list[tuple[Path, str, str, int, dict[str, str]]]:
    rows: list[tuple[Path, str, str, int, dict[str, str]]] = []
    for path, provider_key, external_prefix in STAGING_SPECS:
        for source_row_index, row in enumerate(read_csv_rows(root / path), start=1):
            rows.append((path, provider_key, external_prefix, source_row_index, row))
    return rows


def load_assets(root: Path) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    asset_by_related: dict[str, dict[str, str]] = {}
    for row in read_csv_rows(root / ASSET_SOURCE_INDEX):
        for related_project_id in row.get("related_project_ids", "").split(";"):
            if related_project_id:
                asset_by_related[related_project_id] = row
    technical_by_asset = {
        row["asset_id"]: row
        for row in read_csv_rows(root / ASSET_TECHNICAL_PROFILE)
    }
    visual_by_asset = {
        row["asset_id"]: row
        for row in read_csv_rows(root / ASSET_VISUAL_PROFILE)
    }
    return asset_by_related, technical_by_asset, visual_by_asset


def selected_metadata(row: dict[str, str]) -> dict[str, str]:
    ordered_fields = [
        "provider",
        "collection_name",
        "source_collection_item_id",
        "object_title_en",
        "catalog_reference_text",
        "accession_number",
        "historical_period",
        "object_date",
        "culture",
        "provenience",
        "geography",
        "medium",
        "materials",
        "dimensions",
        "credit_line",
        "provenance_note",
        "current_location",
        "repository",
        "object_page_url",
        "api_url",
        "primary_image_url",
        "thumbnail_url",
    ]
    return {field: row.get(field, "") for field in ordered_fields if row.get(field, "")}


def source_index_row(
    index: int,
    source_path: Path,
    source_row_index: int,
    row: dict[str, str],
) -> dict[str, str]:
    return {
        "source_index_id": f"{project_id(index)}-source-01",
        "project_id": project_id(index),
        "candidate_collection_object_id": row["candidate_collection_object_id"],
        "source_id": row["source_id"],
        "evidence_download_id": row["evidence_download_id"],
        "source_file_path": source_path.as_posix(),
        "source_row_id": str(source_row_index),
        "object_page_url": row.get("object_page_url", ""),
        "source_collection_item_id": row.get("source_collection_item_id", ""),
        "rights_status": row["rights_status"],
        "project_import_status": row["project_import_status"],
        "review_status": row["review_status"],
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def visual_index_row(
    index: int,
    row: dict[str, str],
    asset_row: dict[str, str] | None,
    technical_row: dict[str, str] | None,
    visual_row: dict[str, str] | None,
) -> dict[str, str]:
    if asset_row:
        return {
            "visual_index_id": f"{project_id(index)}-visual-01",
            "project_id": project_id(index),
            "candidate_collection_object_id": row["candidate_collection_object_id"],
            "visual_entry_type": "committed_public_domain_asset",
            "asset_id": asset_row["asset_id"],
            "asset_path": asset_row["canonical_path"],
            "thumbnail_url": row.get("thumbnail_url", ""),
            "source_image_url": asset_row["source_url"],
            "rights_status": asset_row["rights_status"],
            "download_or_commit_status": "committed_under_size_limit",
            "technical_profile_status": technical_row["review_status"] if technical_row else "missing",
            "visual_profile_status": visual_row["review_status"] if visual_row else "missing",
            "review_status": "reviewed_metadata_only",
            "caution": asset_row["risk_note"],
            "updated_at": UPDATED_AT,
        }
    if row.get("thumbnail_url"):
        return {
            "visual_index_id": f"{project_id(index)}-visual-01",
            "project_id": project_id(index),
            "candidate_collection_object_id": row["candidate_collection_object_id"],
            "visual_entry_type": "external_thumbnail_url_metadata_only",
            "asset_id": "",
            "asset_path": "",
            "thumbnail_url": row.get("thumbnail_url", ""),
            "source_image_url": row.get("primary_image_url", ""),
            "rights_status": row["rights_status"],
            "download_or_commit_status": row.get("thumbnail_download_status", "not_downloaded_metadata_only"),
            "technical_profile_status": "not_available_metadata_only",
            "visual_profile_status": "not_available_metadata_only",
            "review_status": row["review_status"],
            "caution": row["caution"],
            "updated_at": UPDATED_AT,
        }
    return {
        "visual_index_id": f"{project_id(index)}-visual-01",
        "project_id": project_id(index),
        "candidate_collection_object_id": row["candidate_collection_object_id"],
        "visual_entry_type": "no_committed_visual_asset",
        "asset_id": "",
        "asset_path": "",
        "thumbnail_url": "",
        "source_image_url": row.get("primary_image_url", ""),
        "rights_status": row["rights_status"],
        "download_or_commit_status": "not_downloaded_metadata_only",
        "technical_profile_status": "not_available_metadata_only",
        "visual_profile_status": "not_available_metadata_only",
        "review_status": row["review_status"],
        "caution": row["caution"],
        "updated_at": UPDATED_AT,
    }


def packet_payload(
    index: int,
    relative_dir: Path,
    row: dict[str, str],
    primary_ref: str,
    source_row: dict[str, str],
    visual_row: dict[str, str],
) -> dict[str, object]:
    return {
        "project_id": project_id(index),
        "record_type": RECORD_TYPE,
        "candidate_collection_object_id": row["candidate_collection_object_id"],
        "primary_external_ref_id": primary_ref,
        "canonical_path": relative_dir.as_posix(),
        "object_metadata": selected_metadata(row),
        "source_index": source_row,
        "visual_index": visual_row,
        "object_identity_claim_status": "not_confirmed",
        "inscription_record_status": "not_promoted_to_formal_inscription_record",
        "transcription_status": "not_collected",
        "decipherment_status": "not_applicable_preprocessing_only",
        "project_import_status": row["project_import_status"],
        "rights_status": row["rights_status"],
        "review_status": REVIEW_STATUS,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def metadata_lines(metadata: dict[str, str]) -> str:
    return "\n".join(f"- {key}: `{value}`" for key, value in metadata.items())


def wrapped_bullet(text: str) -> str:
    return textwrap.fill(
        f"- {text}",
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


def relative_link(from_dir: Path, target: str) -> str:
    if not target:
        return ""
    return Path(os.path.relpath(target, start=from_dir.as_posix())).as_posix()


def readme_text(index: int, row: dict[str, str], metadata: dict[str, str], visual_row: dict[str, str]) -> str:
    image_note = "No committed image asset is available for this object yet."
    asset_path = visual_row.get("asset_path", "")
    if asset_path:
        rel_asset = relative_link(object_dir(index, row, "x"), asset_path)
        image_note = f"Committed image asset: `asset_id={visual_row['asset_id']}`.\n\n![object image]({rel_asset})"
    elif visual_row.get("thumbnail_url"):
        image_note = f"External thumbnail URL metadata only: {visual_row['thumbnail_url']}"

    return f"""# {project_id(index)} collection object candidate

English:
This directory is the object-local research entrance for one museum or collection object candidate. Human-readable notes, visual routes, review prompts, and AI-readable packet/index files are stored together in this concrete `corpus/005_excavation-sites-periods-and-batches` object directory.

简体中文：
本目录是一个馆藏或出土相关对象候选的对象内研究入口。人类可读说明、图像入口、复核提示和 AI 可读 packet/index 文件放在同一个具体 `corpus/005_excavation-sites-periods-and-batches` 对象目录里，不另建并行的人类资料目录。

## Boundary / 边界

- This is not a confirmed inscription identity.
- This is not a transcription, formal reading, component analysis, or decipherment conclusion.
- Object labels and image links are source metadata for review only.
- 本对象不是已确认的卜辞身份，不是释文、正式释读、构件分析或破译结论；馆藏标签和图像链接只作为待复核来源 metadata。

## Visual Entrance / 图像入口

{image_note}

## Local Files / 本目录文件

- `01_collection-object-packet.json`: AI-readable object candidate packet.
- `02_collection-source-index.csv`: source, download, rights, and route index.
- `03_visual-asset-index.csv`: committed asset, thumbnail URL, or missing-image status.
- `04_visual-gallery.md`: human-facing image or thumbnail route sheet.
- `05_human-review-sheet.md`: human review checklist.
- `06_human-collection-dossier.md`: human collection object dossier.
- `07_collection-dossier-index.json`: AI-readable dossier support index.

## Object Metadata / 对象 metadata

{metadata_lines(metadata)}

## Review Status / 复核状态

Current status: `{REVIEW_STATUS}`. Reviewers must verify source pages, rights status, object labels, image provenance, and inscription context before promotion.
"""


def collection_dossier_text(
    index: int,
    row: dict[str, str],
    metadata: dict[str, str],
    source_row: dict[str, str],
    visual_row: dict[str, str],
) -> str:
    pid = project_id(index)
    visual_status = visual_row.get("visual_entry_type", "unknown")
    intro_en = wrapped_paragraph(
        "This human-readable dossier gathers the object-level evidence a "
        "researcher should inspect before trusting a museum or collection "
        "object candidate: catalog clues, image route, source trail, rights "
        "status, and the missing findspot, period, batch, plate, inscription, "
        "and character context."
    )
    intro_zh = wrapped_paragraph(
        "\u672c\u6863\u6848\u6c47\u603b\u590d\u6838\u9986\u85cf\u6216"
        "\u51fa\u571f\u76f8\u5173\u5bf9\u8c61\u524d\u9700\u6253\u5f00"
        "\u7684\u5bf9\u8c61\u5c42\u8bc1\u636e\uff1a\u8457\u5f55\u7ebf\u7d22"
        "\u3001\u56fe\u50cf\u8def\u7ebf\u3001\u6765\u6e90\u94fe\u3001"
        "\u6743\u5229\u72b6\u6001\uff0c\u4ee5\u53ca\u5c1a\u7f3a\u7684"
        "\u51fa\u571f\u5730\u3001\u65f6\u671f\u3001\u6279\u6b21\u3001"
        "\u56fe\u7248\u3001\u535c\u8f9e\u548c\u7532\u9aa8\u5355\u5b57"
        "\u8bed\u5883\u3002"
    )
    boundary = wrapped_paragraph(
        "This is not a confirmed collection object identity, not a confirmed "
        "inscription identity, not a transcription, not a formal reading, and "
        "not a decipherment conclusion."
    )
    metadata_rows = "\n".join(
        f"| `{key}` | `{value}` |" for key, value in metadata.items()
    )
    if not metadata_rows:
        metadata_rows = "| metadata | pending source-page review |"
    questions = [
        "Which museum object page, catalog row, or accession record should be opened first?",
        "\u5e94\u5148\u6253\u5f00\u54ea\u4e2a\u9986\u85cf\u5bf9\u8c61"
        "\u9875\u3001\u8457\u5f55\u884c\u6216\u767b\u8bb0\u53f7\u8bb0\u5f55\uff1f",
        "Which image route is local, external-only, or still missing?",
        "\u54ea\u6761\u56fe\u50cf\u8def\u7ebf\u662f\u672c\u5730\u3001"
        "\u4ec5\u5916\u90e8\u6216\u4ecd\u7f3a\u5931\uff1f",
        "Which findspot, period, batch, or plate provenance needs checking?",
        "\u9700\u8981\u6838\u5bf9\u54ea\u4e9b\u51fa\u571f\u5730\u3001"
        "\u65f6\u671f\u3001\u6279\u6b21\u6216\u56fe\u7248\u51fa\u5904\uff1f",
        "Which inscription, glyph, or oracle character route is only a candidate?",
        "\u54ea\u4e9b\u535c\u8f9e\u3001\u5b57\u5f62\u6216"
        "\u7532\u9aa8\u5355\u5b57\u8def\u7ebf\u4ecd\u53ea\u662f\u5019\u9009\uff1f",
        "Which source, checksum, rights status, or risk note must be reviewed?",
        "\u8fd8\u8981\u590d\u6838\u54ea\u4e9b\u6765\u6e90\u3001checksum"
        "\u3001\u6743\u5229\u72b6\u6001\u6216\u98ce\u9669\u63d0\u793a\uff1f",
        "What evidence is missing before any object identity claim?",
        "\u5f62\u6210\u4efb\u4f55\u5bf9\u8c61\u8eab\u4efd\u7ed3\u8bba"
        "\u524d\u8fd8\u7f3a\u54ea\u4e9b\u8bc1\u636e\uff1f",
    ]
    question_lines = "\n".join(wrapped_bullet(text) for text in questions)
    lines = [
        (
            "# Human Collection Object Dossier / "
            f"\u9986\u85cf\u5bf9\u8c61\u7814\u7a76\u6863\u6848: {pid}"
        ),
        "",
        "English:",
        intro_en,
        "",
        "\u7b80\u4f53\u4e2d\u6587\uff1a",
        intro_zh,
        "",
        (
            "## Object Identity And Catalog Clues / "
            "\u9986\u85cf\u5bf9\u8c61\u4e0e\u8457\u5f55\u7ebf\u7d22"
        ),
        "",
        f"- project_id: `{pid}`",
        f"- candidate_collection_object_id: `{row['candidate_collection_object_id']}`",
        f"- source_collection_item_id: `{row.get('source_collection_item_id', '')}`",
        f"- accession_number: `{row.get('accession_number', '') or 'pending'}`",
        "",
        "| Metadata field | Source value |",
        "| --- | --- |",
        metadata_rows,
        "",
        "## Visual And Image Route / \u56fe\u50cf\u8def\u7ebf",
        "",
        f"- visual_entry_type: `{visual_status}`",
        "- visual_index: `03_visual-asset-index.csv`",
        "- visual_gallery: `04_visual-gallery.md`",
        "",
        (
            "## Findspot Period Batch And Plate Checks / "
            "\u51fa\u571f\u5730\u3001\u65f6\u671f\u3001\u6279\u6b21"
            "\u4e0e\u56fe\u7248\u590d\u6838"
        ),
        "",
        "- findspot_or_provenience: source metadata only; needs review",
        "- period_or_date: source metadata only; needs review",
        "- batch_context: not collected; needs source checking",
        "- plate_or_catalog_context: not collected; needs source checking",
        "",
        (
            "## Inscription And Character Links / "
            "\u535c\u8f9e\u4e0e\u7532\u9aa8\u5355\u5b57\u5173\u8054"
        ),
        "",
        "- inscription_identity_claim: `not_confirmed`",
        "- transcription_status: `not_collected`",
        "- character_link_status: candidate route only",
        "",
        (
            "## Source Evidence And Rights Trail / "
            "\u6765\u6e90\u8bc1\u636e\u4e0e\u6743\u5229\u94fe"
        ),
        "",
        f"- source_id: `{source_row['source_id']}`",
        f"- evidence_download_id: `{source_row['evidence_download_id']}`",
        f"- rights_status: `{source_row['rights_status']}`",
        f"- review_status: `{REVIEW_STATUS}`",
        "",
        "## Concrete Questions To Check / \u5177\u4f53\u5f85\u67e5\u95ee\u9898",
        "",
        question_lines,
        "",
        "## Review Boundary / \u590d\u6838\u8fb9\u754c",
        "",
        boundary,
        "- not a confirmed collection object identity",
        "- not a confirmed inscription identity",
        "- not a transcription",
        "- not a formal reading",
        "- not a decipherment conclusion",
    ]
    return "\n".join(lines) + "\n"


def collection_dossier_index_payload(
    index: int,
    relative_dir: Path,
    row: dict[str, str],
    source_row: dict[str, str],
    visual_row: dict[str, str],
) -> dict[str, object]:
    return {
        "project_id": project_id(index),
        "record_type": "collection_object_candidate_dossier_index",
        "candidate_collection_object_id": row["candidate_collection_object_id"],
        "human_readable_files": [
            (relative_dir / "README.md").as_posix(),
            (relative_dir / "04_visual-gallery.md").as_posix(),
            (relative_dir / "05_human-review-sheet.md").as_posix(),
            (relative_dir / "06_human-collection-dossier.md").as_posix(),
        ],
        "ai_support_files": [
            (relative_dir / "01_collection-object-packet.json").as_posix(),
            (relative_dir / "02_collection-source-index.csv").as_posix(),
            (relative_dir / "03_visual-asset-index.csv").as_posix(),
            (relative_dir / "07_collection-dossier-index.json").as_posix(),
        ],
        "source_route_files": [
            source_row["source_file_path"],
            (relative_dir / "02_collection-source-index.csv").as_posix(),
            (relative_dir / "03_visual-asset-index.csv").as_posix(),
            (relative_dir / "04_visual-gallery.md").as_posix(),
            (relative_dir / "06_human-collection-dossier.md").as_posix(),
        ],
        "uncollected_human_research_fields": [
            "findspot_period_batch_plate_context",
            "inscription_occurrence_context",
            "oracle_character_context",
            "catalog_publication_history",
            "object_identity_review_history",
        ],
        "visual_entry_type": visual_row.get("visual_entry_type", ""),
        "claim_boundary": (
            "no confirmed collection object identity; no confirmed inscription "
            "identity; no transcription; no formal reading; no decipherment "
            "conclusion"
        ),
        "rights_status": source_row["rights_status"],
        "review_status": REVIEW_STATUS,
        "updated_at": UPDATED_AT,
    }


def gallery_text(index: int, row: dict[str, str], visual_row: dict[str, str]) -> str:
    if visual_row.get("asset_path"):
        rel_asset = relative_link(object_dir(index, row, "x"), visual_row["asset_path"])
        body = f"""## Committed Asset / 已提交图像

![object image]({rel_asset})

- Asset ID: `{visual_row['asset_id']}`
- Asset path: `{visual_row['asset_path']}`
- Source image URL: {visual_row['source_image_url']}
- Rights status: `{visual_row['rights_status']}`
"""
    elif visual_row.get("thumbnail_url"):
        body = f"""## External Thumbnail Route / 外部缩略图入口

Thumbnail URL metadata is preserved, but the image is not downloaded or committed in this stage:

{visual_row['thumbnail_url']}

Rights status: `{visual_row['rights_status']}`
"""
    else:
        body = """## No Local Image Yet / 暂无本地图像

No committed image asset is available for this candidate. Open the source object page through `02_collection-source-index.csv` before any visual review.
"""
    return f"""# Visual Gallery / 图像入口

Project ID: `{project_id(index)}`

{body}

## Boundary / 边界

This page is a human visual entrance only. It is not glyph segmentation, not component analysis, not a transcription, and not a decipherment conclusion.
"""


def review_sheet_text(index: int, row: dict[str, str]) -> str:
    required_checks = "\n".join(
        wrapped_bullet(text)
        for text in [
            "Open `02_collection-source-index.csv` and verify the source, download, and rights trail.",
            "Open `03_visual-asset-index.csv` and confirm whether the image is committed, external-only, or missing.",
            "Compare object-page labels against catalog references, collection provenance, and inscription context.",
            "Do not record inscription identity, transcription, formal reading, component analysis, or decipherment conclusions here.",
        ]
    )
    concrete_questions = "\n".join(
        [
            wrapped_bullet("Which collection object, thumbnail, or public image route should be opened first?"),
            wrapped_bullet("Which accession, catalog, or object ID is only a source clue?"),
            wrapped_bullet("Which findspot, period, batch, or plate provenance still needs checking?"),
            wrapped_bullet("Which rights status or reuse risk must be rechecked before public use?"),
            wrapped_bullet("Which inscription, glyph, or character link is only a candidate route?"),
            wrapped_bullet("What evidence is still missing before any collection-object identity claim?"),
            "",
            "- 应先核对哪些馆藏对象、缩略图或公开图像路线？",
            "- 哪些 accession、catalog 或 object ID 只是来源线索？",
            "- 需要核对哪些出土地、时期、批次或图版出处？",
            "- 公开使用前还要复核哪些权利状态或复用风险？",
            "- 哪些卜辞、字形或单字关系只是候选路线？",
            "- 正式馆藏对象身份结论前还缺哪些证据？",
        ]
    )
    caution = wrapped_paragraph(CAUTION)
    return f"""# Human Review Sheet / 人工复核表

Project ID: `{project_id(index)}`

Candidate collection object ID: `{row['candidate_collection_object_id']}`

## Required Checks / 必须复核

{required_checks}

## Concrete Questions To Check / 具体待查问题

{concrete_questions}

## Current Evidence Status / 当前证据状态

- Object identity claim: `not_confirmed`
- Formal inscription record: `not_promoted_to_formal_inscription_record`
- Transcription: `not_collected`
- Decipherment: `not_applicable_preprocessing_only`
- Review status: `{REVIEW_STATUS}`

## Caution / 风险提示

{caution}
"""


def build_outputs(root: Path) -> dict[str, dict[str, object]]:
    asset_by_related, technical_by_asset, visual_by_asset = load_assets(root)
    outputs: dict[str, dict[str, object]] = {}
    for index, (source_path, _provider_key, external_prefix, source_row_index, row) in enumerate(
        load_object_rows(root),
        start=1,
    ):
        pid = project_id(index)
        primary_ref = primary_external_ref(row, external_prefix)
        relative_dir = object_dir(index, row, external_prefix)
        asset_row = asset_by_related.get(row["candidate_collection_object_id"])
        technical_row = technical_by_asset.get(asset_row["asset_id"]) if asset_row else None
        visual_profile_row = visual_by_asset.get(asset_row["asset_id"]) if asset_row else None
        src_row = source_index_row(index, source_path, source_row_index, row)
        vis_row = visual_index_row(index, row, asset_row, technical_row, visual_profile_row)
        metadata = selected_metadata(row)
        outputs[pid] = {
            "object_dir": root / relative_dir,
            "relative_object_dir": relative_dir,
            "readme_text": readme_text(index, row, metadata, vis_row),
            "packet": packet_payload(index, relative_dir, row, primary_ref, src_row, vis_row),
            "source_rows": [src_row],
            "visual_rows": [vis_row],
            "gallery_text": gallery_text(index, row, vis_row),
            "review_sheet_text": review_sheet_text(index, row),
            "dossier_text": collection_dossier_text(
                index,
                row,
                metadata,
                src_row,
                vis_row,
            ),
            "dossier_index": collection_dossier_index_payload(
                index,
                relative_dir,
                row,
                src_row,
                vis_row,
            ),
            "manifest_row": {
                "project_id": pid,
                "candidate_collection_object_id": row["candidate_collection_object_id"],
                "candidate_directory": relative_dir.as_posix(),
                "packet_path": (relative_dir / "01_collection-object-packet.json").as_posix(),
                "source_index_path": (relative_dir / "02_collection-source-index.csv").as_posix(),
                "visual_index_path": (relative_dir / "03_visual-asset-index.csv").as_posix(),
                "gallery_path": (relative_dir / "04_visual-gallery.md").as_posix(),
                "human_review_sheet_path": (relative_dir / "05_human-review-sheet.md").as_posix(),
                "human_collection_dossier_path": (relative_dir / "06_human-collection-dossier.md").as_posix(),
                "collection_dossier_index_path": (relative_dir / "07_collection-dossier-index.json").as_posix(),
                "source_id": row["source_id"],
                "rights_status": row["rights_status"],
                "visual_entry_status": vis_row["visual_entry_type"],
                "review_status": REVIEW_STATUS,
                "updated_at": UPDATED_AT,
            },
            "map_row": {
                "project_id": pid,
                "record_type": RECORD_TYPE,
                "canonical_path": relative_dir.as_posix(),
                "primary_external_ref_id": primary_ref,
                "all_external_ref_ids": ";".join(
                    value
                    for value in [
                        row["candidate_collection_object_id"],
                        primary_ref,
                        row.get("source_collection_item_id", ""),
                        row.get("accession_number", ""),
                    ]
                    if value
                ),
                "source_ids": row["source_id"],
                "rights_status": row["rights_status"],
                "review_status": REVIEW_STATUS,
                "updated_at": UPDATED_AT,
            },
        }
    return outputs


def write_outputs(root: Path, outputs: dict[str, dict[str, object]]) -> None:
    manifest_rows: list[dict[str, str]] = []
    map_rows: list[dict[str, str]] = []
    for output in outputs.values():
        directory = output["object_dir"]
        assert isinstance(directory, Path)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "README.md").write_text(str(output["readme_text"]), encoding="utf-8", newline="\n")
        (directory / "01_collection-object-packet.json").write_text(
            json.dumps(output["packet"], ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        write_csv(directory / "02_collection-source-index.csv", output["source_rows"], SOURCE_INDEX_FIELDS)  # type: ignore[arg-type]
        write_csv(directory / "03_visual-asset-index.csv", output["visual_rows"], VISUAL_INDEX_FIELDS)  # type: ignore[arg-type]
        (directory / "04_visual-gallery.md").write_text(str(output["gallery_text"]), encoding="utf-8", newline="\n")
        (directory / "05_human-review-sheet.md").write_text(
            str(output["review_sheet_text"]),
            encoding="utf-8",
            newline="\n",
        )
        (directory / "06_human-collection-dossier.md").write_text(
            str(output["dossier_text"]),
            encoding="utf-8",
            newline="\n",
        )
        (directory / "07_collection-dossier-index.json").write_text(
            json.dumps(output["dossier_index"], ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        manifest_rows.append(output["manifest_row"])  # type: ignore[arg-type]
        map_rows.append(output["map_row"])  # type: ignore[arg-type]
    write_csv(root / OBJECT_ROOT / "000_collection-object-candidate-manifest.csv", manifest_rows, MANIFEST_FIELDS)
    write_csv(root / OBJECT_ID_MAP, map_rows, MAP_FIELDS)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args(argv)
    root = args.root.resolve()
    outputs = build_outputs(root)
    write_outputs(root, outputs)
    print(f"collection_object_candidate_count={len(outputs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
