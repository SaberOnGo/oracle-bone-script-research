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
SOURCE_OBJECT_ROOT = Path(
    "corpus/006_research-sources-and-bibliography/001_source-objects"
)
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
    (
        REGISTER_ROOT / "006_cambridge-cul52-oracle-bone-object-staging.csv",
        "cambridge",
        "cam-cul",
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
    "collection_provenance_evidence_dossier_path",
    "collection_provenance_evidence_index_path",
    "collection_provenance_fact_matrix_path",
    "collection_provenance_fact_matrix_index_path",
    "archaeological_context_review_path",
    "archaeological_context_index_path",
    "human_research_readiness_review_path",
    "human_research_readiness_index_path",
    "preformal_research_start_check_path",
    "preformal_research_start_index_path",
    "material_image_inspection_note_path",
    "source_id",
    "rights_status",
    "visual_entry_status",
    "review_status",
    "updated_at",
]


MATERIAL_IMAGE_OBSERVATIONS = {
    "si-nmaa-obj-00001": {
        "en": [
            "The local photograph shows one flat, broken bone fragment in a "
            "near-edge view.",
            "A centimetre scale is visible below the fragment in this single "
            "photograph.",
            "No inscription-bearing surface is legible in this view; this does "
            "not establish that the object lacks an inscription.",
        ],
        "zh": [
            "本地照片呈现一块扁平、破损的骨片，拍摄角度接近边缘。",
            "这张单幅照片下方可见厘米比例尺。",
            "此视角未见可辨识的载辞表面；这不等于该器物没有卜辞。",
        ],
    },
    "met-obj-00001": {
        "en": [
            "The local photograph shows one long, narrow bone object against a "
            "plain background.",
            "Incised marks are visible in several areas along the photographed "
            "surface.",
            "The local file supplies one view only: it does not supply the "
            "reverse, a plate reference, or a transcription.",
        ],
        "zh": [
            "本地照片呈现一件狭长骨器，背景为单色。",
            "照片所示表面沿长度方向可见多处刻划痕迹。",
            "本地文件只提供单一视角；未提供背面、图版号或释文。",
        ],
    },
    "met-obj-00002": {
        "en": [
            "The local photograph shows an irregular bone fragment with broken "
            "edges.",
            "Dark incised marks are visible near several edges of the photographed "
            "surface.",
            "The image records one surface only; it does not establish mark order, "
            "a plate reference, or a transcription.",
        ],
        "zh": [
            "本地照片呈现一块边缘残缺、不规则的骨片。",
            "照片所示表面的若干边缘附近可见深色刻划痕迹。",
            "图像只记录一个表面，不能据此确定刻划顺序、图版号或释文。",
        ],
    },
}


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


def load_source_routes(
    root: Path,
) -> tuple[dict[tuple[str, str], dict[str, str]], dict[tuple[str, str], str]]:
    """Load exact source access rows for object-local provenance review."""

    route_rows: dict[tuple[str, str], dict[str, str]] = {}
    route_paths: dict[tuple[str, str], str] = {}
    source_root = root / SOURCE_OBJECT_ROOT
    for route_path in sorted(source_root.glob("*_source-object/02_download-route-index.csv")):
        for row in read_csv_rows(route_path):
            key = (row.get("source_id", ""), row.get("download_id", ""))
            if not all(key):
                continue
            route_rows[key] = row
            route_paths[key] = route_path.relative_to(root).as_posix()
    return route_rows, route_paths


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
        "transcription_status": "needs_source_page_transcription_review_route",
        "decipherment_status": "not_applicable_preprocessing_only",
        "project_import_status": row["project_import_status"],
        "rights_status": row["rights_status"],
        "review_status": REVIEW_STATUS,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def metadata_lines(metadata: dict[str, str]) -> str:
    lines: list[str] = []
    for key, value in metadata.items():
        lines.append(
            textwrap.fill(
                f"- {key}: `{value}`",
                width=MAX_HUMAN_LINE_LENGTH,
                subsequent_indent="  ",
                break_long_words=True,
                break_on_hyphens=False,
            )
        )
    return "\n".join(lines)


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
        image_note = (
            "External thumbnail URL metadata only.\n\n"
            "See `thumbnail_url` in Object Metadata."
        )

    english_intro = wrapped_paragraph(
        "This directory is the object-local research entrance for one museum "
        "or collection object candidate. Human-readable notes, visual routes, "
        "review prompts, and provenance dossiers are the primary materials. "
        "Structured support files only serve the human collection dossier, "
        "source tracing, comparison, and review."
    )
    chinese_intro = "\n".join(
        [
            "本目录是一个馆藏或出土相关对象候选的对象内研究入口。",
            "人类可读说明、图像入口、复核提示和出处档案是主体资料。",
            "结构化辅助文件只服务人类馆藏档案、来源追溯、比较和复核。",
        ]
    )
    boundary_entries = "\n".join(
        [
            wrapped_bullet("This is not a confirmed inscription identity."),
            wrapped_bullet(
                "This is not a transcription, formal reading, component "
                "analysis, or decipherment conclusion."
            ),
            wrapped_bullet(
                "Object labels and image links are source metadata for review only."
            ),
            "- 本对象不是已确认的卜辞身份，不是释文、正式释读、构件分析或"
            "\n  破译结论；馆藏标签和图像链接只作为待复核来源 metadata。",
        ]
    )
    file_entries = "\n".join(
        [
            wrapped_bullet(
                "`04_visual-gallery.md`: human-facing image or thumbnail route sheet."
            ),
            wrapped_bullet("`05_human-review-sheet.md`: human review checklist."),
            wrapped_bullet(
                "`06_human-collection-dossier.md`: human collection object dossier."
            ),
            wrapped_bullet(
                "`08_collection-provenance-evidence-dossier.md`: human source "
                "evidence dossier."
            ),
            wrapped_bullet(
                "`10_collection-provenance-fact-matrix.md`: human provenance "
                "fact matrix."
            ),
            wrapped_bullet(
                "`12_archaeological-context-review.md`: human archaeological "
                "context review sheet."
            ),
            wrapped_bullet(
                "`14_human-research-readiness-review.md`: human pre-research "
                "readiness and missing-evidence review."
            ),
            wrapped_bullet(
                "`16_preformal-research-start-check.md`: human opening "
                "check before formal research starts."
            ),
            "\n## Structured Support Files / 结构化辅助文件\n",
            wrapped_bullet(
                "`01_collection-object-packet.json`: structured candidate "
                "support packet."
            ),
            wrapped_bullet(
                "`02_collection-source-index.csv`: source, download, rights, "
                "and route support table."
            ),
            wrapped_bullet(
                "`03_visual-asset-index.csv`: committed asset, thumbnail URL, "
                "or missing-image status."
            ),
            wrapped_bullet(
                "`07_collection-dossier-index.json`: structured dossier support index."
            ),
            wrapped_bullet(
                "`09_collection-provenance-evidence-index.json`: structured "
                "evidence index."
            ),
            wrapped_bullet(
                "`11_collection-provenance-fact-matrix-index.json`: structured "
                "fact index."
            ),
            wrapped_bullet(
                "`13_archaeological-context-index.json`: structured support "
                "index for archaeological context review."
            ),
            wrapped_bullet(
                "`15_human-research-readiness-index.json`: structured support "
                "index for the human readiness review."
            ),
            wrapped_bullet(
                "`17_preformal-research-start-index.json`: structured support "
                "index for the preformal start check."
            ),
        ]
    )
    if asset_path:
        file_entries = file_entries.replace(
            "\n## Structured Support Files / \u7ed3\u6784\u5316\u8f85\u52a9\u6587\u4ef6\n",
            "\n"
            + wrapped_bullet(
                "`18_material-image-inspection-note.md`: bounded observations "
                "from the local source-linked image."
            )
            + "\n\n## Structured Support Files / \u7ed3\u6784\u5316\u8f85\u52a9\u6587\u4ef6\n",
        )
    status_note = wrapped_paragraph(
        f"Current status: `{REVIEW_STATUS}`. Reviewers must verify source "
        "pages, rights status, object labels, image provenance, and inscription "
        "context before promotion."
    )

    return f"""# {project_id(index)} collection object candidate

English:
{english_intro}

简体中文：
{chinese_intro}

## Boundary / 边界

{boundary_entries}

## Visual Entrance / 图像入口

{image_note}

## Local Files / 本目录文件

{file_entries}

## Object Metadata / 对象 metadata

{metadata_lines(metadata)}

## Review Status / 复核状态

{status_note}
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
        "Which 03_visual-asset-index.csv row records local or external image status?",
        "\u54ea\u4e00\u884c 03_visual-asset-index.csv \u8bb0\u5f55"
        "\u672c\u5730\u6216\u5916\u90e8\u56fe\u50cf\u72b6\u6001\uff1f",
        "Which 02_collection-source-index.csv row records catalog and rights route?",
        "\u54ea\u4e00\u884c 02_collection-source-index.csv \u8bb0\u5f55"
        "\u8457\u5f55\u548c\u6743\u5229\u8def\u7ebf\uff1f",
        "Which findspot, period, batch, or plate provenance needs checking?",
        "\u9700\u8981\u6838\u5bf9\u54ea\u4e9b\u51fa\u571f\u5730\u3001"
        "\u65f6\u671f\u3001\u6279\u6b21\u6216\u56fe\u7248\u51fa\u5904\uff1f",
        "Which inscription, glyph, or oracle character route is only a candidate?",
        "\u54ea\u4e9b\u535c\u8f9e\u3001\u5b57\u5f62\u6216"
        "\u7532\u9aa8\u5355\u5b57\u8def\u7ebf\u4ecd\u53ea\u662f\u5019\u9009\uff1f",
        "Which source, checksum, rights status, or risk note must be reviewed?",
        "\u8fd8\u8981\u590d\u6838\u54ea\u4e9b\u6765\u6e90\u3001checksum"
        "\u3001\u6743\u5229\u72b6\u6001\u6216\u98ce\u9669\u63d0\u793a\uff1f",
        "Record the missing route type before any object identity claim.",
        "\u4efb\u4f55\u5bf9\u8c61\u8eab\u4efd\u7ed3\u8bba\u524d\uff0c"
        "\u8bb0\u5f55\u7f3a\u53e3\u5c5e\u4e8e\u54ea\u7c7b\u8def\u7ebf\u3002",
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
        "- batch_context: pending source-page or catalog batch check",
        "- plate_or_catalog_context: pending source-page or catalog plate check",
        "",
        (
            "## Inscription And Character Links / "
            "\u535c\u8f9e\u4e0e\u7532\u9aa8\u5355\u5b57\u5173\u8054"
        ),
        "",
        "- inscription_identity_claim: `not_confirmed`",
        "- transcription_status: pending source-page transcription check",
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
            (relative_dir / "10_collection-provenance-fact-matrix.md").as_posix(),
            (relative_dir / "12_archaeological-context-review.md").as_posix(),
        ],
        "ai_support_files": [
            (relative_dir / "01_collection-object-packet.json").as_posix(),
            (relative_dir / "02_collection-source-index.csv").as_posix(),
            (relative_dir / "03_visual-asset-index.csv").as_posix(),
            (relative_dir / "07_collection-dossier-index.json").as_posix(),
            (relative_dir / "11_collection-provenance-fact-matrix-index.json").as_posix(),
            (relative_dir / "13_archaeological-context-index.json").as_posix(),
        ],
        "source_route_files": [
            source_row["source_file_path"],
            (relative_dir / "02_collection-source-index.csv").as_posix(),
            (relative_dir / "03_visual-asset-index.csv").as_posix(),
            (relative_dir / "04_visual-gallery.md").as_posix(),
            (relative_dir / "06_human-collection-dossier.md").as_posix(),
            (relative_dir / "12_archaeological-context-review.md").as_posix(),
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


def collection_provenance_evidence_dossier_text(
    index: int,
    row: dict[str, str],
    metadata: dict[str, str],
    source_row: dict[str, str],
    visual_row: dict[str, str],
    source_route: dict[str, str],
    source_route_path: str,
) -> str:
    pid = project_id(index)
    intro = wrapped_paragraph(
        "This dossier records the provenance evidence routes that must be "
        "opened before a museum or collection object candidate can be used "
        "for comparison, citation, or later formal research."
    )
    intro_zh = wrapped_paragraph(
        "本档案记录馆藏或出土相关对象候选进入比较、引用或后续正式研究前"
        "必须打开复核的来源证据路线。这里不确认对象身份、不确认卜辞身份，"
        "也不作释读结论。"
    )
    boundary = wrapped_paragraph(
        "All rows here are candidate evidence only. They preserve source, "
        "rights, visual, catalog, and missing-context routes for human review; "
        "they are not a decipherment conclusion."
    )
    source_table = "\n".join(
        [
            "| Evidence field / 证据字段 | Route or value / 路线或取值 |",
            "| --- | --- |",
            f"| source_id | `{source_row['source_id']}` |",
            f"| evidence_download_id | `{source_row['evidence_download_id']}` |",
            f"| source_file_path | `{source_row['source_file_path']}` |",
            f"| source_row_id | `{source_row['source_row_id']}` |",
            f"| object_page_url | `{source_row.get('object_page_url', '')}` |",
            f"| rights_status | `{source_row['rights_status']}` |",
            f"| review_status | `{REVIEW_STATUS}` |",
            f"| access_route_index | `{source_route_path or 'pending source-object route index'}` |",
            f"| download_status | `{source_route.get('download_status', 'pending')}` |",
            f"| http_status | `{source_route.get('http_status', 'pending')}` |",
            f"| accessed_file_size_bytes | `{source_route.get('file_size_bytes', 'pending')}` |",
            f"| checksum_sha256 | `{source_route.get('checksum_sha256', 'pending')}` |",
            f"| local_temp_path | `{source_route.get('local_temp_path', 'pending')}` |",
            f"| route_review_status | `{source_route.get('review_status', 'pending')}` |",
        ]
    )
    visual_table = "\n".join(
        [
            "| Visual field / 图像字段 | Route or value / 路线或取值 |",
            "| --- | --- |",
            f"| visual_entry_type | `{visual_row.get('visual_entry_type', '')}` |",
            f"| asset_id | `{visual_row.get('asset_id', '')}` |",
            f"| asset_path | `{visual_row.get('asset_path', '')}` |",
            f"| thumbnail_url | `{visual_row.get('thumbnail_url', '')}` |",
            f"| source_image_url | `{visual_row.get('source_image_url', '')}` |",
        ]
    )
    catalog_table_rows = [
        "| Catalog field / 著录字段 | Source value / 来源取值 |",
        "| --- | --- |",
    ]
    for key in [
        "collection_name",
        "source_collection_item_id",
        "object_title_en",
        "catalog_reference_text",
        "accession_number",
        "historical_period",
        "object_date",
        "provenience",
        "geography",
        "repository",
    ]:
        catalog_table_rows.append(f"| `{key}` | `{metadata.get(key, '')}` |")
    questions = "\n".join(
        wrapped_bullet(text)
        for text in [
            "Which source page or catalog row proves the object label route?",
            "哪一个来源页面或著录行可以证明对象标签路线？",
            (
                "Which download log row records access time, checksum, size, "
                "and rights status?"
            ),
            "哪一条下载记录写明访问时间、checksum、大小和权利状态？",
            "Which findspot, period, batch, and plate facts still lack evidence?",
            "哪些出土地、时期、批次和图版事实仍缺少证据？",
            "Which inscription or character links are only candidate routes?",
            "哪些卜辞或单字关联仍只是候选路线？",
            "Which rights or reuse risks must be checked before public use?",
            "公开使用前还要复核哪些权利或复用风险？",
        ]
    )
    lines = [
        (
            "# Collection Provenance Evidence Dossier / "
            f"馆藏来源证据档案: {pid}"
        ),
        "",
        "English:",
        intro,
        "",
        "简体中文：",
        intro_zh,
        "",
        "## Catalog Page And Source Row / 著录页与来源行",
        "",
        source_table,
        "",
        "## Rights Checksum And Risk Route / 权利、checksum 与风险路线",
        "",
        "- rights_status is copied from the registered source row.",
        "- checksum and file size must be checked in the source log or manifest.",
        "- risk notes must be reviewed before reuse or publication.",
        "- 权利状态来自登记来源行；checksum 与大小仍需打开记录复核。",
        "",
        "## Visual Asset Or Thumbnail Evidence / 图像资产或缩略图证据",
        "",
        visual_table,
        "",
        "## Findspot Period Batch Plate Evidence / 出土地、时期、批次与图版证据",
        "",
        "\n".join(catalog_table_rows),
        "",
        "## Inscription And Character Context To Verify / 卜辞与单字语境待复核",
        "",
        "- inscription_identity_claim: `not_confirmed`",
        "- transcription_status: pending source-page transcription check",
        "- oracle_character_route_status: candidate route only",
        "- plate_context_status: needs catalog or source-page checking",
        "",
        "## Component Clue Review / 构件线索待复核",
        "",
        "- component status: open linked character or plate context first.",
        "- no component assignment is made in this provenance dossier.",
        "- 构件、组成和字形线索只能作为下一步待查入口。",
        "",
        "## Scholarship And Dispute Route / 书目与争议路线",
        "",
        "- scholarship route: open bibliography before citing this object.",
        "- dispute status: record proposer and disagreement before promotion.",
        "- 学者、提出者、论文、书目和争议仍需来源页复核。",
        "",
        "## Variant And Relationship Route / 异体与关系路线",
        "",
        "- variant and related-character links remain candidate routes.",
        "- later bronze, seal, and modern forms are not confirmed here.",
        "- 异体、近形、今字和同构件关系均不得写成结论。",
        "",
        "## Concrete Missing Evidence Questions / 具体缺失证据问题",
        "",
        questions,
        "",
        "## Review Boundary / 复核边界",
        "",
        boundary,
        "- candidate evidence only",
        "- not a confirmed collection object identity",
        "- not a confirmed inscription identity",
        "- not a formal reading",
        "- not a decipherment conclusion",
    ]
    return "\n".join(lines) + "\n"


def collection_provenance_evidence_index_payload(
    index: int,
    relative_dir: Path,
    row: dict[str, str],
    source_row: dict[str, str],
    visual_row: dict[str, str],
    source_route: dict[str, str],
    source_route_path: str,
) -> dict[str, object]:
    return {
        "project_id": project_id(index),
        "record_type": "collection_object_candidate_provenance_evidence_index",
        "candidate_collection_object_id": row["candidate_collection_object_id"],
        "human_readable_files": [
            (relative_dir / "08_collection-provenance-evidence-dossier.md").as_posix(),
            (relative_dir / "04_visual-gallery.md").as_posix(),
            (relative_dir / "05_human-review-sheet.md").as_posix(),
            (relative_dir / "06_human-collection-dossier.md").as_posix(),
            (relative_dir / "12_archaeological-context-review.md").as_posix(),
        ],
        "source_evidence_files": [
            source_row["source_file_path"],
            source_route_path,
            (relative_dir / "02_collection-source-index.csv").as_posix(),
            (relative_dir / "03_visual-asset-index.csv").as_posix(),
            (relative_dir / "04_visual-gallery.md").as_posix(),
        ],
        "ai_support_files": [
            (relative_dir / "01_collection-object-packet.json").as_posix(),
            (relative_dir / "07_collection-dossier-index.json").as_posix(),
            (relative_dir / "09_collection-provenance-evidence-index.json").as_posix(),
            (relative_dir / "13_archaeological-context-index.json").as_posix(),
        ],
        "evidence_status": {
            "catalog_page": "source_row_recorded_needs_human_review",
            "download_log": (
                f"{source_route.get('download_status', 'pending')}; "
                f"size={source_route.get('file_size_bytes', 'pending')}; "
                f"checksum={source_route.get('checksum_sha256', 'pending')}"
            ),
            "visual_asset": visual_row.get("visual_entry_type", ""),
            "findspot_period_batch_plate": "candidate_metadata_needs_review",
            "inscription_character_context": "not_confirmed_candidate_route_only",
        },
        "missing_evidence_questions": [
            "which source page or catalog row proves the object label route",
            "which download log row records access time, checksum, size, and rights status",
            "which findspot, period, batch, and plate facts still lack evidence",
            "which inscription or character links are only candidate routes",
            "which rights or reuse risks must be checked before public use",
        ],
        "claim_boundary": (
            "candidate evidence only; no confirmed collection object identity; "
            "no confirmed inscription identity; no transcription; no formal "
            "reading; no decipherment conclusion"
        ),
        "rights_status": source_row["rights_status"],
        "review_status": REVIEW_STATUS,
        "updated_at": UPDATED_AT,
    }


def collection_provenance_fact_rows(
    row: dict[str, str],
    metadata: dict[str, str],
    source_row: dict[str, str],
    visual_row: dict[str, str],
) -> list[dict[str, str]]:
    catalog_route = (
        metadata.get("accession_number")
        or metadata.get("source_collection_item_id")
        or row.get("source_collection_item_id", "")
        or "pending source-page review"
    )
    visual_route = visual_row.get("visual_entry_type", "pending visual review")
    findspot = metadata.get("provenience") or metadata.get("geography")
    period = metadata.get("historical_period") or metadata.get("object_date")
    return [
        {
            "fact": "Collection object / 馆藏对象",
            "status": "candidate object route; identity still needs review",
            "evidence": "01_collection-object-packet.json; 06_human-collection-dossier.md",
        },
        {
            "fact": "Catalog or accession route / 著录或登记路线",
            "status": f"{catalog_route}; source-page route only",
            "evidence": "02_collection-source-index.csv; 06_human-collection-dossier.md",
        },
        {
            "fact": "Image or visual route / 图像或视觉路线",
            "status": f"{visual_route}; open gallery before visual use",
            "evidence": "03_visual-asset-index.csv; 04_visual-gallery.md",
        },
        {
            "fact": "Findspot or provenience / 出土地或来源地",
            "status": findspot or "pending findspot or provenience review",
            "evidence": (
                "06_human-collection-dossier.md; "
                "08_collection-provenance-evidence-dossier.md"
            ),
        },
        {
            "fact": "Period or date / 时期或年代",
            "status": period or "pending period or date source review",
            "evidence": (
                "06_human-collection-dossier.md; "
                "08_collection-provenance-evidence-dossier.md"
            ),
        },
        {
            "fact": "Batch or excavation context / 批次或发掘语境",
            "status": "pending batch, pit, excavation, or plate context review",
            "evidence": "08_collection-provenance-evidence-dossier.md",
        },
        {
            "fact": "Inscription and character links / 卜辞与单字关联",
            "status": "candidate route only; no inscription identity claim",
            "evidence": (
                "06_human-collection-dossier.md; "
                "08_collection-provenance-evidence-dossier.md"
            ),
        },
        {
            "fact": "Source and rights trail / 来源与权利链",
            "status": f"{source_row['source_id']}; rights {source_row['rights_status']}",
            "evidence": (
                "02_collection-source-index.csv; "
                "09_collection-provenance-evidence-index.json"
            ),
        },
        {
            "fact": "Risk note / 风险提示",
            "status": "rights and reuse risk require human review before public use",
            "evidence": "01_collection-object-packet.json; 03_visual-asset-index.csv",
        },
        {
            "fact": "Review status / 复核状态",
            "status": REVIEW_STATUS,
            "evidence": (
                "05_human-review-sheet.md; "
                "09_collection-provenance-evidence-index.json"
            ),
        },
    ]


def collection_provenance_fact_matrix_text(
    index: int,
    row: dict[str, str],
    fact_rows: list[dict[str, str]],
) -> str:
    pid = project_id(index)
    intro = wrapped_paragraph(
        "This matrix gives a compact human review order for the collection "
        "object candidate. It points from each fact to the local evidence file "
        "that must be opened before any comparison, citation, or later "
        "research use."
    )
    intro_zh = wrapped_paragraph(
        "\u672c\u77e9\u9635\u4e3a\u9986\u85cf\u5bf9\u8c61\u5019\u9009"
        "\u63d0\u4f9b\u7b80\u660e\u7684\u4eba\u5de5\u590d\u6838\u987a\u5e8f\uff1b"
        "\u6bcf\u4e2a\u4e8b\u5b9e\u90fd\u6307\u5411\u5fc5\u987b\u5148"
        "\u6253\u5f00\u7684\u672c\u5730\u8bc1\u636e\u6587\u4ef6\u3002"
    )
    rows = "\n".join(
        f"| {item['fact']} | {item['status']} | {item['evidence']} |"
        for item in fact_rows
    )
    review_questions = "\n".join(
        wrapped_bullet(text)
        for text in [
            "Open the catalog or accession source before trusting the label.",
            "Open the visual index and gallery before using the object image.",
            "Check findspot, period, batch, and plate evidence in the dossier.",
            "Separate candidate inscription or character links from confirmed facts.",
            "Review source, checksum, rights, and risk notes before public reuse.",
            "Record the precise missing evidence route for the next researcher.",
            (
                "\u5148\u6838\u5bf9\u8457\u5f55\u6216\u767b\u8bb0\u6765\u6e90\uff0c"
                "\u518d\u4fe1\u4efb\u5bf9\u8c61\u6807\u7b7e\u3002"
            ),
            (
                "\u4f7f\u7528\u56fe\u50cf\u524d\uff0c\u5148\u6253\u5f00"
                "\u56fe\u50cf\u7d22\u5f15\u548c\u56fe\u50cf\u5165\u53e3\u3002"
            ),
            (
                "\u628a\u5019\u9009\u535c\u8f9e\u6216\u5355\u5b57\u5173\u8054"
                "\u4e0e\u5df2\u786e\u8ba4\u4e8b\u5b9e\u5206\u5f00\u8bb0\u5f55\u3002"
            ),
        ]
    )
    lines = [
        (
            "# Collection Provenance Fact Matrix / "
            f"\u9986\u85cf\u6765\u6e90\u4e8b\u5b9e\u77e9\u9635: {pid}"
        ),
        "",
        "English:",
        intro,
        "",
        "\u7b80\u4f53\u4e2d\u6587\uff1a",
        intro_zh,
        "",
        "## Human Review Order / \u4eba\u5de5\u590d\u6838\u987a\u5e8f",
        "",
        "- Start with `10_collection-provenance-fact-matrix.md`.",
        "- Then open `08_collection-provenance-evidence-dossier.md`.",
        "- Use `02_collection-source-index.csv` for source and rights routes.",
        "- Use `03_visual-asset-index.csv` and `04_visual-gallery.md` for images.",
        "- Use `11_collection-provenance-fact-matrix-index.json` only as support.",
        "",
        (
            "## Collection Object Provenance Fact Matrix / "
            "\u9986\u85cf\u5bf9\u8c61\u6765\u6e90\u4e8b\u5b9e\u77e9\u9635"
        ),
        "",
        "| Fact / 项目 | Current status / 当前状态 | Local evidence to open / 需打开的本地证据 |",
        "| --- | --- | --- |",
        rows,
        "",
        "## Concrete Review Questions / \u5177\u4f53\u590d\u6838\u95ee\u9898",
        "",
        review_questions,
        "",
        "## Review Boundary / \u590d\u6838\u8fb9\u754c",
        "",
        "- not a confirmed collection object identity",
        "- not a confirmed inscription identity",
        "- not a transcription",
        "- not a formal reading",
        "- not a decipherment conclusion",
        f"- candidate_collection_object_id: `{row['candidate_collection_object_id']}`",
    ]
    return "\n".join(lines) + "\n"


def collection_provenance_fact_matrix_index_payload(
    index: int,
    relative_dir: Path,
    row: dict[str, str],
    source_row: dict[str, str],
    visual_row: dict[str, str],
    fact_rows: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "project_id": project_id(index),
        "record_type": "collection_provenance_fact_matrix_index",
        "candidate_collection_object_id": row["candidate_collection_object_id"],
        "fact_count": len(fact_rows),
        "facts": fact_rows,
        "human_readable_files": [
            (relative_dir / "README.md").as_posix(),
            (relative_dir / "04_visual-gallery.md").as_posix(),
            (relative_dir / "05_human-review-sheet.md").as_posix(),
            (relative_dir / "06_human-collection-dossier.md").as_posix(),
            (relative_dir / "08_collection-provenance-evidence-dossier.md").as_posix(),
            (relative_dir / "10_collection-provenance-fact-matrix.md").as_posix(),
            (relative_dir / "12_archaeological-context-review.md").as_posix(),
        ],
        "ai_support_files": [
            (relative_dir / "01_collection-object-packet.json").as_posix(),
            (relative_dir / "02_collection-source-index.csv").as_posix(),
            (relative_dir / "03_visual-asset-index.csv").as_posix(),
            (relative_dir / "07_collection-dossier-index.json").as_posix(),
            (relative_dir / "09_collection-provenance-evidence-index.json").as_posix(),
            (relative_dir / "11_collection-provenance-fact-matrix-index.json").as_posix(),
            (relative_dir / "13_archaeological-context-index.json").as_posix(),
        ],
        "source_id": source_row["source_id"],
        "rights_status": source_row["rights_status"],
        "visual_entry_type": visual_row.get("visual_entry_type", ""),
        "claim_boundary": [
            "no confirmed collection object identity",
            "no confirmed inscription identity",
            "no transcription",
            "no formal reading",
            "no decipherment conclusion",
        ],
        "review_status": REVIEW_STATUS,
        "updated_at": UPDATED_AT,
    }


def archaeological_context_review_text(
    index: int,
    row: dict[str, str],
    metadata: dict[str, str],
    source_row: dict[str, str],
    visual_row: dict[str, str],
) -> str:
    pid = project_id(index)
    institution = (
        metadata.get("repository")
        or metadata.get("collection_name")
        or metadata.get("provider")
        or "pending institution review"
    )
    accession = row.get("accession_number", "") or "pending source review"
    source_item = row.get("source_collection_item_id", "")
    catalog = (
        metadata.get("catalog_reference_text")
        or metadata.get("object_title_en")
        or "pending catalog-page review"
    )
    provenience = (
        metadata.get("provenience")
        or metadata.get("geography")
        or "pending findspot review"
    )
    period = (
        metadata.get("historical_period")
        or metadata.get("object_date")
        or "pending period review"
    )
    intro_en = wrapped_paragraph(
        "This review sheet keeps archaeological context questions beside the "
        "collection object candidate. A human reviewer must verify institution, "
        "catalog record, findspot, period, batch, plate, image, and inscription "
        "routes before the object can support later research."
    )
    intro_zh = "\n".join(
        [
            "\u672c\u8868\u628a\u8003\u53e4\u8bed\u5883\u5f85\u6838\u95ee\u9898",
            "\u653e\u5728\u9986\u85cf\u5bf9\u8c61\u5019\u9009\u76ee\u5f55\u5185\u3002",
            "\u4eba\u7c7b\u590d\u6838\u8005\u9700\u5148\u6838\u5bf9\u673a\u6784\u3001\u8457\u5f55\u3001",
            "\u51fa\u571f\u5730\u3001\u65f6\u671f\u3001\u6279\u6b21\u3001\u56fe\u7248\u3001",
            "\u56fe\u50cf\u548c\u535c\u8f9e\u8def\u7ebf\u3002",
        ]
    )
    rows = [
        ("Institution", institution, "02_collection-source-index.csv"),
        ("Catalog or accession", accession, "02_collection-source-index.csv"),
        (
            "Source item",
            source_item or "pending source row review",
            "01_collection-object-packet.json",
        ),
        ("Catalog description", catalog, "01_collection-object-packet.json"),
        (
            "Image route",
            visual_row.get("visual_entry_type", ""),
            "03_visual-asset-index.csv",
        ),
        (
            "Findspot or provenience",
            provenience,
            "08_collection-provenance-evidence-dossier.md",
        ),
        (
            "Period or date",
            period,
            "08_collection-provenance-evidence-dossier.md",
        ),
        (
            "Batch or pit context",
            "pending excavation batch review",
            "10_collection-provenance-fact-matrix.md",
        ),
        (
            "Plate or publication route",
            "pending plate or catalog-page review",
            "06_human-collection-dossier.md",
        ),
        (
            "Inscription route",
            "candidate route only; no identity claim",
            "06_human-collection-dossier.md",
        ),
        (
            "Character route",
            "candidate route only; no reading claim",
            "06_human-collection-dossier.md",
        ),
        ("Rights and risk", source_row["rights_status"], "02_collection-source-index.csv"),
    ]
    table_rows = "\n".join(
        f"| {label} | `{status}` | `{evidence}` |"
        for label, status, evidence in rows
    )
    english_questions = "\n".join(
        wrapped_bullet(text)
        for text in [
            "Which institution page and accession record should be opened first?",
            "Which findspot, period, batch, or pit term is absent from the source?",
            "Which plate or publication route must be checked before citation?",
            "Which inscription or character link is only a candidate route?",
            "Which image route is local, external-only, or unavailable?",
            "Which rights or risk note blocks public reuse?",
        ]
    )
    chinese_questions = "\n".join(
        [
            "- \u5148\u6253\u5f00\u54ea\u4e2a\u673a\u6784\u9875\u548c\u767b\u8bb0\u53f7\uff1f",
            "- \u7f3a\u54ea\u9879\u51fa\u571f\u5730\u3001\u65f6\u671f\u6216\u6279\u6b21\uff1f",
            "- \u54ea\u6761\u56fe\u7248\u6216\u8457\u5f55\u8def\u7ebf\u5f85\u590d\u6838\uff1f",
            "- \u54ea\u4e9b\u535c\u8f9e\u6216\u5355\u5b57\u5173\u8054\u4ecd\u4e3a\u5019\u9009\uff1f",
        ]
    )
    questions = f"{english_questions}\n{chinese_questions}"
    return "\n".join(
        [
            (
                "# Archaeological Context Review / "
                f"\u8003\u53e4\u8bed\u5883\u590d\u6838: {pid}"
            ),
            "",
            "English:",
            intro_en,
            "",
            "\u7b80\u4f53\u4e2d\u6587\uff1a",
            intro_zh,
            "",
            "## Context Fields To Verify / \u5f85\u6838\u8bed\u5883\u9879",
            "",
            "| Context field | Current route or status | Local evidence to open |",
            "| --- | --- | --- |",
            table_rows,
            "",
            "## Concrete Questions To Check / \u5177\u4f53\u5f85\u67e5\u95ee\u9898",
            "",
            questions,
            "",
            "## Review Boundary / \u590d\u6838\u8fb9\u754c",
            "",
            "- collection object identity remains unconfirmed",
            "- inscription identity remains unconfirmed",
            "- no transcription, formal reading, or component analysis is added",
            "- no decipherment conclusion is added",
            f"- candidate_collection_object_id: `{row['candidate_collection_object_id']}`",
        ]
    ) + "\n"


def archaeological_context_index_payload(
    index: int,
    relative_dir: Path,
    row: dict[str, str],
    source_row: dict[str, str],
    visual_row: dict[str, str],
) -> dict[str, object]:
    return {
        "project_id": project_id(index),
        "record_type": "collection_archaeological_context_review_index",
        "candidate_collection_object_id": row["candidate_collection_object_id"],
        "human_readable_files": [
            (relative_dir / "12_archaeological-context-review.md").as_posix(),
            (relative_dir / "06_human-collection-dossier.md").as_posix(),
            (relative_dir / "08_collection-provenance-evidence-dossier.md").as_posix(),
            (relative_dir / "10_collection-provenance-fact-matrix.md").as_posix(),
        ],
        "ai_support_files": [
            (relative_dir / "01_collection-object-packet.json").as_posix(),
            (relative_dir / "02_collection-source-index.csv").as_posix(),
            (relative_dir / "03_visual-asset-index.csv").as_posix(),
            (relative_dir / "13_archaeological-context-index.json").as_posix(),
        ],
        "context_slots": [
            "institution",
            "accession_or_catalog_number",
            "findspot_or_provenience",
            "period_or_date",
            "batch_or_pit_context",
            "plate_or_publication_route",
            "inscription_route",
            "oracle_character_route",
            "image_route",
            "rights_and_risk",
        ],
        "source_id": source_row["source_id"],
        "visual_entry_type": visual_row.get("visual_entry_type", ""),
        "claim_boundary": (
            "human archaeological context review only; no confirmed collection "
            "object identity; no confirmed inscription identity; no "
            "transcription; no reading; no decipherment conclusion"
        ),
        "review_status": REVIEW_STATUS,
        "updated_at": UPDATED_AT,
    }


def human_research_readiness_review_text(
    index: int,
    row: dict[str, str],
    metadata: dict[str, str],
    source_row: dict[str, str],
    visual_row: dict[str, str],
) -> str:
    pid = project_id(index)
    intro_en = wrapped_paragraph(
        "This review records what a human researcher must still open before "
        "using this collection object candidate in formal oracle-bone "
        "research. It gathers source, visual, archaeological, inscription, "
        "character, rights, and dispute checks without promoting any claim."
    )
    intro_zh = wrapped_paragraph(
        "\u672c\u590d\u6838\u6587\u4ef6\u8bb0\u5f55\u6b63\u5f0f"
        "\u7532\u9aa8\u7814\u7a76\u524d\uff0c\u4eba\u7c7b\u7814\u7a76\u8005"
        "\u8fd8\u5fc5\u987b\u6253\u5f00\u54ea\u4e9b\u6765\u6e90\u3001"
        "\u56fe\u50cf\u3001\u8003\u53e4\u8bed\u5883\u3001\u535c\u8f9e"
        "\u3001\u5355\u5b57\u3001\u6743\u5229\u548c\u4e89\u8bae\u8def\u7ebf\u3002"
        "\u5b83\u4e0d\u63d0\u5347\u4efb\u4f55\u8eab\u4efd\u6216\u91ca\u8bfb"
        "\u7ed3\u8bba\u3002"
    )
    source_label = (
        metadata.get("accession_number")
        or metadata.get("source_collection_item_id")
        or row.get("source_collection_item_id", "")
        or "pending source-page review"
    )
    image_status = visual_row.get("visual_entry_type", "pending visual review")
    context_status = metadata.get("provenience") or metadata.get("geography")
    period_status = metadata.get("historical_period") or metadata.get("object_date")
    if not context_status:
        context_status = "pending findspot or provenience source review"
    if not period_status:
        period_status = "pending period or date source review"
    table_rows = "\n".join(
        [
            "| Readiness area | Current route or status | Human file to open |",
            "| --- | --- | --- |",
            f"| Catalog source | `{source_label}` | `02_collection-source-index.csv` |",
            f"| Visual evidence | `{image_status}` | `04_visual-gallery.md` |",
            f"| Findspot route | `{context_status}` | `08_collection-provenance-evidence-dossier.md` |",
            f"| Period route | `{period_status}` | `12_archaeological-context-review.md` |",
            "| Batch or pit route | `pending source-page review` | `12_archaeological-context-review.md` |",
            "| Plate or publication route | `pending catalog-page review` | `06_human-collection-dossier.md` |",
            "| Inscription relation | `candidate route only` | `10_collection-provenance-fact-matrix.md` |",
            "| Character relation | `candidate route only` | `10_collection-provenance-fact-matrix.md` |",
            f"| Rights and risk | `{source_row['rights_status']}` | `02_collection-source-index.csv` |",
            "| Scholarship and dispute route | `pending bibliography review` | `08_collection-provenance-evidence-dossier.md` |",
        ]
    )
    questions = "\n".join(
        wrapped_bullet(text)
        for text in [
            "Which catalog page or accession record proves the object label?",
            "Which committed image, thumbnail URL, or missing visual route is usable?",
            "Which source row records checksum, size, rights status, and risk note?",
            "Which findspot, period, batch, pit, or plate route remains absent?",
            "Which inscription relation is only a candidate route for later review?",
            "Which oracle-character relation is only a candidate route for later review?",
            "Which bibliography, proposer, disagreement, or citation trail is missing?",
            "Which raw image or uncertain-rights item must stay outside regular Git?",
            "\u54ea\u4e2a\u8457\u5f55\u9875\u6216\u767b\u8bb0\u53f7\u8bb0\u5f55"
            "\u80fd\u652f\u6301\u5bf9\u8c61\u6807\u7b7e\uff1f",
            "\u54ea\u6761\u56fe\u50cf\u8def\u7ebf\u53ef\u7528\uff1a"
            "\u5df2\u63d0\u4ea4\u56fe\u50cf\u3001\u7f29\u7565\u56fe URL "
            "\u8fd8\u662f\u7f3a\u56fe\uff1f",
            "\u54ea\u6761\u6765\u6e90\u884c\u8bb0\u5f55 checksum\u3001"
            "\u5927\u5c0f\u3001\u6743\u5229\u72b6\u6001\u548c\u98ce\u9669\uff1f",
            "\u54ea\u9879\u51fa\u571f\u5730\u3001\u65f6\u671f\u3001"
            "\u6279\u6b21\u3001\u5751\u4f4d\u6216\u56fe\u7248\u4ecd\u7f3a\uff1f",
            "\u54ea\u4e9b\u535c\u8f9e\u6216\u5355\u5b57\u5173\u8054"
            "\u4ec5\u662f\u5019\u9009\u8def\u7ebf\uff1f",
            "\u54ea\u4e9b\u4e66\u76ee\u3001\u63d0\u51fa\u8005\u3001"
            "\u4e0d\u540c\u610f\u89c1\u6216\u5f15\u7528\u94fe\u5f85\u67e5\uff1f",
        ]
    )
    boundary = "\n".join(
        [
            "- no confirmed collection object identity",
            "- no confirmed inscription identity",
            "- no transcription or OCR correction is accepted here",
            "- no formal reading, component assignment, or dating claim",
            "- no decipherment conclusion",
            "- \u4e0d\u786e\u8ba4\u9986\u85cf\u5bf9\u8c61\u8eab\u4efd",
            "- \u4e0d\u786e\u8ba4\u535c\u8f9e\u8eab\u4efd\u6216\u91ca\u6587",
            "- \u4e0d\u63a5\u53d7\u91ca\u8bfb\u3001\u6784\u4ef6\u6216\u65ad\u4ee3\u7ed3\u8bba",
        ]
    )
    return "\n".join(
        [
            (
                "# Human Research Readiness Review / "
                f"\u4eba\u7c7b\u7814\u7a76\u51c6\u5907\u5ea6\u590d\u6838: {pid}"
            ),
            "",
            "English:",
            intro_en,
            "",
            "\u7b80\u4f53\u4e2d\u6587\uff1a",
            intro_zh,
            "",
            "## Readiness Routes To Open / \u9700\u6253\u5f00\u7684\u51c6\u5907\u8def\u7ebf",
            "",
            table_rows,
            "",
            "## Concrete Missing Evidence Questions / \u5177\u4f53\u7f3a\u8bc1\u95ee\u9898",
            "",
            questions,
            "",
            "## Research Boundary / \u7814\u7a76\u8fb9\u754c",
            "",
            boundary,
            f"- candidate_collection_object_id: `{row['candidate_collection_object_id']}`",
            f"- review_status: `{REVIEW_STATUS}`",
        ]
    ) + "\n"


def human_research_readiness_index_payload(
    index: int,
    relative_dir: Path,
    row: dict[str, str],
    source_row: dict[str, str],
    visual_row: dict[str, str],
) -> dict[str, object]:
    return {
        "project_id": project_id(index),
        "record_type": "collection_human_research_readiness_index",
        "candidate_collection_object_id": row["candidate_collection_object_id"],
        "human_readable_files": [
            (relative_dir / "14_human-research-readiness-review.md").as_posix(),
            (relative_dir / "06_human-collection-dossier.md").as_posix(),
            (relative_dir / "08_collection-provenance-evidence-dossier.md").as_posix(),
            (relative_dir / "10_collection-provenance-fact-matrix.md").as_posix(),
            (relative_dir / "12_archaeological-context-review.md").as_posix(),
        ],
        "ai_support_files": [
            (relative_dir / "01_collection-object-packet.json").as_posix(),
            (relative_dir / "02_collection-source-index.csv").as_posix(),
            (relative_dir / "03_visual-asset-index.csv").as_posix(),
            (relative_dir / "15_human-research-readiness-index.json").as_posix(),
        ],
        "readiness_slots": [
            "catalog_source",
            "visual_evidence",
            "checksum_size_rights_risk",
            "findspot_period_batch_pit_plate",
            "inscription_relation_candidate_route",
            "oracle_character_relation_candidate_route",
            "bibliography_proposer_dispute_citation",
            "raw_or_uncertain_rights_asset_boundary",
        ],
        "missing_evidence_questions": [
            "which catalog page or accession record proves the object label",
            "which image route is usable before formal research",
            "which source row records checksum size rights status and risk note",
            "which findspot period batch pit or plate route remains absent",
            "which inscription or oracle-character relation is candidate only",
            "which bibliography proposer disagreement or citation trail is missing",
            "which raw image or uncertain-rights item must stay outside regular Git",
        ],
        "source_id": source_row["source_id"],
        "visual_entry_type": visual_row.get("visual_entry_type", ""),
        "rights_status": source_row["rights_status"],
        "claim_boundary": (
            "human readiness review only; no confirmed collection object "
            "identity; no confirmed inscription identity; no transcription; "
            "no reading; no component assignment; no dating claim; no "
            "decipherment conclusion"
        ),
        "review_status": REVIEW_STATUS,
        "updated_at": UPDATED_AT,
    }


def preformal_research_start_check_text(
    index: int,
    row: dict[str, str],
    metadata: dict[str, str],
    source_row: dict[str, str],
    visual_row: dict[str, str],
) -> str:
    pid = project_id(index)
    source_label = (
        metadata.get("accession_number")
        or metadata.get("source_collection_item_id")
        or row.get("source_collection_item_id", "")
        or "pending catalog-page review"
    )
    visual_status = visual_row.get("visual_entry_type", "pending visual review")
    intro_en = wrapped_paragraph(
        "This human check fixes the opening order before formal research "
        "starts. A reviewer first opens the object page, image route, catalog "
        "reference, and source row, then checks archaeological context, "
        "inscription links, character routes, rights, and unresolved disputes."
    )
    intro_zh = wrapped_paragraph(
        "本核查固定正式研究开始前的开包顺序。研究者先看实物和馆藏记录、"
        "图像路线、著录线索和来源行，再核对考古语境、卜辞关联、单字"
        "路线、权利状态和仍待复核的争议。"
    )
    opening_rows = "\n".join(
        [
            "| Order | Open first | What to verify |",
            "| --- | --- | --- |",
            f"| 1 | `02_collection-source-index.csv` | `{source_label}` |",
            f"| 2 | `04_visual-gallery.md` | `{visual_status}` |",
            "| 3 | `06_human-collection-dossier.md` | catalog clues |",
            "| 4 | `12_archaeological-context-review.md` | context gaps |",
            "| 5 | `14_human-research-readiness-review.md` | blockers |",
        ]
    )
    questions = "\n".join(
        wrapped_bullet(text)
        for text in [
            (
                "Which object page, image route, catalog reference, and source "
                "row must be opened first?"
            ),
            "Which findspot, period, batch, pit, or plate route remains pending?",
            "Which inscription or oracle-character relation is candidate only?",
            "Which rights, checksum, size, manifest, or field map is unresolved?",
            "Which bibliography, proposer, disagreement, or citation is missing?",
            "哪一个对象页、图像路线、著录线索和来源行要先打开？",
            "哪一项出土地、时期、批次、坑位或图版路线仍待查？",
            "哪一条卜辞或甲骨单字关联仍只是候选路线？",
            "哪一项权利、checksum、大小、manifest 或字段映射未解决？",
            "哪一项书目、提出者、不同意见或引用链仍缺失？",
        ]
    )
    boundary = "\n".join(
        [
            "- no confirmed collection object identity",
            "- no confirmed inscription identity",
            "- no transcription or OCR correction is accepted here",
            "- no formal reading, component assignment, or dating claim",
            "- no decipherment conclusion",
            "- 不确认馆藏对象身份",
            "- 不确认卜辞身份或释文",
            "- 不接受释读、构件归属或断代结论",
        ]
    )
    return "\n".join(
        [
            (
                "# Preformal Research Start Check / "
                f"正式研究开始前开包核查: {pid}"
            ),
            "",
            "English:",
            intro_en,
            "",
            "简体中文：",
            intro_zh,
            "",
            "## Object Opening Order / 对象开包顺序",
            "",
            opening_rows,
            "",
            "## Concrete Start Questions / 具体开包问题",
            "",
            questions,
            "",
            "## Research Boundary / 研究边界",
            "",
            boundary,
            f"- candidate_collection_object_id: `{row['candidate_collection_object_id']}`",
            f"- source_id: `{source_row['source_id']}`",
            f"- rights_status: `{source_row['rights_status']}`",
            f"- review_status: `{REVIEW_STATUS}`",
        ]
    ) + "\n"


def preformal_research_start_index_payload(
    index: int,
    relative_dir: Path,
    row: dict[str, str],
    source_row: dict[str, str],
    visual_row: dict[str, str],
) -> dict[str, object]:
    return {
        "project_id": project_id(index),
        "record_type": "collection_preformal_research_start_index",
        "candidate_collection_object_id": row["candidate_collection_object_id"],
        "human_readable_files": [
            (relative_dir / "16_preformal-research-start-check.md").as_posix(),
            (relative_dir / "06_human-collection-dossier.md").as_posix(),
            (relative_dir / "12_archaeological-context-review.md").as_posix(),
            (relative_dir / "14_human-research-readiness-review.md").as_posix(),
        ],
        "ai_support_files": [
            (relative_dir / "01_collection-object-packet.json").as_posix(),
            (relative_dir / "02_collection-source-index.csv").as_posix(),
            (relative_dir / "03_visual-asset-index.csv").as_posix(),
            (relative_dir / "17_preformal-research-start-index.json").as_posix(),
        ],
        "preformal_start_slots": [
            "open_object_page_visual_catalog_source_first",
            "review_archaeological_context_before_identity_claim",
            "keep_inscription_and_character_links_candidate_only",
            "check_rights_checksum_size_manifest_field_map",
            "record_bibliography_dispute_and_missing_items",
        ],
        "concrete_start_questions": [
            "which object page image route catalog reference and source row",
            "which findspot period batch pit or plate route remains pending",
            "which inscription or oracle-character relation is candidate only",
            "which rights checksum size manifest or field map is unresolved",
            "which bibliography proposer disagreement or citation is missing",
        ],
        "source_id": source_row["source_id"],
        "visual_entry_type": visual_row.get("visual_entry_type", ""),
        "rights_status": source_row["rights_status"],
        "claim_boundary": (
            "preformal opening check only; no confirmed collection object "
            "identity; no confirmed inscription identity; no transcription; "
            "no reading; no component assignment; no dating claim; no "
            "decipherment conclusion"
        ),
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
        wrapped_bullet(text)
        for text in [
            "Open 02_collection-source-index.csv and name the missing source row.",
            "Open 03_visual-asset-index.csv and name the image route status.",
            "Which accession, catalog, or object ID is only a source clue?",
            "Which findspot, period, batch, or plate provenance still needs checking?",
            "Which rights status or reuse risk must be rechecked before public use?",
            "Which inscription, glyph, or character link is only a candidate route?",
            "Record missing source, visual, rights, or context route type.",
            "打开 02_collection-source-index.csv，写明待补来源行。",
            "打开 03_visual-asset-index.csv，写明图像路线状态。",
            "哪些 accession、catalog 或 object ID 只是来源线索？",
            "需核对哪些出土地、时期、批次或图版？",
            "公开使用前还需复核哪些权利或风险？",
            "哪些卜辞、字形或单字关联只是候选路线？",
            "记录缺口属于来源、图像、权利还是上下文路线。",
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
- Transcription: pending source-page or catalog transcription check
- Decipherment: `not_applicable_preprocessing_only`
- Review status: `{REVIEW_STATUS}`

## Caution / 风险提示

{caution}
"""


def material_image_inspection_note_text(
    index: int,
    row: dict[str, str],
    visual_row: dict[str, str],
) -> str:
    """Return a bounded image-inspection record for reviewed local assets only."""
    observations = MATERIAL_IMAGE_OBSERVATIONS.get(
        row["candidate_collection_object_id"]
    )
    if not observations or not visual_row.get("asset_path"):
        return ""
    english_observations = "\n".join(
        wrapped_bullet(value) for value in observations["en"]
    )
    chinese_observations = "\n".join(
        wrapped_bullet(value) for value in observations["zh"]
    )
    source_title = row.get("object_title_en", "") or "catalog object"
    return f"""# Material Image Inspection Note / \u5b9e\u7269\u56fe\u50cf\u67e5\u9605\u8bb0\u5f55

Project ID: `{project_id(index)}`

Candidate collection object ID: `{row['candidate_collection_object_id']}`

## Evidence Opened / \u5df2\u6253\u5f00\u7684\u8bc1\u636e

- Catalog title / \u8457\u5f55\u6807\u9898: `{source_title}`
- Asset ID: `{visual_row['asset_id']}`
- Local asset path / \u672c\u5730\u8d44\u4ea7\u8def\u5f84: open `03_visual-asset-index.csv`.
- Source image route / \u6e90\u56fe\u8def\u7ebf: open `03_visual-asset-index.csv`.
- Rights status / \u6743\u5229\u72b6\u6001: `{visual_row['rights_status']}`

## Direct Visual Record / \u76f4\u89c2\u8bb0\u5f55

English:
This bounded note records what is directly visible in the local review image.
It separates the photographed surface from any unverified inscription,
character, component, or reading claim.

{english_observations}

\u7b80\u4f53\u4e2d\u6587\uff1a
\u672c\u8bb0\u5f55\u53ea\u4e66\u660e\u672c\u5730\u590d\u6838\u56fe\u50cf\u4e2d\u76f4\u63a5\u53ef\u89c1\u7684\u60c5\u51b5\uff0c\n\u4e0e\u5c1a\u672a\u590d\u6838\u7684\u535c\u8f9e\u3001\u5355\u5b57\u3001\u6784\u4ef6\u6216\u91ca\u8bfb\u4e3b\u5f20\u5206\u5f00\u8bb0\u5f55\u3002

{chinese_observations}

## Next Evidence To Open / \u4e0b\u4e00\u6b65\u5f85\u67e5\u8bc1\u636e

- Open the source catalog page for additional views, object description, and
  any accession-linked documentation.
- Locate a publication plate or rubbing before transcribing any visible mark.
- Check whether a full-text, findspot, period, batch, or collection history
  record is available for this exact accession route.
- \u5f00\u542f\u6765\u6e90\u8457\u5f55\u9875\uff0c\u67e5\u770b\u5176\u4ed6\u89c6\u89d2\u3001\u5668\u7269\u8bf4\u660e\u548c\u767b\u5f55\u6587\u4ef6\u3002
- \u5728\u8f6c\u5199\u4efb\u4f55\u53ef\u89c1\u523b\u5212\u524d\uff0c\u5148\u67e5\u627e\u51fa\u7248\u56fe\u7248\u6216\u62d3\u7247\u3002
- \u6309\u8be5\u767b\u5f55\u8def\u7ebf\u67e5\u627e\u5168\u6587\u3001\u51fa\u571f\u5730\u3001\u65f6\u671f\u3001\u6279\u6b21\u6216\u9986\u85cf\u5386\u53f2\u8bb0\u5f55\u3002

## Boundary / \u8fb9\u754c

This is an image inspection record, not a transcription, character
identification, component analysis, formal reading, or decipherment conclusion.
\u672c\u8bb0\u5f55\u662f\u56fe\u50cf\u67e5\u9605\u8bb0\u5f55\uff0c\u4e0d\u662f\u91ca\u6587\u3001\u5355\u5b57\u8ba4\u5b9a\u3001\u6784\u4ef6\u5206\u6790\u3001\n\u6b63\u5f0f\u91ca\u8bfb\u6216\u7834\u8bd1\u7ed3\u8bba\u3002
"""


def build_outputs(root: Path) -> dict[str, dict[str, object]]:
    asset_by_related, technical_by_asset, visual_by_asset = load_assets(root)
    source_routes, source_route_paths = load_source_routes(root)
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
        route_key = (src_row["source_id"], src_row["evidence_download_id"])
        source_route = source_routes.get(route_key, {})
        source_route_path = source_route_paths.get(route_key, "")
        metadata = selected_metadata(row)
        fact_rows = collection_provenance_fact_rows(row, metadata, src_row, vis_row)
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
            "provenance_evidence_dossier_text": collection_provenance_evidence_dossier_text(
                index,
                row,
                metadata,
                src_row,
                vis_row,
                source_route,
                source_route_path,
            ),
            "provenance_evidence_index": collection_provenance_evidence_index_payload(
                index,
                relative_dir,
                row,
                src_row,
                vis_row,
                source_route,
                source_route_path,
            ),
            "collection_provenance_fact_matrix_text": (
                collection_provenance_fact_matrix_text(
                    index,
                    row,
                    fact_rows,
                )
            ),
            "collection_provenance_fact_matrix_index": (
                collection_provenance_fact_matrix_index_payload(
                    index,
                    relative_dir,
                    row,
                    src_row,
                    vis_row,
                    fact_rows,
                )
            ),
            "archaeological_context_review_text": archaeological_context_review_text(
                index,
                row,
                metadata,
                src_row,
                vis_row,
            ),
            "archaeological_context_index": archaeological_context_index_payload(
                index,
                relative_dir,
                row,
                src_row,
                vis_row,
            ),
            "human_research_readiness_review_text": (
                human_research_readiness_review_text(
                    index,
                    row,
                    metadata,
                    src_row,
                    vis_row,
                )
            ),
            "human_research_readiness_index": human_research_readiness_index_payload(
                index,
                relative_dir,
                row,
                src_row,
                vis_row,
            ),
            "preformal_research_start_check_text": (
                preformal_research_start_check_text(
                    index,
                    row,
                    metadata,
                    src_row,
                    vis_row,
                )
            ),
            "preformal_research_start_index": preformal_research_start_index_payload(
                index,
                relative_dir,
                row,
                src_row,
                vis_row,
            ),
            "material_image_inspection_note_text": material_image_inspection_note_text(
                index,
                row,
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
                "collection_provenance_evidence_dossier_path": (
                    relative_dir / "08_collection-provenance-evidence-dossier.md"
                ).as_posix(),
                "collection_provenance_evidence_index_path": (
                    relative_dir / "09_collection-provenance-evidence-index.json"
                ).as_posix(),
                "collection_provenance_fact_matrix_path": (
                    relative_dir / "10_collection-provenance-fact-matrix.md"
                ).as_posix(),
                "collection_provenance_fact_matrix_index_path": (
                    relative_dir / "11_collection-provenance-fact-matrix-index.json"
                ).as_posix(),
                "archaeological_context_review_path": (
                    relative_dir / "12_archaeological-context-review.md"
                ).as_posix(),
                "archaeological_context_index_path": (
                    relative_dir / "13_archaeological-context-index.json"
                ).as_posix(),
                "human_research_readiness_review_path": (
                    relative_dir / "14_human-research-readiness-review.md"
                ).as_posix(),
                "human_research_readiness_index_path": (
                    relative_dir / "15_human-research-readiness-index.json"
                ).as_posix(),
                "preformal_research_start_check_path": (
                    relative_dir / "16_preformal-research-start-check.md"
                ).as_posix(),
                "preformal_research_start_index_path": (
                    relative_dir / "17_preformal-research-start-index.json"
                ).as_posix(),
                "material_image_inspection_note_path": (
                    (relative_dir / "18_material-image-inspection-note.md").as_posix()
                    if asset_row
                    else ""
                ),
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
        (directory / "08_collection-provenance-evidence-dossier.md").write_text(
            str(output["provenance_evidence_dossier_text"]),
            encoding="utf-8",
            newline="\n",
        )
        (directory / "09_collection-provenance-evidence-index.json").write_text(
            json.dumps(
                output["provenance_evidence_index"],
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (directory / "10_collection-provenance-fact-matrix.md").write_text(
            str(output["collection_provenance_fact_matrix_text"]),
            encoding="utf-8",
            newline="\n",
        )
        (directory / "11_collection-provenance-fact-matrix-index.json").write_text(
            json.dumps(
                output["collection_provenance_fact_matrix_index"],
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (directory / "12_archaeological-context-review.md").write_text(
            str(output["archaeological_context_review_text"]),
            encoding="utf-8",
            newline="\n",
        )
        (directory / "13_archaeological-context-index.json").write_text(
            json.dumps(
                output["archaeological_context_index"],
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (directory / "14_human-research-readiness-review.md").write_text(
            str(output["human_research_readiness_review_text"]),
            encoding="utf-8",
            newline="\n",
        )
        (directory / "15_human-research-readiness-index.json").write_text(
            json.dumps(
                output["human_research_readiness_index"],
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (directory / "16_preformal-research-start-check.md").write_text(
            str(output["preformal_research_start_check_text"]),
            encoding="utf-8",
            newline="\n",
        )
        (directory / "17_preformal-research-start-index.json").write_text(
            json.dumps(
                output["preformal_research_start_index"],
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        material_note = str(output["material_image_inspection_note_text"])
        material_note_path = directory / "18_material-image-inspection-note.md"
        if material_note:
            material_note_path.write_text(material_note, encoding="utf-8", newline="\n")
        elif material_note_path.exists():
            material_note_path.unlink()
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
